import os

from google import genai
from google.genai import types
from pydantic import ValidationError

from models import Enquiry

MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

SYSTEM_PROMPT = """You classify customer enquiries for a fitness studio.
Return JSON only. Do NOT answer the customer and do NOT state any prices or times.
- intent: pricing | availability | pricing_and_availability | other
- details.packages: which packages the customer asks about:
  "single" (single session), "five" (5 sessions), "twelve" (12 sessions). Empty list if none named.
- details.asks_saturday: true if they ask about Saturday slots.
- details.unknown_topics: anything asked that is NOT package pricing or Saturday availability
  (e.g. bookings, payments, discounts, other days, other packages like 20 sessions).
- requires_human_approval: always true."""


class AIUnavailable(Exception):
    """Gemini failed, timed out, or no key configured."""


class InvalidAIOutput(Exception):
    """Gemini returned JSON that does not match the Pydantic model."""


def _call_gemini(message: str) -> str:
    """Raw call. Returns the JSON text. Tests mock this function."""
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise AIUnavailable("GEMINI_API_KEY is not set")
    try:
        client = genai.Client(
            api_key=key, http_options=types.HttpOptions(timeout=15000)
        )
        response = client.models.generate_content(
            model=os.getenv("GEMINI_MODEL", MODEL),
            contents=message,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                response_mime_type="application/json",
                response_schema=Enquiry,
                temperature=0,
            ),
        )
        return response.text or ""
    except Exception as exc:  # network, quota, timeout, auth
        raise AIUnavailable(str(exc)) from exc


def classify(message: str) -> Enquiry:
    raw = _call_gemini(message)
    try:
        return Enquiry.model_validate_json(raw)
    except ValidationError as exc:
        raise InvalidAIOutput(str(exc)) from exc
