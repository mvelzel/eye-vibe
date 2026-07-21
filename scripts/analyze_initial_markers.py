#!/usr/bin/env python3
"""Report evidence that the first trigrams may be metadata or list markers."""

from __future__ import annotations

import argparse

from eye_mystery.corpus import MESSAGE_ORDER
from eye_mystery.initials import (
    marker_grid_exit_signatures,
    marker_grid_permutation_null_counts,
    marker_summary,
    simulate_any_circular_digit_rule,
    simulate_marker_grid_events,
    trace_marker_digit,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rule-trials", type=int, default=0)
    parser.add_argument("--seed", type=int, default=20260721)
    parser.add_argument("--grid-null", action="store_true")
    parser.add_argument("--grid-trials", type=int, default=0)
    args = parser.parse_args()
    result = marker_summary()
    print("name   base5 value gcd(value,66)")
    for name, digits, value, divisor in zip(
        MESSAGE_ORDER,
        result["digits"],
        result["values"],
        result["gcd_with_66"],
    ):
        print(f"{name:5}  {''.join(map(str, digits))}   {value:>2}       {divisor:>2}")
    print()
    print("all initial values >26:", result["all_above_26"])
    print(
        "fixed null P(all >26, distinct):",
        f"{result['above_26_without_replacement_probability']:.8f}",
    )
    print(
        "fixed null P(all share a factor with universal second value 66):",
        f"{result['gcd_without_replacement_probability']:.8f}",
    )
    print("seven links before unpaired East 5:", result["seven_link_chain"])
    print("West 4 -> East 5 link:", result["last_link"])
    print(
        "fixed canonical-trigram null P(seven-link rule):",
        f"{result['chain_null_probability']:.10f}",
    )
    favorable, total = result["circular_chain_event_counts"]
    print("circular links:", result["circular_successor_links"])
    print("unique perfect rotation:", result["perfect_successor_rotation"])
    print(
        "exact fixed-rule P(any perfect cyclic rotation):",
        f"{favorable / total:.10f}",
    )
    if args.rule_trials:
        fixed, any_rule = simulate_any_circular_digit_rule(
            args.rule_trials, seed=args.seed
        )
        print(
            "simulated fixed / any digit-rule events:",
            fixed,
            any_rule,
            "of",
            args.rule_trials,
        )
    print("message sums:", result["message_sums"])
    print("sums divisible by 101:", result["sums_divisible_by_101"])
    print("largest gcd among all three-message subsets:", result["largest_triple_gcd"])
    print("subsets attaining it:", result["largest_triple_gcd_groups"])
    print("markers required for body checksum mod 101:", result["body_checksum_targets_mod_101"])
    print("actual marker offsets from those checksums:", result["marker_checksum_offsets_mod_101"])
    print("East 5 marker-direction exits (path, direction):")
    for digit_index in range(3):
        print(f"  digit {digit_index}:", trace_marker_digit("east5", digit_index))
    signatures = marker_grid_exit_signatures()
    print("all marker-grid exit signatures (None means no exit):")
    for name, signature in zip(MESSAGE_ORDER, signatures, strict=True):
        print(f"  {name:5}: {signature}")
    print(
        "starts with north/east/south exits:",
        tuple(
            name
            for name, signature in zip(
                MESSAGE_ORDER, signatures, strict=True
            )
            if signature == (1, 2, 3)
        ),
    )
    if args.grid_null:
        for hold in (False, True):
            fixed, histogram, total = marker_grid_permutation_null_counts(
                hold_east5_marker=hold
            )
            print(
                "grid marker-shuffle null",
                "(East 5 marker held)" if hold else "(all markers move)",
            )
            print("  fixed East 5 NES:", fixed, "of", total)
            print("  number-of-NES-starts histogram:", histogram)
    if args.grid_trials:
        print(
            "simulated grid events (fixed NES, any NES, >=3 NES, "
            "any repeated distinct-exit signature):",
            simulate_marker_grid_events(
                args.grid_trials, seed=args.seed
            ),
            "of",
            args.grid_trials,
        )


if __name__ == "__main__":
    main()
