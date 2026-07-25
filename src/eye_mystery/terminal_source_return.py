"""Audit the terminal source-pair body state returning to header 27."""

from __future__ import annotations

from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass
from fractions import Fraction
from itertools import permutations, product

from eye_mystery.factoradic_headers import header_ranks
from eye_mystery.gap_anchor import FINAL_MESSAGES
from eye_mystery.gate_plus3_transfer import (
    MODULUS,
    admissible_assignment_ranks,
)
from eye_mystery.ninth_causal import equality_signature
from eye_mystery.phase_overlap import phase_sequences
from eye_mystery.terminal_repeat_record import (
    repeat_events,
    terminal_event,
    terminal_record_matches,
)
from eye_mystery.phase_marker_closure import topology_closes


LOOP_PANEL = "east4"
SOURCE_MATE = "west4"
TARGET_CLASS = 15


def class_labels(message: str) -> dict[int, int]:
    _old, late = phase_sequences()[message]
    signature = equality_signature(late)
    labels: dict[int, int] = {}
    for class_id, label in zip(signature, late, strict=True):
        previous = labels.setdefault(class_id, label)
        if previous != label:
            raise AssertionError("equality class has inconsistent labels")
    return labels


def class_multiplicities(message: str) -> Counter[int]:
    _old, late = phase_sequences()[message]
    return Counter(equality_signature(late))


def reused_classes(message: str) -> frozenset[int]:
    old, _late = phase_sequences()[message]
    old_labels = set(old)
    return frozenset(
        class_id
        for class_id, label in class_labels(message).items()
        if label in old_labels
    )


def compatible_classes(
    message: str,
    target_class: int = TARGET_CLASS,
) -> tuple[int, ...]:
    multiplicities = class_multiplicities(message)
    reused = reused_classes(message)
    target_type = (
        multiplicities[target_class],
        target_class in reused,
    )
    return tuple(
        class_id
        for class_id in sorted(multiplicities)
        if (
            multiplicities[class_id],
            class_id in reused,
        )
        == target_type
    )


def directed_difference(
    from_value: int,
    to_value: int,
) -> int:
    return (to_value - from_value) % MODULUS


@dataclass(frozen=True)
class TerminalSourceObservation:
    class_id: int
    labels: tuple[tuple[str, int], ...]
    from_panel: str
    to_panel: str
    difference: int
    return_header: int

    @property
    def closes(self) -> bool:
        return self.difference == self.return_header


def terminal_source_observation() -> TerminalSourceObservation:
    event = terminal_event()
    if event.class_id != TARGET_CLASS:
        raise AssertionError("terminal pointer no longer selects class 15")
    labels = tuple(
        (message, class_labels(message)[event.class_id])
        for message in FINAL_MESSAGES
    )
    lookup = dict(labels)
    return TerminalSourceObservation(
        class_id=event.class_id,
        labels=labels,
        from_panel=LOOP_PANEL,
        to_panel=SOURCE_MATE,
        difference=directed_difference(
            lookup[LOOP_PANEL],
            lookup[SOURCE_MATE],
        ),
        return_header=header_ranks()[LOOP_PANEL],
    )


@dataclass(frozen=True)
class CompatibleReturnAudit:
    east_classes: tuple[int, ...]
    west_classes: tuple[int, ...]
    tested_pairs: int
    target_hits: tuple[tuple[int, int, int, int], ...]
    exact_probability: Fraction


def audit_compatible_returns() -> CompatibleReturnAudit:
    east_classes = compatible_classes(LOOP_PANEL)
    west_classes = compatible_classes(SOURCE_MATE)
    east_labels = class_labels(LOOP_PANEL)
    west_labels = class_labels(SOURCE_MATE)
    target = header_ranks()[LOOP_PANEL]
    hits = tuple(
        (
            east_class,
            west_class,
            east_labels[east_class],
            west_labels[west_class],
        )
        for east_class, west_class in product(east_classes, west_classes)
        if directed_difference(
            east_labels[east_class],
            west_labels[west_class],
        )
        == target
    )
    tested = len(east_classes) * len(west_classes)
    return CompatibleReturnAudit(
        east_classes=east_classes,
        west_classes=west_classes,
        tested_pairs=tested,
        target_hits=hits,
        exact_probability=Fraction(len(hits), tested),
    )


@dataclass(frozen=True)
class DifferenceHit:
    class_id: int
    from_panel: str
    to_panel: str
    from_value: int
    to_value: int
    difference: int
    markers: tuple[str, ...]


def difference_hits(
    classes: Sequence[int],
    panel_orders: Sequence[tuple[str, str]],
    *,
    marker_target: int | None = None,
) -> tuple[DifferenceHit, ...]:
    ranks = header_ranks()
    marker_lookup = {
        value: tuple(name for name, rank in ranks.items() if rank == value)
        for value in set(ranks.values())
    }
    labels = {
        message: class_labels(message)
        for message in FINAL_MESSAGES
    }
    hits = []
    for class_id in classes:
        for from_panel, to_panel in panel_orders:
            difference = directed_difference(
                labels[from_panel][class_id],
                labels[to_panel][class_id],
            )
            markers = marker_lookup.get(difference, ())
            if marker_target is not None:
                if difference != marker_target:
                    continue
            elif not markers:
                continue
            hits.append(
                DifferenceHit(
                    class_id=class_id,
                    from_panel=from_panel,
                    to_panel=to_panel,
                    from_value=labels[from_panel][class_id],
                    to_value=labels[to_panel][class_id],
                    difference=difference,
                    markers=markers,
                )
            )
    return tuple(hits)


def repeated_class_ids() -> tuple[int, ...]:
    return tuple(event.class_id for event in repeat_events())


def fixed_source_repeat_hits() -> tuple[DifferenceHit, ...]:
    return difference_hits(
        repeated_class_ids(),
        ((LOOP_PANEL, SOURCE_MATE),),
        marker_target=header_ranks()[LOOP_PANEL],
    )


def source_any_marker_hits() -> tuple[DifferenceHit, ...]:
    return difference_hits(
        repeated_class_ids(),
        (
            (LOOP_PANEL, SOURCE_MATE),
            (SOURCE_MATE, LOOP_PANEL),
        ),
    )


def all_pair_marker_hits() -> tuple[DifferenceHit, ...]:
    return difference_hits(
        repeated_class_ids(),
        tuple(permutations(FINAL_MESSAGES, 2)),
    )


def compatible_aligned_marker_hits() -> tuple[DifferenceHit, ...]:
    classes = tuple(
        sorted(
            set(compatible_classes(LOOP_PANEL))
            & set(compatible_classes(SOURCE_MATE))
        )
    )
    return difference_hits(
        classes,
        (
            (LOOP_PANEL, SOURCE_MATE),
            (SOURCE_MATE, LOOP_PANEL),
        ),
    )


@dataclass(frozen=True)
class ReturnConditionalAudit:
    assignments: int
    return_header: int
    return_and_topology: int
    return_terminal_topology: int


def audit_conditional() -> ReturnConditionalAudit:
    returned = terminal_source_observation().difference
    counts = {
        "header": 0,
        "topology": 0,
        "terminal": 0,
    }
    assignments = admissible_assignment_ranks()
    for ranks in assignments:
        header = ranks[LOOP_PANEL] == returned
        counts["header"] += header
        counts["topology"] += header and topology_closes(ranks)
        counts["terminal"] += (
            header
            and topology_closes(ranks)
            and terminal_record_matches(ranks)
        )
    return ReturnConditionalAudit(
        assignments=len(assignments),
        return_header=counts["header"],
        return_and_topology=counts["topology"],
        return_terminal_topology=counts["terminal"],
    )
