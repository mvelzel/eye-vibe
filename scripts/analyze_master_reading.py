#!/usr/bin/env python3
"""Compare the proposed 125-symbol Master reading with canonical structure."""

from __future__ import annotations

from itertools import permutations

from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, trigram_values
from eye_mystery.isomorphs import pattern, repeated_patterns
from eye_mystery.master_reading import master_rule_values, visual_triangles
from eye_mystery.metrics import adjacent_doubles, index_of_coincidence


def nontrivial_pattern_classes(messages: tuple[tuple[int, ...], ...]) -> int:
    patterns = repeated_patterns(messages)
    return sum(
        candidate[0] != "."
        and candidate[-1] != "."
        and len(
            {
                tuple(messages[message][position : position + len(candidate)])
                for message, position in positions
            }
        )
        > 1
        for candidate, positions in patterns.items()
    )


def target_occurrences(messages: tuple[tuple[int, ...], ...]) -> int:
    target = "A.B.CB.AC"
    return sum(
        pattern(message[start : start + len(target)]) == target
        for message in messages
        for start in range(len(message) - len(target) + 1)
    )


def transformed_set(
    triangles: set[tuple[int, int, int]],
    substitution: tuple[int, ...],
    order: tuple[int, int, int],
) -> set[int]:
    return {
        25 * substitution[triangle[order[0]]]
        + 5 * substitution[triangle[order[1]]]
        + substitution[triangle[order[2]]]
        for triangle in triangles
    }


def full_coverage_census() -> None:
    down = set()
    up = set()
    for name in MESSAGE_ORDER:
        for index, triangle in enumerate(visual_triangles(MESSAGES[name])):
            (down if index % 2 == 0 else up).add(triangle)
    orders = tuple(permutations(range(3)))
    identity = tuple(range(5))
    one_swaps = [identity]
    for left in range(5):
        for right in range(left + 1, 5):
            substitution = list(identity)
            substitution[left], substitution[right] = substitution[right], substitution[left]
            one_swaps.append(tuple(substitution))

    for label, substitutions in (
        ("read orders only", (identity,)),
        ("identity or one value-swap per parity", tuple(one_swaps)),
        ("arbitrary value permutation per parity", tuple(permutations(range(5)))),
    ):
        down_sets = tuple(
            transformed_set(down, substitution, order)
            for substitution in substitutions
            for order in orders
        )
        up_sets = tuple(
            transformed_set(up, substitution, order)
            for substitution in substitutions
            for order in orders
        )
        hits = sum(len(down_set | up_set) == 125 for down_set in down_sets for up_set in up_sets)
        total = len(down_sets) * len(up_sets)
        print(f"{label}: {hits}/{total} ({hits / total:.6f}) full-coverage choices")

    down_swap = (0, 1, 4, 3, 2)
    up_swap = (0, 3, 2, 1, 4)
    hits = sum(
        len(
            transformed_set(down, down_swap, down_order)
            | transformed_set(up, up_swap, up_order)
        )
        == 125
        for down_order in orders
        for up_order in orders
    )
    print(f"fixed published value-swaps, free read orders: {hits}/36 full-coverage choices")


def main() -> None:
    canonical = tuple(trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER)
    master = tuple(master_rule_values(MESSAGES[name]) for name in MESSAGE_ORDER)
    for label, streams, alphabet_size in (
        ("canonical", canonical, 83),
        ("master", master, 125),
    ):
        combined = tuple(value for stream in streams for value in stream)
        print(
            f"{label}: symbols={len(set(combined))} doubles={adjacent_doubles(streams)} "
            f"normalized-IoC={index_of_coincidence(combined, alphabet_size):.4f} "
            f"pattern-classes={nontrivial_pattern_classes(streams)} "
            f"A.B.CB.AC={target_occurrences(streams)}"
        )
    down = {value for stream in master for value in stream[::2]}
    up = {value for stream in master for value in stream[1::2]}
    print(
        f"master parity sets: down={len(down)} up={len(up)} "
        f"intersection={len(down & up)} union={len(down | up)}"
    )
    full_coverage_census()


if __name__ == "__main__":
    main()
