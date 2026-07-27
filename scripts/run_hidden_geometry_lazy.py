#!/usr/bin/env python3
"""Run the frozen lazy-injection solver on unresolved context pairs."""

from __future__ import annotations

from eye_mystery.hidden_geometry_lazy import (
    solve_hidden_geometry_lazy_injection,
)
from eye_mystery.hidden_geometry_pairs import (
    pair_constraints,
    planted_sat_pair,
    split_equidistant_star,
)


TARGET_PAIRS = (
    ("first-gap30", "first-cross"),
    ("last-west4", "last-east5"),
    ("last-east5", "last-east3"),
)


def _check_controls() -> None:
    sat_left, sat_right = planted_sat_pair()
    star_left, star_right = split_equidistant_star()
    observed = tuple(
        solve_hidden_geometry_lazy_injection(
            constraints,
            modulus=modulus,
            timeout_ms=5_000,
        ).outcome
        for constraints, modulus in (
            (sat_left, 7),
            (sat_right, 7),
            (sat_left + sat_right, 7),
            (star_left, 5),
            (star_right, 5),
            (star_left + star_right, 5),
        )
    )
    expected = ("sat", "sat", "sat", "sat", "sat", "unsat")
    if observed != expected:
        raise AssertionError(
            f"lazy-injection controls failed: expected {expected}, got {observed}"
        )
    print(f"controls={observed}")


def main() -> None:
    _check_controls()
    counts = {"sat": 0, "unsat": 0, "unknown": 0}
    for left, right in TARGET_PAIRS:
        result = solve_hidden_geometry_lazy_injection(
            pair_constraints(left, right),
            timeout_ms=120_000,
        )
        counts[result.outcome] += 1
        print(
            f"pair={left}+{right}; outcome={result.outcome}; "
            f"constraints={result.constraints}; labels={result.labels}; "
            f"rounds={result.rounds}; cuts={result.collision_cuts}; "
            f"seconds={result.elapsed_seconds:.3f}; reason={result.reason}",
            flush=True,
        )
        if result.outcome == "sat":
            print(
                "coordinates="
                + ",".join(
                    f"{label}:{coordinate}"
                    for label, coordinate in result.coordinates
                ),
                flush=True,
            )
    print(f"summary={counts}")


if __name__ == "__main__":
    main()
