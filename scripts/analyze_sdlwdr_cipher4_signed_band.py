#!/usr/bin/env python3
"""Test canonical signed readings of Cipher 4's odd 57-action band."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import string

from eye_mystery.practice_cipher4 import cyclic_differences
from eye_mystery.practice_cipher4_bijection import CaseNgrams
from eye_mystery.practice_cipher4_gak import signed_band_step
from eye_mystery.practice_cipher4_selector import best_affine_render


ROOT = Path(__file__).resolve().parents[1]
CONVENTIONS = (
    "zigzag-negative-odd",
    "zigzag-positive-odd",
    "centered",
    "centered-reflected",
)


def extended_alphabet() -> str:
    base = (
        string.ascii_uppercase
        + string.digits
        + " .-'?!"
        + string.ascii_lowercase
        + ',;:"/()[]{}_+*=#@&%$<>\\|`~^'
    )
    base += "".join(
        character
        for character in map(chr, range(161, 256))
        if character not in base
    )
    if len(set(base[:83])) != 83:
        raise AssertionError("extended plaintext alphabet is not injective")
    return base[:83]


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
    parser.add_argument("--top", type=int, default=20)
    args = parser.parse_args()

    messages = json.loads(args.data.read_text())
    ranks = tuple(
        tuple(value - 22 for value in cyclic_differences(message))
        for message in messages
    )
    corpus = args.corpus.read_text(errors="ignore")
    base = extended_alphabet()
    results = []
    for modulus in range(19, 84):
        alphabet = base[:modulus]
        model = CaseNgrams.train(corpus, alphabet)
        for convention in CONVENTIONS:
            streams = []
            for stream in ranks:
                accumulator = 0
                output = []
                for rank in stream:
                    accumulator = (
                        accumulator + signed_band_step(rank, convention)
                    ) % modulus
                    output.append(accumulator)
                streams.append(tuple(output))
            rendered = best_affine_render(
                tuple(streams),
                alphabet,
                model,
                independent_portion_shifts=True,
            )
            results.append(
                (
                    rendered.score_per_gram,
                    modulus,
                    convention,
                    rendered,
                )
            )

    for score, modulus, convention, rendered in sorted(
        results, reverse=True
    )[: args.top]:
        print(
            f"score_per_gram={score:.6f} modulus={modulus} "
            f"convention={convention} directions={rendered.directions} "
            f"shifts={rendered.shifts}"
        )
        for text in rendered.texts:
            print(" ", text[:160])


if __name__ == "__main__":
    main()
