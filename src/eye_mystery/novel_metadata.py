"""Small cross-layer checks from the post-Earthquake breadth pass."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations

from eye_mystery.conformance_grid import (
    edge_component_order,
    marker_control_edge,
)
from eye_mystery.corpus import MESSAGES, trigram_values
from eye_mystery.factoradic_headers import (
    Q_MESSAGES,
    fixed_symbols,
    header_ranks,
    lexicographic_unrank,
)
from eye_mystery.fifteenth_second import NATURAL_OPENING_TRIMS
from eye_mystery.gap_anchor import clean_gap_anchors, relative_position_order


NATURAL_ROWS = (
    ("east1", "west1", "east2"),
    ("west2", "east3", "west3"),
    ("east4", "west4", "east5"),
)


@dataclass(frozen=True)
class RangeDescriptor:
    quotient: int
    radix: int
    remainder: int

    @property
    def size(self) -> int:
        return self.quotient * self.radix**2 + self.remainder

    @property
    def maximum_digits(self) -> tuple[int, int, int]:
        value = self.size - 1
        return (
            value // self.radix**2,
            value // self.radix % self.radix,
            value % self.radix,
        )


def range_descriptor(size: int = 83, radix: int = 5) -> RangeDescriptor:
    """Describe a three-digit radix cube prefix by full slabs and a tail."""

    if radix < 2 or not 1 <= size <= radix**3:
        raise ValueError("size must be a nonempty prefix of the radix cube")
    quotient, remainder = divmod(size, radix**2)
    return RangeDescriptor(quotient, radix, remainder)


def descriptor_permutation_matches(
    digits: tuple[int, int, int] = (3, 5, 8),
    *,
    target: int = 83,
) -> tuple[tuple[int, int, int], ...]:
    """Return orders satisfying ``q * radix**2 + remainder = target``."""

    return tuple(
        order
        for order in permutations(digits)
        if order[0] * order[1] ** 2 + order[2] == target
    )


def q_headers_are_noncenter_derangements() -> bool:
    """Whether every Q factoradic header fixes center and no other symbol."""

    ranks = header_ranks()
    return all(
        fixed_symbols(lexicographic_unrank(ranks[name])) == (0,)
        for name in Q_MESSAGES
    )


@dataclass(frozen=True)
class RowStagger:
    messages: tuple[str, str, str]
    middle_order: tuple[int, int, int]
    unique_gap_records: tuple[
        tuple[
            int,
            tuple[int, int, int],
            tuple[int, int, int] | None,
            tuple[int, int, int],
        ],
        ...,
    ]


def row_staggers(
    *,
    minimum_gap: int = 2,
    maximum_gap: int = 30,
) -> tuple[RowStagger, ...]:
    """Audit the literal middle-header consecutive-stagger generalization."""

    values = {
        name: trigram_values(MESSAGES[name])
        for row in NATURAL_ROWS
        for name in row
    }
    results = []
    for row in NATURAL_ROWS:
        bodies = {
            name: values[name][1 + NATURAL_OPENING_TRIMS[name] :]
            for name in row
        }
        middle_order = edge_component_order(
            marker_control_edge(values[row[1]][0])
        )
        records = []
        for gap in range(minimum_gap, maximum_gap + 1):
            hits = tuple(
                clean_gap_anchors(
                    bodies[name],
                    minimum_gap=gap,
                    maximum_gap=gap,
                ).get(gap, ())
                for name in row
            )
            if not all(len(message_hits) == 1 for message_hits in hits):
                continue
            positions = tuple(message_hits[0].position for message_hits in hits)
            anchors = tuple(message_hits[0].value for message_hits in hits)
            records.append(
                (
                    gap,
                    positions,
                    relative_position_order(positions),
                    anchors,
                )
            )
        results.append(RowStagger(row, middle_order, tuple(records)))
    return tuple(results)
