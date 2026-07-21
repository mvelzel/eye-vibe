#!/usr/bin/env python3
"""Run cheap kill tests for several novel-mechanism families."""

from collections import Counter
from math import prod

from eye_mystery.blood_sieve import split_row_pair_values
from eye_mystery.breadth_probes import (
    best_affine_step_translation,
    reuse_stack_distances,
)
from eye_mystery.conformance_grid import marker_control_edge
from eye_mystery.corpus import (
    MESSAGES,
    MESSAGE_ORDER,
    ROW_PAIR_TRIGRAM_LENGTHS,
    trigram_values,
)


def main() -> None:
    streams = {name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER}
    bodies = {name: stream[1:] for name, stream in streams.items()}

    full_rows = tuple(
        row
        for name in MESSAGE_ORDER
        for row in split_row_pair_values(
            MESSAGES[name], ROW_PAIR_TRIGRAM_LENGTHS[name]
        )
        if len(row) == 26
    )
    unique_counts = tuple(len(set(row)) for row in full_rows)
    all_unique_probability = prod((83 - index) / 82 for index in range(1, 26))
    print("complete 26-wide rows:", len(full_rows))
    print("row unique-count distribution:", dict(sorted(Counter(unique_counts).items())))
    print("all-unique rows:", unique_counts.count(26))
    print(
        "uniform-no-double P(no all-unique row):",
        (1 - all_unique_probability) ** len(full_rows),
    )

    distances = tuple(
        distance
        for name in MESSAGE_ORDER
        for distance in reuse_stack_distances(bodies[name])
    )
    print("repeat events:", len(distances))
    print("reuse stack distance <= 8:", sum(value <= 8 for value in distances))
    print("maximum reuse stack distance:", max(distances))

    best_total, translation, state_counts = best_affine_step_translation(
        tuple(bodies.values()), modulus=101
    )
    print("best Z101 affine-step translation:", translation)
    print("best total unique cumulative states:", best_total)
    print("per-message cumulative states:", state_counts)

    residues_by_edge: dict[tuple[int, int], list[int]] = {}
    for name in MESSAGE_ORDER:
        edge = marker_control_edge(streams[name][0])
        residues_by_edge.setdefault(edge, []).append(sum(streams[name]) % 101)
    print(
        "repeated edge residues:",
        {edge: values for edge, values in residues_by_edge.items() if len(values) > 1},
    )


if __name__ == "__main__":
    main()
