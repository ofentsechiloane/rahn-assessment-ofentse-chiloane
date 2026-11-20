# RAPLH log

Maximum attempts per fix: **2**. If the same fix fails twice, stop and escalate to a mentor (playbook rule).

## Entry 1: GENUINE record
- **Task / expected:** Check the repo against the brief, then complete the empty modules (`approval.py`, `drafter.py`, `status_log.py`, `main.py`), tests and docs so the full flow works with Gemini mocked.
- **Prompt summary (Claude, claude.ai):** Gave Claude the assessment PDF, the playbook PDF and my repo zip; asked it to check I was still aligned with the brief and to give me code and commands.
- **Files changed:** `approval.py`, `drafter.py`, `status_log.py`, `main.py`, `tests/test_enquiry.py`, `docs/SRS.md`, `docs/REGRESSION_TESTS.md`, `docs/RAPLH_LOG.md`, `README.md`.
- **Test run and result:** `pytest -v` gave `10 passed`. `python main.py` with no key logged `error_ai_unavailable` and no `sent`.
- **Corrected:** `approval.py` contained `//` (invalid Python); replaced. README setup changed from PowerShell to bash. A weak assertion in T2 (string trick) was replaced with a "no digits" check.
- **Approval decision:** TODO (mine to write after I read the diff).

## Entry 2: TODO, must be a GENUINE record
Fill from a real iteration of mine, for example the first live run with my Gemini key (`python main.py`), what failed or surprised me, the prompt I used to fix it, the test I re-ran, and my decision. If I only have illustrative material, label it **ILLUSTRATIVE** instead.

## Q1. Stopping an AI agent changing unrelated files or exposing the API key
- Give each task an explicit list of files the agent may touch, and review `git diff` before every commit; revert anything outside the list.
- Keep the key only in `.env` (git-ignored), commit `.env.example`, and never paste the key into prompts. Check `git status` and `git diff --staged` for `.env` before pushing; run tests with no key set.

## Q2. Stopping the loop when the agent repeats the same failed fix
- Set a hard cap (2 attempts per fix, as in the playbook). If the same fix fails twice, stop.
- Read the actual failure myself, change the approach (smaller task, different test, or new prompt with the error text), and escalate to a mentor if it still fails.
