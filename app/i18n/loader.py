import json
from pathlib import Path

LOCALES_DIR = Path(__file__).parent / "locales"
_active_locale: dict = {}
_active_code: str = "en"


def load_locale(code: str) -> None:
    global _active_locale, _active_code
    path = LOCALES_DIR / f"{code}.json"
    if not path.exists():
        raise FileNotFoundError(f"Locale file not found: {path}")
    with path.open(encoding="utf-8") as f:
        _active_locale = json.load(f)
    _active_code = code


def get_active_code() -> str:
    return _active_code


def t(key: str) -> str:
    parts = key.split(".")
    value = _active_locale
    for part in parts:
        if not isinstance(value, dict) or part not in value:
            return key
        value = value[part]
    return str(value) if value is not None else key
