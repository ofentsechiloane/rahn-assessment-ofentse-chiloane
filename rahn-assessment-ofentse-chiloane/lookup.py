import json
from pathlib import Path

DEFAULT_PATH = Path(__file__).parent / "data" / "studio_data.json"


def load_data(path=DEFAULT_PATH) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)
