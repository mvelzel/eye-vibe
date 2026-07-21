#!/usr/bin/env python3
"""Find word-list CRC values among the 32-bit Eye storage constants."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from audit_lumikki_hash import CRC_MODELS


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("eye_code", type=Path)
    parser.add_argument("wordlist", type=Path)
    parser.add_argument("--minimum-length", type=int, default=4)
    parser.add_argument("--byte-reversed", action="store_true")
    args = parser.parse_args()

    source = args.eye_code.read_text(errors="ignore")
    constants = {
        int(value, 16)
        for value in re.findall(
            r"local_50\._[04]_4_\s*=\s*0x([0-9a-fA-F]+)", source
        )
    }
    words = {
        line.strip()
        for line in args.wordlist.read_text(errors="ignore").splitlines()
        if len(line.strip()) >= args.minimum_length
    }
    print("Eye constants:", len(constants))
    print("distinct candidate words:", len(words))

    for model, function in CRC_MODELS.items():
        matches = []
        for word in words:
            value = function(word.encode("utf-8"))
            candidates = {value}
            if args.byte_reversed:
                candidates.add(
                    int.from_bytes(value.to_bytes(4, "big"), "little")
                )
            overlap = candidates & constants
            if overlap:
                matches.append((word, min(overlap)))
        print(f"{model}: {len(matches)}")
        for word, value in sorted(matches):
            print(f"  {value:08x} {word}")


if __name__ == "__main__":
    main()
