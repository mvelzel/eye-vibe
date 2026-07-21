#!/usr/bin/env python3
"""Run the predeclared breadth-first architecture probes."""

from __future__ import annotations

import argparse
from random import Random

from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, trigram_values
from eye_mystery.wide_architectures import (
    aligned_determinant_zero_count,
    best_affine_recurrence,
    best_affine_recurrence_from_counts,
    best_debruijn_overlap,
    header_moment_scores,
    trie_transition_counts,
)


def shuffled_bodies(
    bodies: tuple[tuple[int, ...], ...], random: Random
) -> tuple[tuple[int, ...], ...]:
    output = []
    for body in bodies:
        values = list(body)
        random.shuffle(values)
        output.append(tuple(values))
    return tuple(output)


def exceedance(observed: int, null: list[int]) -> str:
    hits = sum(value >= observed for value in null)
    return f"{hits + 1}/{len(null) + 1} = {(hits + 1)/(len(null) + 1):.6f}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=20260721)
    parser.add_argument("--path-trials", type=int, default=5000)
    parser.add_argument("--recurrence-trials", type=int, default=200)
    parser.add_argument("--recurrence-relabel-trials", type=int, default=500)
    parser.add_argument("--grid-trials", type=int, default=5000)
    args = parser.parse_args()

    streams = {name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER}
    bodies_by_name = {name: stream[1:] for name, stream in streams.items()}
    bodies = tuple(bodies_by_name[name] for name in MESSAGE_ORDER)
    random = Random(args.seed)

    path = best_debruijn_overlap(bodies)
    path_null = [
        best_debruijn_overlap(shuffled_bodies(bodies, random)).matches
        for _ in range(args.path_trials)
    ]
    print("base-5 order-two path:")
    print("  best:", path)
    print("  null range:", min(path_null), max(path_null))
    print("  upper-tail exceedance:", exceedance(path.matches, path_null))

    recurrence = best_affine_recurrence(bodies)
    recurrence_null = [
        best_affine_recurrence(shuffled_bodies(bodies, random)).matches
        for _ in range(args.recurrence_trials)
    ]
    print("F83 first-order affine recurrence:")
    print("  best:", recurrence)
    print("  null range:", min(recurrence_null), max(recurrence_null))
    print(
        "  upper-tail exceedance:",
        exceedance(recurrence.matches, recurrence_null),
    )
    alphabet = tuple(range(83))
    recurrence_relabel_null = []
    for _ in range(args.recurrence_relabel_trials):
        relabeled = list(alphabet)
        random.shuffle(relabeled)
        relabeled_bodies = tuple(
            tuple(relabeled[value] for value in body) for body in bodies
        )
        recurrence_relabel_null.append(
            best_affine_recurrence(relabeled_bodies).matches
        )
    print(
        "  equality/prefix-preserving global-relabel null:",
        min(recurrence_relabel_null),
        max(recurrence_relabel_null),
    )
    print(
        "  global-relabel upper-tail:",
        exceedance(recurrence.matches, recurrence_relabel_null),
    )
    merged_transitions = trie_transition_counts(bodies)
    merged_recurrence = best_affine_recurrence_from_counts(merged_transitions)
    print("  merge-copied-prefixes-once best:", merged_recurrence)
    matching_pairs = tuple(
        (current, (recurrence.multiplier * current + recurrence.translation) % 83)
        for current in range(83)
        if any(
            left == current
            and right
            == (recurrence.multiplier * current + recurrence.translation) % 83
            for body in bodies
            for left, right in zip(body, body[1:])
        )
    )
    print("  observed best distinct matching pairs:", len(matching_pairs))

    print("aligned 3x3 determinant closures after body depth 24:")
    for modulus in (83, 101):
        observed, total = aligned_determinant_zero_count(
            bodies_by_name,
            MESSAGE_ORDER,
            modulus=modulus,
            start=24,
        )
        null = []
        for _ in range(args.grid_trials):
            rotations = {
                name: random.randrange(len(body))
                for name, body in bodies_by_name.items()
            }
            hits, _ = aligned_determinant_zero_count(
                bodies_by_name,
                MESSAGE_ORDER,
                modulus=modulus,
                start=24,
                rotations=rotations,
            )
            null.append(hits)
        print(
            f"  mod {modulus}: {observed}/{total}; null {min(null)}..{max(null)};",
            "upper-tail",
            exceedance(observed, null),
        )

    moments = header_moment_scores(streams)
    print("systematic polynomial header moments:")
    for result in sorted(
        moments,
        key=lambda item: (-item.matches, item.modulus, item.degree, item.sign),
    )[:10]:
        print(" ", result)


if __name__ == "__main__":
    main()
