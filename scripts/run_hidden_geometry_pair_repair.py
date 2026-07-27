#!/usr/bin/env python3
"""Run the frozen one-sided search on unresolved geometry pairs."""

from __future__ import annotations

from eye_mystery.hidden_geometry import (
    constraint_holds,
    repair_hidden_geometry,
    repair_hidden_geometry_classes,
)
from eye_mystery.hidden_geometry_pairs import (
    pair_constraints,
    planted_sat_pair,
)


TARGET_PAIRS = (
    ("first-gap30", "first-cross"),
    ("last-west4", "last-east5"),
    ("last-east5", "last-east3"),
)


def _check_control() -> None:
    constraints = planted_sat_pair()[0] + planted_sat_pair()[1]
    direct = repair_hidden_geometry(
        constraints,
        modulus=7,
        restarts=10,
        steps_per_restart=100_000,
    )
    classes = repair_hidden_geometry_classes(
        constraints,
        modulus=7,
        restarts=10,
        steps_per_restart=100_000,
    )
    if not direct.complete or not classes.complete:
        raise AssertionError("pair-repair positive control failed")
    print(
        f"control=joint-sat; direct={direct.satisfied}/{direct.constraints}; "
        f"classes={classes.satisfied}/{classes.constraints}"
    )


def _verified(result, constraints) -> bool:
    return result.complete and all(
        constraint_holds(constraint, result.coordinates)
        for constraint in constraints
    )


def main() -> None:
    _check_control()
    for left, right in TARGET_PAIRS:
        constraints = pair_constraints(left, right)
        direct = repair_hidden_geometry(
            constraints,
            restarts=10,
            steps_per_restart=100_000,
        )
        classes = repair_hidden_geometry_classes(
            constraints,
            restarts=10,
            steps_per_restart=100_000,
        )
        if direct.complete and not _verified(direct, constraints):
            raise AssertionError("direct repair returned an invalid witness")
        if classes.complete and not _verified(classes, constraints):
            raise AssertionError("class repair returned an invalid witness")
        print(
            f"pair={left}+{right}; "
            f"direct={direct.satisfied}/{direct.constraints}; "
            f"direct_complete={direct.complete}; "
            f"class_constraints={classes.satisfied}/{classes.constraints}; "
            f"class_pairs={classes.class_edge_agreement}/{classes.class_edges}; "
            f"class_complete={classes.complete}",
            flush=True,
        )
        winner = direct if direct.complete else classes
        if winner.complete:
            print(
                "coordinates="
                + ",".join(map(str, winner.coordinates)),
                flush=True,
            )


if __name__ == "__main__":
    main()
