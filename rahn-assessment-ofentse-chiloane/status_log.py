import json
from datetime import datetime, timezone
from pathlib import Path

LOG_PATH = Path(__file__).parent / "status_log.json"

VALID_STATUSES = {
    "sent",
    "rejected_by_staff",
    "error_invalid_ai_output",
    "error_ai_unavailable",
}


def record(status, message, reply=None, escalation=False, detail=None, path=None):
    """Append one entry. 'sent' is only ever passed in by main.py after staff say y."""
    if status not in VALID_STATUSES:
        raise ValueError(f"Unknown status: {status}")
    path = Path(path or LOG_PATH)
    entries = []
    if path.exists():
        try:
            entries = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            path.rename(path.with_suffix(".corrupt.json"))  # keep it, start fresh
    entries.append(
        {
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "customer_message": message,
            "status": status,
            "reply": reply,
            "escalation": escalation,
            "detail": detail,
        }
    )
    path.write_text(json.dumps(entries, indent=2, ensure_ascii=False), encoding="utf-8")
