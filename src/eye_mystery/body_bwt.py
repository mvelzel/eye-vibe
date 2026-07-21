"""Calibrated BWT diagnostics for the concatenated Eye-message bodies."""

from __future__ import annotations

import random
from collections.abc import Sequence

from .corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from .language_null import prefix_tree_parity_shuffle
from .marker_bwt import stable_lf_mapping


def lf_cycle_lengths(last_column: Sequence[int]) -> tuple[int, ...]:
    """Return the LF permutation's cycle lengths in descending order."""

    lf = stable_lf_mapping(tuple(last_column))
    visited: set[int] = set()
    lengths = []
    for start in range(len(lf)):
        if start in visited:
            continue
        position = start
        length = 0
        while position not in visited:
            visited.add(position)
            length += 1
            position = lf[position]
        lengths.append(length)
    return tuple(sorted(lengths, reverse=True))


def eye_bodies() -> dict[str, tuple[int, ...]]:
    """Return the nine canonical trigram streams with markers removed."""

    return {
        name: trigram_values(MESSAGES[name])[1:] for name in MESSAGE_ORDER
    }


def concatenate_bodies(
    bodies: dict[str, tuple[int, ...]],
) -> tuple[int, ...]:
    return tuple(value for name in MESSAGE_ORDER for value in bodies[name])


def single_cycle_deletions() -> tuple[tuple[int, str, int, int], ...]:
    """Find one-value deletions that make canonical bodies a cyclic BWT."""

    bodies = eye_bodies()
    stream = concatenate_bodies(bodies)
    locations = []
    for name in MESSAGE_ORDER:
        locations.extend((name, index) for index in range(len(bodies[name])))
    result = []
    for index, (name, body_index) in enumerate(locations):
        candidate = stream[:index] + stream[index + 1 :]
        if lf_cycle_lengths(candidate) == (len(candidate),):
            result.append((index, name, body_index, stream[index]))
    return tuple(result)


def body_bwt_null_counts(
    trials: int = 10_000, seed: int = 20_260_721
) -> dict[str, int]:
    """Compare the near-cycle with prefix-tree-preserving parity shuffles."""

    bodies = eye_bodies()
    observed_size = len(concatenate_bodies(bodies))
    threshold = observed_size - 1
    rng = random.Random(seed)
    counts = {
        "trials": trials,
        "max_cycle_at_least_observed": 0,
        "exact_observed_cycles": 0,
        "single_cycle": 0,
    }
    for _ in range(trials):
        shuffled = prefix_tree_parity_shuffle(
            bodies, bodies, rng, start=0
        )
        cycles = lf_cycle_lengths(concatenate_bodies(shuffled))
        counts["max_cycle_at_least_observed"] += cycles[0] >= threshold
        counts["exact_observed_cycles"] += cycles == (threshold, 1)
        counts["single_cycle"] += cycles == (observed_size,)
    return counts
