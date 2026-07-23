#!/usr/bin/env python3
"""Find renaming-invariant source matches for sdlwdr practice cipher #4.

The author's cyclic-group hint makes the first ciphertext value followed by
mod-83 adjacent differences a monoalphabetic image of the plaintext actions.
That means an exact source passage can be recognized by its equality pattern
before the plaintext alphabet mapping is known.  This scanner compares every
window of those action streams with normalized windows in candidate corpora.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import string
from typing import Iterable, Sequence

from eye_mystery.practice_cipher4 import project_action_band


MODULUS = 83
ROOT = Path(__file__).resolve().parents[1]


def action_stream(message: Sequence[int]) -> tuple[int, ...]:
    if not message:
        return ()
    return (message[0],) + tuple(
        (right - left) % MODULUS for left, right in zip(message, message[1:])
    )


def signature(values: Iterable[object]) -> tuple[int, ...]:
    """Return the canonical first-occurrence signature of ``values``."""

    labels: dict[object, int] = {}
    result: list[int] = []
    for value in values:
        if value not in labels:
            labels[value] = len(labels)
        result.append(labels[value])
    return tuple(result)


def normalize(text: str, mode: str) -> str:
    if mode == "raw":
        return text.replace("\r\n", "\n").replace("\r", "\n")
    if mode == "case-letters-only":
        return "".join(character for character in text if character in string.ascii_letters)
    if mode == "upper-letters-only":
        return "".join(
            character.upper()
            for character in text
            if character in string.ascii_letters
        )
    if mode == "unicode-upper-letters-only":
        return "".join(character.upper() for character in text if character.isalpha())
    if mode in ("case-letters-space", "upper-letters-space"):
        result: list[str] = []
        in_space = True
        for character in text:
            if character in string.ascii_letters:
                result.append(character if mode.startswith("case") else character.upper())
                in_space = False
            elif not in_space:
                result.append(" ")
                in_space = True
        if result and result[-1] == " ":
            result.pop()
        return "".join(result)
    if mode == "unicode-upper-letters-space":
        result = []
        in_space = True
        for character in text:
            if character.isalpha():
                result.append(character.upper())
                in_space = False
            elif not in_space:
                result.append(" ")
                in_space = True
        if result and result[-1] == " ":
            result.pop()
        return "".join(result)
    raise ValueError(f"unknown normalization mode: {mode}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("corpora", nargs="+", type=Path)
    parser.add_argument("--window", type=int, default=48)
    parser.add_argument(
        "--projection",
        choices=(
            "raw",
            "rank-div2",
            "rank-mod2",
            "rank-div3",
            "rank-mod3",
            "rank-div19",
            "rank-mod19",
        ),
        default="raw",
        help="optional Cartesian projection of difference ranks 0..56",
    )
    parser.add_argument(
        "--drop-first-state",
        action="store_true",
        help="omit each portion's initial C83 state before applying a projection",
    )
    parser.add_argument(
        "--modes",
        nargs="+",
        choices=(
            "raw",
            "case-letters-only",
            "upper-letters-only",
            "case-letters-space",
            "upper-letters-space",
            "unicode-upper-letters-only",
            "unicode-upper-letters-space",
        ),
        default=(
            "case-letters-only",
            "upper-letters-only",
            "case-letters-space",
            "upper-letters-space",
        ),
    )
    args = parser.parse_args()

    messages = json.loads(
        (ROOT / "artifacts/practice-sdlwdr/cipher4.json").read_text()
    )
    streams = []
    for message in messages:
        actions = action_stream(message)
        if args.drop_first_state:
            actions = actions[1:]
        streams.append(project_action_band(actions, args.projection))
    streams = tuple(streams)
    targets: dict[tuple[int, ...], list[tuple[int, int]]] = {}
    for message_index, stream in enumerate(streams):
        for start in range(len(stream) - args.window + 1):
            key = signature(stream[start : start + args.window])
            targets.setdefault(key, []).append((message_index, start))

    print(f"target signatures={len(targets)} window={args.window}")
    for path in args.corpora:
        source = path.read_text(errors="ignore")
        for mode in args.modes:
            text = normalize(source, mode)
            matches = 0
            print(f"scan path={path} mode={mode} length={len(text)}", flush=True)
            for start in range(len(text) - args.window + 1):
                key = signature(text[start : start + args.window])
                locations = targets.get(key)
                if locations is None:
                    continue
                matches += 1
                excerpt = text[max(0, start - 60) : start + args.window + 120]
                print(
                    f"  source={start} targets={locations[:8]} excerpt={excerpt!r}",
                    flush=True,
                )
            print(f"  matches={matches}", flush=True)


if __name__ == "__main__":
    main()
