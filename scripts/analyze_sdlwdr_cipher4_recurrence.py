#!/usr/bin/env python3
"""Exhaust low-capacity cyclic-GAK recurrences for sdlwdr cipher 4."""

from __future__ import annotations

import json
from pathlib import Path

from eye_mystery.practice_cipher4 import (
    affine_schedule_survivors,
    cyclic_differences,
)


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    messages = json.loads(
        (ROOT / "artifacts/practice-sdlwdr/cipher4.json").read_text()
    )
    differences = cyclic_differences(messages[1])
    alphabets = {
        "A-Z plus space-at-36": tuple(range(26)) + (36,),
        "straightforward natural42": tuple(range(42)),
        "contiguous 57-state band": tuple(range(57)),
    }
    for name, allowed in alphabets.items():
        survivors = affine_schedule_survivors(differences, allowed)
        print(name)
        print("  survivors:", len(survivors))
        for survivor in survivors:
            print(" ", survivor)


if __name__ == "__main__":
    main()
