#!/usr/bin/env python3
"""Run the frozen finite-domain hidden-geometry solver."""

from __future__ import annotations

from eye_mystery.hidden_geometry_domain import solve_hidden_geometry_domain
from eye_mystery.hidden_geometry_pairs import (
    pair_constraints,
    planted_sat_pair,
    split_equidistant_star,
)


SCALE_PAIR = ("last-west4", "last-east3")
TARGET_PAIRS = (
    ("first-gap30", "first-cross"),
    ("last-west4", "last-east5"),
    ("last-east5", "last-east3"),
)


def _show(label: str, result) -> None:
    print(
        f"{label}; outcome={result.outcome}; "
        f"constraints={result.constraints}; labels={result.labels}; "
        f"classes={result.classes}; nodes={result.nodes}; "
        f"backtracks={result.backtracks}; "
        f"seconds={result.elapsed_seconds:.3f}; reason={result.reason}",
        flush=True,
    )
    if result.outcome == "sat":
        print(
            "coordinates="
            + ",".join(
                f"{item}:{coordinate}"
                for item, coordinate in result.coordinates
            ),
            flush=True,
        )


def main() -> None:
    sat_left, sat_right = planted_sat_pair()
    star_left, star_right = split_equidistant_star()
    sat_control = solve_hidden_geometry_domain(
        sat_left + sat_right,
        modulus=7,
        timeout_ms=5_000,
    )
    star_control = solve_hidden_geometry_domain(
        star_left + star_right,
        modulus=5,
        timeout_ms=5_000,
    )
    if (sat_control.outcome, star_control.outcome) != ("sat", "unsat"):
        raise AssertionError("finite-domain primitive controls failed")
    print(
        f"controls=sat:{sat_control.outcome},star:{star_control.outcome}",
        flush=True,
    )

    scale = solve_hidden_geometry_domain(
        pair_constraints(*SCALE_PAIR),
        timeout_ms=180_000,
    )
    _show(f"scale={'+'.join(SCALE_PAIR)}", scale)
    if scale.outcome != "sat":
        print("scale gate failed; real targets not opened", flush=True)
        return

    counts = {"sat": 0, "unsat": 0, "unknown": 0}
    for left, right in TARGET_PAIRS:
        result = solve_hidden_geometry_domain(
            pair_constraints(left, right),
            timeout_ms=180_000,
        )
        counts[result.outcome] += 1
        _show(f"pair={left}+{right}", result)
    print(f"summary={counts}", flush=True)


if __name__ == "__main__":
    main()
