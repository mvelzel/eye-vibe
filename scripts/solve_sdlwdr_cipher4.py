#!/usr/bin/env python3
"""Beam-search the cyclic-state model suggested for sdlwdr cipher #4.

If the effective deck group is cyclic and the visible cipher alphabet is in
standard order, a repeated plaintext block observed from two deck states must
be a constant translate.  More generally, adjacent ciphertext differences
obey

    p[i + 1] = sign * (c[i + 1] - c[i]) + key[p[i]]  (mod 83)

for a plaintext-selected rotation table ``key``.  This script learns that
table while decoding into a 27-symbol A-Z-plus-space alphabet.  The key is not
guessed independently: its first use branches over the 27 possible following
characters; every later use is deterministic.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
import json
from math import log
from pathlib import Path
from typing import Iterable


MODULUS = 83
UNSET = -1


def normalize(text: str) -> tuple[int, ...]:
    result: list[int] = []
    in_space = True
    for character in text.upper():
        if "A" <= character <= "Z":
            result.append(ord(character) - ord("A"))
            in_space = False
        elif not in_space:
            result.append(26)
            in_space = True
    if result and result[-1] == 26:
        result.pop()
    return tuple(result)


@dataclass(frozen=True)
class NgramModel:
    order: int
    scores: dict[tuple[int, ...], float]
    floor: float

    @classmethod
    def train(cls, text: str, order: int = 5) -> "NgramModel":
        values = normalize(text)
        counts = Counter(
            values[index : index + order]
            for index in range(len(values) - order + 1)
        )
        total = sum(counts.values())
        return cls(
            order,
            {gram: log(count / total) for gram, count in counts.items()},
            log(0.02 / total),
        )

    def score_tail(self, values: tuple[int, ...]) -> float:
        if len(values) < self.order:
            return 0.0
        return self.scores.get(values[-self.order :], self.floor)


@dataclass(frozen=True)
class Candidate:
    score: float
    text: tuple[int, ...]
    key: tuple[int, ...]


def decode_beam(
    ciphertext: tuple[int, ...],
    model: NgramModel,
    *,
    sign: int,
    beam_width: int,
    allowed: tuple[int, ...],
    decode_symbol: dict[int, int],
    initial_keys: Iterable[tuple[int, ...]] | None = None,
) -> list[Candidate]:
    if sign not in (-1, 1):
        raise ValueError("sign must be -1 or +1")
    keys = tuple(initial_keys or ((UNSET,) * MODULUS,))
    beam = [
        Candidate(0.0, (first,), key)
        for key in keys
        for first in allowed
    ]
    differences = tuple(
        (right - left) % MODULUS
        for left, right in zip(ciphertext, ciphertext[1:])
    )
    for position, difference in enumerate(differences, start=1):
        expanded: dict[tuple[tuple[int, ...], tuple[int, ...]], Candidate] = {}
        signed_difference = sign * difference
        for candidate in beam:
            current = candidate.text[-1]
            key_value = candidate.key[current]
            if key_value == UNSET:
                next_values = allowed
            else:
                next_values = ((signed_difference + key_value) % MODULUS,)
            for next_value in next_values:
                if next_value not in decode_symbol:
                    continue
                key = candidate.key
                if key_value == UNSET:
                    mutable = list(key)
                    mutable[current] = (next_value - signed_difference) % MODULUS
                    key = tuple(mutable)
                text = candidate.text + (next_value,)
                language_tail = tuple(decode_symbol[value] for value in text[-model.order :])
                score = candidate.score + model.score_tail(language_tail)
                item = Candidate(score, text, key)
                identity = (text[-(model.order - 1) :], key)
                previous = expanded.get(identity)
                if previous is None or score > previous.score:
                    expanded[identity] = item
        beam = sorted(expanded.values(), key=lambda item: item.score, reverse=True)[
            :beam_width
        ]
        if not beam:
            break
        if position % 50 == 0:
            print(
                f"position={position:>3} beam={len(beam):>6} "
                f"best={beam[0].score:>10.2f} "
                f"{render(beam[0].text[-60:], decode_symbol)}"
            )
    return beam


def render(values: Iterable[int], decode_symbol: dict[int, int]) -> str:
    normalized = (decode_symbol[value] for value in values)
    return "".join(" " if value == 26 else chr(ord("A") + value) for value in normalized)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data",
        type=Path,
        default=Path("artifacts/practice-sdlwdr/cipher4.json"),
    )
    parser.add_argument(
        "--corpus",
        type=Path,
        default=Path(
            "/private/tmp/noita-eye-puzzle-scratchpad/"
            "research/data/lang/english-corpus-large.txt"
        ),
    )
    parser.add_argument("--message", type=int, default=0)
    parser.add_argument("--sign", type=int, choices=(-1, 1), default=1)
    parser.add_argument("--beam", type=int, default=50_000)
    parser.add_argument(
        "--alphabet",
        choices=("compact", "ascii32"),
        default="ascii32",
        help="numeric placement of A-Z and space in the 83-position PTA",
    )
    args = parser.parse_args()

    messages = tuple(tuple(message) for message in json.loads(args.data.read_text()))
    model = NgramModel.train(args.corpus.read_text(errors="ignore"))
    if args.alphabet == "compact":
        allowed = tuple(range(27))
        decode_symbol = {value: value for value in allowed}
    else:
        # PTA position zero renders as ASCII space under the thread's +32
        # convention; positions 33..58 render as A..Z.
        allowed = (0,) + tuple(range(33, 59))
        decode_symbol = {0: 26, **{value: value - 33 for value in range(33, 59)}}
    candidates = decode_beam(
        messages[args.message],
        model,
        sign=args.sign,
        beam_width=args.beam,
        allowed=allowed,
        decode_symbol=decode_symbol,
    )
    print("\nfinal candidates")
    for candidate in candidates[:20]:
        print(f"{candidate.score:>12.2f} {render(candidate.text, decode_symbol)}")
        print("key", candidate.key)


if __name__ == "__main__":
    main()
