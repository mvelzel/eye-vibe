"""Audit Veska ``1,5,3`` and ``+3`` as an Eye state selector."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import permutations, product

from eye_mystery.gate_locale import (
    decimal_component_number,
    eye_increment_text,
)
from eye_mystery.gate_plus3_transfer import MODULUS
from eye_mystery.phase_ledger import phase_suffix_lengths
from eye_mystery.phase_marker_closure import phase_closure_metrics
from eye_mystery.terminal_repeat_record import repeat_events, terminal_event
from eye_mystery.terminal_source_return import terminal_source_observation


VESKA_COMPONENTS = (1, 5, 3)
VESKA_INCREMENT = 3


@dataclass(frozen=True)
class SelectorParse:
    components: tuple[int, ...]
    split: int
    class_id: int
    suffix_width: int


def component_string(components: tuple[int, ...]) -> str:
    if not components or any(value not in range(10) for value in components):
        raise ValueError("components must be decimal digits")
    return "".join(map(str, components))


def valid_splits(
    components: tuple[int, ...],
    classes: tuple[int, ...],
    suffix_widths: tuple[int, ...],
) -> tuple[SelectorParse, ...]:
    text = component_string(components)
    class_set = set(classes)
    width_set = set(suffix_widths)
    results = []
    for split in range(1, len(text)):
        left = int(text[:split])
        right = int(text[split:])
        if left in class_set and right in width_set:
            results.append(
                SelectorParse(
                    components=components,
                    split=split,
                    class_id=left,
                    suffix_width=right,
                )
            )
    return tuple(results)


def repeated_classes() -> tuple[int, ...]:
    return tuple(event.class_id for event in repeat_events())


def distinct_suffix_widths() -> tuple[int, ...]:
    return tuple(sorted(set(phase_suffix_lengths())))


def repeated_cross_hits() -> tuple[tuple[int, int], ...]:
    target = decimal_component_number(VESKA_COMPONENTS)
    return tuple(
        (class_id, width)
        for class_id, width in product(
            repeated_classes(),
            distinct_suffix_widths(),
        )
        if int(f"{class_id}{width}") == target
    )


def all_class_cross_hits() -> tuple[tuple[int, int], ...]:
    target = decimal_component_number(VESKA_COMPONENTS)
    return tuple(
        (class_id, width)
        for class_id, width in product(
            range(25),
            distinct_suffix_widths(),
        )
        if int(f"{class_id}{width}") == target
    )


def permuted_valid_splits() -> tuple[SelectorParse, ...]:
    classes = tuple(range(25))
    widths = distinct_suffix_widths()
    return tuple(
        parse
        for ordering in sorted(set(permutations(VESKA_COMPONENTS)))
        for parse in valid_splits(ordering, classes, widths)
    )


@dataclass(frozen=True)
class VeskaSelectorAudit:
    components: tuple[int, ...]
    number: int
    increment: int
    fixed_repeated_splits: tuple[SelectorParse, ...]
    fixed_all_class_splits: tuple[SelectorParse, ...]
    repeated_cross_hits: tuple[tuple[int, int], ...]
    repeated_cross_probability: Fraction
    all_class_cross_hits: tuple[tuple[int, int], ...]
    permuted_splits: tuple[SelectorParse, ...]
    panel_suffix_matches: tuple[str, ...]
    terminal_class: int
    loop_suffix: int
    returned_header: int
    restarted_phase: int
    late_phase_length: int
    locale_text: str

    @property
    def selector_executes(self) -> bool:
        return (
            self.fixed_repeated_splits
            == (SelectorParse(self.components, 2, self.terminal_class, self.loop_suffix),)
            and self.restarted_phase == self.late_phase_length
        )


def audit_veska_selector() -> VeskaSelectorAudit:
    repeated = repeated_classes()
    widths = distinct_suffix_widths()
    suffixes = phase_suffix_lengths()
    panels = ("east4", "west4", "east5")
    terminal = terminal_event().class_id
    loop_suffix = suffixes[0]
    returned = terminal_source_observation().difference
    restarted = (returned + VESKA_INCREMENT) % MODULUS
    return VeskaSelectorAudit(
        components=VESKA_COMPONENTS,
        number=decimal_component_number(VESKA_COMPONENTS),
        increment=VESKA_INCREMENT,
        fixed_repeated_splits=valid_splits(
            VESKA_COMPONENTS,
            repeated,
            widths,
        ),
        fixed_all_class_splits=valid_splits(
            VESKA_COMPONENTS,
            tuple(range(25)),
            widths,
        ),
        repeated_cross_hits=repeated_cross_hits(),
        repeated_cross_probability=Fraction(
            len(repeated_cross_hits()),
            len(repeated) * len(widths),
        ),
        all_class_cross_hits=all_class_cross_hits(),
        permuted_splits=permuted_valid_splits(),
        panel_suffix_matches=tuple(
            panel
            for panel, suffix in zip(panels, suffixes, strict=True)
            if suffix == VESKA_COMPONENTS[-1]
        ),
        terminal_class=terminal,
        loop_suffix=loop_suffix,
        returned_header=returned,
        restarted_phase=restarted,
        late_phase_length=phase_closure_metrics().late_common_length,
        locale_text=eye_increment_text(
            decimal_component_number(VESKA_COMPONENTS),
            VESKA_INCREMENT,
        ),
    )
