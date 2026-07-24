#!/usr/bin/env python3
"""Run the frozen exact shared-linear-generator Eye audit."""

from __future__ import annotations

import argparse
import random

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.factoradic_headers import P_MESSAGES, Q_MESSAGES
from eye_mystery.fourteenth_linear import (
    LinearRepresentation,
    fit_shared_recurrence,
    generate_recurrence,
    representations,
    scan_shared_recurrences,
)


def eye_bodies() -> dict[str, tuple[int, ...]]:
    streams = {}
    for name in MESSAGE_ORDER:
        body = trigram_values(MESSAGES[name])[1:]
        trim = 25 if name in P_MESSAGES else 6
        streams[name] = body[trim:]
    return streams


def planted_check(seed: int) -> None:
    rng = random.Random(seed)
    coefficients = (2, 5, 7)
    streams = {
        name: generate_recurrence(
            coefficients,
            tuple(rng.randrange(83) for _ in coefficients),
            80,
            83,
        )
        for name in MESSAGE_ORDER
    }
    fit = fit_shared_recurrence(
        streams,
        LinearRepresentation("rank-f83", 83),
        3,
        train_names=P_MESSAGES,
        heldout_names=Q_MESSAGES,
    )
    print("PLANTED")
    print(
        f"  consistent={fit.system.consistent}; "
        f"unique={fit.system.unique}; "
        f"solution={fit.system.solution}"
    )
    print(
        f"  heldout={fit.heldout_matches}/{fit.heldout_equations}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--maximum-order", type=int, default=32)
    parser.add_argument("--seed", type=int, default=0x4C465352455945)
    parser.add_argument("--positive-only", action="store_true")
    args = parser.parse_args()

    planted_check(args.seed)
    if args.positive_only:
        return

    fits = scan_shared_recurrences(
        eye_bodies(),
        train_names=P_MESSAGES,
        heldout_names=Q_MESSAGES,
        maximum_order=args.maximum_order,
    )
    print("OBSERVED")
    for representation in representations():
        family = tuple(
            fit for fit in fits if fit.representation == representation
        )
        consistent = tuple(fit for fit in family if fit.system.consistent)
        final = family[-1]
        if not consistent:
            print(
                f"  {representation.name}: none<=order"
                f"{args.maximum_order}; "
                f"k{final.order} equations={final.system.equations} "
                f"rank={final.system.rank} "
                f"augmented={final.system.augmented_rank}"
            )
            continue
        first = consistent[0]
        print(
            f"  {representation.name}: first order={first.order}; "
            f"unique={first.system.unique}; "
            f"train-rank={first.system.rank}/{first.system.variables}; "
            f"heldout={first.heldout_matches}/{first.heldout_equations}"
        )


if __name__ == "__main__":
    main()
