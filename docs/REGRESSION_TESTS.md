# Regression tests

All tests are automated in `tests/` (pytest). Gemini is mocked, so no API key or paid call is needed.
Run: `pytest -v`
Last run: 2026-11-20, `12 passed` (T3 has three parametrised cases; T9 and T9b are in `tests/test_menu.py`).

| ID | Requirement | Input / precondition | Steps | Expected result | Actual result | Result |
|---|---|---|---|---|---|---|
| T1 | FR-03, FR-04, FR-06 | Mock returns `pricing_and_availability`, package `twelve`, asks Saturday. Staff input `y`. | 1. Mock `llm._call_gemini`. 2. Call `process("12-session price and Saturday slots?")`. 3. Read printed draft and the log. | Draft has R1,680, 09:00 available, 10:00 full, 11:00 available and no escalation phrase. Logged `sent`. | As expected. | Pass |
| T2 | FR-04 | Mock returns intent `other`, unknown topic "20 sessions". Staff input `n`. | 1. Mock Gemini. 2. Call `process("How much is the 20-session pack?")`. 3. Read the log entry. | Reply is exactly `I'll check with the owner and come back to you.`, contains no digits, `escalation: true`. | As expected. | Pass |
| T3 | FR-02, FR-07 | Mock returns (a) non-JSON text, (b) JSON missing fields, (c) JSON with an invalid intent value. | 1. Mock Gemini with each bad value. 2. Call `process("price?")` with an approval callback that fails the test if called. 3. Read the log. | Status `error_invalid_ai_output`, no approval prompt, no `sent` entry. | As expected for all three. | Pass |
| T4 | FR-07 | `GEMINI_API_KEY` set to a fake value; `genai.Client` raises `TimeoutError`. | 1. Patch `genai.Client` to raise. 2. Call `process("price?")` with a failing approval callback. 3. Read the log. | Status `error_ai_unavailable`, no approval prompt, no `sent` entry. | As expected. | Pass |
| T5 | FR-05, FR-06 | Mock returns a normal enquiry. Staff input `n`. | 1. Mock Gemini. 2. Call `process("12-session price?")`. 3. Read the log. | Status `rejected_by_staff`; no `sent` entry. | As expected. | Pass |
| T6 | FR-04, FR-06 | Mock returns a missing-fact enquiry. Staff input `y`. | 1. Mock Gemini. 2. Call `process("20-session pack?")`. 3. Read the log. | Status `sent` with `escalation: true` (staff approved the escalation message). | As expected. | Pass |
| T7 | FR-05 | Mock returns `requires_human_approval: false`. | 1. Mock Gemini. 2. Call `process()` with a callback that records prompts. 3. Check the callback was called. | Approval prompt is still shown. | As expected. | Pass |
| T8 | FR-05 | Staff type `maybe`, then empty, then `n`. | 1. Mock Gemini. 2. Call `process()` with those answers in order. 3. Read the status. | Prompt repeats until y/n; final status `rejected_by_staff`. | As expected. | Pass |
| T9 | FR-01, FR-03 | Real `data/studio_data.json`. | 1. Call `build_menu(load_data())`. 2. Call `resolve_choice` with `"1"`, `"99"` and free text. | Menu lists the data-file packages and Saturday; valid numbers map to preset questions; anything else is treated as free text. | As expected. | Pass |
| T9b | FR-03 | Data with no packages and no Saturday slots. | 1. Call `build_menu` on the empty data. | "Saturday availability" is not offered. | As expected. | Pass |

Not automated: a live call to Gemini with a real key (manual check; see `RAPLH_LOG.md` Entry 2).
