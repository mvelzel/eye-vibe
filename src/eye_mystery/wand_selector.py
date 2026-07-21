"""Connect the procedural-wand 83/101 branch to Eye trie structure."""

from __future__ import annotations

import re
from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from itertools import combinations

from .prefix_hierarchy import prefix_clusters
from .random_thresholds import successful_outcomes
from .trie_checksum import branch_descendant_checksums


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


@dataclass(frozen=True)
class ControlScope:
    """One internal Eye-trie subtree and its locally owned control records."""

    members: tuple[str, ...]
    depth: int
    degree: int
    internal_nodes: int
    structural_records: int
    visible_edges: int
    visible_residue: int


def compressed_control_scopes(
    streams: Mapping[str, Sequence[int]],
    *,
    start: int = 0,
    modulus: int = 101,
) -> tuple[ControlScope, ...]:
    """Audit structural-record counts in every compressed-trie subtree.

    A control record is counted for each internal branch node and for each of
    its outgoing compressed edges.  This is the exact convention behind the
    exploratory ``5 + 13 = 18`` correspondence.  Restricting the count to a
    subtree reveals whether a checksum complement and its proposed controls
    inhabit the same scope.
    """

    clusters = prefix_clusters(streams, start=start)
    checksums = branch_descendant_checksums(
        streams, start=start, modulus=modulus
    )
    degrees = compressed_branch_degrees(streams, start=start)
    results = []
    for cluster, checksum, degree in zip(
        clusters, checksums, degrees, strict=True
    ):
        members = set(cluster.members)
        descendant_indices = tuple(
            index
            for index, other in enumerate(clusters)
            if set(other.members) <= members
        )
        results.append(
            ControlScope(
                members=cluster.members,
                depth=cluster.length,
                degree=degree,
                internal_nodes=len(descendant_indices),
                structural_records=sum(
                    1 + degrees[index] for index in descendant_indices
                ),
                visible_edges=checksum.descendant_edge_count,
                visible_residue=checksum.descendant_residue,
            )
        )
    return tuple(results)


def hidden_subset_residue_count(
    values: Sequence[int],
    choose_count: int,
    target_residue: int,
    *,
    modulus: int = 101,
) -> int:
    """Count unordered hidden-label subsets with a requested residue."""

    if choose_count < 0 or choose_count > len(values):
        return 0
    return sum(
        sum(selection) % modulus == target_residue % modulus
        for selection in combinations(values, choose_count)
    )
