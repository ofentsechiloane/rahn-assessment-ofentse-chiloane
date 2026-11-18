import json

import pytest

import llm
from drafter import ESCALATION_PHRASE
from main import process

NORMAL = {
    "intent": "pricing_and_availability",
    "details": {"packages": ["twelve"], "asks_saturday": True, "unknown_topics": []},
    "requires_human_approval": True,
}
MISSING = {
    "intent": "other",
    "details": {"packages": [], "asks_saturday": False, "unknown_topics": ["20 sessions"]},
    "requires_human_approval": True,
}


@pytest.fixture
def log(tmp_path):
    return tmp_path / "status_log.json"


def mock_ai(monkeypatch, payload):
    raw = payload if isinstance(payload, str) else json.dumps(payload)
    monkeypatch.setattr(llm, "_call_gemini", lambda message: raw)


def entries(log):
    return json.loads(log.read_text(encoding="utf-8"))


def test_t1_normal_enquiry_staff_yes(monkeypatch, log, capsys):  # FR-03, FR-04, FR-06
    mock_ai(monkeypatch, NORMAL)
    status = process("12-session price and Saturday slots?", input_fn=lambda _: "y", log_path=log)
    out = capsys.readouterr().out
    assert status == "sent"
    for fact in ("R1,680", "09:00 available", "10:00 full", "11:00 available"):
        assert fact in out
    assert ESCALATION_PHRASE not in out
    assert entries(log)[0]["status"] == "sent"


def test_t2_missing_fact_uses_exact_phrase(monkeypatch, log, capsys):  # FR-04
    mock_ai(monkeypatch, MISSING)
    process("How much is the 20-session pack?", input_fn=lambda _: "n", log_path=log)
    entry = entries(log)[0]
    assert entry["reply"] == ESCALATION_PHRASE
    assert entry["escalation"] is True
    assert not any(c.isdigit() for c in entry["reply"])  # no invented price


@pytest.mark.parametrize("bad", ["not json at all", '{"intent": "pricing"}', '{"intent": "banana"}'])
def test_t3_invalid_json_never_sent(monkeypatch, log, bad):  # FR-02, FR-07
    mock_ai(monkeypatch, bad)
    status = process("price?", input_fn=lambda _: pytest.fail("must not ask approval"), log_path=log)
    assert status == "error_invalid_ai_output"
    assert all(e["status"] != "sent" for e in entries(log))


def test_t4_ai_service_failure_never_sent(monkeypatch, log):  # FR-07
    monkeypatch.setenv("GEMINI_API_KEY", "fake-key")

    class Boom:
        def __init__(self, *a, **k):
            raise TimeoutError("simulated timeout")

    monkeypatch.setattr(llm.genai, "Client", Boom)
    status = process("price?", input_fn=lambda _: pytest.fail("must not ask approval"), log_path=log)
    assert status == "error_ai_unavailable"
    assert all(e["status"] != "sent" for e in entries(log))


def test_t5_staff_no_never_sent(monkeypatch, log):  # FR-05, FR-06
    mock_ai(monkeypatch, NORMAL)
    status = process("12-session price?", input_fn=lambda _: "n", log_path=log)
    assert status == "rejected_by_staff"
    assert entries(log)[0]["status"] == "rejected_by_staff"


def test_t6_staff_yes_on_escalation_is_sent_and_flagged(monkeypatch, log):  # FR-04, FR-06
    mock_ai(monkeypatch, MISSING)
    status = process("20-session pack?", input_fn=lambda _: "y", log_path=log)
    entry = entries(log)[0]
    assert status == "sent" and entry["escalation"] is True


def test_t7_model_cannot_skip_approval(monkeypatch, log):  # FR-05
    mock_ai(monkeypatch, {**NORMAL, "requires_human_approval": False})
    asked = []
    process("12-session price?", input_fn=lambda p: asked.append(p) or "n", log_path=log)
    assert asked, "approval prompt must be shown even if the model says it is not needed"


def test_t8_unrecognised_answer_reprompts(monkeypatch, log):  # FR-05
    mock_ai(monkeypatch, NORMAL)
    answers = iter(["maybe", "", "n"])
    status = process("12-session price?", input_fn=lambda _: next(answers), log_path=log)
    assert status == "rejected_by_staff"
