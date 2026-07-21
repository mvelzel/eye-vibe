#!/usr/bin/env python3
"""Calibrate the East 1/East 3/East 5 common-divisor observation."""

from __future__ import annotations

import argparse

from eye_mystery.checksum_null import (
    TWO_DIGIT_PRIMES,
    all_sums_avoid_divisors_probability,
    gcd_at_least_probability,
    marker_permutation_divisor_counts,
    marker_permutation_event_counts,
    simulate_gcd_events,
    simulate_partition_gcd_events,
)
from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, trigram_values
from eye_mystery.initials import body_sums, initial_values


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=1_000_000)
    parser.add_argument(
        "--partition-trials",
        type=int,
        default=0,
        help="also shuffle the observed corpus into fixed message lengths",
    )
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    lengths = tuple(len(trigram_values(MESSAGES[name])) for name in MESSAGE_ORDER)
    diagonal = (0, 4, 8)
    exact = gcd_at_least_probability(
        tuple(lengths[index] for index in diagonal), threshold=101
    )
    print("exact fixed-diagonal P(gcd >= 101):", f"{exact:.10g}")
    no_two_digit_prime = all_sums_avoid_divisors_probability(lengths)
    print(
        "exact P(all nine sums avoid every two-digit prime):",
        f"{no_two_digit_prime:.10g}",
    )
    fixed, any_triple = simulate_gcd_events(
        lengths,
        fixed_indices=diagonal,
        trials=args.trials,
        seed=args.seed,
    )
    print(
        f"sample seed={args.seed} trials={args.trials}: "
        f"fixed={fixed} ({fixed / args.trials:.10g}), "
        f"any={any_triple} ({any_triple / args.trials:.10g})"
    )
    assignment_counts = marker_permutation_event_counts(
        body_sums(),
        initial_values(),
        modulus=101,
        fixed_indices=diagonal,
        families=((0, 1, 2), (3, 4, 5), (6, 7, 8)),
    )
    total = assignment_counts["total"]
    print(
        "exact observed-marker assignments:",
        ", ".join(
            f"{name}={count}/{total} ({count / total:.10g})"
            for name, count in assignment_counts.items()
            if name != "total"
        ),
    )
    divisor_counts = marker_permutation_divisor_counts(
        body_sums(),
        initial_values(),
        divisors=TWO_DIGIT_PRIMES,
        modulus=101,
        fixed_indices=diagonal,
    )
    divisor_total = divisor_counts["total"]
    print(
        "exact observed-marker divisor/checksum assignments:",
        ", ".join(
            f"{name}={count}/{divisor_total} ({count / divisor_total:.10g})"
            for name, count in divisor_counts.items()
            if name != "total"
        ),
    )
    if args.partition_trials:
        messages = tuple(
            trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
        )
        all_values = tuple(value for message in messages for value in message)
        body_values = tuple(value for message in messages for value in message[1:])
        for label, values, markers in (
            ("whole-corpus", all_values, None),
            ("fixed-markers", body_values, initial_values()),
        ):
            fixed, any_triple = simulate_partition_gcd_events(
                values,
                lengths,
                fixed_indices=diagonal,
                trials=args.partition_trials,
                seed=args.seed,
                markers=markers,
            )
            print(
                f"partition {label} seed={args.seed} "
                f"trials={args.partition_trials}: "
                f"fixed={fixed} ({fixed / args.partition_trials:.10g}), "
                f"any={any_triple} ({any_triple / args.partition_trials:.10g})"
            )


if __name__ == "__main__":
    main()
