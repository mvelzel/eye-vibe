#!/usr/bin/env python3
"""Compose Eye isomorph maps and derive exact group-order lower bounds.

This transfers the useful first stage of the solved practice-``two`` attack to
the Eye corpus.  It does not complete any 83-point permutation.  Instead, it
uses only forced chains of observed edges; a clique of mutually conflicting
partial words is therefore a certificate that every compatible permutation
group contains at least that many distinct elements.
"""

from __future__ import annotations

import argparse
import random
import statistics
from collections import Counter
from dataclasses import dataclass

from eye_mystery.partial_group import (
    PartialWord,
    conflict_witness,
    distinctness_clique,
    generate_partial_words,
    verify_distinctness_clique,
)
from eye_mystery.progression_certificate import context_mapping


@dataclass(frozen=True)
class ContextSpec:
    name: str
    left: str
    left_start: int
    right: str
    right_start: int
    length: int


CONTEXTS = (
    ContextSpec("F_gap30", "west1", 34, "west1", 64, 18),
    ContextSpec("F_cross", "west1", 34, "east2", 39, 18),
    ContextSpec("F_cross_late", "west1", 34, "east2", 74, 18),
    ContextSpec("F_gap28", "east1", 40, "east1", 68, 9),
    ContextSpec("L_west4", "east4", 68, "west4", 71, 30),
    ContextSpec("L_east5", "east4", 68, "east5", 69, 30),
    ContextSpec("L_east3", "east4", 73, "east3", 64, 25),
)


def trimmed_mapping(spec: ContextSpec, trim: int) -> dict[int, int]:
    length = spec.length - 2 * trim
    if length < 1:
        raise ValueError(f"trim {trim} removes all of {spec.name}")
    return context_mapping(
        spec.left,
        spec.left_start + trim,
        spec.right,
        spec.right_start + trim,
        length,
    )


def pairwise_generator_conflicts(
    generators: dict[str, dict[int, int]],
) -> tuple[int, int]:
    names = sorted(generators)
    comparisons = 0
    conflicts = 0
    for index, left_name in enumerate(names):
        for right_name in names[index + 1 :]:
            comparisons += 1
            if (
                conflict_witness(
                    generators[left_name], generators[right_name]
                )
                is not None
            ):
                conflicts += 1
    return conflicts, comparisons


def describe_word(word: PartialWord) -> str:
    pairs = ",".join(f"{source}->{target}" for source, target in word.pairs)
    return f"{word.name} [{len(word.pairs)} edges: {pairs}]"


def randomized_generator(
    mapping: dict[int, int], rng: random.Random
) -> dict[int, int]:
    """Shuffle a map over its exact domain/image sets and fixed-point count."""

    sources = sorted(mapping)
    targets = list(mapping.values())
    fixed_points = sum(source == target for source, target in mapping.items())
    for _attempt in range(10_000):
        rng.shuffle(targets)
        candidate = dict(zip(sources, targets, strict=True))
        if (
            sum(source == target for source, target in candidate.items())
            == fixed_points
        ):
            return candidate
    raise RuntimeError("could not construct fixed-point-matched null map")


def closure_summary(
    generators: dict[str, dict[int, int]],
    max_depth: int,
    minimum_edges: int,
) -> tuple[tuple[PartialWord, ...], tuple[PartialWord, ...]]:
    words = generate_partial_words(
        generators,
        83,
        max_depth=max_depth,
        minimum_edges=minimum_edges,
    )
    clique = distinctness_clique(words)
    assert verify_distinctness_clique(clique)
    return words, clique


def run(
    trim: int,
    max_depth: int,
    minimum_edges: int,
    *,
    show_clique: bool,
    null_trials: int,
    seed: int,
) -> None:
    generators = {spec.name: trimmed_mapping(spec, trim) for spec in CONTEXTS}
    print(f"trim={trim}")
    print(
        "generator edges:",
        " ".join(f"{name}={len(mapping)}" for name, mapping in generators.items()),
    )
    conflicts, comparisons = pairwise_generator_conflicts(generators)
    print(f"direct generator conflicts: {conflicts}/{comparisons}")

    words, clique = closure_summary(generators, max_depth, minimum_edges)
    depth_counts = Counter(len(word.letters) for word in words)
    edge_counts = Counter(len(word.pairs) for word in words)
    print(
        f"unique forced restrictions: {len(words)}; "
        f"by depth={dict(sorted(depth_counts.items()))}; "
        f"edge range={min(edge_counts)}..{max(edge_counts)}"
    )

    print(
        f"certified group-order lower bound: {len(clique)} "
        "(greedy clique; not claimed maximal)"
    )
    if show_clique:
        for index, word in enumerate(clique, start=1):
            print(f"  {index:>2}. {describe_word(word)}")

    if null_trials:
        rng = random.Random(seed + trim)
        null_bounds = []
        null_restrictions = []
        for _trial in range(null_trials):
            randomized = {
                name: randomized_generator(mapping, rng)
                for name, mapping in generators.items()
            }
            null_words, null_clique = closure_summary(
                randomized, max_depth, minimum_edges
            )
            null_restrictions.append(len(null_words))
            null_bounds.append(len(null_clique))
        tail = sum(bound >= len(clique) for bound in null_bounds)
        print(
            f"matched null ({null_trials} trials, seed={seed + trim}): "
            f"restrictions min/median/max={min(null_restrictions)}/"
            f"{statistics.median(null_restrictions):g}/"
            f"{max(null_restrictions)}; clique min/median/max="
            f"{min(null_bounds)}/{statistics.median(null_bounds):g}/"
            f"{max(null_bounds)}; >= observed={tail}/{null_trials}"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trim", type=int, action="append")
    parser.add_argument("--max-depth", type=int, default=3)
    parser.add_argument("--minimum-edges", type=int, default=2)
    parser.add_argument("--show-clique", action="store_true")
    parser.add_argument("--null-trials", type=int, default=0)
    parser.add_argument("--seed", type=int, default=20260721)
    args = parser.parse_args()
    trims = tuple(args.trim) if args.trim is not None else (0, 1, 2, 3)
    for index, trim in enumerate(trims):
        if index:
            print()
        run(
            trim,
            args.max_depth,
            args.minimum_edges,
            show_clique=args.show_clique,
            null_trials=args.null_trials,
            seed=args.seed,
        )


if __name__ == "__main__":
    main()
