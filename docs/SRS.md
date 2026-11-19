# SRS: FitDesk Enquiry Assistant (CLI)

## 1. Business objective
Cut the time staff spend answering package and Saturday-availability enquiries, without ever quoting a wrong price or availability. Staff stay in control: nothing is recorded as sent without their approval.

## 2. Stakeholders
- **Studio owner**: wants time back and no invented prices or promises.
- **Staff member**: types the enquiry, reviews the draft, approves or rejects.
- **Customer**: receives accurate package and slot information.
- **RAHN**: builds and maintains the assistant to the playbook rules.

## 3. Scope
**In scope:** CLI input of one enquiry; Gemini classification to JSON; lookup in the local data file; drafted reply; staff approval; local status log.
**Out of scope:** WhatsApp, bookings, payments, calendar, reminders, editing drafts, multiple users, real sending of messages.

## 4. Functional requirements
- **FR-01** The system accepts a customer message typed at the command line.
- **FR-02** The system sends the message to Gemini and receives JSON containing `intent`, `details` and `requires_human_approval`, validated by a Pydantic model.
- **FR-03** The system looks up package prices and Saturday slots only in `data/studio_data.json`.
- **FR-04** The reply is built only from data-file facts. Any part not in the file is replaced by exactly: `I'll check with the owner and come back to you.`
- **FR-05** The system prints the draft and asks `Send? (y/n)` for every enquiry, even if the model says approval is not required.
- **FR-06** Every outcome is appended to `status_log.json`. Status `sent` is written only after staff answer `y`.
- **FR-07** If Gemini fails, times out or returns invalid JSON, no draft is shown, nothing is `sent`, and an error status is logged.

## 5. Non-functional requirements
- **NFR-01 Security:** the API key lives only in `.env` (git-ignored); `.env.example` is committed instead.
- **NFR-02 Reliability:** Gemini calls time out after 15 s; every failure path ends cleanly with a logged status, never a crash or a false `sent`.
- **NFR-03 Cost:** free tools only; one Gemini call per enquiry; automated tests mock Gemini (zero calls, no key).

## 6. Data inputs and outputs
- **Inputs:** customer message (text); `data/studio_data.json` (3 packages, 3 Saturday slots); `GEMINI_API_KEY`.
- **Outputs:** printed draft reply; `status_log.json` entries (timestamp, message, status, reply, escalation flag, detail).

## 7. Approval and failure rules
- Staff `n` (or anything other than `y`/`n`, re-prompted; EOF counts as `n`): status `rejected_by_staff`.
- Fact missing: draft contains the exact escalation phrase; it is logged `sent` only if staff answer `y` (flagged `escalation: true`).
- Gemini error/timeout/no key: `error_ai_unavailable`. Invalid JSON or schema mismatch: `error_invalid_ai_output`. No approval prompt in either case.

## 8. Acceptance criteria
- **AC-01** Given "12-session price and Saturday slots", the draft contains R1,680, 09:00 available, 10:00 full, 11:00 available, and no escalation phrase.
- **AC-02** Given a question about a package not in the data file, the reply is exactly the escalation phrase and contains no digits.
- **AC-03** Given invalid JSON (3 variants), zero `sent` entries exist and no approval prompt is shown.
- **AC-04** Given a Gemini exception, status is `error_ai_unavailable` and no `sent` entry exists.
- **AC-05** Given `n`, status is `rejected_by_staff`; given `y`, status is `sent`.
- **AC-06** With `requires_human_approval: false` from the model, the approval prompt is still shown.
- **AC-07** All automated tests pass with no API key set.

## 9. Ambiguities and assumptions
| # | Unclear in the brief | Question for the owner | Assumption made |
|---|---|---|---|
| 1 | Saturday data has no date | Is the file for this Saturday only, or every Saturday? | It is the current weekly file; the reply lists the slots as given and states no dates. |
| 2 | Customer asks "how much?" without naming a package | List all prices or ask which? | List all packages from the data file. |
| 3 | Enquiry mixes known and unknown topics | Answer the known part or escalate everything? | Answer known facts, then append the escalation phrase. |
| 4 | "Sent" for an escalation message | Does approving it count as sent? | Yes: logged `sent` with `escalation: true`, only after `y`. |
| 5 | Slot status wording | Is "Full" the only unavailable state? | Slot statuses are repeated exactly as in the file. |
