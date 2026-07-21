#!/usr/bin/env python3
"""Verify the exact solution of sdlwdr practice cipher #5."""

from __future__ import annotations

import hashlib

from eye_mystery.practice_cipher5 import (
    REVISED_SECTIONS,
    decode_revised_sections,
    encode_dynamic_substitution,
    recursive_increasing_chunk_reversal,
    render_plaintext,
)


def main() -> None:
    operations = tuple(
        recursive_increasing_chunk_reversal(83, index) for index in range(83)
    )
    plaintexts = decode_revised_sections()
    replayed = tuple(
        "".join(
            chr(card + 33)
            for card in encode_dynamic_substitution(plaintext, operations)
        )
        for plaintext in plaintexts
    )
    print(f"83 distinct operations: {len(set(operations)) == 83}")
    print(f"exact ciphertext replay: {replayed == REVISED_SECTIONS}")
    print("source: Dr. Seuss, Green Eggs and Ham")
    for number, plaintext in enumerate(plaintexts, 1):
        rendered = render_plaintext(plaintext)
        digest = hashlib.sha256(rendered.encode()).hexdigest()
        preview = rendered[:72].replace("\n", " ")
        print(f"{number}: len={len(rendered):3} sha256={digest} preview={preview!r}")


if __name__ == "__main__":
    main()
