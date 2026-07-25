"""Audit marker row 2 as a terminal-repeat pointer record."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from functools import cache
from itertools import permutations, product

from eye_mystery.factoradic_headers import graph_conditioned_audit, header_ranks
from eye_mystery.gate_plus3_transfer import (
    MODULUS,
    ROWS,
    admissible_assignment_ranks,
    assignment_ranks,
)
from eye_mystery.phase_marker_closure import (
    full_closure,
    late_signatures,
    phase_closure_metrics,
    source_delta_closes,
    topology_closes,
)


ROW2 = ROWS[1]
RECORD_ORDER = ("west3", "east3", "west2")


@dataclass(frozen=True)
class RepeatEvent:
    position: int
    previous_position: int
    distance: int
    class_id: int


@cache
def common_late_signature() -> tuple[int, ...]:
    signatures = late_signatures()
    length = phase_closure_metrics().late_common_length
    prefixes = {
        signature[:length]
        for signature in signatures.values()
    }
    if len(prefixes) != 1:
        raise AssertionError("late phase does not have one equality signature")
    return next(iter(prefixes))


@cache
def repeat_events() -> tuple[RepeatEvent, ...]:
    last_seen: dict[int, int] = {}
    events = []
    for position, class_id in enumerate(common_late_signature()):
        if class_id in last_seen:
            previous = last_seen[class_id]
            events.append(
                RepeatEvent(
                    position=position,
                    previous_position=previous,
                    distance=position - previous,
                    class_id=class_id,
                )
            )
        last_seen[class_id] = position
    return tuple(events)


@cache
def terminal_event() -> RepeatEvent:
    signature = common_late_signature()
    events = {
        event.position: event
        for event in repeat_events()
    }
    terminal = events.get(len(signature) - 1)
    if terminal is None:
        raise AssertionError("late phase does not end in a repeat")
    return terminal


def record_values(
    ranks: Mapping[str, int] | None = None,
) -> tuple[int, int, int]:
    ranks = header_ranks() if ranks is None else ranks
    return tuple(ranks[name] for name in RECORD_ORDER)  # type: ignore[return-value]


def boundary_matches(ranks: Mapping[str, int]) -> bool:
    boundary = max(
        length
        for _pair, length in phase_closure_metrics().late_pair_lcps
    )
    return (
        ranks[RECORD_ORDER[0]]
        == boundary
    )


def position_matches(ranks: Mapping[str, int]) -> bool:
    event = terminal_event()
    return (
        boundary_matches(ranks)
        and (ranks[RECORD_ORDER[0]] + event.position) % MODULUS
        == ranks[RECORD_ORDER[1]]
    )


def terminal_record_matches(ranks: Mapping[str, int]) -> bool:
    event = terminal_event()
    return (
        position_matches(ranks)
        and (ranks[RECORD_ORDER[1]] + event.distance) % MODULUS
        == ranks[RECORD_ORDER[2]]
    )


def ordered_event_match(
    ranks: Mapping[str, int],
    order: Sequence[str],
    event: RepeatEvent,
    *,
    signs: tuple[int, int] = (1, 1),
) -> bool:
    if len(order) != 3 or set(signs) - {-1, 1}:
        raise ValueError("need three fields and two signs in {-1,+1}")
    base, middle, end = (ranks[name] for name in order)
    return (
        (base + signs[0] * event.position) % MODULUS == middle
        and (middle + signs[1] * event.distance) % MODULUS == end
    )


def any_event_match(
    ranks: Mapping[str, int],
    rows: Sequence[Sequence[str]],
    *,
    signed: bool,
) -> bool:
    signs = tuple(product((-1, 1), repeat=2)) if signed else ((1, 1),)
    return any(
        ordered_event_match(ranks, order, event, signs=sign_pair)
        for row in rows
        for order in permutations(row)
        for event in repeat_events()
        for sign_pair in signs
    )


@dataclass(frozen=True)
class EventHit:
    row: int
    order: tuple[str, str, str]
    event: RepeatEvent
    signs: tuple[int, int]


def observed_event_hits(*, signed: bool) -> tuple[EventHit, ...]:
    ranks = header_ranks()
    signs = tuple(product((-1, 1), repeat=2)) if signed else ((1, 1),)
    return tuple(
        EventHit(
            row=row_index + 1,
            order=order,
            event=event,
            signs=sign_pair,
        )
        for row_index, row in enumerate(ROWS)
        for order in permutations(row)
        for event in repeat_events()
        for sign_pair in signs
        if ordered_event_match(ranks, order, event, signs=sign_pair)
    )


@dataclass(frozen=True)
class TerminalRecordAudit:
    assignments: int
    boundary: int
    position: int
    record: int
    record_and_full_closure: int
    record_and_source_delta: int
    record_and_topology: int
    broad_row2: int
    broad_any_row: int
    broad_signed: int
    factoradic_survivors: int
    record_factoradic_survivors: tuple[tuple[int, ...], ...]
    record_and_closure_factoradic_survivors: tuple[tuple[int, ...], ...]


def audit_terminal_record() -> TerminalRecordAudit:
    counts = {
        "boundary": 0,
        "position": 0,
        "record": 0,
        "full": 0,
        "delta": 0,
        "topology": 0,
        "row2": 0,
        "any": 0,
        "signed": 0,
    }
    assignments = admissible_assignment_ranks()
    for ranks in assignments:
        record = terminal_record_matches(ranks)
        counts["boundary"] += boundary_matches(ranks)
        counts["position"] += position_matches(ranks)
        counts["record"] += record
        counts["full"] += record and full_closure(ranks)
        counts["delta"] += record and source_delta_closes(ranks)
        counts["topology"] += record and topology_closes(ranks)
        counts["row2"] += any_event_match(ranks, (ROW2,), signed=False)
        counts["any"] += any_event_match(ranks, ROWS, signed=False)
        counts["signed"] += any_event_match(ranks, ROWS, signed=True)
    factoradic = graph_conditioned_audit()
    record_survivors = tuple(
        assignment
        for assignment in factoradic.survivors
        if terminal_record_matches(assignment_ranks(assignment))
    )
    joint_survivors = tuple(
        assignment
        for assignment in record_survivors
        if full_closure(assignment_ranks(assignment))
    )
    return TerminalRecordAudit(
        assignments=len(assignments),
        boundary=counts["boundary"],
        position=counts["position"],
        record=counts["record"],
        record_and_full_closure=counts["full"],
        record_and_source_delta=counts["delta"],
        record_and_topology=counts["topology"],
        broad_row2=counts["row2"],
        broad_any_row=counts["any"],
        broad_signed=counts["signed"],
        factoradic_survivors=factoradic.full,
        record_factoradic_survivors=record_survivors,
        record_and_closure_factoradic_survivors=joint_survivors,
    )
