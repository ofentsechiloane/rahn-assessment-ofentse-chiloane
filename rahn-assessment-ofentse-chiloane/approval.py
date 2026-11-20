def ask_approval(draft_text: str, input_fn=input) -> bool:
    """Print the draft and ask 'Send? (y/n)'. Anything but a clear y is a no."""
    print("\n--- DRAFT REPLY ---")
    print(draft_text)
    print("-------------------")
    while True:
        try:
            answer = input_fn("Send? (y/n) ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            return False
        if answer in ("y", "n"):
            return answer == "y"
        print("Please type y or n.")
