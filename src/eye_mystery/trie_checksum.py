"""Checksum tests after merging the copied Eye-message body prefixes."""

from __future__ import annotations

from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from random import Random

from .prefix_hierarchy import PrefixCluster, prefix_clusters
from .prefix_hierarchy import serialize_trie_edges


@dataclass(frozen=True)
class TrieChecksum:
    edge_count: int
    total: int
    residue: int
    label_multiplicities: tuple[int, ...]


@dataclass(frozen=True)
class BranchChecksum:
    cluster: PrefixCluster
    descendant_edge_count: int
    descendant_total: int
    descendant_residue: int


def trie_checksum(
    streams: Mapping[str, Sequence[int]],
    order: Sequence[str],
    *,
    start: int,
    modulus: int = 101,
) -> TrieChecksum:
    """Count each distinct prefix-trie edge once and sum its label."""

    values = serialize_trie_edges(
        streams, order, start=start, breadth_first=False
    )
    alphabet_size = max((max(stream) for stream in streams.values()), default=-1) + 1
    counts = Counter(values)
    total = sum(values)
    return TrieChecksum(
        edge_count=len(values),
        total=total,
        residue=total % modulus,
        label_multiplicities=tuple(counts[value] for value in range(alphabet_size)),
    )


def branch_descendant_checksums(
    streams: Mapping[str, Sequence[int]],
    *,
    start: int,
    modulus: int = 101,
) -> tuple[BranchChecksum, ...]:
    """Checksum every branching node after its complete shared prefix."""

    results = []
    for cluster in prefix_clusters(streams, start=start):
        subset = {name: streams[name] for name in cluster.members}
        checksum = trie_checksum(
            subset,
            cluster.members,
            start=start + cluster.length,
            modulus=modulus,
        )
        results.append(
            BranchChecksum(
                cluster=cluster,
                descendant_edge_count=checksum.edge_count,
                descendant_total=checksum.total,
                descendant_residue=checksum.residue,
            )
        )
    return tuple(results)


@dataclass(frozen=True)
class AffineRelabelingCalibration:
    zero_count: int
    total: int
    zero_translations: tuple[int, ...]


def affine_f83_relabeling_calibration(
    multiplicities: Sequence[int], *, checksum_modulus: int = 101
) -> AffineRelabelingCalibration:
    """Relabel ``0..82`` by every affine permutation of F83."""

    if len(multiplicities) != 83:
        raise ValueError("expected one multiplicity for every label in F83")
    zero_count = 0
    zero_translations: list[int] = []
    for multiplier in range(1, 83):
        for translation in range(83):
            residue = sum(
                count * ((multiplier * label + translation) % 83)
                for label, count in enumerate(multiplicities)
            ) % checksum_modulus
            if residue == 0:
                zero_count += 1
                if multiplier == 1:
                    zero_translations.append(translation)
    return AffineRelabelingCalibration(
        zero_count=zero_count,
        total=82 * 83,
        zero_translations=tuple(zero_translations),
    )


def random_relabeling_zero_count(
    multiplicities: Sequence[int],
    *,
    samples: int,
    seed: int,
    checksum_modulus: int = 101,
) -> int:
    """Monte Carlo global relabelings preserving the entire equality trie."""

    if samples < 0:
        raise ValueError("samples must be nonnegative")
    rng = Random(seed)
    labels = list(range(len(multiplicities)))
    zero_count = 0
    for _ in range(samples):
        rng.shuffle(labels)
        zero_count += (
            sum(
                count * relabeled
                for count, relabeled in zip(multiplicities, labels, strict=True)
            )
            % checksum_modulus
            == 0
        )
    return zero_count


def vector_rank_mod(vectors: Sequence[Sequence[int]], modulus: int) -> int:
    """Rank of row vectors over a prime field."""

    if not vectors:
        return 0
    width = len(vectors[0])
    if any(len(vector) != width for vector in vectors):
        raise ValueError("vectors must have equal widths")
    matrix = [list(value % modulus for value in vector) for vector in vectors]
    rank = 0
    for column in range(width):
        pivot = next(
            (row for row in range(rank, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inverse = pow(matrix[rank][column], -1, modulus)
        matrix[rank] = [(value * inverse) % modulus for value in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank or not matrix[row][column]:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                (left - factor * right) % modulus
                for left, right in zip(matrix[row], matrix[rank], strict=True)
            ]
        rank += 1
        if rank == len(matrix):
            break
    return rank
