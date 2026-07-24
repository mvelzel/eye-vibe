"""Cheap screens from the twelfth breadth-first Eye-cipher horizon.

The module keeps five unrelated hypotheses small enough to calibrate:

* partial context maps as projective linear transformations;
* raw eye trigrams as header-conditioned Coxeter words in ``S6``;
* visible values as directed edges on nine hidden states;
* aligned panels as finite-field polynomial shares;
* the authored eye layout as a discrete vector field.

None of the functions scores language or proposes plaintext.
"""

from __future__ import annotations

import random
from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from itertools import combinations, permutations

from eye_mystery.corpus import (
    MESSAGE_ORDER,
    MESSAGES,
    ROW_PAIR_TRIGRAM_LENGTHS,
    trigram_values,
)
from eye_mystery.factoradic_headers import compose, lexicographic_unrank
from eye_mystery.ninth_causal import CONTEXT_SPECS
from eye_mystery.progression_certificate import context_mapping
from eye_mystery.visual_rows import visual_rows


Permutation = tuple[int, ...]
ProjectiveMatrix = tuple[int, int, int, int]
Orientation = tuple[bool, bool, bool]

IDENTITY_S6: Permutation = tuple(range(6))
ADJACENT_S6: tuple[Permutation, ...] = tuple(
    tuple(
        index + 1
        if index == adjacent
        else index - 1
        if index == adjacent + 1
        else index
        for index in range(6)
    )
    for adjacent in range(5)
)
COXETER_ASSIGNMENTS: tuple[tuple[int, ...], ...] = tuple(permutations(range(5)))
EDGE_ORIENTATIONS: tuple[Orientation, ...] = tuple(
    (swap, reverse_tail, reverse_head)
    for swap in (False, True)
    for reverse_tail in (False, True)
    for reverse_head in (False, True)
)


def eye_streams() -> dict[str, tuple[int, ...]]:
    return {
        name: trigram_values(MESSAGES[name])
        for name in MESSAGE_ORDER
    }


def eye_bodies() -> dict[str, tuple[int, ...]]:
    return {name: values[1:] for name, values in eye_streams().items()}


def context_mappings() -> tuple[dict[int, int], ...]:
    return tuple(
        context_mapping(left, left_start, right, right_start, length)
        for _, left, left_start, right, right_start, length in CONTEXT_SPECS
    )


def _homogeneous_null_vector(
    rows: Sequence[Sequence[int]], prime: int
) -> tuple[int, ...] | None:
    """Return the unique projective null vector, or ``None`` otherwise."""

    matrix = [[value % prime for value in row] for row in rows]
    if not matrix:
        return None
    width = len(matrix[0])
    pivots: list[int] = []
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
        inverse = pow(matrix[pivot_row][column], -1, prime)
        matrix[pivot_row] = [
            value * inverse % prime for value in matrix[pivot_row]
        ]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                (value - factor * pivot) % prime
                for value, pivot in zip(
                    matrix[row], matrix[pivot_row], strict=True
                )
            ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(matrix):
            break

    free = [column for column in range(width) if column not in pivots]
    if len(free) != 1:
        return None
    vector = [0] * width
    vector[free[0]] = 1
    for row, pivot in reversed(tuple(enumerate(pivots))):
        vector[pivot] = -sum(
            matrix[row][column] * vector[column]
            for column in free
        ) % prime
    first_nonzero = next((value for value in vector if value), None)
    if first_nonzero is None:
        return None
    scale = pow(first_nonzero, -1, prime)
    return tuple(value * scale % prime for value in vector)


def fit_mobius(
    pairs: Sequence[tuple[int, int]], prime: int
) -> ProjectiveMatrix | None:
    """Fit the unique Möbius map through three finite point pairs."""

    if len(pairs) != 3:
        raise ValueError("exactly three pairs determine a projective map")
    rows = [
        (source, 1, -source * target, -target)
        for source, target in pairs
    ]
    vector = _homogeneous_null_vector(rows, prime)
    if vector is None:
        return None
    a, b, c, d = vector
    if (a * d - b * c) % prime == 0:
        return None
    return a, b, c, d


def apply_mobius(
    matrix: ProjectiveMatrix, value: int, prime: int
) -> int | None:
    """Apply a finite-field Möbius map; ``None`` denotes infinity."""

    a, b, c, d = matrix
    denominator = (c * value + d) % prime
    if denominator == 0:
        return None
    return (a * value + b) * pow(denominator, -1, prime) % prime


@dataclass(frozen=True)
class ProjectiveContextScore:
    prime: int
    edge_counts: tuple[int, ...]
    maximum_supports: tuple[int, ...]

    @property
    def extra_support(self) -> int:
        return sum(support - 3 for support in self.maximum_supports)

    @property
    def exact_contexts(self) -> int:
        return sum(
            support == edges
            for support, edges in zip(
                self.maximum_supports, self.edge_counts, strict=True
            )
        )


def maximum_mobius_support(
    mapping: Mapping[int, int], prime: int
) -> tuple[int, ProjectiveMatrix]:
    """Return the best exact projective support among all three-edge fits."""

    items = tuple(sorted(mapping.items()))
    if len(items) < 3:
        raise ValueError("at least three edges are required")
    best_support = -1
    best_matrix = (0, 0, 0, 0)
    for selected in combinations(items, 3):
        matrix = fit_mobius(selected, prime)
        if matrix is None:
            continue
        support = sum(
            apply_mobius(matrix, source, prime) == target
            for source, target in items
        )
        if support > best_support or (
            support == best_support and matrix < best_matrix
        ):
            best_support = support
            best_matrix = matrix
    if best_support < 0:
        raise AssertionError("three distinct injective pairs must define PGL(2,p)")
    return best_support, best_matrix


def projective_context_score(
    mappings: Sequence[Mapping[int, int]], prime: int
) -> ProjectiveContextScore:
    supports = tuple(
        maximum_mobius_support(mapping, prime)[0] for mapping in mappings
    )
    return ProjectiveContextScore(
        prime,
        tuple(len(mapping) for mapping in mappings),
        supports,
    )


def shuffled_context_targets(
    mappings: Sequence[Mapping[int, int]], rng: random.Random
) -> tuple[dict[int, int], ...]:
    output = []
    for mapping in mappings:
        sources = tuple(sorted(mapping))
        targets = list(mapping.values())
        rng.shuffle(targets)
        output.append(dict(zip(sources, targets, strict=True)))
    return tuple(output)


def _header_eye_ranks(header_name: str) -> tuple[int, ...]:
    rank = trigram_values(MESSAGES[header_name])[0]
    order = tuple(
        symbol for symbol in lexicographic_unrank(rank) if symbol != 5
    )
    inverse = [0] * 5
    for position, symbol in enumerate(order):
        inverse[symbol] = position
    return tuple(inverse)


def coxeter_word(
    raw_trigram: Sequence[int],
    eye_ranks: Sequence[int],
    assignment: Sequence[int],
) -> Permutation:
    value = IDENTITY_S6
    for eye in raw_trigram:
        generator = ADJACENT_S6[assignment[eye_ranks[eye]]]
        value = compose(generator, value)
    return value


def coxeter_quotient_stream(
    message_name: str,
    header_name: str,
    assignment: Sequence[int],
) -> tuple[Permutation, ...]:
    raw = MESSAGES[message_name]
    ranks = _header_eye_ranks(header_name)
    return tuple(
        coxeter_word(raw[start : start + 3], ranks, assignment)
        for start in range(0, len(raw), 3)
    )


def _coxeter_context_scores(
    header_sources: Mapping[str, str],
    assignment: Sequence[int],
) -> tuple[int, ...]:
    streams = {
        name: coxeter_quotient_stream(
            name, header_sources[name], assignment
        )
        for name in MESSAGE_ORDER
    }
    return tuple(
        sum(
            source == target
            for source, target in zip(
                streams[left][left_start : left_start + length],
                streams[right][right_start : right_start + length],
                strict=True,
            )
        )
        for _, left, left_start, right, right_start, length in CONTEXT_SPECS
    )


@dataclass(frozen=True)
class CoxeterScan:
    natural_context_scores: tuple[int, ...]
    natural_distinct_states: tuple[int, ...]
    best_total: int
    best_total_assignment: tuple[int, ...]
    selected_training: int
    selected_heldout: int
    selected_assignment: tuple[int, ...]


@dataclass(frozen=True)
class CoxeterContextTable:
    """Precomputed context scores for all body/header/assignment choices."""

    # assignment -> context -> left-header -> right-header -> equal positions
    scores: tuple[
        tuple[tuple[tuple[int, ...], ...], ...], ...
    ]

    def context_scores(
        self,
        header_sources: Mapping[str, str],
        assignment_index: int,
    ) -> tuple[int, ...]:
        indices = {name: MESSAGE_ORDER.index(name) for name in MESSAGE_ORDER}
        output = []
        for context_index, spec in enumerate(CONTEXT_SPECS):
            _, left, _, right, _, _ = spec
            left_header = indices[header_sources[left]]
            right_header = indices[header_sources[right]]
            output.append(
                self.scores[assignment_index][context_index][left_header][
                    right_header
                ]
            )
        return tuple(output)


def build_coxeter_context_table() -> CoxeterContextTable:
    quotient = {
        (assignment_index, message, header): coxeter_quotient_stream(
            message, header, assignment
        )
        for assignment_index, assignment in enumerate(COXETER_ASSIGNMENTS)
        for message in MESSAGE_ORDER
        for header in MESSAGE_ORDER
    }
    assignment_rows = []
    for assignment_index in range(len(COXETER_ASSIGNMENTS)):
        context_rows = []
        for _, left, left_start, right, right_start, length in CONTEXT_SPECS:
            header_rows = []
            for left_header in MESSAGE_ORDER:
                target_rows = []
                left_values = quotient[
                    (assignment_index, left, left_header)
                ][left_start : left_start + length]
                for right_header in MESSAGE_ORDER:
                    right_values = quotient[
                        (assignment_index, right, right_header)
                    ][right_start : right_start + length]
                    target_rows.append(
                        sum(
                            left_value == right_value
                            for left_value, right_value in zip(
                                left_values, right_values, strict=True
                            )
                        )
                    )
                header_rows.append(tuple(target_rows))
            context_rows.append(tuple(header_rows))
        assignment_rows.append(tuple(context_rows))
    return CoxeterContextTable(tuple(assignment_rows))


def coxeter_scan(
    header_sources: Mapping[str, str] | None = None,
    *,
    table: CoxeterContextTable | None = None,
) -> CoxeterScan:
    if header_sources is None:
        header_sources = {name: name for name in MESSAGE_ORDER}
    if table is None:
        table = build_coxeter_context_table()
    natural = tuple(range(5))
    natural_index = COXETER_ASSIGNMENTS.index(natural)
    natural_scores = table.context_scores(
        header_sources, natural_index
    )
    natural_states = tuple(
        len(
            set(
                coxeter_quotient_stream(
                    name, header_sources[name], natural
                )[1:]
            )
        )
        for name in MESSAGE_ORDER
    )
    scored = []
    for assignment_index, assignment in enumerate(COXETER_ASSIGNMENTS):
        scores = table.context_scores(header_sources, assignment_index)
        scored.append((sum(scores), sum(scores[:6]), sum(scores[6:]), assignment))
    best_total_row = max(scored, key=lambda row: (row[0], tuple(-x for x in row[3])))
    best_training = max(row[1] for row in scored)
    selected = next(row for row in scored if row[1] == best_training)
    return CoxeterScan(
        natural_scores,
        natural_states,
        best_total_row[0],
        best_total_row[3],
        selected[1],
        selected[2],
        selected[3],
    )


def shuffled_header_sources(rng: random.Random) -> dict[str, str]:
    sources = list(MESSAGE_ORDER)
    rng.shuffle(sources)
    return dict(zip(MESSAGE_ORDER, sources, strict=True))


def value_edge(
    value: int, orientation: Orientation
) -> tuple[int, int] | None:
    if value >= 81:
        return None
    row, column = divmod(value, 9)
    swap, reverse_tail, reverse_head = orientation
    tail, head = (column, row) if swap else (row, column)
    if reverse_tail:
        tail = 8 - tail
    if reverse_head:
        head = 8 - head
    return tail, head


@dataclass(frozen=True)
class EdgePathScore:
    orientation: Orientation
    joins: int
    eligible: int
    sentinel_transitions: int
    loops: int


def edge_path_score(
    bodies: Mapping[str, Sequence[int]], orientation: Orientation
) -> EdgePathScore:
    joins = eligible = sentinels = loops = 0
    for body in bodies.values():
        for value in body:
            edge = value_edge(value, orientation)
            loops += edge is not None and edge[0] == edge[1]
        for left, right in zip(body, body[1:]):
            left_edge = value_edge(left, orientation)
            right_edge = value_edge(right, orientation)
            if left_edge is None or right_edge is None:
                sentinels += 1
                continue
            eligible += 1
            joins += left_edge[1] == right_edge[0]
    return EdgePathScore(orientation, joins, eligible, sentinels, loops)


@dataclass(frozen=True)
class EdgePathSplit:
    selected_orientation: Orientation
    training_joins: int
    training_eligible: int
    heldout_joins: int
    heldout_eligible: int
    all_scores: tuple[EdgePathScore, ...]


def edge_path_split(
    bodies: Mapping[str, Sequence[int]],
) -> EdgePathSplit:
    training_names = MESSAGE_ORDER[:4]
    heldout_names = MESSAGE_ORDER[4:]
    training = {name: bodies[name] for name in training_names}
    heldout = {name: bodies[name] for name in heldout_names}
    all_scores = tuple(
        edge_path_score(bodies, orientation)
        for orientation in EDGE_ORIENTATIONS
    )
    training_scores = tuple(
        edge_path_score(training, orientation)
        for orientation in EDGE_ORIENTATIONS
    )
    selected = max(
        training_scores,
        key=lambda score: (
            score.joins,
            tuple(-int(value) for value in score.orientation),
        ),
    )
    heldout_score = edge_path_score(heldout, selected.orientation)
    return EdgePathSplit(
        selected.orientation,
        selected.joins,
        selected.eligible,
        heldout_score.joins,
        heldout_score.eligible,
        all_scores,
    )


def relabel_bodies_as_edges(
    bodies: Mapping[str, Sequence[int]], rng: random.Random
) -> dict[str, tuple[int, ...]]:
    labels = list(range(81))
    rng.shuffle(labels)
    mapping = {source: target for source, target in enumerate(labels)}
    mapping.update({81: 81, 82: 82})
    return {
        name: tuple(mapping[value] for value in body)
        for name, body in bodies.items()
    }


def interpolate_polynomial(
    xs: Sequence[int], ys: Sequence[int], prime: int
) -> tuple[int, ...]:
    """Return monomial coefficients of the unique interpolating polynomial."""

    if len(xs) != len(ys) or not xs:
        raise ValueError("nonempty x/y samples must have equal length")
    if len(set(value % prime for value in xs)) != len(xs):
        raise ValueError("x coordinates must be distinct")
    coefficients = [0] * len(xs)
    for index, (x_value, y_value) in enumerate(zip(xs, ys, strict=True)):
        basis = [1]
        denominator = 1
        for other_index, other_x in enumerate(xs):
            if other_index == index:
                continue
            next_basis = [0] * (len(basis) + 1)
            for power, coefficient in enumerate(basis):
                next_basis[power] = (
                    next_basis[power] - other_x * coefficient
                ) % prime
                next_basis[power + 1] = (
                    next_basis[power + 1] + coefficient
                ) % prime
            basis = next_basis
            denominator = denominator * (x_value - other_x) % prime
        scale = y_value * pow(denominator, -1, prime) % prime
        for power, coefficient in enumerate(basis):
            coefficients[power] = (
                coefficients[power] + scale * coefficient
            ) % prime
    while len(coefficients) > 1 and coefficients[-1] == 0:
        coefficients.pop()
    return tuple(coefficients)


@dataclass(frozen=True)
class PolynomialShareScore:
    prime: int
    start_column: int
    columns: int
    degree_histogram: tuple[tuple[int, int], ...]

    def at_most(self, degree: int) -> int:
        return sum(count for value, count in self.degree_histogram if value <= degree)


def polynomial_share_score(
    bodies: Mapping[str, Sequence[int]],
    markers: Mapping[str, int],
    prime: int,
    *,
    start_column: int = 25,
) -> PolynomialShareScore:
    stop = min(len(bodies[name]) for name in MESSAGE_ORDER)
    xs = tuple(markers[name] for name in MESSAGE_ORDER)
    degrees = Counter()
    for column in range(start_column, stop):
        ys = tuple(bodies[name][column] for name in MESSAGE_ORDER)
        degree = len(interpolate_polynomial(xs, ys, prime)) - 1
        degrees[degree] += 1
    return PolynomialShareScore(
        prime,
        start_column,
        stop - start_column,
        tuple(sorted(degrees.items())),
    )


def shuffle_panel_columns(
    bodies: Mapping[str, Sequence[int]],
    rng: random.Random,
) -> dict[str, tuple[int, ...]]:
    mutable = {name: list(values) for name, values in bodies.items()}
    stop = min(len(bodies[name]) for name in MESSAGE_ORDER)
    for column in range(stop):
        values = [mutable[name][column] for name in MESSAGE_ORDER]
        rng.shuffle(values)
        for name, value in zip(MESSAGE_ORDER, values, strict=True):
            mutable[name][column] = value
    return {name: tuple(values) for name, values in mutable.items()}


DIRECTION_VECTORS = {
    0: (0, 0),
    1: (0, -1),
    2: (1, 0),
    3: (0, 1),
    4: (-1, 0),
}
NEIGHBOUR_OFFSETS = ((-2, 0), (2, 0), (-1, -1), (1, -1), (-1, 1), (1, 1))


def visual_field(
    message: Sequence[int], row_lengths: Sequence[int]
) -> dict[tuple[int, int], int]:
    rows = visual_rows(message, row_lengths)
    return {
        (2 * column + row_index % 2, row_index): direction
        for row_index, row in enumerate(rows)
        for column, direction in enumerate(row)
    }


def hodge_features(
    field: Mapping[tuple[int, int], int]
) -> dict[tuple[int, int], tuple[int, int]]:
    """Compute an integer divergence/curl stencil on the triangular lattice."""

    output = {}
    for coordinate, center_direction in field.items():
        x, y = coordinate
        neighbours = tuple(
            (x + dx, y + dy) for dx, dy in NEIGHBOUR_OFFSETS
        )
        if any(neighbour not in field for neighbour in neighbours):
            continue
        center_x, center_y = DIRECTION_VECTORS[center_direction]
        divergence = 0
        curl = 0
        for (dx, dy), neighbour in zip(
            NEIGHBOUR_OFFSETS, neighbours, strict=True
        ):
            neighbour_x, neighbour_y = DIRECTION_VECTORS[field[neighbour]]
            delta_x = neighbour_x - center_x
            delta_y = neighbour_y - center_y
            divergence += dx * delta_x + dy * delta_y
            curl += dx * delta_y - dy * delta_x
        output[coordinate] = divergence, curl
    return output


def _stencil_signature(
    field: Mapping[tuple[int, int], int], coordinate: tuple[int, int]
) -> tuple[int, ...]:
    x, y = coordinate
    return (
        field[coordinate],
        *(
            field[(x + dx, y + dy)]
            for dx, dy in NEIGHBOUR_OFFSETS
        ),
    )


@dataclass(frozen=True)
class HodgeScore:
    vertices: int
    distinct_features: int
    zero_features: int
    nontrivial_aligned_pairs: int
    aligned_feature_agreements: int

    @property
    def zero_rate(self) -> float:
        return self.zero_features / self.vertices

    @property
    def aligned_agreement_rate(self) -> float:
        return (
            self.aligned_feature_agreements / self.nontrivial_aligned_pairs
            if self.nontrivial_aligned_pairs
            else 0.0
        )


def hodge_score(
    messages: Mapping[str, Sequence[int]],
) -> HodgeScore:
    fields = {
        name: visual_field(messages[name], ROW_PAIR_TRIGRAM_LENGTHS[name])
        for name in MESSAGE_ORDER
    }
    features = {name: hodge_features(field) for name, field in fields.items()}
    all_values = [
        value for values in features.values() for value in values.values()
    ]
    nontrivial = agreements = 0
    for left_index, left_name in enumerate(MESSAGE_ORDER):
        for right_name in MESSAGE_ORDER[left_index + 1 :]:
            shared = features[left_name].keys() & features[right_name].keys()
            for coordinate in shared:
                if _stencil_signature(fields[left_name], coordinate) == (
                    _stencil_signature(fields[right_name], coordinate)
                ):
                    continue
                nontrivial += 1
                agreements += (
                    features[left_name][coordinate]
                    == features[right_name][coordinate]
                )
    return HodgeScore(
        len(all_values),
        len(set(all_values)),
        sum(value == (0, 0) for value in all_values),
        nontrivial,
        agreements,
    )


def shuffle_visual_rows(
    messages: Mapping[str, Sequence[int]],
    rng: random.Random,
) -> dict[str, tuple[int, ...]]:
    """Shuffle within every authored row while preserving its direction counts."""

    from eye_mystery.visual_rows import interleave_visual_rows

    output = {}
    for name in MESSAGE_ORDER:
        rows = [
            list(row)
            for row in visual_rows(
                messages[name], ROW_PAIR_TRIGRAM_LENGTHS[name]
            )
        ]
        for row in rows:
            rng.shuffle(row)
        output[name] = interleave_visual_rows(rows)
    return output
