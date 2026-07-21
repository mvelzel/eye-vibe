#!/usr/bin/env python3
"""Compare printable ASCII strings in two binaries."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def strings(path: Path, minimum: int) -> set[str]:
    pattern = re.compile(rb"[\x20-\x7e]{%d,}" % minimum)
    return {match.group().decode("ascii") for match in pattern.finditer(path.read_bytes())}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("left", type=Path)
    parser.add_argument("right", type=Path)
    parser.add_argument("--regex", default=".*")
    parser.add_argument("--minimum", type=int, default=4)
    args = parser.parse_args()
    left = strings(args.left, args.minimum)
    right = strings(args.right, args.minimum)
    expression = re.compile(args.regex, re.IGNORECASE)
    left_only = sorted(value for value in left - right if expression.search(value))
    right_only = sorted(value for value in right - left if expression.search(value))
    print(
        f"left={len(left)} right={len(right)} common={len(left & right)} "
        f"left_only={len(left - right)} right_only={len(right - left)}"
    )
    print(f"left_only_matching={len(left_only)}")
    for value in left_only:
        print(f"  {value}")
    print(f"right_only_matching={len(right_only)}")
    for value in right_only:
        print(f"  {value}")


if __name__ == "__main__":
    main()
