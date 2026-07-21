"""Connect the procedural-wand 83/101 branch to Eye trie structure."""

from __future__ import annotations

import re
from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from .prefix_hierarchy import prefix_clusters
from .random_thresholds import successful_outcomes


ACTION_ENUM = re.compile(
    rb"^ACTION_TYPE_([A-Z_]+)\s*=\s*(\d+)\s*$", re.MULTILINE
)
ACTION_ASSIGNMENT = re.compile(rb"type\s*=\s*ACTION_TYPE_([A-Z_]+)")


def action_type_enums(contents: bytes) -> dict[str, int]:
    return {
        match.group(1).decode("ascii"): int(match.group(2))
        for match in ACTION_ENUM.finditer(contents)
    }


def action_type_counts(contents: bytes) -> Counter[str]:
    return Counter(
        match.group(1).decode("ascii")
        for match in ACTION_ASSIGNMENT.finditer(contents)
    )


def compressed_branch_degrees(
    streams: Mapping[str, Sequence[int]], *, start: int = 0
) -> tuple[int, ...]:
    """Return the fan-out of each internal node in prefix-cluster order."""

    degrees = []
    for cluster in prefix_clusters(streams, start=start):
        following = set()
        for name in cluster.members:
            index = start + cluster.length
            following.add(
                streams[name][index] if index < len(streams[name]) else None
            )
        degrees.append(len(following))
    return tuple(degrees)


@dataclass(frozen=True)
class SelectorPartition:
    modifier_outcomes: tuple[int, ...]
    draw_many_outcomes: tuple[int, ...]

    @property
    def domain_size(self) -> int:
        return len(self.modifier_outcomes) + len(self.draw_many_outcomes)


def procedural_wand_partition() -> SelectorPartition:
    modifier = successful_outcomes("<", 83)
    draw_many = tuple(value for value in range(101) if value not in modifier)
    return SelectorPartition(modifier, draw_many)
