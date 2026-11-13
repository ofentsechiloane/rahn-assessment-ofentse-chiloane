# FitDesk Enquiry Assistant

**Hours actually spent:** TODO (fill in at the end)

A command-line assistant for a Hermanus fitness studio. It reads a customer
enquiry, asks Gemini to classify it into structured JSON, looks up facts in a
local data file, drafts a reply, and waits for staff approval before recording
anything as sent. It takes no bookings or payments.

## How it works

1. Staff type a customer message at the command line.
2. Gemini returns JSON (`intent`, `details`, `requires_human_approval`), checked against a Pydantic model.
3. Python looks up prices and Saturday slots in `data/studio_data.json`.
4. Python builds the reply from the data only. If a fact is missing, the reply is exactly:
   `I'll check with the owner and come back to you.`
5. The draft is printed and staff are asked `Send? (y/n)`.
6. The outcome is appended to `status_log.json`.

Gemini never writes the reply, so it cannot invent prices or availability.
Approval is always asked in code, whatever the model returns.

## Setup (Windows, PowerShell)

```powershell
git clone https://github.com/<your-username>/rahn-assessment-ofentse-chiloane.git
cd rahn-assessment-ofentse-chiloane
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

Get a free key at https://aistudio.google.com/ and put it in `.env`:

```
GEMINI_API_KEY=your_key_here
```

## Run

```powershell
python main.py
```

## Test

Tests mock Gemini, so they need no API key and make no paid calls.

```powershell
pytest
```

## Status values

`sent`, `rejected_by_staff`, `error_invalid_ai_output`, `error_ai_unavailable`, `escalation_sent`

## Docs

- `docs/SRS.md`: requirements
- `docs/REGRESSION_TESTS.md`: tests mapped to requirements
- `docs/RAPLH_LOG.md`: AI-assisted build log

## AI use

TODO: which AI tools I used, and for what.

## What doesn't work yet

TODO: be specific.

## Working style

TODO: four answers, 80 to 150 words each, written by me without AI.