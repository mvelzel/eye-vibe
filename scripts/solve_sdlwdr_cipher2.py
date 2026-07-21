#!/usr/bin/env python3
"""Decode and verify sdlwdr practice cipher #2."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from eye_mystery.practice_sdlwdr import decode_puzzle2_sections


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    messages = json.loads(
        (ROOT / "artifacts/practice-sdlwdr/cipher2.json").read_text()
    )
    plaintexts = decode_puzzle2_sections(messages)
    print("source: The Kalevala, Rune XLIX, Restoration of the Sun and Moon")
    for index, plaintext in enumerate(plaintexts):
        digest = hashlib.sha256(plaintext.encode()).hexdigest()
        print(
            f"{index:2}: len={len(plaintext):3} sha256={digest} "
            f"preview={plaintext[:88]!r}"
        )


if __name__ == "__main__":
    main()
