"""Audit the Gate ``+3`` closure through measured final-phase lengths."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from functools import cache
from itertools import combinations, permutations

from eye_mystery.factoradic_headers import (
    graph_conditioned_audit,
    header_ranks,
)
from eye_mystery.gap_anchor import FINAL_MESSAGES
from eye_mystery.gate_plus3_transfer import (
    MODULUS,
    ROWS,
    SHIFT,
    admissible_assignment_ranks,
    assignment_ranks,
    control_edge,
)
from eye_mystery.ninth_causal import equality_signature
from eye_mystery.phase_ledger import phase_suffix_lengths
from eye_mystery.synchronizing_bridge import (
    bridge_specs,
    canonical_streams,
    common_prefix_length,
    observed_metrics,
)


FINAL_ROW = ROWS[2]
FIRST_ROW = ROWS[0]
SELF_INDEX = 0


@dataclass(frozen=True)
class PhaseClosureMetrics:
    bridge_lengths: tuple[int, int, int]
    old_common_length: int
    old_pair_lcps: tuple[tuple[tuple[str, str], int], ...]
    late_common_length: int
    late_pair_lcps: tuple[tuple[tuple[str, str], int], ...]


@cache
def late_signatures() -> dict[str, tuple[int, ...]]:
    streams = canonical_streams()
    specs = bridge_specs()
    return {
        name: equality_signature(
            streams[name][specs[name].late_entry_full :]
        )
        for name in FINAL_MESSAGES
    }


@cache
def phase_closure_metrics() -> PhaseClosureMetrics:
    streams = canonical_streams()
    specs = bridge_specs()
    old_signatures = {
        name: equality_signature(
            streams[name][
                specs[name].endpoint_full : specs[name].late_entry_full
            ]
        )
        for name in FINAL_MESSAGES
    }
    late = late_signatures()
    return PhaseClosureMetrics(
        bridge_lengths=tuple(
            specs[name].length for name in FINAL_MESSAGES
        ),  # type: ignore[arg-type]
        old_common_length=observed_metrics().triple_lcp,
        old_pair_lcps=tuple(
            (
                (left, right),
                common_prefix_length(
                    (old_signatures[left], old_signatures[right])
                ),
            )
            for left, right in combinations(FINAL_MESSAGES, 2)
        ),
        late_common_length=common_prefix_length(tuple(late.values())),
        late_pair_lcps=tuple(
            (
                (left, right),
                common_prefix_length(
                    (late[left], late[right])
                ),
            )
            for left, right in combinations(FINAL_MESSAGES, 2)
        ),
    )


def row_vector(
    ranks: Mapping[str, int],
    row: Sequence[str],
) -> tuple[int, int, int]:
    if len(row) != 3:
        raise ValueError("marker rows must contain three fields")
    return tuple(ranks[name] for name in row)  # type: ignore[return-value]


def shifted_vector(
    ranks: Mapping[str, int],
    row: Sequence[str],
    *,
    shift: int = SHIFT,
) -> tuple[int, int, int]:
    return tuple(
        (value + shift) % MODULUS
        for value in row_vector(ranks, row)
    )  # type: ignore[return-value]


@dataclass(frozen=True)
class ClosureObservation:
    source: tuple[int, int, int]
    shifted: tuple[int, int, int]
    repaired: tuple[int, int, int]
    target: tuple[int, int, int]
    bridge_length: int
    late_phase_length: int

    @property
    def closes(self) -> bool:
        return self.repaired == self.target


def closure_observation(
    ranks: Mapping[str, int] | None = None,
) -> ClosureObservation:
    ranks = header_ranks() if ranks is None else ranks
    metrics = phase_closure_metrics()
    source = row_vector(ranks, FINAL_ROW)
    shifted = shifted_vector(ranks, FINAL_ROW)
    repaired_list = list(shifted)
    repaired_list[SELF_INDEX] = (
        repaired_list[SELF_INDEX]
        + metrics.bridge_lengths[SELF_INDEX]
    ) % MODULUS
    return ClosureObservation(
        source=source,
        shifted=shifted,
        repaired=tuple(repaired_list),  # type: ignore[arg-type]
        target=row_vector(ranks, FIRST_ROW),
        bridge_length=metrics.bridge_lengths[SELF_INDEX],
        late_phase_length=metrics.late_common_length,
    )


def nonself_closes(ranks: Mapping[str, int]) -> bool:
    source = shifted_vector(ranks, FINAL_ROW)
    target = row_vector(ranks, FIRST_ROW)
    return all(
        source[index] == target[index]
        for index in range(3)
        if index != SELF_INDEX
    )


def self_points_to_phase(ranks: Mapping[str, int]) -> bool:
    return (
        nonself_closes(ranks)
        and shifted_vector(ranks, FINAL_ROW)[SELF_INDEX]
        == phase_closure_metrics().late_common_length
    )


def full_closure(ranks: Mapping[str, int]) -> bool:
    observation = closure_observation(ranks)
    return self_points_to_phase(ranks) and observation.closes


def _unique_longest_pair(
    pair_lcps: Sequence[tuple[tuple[str, str], int]],
) -> tuple[tuple[str, str], int]:
    maximum = max(length for _pair, length in pair_lcps)
    winners = tuple(
        (pair, length)
        for pair, length in pair_lcps
        if length == maximum
    )
    if len(winners) != 1:
        raise AssertionError("phase does not have a unique longest pair")
    return winners[0]


@dataclass(frozen=True)
class PhaseTopologyObservation:
    edges: tuple[tuple[str, tuple[int, int]], ...]
    loop: str
    target_pair: tuple[str, str]
    source_pair: tuple[str, str]
    old_longest_pair: tuple[str, str]
    late_longest_pair: tuple[str, str]
    old_extension: int
    late_extension: int
    suffixes: tuple[int, int, int]
    scope_switch_matches: bool
    mate_extensions_match: bool
    phase_total: int
    first_self_rank: int
    source_pair_delta: int
    late_pair_boundary: int
    late_boundary_markers: tuple[str, ...]


def phase_topology_observation(
    ranks: Mapping[str, int] | None = None,
) -> PhaseTopologyObservation:
    ranks = header_ranks() if ranks is None else ranks
    metrics = phase_closure_metrics()
    edges = {
        name: control_edge(ranks[name])
        for name in FINAL_MESSAGES
    }
    loops = tuple(
        name for name, (source, target) in edges.items() if source == target
    )
    if len(loops) != 1:
        raise AssertionError("final row does not have one control-edge loop")
    loop = loops[0]
    source_pair = tuple(
        name
        for name, edge in edges.items()
        if edge[0] == edges[loop][0]
    )
    target_pair = tuple(
        name
        for name, edge in edges.items()
        if edge[1] == edges[loop][1]
    )
    if len(source_pair) != 2 or len(target_pair) != 2:
        raise AssertionError("loop does not have one source and target mate")
    old_pair, old_length = _unique_longest_pair(metrics.old_pair_lcps)
    late_pair, late_length = _unique_longest_pair(metrics.late_pair_lcps)
    suffixes = phase_suffix_lengths()
    suffix_by_name = dict(zip(FINAL_MESSAGES, suffixes, strict=True))
    target_mate = next(name for name in target_pair if name != loop)
    source_mate = next(name for name in source_pair if name != loop)
    old_extension = old_length - metrics.old_common_length
    late_extension = late_length - metrics.late_common_length
    phase_total = old_length + metrics.late_common_length
    marker_lookup = {
        rank: tuple(name for name, value in ranks.items() if value == rank)
        for rank in set(ranks.values())
    }
    return PhaseTopologyObservation(
        edges=tuple((name, edges[name]) for name in FINAL_MESSAGES),
        loop=loop,
        target_pair=target_pair,  # type: ignore[arg-type]
        source_pair=source_pair,  # type: ignore[arg-type]
        old_longest_pair=old_pair,
        late_longest_pair=late_pair,
        old_extension=old_extension,
        late_extension=late_extension,
        suffixes=suffixes,
        scope_switch_matches=(
            set(old_pair) == set(target_pair)
            and set(late_pair) == set(source_pair)
        ),
        mate_extensions_match=(
            old_extension == suffix_by_name[target_mate]
            and late_extension == suffix_by_name[source_mate]
        ),
        phase_total=phase_total,
        first_self_rank=ranks[FIRST_ROW[SELF_INDEX]],
        source_pair_delta=(ranks[source_mate] - ranks[loop]) % MODULUS,
        late_pair_boundary=late_length,
        late_boundary_markers=marker_lookup.get(late_length, ()),
    )


def source_delta_closes(ranks: Mapping[str, int]) -> bool:
    if not full_closure(ranks):
        return False
    topology = phase_topology_observation(ranks)
    return (
        topology.source_pair_delta == topology.phase_total
        and topology.first_self_rank == topology.phase_total
    )


def topology_closes(ranks: Mapping[str, int]) -> bool:
    if not source_delta_closes(ranks):
        return False
    topology = phase_topology_observation(ranks)
    return "west3" in topology.late_boundary_markers


def natural_repair(
    ranks: Mapping[str, int],
    source_row: Sequence[str],
    target_row: Sequence[str],
    *,
    self_index: int,
    bridge_length: int,
    shift: int = SHIFT,
) -> bool:
    if self_index not in range(3):
        raise ValueError("self index must lie in 0..2")
    shifted = list(shifted_vector(ranks, source_row, shift=shift))
    late = phase_closure_metrics().late_common_length
    if shifted[self_index] != late:
        return False
    shifted[self_index] = (late + bridge_length) % MODULUS
    return tuple(shifted) == row_vector(ranks, target_row)


def permuted_repair(
    ranks: Mapping[str, int],
    source_row: Sequence[str],
    target_row: Sequence[str],
    *,
    self_index: int,
    bridge_length: int,
    shift: int = SHIFT,
) -> bool:
    if self_index not in range(3):
        raise ValueError("self index must lie in 0..2")
    shifted = list(shifted_vector(ranks, source_row, shift=shift))
    late = phase_closure_metrics().late_common_length
    if shifted[self_index] != late:
        return False
    shifted[self_index] = (late + bridge_length) % MODULUS
    return row_vector(ranks, target_row) in set(permutations(shifted))


def any_repair(
    ranks: Mapping[str, int],
    *,
    permute_target: bool,
    shift: int = SHIFT,
) -> bool:
    predicate = permuted_repair if permute_target else natural_repair
    bridge_lengths = tuple(
        sorted(set(phase_closure_metrics().bridge_lengths))
    )
    for source_index, source_row in enumerate(ROWS):
        for target_index, target_row in enumerate(ROWS):
            if source_index == target_index:
                continue
            for self_index in range(3):
                for bridge_length in bridge_lengths:
                    if predicate(
                        ranks,
                        source_row,
                        target_row,
                        self_index=self_index,
                        bridge_length=bridge_length,
                        shift=shift,
                    ):
                        return True
    return False


@dataclass(frozen=True)
class ClosureConditionalAudit:
    assignments: int
    nonself: int
    self_to_phase: int
    full: int
    full_and_source_delta: int
    full_topology: int
    broad_natural: int
    broad_permuted: int
    factoradic_survivors: int
    matching_factoradic_survivors: tuple[tuple[int, ...], ...]


def audit_conditional() -> ClosureConditionalAudit:
    counts = {
        "nonself": 0,
        "self": 0,
        "full": 0,
        "delta": 0,
        "topology": 0,
        "natural": 0,
        "permuted": 0,
    }
    assignments = admissible_assignment_ranks()
    for ranks in assignments:
        counts["nonself"] += nonself_closes(ranks)
        counts["self"] += self_points_to_phase(ranks)
        counts["full"] += full_closure(ranks)
        counts["delta"] += source_delta_closes(ranks)
        counts["topology"] += topology_closes(ranks)
        counts["natural"] += any_repair(ranks, permute_target=False)
        counts["permuted"] += any_repair(ranks, permute_target=True)
    factoradic = graph_conditioned_audit()
    matching = tuple(
        assignment
        for assignment in factoradic.survivors
        if full_closure(assignment_ranks(assignment))
    )
    return ClosureConditionalAudit(
        assignments=len(assignments),
        nonself=counts["nonself"],
        self_to_phase=counts["self"],
        full=counts["full"],
        full_and_source_delta=counts["delta"],
        full_topology=counts["topology"],
        broad_natural=counts["natural"],
        broad_permuted=counts["permuted"],
        factoradic_survivors=factoradic.full,
        matching_factoradic_survivors=matching,
    )


@dataclass(frozen=True)
class RepairHit:
    shift: int
    source_row: int
    target_row: int
    self_index: int
    bridge_length: int
    permuted_target: bool


def scan_observed_repairs(
    *,
    permute_target: bool,
) -> tuple[RepairHit, ...]:
    ranks = header_ranks()
    predicate = permuted_repair if permute_target else natural_repair
    bridge_lengths = tuple(
        sorted(set(phase_closure_metrics().bridge_lengths))
    )
    hits = []
    for shift in range(1, MODULUS):
        for source_index, source_row in enumerate(ROWS):
            for target_index, target_row in enumerate(ROWS):
                if source_index == target_index:
                    continue
                for self_index in range(3):
                    for bridge_length in bridge_lengths:
                        if predicate(
                            ranks,
                            source_row,
                            target_row,
                            self_index=self_index,
                            bridge_length=bridge_length,
                            shift=shift,
                        ):
                            hits.append(
                                RepairHit(
                                    shift=shift,
                                    source_row=source_index + 1,
                                    target_row=target_index + 1,
                                    self_index=self_index,
                                    bridge_length=bridge_length,
                                    permuted_target=permute_target,
                                )
                            )
    return tuple(hits)


def pair_marker_matches(
    ranks: Mapping[str, int] | None = None,
) -> tuple[tuple[tuple[str, str], int, tuple[str, ...]], ...]:
    ranks = header_ranks() if ranks is None else ranks
    return tuple(
        (
            pair,
            length,
            tuple(name for name, rank in ranks.items() if rank == length),
        )
        for pair, length in phase_closure_metrics().late_pair_lcps
    )
