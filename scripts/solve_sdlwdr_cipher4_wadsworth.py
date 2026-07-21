#!/usr/bin/env python3
"""Search Wadsworth-style cyclic deck readings of sdlwdr puzzle #4.

The puzzle author described the construction as deck-based, and a solver
identified its effective group as cyclic with the equivalent ciphertext
alphabet in standard order.  In a two-wheel/Wadsworth realization, movement
around the 83-card ciphertext wheel advances a plaintext wheel of a possibly
different size.  The plaintext is therefore recovered by accumulating
adjacent ciphertext distances modulo the plaintext-wheel length.

This program searches plausible plaintext-wheel sizes, orientations, origins,
and straightforward initial alphabet orders.  It scores every original output
position with an uppercase letter/space tetragram model; punctuation and digits
are treated as separators, so candidates cannot win merely by emitting little
scoreable text.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
import json
from math import log
from pathlib import Path
import string
from typing import Iterable, Sequence

from eye_mystery.practice_sdlwdr import PLAINTEXT_ALPHABET


MODULUS = 83
ROOT = Path(__file__).resolve().parents[1]


def normalized_fixed(text: str) -> tuple[int, ...]:
    """Map each position to A-Z or space without changing its length."""

    return tuple(
        ord(character.upper()) - ord("A")
        if character.upper() in string.ascii_uppercase
        else 26
        for character in text
    )


@dataclass(frozen=True)
class Tetragrams:
    scores: dict[tuple[int, ...], float]
    floor: float

    @classmethod
    def train(cls, text: str) -> "Tetragrams":
        values = normalized_fixed(text)
        counts = Counter(
            values[index : index + 4] for index in range(len(values) - 3)
        )
        total = sum(counts.values())
        return cls(
            {gram: log(count / total) for gram, count in counts.items()},
            log(0.01 / total),
        )

    def score(self, texts: Iterable[str]) -> float:
        total = 0.0
        for text in texts:
            values = normalized_fixed(text)
            total += sum(
                self.scores.get(values[index : index + 4], self.floor)
                for index in range(len(values) - 3)
            )
            # Mapping every punctuation mark to the language model's space
            # class otherwise lets punctuation-only candidates beat prose via
            # the very common "    " tetragram.  Literal spaces are free;
            # digits and punctuation pay for each occupied source position.
            total -= 8.0 * sum(
                character != " " and character.upper() not in string.ascii_uppercase
                for character in text
            )
        return total


def coordinates(
    message: Sequence[int],
    plaintext_modulus: int,
    *,
    multiplier: int,
    include_first: bool,
) -> tuple[int, ...]:
    """Accumulate standard-order CT-wheel distances on the PT wheel."""

    previous = 0 if include_first else message[0]
    accumulator = 0
    result: list[int] = []
    for current in message[0 if include_first else 1 :]:
        distance = multiplier * ((current - previous) % MODULUS) % MODULUS
        accumulator = (accumulator + distance) % plaintext_modulus
        result.append(accumulator)
        previous = current
    return tuple(result)


def alphabet_families(maximum: int) -> dict[str, str]:
    ascii_order = "".join(chr(value) for value in range(32, 127))
    natural = (
        PLAINTEXT_ALPHABET
        + string.ascii_lowercase
        + ",;:\"/()[]{}_+*=#@&%$<>\\|`~^"
    )
    families = {
        "ascii": ascii_order,
        "natural42-first": natural,
        "upper-lower":
            string.ascii_uppercase
            + string.ascii_lowercase
            + string.digits
            + " .,-’?!;:\"/()[]{}",
        "python-printable": string.printable.rstrip(),
    }
    return {
        name: alphabet[:maximum]
        for name, alphabet in families.items()
        if len(alphabet) >= maximum and len(set(alphabet[:maximum])) == maximum
    }


@dataclass(frozen=True)
class Candidate:
    score: float
    modulus: int
    include_first: bool
    multiplier: int
    direction: int
    shift: int
    alphabet_name: str
    texts: tuple[str, ...]


def search(
    messages: Sequence[Sequence[int]],
    model: Tetragrams,
    *,
    minimum_modulus: int,
    maximum_modulus: int,
    multipliers: Iterable[int],
    family_names: set[str] | None,
    top: int,
) -> list[Candidate]:
    best: list[Candidate] = []
    for modulus in range(minimum_modulus, maximum_modulus + 1):
        alphabets = alphabet_families(modulus)
        if family_names is not None:
            alphabets = {
                name: alphabet
                for name, alphabet in alphabets.items()
                if name in family_names
            }
        for include_first in (False, True):
            for multiplier in multipliers:
                streams = tuple(
                    coordinates(
                        message,
                        modulus,
                        multiplier=multiplier,
                        include_first=include_first,
                    )
                    for message in messages
                )
                for direction in (1, -1):
                    for shift in range(modulus):
                        for alphabet_name, alphabet in alphabets.items():
                            texts = tuple(
                                "".join(
                                    alphabet[(direction * value + shift) % modulus]
                                    for value in stream
                                )
                                for stream in streams
                            )
                            candidate = Candidate(
                                model.score(texts),
                                modulus,
                                include_first,
                                multiplier,
                                direction,
                                shift,
                                alphabet_name,
                                texts,
                            )
                            best.append(candidate)
        best.sort(key=lambda candidate: candidate.score, reverse=True)
        del best[top:]
    return best


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data",
        type=Path,
        default=ROOT / "artifacts/practice-sdlwdr/cipher4.json",
    )
    parser.add_argument(
        "--corpus",
        type=Path,
        default=Path(
            "/private/tmp/noita-eye-puzzle-scratchpad/"
            "research/data/lang/english-corpus-large.txt"
        ),
    )
    parser.add_argument("--minimum-modulus", type=int, default=27)
    parser.add_argument("--maximum-modulus", type=int, default=83)
    parser.add_argument(
        "--all-multipliers",
        action="store_true",
        help="also test all nonzero scalings of the standard cyclic generator",
    )
    parser.add_argument("--top", type=int, default=20)
    parser.add_argument(
        "--families",
        nargs="+",
        choices=("ascii", "natural42-first", "upper-lower", "python-printable"),
        help="restrict the straightforward plaintext alphabet orders",
    )
    args = parser.parse_args()

    messages = json.loads(args.data.read_text())
    model = Tetragrams.train(args.corpus.read_text(errors="ignore"))
    multipliers = range(1, MODULUS) if args.all_multipliers else (1,)
    candidates = search(
        messages,
        model,
        minimum_modulus=args.minimum_modulus,
        maximum_modulus=args.maximum_modulus,
        multipliers=multipliers,
        family_names=set(args.families) if args.families else None,
        top=args.top,
    )
    for candidate in candidates:
        print(
            f"score={candidate.score:.2f} modulus={candidate.modulus} "
            f"first={candidate.include_first} multiplier={candidate.multiplier} "
            f"direction={candidate.direction:+d} shift={candidate.shift} "
            f"alphabet={candidate.alphabet_name}"
        )
        for text in candidate.texts:
            print(text[:240])
        print()


if __name__ == "__main__":
    main()
