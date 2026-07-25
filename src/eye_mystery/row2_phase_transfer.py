"""Prospective transfer of the phase-budget rule to the second message row."""

from __future__ import annotations

import random
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from itertools import combinations, permutations

from eye_mystery.corpus import MESSAGES, trigram_values
from eye_mystery.factoradic_headers import header_ranks
from eye_mystery.ninth_causal import (
    equality_signature,
    synchronization_profile,
)
from eye_mystery.phase_ledger import (
    ALL_SYMBOLS,
    NEWLINE_SYMBOL,
    row2_circulation,
    symbol_preimage,
)
from eye_mystery.seventeenth_state import shuffle_without_adjacent_doubles
from eye_mystery.synchronizing_bridge import common_prefix_length


ROW2_MESSAGES = ("west2", "east3", "west3")
OPENING_EXIT = 5
PRIMARY_PAIR = ("west2", "west3")
TARGET_NEW_COMMON = 7


def row2_bodies() -> dict[str, tuple[int, ...]]:
    return {
        name: tuple(trigram_values(MESSAGES[name])[1:])
        for name in ROW2_MESSAGES
    }


def phase_budget(ranks: Mapping[str, int] | None = None) -> int:
    ranks = header_ranks() if ranks is None else ranks
    return row2_circulation(ranks)


def predicted_suffixes(
    *,
    symbol: int = NEWLINE_SYMBOL,
    ranks: Mapping[str, int] | None = None,
) -> tuple[int, int, int] | None:
    """Return budget-minus-preimage suffixes, if all are nonnegative."""

    ranks = header_ranks() if ranks is None else ranks
    budget = phase_budget(ranks)
    suffixes = tuple(
        budget - symbol_preimage(ranks[name], symbol)
        for name in ROW2_MESSAGES
    )
    if min(suffixes) < 0:
        return None
    return suffixes  # type: ignore[return-value]


def initial_common_phase(
    bodies: Mapping[str, Sequence[int]],
) -> int:
    signatures = tuple(
        equality_signature(bodies[name][OPENING_EXIT:])
        for name in ROW2_MESSAGES
    )
    return common_prefix_length(signatures)


def phase_starts(
    bodies: Mapping[str, Sequence[int]],
    suffixes: Sequence[int],
) -> tuple[int, int, int]:
    if len(suffixes) != 3:
        raise ValueError("one suffix is required per row-2 panel")
    common = initial_common_phase(bodies)
    starts = tuple(
        OPENING_EXIT + common + suffix
        for suffix in suffixes
    )
    if any(
        start >= len(bodies[name])
        for name, start in zip(ROW2_MESSAGES, starts, strict=True)
    ):
        raise ValueError("predicted phase start lies outside a body")
    return starts  # type: ignore[return-value]


@dataclass(frozen=True)
class Row2PhaseMetrics:
    suffixes: tuple[int, int, int]
    old_common: int
    starts: tuple[int, int, int]
    pair: tuple[str, str]
    pair_bridge_length: int
    pair_complete: bool
    pair_switch: bool
    new_common: int

    @property
    def joint(self) -> bool:
        return (
            self.pair_complete
            and self.pair_switch
            and self.new_common >= TARGET_NEW_COMMON
        )


def transfer_metrics(
    bodies: Mapping[str, Sequence[int]],
    *,
    suffixes: Sequence[int] | None = None,
    pair: tuple[str, str] = PRIMARY_PAIR,
) -> Row2PhaseMetrics:
    suffixes = (
        predicted_suffixes()
        if suffixes is None
        else tuple(suffixes)
    )
    if suffixes is None:
        raise ValueError("predicted suffixes are negative")
    suffixes = tuple(suffixes)
    starts = phase_starts(bodies, suffixes)
    start_by_name = dict(zip(ROW2_MESSAGES, starts, strict=True))
    left, right = pair
    if left not in start_by_name or right not in start_by_name or left == right:
        raise ValueError("pair must contain distinct row-2 messages")
    left_bridge = tuple(bodies[left][OPENING_EXIT : start_by_name[left]])
    right_bridge = tuple(bodies[right][OPENING_EXIT : start_by_name[right]])
    bridge_length = min(len(left_bridge), len(right_bridge))
    profile = synchronization_profile(
        left_bridge[:bridge_length],
        right_bridge[:bridge_length],
    )
    pair_complete = profile.first_conflict is None
    extended = synchronization_profile(
        left_bridge[:bridge_length]
        + (bodies[left][OPENING_EXIT + bridge_length],),
        right_bridge[:bridge_length]
        + (bodies[right][OPENING_EXIT + bridge_length],),
    )
    pair_switch = (
        pair_complete
        and extended.first_conflict == bridge_length
    )
    new_signatures = tuple(
        equality_signature(bodies[name][start:])
        for name, start in zip(ROW2_MESSAGES, starts, strict=True)
    )
    return Row2PhaseMetrics(
        suffixes=suffixes,  # type: ignore[arg-type]
        old_common=initial_common_phase(bodies),
        starts=starts,
        pair=pair,
        pair_bridge_length=bridge_length,
        pair_complete=pair_complete,
        pair_switch=pair_switch,
        new_common=common_prefix_length(new_signatures),
    )


def broad_suffix_vectors(
    ranks: Mapping[str, int] | None = None,
) -> tuple[tuple[int, int, int], ...]:
    ranks = header_ranks() if ranks is None else ranks
    variants = set()
    for symbol in ALL_SYMBOLS:
        suffixes = predicted_suffixes(symbol=symbol, ranks=ranks)
        if suffixes is None:
            continue
        variants.update(permutations(suffixes))
    return tuple(sorted(variants))


CANONICAL_BROAD_SUFFIX_VECTORS = broad_suffix_vectors()


@dataclass(frozen=True)
class Row2BroadMetrics:
    maximum_new_common: int
    any_pair_complete: bool
    any_pair_switch: bool
    any_joint: bool


def broad_metrics(
    bodies: Mapping[str, Sequence[int]],
) -> Row2BroadMetrics:
    old_common = initial_common_phase(bodies)
    maximum = 0
    any_complete = False
    any_switch = False
    any_joint = False
    for suffixes in CANONICAL_BROAD_SUFFIX_VECTORS:
        starts = tuple(
            OPENING_EXIT + old_common + suffix
            for suffix in suffixes
        )
        start_by_name = dict(zip(ROW2_MESSAGES, starts, strict=True))
        new_signatures = tuple(
            equality_signature(bodies[name][start:])
            for name, start in zip(ROW2_MESSAGES, starts, strict=True)
        )
        new_common = common_prefix_length(new_signatures)
        maximum = max(maximum, new_common)
        for pair in combinations(ROW2_MESSAGES, 2):
            left, right = pair
            left_bridge = tuple(
                bodies[left][OPENING_EXIT : start_by_name[left]]
            )
            right_bridge = tuple(
                bodies[right][OPENING_EXIT : start_by_name[right]]
            )
            length = min(len(left_bridge), len(right_bridge))
            profile = synchronization_profile(
                left_bridge[:length],
                right_bridge[:length],
            )
            complete = profile.first_conflict is None
            extended = synchronization_profile(
                left_bridge[:length]
                + (bodies[left][OPENING_EXIT + length],),
                right_bridge[:length]
                + (bodies[right][OPENING_EXIT + length],),
            )
            switch = complete and extended.first_conflict == length
            any_complete |= complete
            any_switch |= switch
            any_joint |= (
                complete
                and switch
                and new_common >= TARGET_NEW_COMMON
            )
    return Row2BroadMetrics(
        maximum,
        any_complete,
        any_switch,
        any_joint,
    )


def shuffle_post_opening(
    body: Sequence[int],
    rng: random.Random,
    *,
    max_attempts: int = 10000,
) -> tuple[int, ...]:
    body = tuple(body)
    opening = body[:OPENING_EXIT]
    suffix = body[OPENING_EXIT:]
    for _ in range(max_attempts):
        shuffled = shuffle_without_adjacent_doubles(suffix, rng)
        if opening[-1] == shuffled[0]:
            continue
        return opening + shuffled
    raise RuntimeError("failed to shuffle a row-2 post-opening body")


def shuffled_row2_bodies(
    bodies: Mapping[str, Sequence[int]],
    rng: random.Random,
) -> dict[str, tuple[int, ...]]:
    return {
        name: shuffle_post_opening(bodies[name], rng)
        for name in ROW2_MESSAGES
    }


@dataclass(frozen=True)
class Row2ControlAudit:
    controls: int
    seed: int
    observed: Row2PhaseMetrics
    observed_broad: Row2BroadMetrics
    new_common_exceedances: int
    pair_complete_exceedances: int
    pair_switch_exceedances: int
    joint_exceedances: int
    broad_new_common_exceedances: int
    broad_joint_exceedances: int

    @staticmethod
    def corrected_tail(exceedances: int, controls: int) -> float:
        return (exceedances + 1) / (controls + 1)


def audit_controls(
    *,
    controls: int = 50000,
    seed: int = 0xB0D2,
) -> Row2ControlAudit:
    if controls < 1:
        raise ValueError("at least one control is required")
    rng = random.Random(seed)
    bodies = row2_bodies()
    observed = transfer_metrics(bodies)
    observed_broad = broad_metrics(bodies)
    counts = {
        "common": 0,
        "complete": 0,
        "switch": 0,
        "joint": 0,
        "broad_common": 0,
        "broad_joint": 0,
    }
    for _ in range(controls):
        shuffled = shuffled_row2_bodies(bodies, rng)
        metrics = transfer_metrics(shuffled)
        broad = broad_metrics(shuffled)
        counts["common"] += metrics.new_common >= observed.new_common
        counts["complete"] += metrics.pair_complete
        counts["switch"] += metrics.pair_switch
        counts["joint"] += metrics.joint
        counts["broad_common"] += (
            broad.maximum_new_common
            >= observed_broad.maximum_new_common
        )
        counts["broad_joint"] += broad.any_joint
    return Row2ControlAudit(
        controls=controls,
        seed=seed,
        observed=observed,
        observed_broad=observed_broad,
        new_common_exceedances=counts["common"],
        pair_complete_exceedances=counts["complete"],
        pair_switch_exceedances=counts["switch"],
        joint_exceedances=counts["joint"],
        broad_new_common_exceedances=counts["broad_common"],
        broad_joint_exceedances=counts["broad_joint"],
    )
