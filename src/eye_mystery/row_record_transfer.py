"""Exact header-level audit of the final-row record grammar on earlier rows."""

from __future__ import annotations

import itertools
from collections.abc import Sequence
from dataclasses import dataclass

from eye_mystery.gap_anchor import MODULUS, ordinal_ranks


Order = tuple[int, int, int]
AnchorVector = tuple[int, int, int]

ROW1_HEADERS = (50, 80, 36)
ROW1_ORDERS: tuple[Order, ...] = ((0, 1, 2), (1, 2, 0), (2, 0, 1))
ROW1_TARGET_RANKS = (1, 2, 0)

ROW2_HEADERS = (76, 63, 34)
ROW2_ORDERS: tuple[Order, ...] = ((0, 2, 1), (2, 1, 0), (1, 0, 2))
ROW2_TARGET_RANKS = (2, 1, 0)

FINAL_HEADERS = (27, 77, 33)
FINAL_ORDERS: tuple[Order, ...] = ((0, 1, 2), (0, 2, 1), (1, 0, 2))
FINAL_TARGET_RANKS = (1, 2, 0)
FINAL_ANCHORS = (75, 81, 48)


def slot_headers(
    anchors: Sequence[int],
    orders: Sequence[Order],
) -> tuple[int, int, int]:
    """Apply the frozen source-minus-remaining slot rule."""

    if len(anchors) != 3 or len(orders) != 3:
        raise ValueError("the record grammar requires three anchors and orders")
    if any(sorted(order) != [0, 1, 2] for order in orders):
        raise ValueError("every component order must permute 0..2")
    return tuple(
        (anchors[order[0]] - anchors[order[2]]) % MODULUS
        for order in orders
    )  # type: ignore[return-value]


def feasible_anchor_vectors(
    headers: Sequence[int],
    orders: Sequence[Order],
) -> tuple[AnchorVector, ...]:
    """Enumerate all three-anchor vectors satisfying the frozen slot rule."""

    if len(headers) != 3:
        raise ValueError("the record grammar requires three headers")
    target = tuple(headers)
    return tuple(
        anchors
        for anchors in itertools.product(range(MODULUS), repeat=3)
        if slot_headers(anchors, orders) == target
    )


@dataclass(frozen=True)
class HeaderGrammarResult:
    name: str
    headers: tuple[int, int, int]
    orders: tuple[Order, ...]
    target_ranks: tuple[int, int, int]
    feasible_count: int
    distinct_feasible_count: int
    attainable_rank_patterns: tuple[tuple[int, int, int], ...]
    target_rank_count: int
    example: AnchorVector | None

    @property
    def numeric_feasible(self) -> bool:
        return self.feasible_count > 0

    @property
    def complete_grammar_feasible(self) -> bool:
        return self.target_rank_count > 0


def audit_header_grammar(
    name: str,
    headers: tuple[int, int, int],
    orders: tuple[Order, ...],
    target_ranks: tuple[int, int, int],
) -> HeaderGrammarResult:
    """Audit numeric feasibility and the withheld ordinal-rank field."""

    feasible = feasible_anchor_vectors(headers, orders)
    distinct = tuple(anchors for anchors in feasible if len(set(anchors)) == 3)
    patterns = tuple(sorted({ordinal_ranks(anchors) for anchors in distinct}))
    target_matches = tuple(
        anchors
        for anchors in distinct
        if ordinal_ranks(anchors) == target_ranks
    )
    return HeaderGrammarResult(
        name=name,
        headers=headers,
        orders=orders,
        target_ranks=target_ranks,
        feasible_count=len(feasible),
        distinct_feasible_count=len(distinct),
        attainable_rank_patterns=patterns,
        target_rank_count=len(target_matches),
        example=feasible[0] if feasible else None,
    )


def audit_all_rows() -> tuple[HeaderGrammarResult, ...]:
    """Return the two prospective rows and the known final-row calibration."""

    return (
        audit_header_grammar(
            "row1",
            ROW1_HEADERS,
            ROW1_ORDERS,
            ROW1_TARGET_RANKS,
        ),
        audit_header_grammar(
            "row2",
            ROW2_HEADERS,
            ROW2_ORDERS,
            ROW2_TARGET_RANKS,
        ),
        audit_header_grammar(
            "final",
            FINAL_HEADERS,
            FINAL_ORDERS,
            FINAL_TARGET_RANKS,
        ),
    )
