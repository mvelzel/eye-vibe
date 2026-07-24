"""Exact hidden-cycle constraints induced by Eye-message isomorphs.

The seven nonliteral aligned windows may represent repeated plaintext under
different cipher states.  This module tests a deliberately weak consequence:
corresponding textual chords have equal *unsigned* length in one unknown
cyclic ordering of the 83 visible labels.  Each chord may independently
reverse direction, so this is weaker than requiring a context map to be one
affine or dihedral transformation.
"""

from __future__ import annotations

import random
from collections import Counter
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from itertools import product
from time import monotonic

from eye_mystery.corpus import MESSAGES, trigram_values
from eye_mystery.ninth_causal import CONTEXT_SPECS

try:
    import z3
except ModuleNotFoundError:  # pragma: no cover - exercised without optional Z3
    z3 = None  # type: ignore[assignment]


MODULUS = 83
NONLITERAL_CONTEXT_SPECS = CONTEXT_SPECS[6:]
FIRST_FAMILY_NAMES = frozenset(spec[0] for spec in NONLITERAL_CONTEXT_SPECS[:4])
LAST_FAMILY_NAMES = frozenset(spec[0] for spec in NONLITERAL_CONTEXT_SPECS[4:])
LAST_SHORT_CORE_KEYS = (
    ("last-east5", 3, 13),
    ("last-east5", 1, 16),
    ("last-east3", 2, 9),
    ("last-east3", 3, 9),
    ("last-east3", 2, 11),
    ("last-east3", 1, 12),
    ("last-east5", 2, 15),
    ("last-east5", 2, 13),
)


@dataclass(frozen=True)
class ChordConstraint:
    """One equality of unsigned cyclic chord lengths."""

    context: str
    lag: int
    index: int
    source_left: int
    source_right: int
    target_left: int
    target_right: int

    @property
    def labels(self) -> tuple[int, int, int, int]:
        return (
            self.source_left,
            self.source_right,
            self.target_left,
            self.target_right,
        )


@dataclass(frozen=True)
class GeometrySolve:
    outcome: str
    constraints: int
    labels: int
    elapsed_seconds: float
    coordinates: tuple[tuple[int, int], ...] = ()
    core: tuple[ChordConstraint, ...] = ()
    reason: str | None = None


@dataclass(frozen=True)
class GeometrySearch:
    satisfied: int
    constraints: int
    steps: int
    restart: int
    coordinates: tuple[int, ...]
    class_edge_agreement: int = 0
    class_edges: int = 0

    @property
    def complete(self) -> bool:
        return self.satisfied == self.constraints


@dataclass(frozen=True)
class LinearCoreCertificate:
    constraints: int
    labels: int
    orientation_branches: int
    forced_collision_branches: int
    collision_witness_counts: tuple[tuple[tuple[int, int], int], ...]
    deletion_survivors: tuple[int, ...]


def z3_available() -> bool:
    return z3 is not None


def _require_z3() -> None:
    if z3 is None:
        raise RuntimeError(
            "hidden-geometry solving requires the optional z3 Python package"
        )


def context_sequences(
    *,
    names: Iterable[str] | None = None,
) -> tuple[tuple[str, tuple[int, ...], tuple[int, ...]], ...]:
    """Return the seven fixed nonliteral aligned contexts."""

    selected = None if names is None else frozenset(names)
    contexts = []
    for name, left, left_start, right, right_start, length in (
        NONLITERAL_CONTEXT_SPECS
    ):
        if selected is not None and name not in selected:
            continue
        left_values = trigram_values(MESSAGES[left])[
            left_start : left_start + length
        ]
        right_values = trigram_values(MESSAGES[right])[
            right_start : right_start + length
        ]
        contexts.append((name, left_values, right_values))
    if selected is not None:
        missing = selected - {name for name, _, _ in contexts}
        if missing:
            raise ValueError(f"unknown context names: {sorted(missing)}")
    return tuple(contexts)


def chord_constraints(
    *,
    lags: Iterable[int] = (1,),
    names: Iterable[str] | None = None,
) -> tuple[ChordConstraint, ...]:
    """Build aligned chord equalities for the requested positive lags."""

    selected_lags = tuple(sorted(set(lags)))
    if not selected_lags or selected_lags[0] < 1:
        raise ValueError("lags must contain positive integers")
    constraints = []
    for context, source, target in context_sequences(names=names):
        for lag in selected_lags:
            if lag >= len(source):
                continue
            constraints.extend(
                ChordConstraint(
                    context,
                    lag,
                    index,
                    source[index],
                    source[index + lag],
                    target[index],
                    target[index + lag],
                )
                for index in range(len(source) - lag)
            )
    return tuple(constraints)


def last_short_core() -> tuple[ChordConstraint, ...]:
    """Return the frozen eight-equation last-family contradiction."""

    available = {
        (item.context, item.lag, item.index): item
        for item in chord_constraints(
            names=LAST_FAMILY_NAMES,
            lags=(1, 2, 3),
        )
    }
    return tuple(available[key] for key in LAST_SHORT_CORE_KEYS)


def unsigned_chord(
    coordinates: Sequence[int], left: int, right: int, *, modulus: int = MODULUS
) -> int:
    """Return the canonical magnitude in ``Z_modulus/{±1}``."""

    difference = (coordinates[right] - coordinates[left]) % modulus
    return min(difference, (-difference) % modulus)


def constraint_holds(
    constraint: ChordConstraint,
    coordinates: Sequence[int],
    *,
    modulus: int = MODULUS,
) -> bool:
    return unsigned_chord(
        coordinates,
        constraint.source_left,
        constraint.source_right,
        modulus=modulus,
    ) == unsigned_chord(
        coordinates,
        constraint.target_left,
        constraint.target_right,
        modulus=modulus,
    )


def chord_classes(
    constraints: Sequence[ChordConstraint],
) -> tuple[tuple[tuple[int, int], ...], ...]:
    """Return transitive classes of undirected edges forced to equal length."""

    parent: dict[tuple[int, int], tuple[int, int]] = {}

    def edge(left: int, right: int) -> tuple[int, int]:
        return min((left, right), (right, left))

    def find(item: tuple[int, int]) -> tuple[int, int]:
        parent.setdefault(item, item)
        while parent[item] != item:
            parent[item] = parent[parent[item]]
            item = parent[item]
        return item

    def union(left: tuple[int, int], right: tuple[int, int]) -> None:
        left_root = find(left)
        right_root = find(right)
        if left_root != right_root:
            parent[max(left_root, right_root)] = min(left_root, right_root)

    for constraint in constraints:
        union(
            edge(constraint.source_left, constraint.source_right),
            edge(constraint.target_left, constraint.target_right),
        )
    groups: dict[tuple[int, int], list[tuple[int, int]]] = {}
    for item in parent:
        groups.setdefault(find(item), []).append(item)
    return tuple(
        tuple(sorted(items))
        for _, items in sorted(groups.items())
    )


def _rref_mod(
    rows: Sequence[Sequence[int]], modulus: int
) -> tuple[tuple[tuple[int, ...], ...], tuple[int, ...]]:
    matrix = [
        [value % modulus for value in row]
        for row in rows
        if any(value % modulus for value in row)
    ]
    if not matrix:
        return (), ()
    width = len(matrix[0])
    pivots = []
    pivot_row = 0
    for column in range(width):
        selected = next(
            (
                row
                for row in range(pivot_row, len(matrix))
                if matrix[row][column]
            ),
            None,
        )
        if selected is None:
            continue
        matrix[pivot_row], matrix[selected] = matrix[selected], matrix[pivot_row]
        inverse = pow(matrix[pivot_row][column], -1, modulus)
        matrix[pivot_row] = [
            value * inverse % modulus for value in matrix[pivot_row]
        ]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                (value - factor * pivot) % modulus
                for value, pivot in zip(
                    matrix[row], matrix[pivot_row], strict=True
                )
            ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return tuple(tuple(row) for row in matrix[:pivot_row]), tuple(pivots)


def _in_row_space(
    vector: Sequence[int],
    basis: Sequence[Sequence[int]],
    pivots: Sequence[int],
    modulus: int,
) -> bool:
    residual = [value % modulus for value in vector]
    for row, pivot in zip(basis, pivots, strict=True):
        if not residual[pivot]:
            continue
        factor = residual[pivot]
        residual = [
            (value - factor * basis_value) % modulus
            for value, basis_value in zip(residual, row, strict=True)
        ]
    return not any(residual)


def forced_collision(
    constraints: Sequence[ChordConstraint],
    orientations: Sequence[int],
    *,
    modulus: int = MODULUS,
) -> tuple[int, int] | None:
    """Return a label pair forced equal by one orientation branch."""

    if len(constraints) != len(orientations):
        raise ValueError("one orientation is required per constraint")
    if any(orientation not in (-1, 1) for orientation in orientations):
        raise ValueError("orientations must be -1 or +1")
    labels = tuple(
        sorted({label for item in constraints for label in item.labels})
    )
    indices = {label: index for index, label in enumerate(labels)}
    rows = []
    for item, orientation in zip(constraints, orientations, strict=True):
        row = [0] * len(labels)
        row[indices[item.source_right]] += 1
        row[indices[item.source_left]] -= 1
        row[indices[item.target_right]] -= orientation
        row[indices[item.target_left]] += orientation
        rows.append(row)
    basis, pivots = _rref_mod(rows, modulus)
    for left_index, left in enumerate(labels):
        for right in labels[left_index + 1 :]:
            difference = [0] * len(labels)
            difference[indices[left]] = 1
            difference[indices[right]] = -1
            if _in_row_space(difference, basis, pivots, modulus):
                return left, right
    return None


def linear_core_certificate(
    constraints: Sequence[ChordConstraint] | None = None,
    *,
    modulus: int = MODULUS,
) -> LinearCoreCertificate:
    """Enumerate all sign branches of the short exact contradiction.

    If no coordinate equality is forced in a branch, an injective assignment
    exists: the solution subspace is not contained in any of its
    ``n choose 2`` equality hyperplanes, and there are fewer such hyperplanes
    than the field size. The frozen core uses 11 labels, hence 55 < 83.
    """

    selected = last_short_core() if constraints is None else tuple(constraints)
    labels = {label for item in selected for label in item.labels}
    equality_hyperplanes = len(labels) * (len(labels) - 1) // 2
    if equality_hyperplanes >= modulus:
        raise ValueError("the finite-union injectivity certificate needs nC2 < p")
    witnesses: Counter[tuple[int, int]] = Counter()
    survivors = 0
    for orientations in product((-1, 1), repeat=len(selected)):
        collision = forced_collision(
            selected, orientations, modulus=modulus
        )
        if collision is None:
            survivors += 1
        else:
            witnesses[collision] += 1
    deletion_survivors = []
    for removed in range(len(selected)):
        subset = selected[:removed] + selected[removed + 1 :]
        deletion_survivors.append(
            sum(
                forced_collision(subset, orientations, modulus=modulus) is None
                for orientations in product((-1, 1), repeat=len(subset))
            )
        )
    branches = 2 ** len(selected)
    return LinearCoreCertificate(
        len(selected),
        len(labels),
        branches,
        branches - survivors,
        tuple(sorted(witnesses.items())),
        tuple(deletion_survivors),
    )


def _solver_for(
    constraints: Sequence[ChordConstraint],
    *,
    modulus: int,
    timeout_ms: int,
    assumptions: bool,
    injective: bool,
):
    _require_z3()
    if modulus < 3:
        raise ValueError("modulus must be at least three")
    labels = tuple(sorted({label for constraint in constraints for label in constraint.labels}))
    if len(labels) < 2:
        raise ValueError("at least two labels are required")

    solver = z3.SolverFor("QF_FD")
    solver.set(timeout=timeout_ms)
    coordinates = {
        label: z3.Int(f"hidden_coordinate_{label}") for label in labels
    }
    for coordinate in coordinates.values():
        solver.add(coordinate >= 0, coordinate < modulus)
    if injective:
        solver.add(z3.Distinct(*coordinates.values()))

    # Equality-of-distance equations are invariant under translation and under
    # multiplication by any nonzero field element. Normalize the endpoints of
    # an actually constrained edge; this also fixes one distance class to one.
    anchor_left, anchor_right = next(
        (left, right)
        for constraint in constraints
        for left, right in (
            (constraint.source_left, constraint.source_right),
            (constraint.target_left, constraint.target_right),
        )
        if left != right
    )
    solver.add(coordinates[anchor_left] == 0)
    solver.add(coordinates[anchor_right] == 1)

    guards = []
    if assumptions:
        # Keep each observed equality independently guarded so an UNSAT core
        # maps back to original aligned positions.
        for number, constraint in enumerate(constraints):
            source_delta = (
                coordinates[constraint.source_right]
                - coordinates[constraint.source_left]
            )
            target_delta = (
                coordinates[constraint.target_right]
                - coordinates[constraint.target_left]
            )
            equation = z3.Or(
                *(
                    source_delta == orientation * target_delta + shift
                    for orientation in (-1, 1)
                    for shift in (-modulus, 0, modulus)
                )
            )
            guard = z3.Bool(f"hidden_chord_{number}")
            guards.append(guard)
            solver.add(z3.Implies(guard, equation))
    else:
        # Factor the equalities through their transitive edge classes. This is
        # logically equivalent but replaces four-coordinate disjunctions by a
        # shared positive magnitude and is much faster on the Eye incidence
        # graph.
        for class_index, edges in enumerate(chord_classes(constraints)):
            magnitude = z3.Int(f"hidden_magnitude_{class_index}")
            if any(left == right for left, right in edges):
                solver.add(magnitude == 0)
            else:
                solver.add(magnitude >= 1, magnitude <= (modulus - 1) // 2)
            for left, right in edges:
                delta = coordinates[right] - coordinates[left]
                solver.add(
                    z3.Or(
                        *(
                            delta == orientation * magnitude + shift
                            for orientation in (-1, 1)
                            for shift in (-modulus, 0, modulus)
                        )
                    )
                )
    return solver, coordinates, tuple(guards)


def solve_hidden_geometry(
    constraints: Sequence[ChordConstraint],
    *,
    modulus: int = MODULUS,
    timeout_ms: int = 60_000,
    extract_core: bool = False,
    injective: bool = True,
) -> GeometrySolve:
    """Solve one exact unsigned-chord instance.

    Coordinates are returned only for labels touched by the constraints.
    Such an injection always extends to a complete 83-label wheel.
    """

    started = monotonic()
    solver, coordinates, guards = _solver_for(
        constraints,
        modulus=modulus,
        timeout_ms=timeout_ms,
        assumptions=extract_core,
        injective=injective,
    )
    outcome = solver.check(*guards) if extract_core else solver.check()
    elapsed = monotonic() - started
    if outcome == z3.unknown:
        return GeometrySolve(
            "unknown",
            len(constraints),
            len(coordinates),
            elapsed,
            reason=solver.reason_unknown(),
        )
    if outcome == z3.unsat:
        core = ()
        if extract_core:
            guard_index = {guard: index for index, guard in enumerate(guards)}
            core = tuple(
                constraints[guard_index[guard]]
                for guard in solver.unsat_core()
            )
        return GeometrySolve(
            "unsat",
            len(constraints),
            len(coordinates),
            elapsed,
            core=core,
        )

    model = solver.model()
    resolved = tuple(
        sorted(
            (
                label,
                model.eval(coordinate, model_completion=True).as_long(),
            )
            for label, coordinate in coordinates.items()
        )
    )
    flat = [0] * modulus
    for label, coordinate in resolved:
        flat[label] = coordinate
    if not all(
        constraint_holds(constraint, flat, modulus=modulus)
        for constraint in constraints
    ):
        raise AssertionError("Z3 model does not satisfy chord constraints")
    return GeometrySolve(
        "sat",
        len(constraints),
        len(coordinates),
        elapsed,
        coordinates=resolved,
    )


def solve_hidden_geometry_boolean(
    constraints: Sequence[ChordConstraint],
    *,
    modulus: int = MODULUS,
    timeout_ms: int = 60_000,
) -> GeometrySolve:
    """Solve the same model as an explicit finite-domain Boolean CSP.

    The integer and Boolean encodings are logically independent. This form
    uses one-hot point coordinates and one-hot distance-class magnitudes, with
    local implication clauses for every edge. It is larger but can outperform
    arithmetic search on densely overlapping context families.
    """

    _require_z3()
    if modulus < 3 or modulus % 2 == 0:
        raise ValueError("modulus must be an odd integer at least three")
    if not constraints:
        raise ValueError("at least one constraint is required")
    started = monotonic()
    labels = tuple(
        sorted({label for constraint in constraints for label in constraint.labels})
    )
    classes = chord_classes(constraints)
    solver = z3.SolverFor("QF_FD")
    solver.set(timeout=timeout_ms)
    positions = {
        label: tuple(
            z3.Bool(f"point_{label}_at_{position}")
            for position in range(modulus)
        )
        for label in labels
    }
    for variables in positions.values():
        solver.add(z3.PbEq(tuple((variable, 1) for variable in variables), 1))
    for position in range(modulus):
        solver.add(
            z3.PbLe(
                tuple((positions[label][position], 1) for label in labels),
                1,
            )
        )

    anchor_left = constraints[0].source_left
    anchor_right = constraints[0].source_right
    solver.add(positions[anchor_left][0], positions[anchor_right][1])
    half = (modulus - 1) // 2
    magnitude_variables = []
    for class_index, edges in enumerate(classes):
        if any(left == right for left, right in edges):
            # Equality-isomorphic windows make these pure zero-length classes.
            if any(left != right for left, right in edges):
                return GeometrySolve(
                    "unsat",
                    len(constraints),
                    len(labels),
                    monotonic() - started,
                )
            magnitude_variables.append(())
            continue
        magnitudes = tuple(
            z3.Bool(f"class_{class_index}_magnitude_{magnitude}")
            for magnitude in range(1, half + 1)
        )
        magnitude_variables.append(magnitudes)
        solver.add(z3.PbEq(tuple((variable, 1) for variable in magnitudes), 1))
        for left, right in edges:
            for magnitude, magnitude_variable in enumerate(
                magnitudes, start=1
            ):
                for position in range(modulus):
                    solver.add(
                        z3.Or(
                            z3.Not(magnitude_variable),
                            z3.Not(positions[left][position]),
                            positions[right][(position + magnitude) % modulus],
                            positions[right][(position - magnitude) % modulus],
                        )
                    )

    outcome = solver.check()
    elapsed = monotonic() - started
    if outcome == z3.unknown:
        return GeometrySolve(
            "unknown",
            len(constraints),
            len(labels),
            elapsed,
            reason=solver.reason_unknown(),
        )
    if outcome == z3.unsat:
        return GeometrySolve(
            "unsat",
            len(constraints),
            len(labels),
            elapsed,
        )
    model = solver.model()
    resolved = tuple(
        (
            label,
            next(
                position
                for position, variable in enumerate(positions[label])
                if z3.is_true(model.eval(variable, model_completion=True))
            ),
        )
        for label in labels
    )
    flat = [0] * modulus
    for label, coordinate in resolved:
        flat[label] = coordinate
    if not all(
        constraint_holds(constraint, flat, modulus=modulus)
        for constraint in constraints
    ):
        raise AssertionError("Boolean Z3 model does not satisfy constraints")
    return GeometrySolve(
        "sat",
        len(constraints),
        len(labels),
        elapsed,
        coordinates=resolved,
    )


def solve_hidden_geometry_bitvector(
    constraints: Sequence[ChordConstraint],
    *,
    modulus: int = MODULUS,
    timeout_ms: int = 60_000,
) -> GeometrySolve:
    """Solve lag-one hidden geometry as a finite bit-vector problem.

    This is exactly the same unsigned cyclic-distance model as
    :func:`solve_hidden_geometry`. Coordinates and shared class magnitudes are
    bit vectors, while explicit conditional subtraction implements reduction
    modulo ``modulus`` without native remainder arithmetic.
    """

    _require_z3()
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
    classes = chord_classes(constraints)
    coordinate_bits = (modulus - 1).bit_length()
    half = (modulus - 1) // 2
    magnitude_bits = half.bit_length()
    wide_bits = coordinate_bits + 1
    solver = z3.SolverFor("QF_BV")
    solver.set(timeout=timeout_ms)
    coordinates = {
        label: z3.BitVec(f"hidden_bv_coordinate_{label}", coordinate_bits)
        for label in labels
    }
    modulus_coordinate = z3.BitVecVal(modulus, coordinate_bits)
    for coordinate in coordinates.values():
        solver.add(z3.ULT(coordinate, modulus_coordinate))
    solver.add(z3.Distinct(*coordinates.values()))

    anchor_left, anchor_right = next(
        (left, right)
        for constraint in constraints
        for left, right in (
            (constraint.source_left, constraint.source_right),
            (constraint.target_left, constraint.target_right),
        )
        if left != right
    )
    solver.add(
        coordinates[anchor_left] == z3.BitVecVal(0, coordinate_bits)
    )
    solver.add(
        coordinates[anchor_right] == z3.BitVecVal(1, coordinate_bits)
    )

    modulus_wide = z3.BitVecVal(modulus, wide_bits)
    for class_index, edges in enumerate(classes):
        zero_edges = tuple(left == right for left, right in edges)
        if any(zero_edges):
            if not all(zero_edges):
                return GeometrySolve(
                    "unsat",
                    len(constraints),
                    len(labels),
                    monotonic() - started,
                )
            continue
        magnitude = z3.BitVec(
            f"hidden_bv_magnitude_{class_index}",
            magnitude_bits,
        )
        solver.add(
            z3.UGT(magnitude, z3.BitVecVal(0, magnitude_bits)),
            z3.ULE(magnitude, z3.BitVecVal(half, magnitude_bits)),
        )
        wide_magnitude = z3.ZeroExt(
            wide_bits - magnitude_bits,
            magnitude,
        )
        for left, right in edges:
            wide_left = z3.ZeroExt(1, coordinates[left])
            wide_right = z3.ZeroExt(1, coordinates[right])
            raw_plus = wide_left + wide_magnitude
            plus = z3.If(
                z3.UGE(raw_plus, modulus_wide),
                raw_plus - modulus_wide,
                raw_plus,
            )
            minus = z3.If(
                z3.UGE(wide_left, wide_magnitude),
                wide_left - wide_magnitude,
                wide_left + modulus_wide - wide_magnitude,
            )
            solver.add(z3.Or(wide_right == plus, wide_right == minus))

    outcome = solver.check()
    elapsed = monotonic() - started
    if outcome == z3.unknown:
        return GeometrySolve(
            "unknown",
            len(constraints),
            len(labels),
            elapsed,
            reason=solver.reason_unknown(),
        )
    if outcome == z3.unsat:
        return GeometrySolve(
            "unsat",
            len(constraints),
            len(labels),
            elapsed,
        )

    model = solver.model()
    resolved = tuple(
        sorted(
            (
                label,
                model.eval(
                    coordinate,
                    model_completion=True,
                ).as_long(),
            )
            for label, coordinate in coordinates.items()
        )
    )
    flat = [0] * modulus
    for label, coordinate in resolved:
        flat[label] = coordinate
    if not all(
        constraint_holds(constraint, flat, modulus=modulus)
        for constraint in constraints
    ):
        raise AssertionError(
            "bit-vector model does not satisfy chord constraints"
        )
    return GeometrySolve(
        "sat",
        len(constraints),
        len(labels),
        elapsed,
        coordinates=resolved,
    )


def minimize_unsat_core(
    constraints: Sequence[ChordConstraint],
    *,
    modulus: int = MODULUS,
    timeout_ms: int = 60_000,
) -> GeometrySolve:
    """Greedily shrink an UNSAT core to deletion-minimality.

    The returned core is an independently unsatisfiable subset. It is not
    guaranteed to have globally minimum cardinality.
    """

    initial = solve_hidden_geometry(
        constraints,
        modulus=modulus,
        timeout_ms=timeout_ms,
        extract_core=True,
    )
    if initial.outcome != "unsat":
        return initial
    current = list(initial.core)
    index = 0
    started = monotonic()
    while index < len(current):
        candidate = current[:index] + current[index + 1 :]
        result = solve_hidden_geometry(
            candidate,
            modulus=modulus,
            timeout_ms=timeout_ms,
        )
        if result.outcome == "unsat":
            current = candidate
        else:
            index += 1
    elapsed = initial.elapsed_seconds + monotonic() - started
    return GeometrySolve(
        "unsat",
        len(constraints),
        len({label for constraint in constraints for label in constraint.labels}),
        elapsed,
        core=tuple(current),
    )


def repair_hidden_geometry(
    constraints: Sequence[ChordConstraint],
    *,
    modulus: int = MODULUS,
    restarts: int = 20,
    steps_per_restart: int = 200_000,
    noise: float = 0.08,
    seed: int = 20260724,
) -> GeometrySearch:
    """Seek a full permutation witness by exact min-conflicts repairs.

    This is a one-sided method: a complete result proves satisfiability, while
    an incomplete result says nothing about impossibility.
    """

    if modulus < 3 or modulus % 2 == 0:
        raise ValueError("modulus must be an odd integer at least three")
    if not constraints:
        raise ValueError("at least one constraint is required")
    if restarts < 1 or steps_per_restart < 1:
        raise ValueError("search budgets must be positive")
    if not 0.0 <= noise <= 1.0:
        raise ValueError("noise must be in [0,1]")
    if any(label not in range(modulus) for item in constraints for label in item.labels):
        raise ValueError("constraint label lies outside the wheel")

    incident: list[set[int]] = [set() for _ in range(modulus)]
    for index, item in enumerate(constraints):
        for label in set(item.labels):
            incident[label].add(index)

    rng = random.Random(seed)
    best = GeometrySearch(0, len(constraints), 0, 0, tuple(range(modulus)))
    for restart in range(restarts):
        coordinates = list(range(modulus))
        rng.shuffle(coordinates)
        occupants = [0] * modulus
        for label, coordinate in enumerate(coordinates):
            occupants[coordinate] = label
        satisfied = [
            constraint_holds(item, coordinates, modulus=modulus)
            for item in constraints
        ]
        unsatisfied = {index for index, value in enumerate(satisfied) if not value}
        if len(constraints) - len(unsatisfied) > best.satisfied:
            best = GeometrySearch(
                len(constraints) - len(unsatisfied),
                len(constraints),
                0,
                restart,
                tuple(coordinates),
            )

        for step in range(1, steps_per_restart + 1):
            if not unsatisfied:
                return GeometrySearch(
                    len(constraints),
                    len(constraints),
                    step,
                    restart,
                    tuple(coordinates),
                )
            item = constraints[rng.choice(tuple(unsatisfied))]
            source_magnitude = unsigned_chord(
                coordinates,
                item.source_left,
                item.source_right,
                modulus=modulus,
            )
            target_magnitude = unsigned_chord(
                coordinates,
                item.target_left,
                item.target_right,
                modulus=modulus,
            )
            moves = []
            for moving, fixed, magnitude in (
                (item.source_left, item.source_right, target_magnitude),
                (item.source_right, item.source_left, target_magnitude),
                (item.target_left, item.target_right, source_magnitude),
                (item.target_right, item.target_left, source_magnitude),
            ):
                for orientation in (-1, 1):
                    desired = (
                        coordinates[fixed] + orientation * magnitude
                    ) % modulus
                    other = occupants[desired]
                    if other != moving:
                        moves.append((moving, other))
            if not moves:
                continue

            scored = []
            for moving, other in set(moves):
                affected = incident[moving] | incident[other]
                before = sum(satisfied[index] for index in affected)
                coordinates[moving], coordinates[other] = (
                    coordinates[other],
                    coordinates[moving],
                )
                after = sum(
                    constraint_holds(
                        constraints[index], coordinates, modulus=modulus
                    )
                    for index in affected
                )
                coordinates[moving], coordinates[other] = (
                    coordinates[other],
                    coordinates[moving],
                )
                scored.append((after - before, moving, other))

            if rng.random() < noise:
                _, moving, other = rng.choice(scored)
            else:
                maximum = max(score for score, _, _ in scored)
                _, moving, other = rng.choice(
                    [move for move in scored if move[0] == maximum]
                )
            affected = incident[moving] | incident[other]
            old_moving = coordinates[moving]
            old_other = coordinates[other]
            coordinates[moving], coordinates[other] = old_other, old_moving
            occupants[old_moving], occupants[old_other] = other, moving
            for index in affected:
                value = constraint_holds(
                    constraints[index], coordinates, modulus=modulus
                )
                satisfied[index] = value
                if value:
                    unsatisfied.discard(index)
                else:
                    unsatisfied.add(index)

            current = len(constraints) - len(unsatisfied)
            if current > best.satisfied:
                best = GeometrySearch(
                    current,
                    len(constraints),
                    step,
                    restart,
                    tuple(coordinates),
                )
    return best


def repair_hidden_geometry_classes(
    constraints: Sequence[ChordConstraint],
    *,
    modulus: int = MODULUS,
    restarts: int = 20,
    steps_per_restart: int = 200_000,
    noise: float = 0.08,
    seed: int = 20260724,
) -> GeometrySearch:
    """Min-conflicts search using transitive chord classes as the objective."""

    if modulus < 3 or modulus % 2 == 0:
        raise ValueError("modulus must be an odd integer at least three")
    if not constraints:
        raise ValueError("at least one constraint is required")
    classes = chord_classes(constraints)
    class_pair_total = sum(
        len(edges) * (len(edges) - 1) // 2 for edges in classes
    )
    incident_classes: list[set[int]] = [set() for _ in range(modulus)]
    for class_index, edges in enumerate(classes):
        for edge in edges:
            for label in set(edge):
                incident_classes[label].add(class_index)

    def class_counts(
        class_index: int, coordinates: Sequence[int]
    ) -> Counter[int]:
        return Counter(
            unsigned_chord(coordinates, left, right, modulus=modulus)
            for left, right in classes[class_index]
        )

    def agreement(counts: Counter[int]) -> int:
        return sum(count * (count - 1) // 2 for count in counts.values())

    rng = random.Random(seed)
    best = GeometrySearch(
        0,
        len(constraints),
        0,
        0,
        tuple(range(modulus)),
        0,
        class_pair_total,
    )
    for restart in range(restarts):
        coordinates = list(range(modulus))
        rng.shuffle(coordinates)
        occupants = [0] * modulus
        for label, coordinate in enumerate(coordinates):
            occupants[coordinate] = label
        counts = [
            class_counts(class_index, coordinates)
            for class_index in range(len(classes))
        ]
        class_score = sum(map(agreement, counts))

        for step in range(steps_per_restart + 1):
            if class_score >= best.class_edge_agreement:
                satisfied = sum(
                    constraint_holds(item, coordinates, modulus=modulus)
                    for item in constraints
                )
                if (
                    class_score > best.class_edge_agreement
                    or class_score == best.class_edge_agreement
                    and satisfied > best.satisfied
                ):
                    best = GeometrySearch(
                        satisfied,
                        len(constraints),
                        step,
                        restart,
                        tuple(coordinates),
                        class_score,
                        class_pair_total,
                    )
            if class_score == class_pair_total:
                if satisfied != len(constraints):
                    raise AssertionError("uniform chord classes must satisfy all links")
                return best
            if step == steps_per_restart:
                break

            bad_classes = [
                index
                for index, class_count in enumerate(counts)
                if agreement(class_count)
                != len(classes[index]) * (len(classes[index]) - 1) // 2
            ]
            class_index = rng.choice(bad_classes)
            edges = classes[class_index]
            edge_magnitudes = [
                unsigned_chord(coordinates, left, right, modulus=modulus)
                for left, right in edges
            ]
            modal_count = max(counts[class_index].values())
            modal_magnitudes = tuple(
                magnitude
                for magnitude, count in counts[class_index].items()
                if count == modal_count
            )
            target_magnitudes = (
                (rng.choice(tuple(set(edge_magnitudes))),)
                if rng.random() < 0.2
                else (rng.choice(modal_magnitudes),)
            )
            candidate_edges = [
                edge
                for edge, magnitude in zip(edges, edge_magnitudes, strict=True)
                if magnitude not in target_magnitudes
            ]
            if not candidate_edges:
                candidate_edges = list(edges)
            candidate_edges = (rng.choice(candidate_edges),)

            moves = set()
            for moving_edge in candidate_edges:
                for moving, fixed in (
                    moving_edge,
                    tuple(reversed(moving_edge)),
                ):
                    for magnitude in target_magnitudes:
                        for orientation in (-1, 1):
                            desired = (
                                coordinates[fixed] + orientation * magnitude
                            ) % modulus
                            other = occupants[desired]
                            if other != moving:
                                moves.add((moving, other))
            if not moves:
                continue

            scored = []
            for moving, other in moves:
                affected = incident_classes[moving] | incident_classes[other]
                before = sum(agreement(counts[index]) for index in affected)
                coordinates[moving], coordinates[other] = (
                    coordinates[other],
                    coordinates[moving],
                )
                replacements = {
                    index: class_counts(index, coordinates) for index in affected
                }
                after = sum(agreement(value) for value in replacements.values())
                coordinates[moving], coordinates[other] = (
                    coordinates[other],
                    coordinates[moving],
                )
                scored.append((after - before, moving, other, replacements))

            if rng.random() < noise:
                _, moving, other, replacements = rng.choice(scored)
            else:
                maximum = max(score for score, *_ in scored)
                _, moving, other, replacements = rng.choice(
                    [move for move in scored if move[0] == maximum]
                )
            affected = incident_classes[moving] | incident_classes[other]
            before = sum(agreement(counts[index]) for index in affected)
            old_moving = coordinates[moving]
            old_other = coordinates[other]
            coordinates[moving], coordinates[other] = old_other, old_moving
            occupants[old_moving], occupants[old_other] = other, moving
            for index in affected:
                counts[index] = replacements[index]
            after = sum(agreement(counts[index]) for index in affected)
            class_score += after - before
    return best
