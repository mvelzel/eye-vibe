"""Low-capacity geometric screens for the late 5x5 state tables."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from itertools import permutations, product

from eye_mystery.gap_anchor import FINAL_MESSAGES
from eye_mystery.terminal_source_return import class_labels


CONTROL_CLASSES = (5, 15, 20)
HELDOUT_CLASS = 10


def coordinate_d4(row: int, column: int) -> tuple[tuple[int, int], ...]:
    return (
        (row, column),
        (column, 4 - row),
        (4 - row, 4 - column),
        (4 - column, row),
        (row, 4 - column),
        (4 - row, column),
        (column, row),
        (4 - column, 4 - row),
    )


@dataclass(frozen=True)
class CoordinateWitness:
    source: str
    target: str
    transform: int
    row_shift: int
    column_shift: int
    exact_matches: tuple[int, ...]
    modal_offset: int
    modal_classes: tuple[int, ...]


@dataclass(frozen=True)
class CoordinateScreen:
    models: int
    maximum_exact: int
    maximum_modal_offset: int
    exact_witnesses: tuple[CoordinateWitness, ...]
    offset_witnesses: tuple[CoordinateWitness, ...]


def audit_coordinates(*, translated: bool) -> CoordinateScreen:
    tables = {
        panel: class_labels(panel)
        for panel in FINAL_MESSAGES
    }
    shifts = product(range(5), repeat=2) if translated else ((0, 0),)
    shift_values = tuple(shifts)
    witnesses = []
    for source, target in permutations(FINAL_MESSAGES, 2):
        for transform in range(8):
            for row_shift, column_shift in shift_values:
                pairs = []
                for class_id in range(25):
                    row, column = divmod(class_id, 5)
                    mapped_row, mapped_column = coordinate_d4(
                        row,
                        column,
                    )[transform]
                    mapped_row = (mapped_row + row_shift) % 5
                    mapped_column = (mapped_column + column_shift) % 5
                    mapped_class = 5 * mapped_row + mapped_column
                    pairs.append(
                        (
                            class_id,
                            tables[source][class_id],
                            tables[target][mapped_class],
                        )
                    )
                exact = tuple(
                    class_id
                    for class_id, left, right in pairs
                    if left == right
                )
                offsets = Counter(
                    (right - left) % 83
                    for _class_id, left, right in pairs
                )
                modal_count = max(offsets.values())
                modal_offset = min(
                    offset
                    for offset, count in offsets.items()
                    if count == modal_count
                )
                modal_classes = tuple(
                    class_id
                    for class_id, left, right in pairs
                    if (right - left) % 83 == modal_offset
                )
                witnesses.append(
                    CoordinateWitness(
                        source=source,
                        target=target,
                        transform=transform,
                        row_shift=row_shift,
                        column_shift=column_shift,
                        exact_matches=exact,
                        modal_offset=modal_offset,
                        modal_classes=modal_classes,
                    )
                )
    maximum_exact = max(len(witness.exact_matches) for witness in witnesses)
    maximum_offset = max(len(witness.modal_classes) for witness in witnesses)
    return CoordinateScreen(
        models=len(witnesses),
        maximum_exact=maximum_exact,
        maximum_modal_offset=maximum_offset,
        exact_witnesses=tuple(
            witness
            for witness in witnesses
            if len(witness.exact_matches) == maximum_exact
        ),
        offset_witnesses=tuple(
            witness
            for witness in witnesses
            if len(witness.modal_classes) == maximum_offset
        ),
    )


def base5_digits(rank: int) -> tuple[int, int, int]:
    return rank // 25, (rank // 5) % 5, rank % 5


def from_base5(digits: tuple[int, int, int]) -> int:
    return 25 * digits[0] + 5 * digits[1] + digits[2]


def physical_d4() -> tuple[tuple[int, ...], ...]:
    values = []
    for shift in range(4):
        values.append(
            tuple(
                [0]
                + [1 + ((direction - 1 + shift) % 4) for direction in range(1, 5)]
            )
        )
    for shift in range(4):
        values.append(
            tuple(
                [0]
                + [1 + ((-(direction - 1) + shift) % 4) for direction in range(1, 5)]
            )
        )
    return tuple(dict.fromkeys(values))


@dataclass(frozen=True)
class VisibleWitness:
    source: str
    target: str
    eye_order: tuple[int, int, int]
    direction_transforms: tuple[int, int, int]
    exact_matches: tuple[int, ...]
    training_matches: tuple[int, ...]
    heldout_match: bool


@dataclass(frozen=True)
class VisibleScreen:
    models: int
    maximum_exact: int
    exact_witnesses: tuple[VisibleWitness, ...]
    maximum_training: int
    training_cobest: int
    training_cobest_heldout: int


def audit_visible(*, independent_eyes: bool) -> VisibleScreen:
    tables = {
        panel: class_labels(panel)
        for panel in FINAL_MESSAGES
    }
    transforms = physical_d4()
    transform_choices = (
        tuple(product(range(8), repeat=3))
        if independent_eyes
        else tuple((index, index, index) for index in range(8))
    )
    witnesses = []
    for source, target in permutations(FINAL_MESSAGES, 2):
        for eye_order in permutations(range(3)):
            for selected in transform_choices:
                exact = []
                for class_id in range(25):
                    digits = base5_digits(tables[source][class_id])
                    mapped = tuple(
                        transforms[selected[index]][digits[eye_order[index]]]
                        for index in range(3)
                    )
                    if from_base5(mapped) == tables[target][class_id]:
                        exact.append(class_id)
                exact_tuple = tuple(exact)
                witnesses.append(
                    VisibleWitness(
                        source=source,
                        target=target,
                        eye_order=eye_order,  # type: ignore[arg-type]
                        direction_transforms=selected,
                        exact_matches=exact_tuple,
                        training_matches=tuple(
                            class_id
                            for class_id in CONTROL_CLASSES
                            if class_id in exact_tuple
                        ),
                        heldout_match=HELDOUT_CLASS in exact_tuple,
                    )
                )
    maximum_exact = max(len(witness.exact_matches) for witness in witnesses)
    maximum_training = max(
        len(witness.training_matches) for witness in witnesses
    )
    training_cobest = tuple(
        witness
        for witness in witnesses
        if len(witness.training_matches) == maximum_training
    )
    return VisibleScreen(
        models=len(witnesses),
        maximum_exact=maximum_exact,
        exact_witnesses=tuple(
            witness
            for witness in witnesses
            if len(witness.exact_matches) == maximum_exact
        ),
        maximum_training=maximum_training,
        training_cobest=len(training_cobest),
        training_cobest_heldout=sum(
            witness.heldout_match for witness in training_cobest
        ),
    )
