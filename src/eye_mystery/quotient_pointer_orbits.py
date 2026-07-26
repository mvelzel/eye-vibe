"""Quotient-seeded functional tables in the nine Eye messages.

Every accepted Eye value lies in ``0..82``.  The first 83 values of a panel
can therefore be read, without another key, as a complete addressable table
``f: Z_83 -> Z_83``.  This module follows the Euclidean quotient of the
panel's mod-101 checksum through that table and audits the resulting orbit
structure under a prefix- and occurrence-preserving null.
"""

from __future__ import annotations

from dataclasses import dataclass
from random import Random
from typing import Callable, Sequence

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values


TABLE_SIZE = 83
CHECKSUM_MODULUS = 101
CHECKSUM_FAMILY = ("east1", "east3", "east5")

# Full-array lengths: marker at zero plus every independently established
# literal body prefix.  Freezing the longest known prefix per panel preserves
# all four copied-prefix families.
LOCKED_PREFIX_LENGTHS = {
    "east1": 25,
    "west1": 25,
    "east2": 25,
    "west2": 6,
    "east3": 10,
    "west3": 6,
    "east4": 21,
    "west4": 21,
    "east5": 21,
}


@dataclass(frozen=True)
class FunctionalOrbit:
    """One forward orbit, split at its first repeated state."""

    path: tuple[int, ...]
    tail: tuple[int, ...]
    cycle: tuple[int, ...]
    repeated_state: int

    @property
    def size(self) -> int:
        return len(self.path)

    @property
    def mask(self) -> int:
        result = 0
        for value in self.path:
            result |= 1 << value
        return result


@dataclass(frozen=True)
class PanelOrbit:
    name: str
    quotient: int
    remainder: int
    orbit: FunctionalOrbit


@dataclass(frozen=True)
class OrbitSignature:
    panels: tuple[PanelOrbit, ...]
    all_orbit_total: int
    all_union_size: int
    closing_tail_total: int
    closing_cycle_total: int
    closing_orbit_total: int
    closing_union_size: int
    closing_cycle_lengths: tuple[int, ...]
    pure_nonclosing_orbit_sizes: tuple[int, ...]
    other_nonclosing_orbit_total: int
    closing_intersection_sizes: tuple[int, int, int]

    @property
    def pure_nonclosing_orbit_total(self) -> int:
        return sum(self.pure_nonclosing_orbit_sizes)

    @property
    def gate_component_totals(self) -> tuple[int, int, int, int]:
        """Pointer categories in dossier order: outer, crack, upper, lower."""

        return (
            self.closing_cycle_total,
            self.other_nonclosing_orbit_total,
            self.pure_nonclosing_orbit_total,
            self.closing_tail_total,
        )

    @property
    def omitted_label_count(self) -> int:
        return TABLE_SIZE - self.all_union_size

    @property
    def typed_sieve_remainder_event(self) -> bool:
        """The sieve complement equals the established E4 pivot remainder."""

        east4 = next(panel for panel in self.panels if panel.name == "east4")
        return self.omitted_label_count == east4.remainder

    @property
    def any_checksum_remainder_event(self) -> bool:
        remainders = {
            panel.remainder for panel in self.panels if panel.remainder
        }
        return self.omitted_label_count in remainders

    @property
    def objective_gate_event(self) -> bool:
        """Match the independently objective Veska counts 72, 8, and 9."""

        return (
            self.all_orbit_total == 72
            and self.closing_tail_total == 8
            and self.pure_nonclosing_orbit_total == 9
        )

    @property
    def broad_objective_gate_event(self) -> bool:
        """Allow the objective 8/9 bands to occupy any pointer categories."""

        categories = self.gate_component_totals
        return (
            self.all_orbit_total == 72
            and 8 in categories
            and 9 in categories
        )

    @property
    def predicted_full_partition_event(self) -> bool:
        """Also recover the dossier's unproved 12/43 split."""

        return (
            self.all_orbit_total == 72
            and self.gate_component_totals == (12, 43, 9, 8)
        )

    @property
    def broad_full_partition_event(self) -> bool:
        return (
            self.all_orbit_total == 72
            and sorted(self.gate_component_totals) == [8, 9, 12, 43]
        )

    @property
    def phase_event(self) -> bool:
        """Recover the independently established ``17+3=20`` phase split."""

        return (
            self.closing_orbit_total == 20
            and self.closing_union_size == 17
        )

    @property
    def ordered_cycle_event(self) -> bool:
        return self.closing_cycle_lengths == (1, 4, 7)

    @property
    def ordered_plus_three_cycle_event(self) -> bool:
        left, middle, right = self.closing_cycle_lengths
        return middle - left == 3 and right - middle == 3

    @property
    def header_overlap_event(self) -> bool:
        """Match the checksum-edge composability mask.

        In checksum-family order the established edges are ``0->1, 2->1,
        1->0``.  Only the first/third and second/third pairs compose.
        """

        return tuple(value > 0 for value in self.closing_intersection_sizes) == (
            False,
            True,
            True,
        )


@dataclass(frozen=True)
class PointerNullAudit:
    trials: int
    seed: int
    total_72_hits: int
    objective_gate_hits: int
    broad_objective_gate_hits: int
    predicted_full_partition_hits: int
    broad_full_partition_hits: int
    phase_hits: int
    ordered_cycle_hits: int
    ordered_plus_three_cycle_hits: int
    header_overlap_hits: int
    typed_sieve_remainder_hits: int
    any_checksum_remainder_hits: int
    total_72_and_typed_sieve_hits: int
    phase_and_objective_hits: int
    phase_and_broad_objective_hits: int
    full_bridge_hits: int
    broad_full_bridge_hits: int

    def corrected_rate(self, hits: int) -> float:
        return (hits + 1) / (self.trials + 1)


def functional_orbit(
    table: Sequence[int],
    seed: int,
) -> FunctionalOrbit:
    """Follow ``table[state]`` until a state repeats."""

    if not table:
        raise ValueError("table must be nonempty")
    if any(value not in range(len(table)) for value in table):
        raise ValueError("every table value must be a valid address")
    if seed not in range(len(table)):
        raise ValueError("seed must be a valid address")

    seen: dict[int, int] = {}
    path = []
    state = seed
    while state not in seen:
        seen[state] = len(path)
        path.append(state)
        state = table[state]
    split = seen[state]
    return FunctionalOrbit(
        path=tuple(path),
        tail=tuple(path[:split]),
        cycle=tuple(path[split:]),
        repeated_state=state,
    )


def panel_values(name: str) -> tuple[int, ...]:
    return trigram_values(MESSAGES[name])


def panel_orbit(
    name: str,
    table: Sequence[int] | None = None,
) -> PanelOrbit:
    values = panel_values(name)
    quotient, remainder = divmod(sum(values), CHECKSUM_MODULUS)
    selected = values[:TABLE_SIZE] if table is None else tuple(table)
    if len(selected) != TABLE_SIZE:
        raise ValueError("Eye pointer tables must contain exactly 83 values")
    return PanelOrbit(
        name=name,
        quotient=quotient,
        remainder=remainder,
        orbit=functional_orbit(selected, quotient),
    )


def signature(
    panels: Sequence[PanelOrbit],
) -> OrbitSignature:
    by_name = {panel.name: panel for panel in panels}
    if tuple(by_name) != MESSAGE_ORDER:
        raise ValueError("panels must be supplied in canonical message order")

    closing = tuple(by_name[name] for name in CHECKSUM_FAMILY)
    nonclosing = tuple(
        by_name[name] for name in MESSAGE_ORDER if name not in CHECKSUM_FAMILY
    )
    if any(panel.remainder for panel in closing):
        raise ValueError("checksum family no longer closes modulo 101")
    if any(not panel.remainder for panel in nonclosing):
        raise ValueError("a non-checksum panel unexpectedly closes modulo 101")

    closing_union_mask = 0
    for panel in closing:
        closing_union_mask |= panel.orbit.mask
    all_union_mask = 0
    for panel in panels:
        all_union_mask |= panel.orbit.mask

    pairs = ((0, 1), (0, 2), (1, 2))
    intersections = tuple(
        (closing[left].orbit.mask & closing[right].orbit.mask).bit_count()
        for left, right in pairs
    )
    pure_nonclosing = tuple(
        panel.orbit.size
        for panel in nonclosing
        if not panel.orbit.tail
    )
    other_nonclosing_total = sum(
        panel.orbit.size
        for panel in nonclosing
        if panel.orbit.tail
    )
    return OrbitSignature(
        panels=tuple(panels),
        all_orbit_total=sum(panel.orbit.size for panel in panels),
        all_union_size=all_union_mask.bit_count(),
        closing_tail_total=sum(len(panel.orbit.tail) for panel in closing),
        closing_cycle_total=sum(len(panel.orbit.cycle) for panel in closing),
        closing_orbit_total=sum(panel.orbit.size for panel in closing),
        closing_union_size=closing_union_mask.bit_count(),
        closing_cycle_lengths=tuple(
            len(panel.orbit.cycle) for panel in closing
        ),
        pure_nonclosing_orbit_sizes=pure_nonclosing,
        other_nonclosing_orbit_total=other_nonclosing_total,
        closing_intersection_sizes=intersections,
    )


def canonical_signature() -> OrbitSignature:
    return signature(tuple(panel_orbit(name) for name in MESSAGE_ORDER))


def common_window_signatures() -> tuple[tuple[int, OrbitSignature], ...]:
    """Evaluate every 83-cell start available in all nine panels."""

    values = {name: panel_values(name) for name in MESSAGE_ORDER}
    common_starts = min(len(stream) for stream in values.values()) - TABLE_SIZE + 1
    return tuple(
        (
            start,
            signature(
                tuple(
                    panel_orbit(
                        name,
                        values[name][start : start + TABLE_SIZE],
                    )
                    for name in MESSAGE_ORDER
                )
            ),
        )
        for start in range(common_starts)
    )


@dataclass(frozen=True)
class ConditionedTableSpec:
    name: str
    base: tuple[int, ...]
    continuation: int
    fixed_positions: frozenset[int]
    free_positions: tuple[int, ...]
    free_values: tuple[int, ...]


def conditioned_table_spec(name: str) -> ConditionedTableSpec:
    values = panel_values(name)
    table = tuple(values[:TABLE_SIZE])
    quotient, _remainder = divmod(sum(values), CHECKSUM_MODULUS)
    fixed = frozenset(
        set(range(LOCKED_PREFIX_LENGTHS[name]))
        | {index for index, value in enumerate(table) if value == quotient}
    )
    free = tuple(index for index in range(TABLE_SIZE) if index not in fixed)
    return ConditionedTableSpec(
        name=name,
        base=table,
        continuation=values[TABLE_SIZE],
        fixed_positions=fixed,
        free_positions=free,
        free_values=tuple(table[index] for index in free),
    )


def sample_conditioned_table(
    spec: ConditionedTableSpec,
    random: Random,
) -> tuple[int, ...]:
    """Uniformly shuffle free cells, rejecting adjacent repeated values."""

    while True:
        shuffled = list(spec.free_values)
        random.shuffle(shuffled)
        candidate = list(spec.base)
        for position, value in zip(
            spec.free_positions,
            shuffled,
            strict=True,
        ):
            candidate[position] = value
        if any(
            candidate[index] == candidate[index + 1]
            for index in range(TABLE_SIZE - 1)
        ):
            continue
        if candidate[-1] == spec.continuation:
            continue
        return tuple(candidate)


def matched_pointer_null(
    trials: int,
    *,
    seed: int = 0x5645534B41,
    progress: Callable[[int], None] | None = None,
) -> PointerNullAudit:
    """Run the exact-condition Monte Carlo used for the pointer bridge.

    Each panel independently preserves:

    - its complete first-83 multiset and checksum;
    - its marker and longest established copied prefix;
    - every in-table occurrence of its already selected quotient;
    - the absence of adjacent repeated values, including the table boundary.
    """

    if trials < 1:
        raise ValueError("trials must be positive")
    random = Random(seed)
    specs = tuple(conditioned_table_spec(name) for name in MESSAGE_ORDER)
    counts = {
        "total_72": 0,
        "objective": 0,
        "broad_objective": 0,
        "partition": 0,
        "broad_partition": 0,
        "phase": 0,
        "cycles": 0,
        "plus_three": 0,
        "overlap": 0,
        "sieve": 0,
        "any_remainder": 0,
        "total_sieve": 0,
        "phase_objective": 0,
        "phase_broad_objective": 0,
        "full": 0,
        "broad_full": 0,
    }

    for trial in range(1, trials + 1):
        panels = tuple(
            panel_orbit(
                spec.name,
                sample_conditioned_table(spec, random),
            )
            for spec in specs
        )
        item = signature(panels)
        objective = item.objective_gate_event
        broad_objective = item.broad_objective_gate_event
        phase = item.phase_event
        cycles = item.ordered_cycle_event
        counts["total_72"] += item.all_orbit_total == 72
        counts["objective"] += objective
        counts["broad_objective"] += broad_objective
        counts["partition"] += item.predicted_full_partition_event
        counts["broad_partition"] += item.broad_full_partition_event
        counts["phase"] += phase
        counts["cycles"] += cycles
        counts["plus_three"] += item.ordered_plus_three_cycle_event
        counts["overlap"] += item.header_overlap_event
        counts["sieve"] += item.typed_sieve_remainder_event
        counts["any_remainder"] += item.any_checksum_remainder_event
        counts["total_sieve"] += (
            item.all_orbit_total == 72
            and item.typed_sieve_remainder_event
        )
        counts["phase_objective"] += phase and objective
        counts["phase_broad_objective"] += phase and broad_objective
        counts["full"] += phase and objective and cycles
        counts["broad_full"] += phase and broad_objective and cycles
        if progress is not None and trial % 100_000 == 0:
            progress(trial)

    return PointerNullAudit(
        trials=trials,
        seed=seed,
        total_72_hits=counts["total_72"],
        objective_gate_hits=counts["objective"],
        broad_objective_gate_hits=counts["broad_objective"],
        predicted_full_partition_hits=counts["partition"],
        broad_full_partition_hits=counts["broad_partition"],
        phase_hits=counts["phase"],
        ordered_cycle_hits=counts["cycles"],
        ordered_plus_three_cycle_hits=counts["plus_three"],
        header_overlap_hits=counts["overlap"],
        typed_sieve_remainder_hits=counts["sieve"],
        any_checksum_remainder_hits=counts["any_remainder"],
        total_72_and_typed_sieve_hits=counts["total_sieve"],
        phase_and_objective_hits=counts["phase_objective"],
        phase_and_broad_objective_hits=counts["phase_broad_objective"],
        full_bridge_hits=counts["full"],
        broad_full_bridge_hits=counts["broad_full"],
    )
