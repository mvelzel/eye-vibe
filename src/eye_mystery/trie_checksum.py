"""Checksum tests after merging the copied Eye-message body prefixes."""

from __future__ import annotations

from collections import Counter
from collections import defaultdict
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from itertools import permutations
from math import factorial
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
    label_multiplicities: tuple[int, ...]


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
                label_multiplicities=checksum.label_multiplicities,
            )
        )
    return tuple(results)


@dataclass(frozen=True)
class AffineRelabelingCalibration:
    zero_count: int
    total: int
    zero_translations: tuple[int, ...]


@dataclass(frozen=True)
class SignatureRelabelingCalibration:
    """Exact checksum distribution in a checksum-preserving subgroup."""

    residue_counts: tuple[int, ...]

    @property
    def total(self) -> int:
        return sum(self.residue_counts)

    @property
    def zero_count(self) -> int:
        return self.residue_counts[0]


@dataclass(frozen=True)
class JointSignatureRelabelingCalibration:
    """Exact joint distribution of two sums in the same protected subgroup."""

    residue_counts: tuple[tuple[int, ...], ...]

    @property
    def total(self) -> int:
        return sum(sum(row) for row in self.residue_counts)

    def count(self, first_residue: int, second_residue: int) -> int:
        return self.residue_counts[first_residue][second_residue]


@dataclass(frozen=True)
class LinearSignatureRelabelingCalibration:
    """Exact integer distribution of a signed label statistic."""

    value_counts: tuple[tuple[int, int], ...]

    @property
    def total(self) -> int:
        return sum(count for _, count in self.value_counts)

    def count(self, value: int) -> int:
        return dict(self.value_counts).get(value, 0)


def _signature_groups(
    alphabet_size: int,
    constraint_vectors: Sequence[Sequence[int]],
    fixed_labels: Sequence[int],
) -> list[list[int]]:
    if any(len(vector) != alphabet_size for vector in constraint_vectors):
        raise ValueError("constraint vectors must span the visible alphabet")
    fixed = set(fixed_labels)
    if any(label not in range(alphabet_size) for label in fixed):
        raise ValueError("fixed label outside the visible alphabet")
    classes: dict[tuple[int, ...], list[int]] = defaultdict(list)
    for label in range(alphabet_size):
        classes[
            tuple(vector[label] for vector in constraint_vectors)
        ].append(label)
    groups: list[list[int]] = []
    for labels in classes.values():
        groups.extend([label] for label in labels if label in fixed)
        free = [label for label in labels if label not in fixed]
        if free:
            groups.append(free)
    return groups


def random_signature_preserving_relabeling(
    alphabet_size: int,
    constraint_vectors: Sequence[Sequence[int]],
    rng: Random,
    *,
    fixed_labels: Sequence[int] = (),
) -> tuple[int, ...]:
    """Draw one uniform relabeling from the protected signature subgroup."""

    groups = _signature_groups(
        alphabet_size,
        constraint_vectors,
        fixed_labels,
    )
    mapping = list(range(alphabet_size))
    for labels in groups:
        replacements = labels.copy()
        rng.shuffle(replacements)
        for label, replacement in zip(labels, replacements, strict=True):
            mapping[label] = replacement
    return tuple(mapping)


def signature_preserving_relabeling_calibration(
    multiplicities: Sequence[int],
    constraint_vectors: Sequence[Sequence[int]],
    *,
    fixed_labels: Sequence[int] = (),
    checksum_modulus: int = 101,
) -> SignatureRelabelingCalibration:
    """Permute labels having identical counts in every protected message.

    Such relabelings preserve each protected message sum exactly, not merely
    modulo the checksum.  Fixed labels can additionally preserve the visible
    marker values.  Independent within-class residue histograms are convolved
    to count the entire subgroup exactly.
    """

    alphabet_size = len(multiplicities)
    groups = _signature_groups(
        alphabet_size, constraint_vectors, fixed_labels
    )

    distribution = [0] * checksum_modulus
    distribution[0] = 1
    expected_total = 1
    for labels in groups:
        group_distribution = [0] * checksum_modulus
        for relabeled in permutations(labels):
            residue = sum(
                multiplicities[label] * value
                for label, value in zip(labels, relabeled, strict=True)
            ) % checksum_modulus
            group_distribution[residue] += 1
        next_distribution = [0] * checksum_modulus
        for left_residue, left_count in enumerate(distribution):
            if not left_count:
                continue
            for right_residue, right_count in enumerate(group_distribution):
                if right_count:
                    next_distribution[
                        (left_residue + right_residue) % checksum_modulus
                    ] += left_count * right_count
        distribution = next_distribution
        expected_total *= factorial(len(labels))
    if sum(distribution) != expected_total:
        raise AssertionError("relabeling convolution lost assignments")
    return SignatureRelabelingCalibration(tuple(distribution))


def signature_preserving_joint_calibration(
    first_multiplicities: Sequence[int],
    second_multiplicities: Sequence[int],
    constraint_vectors: Sequence[Sequence[int]],
    *,
    fixed_labels: Sequence[int] = (),
    checksum_modulus: int = 101,
) -> JointSignatureRelabelingCalibration:
    """Count two checksum residues over every protected relabeling exactly."""

    if len(first_multiplicities) != len(second_multiplicities):
        raise ValueError("the two count vectors must span the same alphabet")
    groups = _signature_groups(
        len(first_multiplicities), constraint_vectors, fixed_labels
    )
    distribution: dict[tuple[int, int], int] = {(0, 0): 1}
    expected_total = 1
    for labels in groups:
        group_distribution: Counter[tuple[int, int]] = Counter()
        for relabeled in permutations(labels):
            first = sum(
                first_multiplicities[label] * value
                for label, value in zip(labels, relabeled, strict=True)
            ) % checksum_modulus
            second = sum(
                second_multiplicities[label] * value
                for label, value in zip(labels, relabeled, strict=True)
            ) % checksum_modulus
            group_distribution[first, second] += 1
        next_distribution: dict[tuple[int, int], int] = defaultdict(int)
        for (left_first, left_second), left_count in distribution.items():
            for (right_first, right_second), right_count in group_distribution.items():
                next_distribution[
                    (
                        (left_first + right_first) % checksum_modulus,
                        (left_second + right_second) % checksum_modulus,
                    )
                ] += left_count * right_count
        distribution = dict(next_distribution)
        expected_total *= factorial(len(labels))
    rows = tuple(
        tuple(
            distribution.get((first, second), 0)
            for second in range(checksum_modulus)
        )
        for first in range(checksum_modulus)
    )
    result = JointSignatureRelabelingCalibration(rows)
    if result.total != expected_total:
        raise AssertionError("joint relabeling convolution lost assignments")
    return result


def signature_preserving_linear_calibration(
    coefficients: Sequence[int],
    constraint_vectors: Sequence[Sequence[int]],
    *,
    fixed_labels: Sequence[int] = (),
) -> LinearSignatureRelabelingCalibration:
    """Count a signed integer statistic over every protected relabeling."""

    groups = _signature_groups(
        len(coefficients), constraint_vectors, fixed_labels
    )
    distribution: Counter[int] = Counter({0: 1})
    expected_total = 1
    for labels in groups:
        group_distribution: Counter[int] = Counter()
        for relabeled in permutations(labels):
            value = sum(
                coefficients[label] * replacement
                for label, replacement in zip(labels, relabeled, strict=True)
            )
            group_distribution[value] += 1
        next_distribution: Counter[int] = Counter()
        for left_value, left_count in distribution.items():
            for right_value, right_count in group_distribution.items():
                next_distribution[left_value + right_value] += (
                    left_count * right_count
                )
        distribution = next_distribution
        expected_total *= factorial(len(labels))
    result = LinearSignatureRelabelingCalibration(
        tuple(sorted(distribution.items()))
    )
    if result.total != expected_total:
        raise AssertionError("linear relabeling convolution lost assignments")
    return result


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
