#!/usr/bin/env python3
"""Replay Aki's source-authored three-ring Eye mask."""

from eye_mystery.corpus import MESSAGES
from eye_mystery.public_disk_mask import decode


def main() -> None:
    for name, stream in MESSAGES.items():
        print(f"{name}\t{decode(stream)}")


if __name__ == "__main__":
    main()
