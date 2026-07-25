"""Conditional audit of the Gate/Veska ``+3`` operator on Eye headers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

from eye_mystery.corpus import MESSAGE_ORDER
from eye_mystery.factoradic_headers import (
    base5_digits,
    compose,
    generated_group,
    header_ranks,
    inverse,
    lexicographic_unrank,
    permutation_order,
    unique_multiset_permutations,
)


MODULUS = 83
SHIFT = 3
ROWS = (
    ("east1", "west1", "east2"),
    ("west2", "east3", "west3"),
    ("east4", "west4", "east5"),
)
FINAL_SELF = "east4"
FINAL_NONSELF = ("west4", "east5")

Permutation = tuple[int, ...]


def control_edge(rank: int) -> tuple[int, int]:
    """Return the established ``middle -> first-1`` header edge."""

    first, middle, _scalar = base5_digits(rank)
    if first not in (1, 2, 3):
        raise ValueError("rank does not encode an observed three-state edge")
    return middle, first - 1


def nonself_messages(
    row: Sequence[str],
    ranks: Mapping[str, int],
) -> tuple[str, ...]:
    """Return a row's messages whose frozen control edge is not a loop."""

    return tuple(name for name in row if len(set(control_edge(ranks[name]))) == 2)


@dataclass(frozen=True)
class Transfer:
    source_name: str
    source_rank: int
    target_name: str
    target_rank: int
    left_quotient: Permutation
    right_quotient: Permutation


def quotient_pair(source_rank: int, target_rank: int) -> tuple[Permutation, Permutation]:
    """Return target/source quotients under both multiplication conventions."""

    source = lexicographic_unrank(source_rank)
    target = lexicographic_unrank(target_rank)
    return (
        compose(target, inverse(source)),
        compose(inverse(source), target),
    )


def transfers_between_rows(
    ranks: Mapping[str, int],
    source_row: Sequence[str],
    target_row: Sequence[str],
    *,
    shift: int = SHIFT,
) -> tuple[Transfer, ...]:
    """Apply one shift to source non-self fields and retain target-row hits."""

    targets = {ranks[name]: name for name in target_row}
    transfers = []
    for source_name in nonself_messages(source_row, ranks):
        source_rank = ranks[source_name]
        target_rank = (source_rank + shift) % MODULUS
        target_name = targets.get(target_rank)
        if target_name is None:
            continue
        left, right = quotient_pair(source_rank, target_rank)
        transfers.append(
            Transfer(
                source_name=source_name,
                source_rank=source_rank,
                target_name=target_name,
                target_rank=target_rank,
                left_quotient=left,
                right_quotient=right,
            )
        )
    return tuple(transfers)


def shared_quotient(
    transfers: Sequence[Transfer],
    *,
    side: str,
) -> Permutation | None:
    """Return a quotient shared by at least two complete transfers."""

    if len(transfers) < 2:
        return None
    if side == "left":
        values = tuple(transfer.left_quotient for transfer in transfers)
    elif side == "right":
        values = tuple(transfer.right_quotient for transfer in transfers)
    else:
        raise ValueError("side must be 'left' or 'right'")
    return values[0] if len(set(values)) == 1 else None


def complete_transfer(
    ranks: Mapping[str, int],
    source_row: Sequence[str],
    target_row: Sequence[str],
    *,
    shift: int = SHIFT,
) -> tuple[Transfer, ...] | None:
    """Return all transfers iff every source non-self field lands in target."""

    eligible = nonself_messages(source_row, ranks)
    transfers = transfers_between_rows(
        ranks,
        source_row,
        target_row,
        shift=shift,
    )
    return transfers if len(transfers) == len(eligible) else None


def observed_transfers() -> tuple[Transfer, ...]:
    """Return the fixed final-row-to-first-row ``+3`` transfers."""

    ranks = header_ranks()
    result = complete_transfer(ranks, ROWS[2], ROWS[0])
    if result is None:
        raise AssertionError("observed complete transfer disappeared")
    return result


def cycle_structure(permutation: Permutation) -> tuple[int, ...]:
    """Return sorted nontrivial cycle lengths."""

    visited: set[int] = set()
    lengths = []
    for start in range(len(permutation)):
        if start in visited:
            continue
        current = start
        length = 0
        while current not in visited:
            visited.add(current)
            length += 1
            current = permutation[current]
        if length > 1:
            lengths.append(length)
    return tuple(sorted(lengths, reverse=True))


@dataclass(frozen=True)
class ObservedAudit:
    transfers: tuple[Transfer, ...]
    self_shift_rank: int
    self_shift_target: str | None
    shared_left: Permutation | None
    shared_right: Permutation | None
    shared_left_cycles: tuple[int, ...] | None
    shared_right_cycles: tuple[int, ...] | None
    shared_left_order: int | None
    shared_right_order: int | None
    shared_left_in_p_d4: bool
    shared_right_in_p_d4: bool


def audit_observed() -> ObservedAudit:
    ranks = header_ranks()
    transfers = observed_transfers()
    shifted_self = (ranks[FINAL_SELF] + SHIFT) % MODULUS
    target_lookup = {rank: name for name, rank in ranks.items()}
    left = shared_quotient(transfers, side="left")
    right = shared_quotient(transfers, side="right")
    p_group = generated_group(
        lexicographic_unrank(ranks[name]) for name in ROWS[0]
    )
    return ObservedAudit(
        transfers=transfers,
        self_shift_rank=shifted_self,
        self_shift_target=target_lookup.get(shifted_self),
        shared_left=left,
        shared_right=right,
        shared_left_cycles=cycle_structure(left) if left is not None else None,
        shared_right_cycles=cycle_structure(right) if right is not None else None,
        shared_left_order=permutation_order(left) if left is not None else None,
        shared_right_order=permutation_order(right) if right is not None else None,
        shared_left_in_p_d4=left in p_group if left is not None else False,
        shared_right_in_p_d4=right in p_group if right is not None else False,
    )


def assignment_ranks(assignment: Sequence[int]) -> dict[str, int]:
    """Rebuild ranks while holding the observed first two digits fixed."""

    if len(assignment) != len(MESSAGE_ORDER):
        raise ValueError("one scalar is required per message")
    observed = header_ranks()
    return {
        name: 25 * base5_digits(observed[name])[0]
        + 5 * base5_digits(observed[name])[1]
        + scalar
        for name, scalar in zip(MESSAGE_ORDER, assignment, strict=True)
    }


def admissible_assignment_ranks() -> tuple[dict[str, int], ...]:
    """Return the existing 12,096-member conditional universe."""

    observed = header_ranks()
    scalars = tuple(base5_digits(observed[name])[2] for name in MESSAGE_ORDER)
    results = []
    for assignment in unique_multiset_permutations(scalars):
        ranks = assignment_ranks(assignment)
        if max(ranks.values()) > 82 or len(set(ranks.values())) != 9:
            continue
        results.append(ranks)
    return tuple(results)


@dataclass(frozen=True)
class ConditionalAudit:
    assignments: int
    exact_complete: int
    exact_complete_self_absent: int
    exact_shared_left: int
    exact_shared_right: int
    exact_shared_either: int
    broad_any_complete: int
    broad_any_complete_shared: int
    broad_max_hits_at_least_observed: int
    broad_max_fraction_complete: int


def audit_conditional() -> ConditionalAudit:
    """Enumerate exact and broadened transfer events under the fixed null."""

    counts = {
        "exact_complete": 0,
        "exact_complete_self_absent": 0,
        "exact_shared_left": 0,
        "exact_shared_right": 0,
        "exact_shared_either": 0,
        "broad_any_complete": 0,
        "broad_any_complete_shared": 0,
        "broad_max_hits": 0,
        "broad_max_fraction": 0,
    }
    assignments = admissible_assignment_ranks()
    for ranks in assignments:
        exact = complete_transfer(ranks, ROWS[2], ROWS[0])
        if exact is not None:
            counts["exact_complete"] += 1
            shifted_self = (ranks[FINAL_SELF] + SHIFT) % MODULUS
            if shifted_self not in set(ranks.values()):
                counts["exact_complete_self_absent"] += 1
            left = shared_quotient(exact, side="left")
            right = shared_quotient(exact, side="right")
            counts["exact_shared_left"] += left is not None
            counts["exact_shared_right"] += right is not None
            counts["exact_shared_either"] += left is not None or right is not None

        any_complete = False
        any_complete_shared = False
        max_hits = 0
        max_fraction = 0.0
        for source_index, source_row in enumerate(ROWS):
            eligible_count = len(nonself_messages(source_row, ranks))
            for target_index, target_row in enumerate(ROWS):
                if source_index == target_index:
                    continue
                transfers = transfers_between_rows(ranks, source_row, target_row)
                max_hits = max(max_hits, len(transfers))
                max_fraction = max(
                    max_fraction,
                    len(transfers) / eligible_count,
                )
                if len(transfers) != eligible_count:
                    continue
                any_complete = True
                if (
                    shared_quotient(transfers, side="left") is not None
                    or shared_quotient(transfers, side="right") is not None
                ):
                    any_complete_shared = True
        counts["broad_any_complete"] += any_complete
        counts["broad_any_complete_shared"] += any_complete_shared
        counts["broad_max_hits"] += max_hits >= len(FINAL_NONSELF)
        counts["broad_max_fraction"] += max_fraction == 1.0

    return ConditionalAudit(
        assignments=len(assignments),
        exact_complete=counts["exact_complete"],
        exact_complete_self_absent=counts["exact_complete_self_absent"],
        exact_shared_left=counts["exact_shared_left"],
        exact_shared_right=counts["exact_shared_right"],
        exact_shared_either=counts["exact_shared_either"],
        broad_any_complete=counts["broad_any_complete"],
        broad_any_complete_shared=counts["broad_any_complete_shared"],
        broad_max_hits_at_least_observed=counts["broad_max_hits"],
        broad_max_fraction_complete=counts["broad_max_fraction"],
    )


@dataclass(frozen=True)
class ShiftHit:
    shift: int
    source_row: int
    target_row: int
    transfer_count: int
    shared_left: bool
    shared_right: bool


def scan_observed_shifts() -> tuple[ShiftHit, ...]:
    """Enumerate nonzero shifts producing any complete observed row transfer."""

    ranks = header_ranks()
    hits = []
    for shift in range(1, MODULUS):
        for source_index, source_row in enumerate(ROWS):
            for target_index, target_row in enumerate(ROWS):
                if source_index == target_index:
                    continue
                transfers = complete_transfer(
                    ranks,
                    source_row,
                    target_row,
                    shift=shift,
                )
                if transfers is None:
                    continue
                hits.append(
                    ShiftHit(
                        shift=shift,
                        source_row=source_index + 1,
                        target_row=target_index + 1,
                        transfer_count=len(transfers),
                        shared_left=shared_quotient(
                            transfers,
                            side="left",
                        )
                        is not None,
                        shared_right=shared_quotient(
                            transfers,
                            side="right",
                        )
                        is not None,
                    )
                )
    return tuple(hits)

