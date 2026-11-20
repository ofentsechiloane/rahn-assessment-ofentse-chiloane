## Entry 2: GENUINE record  (DRAFT: edit every [CONFIRM] so it matches what you really did)
- **Task / expected:** Run the program against the real Gemini API for the first time and see it classify an enquiry, then draft and log it. [CONFIRM]
- **What actually happened (from `status_log.json`, real timestamps):**
    - 17 Nov, about 10:03 to 10:06 (SAST): three live runs worked (Saturday slots, single-session price, Saturday slots again). Each was approved with `y` and logged `sent`.
    - 18 Nov, about 10:39 to 10:42 (SAST): five live runs failed with `503 UNAVAILABLE` ("high demand"), `504 DEADLINE_EXCEEDED`, and "The read operation timed out". Each was logged `error_ai_unavailable` and nothing was recorded as `sent`.
- **Prompt summary (AI tool):** [CONFIRM: what you asked your AI tool, e.g. why Gemini was erroring and whether it was my code or the service.]
- **Files changed:** `llm.py` (commit 0a34a95 on 18 Nov: default model changed from `gemini-2.5-flash` to `gemini-3.8-flash`, and the model is now read from `GEMINI_MODEL` in `.env`). I also used a throwaway script, `check.py`, to test the key and model outside the app, then deleted it. [CONFIRM]
- **Test run and result:** `pytest -v` after the change: `12 passed` (mocked). Live run: [CONFIRM: did the errors stop? what did you do next?]
- **Corrected:** [CONFIRM: e.g. you learned the errors were Gemini overload, not a bug; the failure path behaved as designed.]
- **Approval decision:** [CONFIRM: yours to write, e.g. accepted the llm.py change after reading the diff; did not add retries because it is out of scope.]