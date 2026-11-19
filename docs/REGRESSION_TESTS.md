# Regression tests

All tests are automated in `tests/test_enquiry.py` (pytest). Gemini is mocked, so no API key or paid call is needed.
Run: `pytest -v`
Last run: 2026-11-17, `10 passed` (T3 has three parametrised cases). Re-run on your own machine before submitting and update the Actual/Result columns if anything differs.

| ID | Requirement | Precondition / input | Steps | Expected result | Actual result | Result |
|---|---|---|---|---|---|---|
| T1 | FR-03, FR-04, FR-06 | Mock returns pricing_and_availability, package `twelve`, asks Saturday. Staff answer `y`. | Run `process()` with "12-session price and Saturday slots?" | Draft has R1,680, 09:00 available, 10:00 full, 11:00 available, no escalation phrase. Logged `sent`. | As expected. | Pass |
| T2 | FR-04 | Mock returns intent `other`, unknown topic "20 sessions". Staff answer `n`. | Run `process()` with "How much is the 20-session pack?" | Reply is exactly `I'll check with the owner and come back to you.`, no digits, `escalation: true`. | As expected. | Pass |
| T3 | FR-02, FR-07 | Mock returns (a) non-JSON text, (b) JSON missing fields, (c) JSON with an invalid intent value. | Run `process()` with each; approval callback fails the test if called. | Status `error_invalid_ai_output`, no approval prompt, no `sent` entry. | As expected for all three. | Pass |
| T4 | FR-07 | `GEMINI_API_KEY` set to a fake value; `genai.Client` raises `TimeoutError`. | Run `process()` with "price?" | Status `error_ai_unavailable`, no approval prompt, no `sent` entry. | As expected. | Pass |
| T5 | FR-05, FR-06 | Mock returns a normal enquiry. Staff answer `n`. | Run `process()` | Status `rejected_by_staff`; no `sent` entry. | As expected. | Pass |
| T6 | FR-04, FR-06 | Mock returns a missing-fact enquiry. Staff answer `y`. | Run `process()` | Status `sent` with `escalation: true` (staff approved the escalation message). | As expected. | Pass |
| T7 | FR-05 | Mock returns `requires_human_approval: false`. | Run `process()`; record whether the prompt was shown. | Approval prompt is still shown. | As expected. | Pass |
| T8 | FR-05 | Staff type `maybe`, then empty, then `n`. | Run `process()` | Prompt repeats until y/n; final status `rejected_by_staff`. | As expected. | Pass |

Not automated: a live call to Gemini with a real key (manual check, see RAPLH_LOG).
