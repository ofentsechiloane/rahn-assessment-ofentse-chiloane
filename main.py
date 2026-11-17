from dotenv import load_dotenv

from approval import ask_approval
from drafter import draft_reply
from llm import AIUnavailable, InvalidAIOutput, classify
from lookup import load_data
from status_log import record


def process(message, data=None, input_fn=input, log_path=None) -> str:
    """Run one enquiry end to end. Returns the status that was recorded."""
    data = data if data is not None else load_data()

    try:
        enquiry = classify(message)
    except AIUnavailable as exc:
        print("The AI service is unavailable. Nothing was sent.")
        record("error_ai_unavailable", message, detail=str(exc), path=log_path)
        return "error_ai_unavailable"
    except InvalidAIOutput as exc:
        print("The AI returned invalid output. Nothing was sent.")
        record("error_invalid_ai_output", message, detail=str(exc), path=log_path)
        return "error_invalid_ai_output"

    draft = draft_reply(enquiry, data)
    # Approval is always asked here, whatever requires_human_approval says.
    approved = ask_approval(draft.text, input_fn)
    status = "sent" if approved else "rejected_by_staff"
    record(status, message, reply=draft.text, escalation=draft.escalation, path=log_path)
    print(f"Recorded as: {status}" + (" (nothing is actually sent in this demo)" if approved else ""))
    return status


def build_menu(data):
    """Options come from the data file, so the menu can never offer something that doesn't exist."""
    options = [
        (f"Price: {pkg['label']}", f"What is the price of {pkg['label']}?")
        for pkg in data.get("packages", {}).values()
    ]
    if data.get("saturday_slots"):
        options.append(("Saturday availability", "Which Saturday slots are available?"))
    options.append(("All package prices", "What are all your package prices?"))
    return options


def resolve_choice(text, options):
    """A valid menu number becomes its preset question; anything else is the customer's own text."""
    if text.isdigit() and 1 <= int(text) <= len(options):
        return options[int(text) - 1][1]
    return text


def main():
    load_dotenv()
    data = load_data()
    options = build_menu(data)
    while True:
        print("\nWhat does the customer want to know?")
        for i, (label, _) in enumerate(options, 1):
            print(f"  {i}. {label}")
        print("Type a number, or type the customer's own message. Press Enter on a blank line to quit.")
        try:
            text = input("> ").strip()
        except EOFError:
            text = ""
        if not text:
            print("Goodbye.")
            return
        message = resolve_choice(text, options)
        print(f"Enquiry: {message}")
        process(message, data)

if __name__ == "__main__":
    main()
