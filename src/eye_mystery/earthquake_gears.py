"""Executable audit of Lymm's Earthquake-gear Wadsworth construction.

The proposed machine has one plaintext disk, one 83-position ciphertext disk,
and the three binary bands from the Earthquake symbol between them.  Every
unit move of the plaintext disk advances all bands by one tooth.  An open eye
on a band contributes that band's fixed weight to the ciphertext rotation.

This module deliberately separates two questions:

* whether the visible base-five ranks themselves form the ciphertext disk;
* whether *some* hidden permutation of the 83 visible labels forms the disk.

The second question is encoded as solver-agnostic SMT-LIB and uses the
command-line ``z3`` executable, so the optional Python Z3 package is not
required.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
import re
import shutil
import subprocess
from time import monotonic


MODULUS = 83
ALTERNATING_BAND = tuple(int(bit) for bit in "10101010101010101010")
IRREGULAR_BAND = tuple(int(bit) for bit in "11110111011101110")
SCHEDULE_PERIOD = 34

ContextSequences = tuple[str, tuple[int, ...], tuple[int, ...]]


def _validate_direction(direction: int) -> None:
    if direction not in (-1, 1):
        raise ValueError("direction must be -1 or +1")


def active_counts(
    phase: int,
    distance: int,
    *,
    direction: int = 1,
) -> tuple[int, int, int]:
    """Return open-eye counts for one positive plaintext-disk movement.

    The outer 24-tooth band is entirely open, so its count is exactly the
    movement distance.  The 20-tooth band's visible content has period two;
    together with the 17-tooth irregular band this gives output period 34.
    A before/after-step timing choice is absorbed by the free phase.
    """

    _validate_direction(direction)
    if not 0 <= phase < SCHEDULE_PERIOD:
        raise ValueError("phase must be in 0..33")
    if distance < 1:
        raise ValueError("distance must be positive")
    alternating = 0
    irregular = 0
    for offset in range(distance):
        tooth = phase + direction * offset
        alternating += ALTERNATING_BAND[tooth % len(ALTERNATING_BAND)]
        irregular += IRREGULAR_BAND[tooth % len(IRREGULAR_BAND)]
    return distance, alternating, irregular


def weighted_increment(
    phase: int,
    distance: int,
    weights: Sequence[int] = (1, 1, 1),
    *,
    direction: int = 1,
    modulus: int = MODULUS,
) -> int:
    """Return the ciphertext-disk rotation for one plaintext transition."""

    if len(weights) != 3:
        raise ValueError("the machine requires three band weights")
    counts = active_counts(phase, distance, direction=direction)
    return sum(
        weight * count for weight, count in zip(weights, counts, strict=True)
    ) % modulus


def simulate_positions(
    distances: Sequence[int],
    *,
    phase: int,
    start: int = 0,
    weights: Sequence[int] = (1, 1, 1),
    direction: int = 1,
    modulus: int = MODULUS,
) -> tuple[int, ...]:
    """Emit ciphertext-disk positions for one known distance schedule."""

    if not 0 <= start < modulus:
        raise ValueError("start must be a ciphertext position")
    if not 0 <= phase < SCHEDULE_PERIOD:
        raise ValueError("phase must be in 0..33")
    positions = [start]
    current = start
    current_phase = phase
    for distance in distances:
        current = (
            current
            + weighted_increment(
                current_phase,
                distance,
                weights,
                direction=direction,
                modulus=modulus,
            )
        ) % modulus
        positions.append(current)
        current_phase = (current_phase + direction * distance) % SCHEDULE_PERIOD
    return tuple(positions)


@dataclass(frozen=True)
class DirectGearTrace:
    """One exact natural-rank fit for an aligned repeated passage."""

    direction: int
    scale: int
    source_phase: int
    target_phase: int
    distances: tuple[int, ...]


@dataclass(frozen=True)
class DirectContextFit:
    """Best direct-coordinate prefix and any full witness for one context."""

    matched_transitions: int
    transitions: int
    trace: DirectGearTrace | None

    @property
    def complete(self) -> bool:
        return self.matched_transitions == self.transitions


@dataclass(frozen=True)
class DirectRankAudit:
    """Best one-configuration fit over a family of scales and directions."""

    plaintext_alphabet_size: int
    weights: tuple[int, int, int]
    contexts: int
    transitions: int
    best_full_contexts: int
    best_matched_transitions: int
    best_direction: int
    best_scale: int
    per_context_prefixes: tuple[tuple[str, int, int], ...]
    complete_configurations: tuple[tuple[int, int], ...]

    @property
    def complete(self) -> bool:
        return bool(self.complete_configurations)


@dataclass(frozen=True)
class DirectParameterScreen:
    """Independent-phase necessary screen for every normalized band weight."""

    plaintext_alphabet_size: int
    constraints_tested: int
    total_constraints: int
    survivors: tuple[tuple[int, int, int], ...]
    survivor_history: tuple[int, ...]
    stopping_constraint: tuple[str, int] | None

    @property
    def compatible(self) -> bool:
        return bool(self.survivors)


def _solve_weight_equations(
    first: tuple[int, int, int],
    first_target: int,
    second: tuple[int, int, int],
    second_target: int,
    *,
    modulus: int = MODULUS,
) -> tuple[tuple[int, int], ...]:
    """Solve two affine equations for the alternating/irregular weights."""

    _, first_alternating, first_irregular = first
    _, second_alternating, second_irregular = second
    determinant = (
        first_alternating * second_irregular
        - first_irregular * second_alternating
    ) % modulus
    if determinant:
        inverse = pow(determinant, -1, modulus)
        alternating = (
            first_target * second_irregular
            - first_irregular * second_target
        ) * inverse % modulus
        irregular = (
            first_alternating * second_target
            - first_target * second_alternating
        ) * inverse % modulus
        return ((alternating, irregular),)

    solutions = []
    for alternating in range(modulus):
        if first_irregular:
            irregular = (
                first_target - first_alternating * alternating
            ) * pow(first_irregular, -1, modulus) % modulus
            candidates = (irregular,)
        elif second_irregular:
            irregular = (
                second_target - second_alternating * alternating
            ) * pow(second_irregular, -1, modulus) % modulus
            candidates = (irregular,)
        else:
            candidates = range(modulus)
        for irregular in candidates:
            if (
                first_alternating * alternating
                + first_irregular * irregular
                - first_target
            ) % modulus:
                continue
            if (
                second_alternating * alternating
                + second_irregular * irregular
                - second_target
            ) % modulus:
                continue
            solutions.append((alternating, irregular))
    return tuple(solutions)


def direct_parameter_candidates(
    contexts: Sequence[ContextSequences],
    *,
    plaintext_alphabet_size: int,
    scales: Iterable[int] = range(1, MODULUS),
    modulus: int = MODULUS,
) -> DirectParameterScreen:
    """Intersect every direct-rank weight triple under independent phases.

    The outer-band weight is normalized to one and ``scale`` maps visible
    ranks into that normalized disk.  Every transition may choose a fresh
    distance and two fresh phases, discarding the real machine's continuity.
    Therefore an empty intersection is a strict rejection of all fixed band
    weights in the arithmetic-progression ciphertext-disk family.
    """

    if not contexts:
        raise ValueError("at least one context is required")
    if plaintext_alphabet_size < 2:
        raise ValueError("plaintext alphabet must contain at least two symbols")
    selected_scales = tuple(dict.fromkeys(scales))
    if not selected_scales or any(
        not 1 <= scale < modulus for scale in selected_scales
    ):
        raise ValueError("scales must be nonzero residues")

    features_by_distance = {
        distance: tuple(
            sorted(
                {
                    active_counts(phase, distance)
                    for phase in range(SCHEDULE_PERIOD)
                }
            )
        )
        for distance in range(1, plaintext_alphabet_size + 1)
    }
    constraints = tuple(
        (
            name,
            transition,
            (source_right - source_left) % modulus,
            (target_right - target_left) % modulus,
        )
        for name, source, target in contexts
        for transition, ((source_left, source_right), (target_left, target_right)) in enumerate(
            zip(
                zip(source, source[1:]),
                zip(target, target[1:]),
                strict=True,
            )
        )
    )
    survivors: set[tuple[int, int, int]] | None = None
    history = []
    stopping = None
    for name, transition, source_delta, target_delta in constraints:
        compatible: set[tuple[int, int, int]] = set()
        for scale in selected_scales:
            scaled_source = scale * source_delta % modulus
            scaled_target = scale * target_delta % modulus
            for distance, features in features_by_distance.items():
                first_target = (scaled_source - distance) % modulus
                second_target = (scaled_target - distance) % modulus
                for source_features in features:
                    for target_features in features:
                        for alternating, irregular in _solve_weight_equations(
                            source_features,
                            first_target,
                            target_features,
                            second_target,
                            modulus=modulus,
                        ):
                            compatible.add((scale, alternating, irregular))
        survivors = compatible if survivors is None else survivors & compatible
        history.append(len(survivors))
        if not survivors:
            stopping = (name, transition)
            break
    return DirectParameterScreen(
        plaintext_alphabet_size,
        len(history),
        len(constraints),
        tuple(sorted(survivors or ())),
        tuple(history),
        stopping,
    )


def fit_direct_context(
    source: Sequence[int],
    target: Sequence[int],
    *,
    plaintext_alphabet_size: int,
    weights: Sequence[int] = (1, 1, 1),
    direction: int = 1,
    scale: int = 1,
    modulus: int = MODULUS,
) -> DirectContextFit:
    """Fit one repeated passage in visible ranks up to one global scale.

    ``scale`` permits the small family of arithmetic-progression disk orders.
    Translation cancels in consecutive differences.  The two occurrences get
    independent initial gear phases, and every transition gets any positive
    plaintext-ring distance in ``1..plaintext_alphabet_size``.  This is more
    permissive than a complete message-level reconstruction.
    """

    _validate_direction(direction)
    if len(source) != len(target):
        raise ValueError("aligned contexts must have equal lengths")
    if len(source) < 2:
        raise ValueError("a context must contain at least one transition")
    if plaintext_alphabet_size < 2:
        raise ValueError("plaintext alphabet must contain at least two symbols")
    if not 1 <= scale < modulus:
        raise ValueError("scale must be a nonzero residue")
    if any(not 0 <= value < modulus for value in (*source, *target)):
        raise ValueError("ciphertext label lies outside the modulus")

    normalized_weights = tuple(int(weight) % modulus for weight in weights)
    if len(normalized_weights) != 3:
        raise ValueError("the machine requires three band weights")
    increments = {
        (phase, distance): weighted_increment(
            phase,
            distance,
            normalized_weights,
            direction=direction,
            modulus=modulus,
        )
        for phase in range(SCHEDULE_PERIOD)
        for distance in range(1, plaintext_alphabet_size + 1)
    }
    source_deltas = tuple(
        scale * (right - left) % modulus
        for left, right in zip(source, source[1:])
    )
    target_deltas = tuple(
        scale * (right - left) % modulus
        for left, right in zip(target, target[1:])
    )

    # One witness per reachable phase pair is enough.  The phase difference
    # remains coupled because both occurrences consume the same distances.
    states: dict[tuple[int, int], tuple[int, int, tuple[int, ...]]] = {
        (source_phase, target_phase): (
            source_phase,
            target_phase,
            (),
        )
        for source_phase in range(SCHEDULE_PERIOD)
        for target_phase in range(SCHEDULE_PERIOD)
    }
    matched = 0
    for source_delta, target_delta in zip(
        source_deltas,
        target_deltas,
        strict=True,
    ):
        next_states: dict[
            tuple[int, int], tuple[int, int, tuple[int, ...]]
        ] = {}
        for (source_phase, target_phase), (
            initial_source,
            initial_target,
            distances,
        ) in states.items():
            for distance in range(1, plaintext_alphabet_size + 1):
                if (
                    increments[source_phase, distance] != source_delta
                    or increments[target_phase, distance] != target_delta
                ):
                    continue
                next_source = (
                    source_phase + direction * distance
                ) % SCHEDULE_PERIOD
                next_target = (
                    target_phase + direction * distance
                ) % SCHEDULE_PERIOD
                next_states.setdefault(
                    (next_source, next_target),
                    (
                        initial_source,
                        initial_target,
                        distances + (distance,),
                    ),
                )
        if not next_states:
            return DirectContextFit(matched, len(source_deltas), None)
        states = next_states
        matched += 1

    initial_source, initial_target, distances = next(iter(states.values()))
    return DirectContextFit(
        matched,
        len(source_deltas),
        DirectGearTrace(
            direction,
            scale,
            initial_source,
            initial_target,
            distances,
        ),
    )


def audit_direct_rank(
    contexts: Sequence[ContextSequences],
    *,
    plaintext_alphabet_size: int,
    weights: Sequence[int] = (1, 1, 1),
    directions: Iterable[int] = (-1, 1),
    scales: Iterable[int] = range(1, MODULUS),
) -> DirectRankAudit:
    """Audit one globally shared direct disk configuration."""

    if not contexts:
        raise ValueError("at least one context is required")
    selected_directions = tuple(dict.fromkeys(directions))
    selected_scales = tuple(dict.fromkeys(scales))
    if not selected_directions or not selected_scales:
        raise ValueError("directions and scales must be nonempty")
    normalized_weights = tuple(int(weight) % MODULUS for weight in weights)
    if len(normalized_weights) != 3:
        raise ValueError("the machine requires three band weights")

    totals = sum(len(source) - 1 for _, source, _ in contexts)
    best_score = (-1, -1)
    best_configuration = (selected_directions[0], selected_scales[0])
    best_prefixes: dict[str, int] = {name: 0 for name, _, _ in contexts}
    complete_configurations = []
    for direction in selected_directions:
        _validate_direction(direction)
        for scale in selected_scales:
            fits = tuple(
                fit_direct_context(
                    source,
                    target,
                    plaintext_alphabet_size=plaintext_alphabet_size,
                    weights=normalized_weights,
                    direction=direction,
                    scale=scale,
                )
                for _, source, target in contexts
            )
            full = sum(fit.complete for fit in fits)
            matched = sum(fit.matched_transitions for fit in fits)
            score = (full, matched)
            if score > best_score:
                best_score = score
                best_configuration = (direction, scale)
            for (name, _, _), fit in zip(contexts, fits, strict=True):
                best_prefixes[name] = max(
                    best_prefixes[name],
                    fit.matched_transitions,
                )
            if full == len(contexts):
                complete_configurations.append((direction, scale))
    return DirectRankAudit(
        plaintext_alphabet_size,
        normalized_weights,  # type: ignore[arg-type]
        len(contexts),
        totals,
        best_score[0],
        best_score[1],
        best_configuration[0],
        best_configuration[1],
        tuple(
            (name, best_prefixes[name], len(source) - 1)
            for name, source, _ in contexts
        ),
        tuple(complete_configurations),
    )


@dataclass(frozen=True)
class HiddenGearContextWitness:
    """Recovered phases and plaintext distances for one aligned context."""

    name: str
    source_phase: int
    target_phase: int
    distances: tuple[int, ...]


@dataclass(frozen=True)
class HiddenGearWitness:
    """One exact hidden ciphertext-disk embedding."""

    coordinates: tuple[tuple[int, int], ...]
    weights: tuple[int, int, int]
    contexts: tuple[HiddenGearContextWitness, ...]


@dataclass(frozen=True)
class HiddenGearResult:
    """SMT feasibility result for the permissive hidden-disk model."""

    status: str
    witness: HiddenGearWitness | None
    elapsed_seconds: float
    formula_bytes: int
    solver_output: str


@dataclass(frozen=True)
class RelaxedPairResult:
    """Result of the phase-independent same-distance necessary condition."""

    status: str
    coordinates: tuple[tuple[int, int], ...] | None
    elapsed_seconds: float
    formula_bytes: int
    allowed_pairs: int
    solver_output: str


def _safe_name(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9_]", "_", name)


def _linear_weight_expression(
    count: str,
    weight: str,
    *,
    maximum: int,
) -> str:
    """Multiply two bounded variables using only linear-arithmetic ITEs."""

    expression = f"(* {maximum} {weight})"
    for value in range(maximum - 1, -1, -1):
        term = "0" if value == 0 else (
            weight if value == 1 else f"(* {value} {weight})"
        )
        expression = f"(ite (= {count} {value}) {term} {expression})"
    return expression


def _append_symbolic_increment(
    lines: list[str],
    *,
    prefix: str,
    phase: str,
    distance: str,
    direction: int,
    plaintext_alphabet_size: int,
    fixed_weights: tuple[int, int, int] | None,
) -> str:
    """Append an exact linear encoding of one weighted band increment."""

    alternating = f"{prefix}_alternating_count"
    irregular = f"{prefix}_irregular_count"
    increment = f"{prefix}_increment"
    lines.extend(
        (
            f"(declare-const {alternating} Int)",
            f"(declare-const {irregular} Int)",
            f"(declare-const {increment} Int)",
            f"(assert (and (<= 0 {alternating}) "
            f"(<= {alternating} {plaintext_alphabet_size})))",
            f"(assert (and (<= 0 {irregular}) "
            f"(<= {irregular} {plaintext_alphabet_size})))",
            f"(assert (and (<= 0 {increment}) (< {increment} 83)))",
        )
    )
    # The alternating tape is open at even phases.  Reversal does not alter
    # the count because parity flips on every unit step in either direction.
    lines.append(
        f"(assert (= {alternating} "
        f"(div (+ {distance} (ite (= (mod {phase} 2) 0) 1 0)) 2)))"
    )

    # The irregular 17-tape is closed only at positions 4, 8, 12, and 16.
    # Count the first visit to each closed tooth and any full 17-step returns.
    zero_terms = []
    for zero in (4, 8, 12, 16):
        first = (
            f"(mod (- {zero} {phase}) 17)"
            if direction == 1
            else f"(mod (- {phase} {zero}) 17)"
        )
        zero_terms.append(
            f"(ite (< {first} {distance}) "
            f"(+ 1 (div (- (- {distance} 1) {first}) 17)) 0)"
        )
    lines.append(
        f"(assert (= {irregular} "
        f"(- {distance} (+ {' '.join(zero_terms)}))))"
    )
    if fixed_weights is None:
        alternating_weight = _linear_weight_expression(
            alternating,
            "weight_alternating",
            maximum=plaintext_alphabet_size,
        )
        irregular_weight = _linear_weight_expression(
            irregular,
            "weight_irregular",
            maximum=plaintext_alphabet_size,
        )
    else:
        alternating_weight = f"(* {fixed_weights[1]} {alternating})"
        irregular_weight = f"(* {fixed_weights[2]} {irregular})"
    lines.append(
        f"(assert (= {increment} "
        f"(mod (+ {distance} {alternating_weight} {irregular_weight}) 83)))"
    )
    return increment


def _exactly_one(names: Sequence[str]) -> str:
    return (
        "(assert (= (+ "
        + " ".join(f"(ite {name} 1 0)" for name in names)
        + ") 1))"
    )


def _modular_delta_equation(left: int, right: int, increment: int) -> str:
    difference = f"(- coord_{right} coord_{left})"
    if increment == 0:
        return f"(= {difference} 0)"
    return (
        f"(or (= {difference} {increment}) "
        f"(= {difference} {increment - MODULUS}))"
    )


def allowed_increment_pairs(
    *,
    plaintext_alphabet_size: int,
    weights: Sequence[int] = (1, 1, 1),
    direction: int = 1,
) -> frozenset[tuple[int, int]]:
    """Return increment pairs possible at one common plaintext distance.

    The two repeated-passage occurrences may have arbitrary, independent
    phases at this relaxed screen.  Exact phase continuity is intentionally
    discarded, so failure is a valid rejection while success is not a fit.
    """

    _validate_direction(direction)
    if plaintext_alphabet_size < 2:
        raise ValueError("plaintext alphabet must contain at least two symbols")
    possible: set[tuple[int, int]] = set()
    for distance in range(1, plaintext_alphabet_size + 1):
        increments = {
            weighted_increment(
                phase,
                distance,
                weights,
                direction=direction,
            )
            for phase in range(SCHEDULE_PERIOD)
        }
        possible.update(
            (source, target)
            for source in increments
            for target in increments
        )
    return frozenset(possible)


def build_relaxed_pair_smt2(
    contexts: Sequence[ContextSequences],
    *,
    plaintext_alphabet_size: int,
    weights: Sequence[int] = (1, 1, 1),
    direction: int = 1,
    timeout_ms: int = 120_000,
    request_model: bool = True,
) -> str:
    """Build the hidden-disk same-distance relaxation in linear arithmetic."""

    _validate_direction(direction)
    if not contexts:
        raise ValueError("at least one context is required")
    if timeout_ms < 1:
        raise ValueError("timeout must be positive")
    for _, source, target in contexts:
        if len(source) != len(target) or len(source) < 2:
            raise ValueError("every context needs equal nontrivial sequences")
        if any(not 0 <= value < MODULUS for value in (*source, *target)):
            raise ValueError("ciphertext label lies outside 0..82")
    increments_by_distance = tuple(
        tuple(
            sorted(
                {
                    weighted_increment(
                        phase,
                        distance,
                        weights,
                        direction=direction,
                    )
                    for phase in range(SCHEDULE_PERIOD)
                }
            )
        )
        for distance in range(1, plaintext_alphabet_size + 1)
    )
    observed = tuple(
        sorted(
            {
                value
                for _, source, target in contexts
                for value in (*source, *target)
            }
        )
    )
    lines = [
        "(set-logic QF_LIA)",
        "(set-option :produce-models true)",
        f"(set-option :timeout {timeout_ms})",
    ]
    coordinate_names = tuple(f"coord_{label}" for label in observed)
    for coordinate in coordinate_names:
        lines.append(f"(declare-const {coordinate} Int)")
        lines.append(
            f"(assert (and (<= 0 {coordinate}) (< {coordinate} 83)))"
        )
    lines.append(f"(assert (distinct {' '.join(coordinate_names)}))")
    lines.append(f"(assert (= {coordinate_names[0]} 0))")

    for context_index, (name, source, target) in enumerate(contexts):
        prefix = f"r{context_index}_{_safe_name(name)}"
        for transition, ((source_left, source_right), (target_left, target_right)) in enumerate(
            zip(
                zip(source, source[1:]),
                zip(target, target[1:]),
                strict=True,
            )
        ):
            source_delta = f"{prefix}_source_delta_{transition}"
            target_delta = f"{prefix}_target_delta_{transition}"
            lines.append(f"(declare-const {source_delta} Int)")
            lines.append(f"(declare-const {target_delta} Int)")
            for delta, left, right in (
                (source_delta, source_left, source_right),
                (target_delta, target_left, target_right),
            ):
                difference = f"(- coord_{right} coord_{left})"
                lines.append(
                    f"(assert (and (<= 0 {delta}) (< {delta} 83)))"
                )
                lines.append(
                    f"(assert (or (= {difference} {delta}) "
                    f"(= {difference} (- {delta} 83))))"
                )
            lines.append(
                "(assert (or "
                + " ".join(
                    "(and "
                    + (
                        f"(= {source_delta} {increments[0]})"
                        if len(increments) == 1
                        else "(or "
                        + " ".join(
                            f"(= {source_delta} {value})"
                            for value in increments
                        )
                        + ")"
                    )
                    + " "
                    + (
                        f"(= {target_delta} {increments[0]})"
                        if len(increments) == 1
                        else "(or "
                        + " ".join(
                            f"(= {target_delta} {value})"
                            for value in increments
                        )
                        + ")"
                    )
                    + ")"
                    for increments in increments_by_distance
                )
                + "))"
            )
    lines.append("(check-sat)")
    if request_model:
        lines.append(f"(get-value ({' '.join(coordinate_names)}))")
    lines.append("(exit)")
    return "\n".join(lines) + "\n"


def build_relaxed_pair_bv_smt2(
    contexts: Sequence[ContextSequences],
    *,
    plaintext_alphabet_size: int,
    weights: Sequence[int] = (1, 1, 1),
    direction: int = 1,
    timeout_ms: int = 120_000,
    request_model: bool = True,
) -> str:
    """Build the same relaxation as a finite seven-bit SAT problem."""

    _validate_direction(direction)
    if not contexts:
        raise ValueError("at least one context is required")
    if timeout_ms < 1:
        raise ValueError("timeout must be positive")
    increments_by_distance = tuple(
        tuple(
            sorted(
                {
                    weighted_increment(
                        phase,
                        distance,
                        weights,
                        direction=direction,
                    )
                    for phase in range(SCHEDULE_PERIOD)
                }
            )
        )
        for distance in range(1, plaintext_alphabet_size + 1)
    )
    observed = tuple(
        sorted(
            {
                value
                for _, source, target in contexts
                for value in (*source, *target)
            }
        )
    )
    lines = [
        "(set-logic QF_BV)",
        "(set-option :produce-models true)",
        f"(set-option :timeout {timeout_ms})",
    ]
    coordinate_names = tuple(f"coord_{label}" for label in observed)
    for coordinate in coordinate_names:
        lines.append(f"(declare-const {coordinate} (_ BitVec 7))")
        lines.append(f"(assert (bvult {coordinate} (_ bv83 7)))")
    lines.append(f"(assert (distinct {' '.join(coordinate_names)}))")
    lines.append(f"(assert (= {coordinate_names[0]} (_ bv0 7)))")

    delta_names = []
    for context_index, (name, source, target) in enumerate(contexts):
        prefix = f"b{context_index}_{_safe_name(name)}"
        for transition, ((source_left, source_right), (target_left, target_right)) in enumerate(
            zip(
                zip(source, source[1:]),
                zip(target, target[1:]),
                strict=True,
            )
        ):
            pair_names = []
            for side_name, left, right in (
                ("source", source_left, source_right),
                ("target", target_left, target_right),
            ):
                delta = f"{prefix}_{side_name}_delta_{transition}"
                delta_names.append(delta)
                pair_names.append(delta)
                raw = (
                    f"(bvsub (bvadd ((_ zero_extend 1) coord_{right}) "
                    f"(_ bv83 8)) ((_ zero_extend 1) coord_{left}))"
                )
                reduced = (
                    f"(ite (bvuge {raw} (_ bv83 8)) "
                    f"(bvsub {raw} (_ bv83 8)) {raw})"
                )
                lines.append(
                    f"(define-fun {delta} () (_ BitVec 7) "
                    f"((_ extract 6 0) {reduced}))"
                )
            source_delta, target_delta = pair_names
            lines.append(
                "(assert (or "
                + " ".join(
                    "(and "
                    + (
                        f"(= {source_delta} (_ bv{increments[0]} 7))"
                        if len(increments) == 1
                        else "(or "
                        + " ".join(
                            f"(= {source_delta} (_ bv{value} 7))"
                            for value in increments
                        )
                        + ")"
                    )
                    + " "
                    + (
                        f"(= {target_delta} (_ bv{increments[0]} 7))"
                        if len(increments) == 1
                        else "(or "
                        + " ".join(
                            f"(= {target_delta} (_ bv{value} 7))"
                            for value in increments
                        )
                        + ")"
                    )
                    + ")"
                    for increments in increments_by_distance
                )
                + "))"
            )
    lines.append("(check-sat)")
    if request_model:
        lines.append(f"(get-value ({' '.join(coordinate_names)}))")
    lines.append("(exit)")
    return "\n".join(lines) + "\n"


def solve_relaxed_pairs_with_z3(
    contexts: Sequence[ContextSequences],
    *,
    plaintext_alphabet_size: int,
    weights: Sequence[int] = (1, 1, 1),
    direction: int = 1,
    timeout_ms: int = 120_000,
    z3_path: str | None = None,
    encoding: str = "bv",
) -> RelaxedPairResult:
    """Solve and verify the phase-independent same-distance screen."""

    executable = z3_path or shutil.which("z3")
    if executable is None:
        raise RuntimeError("z3 executable is unavailable")
    allowed = allowed_increment_pairs(
        plaintext_alphabet_size=plaintext_alphabet_size,
        weights=weights,
        direction=direction,
    )
    if encoding == "bv":
        formula = build_relaxed_pair_bv_smt2(
            contexts,
            plaintext_alphabet_size=plaintext_alphabet_size,
            weights=weights,
            direction=direction,
            timeout_ms=timeout_ms,
        )
    elif encoding == "lia":
        formula = build_relaxed_pair_smt2(
            contexts,
            plaintext_alphabet_size=plaintext_alphabet_size,
            weights=weights,
            direction=direction,
            timeout_ms=timeout_ms,
        )
    else:
        raise ValueError("encoding must be 'bv' or 'lia'")
    started = monotonic()
    try:
        completed = subprocess.run(
            (executable, "-in"),
            input=formula,
            text=True,
            capture_output=True,
            timeout=timeout_ms / 1_000 + 3,
            check=False,
        )
        output = completed.stdout + completed.stderr
    except subprocess.TimeoutExpired as error:
        output = (error.stdout or "") + (error.stderr or "")
        return RelaxedPairResult(
            "unknown",
            None,
            monotonic() - started,
            len(formula.encode()),
            len(allowed),
            output,
        )
    first_line = output.lstrip().splitlines()[0] if output.strip() else ""
    status = first_line if first_line in {"sat", "unsat", "unknown"} else "error"
    coordinates = None
    if status == "sat":
        if encoding == "bv":
            assignments = {
                int(label): int(bits, 2)
                for label, bits in re.findall(
                    r"\(coord_(\d+)\s+#b([01]+)\)",
                    output,
                )
            }
        else:
            assignments = {
                int(label): int(value)
                for label, value in re.findall(
                    r"\(coord_(\d+)\s+(-?\d+)\)",
                    output,
                )
            }
        observed = {
            value
            for _, source, target in contexts
            for value in (*source, *target)
        }
        if set(assignments) != observed:
            raise AssertionError("SAT model omitted hidden coordinates")
        if len(set(assignments.values())) != len(assignments):
            raise AssertionError("SAT model violated coordinate injectivity")
        for _, source, target in contexts:
            for (source_left, source_right), (target_left, target_right) in zip(
                zip(source, source[1:]),
                zip(target, target[1:]),
                strict=True,
            ):
                pair = (
                    (assignments[source_right] - assignments[source_left])
                    % MODULUS,
                    (assignments[target_right] - assignments[target_left])
                    % MODULUS,
                )
                if pair not in allowed:
                    raise AssertionError("relaxed-pair witness failed replay")
        coordinates = tuple(sorted(assignments.items()))
    return RelaxedPairResult(
        status,
        coordinates,
        monotonic() - started,
        len(formula.encode()),
        len(allowed),
        output,
    )


def _build_fixed_hidden_gear_smt2(
    contexts: Sequence[ContextSequences],
    *,
    plaintext_alphabet_size: int,
    direction: int,
    weights: tuple[int, int, int],
    timeout_ms: int,
    request_model: bool,
) -> str:
    """Build a finite one-hot encoding for fixed band weights."""

    observed = tuple(
        sorted(
            {
                value
                for _, source, target in contexts
                for value in (*source, *target)
            }
        )
    )
    lines = [
        "(set-logic QF_LIA)",
        "(set-option :produce-models true)",
        f"(set-option :timeout {timeout_ms})",
    ]
    coordinate_names = tuple(f"coord_{label}" for label in observed)
    for coordinate in coordinate_names:
        lines.append(f"(declare-const {coordinate} Int)")
        lines.append(
            f"(assert (and (<= 0 {coordinate}) (< {coordinate} 83)))"
        )
    lines.append(f"(assert (distinct {' '.join(coordinate_names)}))")
    lines.append(f"(assert (= {coordinate_names[0]} 0))")
    requested = [*coordinate_names]

    for context_index, (name, source, target) in enumerate(contexts):
        prefix = f"k{context_index}_{_safe_name(name)}"
        phase_rows: list[list[tuple[str, ...]]] = [[], []]
        for side_name, rows in zip(("source", "target"), phase_rows, strict=True):
            initial = tuple(
                f"{prefix}_{side_name}_phasebit_0_{phase}"
                for phase in range(SCHEDULE_PERIOD)
            )
            for variable in initial:
                lines.append(f"(declare-const {variable} Bool)")
            lines.append(_exactly_one(initial))
            rows.append(initial)
            initial_value = f"{prefix}_{side_name}_phase_0"
            requested.append(initial_value)
            lines.append(f"(declare-const {initial_value} Int)")
            lines.append(
                f"(assert (= {initial_value} (+ "
                + " ".join(
                    f"(ite {variable} {phase} 0)"
                    for phase, variable in enumerate(initial)
                )
                + ")))"
            )

        for transition, ((source_left, source_right), (target_left, target_right)) in enumerate(
            zip(
                zip(source, source[1:]),
                zip(target, target[1:]),
                strict=True,
            )
        ):
            distance_bits = tuple(
                f"{prefix}_distancebit_{transition}_{distance}"
                for distance in range(1, plaintext_alphabet_size + 1)
            )
            for variable in distance_bits:
                lines.append(f"(declare-const {variable} Bool)")
            lines.append(_exactly_one(distance_bits))
            distance_value = f"{prefix}_distance_{transition}"
            requested.append(distance_value)
            lines.append(f"(declare-const {distance_value} Int)")
            lines.append(
                f"(assert (= {distance_value} (+ "
                + " ".join(
                    f"(ite {variable} {distance} 0)"
                    for distance, variable in enumerate(distance_bits, start=1)
                )
                + ")))"
            )

            for side, (left, right) in enumerate(
                (
                    (source_left, source_right),
                    (target_left, target_right),
                )
            ):
                current = phase_rows[side][-1]
                side_name = "source" if side == 0 else "target"
                following = tuple(
                    f"{prefix}_{side_name}_phasebit_{transition + 1}_{phase}"
                    for phase in range(SCHEDULE_PERIOD)
                )
                for variable in following:
                    lines.append(f"(declare-const {variable} Bool)")
                lines.append(_exactly_one(following))
                phase_rows[side].append(following)

                for phase, phase_bit in enumerate(current):
                    for distance, distance_bit in enumerate(
                        distance_bits,
                        start=1,
                    ):
                        next_phase = (
                            phase + direction * distance
                        ) % SCHEDULE_PERIOD
                        increment = weighted_increment(
                            phase,
                            distance,
                            weights,
                            direction=direction,
                        )
                        lines.append(
                            f"(assert (=> (and {phase_bit} {distance_bit}) "
                            f"(and {following[next_phase]} "
                            f"{_modular_delta_equation(left, right, increment)})))"
                        )

    lines.append("(check-sat)")
    if request_model:
        lines.append(f"(get-value ({' '.join(requested)}))")
    lines.append("(exit)")
    return "\n".join(lines) + "\n"


def build_hidden_gear_smt2(
    contexts: Sequence[ContextSequences],
    *,
    plaintext_alphabet_size: int,
    direction: int,
    weights: Sequence[int] | None = None,
    timeout_ms: int = 120_000,
    request_model: bool = True,
) -> str:
    """Build the exact hidden-83-disk compatibility formula.

    The outer-band weight is normalized to one.  This loses no model with a
    nonzero outer weight because 83 is prime: multiply every disk coordinate
    and band weight by the outer weight's modular inverse.  Each context gets
    independent initial phases and its own plaintext-distance sequence, making
    the encoding a necessary-condition screen rather than a full decoder.
    """

    _validate_direction(direction)
    if not contexts:
        raise ValueError("at least one context is required")
    if plaintext_alphabet_size < 2:
        raise ValueError("plaintext alphabet must contain at least two symbols")
    if timeout_ms < 1:
        raise ValueError("timeout must be positive")
    for _, source, target in contexts:
        if len(source) != len(target) or len(source) < 2:
            raise ValueError("every context needs equal nontrivial sequences")
        if any(not 0 <= value < MODULUS for value in (*source, *target)):
            raise ValueError("ciphertext label lies outside 0..82")

    observed = tuple(
        sorted(
            {
                value
                for _, source, target in contexts
                for value in (*source, *target)
            }
        )
    )
    fixed_weights = None
    if weights is not None:
        if len(weights) != 3:
            raise ValueError("the machine requires three band weights")
        normalized = tuple(int(weight) % MODULUS for weight in weights)
        if normalized[0] != 1:
            raise ValueError("hidden-model outer weight must be normalized to one")
        fixed_weights = normalized  # type: ignore[assignment]
        return _build_fixed_hidden_gear_smt2(
            contexts,
            plaintext_alphabet_size=plaintext_alphabet_size,
            direction=direction,
            weights=fixed_weights,
            timeout_ms=timeout_ms,
            request_model=request_model,
        )

    lines = [
        "(set-logic QF_LIA)",
        "(set-option :produce-models true)",
        f"(set-option :timeout {timeout_ms})",
    ]
    if fixed_weights is None:
        lines.extend(
            (
                "(declare-const weight_alternating Int)",
                "(declare-const weight_irregular Int)",
                "(assert (and (<= 0 weight_alternating) (< weight_alternating 83)))",
                "(assert (and (<= 0 weight_irregular) (< weight_irregular 83)))",
            )
        )

    coordinate_names = tuple(f"coord_{label}" for label in observed)
    for name in coordinate_names:
        lines.append(f"(declare-const {name} Int)")
        lines.append(f"(assert (and (<= 0 {name}) (< {name} 83)))")
    lines.append(f"(assert (distinct {' '.join(coordinate_names)}))")
    lines.append(f"(assert (= {coordinate_names[0]} 0))")

    requested = [*coordinate_names]
    if fixed_weights is None:
        requested[:0] = ["weight_alternating", "weight_irregular"]
    for context_index, (name, source, target) in enumerate(contexts):
        prefix = f"k{context_index}_{_safe_name(name)}"
        source_phase = f"{prefix}_source_phase_0"
        target_phase = f"{prefix}_target_phase_0"
        requested.extend((source_phase, target_phase))
        lines.append(f"(declare-const {source_phase} Int)")
        lines.append(f"(declare-const {target_phase} Int)")
        lines.append(
            f"(assert (and (<= 0 {source_phase}) (< {source_phase} 34)))"
        )
        lines.append(
            f"(assert (and (<= 0 {target_phase}) (< {target_phase} 34)))"
        )
        current_phases = [source_phase, target_phase]
        for transition, ((source_left, source_right), (target_left, target_right)) in enumerate(
            zip(
                zip(source, source[1:]),
                zip(target, target[1:]),
                strict=True,
            )
        ):
            distance = f"{prefix}_distance_{transition}"
            requested.append(distance)
            lines.append(f"(declare-const {distance} Int)")
            lines.append(
                f"(assert (and (<= 1 {distance}) "
                f"(<= {distance} {plaintext_alphabet_size})))"
            )
            for side, (left, right) in enumerate(
                (
                    (source_left, source_right),
                    (target_left, target_right),
                )
            ):
                phase = current_phases[side]
                increment = _append_symbolic_increment(
                    lines,
                    prefix=(
                        f"{prefix}_{'source' if side == 0 else 'target'}"
                        f"_transition_{transition}"
                    ),
                    phase=phase,
                    distance=distance,
                    direction=direction,
                    plaintext_alphabet_size=plaintext_alphabet_size,
                    fixed_weights=None,
                )
                lines.append(
                    f"(assert (= (mod (- coord_{right} coord_{left}) 83) "
                    f"{increment}))"
                )
                next_phase = f"{prefix}_{'source' if side == 0 else 'target'}_phase_{transition + 1}"
                lines.append(f"(declare-const {next_phase} Int)")
                lines.append(
                    f"(assert (= {next_phase} "
                    f"(mod (+ {phase} (* {direction} {distance})) 34)))"
                )
                current_phases[side] = next_phase

    lines.append("(check-sat)")
    if request_model:
        lines.append(f"(get-value ({' '.join(requested)}))")
    lines.append("(exit)")
    return "\n".join(lines) + "\n"


def _parse_hidden_witness(
    output: str,
    contexts: Sequence[ContextSequences],
    *,
    fixed_weights: tuple[int, int, int] | None,
) -> HiddenGearWitness | None:
    assignments = {
        name: int(value)
        for name, value in re.findall(r"\(([A-Za-z0-9_]+)\s+(-?\d+)\)", output)
    }
    coordinate_labels = tuple(
        sorted(
            {
                value
                for _, source, target in contexts
                for value in (*source, *target)
            }
        )
    )
    required = {*(f"coord_{label}" for label in coordinate_labels)}
    if fixed_weights is None:
        required.update(("weight_alternating", "weight_irregular"))
    witnesses = []
    for context_index, (name, source, _) in enumerate(contexts):
        prefix = f"k{context_index}_{_safe_name(name)}"
        source_phase = f"{prefix}_source_phase_0"
        target_phase = f"{prefix}_target_phase_0"
        distances = tuple(
            f"{prefix}_distance_{transition}"
            for transition in range(len(source) - 1)
        )
        required.update((source_phase, target_phase, *distances))
        if not {source_phase, target_phase, *distances} <= assignments.keys():
            return None
        witnesses.append(
            HiddenGearContextWitness(
                name,
                assignments[source_phase],
                assignments[target_phase],
                tuple(assignments[item] for item in distances),
            )
        )
    if not required <= assignments.keys():
        return None
    return HiddenGearWitness(
        tuple(
            (label, assignments[f"coord_{label}"])
            for label in coordinate_labels
        ),
        fixed_weights
        if fixed_weights is not None
        else (
            1,
            assignments["weight_alternating"],
            assignments["weight_irregular"],
        ),
        tuple(witnesses),
    )


def verify_hidden_witness(
    contexts: Sequence[ContextSequences],
    witness: HiddenGearWitness,
    *,
    direction: int,
) -> bool:
    """Replay every SMT witness transition in ordinary Python."""

    _validate_direction(direction)
    coordinates = dict(witness.coordinates)
    if (
        len(coordinates) != len(witness.coordinates)
        or len(set(coordinates.values())) != len(coordinates)
        or any(not 0 <= value < MODULUS for value in coordinates.values())
    ):
        return False
    by_name: Mapping[str, HiddenGearContextWitness] = {
        item.name: item for item in witness.contexts
    }
    if len(by_name) != len(witness.contexts):
        return False
    for name, source, target in contexts:
        if name not in by_name:
            return False
        item = by_name[name]
        if len(item.distances) != len(source) - 1:
            return False
        phases = [item.source_phase, item.target_phase]
        for transition, distance in enumerate(item.distances):
            if distance < 1:
                return False
            expected = [
                weighted_increment(
                    phase,
                    distance,
                    witness.weights,
                    direction=direction,
                )
                for phase in phases
            ]
            observed = [
                (
                    coordinates[sequence[transition + 1]]
                    - coordinates[sequence[transition]]
                )
                % MODULUS
                for sequence in (source, target)
            ]
            if expected != observed:
                return False
            phases = [
                (phase + direction * distance) % SCHEDULE_PERIOD
                for phase in phases
            ]
    return True


def solve_hidden_gear_with_z3(
    contexts: Sequence[ContextSequences],
    *,
    plaintext_alphabet_size: int,
    direction: int,
    weights: Sequence[int] | None = None,
    timeout_ms: int = 120_000,
    z3_path: str | None = None,
) -> HiddenGearResult:
    """Run and independently replay the hidden-disk compatibility formula."""

    executable = z3_path or shutil.which("z3")
    if executable is None:
        raise RuntimeError("z3 executable is unavailable")
    fixed_weights = None
    if weights is not None:
        if len(weights) != 3:
            raise ValueError("the machine requires three band weights")
        normalized = tuple(int(weight) % MODULUS for weight in weights)
        if normalized[0] != 1:
            raise ValueError("hidden-model outer weight must be normalized to one")
        fixed_weights = normalized  # type: ignore[assignment]
    formula = build_hidden_gear_smt2(
        contexts,
        plaintext_alphabet_size=plaintext_alphabet_size,
        direction=direction,
        weights=fixed_weights,
        timeout_ms=timeout_ms,
    )
    started = monotonic()
    try:
        completed = subprocess.run(
            (executable, "-in"),
            input=formula,
            text=True,
            capture_output=True,
            timeout=timeout_ms / 1_000 + 3,
            check=False,
        )
        output = completed.stdout + completed.stderr
    except subprocess.TimeoutExpired as error:
        output = (error.stdout or "") + (error.stderr or "")
        return HiddenGearResult(
            "unknown",
            None,
            monotonic() - started,
            len(formula.encode()),
            output,
        )

    first_line = output.lstrip().splitlines()[0] if output.strip() else ""
    status = first_line if first_line in {"sat", "unsat", "unknown"} else "error"
    witness = None
    if status == "sat":
        witness = _parse_hidden_witness(
            output,
            contexts,
            fixed_weights=fixed_weights,
        )
        if witness is None:
            raise AssertionError("SAT model omitted requested witness values")
        if not verify_hidden_witness(contexts, witness, direction=direction):
            raise AssertionError("hidden gear witness failed exact replay")
    return HiddenGearResult(
        status,
        witness,
        monotonic() - started,
        len(formula.encode()),
        output,
    )
