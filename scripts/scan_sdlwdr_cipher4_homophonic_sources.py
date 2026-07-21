#!/usr/bin/env python3
"""Scan source corpora for homophonic plaintext of sdlwdr puzzle #4.

After cyclic reduction, portions 1 and 2 share a 200-symbol action block.  If
the actions are static homophones, every occurrence of one action symbol must
align with one source character, while several action symbols may align with
the same character.  This one-way equality condition is source-searchable
without first recovering the key.

The scanner checks that condition and optionally caps the number of action
symbols assigned to any source character.  It uses early repeated-position
constraints so million-character corpora can be searched quickly.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path
import string
from typing import Iterable, Sequence


MODULUS = 83
ROOT = Path(__file__).resolve().parents[1]


def action_stream(message: Sequence[int]) -> tuple[int, ...]:
    if not message:
        return ()
    return (message[0],) + tuple(
        (right - left) % MODULUS for left, right in zip(message, message[1:])
    )


def normalize(text: str, mode: str) -> str:
    if mode == "letters":
        return "".join(character.upper() for character in text if character in string.ascii_letters)
    if mode == "letters-space":
        result: list[str] = []
        in_space = True
        for character in text.upper():
            if character in string.ascii_uppercase:
                result.append(character)
                in_space = False
            elif not in_space:
                result.append(" ")
                in_space = True
        if result and result[-1] == " ":
            result.pop()
        return "".join(result)
    raise ValueError(f"unknown mode: {mode}")


def repeat_constraints(target: Sequence[int]) -> tuple[tuple[int, int], ...]:
    first: dict[int, int] = {}
    constraints: list[tuple[int, int]] = []
    for position, symbol in enumerate(target):
        if symbol in first:
            constraints.append((first[symbol], position))
        else:
            first[symbol] = position
    # Widely separated checks tend to reject wrong windows earlier.
    constraints.sort(key=lambda pair: pair[1] - pair[0], reverse=True)
    return tuple(constraints)


def compatible(
    target: Sequence[int],
    source: str,
    start: int,
    *,
    maximum_homophones: int | None,
) -> dict[int, str] | None:
    mapping: dict[int, str] = {}
    reverse: dict[str, set[int]] = defaultdict(set)
    for position, symbol in enumerate(target):
        character = source[start + position]
        previous = mapping.setdefault(symbol, character)
        if previous != character:
            return None
        reverse[character].add(symbol)
        if maximum_homophones is not None and len(reverse[character]) > maximum_homophones:
            return None
    return mapping


def matches(
    target: Sequence[int],
    source: str,
    *,
    maximum_homophones: int | None,
) -> Iterable[tuple[int, dict[int, str]]]:
    constraints = repeat_constraints(target)
    for start in range(len(source) - len(target) + 1):
        if any(source[start + left] != source[start + right] for left, right in constraints):
            continue
        mapping = compatible(
            target,
            source,
            start,
            maximum_homophones=maximum_homophones,
        )
        if mapping is not None:
            yield start, mapping


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("corpora", nargs="+", type=Path)
    parser.add_argument(
        "--mode", choices=("letters", "letters-space"), default="letters"
    )
    parser.add_argument("--maximum-homophones", type=int, default=2)
    parser.add_argument("--portion", type=int, default=1)
    parser.add_argument("--start", type=int, default=6)
    parser.add_argument("--length", type=int, default=200)
    args = parser.parse_args()

    messages = json.loads(
        (ROOT / "artifacts/practice-sdlwdr/cipher4.json").read_text()
    )
    stream = action_stream(messages[args.portion])
    target = stream[args.start : args.start + args.length]
    print(
        f"target portion={args.portion} start={args.start} length={len(target)} "
        f"symbols={len(set(target))} constraints={len(repeat_constraints(target))}"
    )
    for path in args.corpora:
        source = normalize(path.read_text(errors="ignore"), args.mode)
        found = list(
            matches(
                target,
                source,
                maximum_homophones=args.maximum_homophones,
            )
        )
        print(
            f"corpus={path} mode={args.mode} normalized={len(source)} "
            f"matches={len(found)}"
        )
        for start, mapping in found[:20]:
            preview = source[max(0, start - 80) : start + len(target) + 160]
            print(f"  start={start} mapped={len(mapping)} preview={preview!r}")


if __name__ == "__main__":
    main()
