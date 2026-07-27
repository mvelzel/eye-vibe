"""Exact pair census for the frozen adjacent hidden-cycle model."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from itertools import combinations

from eye_mystery.hidden_geometry import (
    ChordConstraint,
    GeometrySolve,
    NONLITERAL_CONTEXT_SPECS,
    chord_constraints,
    solve_hidden_geometry,
    solve_hidden_geometry_bitvector,
)


CONTEXT_NAMES = tuple(spec[0] for spec in NONLITERAL_CONTEXT_SPECS)


@dataclass(frozen=True)
class ContextPairSolve:
    """One canonical two-context feasibility result."""

    left: str
    right: str
    constraints: int
    labels: int
    bitvector: GeometrySolve
    integer: GeometrySolve | None

    @property
    def outcome(self) -> str:
        if self.bitvector.outcome != "unknown":
            return self.bitvector.outcome
        if self.integer is None:
            return "unknown"
        return self.integer.outcome

    @property
    def elapsed_seconds(self) -> float:
        return self.bitvector.elapsed_seconds + (
            0.0 if self.integer is None else self.integer.elapsed_seconds
        )


def canonical_context_pairs() -> tuple[tuple[str, str], ...]:
    """Return all 21 unordered context pairs in authored registry order."""

    return tuple(combinations(CONTEXT_NAMES, 2))


def pair_constraints(left: str, right: str) -> tuple[ChordConstraint, ...]:
    """Return the unchanged lag-one constraints for one context pair."""

    if left == right:
        raise ValueError("a context pair must contain two different names")
    order = {name: index for index, name in enumerate(CONTEXT_NAMES)}
    if left not in order or right not in order:
        unknown = sorted({left, right} - set(CONTEXT_NAMES))
        raise ValueError(f"unknown context names: {unknown}")
    selected = {left, right}
    return tuple(
        constraint
        for constraint in chord_constraints(names=selected)
        if constraint.context in selected
    )


def solve_context_pair(
    left: str,
    right: str,
    *,
    timeout_ms: int = 15_000,
) -> ContextPairSolve:
    """Run the frozen bit-vector solver and integer timeout fallback."""

    constraints = pair_constraints(left, right)
    labels = {
        label for constraint in constraints for label in constraint.labels
    }
    bitvector = solve_hidden_geometry_bitvector(
        constraints,
        timeout_ms=timeout_ms,
    )
    integer = (
        solve_hidden_geometry(constraints, timeout_ms=timeout_ms)
        if bitvector.outcome == "unknown"
        else None
    )
    return ContextPairSolve(
        left,
        right,
        len(constraints),
        len(labels),
        bitvector,
        integer,
    )


def planted_sat_pair() -> tuple[
    tuple[ChordConstraint, ...],
    tuple[ChordConstraint, ...],
]:
    """Return two compatible planted context fragments over ``F7``."""

    return (
        (ChordConstraint("sat-left", 1, 0, 0, 1, 2, 3),),
        (ChordConstraint("sat-right", 1, 0, 1, 2, 3, 4),),
    )


def split_equidistant_triangle() -> tuple[
    tuple[ChordConstraint, ...],
    tuple[ChordConstraint, ...],
]:
    """Return two SAT fragments whose union is UNSAT over ``F5``."""

    return (
        (ChordConstraint("triangle-left", 1, 0, 0, 1, 0, 2),),
        (ChordConstraint("triangle-right", 1, 0, 0, 1, 1, 2),),
    )


def split_equidistant_star() -> tuple[
    tuple[ChordConstraint, ...],
    tuple[ChordConstraint, ...],
]:
    """Return halves whose union is SAT only by colliding leaves over ``F5``."""

    return (
        (ChordConstraint("star-left", 1, 0, 0, 1, 0, 2),),
        (ChordConstraint("star-right", 1, 0, 0, 1, 0, 3),),
    )


def solve_control_fragments(
    fragments: Sequence[Sequence[ChordConstraint]],
    *,
    modulus: int,
    timeout_ms: int = 5_000,
) -> tuple[tuple[GeometrySolve, GeometrySolve], ...]:
    """Solve each fragment and their union with both exact encodings."""

    groups = tuple(tuple(fragment) for fragment in fragments)
    combined = tuple(constraint for group in groups for constraint in group)
    return tuple(
        (
            solve_hidden_geometry(
                constraints,
                modulus=modulus,
                timeout_ms=timeout_ms,
            ),
            solve_hidden_geometry_bitvector(
                constraints,
                modulus=modulus,
                timeout_ms=timeout_ms,
            ),
        )
        for constraints in (*groups, combined)
    )
