#!/usr/bin/env python3
"""Calibrate the post-hoc 34x27 merged-trie checksum layout strictly."""

from __future__ import annotations

import argparse
from collections import Counter
from random import Random

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.marker_orders import MARKER_TRIE_ORDER
from eye_mystery.prefix_hierarchy import serialize_trie_edges
from eye_mystery.trie_checksum import random_signature_preserving_relabeling


def count_vector(values: tuple[int, ...]) -> tuple[int, ...]:
    counts = Counter(values)
    return tuple(counts[value] for value in range(83))


def closure_count(values: tuple[int, ...]) -> int:
    """Count zero row and column sums in a 34x27 layout modulo 101."""

    if len(values) != 34 * 27:
        raise ValueError("layout must contain exactly 918 values")
    rows = tuple(values[index : index + 27] for index in range(0, len(values), 27))
    return sum(sum(row) % 101 == 0 for row in rows) + sum(
        sum(row[column] for row in rows) % 101 == 0 for column in range(27)
    )


def phase_family_closure_count(values: tuple[int, ...]) -> int:
    """Maximize the closure count over all 27 within-record start phases."""

    return max(
        closure_count(values[phase:] + values[:phase]) for phase in range(27)
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--accepted", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=20260721)
    parser.add_argument("--phase-family", action="store_true")
    args = parser.parse_args()
    if args.accepted < 1:
        parser.error("--accepted must be positive")

    streams = {name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER}
    bodies = {name: values[1:] for name, values in streams.items()}
    layouts = tuple(
        serialize_trie_edges(
            bodies,
            MARKER_TRIE_ORDER,
            start=0,
            breadth_first=breadth_first,
        )
        for breadth_first in (False, True)
    )
    observed_each = tuple(closure_count(layout) for layout in layouts)
    observed = max(observed_each)
    observed_phase_scores = tuple(
        tuple(
            closure_count(layout[phase:] + layout[:phase])
            for phase in range(27)
        )
        for layout in layouts
    )
    observed_phase_family = max(map(max, observed_phase_scores))
    multiplicities = count_vector(layouts[0])
    diagonal = tuple(
        count_vector(streams[name]) for name in ("east1", "east3", "east5")
    )
    fixed_markers = tuple(streams[name][0] for name in MESSAGE_ORDER)

    rng = Random(args.seed)
    distribution: Counter[int] = Counter()
    phase_distribution: Counter[int] = Counter()
    attempts = 0
    accepted = 0
    while accepted < args.accepted:
        attempts += 1
        mapping = random_signature_preserving_relabeling(
            83,
            diagonal,
            rng,
            fixed_labels=fixed_markers,
        )
        if (
            sum(
                multiplicity * mapping[label]
                for label, multiplicity in enumerate(multiplicities)
            )
            % 101
            != 0
        ):
            continue
        accepted += 1
        relabeled_layouts = tuple(
            tuple(mapping[value] for value in layout) for layout in layouts
        )
        distribution[max(map(closure_count, relabeled_layouts))] += 1
        if args.phase_family:
            phase_distribution[
                max(map(phase_family_closure_count, relabeled_layouts))
            ] += 1

    hits = sum(count for score, count in distribution.items() if score >= observed)
    print("observed DFS/BFS closure counts:", observed_each)
    print("observed selected maximum:", observed)
    print("observed phase scores:", observed_phase_scores)
    print("accepted / attempted:", accepted, attempts)
    print("conditional distribution:", tuple(sorted(distribution.items())))
    print(
        "conditional upper tail:",
        f"{hits + 1}/{accepted + 1} = {(hits + 1)/(accepted + 1):.8f}",
    )
    if args.phase_family:
        phase_hits = sum(
            count
            for score, count in phase_distribution.items()
            if score >= observed_phase_family
        )
        print("phase-family selected maximum:", observed_phase_family)
        print("phase-family distribution:", tuple(sorted(phase_distribution.items())))
        print(
            "phase-family upper tail:",
            f"{phase_hits + 1}/{accepted + 1} = "
            f"{(phase_hits + 1)/(accepted + 1):.8f}",
        )


if __name__ == "__main__":
    main()
