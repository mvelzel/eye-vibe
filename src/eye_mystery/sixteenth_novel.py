"""Frozen A/C/D/E probes from the sixteenth wide Eye-cipher horizon."""

from __future__ import annotations

import random
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from itertools import combinations, permutations, product

from eye_mystery.corpus import (
    MESSAGE_ORDER,
    ROW_PAIR_TRIGRAM_LENGTHS,
)
from eye_mystery.factoradic_headers import inverse, lexicographic_unrank
from eye_mystery.fourteenth_selector import global_relabel
from eye_mystery.practice_cipher4_routes import PatternModel


Vector3 = tuple[int, int, int]
Matrix3 = tuple[Vector3, Vector3, Vector3]


def base5_digits(value: int) -> Vector3:
    if value not in range(125):
        raise ValueError("three base-five digits require a value in 0..124")
    return value // 25, value // 5 % 5, value % 5


def base5_rank(vector: Sequence[int]) -> int:
    if len(vector) != 3 or any(value not in range(5) for value in vector):
        raise ValueError("a base-five vector must contain three digits")
    return 25 * vector[0] + 5 * vector[1] + vector[2]


def normalize_projective(vector: Sequence[int]) -> tuple[Vector3, int]:
    """Return the canonical PG(2,5) point and its nonzero scalar."""

    if len(vector) != 3 or any(value not in range(5) for value in vector):
        raise ValueError("a projective vector must contain three F5 values")
    vector = tuple(vector)
    if vector == (0, 0, 0):
        raise ValueError("zero has no projective point")
    first = next(value for value in vector if value)
    inverse_first = pow(first, -1, 5)
    return (
        tuple(value * inverse_first % 5 for value in vector),
        first,
    )


PROJECTIVE_POINTS = tuple(
    sorted(
        {
            normalize_projective(vector)[0]
            for vector in product(range(5), repeat=3)
            if vector != (0, 0, 0)
        }
    )
)
PROJECTIVE_INDEX = {
    point: index for index, point in enumerate(PROJECTIVE_POINTS)
}
PROJECTIVE_SENTINEL = len(PROJECTIVE_POINTS)


def projective_point_scalar(value: int) -> tuple[int, int]:
    """Return point index/scalar; zero uses the dedicated index and scalar zero."""

    vector = base5_digits(value)
    if vector == (0, 0, 0):
        return PROJECTIVE_SENTINEL, 0
    point, scalar = normalize_projective(vector)
    return PROJECTIVE_INDEX[point], scalar


def projective_stream(values: Sequence[int]) -> tuple[int, ...]:
    return tuple(projective_point_scalar(value)[0] for value in values)


def scalar_stream(values: Sequence[int]) -> tuple[int, ...]:
    return tuple(projective_point_scalar(value)[1] for value in values)


def accepted_projective_multiplicities() -> tuple[int, ...]:
    counts = [0] * len(PROJECTIVE_POINTS)
    for value in range(1, 83):
        point, _ = projective_point_scalar(value)
        counts[point] += 1
    return tuple(counts)


def determinant_mod5(left: Vector3, middle: Vector3, right: Vector3) -> int:
    return (
        left[0] * (middle[1] * right[2] - middle[2] * right[1])
        - left[1] * (middle[0] * right[2] - middle[2] * right[0])
        + left[2] * (middle[0] * right[1] - middle[1] * right[0])
    ) % 5


@dataclass(frozen=True)
class ProjectiveConflict:
    context: str
    index: int
    direction: str
    point: int
    expected: int
    observed: int


@dataclass(frozen=True)
class CollinearityConflict:
    context: str
    indices: tuple[int, int, int]
    source_collinear: bool
    target_collinear: bool


@dataclass(frozen=True)
class ProjectiveContextScore:
    context: str
    edges: int
    distinct_source_points: int
    distinct_target_points: int
    functional: bool
    injective: bool
    triple_comparisons: int
    collinearity_agreements: int
    projective_conflict: ProjectiveConflict | None
    collinearity_conflict: CollinearityConflict | None

    @property
    def incidence_exact(self) -> bool:
        return (
            self.functional
            and self.injective
            and self.collinearity_agreements == self.triple_comparisons
        )


def projective_context_score(
    context: str,
    source: Sequence[int],
    target: Sequence[int],
) -> ProjectiveContextScore:
    """Test projected functionality, injectivity, and ternary incidence."""

    if len(source) != len(target):
        raise ValueError("projective context sequences must align")
    source_points = projective_stream(source)
    target_points = projective_stream(target)
    forward: dict[int, int] = {}
    reverse: dict[int, int] = {}
    projective_conflict = None
    functional = injective = True
    for index, (left, right) in enumerate(
        zip(source_points, target_points, strict=True)
    ):
        if left in forward and forward[left] != right:
            functional = False
            if projective_conflict is None:
                projective_conflict = ProjectiveConflict(
                    context,
                    index,
                    "forward",
                    left,
                    forward[left],
                    right,
                )
        else:
            forward[left] = right
        if right in reverse and reverse[right] != left:
            injective = False
            if projective_conflict is None:
                projective_conflict = ProjectiveConflict(
                    context,
                    index,
                    "reverse",
                    right,
                    reverse[right],
                    left,
                )
        else:
            reverse[right] = left

    triple_comparisons = agreements = 0
    collinearity_conflict = None
    if functional and injective:
        distinct_edges = tuple(sorted(forward.items()))
        for indices in combinations(range(len(distinct_edges)), 3):
            source_vectors = tuple(
                PROJECTIVE_POINTS[distinct_edges[index][0]]
                for index in indices
            )
            target_vectors = tuple(
                PROJECTIVE_POINTS[distinct_edges[index][1]]
                for index in indices
            )
            source_collinear = determinant_mod5(*source_vectors) == 0
            target_collinear = determinant_mod5(*target_vectors) == 0
            triple_comparisons += 1
            agreements += source_collinear == target_collinear
            if (
                source_collinear != target_collinear
                and collinearity_conflict is None
            ):
                collinearity_conflict = CollinearityConflict(
                    context,
                    indices,
                    source_collinear,
                    target_collinear,
                )
    return ProjectiveContextScore(
        context,
        len(source),
        len(set(source_points)),
        len(set(target_points)),
        functional,
        injective,
        triple_comparisons,
        agreements,
        projective_conflict,
        collinearity_conflict,
    )


def projective_context_audit(
    contexts: Sequence[tuple[str, Sequence[int], Sequence[int]]],
) -> tuple[ProjectiveContextScore, ...]:
    return tuple(
        projective_context_score(name, source, target)
        for name, source, target in contexts
    )


def apply_projective_matrix(value: int, matrix: Matrix3) -> int:
    """Apply a supplied F5 matrix and return the canonical output rank."""

    vector = base5_digits(value)
    target = tuple(
        sum(matrix[row][column] * vector[column] for column in range(3)) % 5
        for row in range(3)
    )
    if target == (0, 0, 0):
        return 0
    point, _ = normalize_projective(target)
    return base5_rank(point)


@dataclass(frozen=True)
class RayProjectionAudit:
    train_score: float
    heldout_score: float
    train_exceedances: int
    heldout_exceedances: int
    controls: int
    corrected_train_tail: float
    corrected_heldout_tail: float


def audit_ray_projection(
    streams: Mapping[str, Sequence[int]],
    model: PatternModel,
    *,
    train_names: Sequence[str],
    heldout_names: Sequence[str],
    controls: int,
    seed: int,
) -> RayProjectionAudit:
    if controls < 1:
        raise ValueError("at least one ray-projection control is required")
    train_score = model.score(
        tuple(projective_stream(streams[name]) for name in train_names)
    )
    heldout_score = model.score(
        tuple(projective_stream(streams[name]) for name in heldout_names)
    )
    train_exceedances = heldout_exceedances = 0
    generator = random.Random(seed)
    for _ in range(controls):
        mapping = list(range(83))
        generator.shuffle(mapping)
        control = global_relabel(streams, mapping)
        control_train = model.score(
            tuple(projective_stream(control[name]) for name in train_names)
        )
        control_heldout = model.score(
            tuple(projective_stream(control[name]) for name in heldout_names)
        )
        train_exceedances += control_train >= train_score
        heldout_exceedances += control_heldout >= heldout_score
    denominator = controls + 1
    return RayProjectionAudit(
        train_score,
        heldout_score,
        train_exceedances,
        heldout_exceedances,
        controls,
        (train_exceedances + 1) / denominator,
        (heldout_exceedances + 1) / denominator,
    )


@dataclass(frozen=True, order=True)
class DyckSpec:
    route: str
    pairing: str

    @property
    def name(self) -> str:
        return f"{self.route}-{self.pairing}"


def dyck_specs() -> tuple[DyckSpec, ...]:
    return tuple(
        DyckSpec(route, pairing)
        for route in ("header", "inverse")
        for pairing in ("aligned", "reversed")
    )


@dataclass(frozen=True)
class DyckScan:
    valid_prefix: int
    symbols: int
    final_depth: int
    contradiction_index: int | None
    expected_type: int | None
    observed_type: int | None

    @property
    def valid(self) -> bool:
        return self.contradiction_index is None


def _dyck_order(header: int, route: str) -> tuple[int, ...]:
    order = lexicographic_unrank(header)
    if route == "header":
        return order
    if route == "inverse":
        return inverse(order)
    raise ValueError(f"unknown Dyck header route: {route}")


def dyck_scan(tape: Sequence[int], header: int, spec: DyckSpec) -> DyckScan:
    if any(symbol not in range(6) for symbol in tape):
        raise ValueError("Dyck renderer symbols must lie in 0..5")
    order = _dyck_order(header, spec.route)
    opens = {symbol: index for index, symbol in enumerate(order[:3])}
    close_order = order[3:] if spec.pairing == "aligned" else tuple(reversed(order[3:]))
    closes = {symbol: index for index, symbol in enumerate(close_order)}
    stack: list[int] = []
    for index, symbol in enumerate(tape):
        if symbol in opens:
            stack.append(opens[symbol])
            continue
        observed = closes[symbol]
        expected = stack[-1] if stack else None
        if expected != observed:
            return DyckScan(
                index,
                len(tape),
                len(stack),
                index,
                expected,
                observed,
            )
        stack.pop()
    return DyckScan(len(tape), len(tape), len(stack), None, None, None)


@dataclass(frozen=True)
class DyckCandidateScore:
    spec: DyckSpec
    training_prefix: int
    training_symbols: int
    heldout_prefix: int
    heldout_symbols: int
    training_valid_panels: int
    heldout_valid_panels: int
    first_training_contradiction: tuple[str, DyckScan] | None
    first_heldout_contradiction: tuple[str, DyckScan] | None

    @property
    def exact(self) -> bool:
        return (
            self.training_prefix == self.training_symbols
            and self.heldout_prefix == self.heldout_symbols
        )


def dyck_candidate_score(
    tapes: Mapping[str, Sequence[int]],
    headers: Mapping[str, int],
    spec: DyckSpec,
    *,
    train_names: Sequence[str],
    heldout_names: Sequence[str],
) -> DyckCandidateScore:
    def score(names: Sequence[str]):
        prefix = symbols = valid = 0
        first = None
        for name in names:
            scan = dyck_scan(tapes[name], headers[name], spec)
            prefix += scan.valid_prefix
            symbols += scan.symbols
            valid += scan.valid
            if not scan.valid and first is None:
                first = name, scan
        return prefix, symbols, valid, first

    training = score(train_names)
    heldout = score(heldout_names)
    return DyckCandidateScore(
        spec,
        training[0],
        training[1],
        heldout[0],
        heldout[1],
        training[2],
        heldout[2],
        training[3],
        heldout[3],
    )


def audit_dyck_syntax(
    tapes: Mapping[str, Sequence[int]],
    headers: Mapping[str, int],
    *,
    train_names: Sequence[str],
    heldout_names: Sequence[str],
) -> tuple[DyckCandidateScore, tuple[DyckCandidateScore, ...]]:
    scores = tuple(
        dyck_candidate_score(
            tapes,
            headers,
            spec,
            train_names=train_names,
            heldout_names=heldout_names,
        )
        for spec in dyck_specs()
    )
    selected = min(
        scores,
        key=lambda score: (
            -score.training_prefix,
            -score.training_valid_panels,
            score.spec,
        ),
    )
    return selected, scores


def canonical_cycle(values: Sequence[int]) -> tuple[int, ...]:
    values = tuple(values)
    if len(values) != 5 or sorted(values) != list(range(5)):
        raise ValueError("a rotor cycle must permute 0..4")
    rotations = tuple(values[offset:] + values[:offset] for offset in range(5))
    return min(rotations)


def local_successor_words(
    stream: Sequence[int],
) -> tuple[tuple[int, ...], ...]:
    if any(value not in range(5) for value in stream):
        raise ValueError("a raw rotor stream must use directions 0..4")
    output = [[] for _ in range(5)]
    for current, following in zip(stream, stream[1:]):
        output[current].append(following)
    return tuple(tuple(word) for word in output)


def cycle_word_compatible(word: Sequence[int], cycle: Sequence[int]) -> bool:
    if not word:
        return True
    cycle = tuple(cycle)
    starts = tuple(index for index, value in enumerate(cycle) if value == word[0])
    return any(
        all(value == cycle[(start + index) % 5] for index, value in enumerate(word))
        for start in starts
    )


@dataclass(frozen=True)
class RotorContradiction:
    panel: str
    current: int
    occurrence: int
    reason: str
    expected: int | None
    observed: int | None
    prefix: tuple[int, ...]


@dataclass(frozen=True)
class RotorFit:
    cycles: tuple[tuple[int, ...], ...]
    observations: int
    contradiction: RotorContradiction | None

    @property
    def exact(self) -> bool:
        return self.contradiction is None


def _first_cycle_from_word(word: Sequence[int]) -> tuple[int, ...] | None:
    if len(word) < 5:
        return None
    first = tuple(word[:5])
    if sorted(first) != list(range(5)):
        return ()
    cycle = canonical_cycle(first)
    return cycle if cycle_word_compatible(word, cycle) else ()


def fit_rotor_cycles(
    streams: Mapping[str, Sequence[int]],
    *,
    initial: Sequence[Sequence[int]] | None = None,
) -> RotorFit:
    words = {name: local_successor_words(stream) for name, stream in streams.items()}
    cycles: list[tuple[int, ...] | None] = (
        [tuple(cycle) for cycle in initial]
        if initial is not None
        else [None] * 5
    )
    observations = 0
    for current in range(5):
        if cycles[current] is None:
            for name in streams:
                candidate = _first_cycle_from_word(words[name][current])
                if candidate == ():
                    word = words[name][current]
                    return RotorFit(
                        tuple(cycle or () for cycle in cycles),
                        observations,
                        RotorContradiction(
                            name,
                            current,
                            min(4, len(word) - 1),
                            "first-five-not-permutation",
                            None,
                            word[min(4, len(word) - 1)],
                            tuple(word[:5]),
                        ),
                    )
                if candidate is not None:
                    cycles[current] = candidate
                    break
        if cycles[current] is None:
            return RotorFit(tuple(cycle or () for cycle in cycles), observations, None)
        cycle = cycles[current]
        for name in streams:
            word = words[name][current]
            observations += len(word)
            if cycle_word_compatible(word, cycle):
                continue
            start = cycle.index(word[0]) if word and word[0] in cycle else 0
            mismatch = next(
                index
                for index, value in enumerate(word)
                if value != cycle[(start + index) % 5]
            )
            return RotorFit(
                tuple(value or () for value in cycles),
                observations,
                RotorContradiction(
                    name,
                    current,
                    mismatch,
                    "periodic-order-mismatch",
                    cycle[(start + mismatch) % 5],
                    word[mismatch],
                    tuple(word[: max(5, mismatch + 1)]),
                ),
            )
    return RotorFit(
        tuple(cycle or () for cycle in cycles),
        observations,
        None,
    )


@dataclass(frozen=True)
class RotorAudit:
    training: RotorFit
    heldout: RotorFit | None

    @property
    def exact(self) -> bool:
        return (
            self.training.exact
            and self.heldout is not None
            and self.heldout.exact
        )


def audit_rotor_router(
    streams: Mapping[str, Sequence[int]],
    *,
    train_names: Sequence[str],
    heldout_names: Sequence[str],
) -> RotorAudit:
    training = fit_rotor_cycles({name: streams[name] for name in train_names})
    heldout = (
        fit_rotor_cycles(
            {name: streams[name] for name in heldout_names},
            initial=training.cycles,
        )
        if training.exact and all(len(cycle) == 5 for cycle in training.cycles)
        else None
    )
    return RotorAudit(training, heldout)


Field25 = tuple[int, int]


@dataclass(frozen=True, order=True)
class Field25Spec:
    linear: int
    constant: int

    @property
    def name(self) -> str:
        return f"x2+{self.linear}x+{self.constant}"


def field25_specs() -> tuple[Field25Spec, ...]:
    """Return the ten monic irreducible quadratics over F5."""

    output = []
    for linear in range(5):
        for constant in range(5):
            if all(
                (root * root + linear * root + constant) % 5
                for root in range(5)
            ):
                output.append(Field25Spec(linear, constant))
    return tuple(output)


def f25_add(left: Field25, right: Field25) -> Field25:
    return (left[0] + right[0]) % 5, (left[1] + right[1]) % 5


def f25_sub(left: Field25, right: Field25) -> Field25:
    return (left[0] - right[0]) % 5, (left[1] - right[1]) % 5


def f25_mul(
    left: Field25,
    right: Field25,
    field: Field25Spec,
) -> Field25:
    quadratic = left[0] * right[0]
    x_coefficient = left[0] * right[1] + left[1] * right[0]
    constant = left[1] * right[1]
    return (
        x_coefficient - field.linear * quadratic
    ) % 5, (
        constant - field.constant * quadratic
    ) % 5


def f25_pow(value: Field25, exponent: int, field: Field25Spec) -> Field25:
    result = (0, 1)
    base = value
    while exponent:
        if exponent & 1:
            result = f25_mul(result, base, field)
        base = f25_mul(base, base, field)
        exponent //= 2
    return result


def f25_inv(value: Field25, field: Field25Spec) -> Field25:
    if value == (0, 0):
        raise ZeroDivisionError("zero has no F25 inverse")
    return f25_pow(value, 23, field)


def f25_div(
    left: Field25,
    right: Field25,
    field: Field25Spec,
) -> Field25:
    return f25_mul(left, f25_inv(right, field), field)


F25_ELEMENTS = tuple(product(range(5), repeat=2))
EYE_PAIRS = tuple(permutations(range(3), 2))


@dataclass(frozen=True, order=True)
class RowCodeSpec:
    field: Field25Spec
    eye_pair: tuple[int, int]
    reverse: bool
    degree: int

    @property
    def name(self) -> str:
        direction = "reverse" if self.reverse else "forward"
        return (
            f"{self.field.name}-eyes{self.eye_pair[0]}{self.eye_pair[1]}"
            f"-{direction}-d{self.degree}"
        )


def row_code_specs() -> tuple[RowCodeSpec, ...]:
    return tuple(
        RowCodeSpec(field, eye_pair, reverse, degree)
        for field in field25_specs()
        for eye_pair in EYE_PAIRS
        for reverse in (False, True)
        for degree in range(6)
    )


def solve_linear_f25(
    matrix: Sequence[Sequence[Field25]],
    values: Sequence[Field25],
    field: Field25Spec,
) -> tuple[Field25, ...] | None:
    size = len(values)
    work = [list(row) + [values[index]] for index, row in enumerate(matrix)]
    for column in range(size):
        pivot = next(
            (
                row
                for row in range(column, size)
                if work[row][column] != (0, 0)
            ),
            None,
        )
        if pivot is None:
            return None
        work[column], work[pivot] = work[pivot], work[column]
        inverse_pivot = f25_inv(work[column][column], field)
        work[column] = [
            f25_mul(value, inverse_pivot, field)
            for value in work[column]
        ]
        for row in range(size):
            if row == column or work[row][column] == (0, 0):
                continue
            factor = work[row][column]
            work[row] = [
                f25_sub(
                    work[row][index],
                    f25_mul(factor, work[column][index], field),
                )
                for index in range(size + 1)
            ]
    return tuple(work[row][-1] for row in range(size))


def evaluate_polynomial_f25(
    coefficients: Sequence[Field25],
    value: Field25,
    field: Field25Spec,
) -> Field25:
    result = (0, 0)
    for coefficient in reversed(coefficients):
        result = f25_add(f25_mul(result, value, field), coefficient)
    return result


def row_symbols(
    row: Sequence[int],
    spec: RowCodeSpec,
) -> tuple[Field25, ...]:
    if len(row) != 26:
        raise ValueError("an extended F25 row must have 26 symbols")
    values = tuple(reversed(row)) if spec.reverse else tuple(row)
    return tuple(
        (
            base5_digits(value)[spec.eye_pair[0]],
            base5_digits(value)[spec.eye_pair[1]],
        )
        for value in values
    )


def row_code_coefficients(
    row: Sequence[int],
    spec: RowCodeSpec,
) -> tuple[Field25, ...] | None:
    """Return coefficients iff the row is an exact degree-d extended codeword."""

    outputs = row_symbols(row, spec)
    size = spec.degree + 1
    positions = F25_ELEMENTS
    matrix = tuple(
        tuple(f25_pow(positions[row_index], degree, spec.field) for degree in range(size))
        for row_index in range(size)
    )
    coefficients = solve_linear_f25(matrix, outputs[:size], spec.field)
    if coefficients is None:
        return None
    if any(
        evaluate_polynomial_f25(coefficients, position, spec.field) != output
        for position, output in zip(positions, outputs[:25], strict=True)
    ):
        return None
    if outputs[25] != coefficients[-1]:
        return None
    if spec.degree and coefficients[-1] == (0, 0):
        return None
    return coefficients


def complete_rows(
    streams: Mapping[str, Sequence[int]],
) -> dict[str, tuple[tuple[int, ...], ...]]:
    output = {}
    for name in streams:
        cursor = 0
        rows = []
        for length in ROW_PAIR_TRIGRAM_LENGTHS[name]:
            row = tuple(streams[name][cursor : cursor + length])
            cursor += length
            if length == 26:
                rows.append(row)
        if cursor != len(streams[name]):
            raise ValueError(f"row lengths do not partition {name}")
        output[name] = tuple(rows)
    return output


@dataclass(frozen=True)
class RowCodeScore:
    spec: RowCodeSpec
    exact_rows: int
    rows: int

    @property
    def exact(self) -> bool:
        return self.exact_rows == self.rows


@dataclass(frozen=True)
class RowCodeAudit:
    selected: RowCodeSpec
    training: RowCodeScore
    heldout: RowCodeScore
    exact_training_specs: tuple[str, ...]

    @property
    def exact(self) -> bool:
        return self.training.exact and self.heldout.exact


def row_code_score(
    rows: Mapping[str, Sequence[Sequence[int]]],
    names: Sequence[str],
    spec: RowCodeSpec,
) -> RowCodeScore:
    selected_rows = tuple(row for name in names for row in rows[name])
    exact = sum(row_code_coefficients(row, spec) is not None for row in selected_rows)
    return RowCodeScore(spec, exact, len(selected_rows))


def audit_row_codes(
    streams: Mapping[str, Sequence[int]],
    *,
    train_names: Sequence[str],
    heldout_names: Sequence[str],
) -> RowCodeAudit:
    rows = complete_rows(streams)
    training_scores = tuple(
        row_code_score(rows, train_names, spec) for spec in row_code_specs()
    )
    selected = min(
        training_scores,
        key=lambda score: (-score.exact_rows, score.spec),
    )
    return RowCodeAudit(
        selected.spec,
        selected,
        row_code_score(rows, heldout_names, selected.spec),
        tuple(score.spec.name for score in training_scores if score.exact),
    )
