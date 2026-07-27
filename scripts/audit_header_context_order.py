#!/usr/bin/env python3
"""Audit finite-order header actions against nonliteral context maps."""

from __future__ import annotations

from eye_mystery.factoradic_headers import (
    compose,
    header_ranks,
    inverse,
    lexicographic_unrank,
    permutation_order,
)
from eye_mystery.partial_permutation import finite_order_completion
from eye_mystery.progression_certificate import context_mapping


CONTEXTS = (
    ("first-cross", "west1", 34, "east2", 39, 18),
    ("first-cross-late", "west1", 34, "east2", 74, 18),
    ("last-west4", "east4", 68, "west4", 71, 30),
    ("last-east5", "east4", 68, "east5", 69, 30),
    ("last-east3", "east4", 73, "east3", 64, 25),
)


def main() -> None:
    headers = {
        name: lexicographic_unrank(rank)
        for name, rank in header_ranks().items()
    }
    print(
        "context           source target mode     exponent feasible "
        "paths cycles filler/free"
    )
    convention_passes = {"source": True, "target": True, "relative": True}
    for name, source, source_start, target, target_start, length in CONTEXTS:
        mapping = context_mapping(
            source,
            source_start,
            target,
            target_start,
            length,
        )
        candidates = {
            "source": headers[source],
            "target": headers[target],
            "relative": compose(headers[target], inverse(headers[source])),
        }
        for mode, permutation in candidates.items():
            exponent = permutation_order(permutation)
            result = finite_order_completion(mapping, 83, exponent)
            convention_passes[mode] &= result.feasible
            paths = ",".join(map(str, result.path_vertex_lengths)) or "-"
            cycles = ",".join(map(str, result.cycle_lengths)) or "-"
            filler = (
                "-"
                if result.minimum_extra_vertices is None
                else str(result.minimum_extra_vertices)
            )
            print(
                f"{name:<17} {source:<6} {target:<6} {mode:<8} "
                f"{exponent:>8} {str(result.feasible):>8} "
                f"{paths:<17} {cycles:<8} "
                f"{filler}/{result.unobserved_vertices}"
            )
    print("global conventions:", convention_passes)


if __name__ == "__main__":
    main()
