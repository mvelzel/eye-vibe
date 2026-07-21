"""Canonical branch/exit records selected by the decoded Eye metadata."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from eye_mystery.prefix_hierarchy import breadth_first_prefix_clusters


@dataclass(frozen=True)
class BranchExitRecord:
    members: tuple[str, ...]
    depth: int
    exit_labels: tuple[int, ...]

    def corrected_sum(self, *, modulus: int = 101, depth_coefficient: int = 1) -> int:
        """Add the node depth to its distinct outgoing labels modulo ``modulus``."""
        return (
            sum(self.exit_labels) + depth_coefficient * self.depth
        ) % modulus


def branch_exit_records(
    streams: Mapping[str, Sequence[int]],
) -> tuple[BranchExitRecord, ...]:
    """Read branch nodes breadth-first and retain each distinct next edge once.

    Input order fixes sibling order.  With marker-free Eye bodies in the
    independently decoded East-5-first order, record depths spell ``BEXIT``.
    """
    records = []
    for cluster in breadth_first_prefix_clusters(streams):
        labels: list[int] = []
        for name in cluster.members:
            if cluster.length >= len(streams[name]):
                raise ValueError("a branch member ends at an internal node")
            label = streams[name][cluster.length]
            if label not in labels:
                labels.append(label)
        records.append(BranchExitRecord(cluster.members, cluster.length, tuple(labels)))
    return tuple(records)


def corrected_exit_residues(
    records: Sequence[BranchExitRecord],
    *,
    modulus: int = 101,
    depth_coefficient: int = 1,
) -> tuple[int, ...]:
    """Return one depth-corrected outgoing-label sum per branch record."""
    return tuple(
        record.corrected_sum(
            modulus=modulus,
            depth_coefficient=depth_coefficient,
        )
        for record in records
    )
