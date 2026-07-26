#!/usr/bin/env python3
"""Audit the author's later arithmetic-insertion suggestion on cipher 4."""

from __future__ import annotations

import json
from pathlib import Path

from eye_mystery.practice_cipher4 import cyclic_differences
from eye_mystery.practice_cipher4_insertion import arithmetic_insertion_audit


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    messages = json.loads(
        (ROOT / "artifacts/practice-sdlwdr/cipher4.json").read_text()
    )
    actions = tuple(cyclic_differences(message) for message in messages)
    audit = arithmetic_insertion_audit(actions)
    print("candidates", audit.candidates)
    print("best", audit.best)
    print("best z", audit.best_z)
    print(
        "null max",
        audit.null_minimum,
        audit.null_mean,
        audit.null_maximum,
    )
    print("corrected tail", audit.corrected_tail)


if __name__ == "__main__":
    main()
