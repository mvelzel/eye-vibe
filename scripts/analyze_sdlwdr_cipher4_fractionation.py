#!/usr/bin/env python3
"""Run the frozen selector-demultiplex audit for sdlwdr cipher 4."""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

from eye_mystery.practice_cipher4 import cyclic_differences
from eye_mystery.practice_cipher4_fractionation import (
    audit_lane_demultiplex,
    audit_reassociation,
    interleave_lanes,
    reassociate_selectors,
    ReassociationSpec,
    split_coordinates,
)
from eye_mystery.practice_cipher4_routes import PatternModel


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


def planted_ranks(
    source: tuple[int, ...],
    lengths: tuple[int, ...],
    seed: int,
) -> tuple[tuple[int, ...], ...]:
    rng = random.Random(seed)
    labels = list(range(28))
    rng.shuffle(labels)
    mapped = tuple(labels[value] for value in source)
    cursor = 0
    output = []
    for length in lengths:
        selectors = tuple(rng.randrange(2) for _ in range(length))
        counts = (selectors.count(0), selectors.count(1))
        lanes = (
            mapped[cursor : cursor + counts[0]],
            mapped[cursor + counts[0] : cursor + sum(counts)],
        )
        cursor += sum(counts) + 13
        output.append(interleave_lanes(lanes, selectors))
    return tuple(output)


def planted_reassociation(
    source: tuple[int, ...],
    lengths: tuple[int, ...],
    seed: int,
) -> tuple[tuple[int, ...], ...]:
    rng = random.Random(seed)
    labels = list(range(28))
    rng.shuffle(labels)
    mapped = tuple(labels[value] for value in source)
    cursor = 0
    plaintexts = []
    for length in lengths:
        plaintexts.append(mapped[cursor : cursor + length])
        cursor += length + 13
    # Applying shift-right undoes a shift-left association block by block.
    encrypt = ReassociationSpec(3, 7, "shift-right")
    ciphertexts = []
    for plaintext in plaintexts:
        coordinates = split_coordinates(plaintext, 3)
        encrypted = reassociate_selectors(coordinates, encrypt)
        if encrypted is None:
            raise AssertionError("planted rank mapping must stay in 0..56")
        ciphertexts.append(encrypted)
    return tuple(ciphertexts)


def describe(label, audit) -> None:
    selected = audit.selected
    print(label)
    print(
        f"  selected={selected.spec.name}; "
        f"train={selected.train_improvement:+.9f}; "
        f"heldout={selected.heldout_improvement:+.9f}"
    )
    print(
        f"  null={audit.null_minimum:+.9f}..{audit.null_maximum:+.9f}; "
        f"mean={audit.null_mean:+.9f}; "
        f"upper={audit.corrected_upper_tail:.9f}"
    )


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
    parser.add_argument("--reassociation-order", type=int, default=14)
    parser.add_argument("--controls", type=int, default=2_000)
    parser.add_argument("--reassociation-controls", type=int, default=500)
    parser.add_argument("--seed", type=int, default=0x53444C5744520407)
    args = parser.parse_args()

    source = normalize_english(args.corpus.read_text(errors="ignore"))
    model = PatternModel.train(source, order=args.order)
    reassociation_model = PatternModel.train(
        source, order=args.reassociation_order
    )
    messages = json.loads(args.data.read_text())
    ranks = tuple(
        tuple(value - 22 for value in cyclic_differences(message))
        for message in messages
    )
    observed = audit_lane_demultiplex(
        ranks, model, controls=args.controls, seed=args.seed
    )
    describe("OBSERVED", observed)

    control_ranks = planted_ranks(
        source,
        tuple(map(len, ranks)),
        args.seed ^ 0x504C414E54,
    )
    planted = audit_lane_demultiplex(
        control_ranks,
        model,
        controls=max(50, min(args.controls, 200)),
        seed=args.seed ^ 0x434F4E54524F4C,
    )
    describe("PLANTED", planted)

    reassociation = audit_reassociation(
        ranks,
        reassociation_model,
        controls=args.reassociation_controls,
        seed=args.seed ^ 0x52454153534F43,
    )
    describe("REASSOCIATION OBSERVED", reassociation)

    reassociation_control = audit_reassociation(
        planted_reassociation(
            source,
            tuple(map(len, ranks)),
            args.seed ^ 0x5459504544504C,
        ),
        reassociation_model,
        controls=max(50, min(args.reassociation_controls, 200)),
        seed=args.seed ^ 0x52454153504354,
    )
    describe("REASSOCIATION PLANTED", reassociation_control)


if __name__ == "__main__":
    main()
