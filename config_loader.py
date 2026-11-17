"""Reads settings.cfg (simple `key = value` lines, `#` comments)."""

import warnings

SETTINGS_FILE = "settings.cfg"

KNOWN_KEYS = {
    "service_interval_km",
    "warn_at_percent",
    "report_title",
    "history_file",
    "log_file",
    "mileage_unit",
}


def load_settings(path: str | None = None) -> dict[str, str]:
    """Return the known settings as strings. Unknown keys and bad lines raise a warning."""
    path = path or SETTINGS_FILE
    settings: dict[str, str] = {}
    with open(path) as f:
        for number, raw in enumerate(f, start=1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                warnings.warn(f"{path}:{number}: ignoring line without '=': {line!r}")
                continue
            key, value = (part.strip() for part in line.split("=", 1))
            if key in KNOWN_KEYS:
                settings[key] = value
            else:
                warnings.warn(f"{path}:{number}: unknown setting {key!r} ignored")
    return settings


def get_int(settings: dict[str, str], key: str, fallback: int) -> int:
    """Return a setting as an int, or `fallback` if it is missing or not a number."""
    try:
        return int(settings[key])
    except (KeyError, ValueError):
        return fallback
