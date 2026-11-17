from dataclasses import dataclass

from models import Enquiry

ESCALATION_PHRASE = "I'll check with the owner and come back to you."


@dataclass
class Draft:
    text: str
    escalation: bool  # True if any part of the reply needed the escalation phrase


def _rand(amount: int) -> str:
    return f"R{amount:,}"


def draft_reply(enquiry: Enquiry, data: dict) -> Draft:
    """Build the reply from the data file only. Never guesses."""
    packages = data.get("packages", {})
    slots = data.get("saturday_slots", {})
    lines: list[str] = []
    escalate = False

    wanted = list(dict.fromkeys(enquiry.details.packages))  # de-duplicate, keep order
    # Asked about price but named no package: list every package in the data file.
    if not wanted and enquiry.intent in ("pricing", "pricing_and_availability"):
        wanted = list(packages)

    for key in wanted:
        pkg = packages.get(key)
        if pkg is None:
            escalate = True
            continue
        lines.append(f"- {pkg['label']}: {_rand(pkg['price_zar'])}")

    if enquiry.details.asks_saturday:
        if slots:
            text = ", ".join(f"{t} {s}" for t, s in sorted(slots.items()))
            lines.append(f"- Saturday slots: {text}")
        else:
            escalate = True

    if enquiry.details.unknown_topics:
        escalate = True

    if not lines:
        return Draft(ESCALATION_PHRASE, True)

    body = "Hi! Here is what I can confirm:\n" + "\n".join(lines)
    if escalate:
        body += "\n" + ESCALATION_PHRASE
    return Draft(body, escalate)
