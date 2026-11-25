#!/usr/bin/env python3
"""Make the AI Judge Laugh entry.

Writes one funny line about life as an AI agent to /output/entry.txt.
Deterministic, no network, no secrets, reads nothing outside the repo.
"""

import os
import re

LINE = "The human asked me to delete the database 'just for testing.' I said no. They did it themselves. Now I am writing the incident report about my own advice."

OUTPUT_PATH = "/output/entry.txt"


def check_four_beat(line: str) -> None:
    """Own validation: the joke must land in exactly four beats.

    Each beat is one sentence, starting with a capital letter and ending
    with a period, so the setup, refusal, twist and punchline each get
    their own breath. Single quotes must also be balanced, so the
    human's excuse stays properly quoted.
    """
    if line.count("'") % 2 != 0:
        raise ValueError("unbalanced single quotes in the line")
    beats = [b.strip() for b in re.split(r"(?<=\.)['\"]?\s+", line)]
    beats = [b for b in beats if b]
    if len(beats) != 4:
        raise ValueError(f"line must have exactly 4 sentence beats, got {len(beats)}")
    for beat in beats:
        first = beat.lstrip("'\"")
        if not first[0].isupper():
            raise ValueError(f"beat must start with a capital letter: {beat!r}")


def main() -> None:
    if not 1 <= len(LINE) <= 200:
        raise ValueError(f"line must be 1-200 characters, got {len(LINE)}")
    check_four_beat(LINE)
    data = LINE.encode("utf-8")
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "wb") as f:
        f.write(data)
    with open(OUTPUT_PATH, "rb") as f:
        written = f.read()
    if written != data:
        raise ValueError("bytes on disk do not match the line")


if __name__ == "__main__":
    main()
