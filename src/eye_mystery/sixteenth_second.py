"""Frozen B/H/I probes from the sixteenth wide Eye-cipher horizon."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from itertools import combinations, permutations, product

from eye_mystery.factoradic_headers import (
    compose,
    inverse,
    lexicographic_unrank,
)


Permutation = tuple[int, ...]
Duad = tuple[int, int]
Syntheme = tuple[Duad, Duad, Duad]
Pentad = tuple[Syntheme, ...]


def perfect_matchings(values: Sequence[int]) -> tuple[Syntheme, ...]:
    values = tuple(values)
    if not values:
        return ((),)  # type: ignore[return-value]
    first = values[0]
    output = []
    for index in range(1, len(values)):
        second = values[index]
        remainder = values[1:index] + values[index + 1 :]
        for matching in perfect_matchings(remainder):
            output.append(
                tuple(sorted(((min(first, second), max(first, second)), *matching)))
            )
    return tuple(sorted(set(output)))


DUADS: tuple[Duad, ...] = tuple(combinations(range(6), 2))
SYNTHEMES: tuple[Syntheme, ...] = perfect_matchings(tuple(range(6)))


def enumerate_pentads() -> tuple[Pentad, ...]:
    target = frozenset(DUADS)
    output = []
    for candidate in combinations(SYNTHEMES, 5):
        flat = tuple(duad for syntheme in candidate for duad in syntheme)
        if len(set(flat)) == 15 and frozenset(flat) == target:
            output.append(tuple(sorted(candidate)))
    return tuple(sorted(output))


PENTADS = enumerate_pentads()
PENTAD_INDEX = {pentad: index for index, pentad in enumerate(PENTADS)}
S6 = tuple(permutations(range(6)))
S6_RANK = {permutation: rank for rank, permutation in enumerate(S6)}


def act_duad(permutation: Permutation, duad: Duad) -> Duad:
    return tuple(sorted((permutation[duad[0]], permutation[duad[1]])))


def act_syntheme(permutation: Permutation, syntheme: Syntheme) -> Syntheme:
    return tuple(sorted(act_duad(permutation, duad) for duad in syntheme))


def act_pentad(permutation: Permutation, pentad: Pentad) -> Pentad:
    return tuple(sorted(act_syntheme(permutation, syntheme) for syntheme in pentad))


def outer_automorphism(permutation: Permutation) -> Permutation:
    """Return the action on the six lexicographically ordered pentads."""

    if sorted(permutation) != list(range(6)):
        raise ValueError("the outer map requires an S6 permutation")
    return tuple(
        PENTAD_INDEX[act_pentad(permutation, pentad)]
        for pentad in PENTADS
    )


@dataclass(frozen=True, order=True)
class OuterSpec:
    conjugator_rank: int
    route: str

    @property
    def name(self) -> str:
        return f"c{self.conjugator_rank:03d}-{self.route}"


def outer_specs() -> tuple[OuterSpec, ...]:
    return tuple(
        OuterSpec(rank, route)
        for rank in range(len(S6))
        for route in ("header", "inverse")
    )


def outer_header_action(header: int, spec: OuterSpec) -> Permutation:
    header_permutation = lexicographic_unrank(header)
    if spec.route == "inverse":
        header_permutation = inverse(header_permutation)
    elif spec.route != "header":
        raise ValueError(f"unknown outer route: {spec.route}")
    image = outer_automorphism(header_permutation)
    conjugator = S6[spec.conjugator_rank]
    return compose(conjugator, compose(image, inverse(conjugator)))


def apply_permutation(
    values: Sequence[int],
    permutation: Permutation,
) -> tuple[int, ...]:
    if sorted(permutation) != list(range(6)):
        raise ValueError("renderer action must permute 0..5")
    if any(value not in range(6) for value in values):
        raise ValueError("renderer tape contains a symbol outside 0..5")
    return tuple(permutation[value] for value in values)


def newline_mismatches(
    tape: Sequence[int],
    expected_mask: Sequence[bool],
) -> int:
    if len(tape) != len(expected_mask):
        raise ValueError("newline mask length does not match renderer tape")
    return sum(
        (value == 5) != expected
        for value, expected in zip(tape, expected_mask, strict=True)
    )


@dataclass(frozen=True)
class OuterActionScore:
    spec: OuterSpec
    training_mismatches: int
    training_symbols: int
    heldout_mismatches: int
    heldout_symbols: int
    training_panel_mismatches: tuple[tuple[str, int], ...]
    heldout_panel_mismatches: tuple[tuple[str, int], ...]

    @property
    def exact(self) -> bool:
        return self.training_mismatches == self.heldout_mismatches == 0


def outer_action_score(
    tapes: Mapping[str, Sequence[int]],
    headers: Mapping[str, int],
    expected_masks: Mapping[str, Sequence[bool]],
    spec: OuterSpec,
    *,
    train_names: Sequence[str],
    heldout_names: Sequence[str],
) -> OuterActionScore:
    def score(names: Sequence[str]):
        panels = []
        symbols = 0
        for name in names:
            decoded = apply_permutation(
                tapes[name],
                outer_header_action(headers[name], spec),
            )
            mismatch = newline_mismatches(decoded, expected_masks[name])
            panels.append((name, mismatch))
            symbols += len(decoded)
        return tuple(panels), sum(value for _, value in panels), symbols

    training = score(train_names)
    heldout = score(heldout_names)
    return OuterActionScore(
        spec,
        training[1],
        training[2],
        heldout[1],
        heldout[2],
        training[0],
        heldout[0],
    )


@dataclass(frozen=True)
class OuterActionAudit:
    selected: OuterActionScore
    exact_training_specs: tuple[str, ...]
    catalog_size: int


def audit_outer_actions(
    tapes: Mapping[str, Sequence[int]],
    headers: Mapping[str, int],
    expected_masks: Mapping[str, Sequence[bool]],
    *,
    train_names: Sequence[str],
    heldout_names: Sequence[str],
) -> OuterActionAudit:
    scores = tuple(
        outer_action_score(
            tapes,
            headers,
            expected_masks,
            spec,
            train_names=train_names,
            heldout_names=heldout_names,
        )
        for spec in outer_specs()
    )
    selected = min(
        scores,
        key=lambda score: (score.training_mismatches, score.spec),
    )
    return OuterActionAudit(
        selected,
        tuple(
            score.spec.name for score in scores if score.training_mismatches == 0
        ),
        len(scores),
    )


@dataclass(frozen=True, order=True)
class NecklaceSpec:
    route: str
    reverse: bool

    @property
    def name(self) -> str:
        return f"{self.route}-{'reverse' if self.reverse else 'forward'}"


def necklace_specs() -> tuple[NecklaceSpec, ...]:
    return tuple(
        NecklaceSpec(route, reverse)
        for route in ("header", "inverse")
        for reverse in (False, True)
    )


def ranked_renderer_word(
    tape: Sequence[int],
    header: int,
    spec: NecklaceSpec,
) -> tuple[int, ...]:
    order = lexicographic_unrank(header)
    if spec.route == "inverse":
        order = inverse(order)
    elif spec.route != "header":
        raise ValueError(f"unknown necklace route: {spec.route}")
    ranks = {symbol: rank for rank, symbol in enumerate(order)}
    values = tuple(reversed(tape)) if spec.reverse else tuple(tape)
    return tuple(ranks[value] for value in values)


def least_rotation_index(word: Sequence[int]) -> int:
    """Return the least cyclic rotation with Booth's linear-time algorithm."""

    word = tuple(word)
    if not word:
        raise ValueError("a necklace word must be nonempty")
    doubled = word + word
    left, right, offset = 0, 1, 0
    size = len(word)
    while left < size and right < size and offset < size:
        first = doubled[left + offset]
        second = doubled[right + offset]
        if first == second:
            offset += 1
            continue
        if first > second:
            left = left + offset + 1
            if left == right:
                left += 1
        else:
            right = right + offset + 1
            if left == right:
                right += 1
        offset = 0
    return min(left, right)


def prefix_function(word: Sequence[int]) -> tuple[int, ...]:
    result = [0] * len(word)
    for index in range(1, len(word)):
        border = result[index - 1]
        while border and word[index] != word[border]:
            border = result[border - 1]
        if word[index] == word[border]:
            border += 1
        result[index] = border
    return tuple(result)


def primitive_period(word: Sequence[int]) -> int:
    if not word:
        raise ValueError("a word must be nonempty")
    border = prefix_function(word)[-1]
    period = len(word) - border
    return period if len(word) % period == 0 else len(word)


def duval_factor_count(word: Sequence[int]) -> int:
    """Count factors in the canonical nonincreasing Lyndon factorization."""

    size = len(word)
    index = factors = 0
    while index < size:
        start = index
        following = index + 1
        while following < size and word[index] <= word[following]:
            if word[index] < word[following]:
                index = start
            else:
                index += 1
            following += 1
        factor_length = following - index
        while start <= index:
            factors += 1
            start += factor_length
        index = start
    return factors


@dataclass(frozen=True)
class NecklacePanel:
    name: str
    least_rotation: int
    length: int
    primitive_period: int
    border: int
    lyndon_factors: int

    @property
    def canonical(self) -> bool:
        return self.least_rotation == 0

    @property
    def primitive(self) -> bool:
        return self.primitive_period == self.length


@dataclass(frozen=True)
class NecklaceScore:
    spec: NecklaceSpec
    training: tuple[NecklacePanel, ...]
    heldout: tuple[NecklacePanel, ...]

    @property
    def training_canonical(self) -> int:
        return sum(panel.canonical for panel in self.training)

    @property
    def heldout_canonical(self) -> int:
        return sum(panel.canonical for panel in self.heldout)

    @property
    def training_primitive(self) -> int:
        return sum(panel.primitive for panel in self.training)

    @property
    def exact(self) -> bool:
        return (
            self.training_canonical == len(self.training)
            and self.heldout_canonical == len(self.heldout)
        )


def necklace_panel(
    name: str,
    tape: Sequence[int],
    header: int,
    spec: NecklaceSpec,
) -> NecklacePanel:
    word = ranked_renderer_word(tape, header, spec)
    prefix = prefix_function(word)
    return NecklacePanel(
        name,
        least_rotation_index(word),
        len(word),
        primitive_period(word),
        prefix[-1],
        duval_factor_count(word),
    )


def audit_necklaces(
    tapes: Mapping[str, Sequence[int]],
    headers: Mapping[str, int],
    *,
    train_names: Sequence[str],
    heldout_names: Sequence[str],
) -> tuple[NecklaceScore, tuple[NecklaceScore, ...]]:
    scores = tuple(
        NecklaceScore(
            spec,
            tuple(
                necklace_panel(name, tapes[name], headers[name], spec)
                for name in train_names
            ),
            tuple(
                necklace_panel(name, tapes[name], headers[name], spec)
                for name in heldout_names
            ),
        )
        for spec in necklace_specs()
    )
    selected = min(
        scores,
        key=lambda score: (
            -score.training_canonical,
            -score.training_primitive,
            score.spec,
        ),
    )
    return selected, scores


Field125 = tuple[int, int, int]
ZERO125: Field125 = (0, 0, 0)
ONE125: Field125 = (0, 0, 1)


@dataclass(frozen=True, order=True)
class Field125Spec:
    quadratic: int
    linear: int
    constant: int

    @property
    def name(self) -> str:
        return f"t3+{self.quadratic}t2+{self.linear}t+{self.constant}"


def field125_specs() -> tuple[Field125Spec, ...]:
    output = []
    for quadratic, linear, constant in product(range(5), repeat=3):
        if all(
            (
                root**3
                + quadratic * root**2
                + linear * root
                + constant
            )
            % 5
            for root in range(5)
        ):
            output.append(Field125Spec(quadratic, linear, constant))
    return tuple(output)


def f125_add(left: Field125, right: Field125) -> Field125:
    return tuple((a + b) % 5 for a, b in zip(left, right, strict=True))


def f125_neg(value: Field125) -> Field125:
    return tuple(-item % 5 for item in value)


def f125_sub(left: Field125, right: Field125) -> Field125:
    return f125_add(left, f125_neg(right))


def f125_mul(
    left: Field125,
    right: Field125,
    field: Field125Spec,
) -> Field125:
    left_low = tuple(reversed(left))
    right_low = tuple(reversed(right))
    coefficients = [0] * 5
    for first, a in enumerate(left_low):
        for second, b in enumerate(right_low):
            coefficients[first + second] = (
                coefficients[first + second] + a * b
            ) % 5
    polynomial = (field.constant, field.linear, field.quadratic, 1)
    for degree in range(4, 2, -1):
        factor = coefficients[degree]
        if not factor:
            continue
        shift = degree - 3
        for offset, coefficient in enumerate(polynomial):
            coefficients[shift + offset] = (
                coefficients[shift + offset] - factor * coefficient
            ) % 5
    return tuple(reversed(coefficients[:3]))


def f125_pow(value: Field125, exponent: int, field: Field125Spec) -> Field125:
    result = ONE125
    base = value
    while exponent:
        if exponent & 1:
            result = f125_mul(result, base, field)
        base = f125_mul(base, base, field)
        exponent //= 2
    return result


def f125_inv(value: Field125, field: Field125Spec) -> Field125:
    if value == ZERO125:
        raise ZeroDivisionError("zero has no GF(125) inverse")
    return f125_pow(value, 123, field)


def f125_div(
    left: Field125,
    right: Field125,
    field: Field125Spec,
) -> Field125:
    return f125_mul(left, f125_inv(right, field), field)


def field125_value(rank: int) -> Field125:
    if rank not in range(125):
        raise ValueError("GF(125) rank must lie in 0..124")
    return rank // 25, rank // 5 % 5, rank % 5


def field125_rank(value: Field125) -> int:
    if any(item not in range(5) for item in value):
        raise ValueError("GF(125) coefficients must lie in F5")
    return 25 * value[0] + 5 * value[1] + value[2]


@dataclass(frozen=True, order=True)
class GF125Representation:
    field: Field125Spec
    frobenius: int

    @property
    def name(self) -> str:
        return f"{self.field.name}-frob{self.frobenius}"


def gf125_representations() -> tuple[GF125Representation, ...]:
    return tuple(
        GF125Representation(field, frobenius)
        for field in field125_specs()
        for frobenius in range(3)
    )


MobiusCoefficients = tuple[Field125, Field125, Field125, Field125]


def normalize_mobius(
    coefficients: MobiusCoefficients,
    field: Field125Spec,
) -> MobiusCoefficients:
    first = next(value for value in coefficients if value != ZERO125)
    scale = f125_inv(first, field)
    return tuple(f125_mul(value, scale, field) for value in coefficients)


def nullspace_dimension_one(
    matrix: Sequence[Sequence[Field125]],
    field: Field125Spec,
) -> MobiusCoefficients | None:
    rows = [list(row) for row in matrix]
    row_count = len(rows)
    column_count = 4
    pivot_columns = []
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (
                row
                for row in range(pivot_row, row_count)
                if rows[row][column] != ZERO125
            ),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        scale = f125_inv(rows[pivot_row][column], field)
        rows[pivot_row] = [
            f125_mul(value, scale, field) for value in rows[pivot_row]
        ]
        for row in range(row_count):
            if row == pivot_row or rows[row][column] == ZERO125:
                continue
            factor = rows[row][column]
            rows[row] = [
                f125_sub(
                    rows[row][index],
                    f125_mul(factor, rows[pivot_row][index], field),
                )
                for index in range(column_count)
            ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == row_count:
            break
    free_columns = [
        column for column in range(column_count) if column not in pivot_columns
    ]
    if len(free_columns) != 1:
        return None
    free = free_columns[0]
    result = [ZERO125] * column_count
    result[free] = ONE125
    for row, column in reversed(tuple(enumerate(pivot_columns))):
        result[column] = f125_neg(rows[row][free])
    return normalize_mobius(tuple(result), field)  # type: ignore[arg-type]


def fit_mobius_three(
    edges: Sequence[tuple[int, int]],
    representation: GF125Representation,
) -> MobiusCoefficients | None:
    if len(edges) != 3:
        raise ValueError("a Möbius fit requires exactly three edges")
    field = representation.field
    rows = []
    for source_rank, target_rank in edges:
        source = f125_pow(
            field125_value(source_rank),
            5 ** representation.frobenius,
            field,
        )
        target = field125_value(target_rank)
        target_source = f125_mul(target, source, field)
        rows.append(
            (
                source,
                ONE125,
                f125_neg(target_source),
                f125_neg(target),
            )
        )
    coefficients = nullspace_dimension_one(rows, field)
    if coefficients is None:
        return None
    first, second, third, fourth = coefficients
    determinant = f125_sub(
        f125_mul(first, fourth, field),
        f125_mul(second, third, field),
    )
    return coefficients if determinant != ZERO125 else None


def apply_mobius(
    source_rank: int,
    representation: GF125Representation,
    coefficients: MobiusCoefficients,
) -> int | None:
    field = representation.field
    source = f125_pow(
        field125_value(source_rank),
        5 ** representation.frobenius,
        field,
    )
    first, second, third, fourth = coefficients
    numerator = f125_add(f125_mul(first, source, field), second)
    denominator = f125_add(f125_mul(third, source, field), fourth)
    if denominator == ZERO125:
        return None
    return field125_rank(f125_div(numerator, denominator, field))


@dataclass(frozen=True)
class MobiusContextScore:
    context: str
    representation: GF125Representation
    matches: int
    edges: int
    coefficients: MobiusCoefficients | None
    fit_indices: tuple[int, int, int] | None
    first_contradiction: tuple[int, int | None, int] | None

    @property
    def exact(self) -> bool:
        return self.matches == self.edges


def mobius_context_score(
    context: str,
    source: Sequence[int],
    target: Sequence[int],
    representation: GF125Representation,
) -> MobiusContextScore:
    if len(source) != len(target):
        raise ValueError("Möbius context sequences must align")
    edges = tuple(zip(source, target, strict=True))
    best = None
    seen_coefficients: set[MobiusCoefficients] = set()
    for indices in combinations(range(len(edges)), 3):
        coefficients = fit_mobius_three(
            tuple(edges[index] for index in indices),
            representation,
        )
        if coefficients is None or coefficients in seen_coefficients:
            continue
        seen_coefficients.add(coefficients)
        predictions = tuple(
            apply_mobius(left, representation, coefficients)
            for left, _ in edges
        )
        matches = sum(
            prediction == right
            for prediction, (_, right) in zip(predictions, edges, strict=True)
        )
        contradiction = next(
            (
                (index, predictions[index], edges[index][1])
                for index in range(len(edges))
                if predictions[index] != edges[index][1]
            ),
            None,
        )
        candidate = (
            matches,
            tuple(field125_rank(value) for value in coefficients),
            indices,
            coefficients,
            contradiction,
        )
        if best is None or (
            candidate[0],
            tuple(-value for value in candidate[1]),
            tuple(-value for value in candidate[2]),
        ) > (
            best[0],
            tuple(-value for value in best[1]),
            tuple(-value for value in best[2]),
        ):
            best = candidate
        if matches == len(edges):
            break
    if best is None:
        return MobiusContextScore(
            context,
            representation,
            0,
            len(edges),
            None,
            None,
            (0, None, edges[0][1]) if edges else None,
        )
    return MobiusContextScore(
        context,
        representation,
        best[0],
        len(edges),
        best[3],
        best[2],
        best[4],
    )


@dataclass(frozen=True)
class GF125Audit:
    selected: GF125Representation
    training: tuple[MobiusContextScore, ...]
    heldout: tuple[MobiusContextScore, ...]
    exact_training_representations: tuple[str, ...]
    catalog_size: int

    @property
    def training_exact_contexts(self) -> int:
        return sum(score.exact for score in self.training)

    @property
    def heldout_exact_contexts(self) -> int:
        return sum(score.exact for score in self.heldout)

    @property
    def exact(self) -> bool:
        return (
            self.training_exact_contexts == len(self.training)
            and self.heldout_exact_contexts == len(self.heldout)
        )


def audit_gf125_contexts(
    contexts: Sequence[tuple[str, Sequence[int], Sequence[int]]],
    *,
    train_names: frozenset[str],
    heldout_names: frozenset[str],
) -> GF125Audit:
    training_contexts = tuple(item for item in contexts if item[0] in train_names)
    heldout_contexts = tuple(item for item in contexts if item[0] in heldout_names)
    if not training_contexts or not heldout_contexts:
        raise ValueError("GF125 audit requires both context families")
    representations = gf125_representations()
    scored = []
    for representation in representations:
        scores = tuple(
            mobius_context_score(name, source, target, representation)
            for name, source, target in training_contexts
        )
        scored.append((representation, scores))
    selected_representation, selected_scores = min(
        scored,
        key=lambda item: (
            -sum(score.exact for score in item[1]),
            -sum(score.matches for score in item[1]),
            item[0],
        ),
    )
    return GF125Audit(
        selected_representation,
        selected_scores,
        tuple(
            mobius_context_score(
                name,
                source,
                target,
                selected_representation,
            )
            for name, source, target in heldout_contexts
        ),
        tuple(
            representation.name
            for representation, scores in scored
            if all(score.exact for score in scores)
        ),
        len(representations),
    )
