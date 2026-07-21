#!/usr/bin/env python3
"""Report exact permutation-completion bounds for strong Eye contexts."""

from __future__ import annotations

from eye_mystery.partial_permutation import completion_stats
from eye_mystery.progression_certificate import context_mapping


CONTEXTS = (
    ("marker-e1-w1", "east1", 0, "west1", 0, 25),
    ("marker-e1-e2", "east1", 0, "east2", 0, 25),
    ("marker-w2-e3", "west2", 0, "east3", 0, 6),
    ("marker-w2-w3", "west2", 0, "west3", 0, 6),
    ("marker-e4-w4", "east4", 0, "west4", 0, 21),
    ("marker-e4-e5", "east4", 0, "east5", 0, 21),
    ("first-gap30", "west1", 34, "west1", 64, 18),
    ("first-cross", "west1", 34, "east2", 39, 18),
    ("first-cross-late", "west1", 34, "east2", 74, 18),
    ("first-gap28", "east1", 40, "east1", 68, 9),
    ("last-west4", "east4", 68, "west4", 71, 30),
    ("last-east5", "east4", 68, "east5", 69, 30),
    ("last-east3", "east4", 73, "east3", 64, 25),
)


def main() -> None:
    print(
        "context            edges fixed min-swaps even/odd min-support "
        "longest-path cycles signs"
    )
    for name, left, left_start, right, right_start, length in CONTEXTS:
        mapping = context_mapping(
            left, left_start, right, right_start, length
        )
        stats = completion_stats(mapping, 83)
        signs = (
            ("even" if stats.even_completion else "")
            + ("+" if stats.even_completion and stats.odd_completion else "")
            + ("odd" if stats.odd_completion else "")
        )
        longest_path = max(stats.path_lengths, default=0)
        nontrivial_cycles = tuple(
            length for length in stats.cycle_lengths if length > 1
        )
        cycles = ",".join(map(str, nontrivial_cycles)) or "-"
        print(
            f"{name:<18} {stats.observed_edges:>5} "
            f"{stats.observed_fixed_points:>5} "
            f"{stats.minimum_transpositions:>9} "
            f"{stats.minimum_even_transpositions!s:>4}/"
            f"{stats.minimum_odd_transpositions!s:<4} "
            f"{stats.minimum_support:>11} {longest_path:>12} "
            f"{cycles:>6} {signs}"
        )


if __name__ == "__main__":
    main()
