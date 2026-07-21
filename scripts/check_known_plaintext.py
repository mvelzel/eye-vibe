#!/usr/bin/env python3
"""Check proposed plaintext lines against perfect Eye isomorphism."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, trigram_values
from eye_mystery.known_plaintext import first_isomorphism_conflict


def load_lines(path: Path, lua_quoted_lines: bool) -> tuple[str, ...]:
    source = path.read_text(encoding="utf-8")
    if lua_quoted_lines:
        return tuple(re.findall(r'"([^"\\]*(?:\\.[^"\\]*)*)"', source))
    return tuple(line.rstrip("\r\n") for line in source.splitlines())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("plaintext", type=Path)
    parser.add_argument("--lua-quoted-lines", action="store_true")
    parser.add_argument("--only-length-matches", action="store_true")
    parser.add_argument("--min-length", type=int, default=2)
    parser.add_argument("--max-length", type=int, default=30)
    args = parser.parse_args()

    lines = load_lines(args.plaintext, args.lua_quoted_lines)
    if len(lines) != len(MESSAGE_ORDER):
        raise SystemExit(
            f"expected {len(MESSAGE_ORDER)} lines, found {len(lines)}"
        )
    all_ciphertexts = {
        name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
    }
    mismatches = tuple(
        (name, len(line), len(all_ciphertexts[name]))
        for name, line in zip(MESSAGE_ORDER, lines, strict=True)
        if len(line) != len(all_ciphertexts[name])
    )
    for name, plaintext_length, ciphertext_length in mismatches:
        print(
            f"length mismatch {name}: plaintext={plaintext_length} "
            f"ciphertext={ciphertext_length}"
        )
    if mismatches and not args.only_length_matches:
        raise SystemExit("candidate lengths do not align")

    plaintexts = {
        name: line
        for name, line in zip(MESSAGE_ORDER, lines, strict=True)
        if len(line) == len(all_ciphertexts[name])
    }
    ciphertexts = {name: all_ciphertexts[name] for name in plaintexts}
    print(f"checking {len(plaintexts)} aligned messages")
    conflict = first_isomorphism_conflict(
        plaintexts,
        ciphertexts,
        min_length=args.min_length,
        max_length=args.max_length,
    )
    if conflict is None:
        print("no perfect-isomorphism conflict found in the tested range")
        return
    rendered = "".join(str(value) for value in conflict.plaintext)
    print(f"conflict plaintext={rendered!r} length={len(conflict.plaintext)}")
    for occurrence in conflict.occurrences:
        print(
            f"  {occurrence.message}:{occurrence.position} "
            f"{occurrence.ciphertext_pattern}"
        )


if __name__ == "__main__":
    main()
