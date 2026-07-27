#!/usr/bin/env python3
"""Run the frozen 21-pair adjacent hidden-geometry census."""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed

from eye_mystery.hidden_geometry import (
    solve_hidden_geometry,
    solve_hidden_geometry_bitvector,
)
from eye_mystery.hidden_geometry_pairs import (
    canonical_context_pairs,
    planted_sat_pair,
    solve_context_pair,
    split_equidistant_triangle,
)


def _control(
    name: str,
    fragments,
    *,
    modulus: int,
    expected_union: str,
) -> None:
    groups = tuple(tuple(fragment) for fragment in fragments)
    combined = tuple(constraint for group in groups for constraint in group)
    outcomes = []
    for constraints in (*groups, combined):
        integer = solve_hidden_geometry(
            constraints,
            modulus=modulus,
            timeout_ms=5_000,
        )
        bitvector = solve_hidden_geometry_bitvector(
            constraints,
            modulus=modulus,
            timeout_ms=5_000,
        )
        outcomes.append((integer.outcome, bitvector.outcome))
    expected = (("sat", "sat"), ("sat", "sat"), (expected_union,) * 2)
    if tuple(outcomes) != expected:
        raise AssertionError(
            f"{name} control failed: expected {expected}, got {outcomes}"
        )
    print(f"control={name}; outcomes={outcomes}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout-ms", type=int, default=15_000)
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()

    _control(
        "joint-sat",
        planted_sat_pair(),
        modulus=7,
        expected_union="sat",
    )
    _control(
        "split-triangle",
        split_equidistant_triangle(),
        modulus=5,
        expected_union="unsat",
    )

    pairs = canonical_context_pairs()
    results = {}
    with ProcessPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(
                solve_context_pair,
                left,
                right,
                timeout_ms=args.timeout_ms,
            ): (left, right)
            for left, right in pairs
        }
        for future in as_completed(futures):
            result = future.result()
            results[(result.left, result.right)] = result
            fallback = (
                "-"
                if result.integer is None
                else result.integer.outcome
            )
            print(
                f"pair={result.left}+{result.right}; "
                f"constraints={result.constraints}; labels={result.labels}; "
                f"bitvector={result.bitvector.outcome}; "
                f"integer={fallback}; outcome={result.outcome}; "
                f"seconds={result.elapsed_seconds:.3f}",
                flush=True,
            )

    print("canonical census:")
    for pair in pairs:
        result = results[pair]
        print(
            f"{result.left}\t{result.right}\t{result.constraints}\t"
            f"{result.labels}\t{result.bitvector.outcome}\t"
            f"{'-' if result.integer is None else result.integer.outcome}\t"
            f"{result.outcome}\t{result.elapsed_seconds:.6f}"
        )
    counts = {
        outcome: sum(result.outcome == outcome for result in results.values())
        for outcome in ("sat", "unsat", "unknown")
    }
    print(f"summary={counts}")


if __name__ == "__main__":
    main()
