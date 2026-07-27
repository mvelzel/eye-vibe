"""Exact lazy-injection solver for hidden-cycle chord geometry."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Sequence
from dataclasses import dataclass
from itertools import combinations
from time import monotonic

import eye_mystery.hidden_geometry as geometry
from eye_mystery.hidden_geometry import (
    MODULUS,
    ChordConstraint,
    constraint_holds,
)


@dataclass(frozen=True)
class LazyGeometrySolve:
    outcome: str
    constraints: int
    labels: int
    rounds: int
    collision_cuts: int
    elapsed_seconds: float
    coordinates: tuple[tuple[int, int], ...] = ()
    reason: str | None = None


def solve_hidden_geometry_lazy_injection(
    constraints: Sequence[ChordConstraint],
    *,
    modulus: int = MODULUS,
    timeout_ms: int = 120_000,
) -> LazyGeometrySolve:
    """Solve exact chord geometry while generating injection cuts lazily."""

    if timeout_ms < 1:
        raise ValueError("timeout must be positive")
    started = monotonic()
    solver, coordinate_variables, _ = geometry._solver_for(
        constraints,
        modulus=modulus,
        timeout_ms=timeout_ms,
        assumptions=False,
        injective=False,
    )
    labels = tuple(sorted(coordinate_variables))
    rounds = 0
    cuts = 0
    while True:
        elapsed = monotonic() - started
        remaining_ms = timeout_ms - int(elapsed * 1_000)
        if remaining_ms <= 0:
            return LazyGeometrySolve(
                "unknown",
                len(constraints),
                len(labels),
                rounds,
                cuts,
                elapsed,
                reason="timeout",
            )
        solver.set(timeout=max(1, remaining_ms))
        outcome = solver.check()
        elapsed = monotonic() - started
        if outcome == geometry.z3.unknown:
            return LazyGeometrySolve(
                "unknown",
                len(constraints),
                len(labels),
                rounds,
                cuts,
                elapsed,
                reason=solver.reason_unknown(),
            )
        if outcome == geometry.z3.unsat:
            return LazyGeometrySolve(
                "unsat",
                len(constraints),
                len(labels),
                rounds,
                cuts,
                elapsed,
            )

        model = solver.model()
        resolved = tuple(
            (
                label,
                model.eval(
                    coordinate_variables[label],
                    model_completion=True,
                ).as_long(),
            )
            for label in labels
        )
        by_coordinate: dict[int, list[int]] = defaultdict(list)
        for label, coordinate in resolved:
            by_coordinate[coordinate].append(label)
        collisions = tuple(
            pair
            for group in by_coordinate.values()
            for pair in combinations(group, 2)
        )
        if not collisions:
            flat = [0] * modulus
            for label, coordinate in resolved:
                flat[label] = coordinate
            if not all(
                constraint_holds(
                    constraint,
                    flat,
                    modulus=modulus,
                )
                for constraint in constraints
            ):
                raise AssertionError(
                    "lazy-injection model violates a chord constraint"
                )
            return LazyGeometrySolve(
                "sat",
                len(constraints),
                len(labels),
                rounds,
                cuts,
                elapsed,
                tuple(sorted(resolved)),
            )

        for left, right in collisions:
            solver.add(
                coordinate_variables[left] != coordinate_variables[right]
            )
        cuts += len(collisions)
        rounds += 1
