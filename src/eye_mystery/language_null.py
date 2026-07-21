"""Structure-preserving nulls for language-model experiments."""

from __future__ import annotations

import random
from collections.abc import Mapping, Sequence

from .prefix_hierarchy import prefix_clusters


def prefix_tree_parity_shuffle(
    streams: Mapping[str, Sequence[int]],
    reference_streams: Mapping[str, Sequence[int]],
    rng: random.Random,
    *,
    start: int = 1,
) -> dict[str, tuple[int, ...]]:
    """Shuffle jointly inside every prefix-tree edge, preserving parity.

    The same position permutation is applied to every member of a shared
    prefix edge.  Singleton suffixes are shuffled independently.  This keeps
    message lengths, per-message parity frequencies, and the complete copied
    prefix hierarchy while destroying local order inside each disjoint block.
    Positions before ``start`` are left fixed.
    """

    if set(streams) != set(reference_streams):
        raise ValueError("stream and reference names must match")
    if any(len(streams[name]) != len(reference_streams[name]) for name in streams):
        raise ValueError("stream and reference lengths must match")
    output = {name: list(values) for name, values in streams.items()}
    covered = {name: set(range(start)) for name in streams}
    clusters = prefix_clusters(reference_streams, start=start)

    for cluster in clusters:
        supersets = [
            parent.length
            for parent in clusters
            if set(cluster.members) < set(parent.members)
        ]
        parent_length = max(supersets, default=0)
        positions = list(
            range(start + parent_length, start + cluster.length)
        )
        for parity in (0, 1):
            targets = [position for position in positions if position % 2 == parity]
            sources = targets.copy()
            rng.shuffle(sources)
            for name in cluster.members:
                for target, source in zip(targets, sources, strict=True):
                    output[name][target] = streams[name][source]
                covered[name].update(targets)

    for name, values in streams.items():
        for parity in (0, 1):
            targets = [
                position
                for position in range(start, len(values))
                if position % 2 == parity and position not in covered[name]
            ]
            sources = targets.copy()
            rng.shuffle(sources)
            for target, source in zip(targets, sources, strict=True):
                output[name][target] = values[source]
    return {name: tuple(values) for name, values in output.items()}
