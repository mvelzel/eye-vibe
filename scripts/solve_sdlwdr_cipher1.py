#!/usr/bin/env python3
"""Print and fingerprint the complete recovered sdlwdr practice cipher #1."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from eye_mystery.practice_sdlwdr import decode_puzzle1_sections


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    messages = json.loads(
        (ROOT / "artifacts/practice-sdlwdr/cipher1.json").read_text()
    )
    plaintexts = decode_puzzle1_sections(messages)
    for number, plaintext in enumerate(plaintexts, 1):
        digest = hashlib.sha256(plaintext.encode()).hexdigest()
        print(f"SECTION {number} len={len(plaintext)} sha256={digest}")
        print(plaintext)
        print()


if __name__ == "__main__":
    main()
