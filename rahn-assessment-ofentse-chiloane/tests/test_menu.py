from lookup import load_data
from main import build_menu, resolve_choice


def test_t9_menu_built_from_data_and_numbers_resolve():  # FR-01, FR-03
    options = build_menu(load_data())
    labels = [label for label, _ in options]
    assert "Price: 12 sessions" in labels and "Saturday availability" in labels
    assert resolve_choice("1", options) == options[0][1]
    assert resolve_choice("99", options) == "99"            # out of range: treated as free text
    assert resolve_choice("Do you do yoga?", options) == "Do you do yoga?"


def test_t9b_menu_drops_saturday_when_no_slots():  # FR-03
    labels = [l for l, _ in build_menu({"packages": {}, "saturday_slots": {}})]
    assert "Saturday availability" not in labels