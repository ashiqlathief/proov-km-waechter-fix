"""A tiny logger that collects lines and appends them to a file on flush."""

import time

LOG_LINES: list[str] = []


def log(message: str) -> None:
    """Print a timestamped line and remember it for the next flush."""
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{stamp}] {message}"
    LOG_LINES.append(line)
    print(line)


def flush_log(path: str) -> None:
    """Append all remembered lines to the file at `path`, then clear them."""
    with open(path, "a") as f:
        for line in LOG_LINES:
            f.write(line + "\n")
    LOG_LINES.clear()
