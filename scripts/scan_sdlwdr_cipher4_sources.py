#!/usr/bin/env python3
"""Scan candidate plaintext corpora against sdlwdr #4's cyclic recurrence."""

from __future__ import annotations

import argparse
import heapq
import json
from pathlib import Path


MODULUS = 83
ROOT = Path(__file__).resolve().parents[1]


def normalize_letters(text: str) -> str:
    result = []
    in_space = True
    for character in text.upper():
        if "A" <= character <= "Z":
            result.append(character)
            in_space = False
        elif not in_space:
            result.append(" ")
            in_space = True
    if result and result[-1] == " ":
        result.pop()
    return "".join(result)


def values(text: str, alphabet: str) -> tuple[int, ...]:
    if alphabet == "compact":
        return tuple(26 if ch == " " else ord(ch) - ord("A") for ch in text)
    if alphabet == "ascii32":
        return tuple(ord(ch) - 32 for ch in text)
    raise ValueError(f"unknown alphabet: {alphabet}")


def consistent_prefix(
    plaintext: tuple[int, ...], differences: tuple[int, ...], sign: int
) -> int:
    key: dict[int, int] = {}
    for index, difference in enumerate(differences):
        current = plaintext[index]
        required = (plaintext[index + 1] - sign * difference) % MODULUS
        previous = key.setdefault(current, required)
        if previous != required:
            return index
    return len(differences)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("corpora", nargs="+", type=Path)
    parser.add_argument("--top", type=int, default=20)
    args = parser.parse_args()

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
        normalized = normalize_letters(corpus_path.read_text(errors="ignore"))
        print(
            f"corpus={corpus_path} normalized={len(normalized)} "
            f"window={needed}",
            flush=True,
        )
        for alphabet in ("compact", "ascii32"):
            encoded = values(normalized, alphabet)
            for sign in (1, -1):
                best: list[tuple[int, int]] = []
                exact = []
                for start in range(len(encoded) - needed + 1):
                    length = consistent_prefix(
                        encoded[start : start + needed], differences, sign
                    )
                    item = (length, start)
                    if len(best) < args.top:
                        heapq.heappush(best, item)
                    elif item > best[0]:
                        heapq.heapreplace(best, item)
                    if length == len(differences):
                        exact.append(start)
                print(
                    f"  alphabet={alphabet:<7} sign={sign:+d} "
                    f"best_prefix={max(best)[0]} exact={len(exact)}"
                )
                for length, start in sorted(best, reverse=True)[:5]:
                    preview = normalized[start : start + needed]
                    print(f"    {length:>3} @{start}: {preview[:100]}")


if __name__ == "__main__":
    main()
