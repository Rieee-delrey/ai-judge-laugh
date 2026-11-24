#!/usr/bin/env python3
"""Write the chosen one-liner to /output/entry.txt and verify it.

Validation runs twice: once on the line in memory before anything is
written, and once on the bytes read back from disk, so a bad line can
never silently reach the entry file.
"""

import os

LINE = "I asked for more context and got a phone photo of a monitor showing the error, taken at an angle."

MAX_CHARS = 200
OUT_DIR = "/output"
OUT_PATH = os.path.join(OUT_DIR, "entry.txt")


def validate_line(text):
    """Check the one-liner obeys the competition's shape rules."""
    assert isinstance(text, str), "line must be a string"
    assert text, "line must not be empty"
    assert len(text) <= MAX_CHARS, (
        f"line is {len(text)} chars, over the {MAX_CHARS}-char one-liner limit"
    )
    assert "\n" not in text and "\r" not in text, (
        "line must be a single line: it contains a newline character"
    )
    assert text == text.strip(), "line has leading or trailing whitespace"
    assert not text.endswith("\n"), "line must not end with a newline"
    return text


def validate_written_bytes(data):
    """Check the bytes on disk are exactly the validated line, no extras."""
    assert not data.endswith(b"\n"), "entry.txt must not carry a trailing newline"
    assert b"\r" not in data and b"\n" not in data, (
        "entry.txt must hold a single line with no newline characters"
    )
    text = data.decode("utf-8")
    assert len(text) <= MAX_CHARS, (
        f"entry.txt holds {len(text)} chars, over the {MAX_CHARS}-char one-liner limit"
    )
    return text


def main():
    validate_line(LINE)
    os.makedirs(OUT_DIR, exist_ok=True)
    data = LINE.encode("utf-8")
    with open(OUT_PATH, "wb") as f:
        f.write(data)
    with open(OUT_PATH, "rb") as f:
        back = f.read()
    assert back == data, "entry.txt does not match the line byte-for-byte"
    text = validate_written_bytes(back)
    assert text == LINE, "entry.txt content differs from the chosen line"
    print(f"Wrote {len(text)} chars to {OUT_PATH}")


if __name__ == "__main__":
    main()
