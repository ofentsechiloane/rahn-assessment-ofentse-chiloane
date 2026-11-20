# FitDesk Enquiry Assistant

**Hours actually spent:** TODO (fill in honestly at the end)

A command-line assistant for a Hermanus fitness studio. It reads a customer enquiry, asks Gemini to classify it into structured JSON, looks up facts in a local data file, drafts a reply, and waits for staff approval before recording anything as sent. It takes no bookings or payments, and nothing is actually sent anywhere.

## How it works

1. Staff type a customer message at the command line.
2. Gemini returns JSON (`intent`, `details`, `requires_human_approval`), checked against a Pydantic model.
3. Python looks up prices and Saturday slots in `data/studio_data.json`.
4. Python builds the reply from the data only. Any missing fact becomes exactly: `I'll check with the owner and come back to you.`
5. The draft is printed and staff are asked `Send? (y/n)`.
6. The outcome is appended to `status_log.json`.

Gemini only classifies; it never writes the reply, so it cannot invent prices or availability. Approval is always asked in code, whatever the model returns.

## Setup (Linux / macOS, bash)

```bash
git clone https://github.com/ofentsechiloane/rahn-assessment-ofentse-chiloane.git
cd rahn-assessment-ofentse-chiloane
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Get a free key at https://aistudio.google.com/ and put it in `.env`:

```
GEMINI_API_KEY=your_key_here
```

## Run

```bash
python main.py
```

Example message: `How much is the 12-session pack and do you have Saturday slots?`

## Test

Tests mock Gemini, so they need no API key and make no paid calls.

```bash
pytest -v
```

## Status values

`sent`, `rejected_by_staff`, `error_invalid_ai_output`, `error_ai_unavailable`. An approved escalation message is logged as `sent` with `escalation: true`.

## Docs

- `docs/SRS.md`: requirements
- `docs/REGRESSION_TESTS.md`: tests mapped to requirements
- `docs/RAPLH_LOG.md`: AI-assisted build log

## AI use

- Claude (claude.ai): checked my repo against the brief, wrote the drafter/approval/status-log/main modules, the pytest tests, and first drafts of the SRS, regression test doc and RAPLH log. I reviewed and ran everything.
- TODO: add any other tool I used (e.g. IDE assistant) and what for.

## What doesn't work yet

- Live Gemini call is only checked manually; automated tests mock it.
- One message per run; no loop for several enquiries.
- Saturday slots carry no dates, so replies cannot say which Saturday.
- If Gemini mislabels an unsupported request as a normal pricing enquiry, the reply only contains data-file facts, but it may skip the escalation phrase.
- `status_log.json` is a plain file with no locking (one user at a time).
- No real sending, bookings or payments (out of scope by design).

## Working style

TODO: four answers, 80 to 150 words each, written by me without AI.
