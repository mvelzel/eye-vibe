#!/usr/bin/env python3
"""Scan source corpora against sdlwdr #4's exact cyclic-GAK recurrence.

The adjacent ciphertext differences are not assumed to be plaintext symbols.
For an arbitrary cyclic deck update they instead constrain one function ``q``:

    p[i+1] = sign_c * delta[i] + q(sign_p * p[selector])  (mod 83)

Whenever a candidate source repeats a selector symbol, it must demand the same
value of ``q``.  This is a key-free necessary condition, so a full-length hit
would be meaningful even though it would not yet recover the deck operation.
"""

from __future__ import annotations

import argparse
import heapq
import json
from pathlib import Path

from eye_mystery.practice_cipher4 import consistent_recurrence_prefix_at


MODULUS = 83
ROOT = Path(__file__).resolve().parents[1]


def normalize(text: str, mode: str) -> str:
    result: list[str] = []
    in_space = True
    for character in text.upper():
        if "A" <= character <= "Z":
            result.append(character)
            in_space = False
        elif mode != "letters-only" and not in_space:
            result.append(" ")
            in_space = True
    if result and result[-1] == " ":
        result.pop()
    return "".join(result)


def values(text: str, mode: str) -> tuple[int, ...]:
    if mode == "letters-only":
        return tuple(ord(character) - ord("A") for character in text)
    if mode == "compact-space":
        return tuple(
            26 if character == " " else ord(character) - ord("A")
            for character in text
        )
    if mode == "natural42":
        # The straightforward ordering used in the related puzzles is
        # A-Z, 0-9, then space and punctuation.
        return tuple(
            36 if character == " " else ord(character) - ord("A")
            for character in text
        )
    if mode == "ascii32":
        return tuple(ord(character) - 32 for character in text)
    raise ValueError(f"unknown mode: {mode}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("corpora", nargs="+", type=Path)
    parser.add_argument("--top", type=int, default=20)
    parser.add_argument(
        "--mode",
        dest="modes",
        action="append",
        choices=("letters-only", "compact-space", "natural42", "ascii32"),
        help="normalization to scan; repeat the option to select several",
    )
    args = parser.parse_args()
    if args.top < 0:
        parser.error("--top must be nonnegative")

    messages = json.loads(
        (ROOT / "artifacts/practice-sdlwdr/cipher4.json").read_text()
    )
    # Portions 1 and 2 have 200 equal adjacent differences at these offsets.
    message = messages[1]
    differences = tuple(
        (right - left) % MODULUS
        for left, right in zip(message, message[1:])
    )[5:205]
    needed = len(differences) + 1

    for corpus_path in args.corpora:
        source = corpus_path.read_text(errors="ignore")
        modes = args.modes or ("letters-only", "compact-space", "natural42")
        for mode in modes:
            normalized = normalize(source, mode)
            encoded = values(normalized, mode)
            print(
                f"corpus={corpus_path} mode={mode} normalized={len(encoded)} "
                f"window={needed}",
                flush=True,
            )
            for ciphertext_sign in (1, -1):
                for plaintext_sign in (1, -1):
                    for key_on_next in (False, True):
                        best: list[tuple[int, int]] = []
                        best_prefix = 0
                        exact = 0
                        for start in range(len(encoded) - needed + 1):
                            length = consistent_recurrence_prefix_at(
                                encoded,
                                start,
                                differences,
                                ciphertext_sign=ciphertext_sign,
                                plaintext_sign=plaintext_sign,
                                key_on_next=key_on_next,
                            )
                            best_prefix = max(best_prefix, length)
                            if args.top:
                                item = (length, start)
                                if len(best) < args.top:
                                    heapq.heappush(best, item)
                                elif item > best[0]:
                                    heapq.heapreplace(best, item)
                            if length == len(differences):
                                exact += 1
                        print(
                            f"  csign={ciphertext_sign:+d} "
                            f"psign={plaintext_sign:+d} "
                            f"key={'next' if key_on_next else 'current':<7} "
                            f"best_prefix={best_prefix} exact={exact}"
                        )
                        for length, start in sorted(best, reverse=True)[:5]:
                            preview = normalized[start : start + 100]
                            print(f"    {length:>3} @{start}: {preview}")


if __name__ == "__main__":
    main()
