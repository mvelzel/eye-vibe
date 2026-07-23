#!/usr/bin/env python3
"""Enumerate small selector-controlled quotient walks for practice cipher 4."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import random
import string

from eye_mystery.practice_cipher4 import cyclic_differences
from eye_mystery.practice_cipher4_bijection import (
    CaseNgrams,
    normalize_case_text,
)
from eye_mystery.practice_cipher4_selector import (
    SelectorLaw,
    best_affine_render,
    decode_selector_walk,
    encode_unsigned_walk,
    selector_laws,
)


ROOT = Path(__file__).resolve().parents[1]
ALPHABET_FAMILIES = {
    "space-first": string.ascii_uppercase + " .," + string.digits + "-'?!;:/",
    "sdlwdr": string.ascii_uppercase + string.digits + " .-'?!",
    "finnish29": string.ascii_uppercase + "ÄÖ ",
}


def alphabet_for(family: str, modulus: int) -> str | None:
    base = ALPHABET_FAMILIES[family]
    if family == "finnish29":
        return base if modulus == 29 else None
    if len(base) < modulus:
        return None
    return base[:modulus]


def planted_control(
    corpus: str,
    alphabet: str,
    lengths: tuple[int, ...],
    seed: int,
) -> tuple[tuple[int, ...], ...]:
    normalized = normalize_case_text(corpus.upper(), alphabet)
    required = sum(lengths)
    source = normalized[20_000 : 20_000 + required]
    if len(source) != required:
        raise ValueError("corpus is too short for the planted control")
    coordinates = tuple(alphabet.index(character) for character in source)
    rng = random.Random(seed)
    ranks = []
    cursor = 0
    for length in lengths:
        plaintext = coordinates[cursor : cursor + length]
        selectors = []
        previous = 0
        for value in plaintext:
            quotient = (value - previous) % len(alphabet)
            valid = [
                selector
                for selector in range(2)
                if 2 * quotient + selector < 57
            ]
            selectors.append(rng.choice(valid))
            previous = value
        ranks.append(
            encode_unsigned_walk(
                plaintext,
                width=2,
                modulus=len(alphabet),
                selectors=selectors,
            )
        )
        cursor += length
    return tuple(ranks)


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
    parser.add_argument(
        "--moduli",
        nargs="+",
        type=int,
        default=(19, 27, 28, 29, 30, 36, 37, 41, 42),
    )
    parser.add_argument(
        "--families",
        nargs="+",
        choices=tuple(ALPHABET_FAMILIES),
        default=("space-first", "sdlwdr"),
    )
    parser.add_argument("--top", type=int, default=20)
    parser.add_argument("--seed", type=int, default=0x53444C5744520404)
    parser.add_argument(
        "--shared-shift",
        action="store_true",
        help="require all portions to use one ring orientation and rotation",
    )
    args = parser.parse_args()

    messages = json.loads(args.data.read_text())
    ranks = tuple(
        tuple(value - 22 for value in cyclic_differences(message))
        for message in messages
    )
    corpus = args.corpus.read_text(errors="ignore")

    for family in args.families:
        for modulus in args.moduli:
            alphabet = alphabet_for(family, modulus)
            if alphabet is None:
                continue
            model = CaseNgrams.train(corpus.upper(), alphabet)
            results = []
            for width in (2, 3):
                for law in selector_laws(width):
                    streams = tuple(
                        decode_selector_walk(stream, modulus, law)
                        for stream in ranks
                    )
                    rendered = best_affine_render(
                        streams,
                        alphabet,
                        model,
                        independent_portion_shifts=not args.shared_shift,
                    )
                    results.append((rendered.score_per_gram, law, rendered))
            results.sort(key=lambda item: item[0], reverse=True)

            print(
                f"\nFAMILY={family} MODULUS={modulus} "
                f"ALPHABET={alphabet!r} laws={len(results)}"
            )
            if modulus == 29:
                control_ranks = planted_control(
                    corpus,
                    alphabet,
                    tuple(map(len, ranks)),
                    args.seed,
                )
                control_law = SelectorLaw("unsigned", 2, 0)
                control_streams = tuple(
                    decode_selector_walk(stream, modulus, control_law)
                    for stream in control_ranks
                )
                control = best_affine_render(
                    control_streams,
                    alphabet,
                    model,
                    independent_portion_shifts=not args.shared_shift,
                )
                print(
                    f"CONTROL law={control_law.name} "
                    f"score_per_gram={control.score_per_gram:.6f} "
                    f"directions={control.directions} shifts={control.shifts}"
                )
                for text in control.texts:
                    print("  ", text[:120])
            for score, law, rendered in results[: args.top]:
                print(
                    f"score_per_gram={score:.6f} law={law.name} "
                    f"directions={rendered.directions} shifts={rendered.shifts}"
                )
                for text in rendered.texts:
                    print("  ", text[:120])


if __name__ == "__main__":
    main()
