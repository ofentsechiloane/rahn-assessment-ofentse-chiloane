# RAPLH log

Maximum attempts per fix: **2**. If the same fix fails twice, stop and escalate to a mentor (playbook rule).

## Entry 1: GENUINE record
- **Task / expected:** Check the repo against the brief, then complete the empty modules (`approval.py`, `drafter.py`, `status_log.py`, `main.py`), tests and docs so the full flow works with Gemini mocked.
- **Prompt summary (Claude, claude.ai):** Gave Claude the assessment PDF, the playbook PDF and my repo zip; asked it to check I was still aligned with the brief and to give me code and commands.
- **Files changed:** `approval.py`, `drafter.py`, `status_log.py`, `main.py`, `tests/test_enquiry.py`, `docs/SRS.md`, `docs/REGRESSION_TESTS.md`, `docs/RAPLH_LOG.md`, `README.md`.
- **Test run and result:** `pytest -v` gave `10 passed`. `python main.py` with no key logged `error_ai_unavailable` and no `sent`.
- **Corrected:** `approval.py` contained `//` (invalid Python); replaced. README setup changed from PowerShell to bash. A weak assertion in T2 (string trick) was replaced with a "no digits" check.
- **Approval decision:** Accepted after review. I ran pytest -v (10 passed) and a run with no key (logged error_ai_unavailable, nothing sent). I did not accept the first version as is: the invalid // in approval.py, the PowerShell README steps and the weak T2 assertion were corrected first.

## Entry 2: GENUINE record
- **Task / expected:** Run the program against the real Gemini API and see it classify an enquiry, then draft and log it.
- **What happened (from `status_log.json`):** 17 Nov, about 10:03 to 10:06 (SAST): three live runs worked and were logged `sent` after `y`. 18 Nov, about 10:39 to 10:42: five live runs failed with 503, 504 and a read timeout; each was logged `error_ai_unavailable`.
- **Prompt summary (AI tool):** Asked Claude why Gemini was erroring and whether it was my code or the service
- **Files changed:** `llm.py` (commit 0a34a95, 18 Nov): default model changed from `gemini-2.5-flash` to `gemini-3.8-flash`, now read from `GEMINI_MODEL` in `.env`.
- **Test run and result:** `pytest -v`: 12 passed (mocked). Live run: on 20 Nov (about 12:27 to 12:31 SAST) failed: 503 UNAVAILABLE on gemini-3.8-flash and gemini-3.7-flash, and 404 on gemini-2.5-flash (no longer available to new users). No successful live run today.
- **Corrected:** The errors were Gemini overload, not a bug in my code. `gemini-2.5-flash` now returns 404, so `gemini-3.8-flash` is the correct model. In every failure, nothing was recorded as `sent`.
- **Approval decision:** Accepted the llm.py change after reading the diff. I did not add automatic retries: the failure path handled every error safely and retries are beyond the minimum scope, so I listed it under What doesn't work yet.

## Q1. Stopping an AI agent changing unrelated files or exposing the API key
- Give each task an explicit list of files the agent may touch, and review `git diff` before every commit; revert anything outside the list.
- Keep the key only in `.env` (git-ignored), commit `.env.example`, and never paste the key into prompts. Check `git status` and `git diff --staged` for `.env` before pushing; run tests with no key set.

## Q2. Stopping the loop when the agent repeats the same failed fix
- Set a hard cap (2 attempts per fix, as in the playbook). If the same fix fails twice, stop.
- Read the actual failure myself, change the approach (smaller task, different test, or new prompt with the error text), and escalate to a mentor if it still fails.
