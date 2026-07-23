#!/usr/bin/env python3
"""Selection-corrected small-route screen for sdlwdr cipher 4."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import random

from eye_mystery.practice_cipher4 import cyclic_differences
from eye_mystery.practice_cipher4_routes import (
    PatternModel,
    RouteSpec,
    apply_route,
    audit_routes,
    route_order,
    route_specs,
)


ROOT = Path(__file__).resolve().parents[1]


def normalize_english(text: str) -> tuple[int, ...]:
    values = []
    in_space = True
    for character in text.upper():
        if "A" <= character <= "Z":
            values.append(ord(character) - ord("A"))
            in_space = False
        elif not in_space:
            values.append(26)
            in_space = True
    return tuple(values)


def invert_applied_route(
    values: tuple[int, ...], spec: RouteSpec
) -> tuple[int, ...]:
    order = route_order(len(values), spec)
    ciphertext = [0] * len(values)
    for output, source in enumerate(order):
        ciphertext[source] = values[output]
    return tuple(ciphertext)


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
    parser.add_argument("--order", type=int, default=8)
    parser.add_argument("--controls", type=int, default=100)
    parser.add_argument("--seed", type=int, default=0x53444C5744520406)
    parser.add_argument("--top", type=int, default=12)
    args = parser.parse_args()

    source = normalize_english(args.corpus.read_text(errors="ignore"))
    model = PatternModel.train(source, order=args.order)
    messages = json.loads(args.data.read_text())
    ranks = tuple(
        tuple(value - 22 for value in cyclic_differences(message))
        for message in messages
    )
    specs = route_specs()
    print(
        f"order={args.order} routes={len(specs)} controls={args.controls}"
    )

    for width in (2, 3):
        quotient = tuple(
            tuple(rank // width for rank in stream) for stream in ranks
        )
        audit = audit_routes(
            quotient,
            model,
            controls=args.controls,
            seed=args.seed ^ width,
            specs=specs,
        )
        print(f"\nWIDTH={width}")
        print(
            f"identity={audit.identity.score_per_gram:.9f} "
            f"best={audit.best_nonidentity.spec.name} "
            f"score={audit.best_nonidentity.score_per_gram:.9f} "
            f"improvement={audit.improvement:+.9f}"
        )
        print(
            f"selected-null={audit.null_minimum:+.9f}.."
            f"{audit.null_maximum:+.9f} mean={audit.null_mean:+.9f} "
            f"upper={audit.corrected_upper_tail:.9f}"
        )
        for score in audit.scores[: args.top]:
            print(f"  {score.score_per_gram:+.9f} {score.spec.name}")

    control_lengths = tuple(len(stream) for stream in ranks)
    control_plaintexts = []
    cursor = 0
    for length in control_lengths:
        control_plaintexts.append(tuple(source[cursor : cursor + length]))
        cursor += length + 37
    planted = RouteSpec("rect", 7, "inverse-columns")
    rng = random.Random(args.seed)
    labels = list(range(29))
    rng.shuffle(labels)
    substituted = tuple(
        tuple(labels[value] for value in stream)
        for stream in control_plaintexts
    )
    encrypted = tuple(
        invert_applied_route(stream, planted) for stream in substituted
    )
    control = audit_routes(
        encrypted,
        model,
        controls=max(10, min(args.controls, 50)),
        seed=args.seed ^ 29,
        specs=specs,
    )
    recovered = apply_route(encrypted[0], control.best_nonidentity.spec)
    print("\nPLANTED CONTROL")
    print(
        f"planted={planted.name} "
        f"recovered={control.best_nonidentity.spec.name} "
        f"improvement={control.improvement:+.9f} "
        f"exact-first={recovered == substituted[0]}"
    )


if __name__ == "__main__":
    main()
