"""Independent one-hot CNF encoding of hidden-cycle chord geometry."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from itertools import combinations
from time import monotonic

from eye_mystery.hidden_geometry import (
    MODULUS,
    ChordConstraint,
    chord_classes,
    constraint_holds,
)

try:
    from pysat.formula import IDPool
    from pysat.solvers import Solver
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    IDPool = None  # type: ignore[assignment,misc]
    Solver = None  # type: ignore[assignment,misc]


@dataclass(frozen=True)
class CNFGeometrySolve:
    outcome: str
    constraints: int
    labels: int
    classes: int
    variables: int
    clauses: int
    elapsed_seconds: float
    coordinates: tuple[tuple[int, int], ...] = ()


def pysat_available() -> bool:
    return Solver is not None and IDPool is not None


def _require_pysat() -> None:
    if not pysat_available():
        raise RuntimeError(
            "CNF geometry solving requires the optional python-sat package"
        )


def solve_hidden_geometry_cnf(
    constraints: Sequence[ChordConstraint],
    *,
    modulus: int = MODULUS,
    solver_name: str = "cadical195",
    fixed_coordinates: Mapping[int, int] | None = None,
) -> CNFGeometrySolve:
    """Solve the exact unsigned-chord model as a Boolean CNF."""

    _require_pysat()
    if modulus < 3 or modulus % 2 == 0:
        raise ValueError("modulus must be an odd integer at least three")
    if not constraints:
        raise ValueError("at least one constraint is required")
    started = monotonic()
    labels = tuple(
        sorted(
            {
                label
                for constraint in constraints
                for label in constraint.labels
            }
        )
    )
    label_set = set(labels)
    classes = chord_classes(constraints)
    if any(left == right for edges in classes for left, right in edges):
        raise ValueError("the CNF encoder expects nonzero chord edges")
    pool = IDPool()
    solver = Solver(name=solver_name)
    clauses = 0

    def add(clause: Sequence[int]) -> None:
        nonlocal clauses
        solver.add_clause(list(clause))
        clauses += 1

    def point(label: int, position: int) -> int:
        return pool.id(("point", label, position))

    def magnitude(class_index: int, value: int) -> int:
        return pool.id(("magnitude", class_index, value))

    def exactly_one(variables: Sequence[int]) -> None:
        add(variables)
        for left, right in combinations(variables, 2):
            add((-left, -right))

    for label in labels:
        exactly_one(tuple(point(label, position) for position in range(modulus)))
    for position in range(modulus):
        for left, right in combinations(labels, 2):
            add((-point(left, position), -point(right, position)))

    half = (modulus - 1) // 2
    for class_index, edges in enumerate(classes):
        exactly_one(
            tuple(
                magnitude(class_index, value)
                for value in range(1, half + 1)
            )
        )
        for left, right in edges:
            for value in range(1, half + 1):
                distance = magnitude(class_index, value)
                for position in range(modulus):
                    plus = (position + value) % modulus
                    minus = (position - value) % modulus
                    add(
                        (
                            -distance,
                            -point(left, position),
                            point(right, plus),
                            point(right, minus),
                        )
                    )
                    add(
                        (
                            -distance,
                            -point(right, position),
                            point(left, plus),
                            point(left, minus),
                        )
                    )

    anchor_left, anchor_right = next(
        (left, right)
        for constraint in constraints
        for left, right in (
            (constraint.source_left, constraint.source_right),
            (constraint.target_left, constraint.target_right),
        )
        if left != right
    )
    add((point(anchor_left, 0),))
    add((point(anchor_right, 1),))
    for label, position in (fixed_coordinates or {}).items():
        if label not in label_set:
            raise ValueError(f"fixed label {label} is not in the instance")
        if not 0 <= position < modulus:
            raise ValueError("fixed coordinate is outside the cycle")
        add((point(label, position),))

    satisfiable = solver.solve()
    elapsed = monotonic() - started
    variable_count = pool.top
    if not satisfiable:
        solver.delete()
        return CNFGeometrySolve(
            "unsat",
            len(constraints),
            len(labels),
            len(classes),
            variable_count,
            clauses,
            elapsed,
        )

    positive = {literal for literal in solver.get_model() if literal > 0}
    coordinates = tuple(
        (
            label,
            next(
                position
                for position in range(modulus)
                if point(label, position) in positive
            ),
        )
        for label in labels
    )
    solver.delete()
    flat = [0] * modulus
    for label, coordinate in coordinates:
        flat[label] = coordinate
    if len({coordinate for _, coordinate in coordinates}) != len(coordinates):
        raise AssertionError("CNF model violates coordinate injection")
    if not all(
        constraint_holds(constraint, flat, modulus=modulus)
        for constraint in constraints
    ):
        raise AssertionError("CNF model violates a chord constraint")
    return CNFGeometrySolve(
        "sat",
        len(constraints),
        len(labels),
        len(classes),
        variable_count,
        clauses,
        elapsed,
        coordinates,
    )
