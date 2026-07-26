"""Header-control consumer for checksum self-pointer packet cardinalities."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, permutations, product
from math import comb

from eye_mystery.checksum_self_pointer import (
    MESSAGES_UNDER_TEST,
    circular_packet,
    circular_distance,
    euclidean_profile,
)
from eye_mystery.corpus import MESSAGE_ORDER
from eye_mystery.factoradic_headers import header_ranks
from eye_mystery.gate_plus3_transfer import control_edge


CHECKSUM_FAMILY = ("east1", "east3", "east5")
DEGREE_FEATURES = tuple(
    product(("source", "target"), ("in", "out"))
)
ORIENTATIONS = ("one-plus", "three-minus")


@dataclass(frozen=True)
class CardinalityRow:
    name: str
    edge: tuple[int, int]
    source_indegree: int
    packet_count: int

    @property
    def closes(self) -> bool:
        return self.source_indegree + self.packet_count == 3


@dataclass(frozen=True)
class FormulaHit:
    endpoint: str
    degree_direction: str
    orientation: str


@dataclass(frozen=True)
class AssignmentAudit:
    assignments: int
    exact_hits: int
    broad_hits: int
    exact_assignments: tuple[tuple[int, ...], ...]
    broad_assignments: tuple[tuple[int, ...], ...]
    observed_formula_hits: tuple[FormulaHit, ...]


@dataclass(frozen=True)
class TripleHit:
    names: tuple[str, str, str]
    counts: tuple[int, int, int]
    remainders: tuple[int, int, int]

    @property
    def all_close(self) -> bool:
        return self.remainders == (0, 0, 0)


@dataclass(frozen=True)
class CardinalityAudit:
    rows: tuple[CardinalityRow, ...]
    assignment: AssignmentAudit
    triple_hits: tuple[TripleHit, ...]
    sparse_matrix: tuple[tuple[int | None, ...], ...]
    natural_diagonal_probability: Fraction
    natural_any_target_probability: Fraction
    full_slot_probability: Fraction


def family_edges(
    names: tuple[str, ...],
) -> dict[str, tuple[int, int]]:
    ranks = header_ranks()
    return {name: control_edge(ranks[name]) for name in names}


def degree_maps(
    names: tuple[str, ...],
) -> tuple[Counter[int], Counter[int]]:
    edges = family_edges(names)
    indegrees = Counter(target for _source, target in edges.values())
    outdegrees = Counter(source for source, _target in edges.values())
    return indegrees, outdegrees


def quotient_occurrence_counts(
    names: tuple[str, ...],
) -> tuple[int, ...]:
    return tuple(euclidean_profile(name).body_occurrences for name in names)


def observed_rows() -> tuple[CardinalityRow, ...]:
    edges = family_edges(CHECKSUM_FAMILY)
    indegrees, _outdegrees = degree_maps(CHECKSUM_FAMILY)
    counts = quotient_occurrence_counts(CHECKSUM_FAMILY)
    return tuple(
        CardinalityRow(
            name=name,
            edge=edges[name],
            source_indegree=indegrees[edges[name][0]],
            packet_count=count,
        )
        for name, count in zip(CHECKSUM_FAMILY, counts, strict=True)
    )


def formula_hits(
    names: tuple[str, ...],
    counts: tuple[int, ...],
) -> tuple[FormulaHit, ...]:
    edges = family_edges(names)
    indegrees, outdegrees = degree_maps(names)
    results = []
    for endpoint, degree_direction in DEGREE_FEATURES:
        degrees = indegrees if degree_direction == "in" else outdegrees
        values = tuple(
            degrees[edges[name][0 if endpoint == "source" else 1]]
            for name in names
        )
        for orientation in ORIENTATIONS:
            predicted = tuple(
                1 + value if orientation == "one-plus" else 3 - value
                for value in values
            )
            if predicted == counts:
                results.append(
                    FormulaHit(endpoint, degree_direction, orientation)
                )
    return tuple(results)


def audit_count_assignments() -> AssignmentAudit:
    observed = quotient_occurrence_counts(CHECKSUM_FAMILY)
    exact_assignments = []
    broad_assignments = []
    for assignment in permutations(observed):
        rows = tuple(
            CardinalityRow(
                name=name,
                edge=family_edges(CHECKSUM_FAMILY)[name],
                source_indegree=degree_maps(CHECKSUM_FAMILY)[0][
                    family_edges(CHECKSUM_FAMILY)[name][0]
                ],
                packet_count=count,
            )
            for name, count in zip(CHECKSUM_FAMILY, assignment, strict=True)
        )
        if all(row.closes for row in rows):
            exact_assignments.append(assignment)
        if formula_hits(CHECKSUM_FAMILY, assignment):
            broad_assignments.append(assignment)
    return AssignmentAudit(
        assignments=6,
        exact_hits=len(exact_assignments),
        broad_hits=len(broad_assignments),
        exact_assignments=tuple(exact_assignments),
        broad_assignments=tuple(broad_assignments),
        observed_formula_hits=formula_hits(CHECKSUM_FAMILY, observed),
    )


def exact_cardinality_ledger(names: tuple[str, ...]) -> bool:
    if len(names) != 3:
        raise ValueError("the frozen ledger is defined for triples")
    edges = family_edges(names)
    indegrees, _outdegrees = degree_maps(names)
    counts = quotient_occurrence_counts(names)
    return all(
        count + indegrees[edges[name][0]] == 3
        for name, count in zip(names, counts, strict=True)
    )


def all_triple_hits() -> tuple[TripleHit, ...]:
    hits = []
    for names in combinations(MESSAGE_ORDER, 3):
        if not exact_cardinality_ledger(names):
            continue
        profiles = tuple(euclidean_profile(name) for name in names)
        hits.append(
            TripleHit(
                names=names,
                counts=tuple(item.body_occurrences for item in profiles),
                remainders=tuple(item.remainder for item in profiles),
            )
        )
    return tuple(hits)


def sparse_packet_matrix() -> tuple[tuple[int | None, ...], ...]:
    edges = family_edges(CHECKSUM_FAMILY)
    rows = []
    for row_name in CHECKSUM_FAMILY:
        source = edges[row_name][0]
        included = tuple(
            column_name
            for column_name in CHECKSUM_FAMILY
            if edges[column_name][1] != source
        )
        packet = circular_packet(euclidean_profile(row_name))
        if len(included) != len(packet):
            raise AssertionError("header incidence no longer matches packet size")
        lookup = dict(zip(included, packet, strict=True))
        rows.append(
            tuple(lookup.get(column_name) for column_name in CHECKSUM_FAMILY)
        )
    return tuple(rows)


def _selected_distance_distribution(
    name: str,
    selected_order_index: int,
) -> Counter[int]:
    item = euclidean_profile(name)
    counts: Counter[int] = Counter()
    for positions in combinations(
        range(1, item.length),
        item.body_occurrences,
    ):
        counts[
            circular_distance(
                positions[selected_order_index],
                item.quotient,
            )
        ] += 1
    return counts


def natural_diagonal_probability(
    targets: frozenset[int],
) -> Fraction:
    """Exact probability for the fixed stream-order diagonal."""

    selected_indices = (0, 1, 0)
    distributions = tuple(
        _selected_distance_distribution(name, index)
        for name, index in zip(
            MESSAGES_UNDER_TEST,
            selected_indices,
            strict=True,
        )
    )
    numerator = sum(
        left_count * middle_count * right_count
        for left, left_count in distributions[0].items()
        for middle, middle_count in distributions[1].items()
        for right, right_count in distributions[2].items()
        if left + middle + right in targets
    )
    denominator = 1
    for distribution in distributions:
        denominator *= sum(distribution.values())
    return Fraction(numerator, denominator)


def full_slot_probability(
    targets: frozenset[int] = frozenset((40, 56, 45)),
) -> Fraction:
    """Exact probability after allowing every within-row slot bijection."""

    left = euclidean_profile("east1")
    middle = euclidean_profile("east3")
    right = euclidean_profile("east5")
    middle_total = comb(middle.length - 1, middle.body_occurrences)
    middle_distance_counts = Counter(
        circular_distance(position, middle.quotient)
        for position in range(1, middle.length)
    )
    numerator = 0
    for left_positions in combinations(
        range(1, left.length),
        left.body_occurrences,
    ):
        left_distances = {
            circular_distance(position, left.quotient)
            for position in left_positions
        }
        for right_position in range(1, right.length):
            right_distance = circular_distance(
                right_position,
                right.quotient,
            )
            eligible_middle_distances = {
                target - left_distance - right_distance
                for target in targets
                for left_distance in left_distances
                if 0 <= target - left_distance - right_distance <= 41
            }
            eligible_positions = sum(
                middle_distance_counts[distance]
                for distance in eligible_middle_distances
            )
            numerator += middle_total - comb(
                middle.length - 1 - eligible_positions,
                middle.body_occurrences,
            )
    denominator = (
        comb(left.length - 1, left.body_occurrences)
        * middle_total
        * comb(right.length - 1, right.body_occurrences)
    )
    return Fraction(numerator, denominator)


def run_audit() -> CardinalityAudit:
    return CardinalityAudit(
        rows=observed_rows(),
        assignment=audit_count_assignments(),
        triple_hits=all_triple_hits(),
        sparse_matrix=sparse_packet_matrix(),
        natural_diagonal_probability=natural_diagonal_probability(
            frozenset((56,))
        ),
        natural_any_target_probability=natural_diagonal_probability(
            frozenset((40, 56, 45))
        ),
        full_slot_probability=full_slot_probability(),
    )
