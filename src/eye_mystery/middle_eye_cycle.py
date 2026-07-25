"""Audit positive middle-eye equality classes as a direction cycle."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations

from eye_mystery.factoradic_headers import header_ranks
from eye_mystery.phase_marker_closure import late_signatures, phase_closure_metrics
from eye_mystery.terminal_source_return import (
    LOOP_PANEL,
    SOURCE_MATE,
    class_labels,
    directed_difference,
)


DIRECTIONS = (1, 2, 3, 4)
CLOCKWISE_FROM_UP = (1, 2, 3, 4)
COUNTERCLOCKWISE_FROM_UP = (1, 4, 3, 2)
AXIS_MULTIPLIERS = (25, 5, 1)


@dataclass(frozen=True)
class DirectionRepeat:
    direction: int
    class_id: int
    first_position: int | None
    repeat_position: int | None
    distance: int | None


def class_positions(
    signature: tuple[int, ...],
    class_id: int,
) -> tuple[int, ...]:
    return tuple(
        position
        for position, value in enumerate(signature)
        if value == class_id
    )


def direction_repeats(
    signature: tuple[int, ...],
    multiplier: int,
) -> tuple[DirectionRepeat, ...]:
    records = []
    for direction in DIRECTIONS:
        class_id = multiplier * direction
        positions = class_positions(signature, class_id)
        first = positions[0] if positions else None
        repeat = positions[1] if len(positions) > 1 else None
        records.append(
            DirectionRepeat(
                direction=direction,
                class_id=class_id,
                first_position=first,
                repeat_position=repeat,
                distance=repeat - first
                if first is not None and repeat is not None
                else None,
            )
        )
    return tuple(records)


@dataclass(frozen=True)
class AxisAudit:
    digit_axis: int
    multiplier: int
    records: tuple[DirectionRepeat, ...]
    present: int
    repeated: int
    repeat_order: tuple[int, ...]

    @property
    def complete(self) -> bool:
        return self.repeated == 4


def axis_audits() -> tuple[AxisAudit, ...]:
    boundary = max(
        length
        for _pair, length in phase_closure_metrics().late_pair_lcps
    )
    signature = late_signatures()[LOOP_PANEL][: boundary + 1]
    audits = []
    for axis, multiplier in enumerate(AXIS_MULTIPLIERS):
        records = direction_repeats(signature, multiplier)
        repeated_records = sorted(
            (
                record
                for record in records
                if record.repeat_position is not None
            ),
            key=lambda record: int(record.repeat_position),
        )
        audits.append(
            AxisAudit(
                digit_axis=axis,
                multiplier=multiplier,
                records=records,
                present=sum(
                    record.first_position is not None
                    for record in records
                ),
                repeated=len(repeated_records),
                repeat_order=tuple(
                    record.direction for record in repeated_records
                ),
            )
        )
    return tuple(audits)


def middle_axis_audit() -> AxisAudit:
    audits = axis_audits()
    matches = tuple(audit for audit in audits if audit.multiplier == 5)
    if len(matches) != 1:
        raise AssertionError("middle axis is not unique")
    return matches[0]


@dataclass(frozen=True)
class OrderAudit:
    permutations: int
    exact_counterclockwise_from_up: int
    either_orientation_from_up: int
    any_rotated_physical_cycle: int
    observed_order: tuple[int, ...]


def rotated(sequence: tuple[int, ...]) -> frozenset[tuple[int, ...]]:
    return frozenset(
        sequence[index:] + sequence[:index]
        for index in range(len(sequence))
    )


def audit_order() -> OrderAudit:
    orders = tuple(permutations(DIRECTIONS))
    physical = rotated(CLOCKWISE_FROM_UP) | rotated(COUNTERCLOCKWISE_FROM_UP)
    observed = middle_axis_audit().repeat_order
    return OrderAudit(
        permutations=len(orders),
        exact_counterclockwise_from_up=sum(
            order == COUNTERCLOCKWISE_FROM_UP for order in orders
        ),
        either_orientation_from_up=sum(
            order in {CLOCKWISE_FROM_UP, COUNTERCLOCKWISE_FROM_UP}
            for order in orders
        ),
        any_rotated_physical_cycle=sum(
            order in physical for order in orders
        ),
        observed_order=observed,
    )


@dataclass(frozen=True)
class BoundaryAudit:
    boundary: int
    loop_class: int
    mate_class: int
    first_conflict: bool
    loop_positions: tuple[int, ...]
    loop_value: int
    mate_class_value: int
    loop_to_mate_difference: int
    mate_to_loop_difference: int
    loop_to_mate_markers: tuple[str, ...]
    mate_to_loop_markers: tuple[str, ...]


def boundary_audit() -> BoundaryAudit:
    signatures = late_signatures()
    boundary = max(
        length
        for _pair, length in phase_closure_metrics().late_pair_lcps
    )
    loop_class = signatures[LOOP_PANEL][boundary]
    mate_class = signatures[SOURCE_MATE][boundary]
    labels = {
        panel: class_labels(panel)
        for panel in (LOOP_PANEL, SOURCE_MATE)
    }
    loop_value = labels[LOOP_PANEL][loop_class]
    mate_class_value = labels[SOURCE_MATE][loop_class]
    forward = directed_difference(loop_value, mate_class_value)
    reverse = directed_difference(mate_class_value, loop_value)
    ranks = header_ranks()
    marker_lookup = {
        value: tuple(name for name, rank in ranks.items() if rank == value)
        for value in set(ranks.values())
    }
    return BoundaryAudit(
        boundary=boundary,
        loop_class=loop_class,
        mate_class=mate_class,
        first_conflict=(
            signatures[LOOP_PANEL][:boundary]
            == signatures[SOURCE_MATE][:boundary]
            and loop_class != mate_class
        ),
        loop_positions=class_positions(signatures[LOOP_PANEL], loop_class),
        loop_value=loop_value,
        mate_class_value=mate_class_value,
        loop_to_mate_difference=forward,
        mate_to_loop_difference=reverse,
        loop_to_mate_markers=marker_lookup.get(forward, ()),
        mate_to_loop_markers=marker_lookup.get(reverse, ()),
    )
