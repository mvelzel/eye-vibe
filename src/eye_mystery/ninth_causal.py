"""Breadth-first causal diagnostics for the ninth Eye-cipher pass.

The functions in this module deliberately operate on equality, incidence, and
transition support before assigning meanings to the 83 visible labels.  Each
lane has a matched control or an exact obstruction; none is a plaintext
search.
"""

from __future__ import annotations

import math
import random
from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from itertools import combinations, permutations

from eye_mystery.corpus import MESSAGE_ORDER, ROW_PAIR_TRIGRAM_LENGTHS
from eye_mystery.factoradic_headers import (
    P_MESSAGES,
    Q_EAST_MESSAGES,
    Q_WEST_MESSAGES,
)
from eye_mystery.prefix_hierarchy import prefix_clusters


ALPHABET_SIZE = 83

# These are the thirteen exact partial maps audited by
# ``scripts/analyze_context_completions.py``.  Keeping the definitions here
# makes the learned-common-base control independently executable.
CONTEXT_SPECS = (
    ("marker-e1-w1", "east1", 0, "west1", 0, 25),
    ("marker-e1-e2", "east1", 0, "east2", 0, 25),
    ("marker-w2-e3", "west2", 0, "east3", 0, 6),
    ("marker-w2-w3", "west2", 0, "west3", 0, 6),
    ("marker-e4-w4", "east4", 0, "west4", 0, 21),
    ("marker-e4-e5", "east4", 0, "east5", 0, 21),
    ("first-gap30", "west1", 34, "west1", 64, 18),
    ("first-cross", "west1", 34, "east2", 39, 18),
    ("first-cross-late", "west1", 34, "east2", 74, 18),
    ("first-gap28", "east1", 40, "east1", 68, 9),
    ("last-west4", "east4", 68, "west4", 71, 30),
    ("last-east5", "east4", 68, "east5", 69, 30),
    ("last-east3", "east4", 73, "east3", 64, 25),
)


def _hungarian_minimum(costs: Sequence[Sequence[int]]) -> tuple[int, ...]:
    """Return a minimum-cost row-to-column assignment for a square matrix."""

    size = len(costs)
    if any(len(row) != size for row in costs):
        raise ValueError("assignment matrix must be square")
    # Classic O(n^3) shortest augmenting-path Hungarian algorithm.  The
    # 1-based sentinel form is compact and deterministic under ties.
    u = [0] * (size + 1)
    v = [0] * (size + 1)
    matched_row = [0] * (size + 1)
    predecessor = [0] * (size + 1)
    for row in range(1, size + 1):
        matched_row[0] = row
        column = 0
        minimum = [math.inf] * (size + 1)
        used = [False] * (size + 1)
        while True:
            used[column] = True
            current_row = matched_row[column]
            delta = math.inf
            next_column = 0
            for candidate in range(1, size + 1):
                if used[candidate]:
                    continue
                reduced = (
                    costs[current_row - 1][candidate - 1]
                    - u[current_row]
                    - v[candidate]
                )
                if reduced < minimum[candidate]:
                    minimum[candidate] = reduced
                    predecessor[candidate] = column
                if minimum[candidate] < delta:
                    delta = minimum[candidate]
                    next_column = candidate
            for candidate in range(size + 1):
                if used[candidate]:
                    u[matched_row[candidate]] += delta
                    v[candidate] -= delta
                else:
                    minimum[candidate] -= delta
            column = next_column
            if matched_row[column] == 0:
                break
        while True:
            previous = predecessor[column]
            matched_row[column] = matched_row[previous]
            column = previous
            if column == 0:
                break
    assignment = [0] * size
    for column in range(1, size + 1):
        assignment[matched_row[column] - 1] = column - 1
    return tuple(assignment)


@dataclass(frozen=True)
class CommonBaseScore:
    agreements: int
    edges: int
    assignment: tuple[int, ...]

    @property
    def disagreements(self) -> int:
        return self.edges - self.agreements


def common_base_score(
    mappings: Sequence[Mapping[int, int]], *, alphabet_size: int = ALPHABET_SIZE
) -> CommonBaseScore:
    """Learn the one permutation agreeing with the most observed context edges.

    This is an exact assignment lower bound for the planned common-Cayley-base
    problem.  If even one unconstrained base permutation cannot agree with the
    partial maps unusually often, small-radius completions cannot rescue it.
    A positive result is only a screen and does not establish a Cayley radius.
    """

    weights = [[0] * alphabet_size for _ in range(alphabet_size)]
    edges = 0
    for mapping in mappings:
        if len(set(mapping.values())) != len(mapping):
            raise ValueError("each context mapping must be injective")
        for source, target in mapping.items():
            if source not in range(alphabet_size) or target not in range(alphabet_size):
                raise ValueError("context edge lies outside the alphabet")
            weights[source][target] += 1
            edges += 1
    largest = max((max(row) for row in weights), default=0)
    costs = [[largest - weight for weight in row] for row in weights]
    assignment = _hungarian_minimum(costs)
    agreements = sum(weights[source][target] for source, target in enumerate(assignment))
    return CommonBaseScore(agreements, edges, assignment)


def shuffled_context_mappings(
    mappings: Sequence[Mapping[int, int]], rng: random.Random
) -> tuple[dict[int, int], ...]:
    """Shuffle each observed image set over its fixed domain.

    The control preserves every context's domain, image, edge count, and
    injectivity while breaking only the source/target correspondence.
    """

    output = []
    for mapping in mappings:
        sources = tuple(sorted(mapping))
        targets = list(mapping.values())
        rng.shuffle(targets)
        output.append(dict(zip(sources, targets, strict=True)))
    return tuple(output)


def equality_signature(sequence: Sequence[int]) -> tuple[int, ...]:
    """Encode a sequence by first-occurrence indices (its equality skeleton)."""

    labels: dict[int, int] = {}
    result = []
    for value in sequence:
        if value not in labels:
            labels[value] = len(labels)
        result.append(labels[value])
    return tuple(result)


@dataclass(frozen=True)
class SynchronizationProfile:
    length: int
    edges: int
    validation_positions: int
    first_validation: int | None
    last_new_edge: int
    first_conflict: int | None


def synchronization_profile(
    left: Sequence[int], right: Sequence[int]
) -> SynchronizationProfile:
    """Scan the evidence supplied by one aligned partial-bijection context."""

    if len(left) != len(right):
        raise ValueError("aligned contexts must have equal length")
    forward: dict[int, int] = {}
    reverse: dict[int, int] = {}
    validations = 0
    first_validation = None
    last_new = -1
    conflict = None
    for index, (source, target) in enumerate(zip(left, right, strict=True)):
        if (
            source in forward
            and forward[source] != target
            or target in reverse
            and reverse[target] != source
        ):
            conflict = index
            break
        if source in forward:
            validations += 1
            if first_validation is None:
                first_validation = index
        else:
            forward[source] = target
            reverse[target] = source
            last_new = index
    return SynchronizationProfile(
        len(left),
        len(forward),
        validations,
        first_validation,
        last_new,
        conflict,
    )


def partial_bijection_iff_same_equality_signature(
    left: Sequence[int], right: Sequence[int]
) -> bool:
    """Check the exact identity behind all aligned isomorph contexts."""

    profile = synchronization_profile(left, right)
    return (profile.first_conflict is None) == (
        equality_signature(left) == equality_signature(right)
    )


def deepest_leaf_depths(
    bodies: Mapping[str, Sequence[int]],
) -> dict[str, int]:
    clusters = prefix_clusters(bodies)
    return {
        name: max(cluster.length for cluster in clusters if name in cluster.members)
        for name in bodies
    }


def _immediate_children(
    cluster_members: Sequence[str],
    depth: int,
    bodies: Mapping[str, Sequence[int]],
) -> tuple[tuple[str, ...], ...]:
    groups: dict[int | None, list[str]] = {}
    for name in cluster_members:
        value = bodies[name][depth] if depth < len(bodies[name]) else None
        groups.setdefault(value, []).append(name)
    return tuple(tuple(group) for group in groups.values())


def branch_reconvergence_rows(
    bodies: Mapping[str, Sequence[int]],
) -> tuple[int, ...]:
    """Return one position bit-mask for each prefix-tree branch.

    A bit is set when members that left through different immediate child
    edges later show the same visible label at that aligned coordinate.
    Within-child equality is excluded because it belongs to a deeper branch.
    """

    rows = []
    for cluster in prefix_clusters(bodies):
        children = _immediate_children(cluster.members, cluster.length, bodies)
        pairs = tuple(
            (left, right)
            for first_index, first in enumerate(children)
            for second in children[first_index + 1 :]
            for left in first
            for right in second
        )
        mask = 0
        for left, right in pairs:
            for position in range(cluster.length + 1, min(len(bodies[left]), len(bodies[right]))):
                if bodies[left][position] == bodies[right][position]:
                    mask |= 1 << position
        rows.append(mask)
    return tuple(rows)


def gf2_rank(rows: Iterable[int]) -> int:
    """Return the exact binary rank of integer-encoded rows."""

    basis: dict[int, int] = {}
    for row in rows:
        value = row
        while value:
            pivot = value.bit_length() - 1
            if pivot in basis:
                value ^= basis[pivot]
            else:
                basis[pivot] = value
                break
    return len(basis)


def boolean_rank_small_rows(rows: Sequence[int]) -> int:
    """Return exact Boolean rank when the number of rows is small.

    For every nonempty subset of rows, its maximal legal rectangle contains
    precisely the columns where all subset rows are 1.  Enlarging a legal
    rectangle cannot hurt an OR cover, so searching those maximal rectangles
    is exact.  The Eye branch matrix has only five rows.
    """

    row_count = len(rows)
    if row_count == 0 or not any(rows):
        return 0
    patterns = set()
    width = max(row.bit_length() for row in rows)
    for column in range(width):
        pattern = sum(((row >> column) & 1) << index for index, row in enumerate(rows))
        if pattern:
            patterns.add(pattern)
    candidates = tuple(range(1, 1 << row_count))
    for count in range(1, row_count + 1):
        for selected in combinations(candidates, count):
            if all(
                pattern
                == _union_subsets(
                    subset for subset in selected if subset & ~pattern == 0
                )
                for pattern in patterns
            ):
                return count
    raise AssertionError("single-row rectangles always form a cover")


def _union_subsets(subsets: Iterable[int]) -> int:
    result = 0
    for subset in subsets:
        result |= subset
    return result


@dataclass(frozen=True)
class BranchInfluenceScore:
    branches: int
    active_columns: int
    gf2_rank: int
    boolean_rank: int
    nested_pairs: int


def branch_influence_score(
    bodies: Mapping[str, Sequence[int]],
) -> BranchInfluenceScore:
    rows = branch_reconvergence_rows(bodies)
    support = _union_subsets(rows)
    nested = sum(
        left & ~right == 0 or right & ~left == 0
        for left, right in combinations(rows, 2)
    )
    return BranchInfluenceScore(
        len(rows), support.bit_count(), gf2_rank(rows), boolean_rank_small_rows(rows), nested
    )


def shuffle_after_leaf_exits(
    bodies: Mapping[str, Sequence[int]], rng: random.Random
) -> dict[str, tuple[int, ...]]:
    """Prefix-tree-preserving positional control for branch influence."""

    depths = deepest_leaf_depths(bodies)
    output = {}
    for name, body in bodies.items():
        frozen = depths[name] + 1
        suffix = list(body[frozen:])
        rng.shuffle(suffix)
        output[name] = tuple(body[:frozen]) + tuple(suffix)
    return output


def aligned_equality_edge_colors(
    bodies: Mapping[str, Sequence[int]], *, truncate: bool
) -> dict[frozenset[str], tuple[int, ...]]:
    """Color every message pair by its aligned equality coordinates."""

    limit = min(map(len, bodies.values())) if truncate else None
    result = {}
    for left, right in combinations(bodies, 2):
        stop = limit if limit is not None else min(len(bodies[left]), len(bodies[right]))
        result[frozenset((left, right))] = tuple(
            index for index in range(stop) if bodies[left][index] == bodies[right][index]
        )
    return result


def message_automorphisms(
    bodies: Mapping[str, Sequence[int]], *, truncate: bool
) -> tuple[tuple[str, ...], ...]:
    """Enumerate message permutations preserving the aligned equality skeleton.

    ``truncate=True`` removes the otherwise decisive unequal path lengths and
    tests the common 98-coordinate core.  With ``truncate=False`` exact path
    length is retained as a vertex color.
    """

    names = tuple(bodies)
    colors = aligned_equality_edge_colors(bodies, truncate=truncate)
    automorphisms = []
    for image in permutations(names):
        mapping = dict(zip(names, image, strict=True))
        if not truncate and any(len(bodies[name]) != len(bodies[mapping[name]]) for name in names):
            continue
        if all(
            colors[frozenset((left, right))]
            == colors[frozenset((mapping[left], mapping[right]))]
            for left, right in combinations(names, 2)
        ):
            automorphisms.append(image)
    return tuple(automorphisms)


def transition_edges(
    bodies: Mapping[str, Sequence[int]],
) -> frozenset[tuple[int, int]]:
    return frozenset(
        (left, right)
        for body in bodies.values()
        for left, right in zip(body, body[1:])
    )


@dataclass(frozen=True)
class ForbiddenSupportScore:
    present_edges: int
    absent_rank: int
    distinct_absent_rows: int
    row_pattern_lower_bound: int


def forbidden_support_score(
    edges: Iterable[tuple[int, int]], *, alphabet_size: int = ALPHABET_SIZE
) -> ForbiddenSupportScore:
    """Measure exact algebraic complexity of the absent-transition matrix.

    ``row_pattern_lower_bound`` is a valid lower bound for an OR rectangle
    cover: k rectangles can induce at most 2**k distinct row patterns.  The
    GF(2) rank is an additional diagnostic, not claimed as a Boolean-rank
    bound because overlapping OR rectangles need not add by XOR.
    """

    edge_set = frozenset(edges)
    full = (1 << alphabet_size) - 1
    present_rows = [0] * alphabet_size
    for source, target in edge_set:
        if source == target:
            raise ValueError("no-loop support expected")
        present_rows[source] |= 1 << target
    absent = tuple(full ^ row for row in present_rows)
    distinct = len(set(absent))
    return ForbiddenSupportScore(
        len(edge_set),
        gf2_rank(absent),
        distinct,
        math.ceil(math.log2(distinct)) if distinct > 1 else 0,
    )


def degree_preserving_edge_swaps(
    edges: Iterable[tuple[int, int]],
    rng: random.Random,
    *,
    attempts: int,
) -> frozenset[tuple[int, int]]:
    """Randomize a directed simple graph while preserving degrees and no loops."""

    edge_set = set(edges)
    edge_list = list(edge_set)
    if len(edge_list) < 2:
        return frozenset(edge_set)
    for _ in range(attempts):
        first_index, second_index = rng.sample(range(len(edge_list)), 2)
        first = edge_list[first_index]
        second = edge_list[second_index]
        source1, target1 = first
        source2, target2 = second
        replacement1 = (source1, target2)
        replacement2 = (source2, target1)
        if (
            source1 == source2
            or target1 == target2
            or source1 == target2
            or source2 == target1
            or replacement1 in edge_set
            or replacement2 in edge_set
        ):
            continue
        edge_set.remove(first)
        edge_set.remove(second)
        edge_set.add(replacement1)
        edge_set.add(replacement2)
        edge_list[first_index] = replacement1
        edge_list[second_index] = replacement2
    return frozenset(edge_set)


def _repeat_distance_bin(body: Sequence[int], position: int) -> str:
    target = body[position]
    for previous in range(position - 1, -1, -1):
        if body[previous] == target:
            distance = position - previous
            if distance == 1:
                return "d1"
            if distance == 2:
                return "d2"
            if distance <= 4:
                return "d3-4"
            if distance <= 8:
                return "d5-8"
            if distance <= 16:
                return "d9-16"
            if distance <= 32:
                return "d17-32"
            return "d33+"
    return "new"


def invariant_transition_features(
    body: Sequence[int], *, start: int
) -> Counter[tuple[str, bool, bool]]:
    """Count label-permutation-invariant transition features after ``start``."""

    seen_edges: set[tuple[int, int]] = set()
    counts: Counter[tuple[str, bool, bool]] = Counter()
    for position in range(1, len(body)):
        edge = (body[position - 1], body[position])
        repeated_edge = edge in seen_edges
        seen_edges.add(edge)
        if position <= start:
            continue
        source_was_new = body[position - 1] not in body[: position - 1]
        counts[(_repeat_distance_bin(body, position), repeated_edge, source_was_new)] += 1
    return counts


def header_groups() -> tuple[frozenset[str], ...]:
    return tuple(
        frozenset(group)
        for group in (P_MESSAGES, Q_WEST_MESSAGES, Q_EAST_MESSAGES)
    )


def three_by_three_partitions(names: Sequence[str]) -> tuple[tuple[frozenset[str], ...], ...]:
    """Enumerate each unlabeled partition of nine names into three triples once."""

    names = tuple(names)
    if len(names) != 9 or len(set(names)) != 9:
        raise ValueError("exactly nine distinct names are required")
    first = names[0]
    partitions = []
    for companions in combinations(names[1:], 2):
        group1 = frozenset((first, *companions))
        remaining = tuple(name for name in names if name not in group1)
        anchor = remaining[0]
        for companions2 in combinations(remaining[1:], 2):
            group2 = frozenset((anchor, *companions2))
            group3 = frozenset(name for name in remaining if name not in group2)
            partitions.append((group1, group2, group3))
    return tuple(partitions)


def _partition_lookup(groups: Sequence[frozenset[str]]) -> dict[str, int]:
    return {name: index for index, group in enumerate(groups) for name in group}


def header_conditional_gain(
    feature_counts: Mapping[str, Counter[tuple[str, bool, bool]]],
    groups: Sequence[frozenset[str]],
    *,
    alpha: float = 0.5,
) -> float:
    """Leave-one-panel-out log gain of class-conditional over global features."""

    lookup = _partition_lookup(groups)
    names = tuple(feature_counts)
    vocabulary = set().union(*(set(counts) for counts in feature_counts.values()))
    width = len(vocabulary)
    gain = 0.0
    for held_out in names:
        global_counts: Counter[tuple[str, bool, bool]] = Counter()
        class_counts: Counter[tuple[str, bool, bool]] = Counter()
        for name in names:
            if name == held_out:
                continue
            global_counts.update(feature_counts[name])
            if lookup[name] == lookup[held_out]:
                class_counts.update(feature_counts[name])
        global_total = sum(global_counts.values())
        class_total = sum(class_counts.values())
        for feature, count in feature_counts[held_out].items():
            class_probability = (class_counts[feature] + alpha) / (
                class_total + alpha * width
            )
            global_probability = (global_counts[feature] + alpha) / (
                global_total + alpha * width
            )
            gain += count * math.log(class_probability / global_probability)
    return gain


@dataclass(frozen=True)
class HeaderConditionalScore:
    observed_gain: float
    partitions: int
    at_least_observed: int
    best_gain: float
    best_groups: tuple[frozenset[str], ...]

    @property
    def exact_tail(self) -> float:
        return self.at_least_observed / self.partitions


def header_conditional_score(
    bodies: Mapping[str, Sequence[int]], *, alpha: float = 0.5
) -> HeaderConditionalScore:
    depths = deepest_leaf_depths(bodies)
    features = {
        name: invariant_transition_features(body, start=depths[name])
        for name, body in bodies.items()
    }
    observed = header_groups()
    observed_gain = header_conditional_gain(features, observed, alpha=alpha)
    all_partitions = three_by_three_partitions(tuple(bodies))
    scored = tuple(
        (header_conditional_gain(features, partition, alpha=alpha), partition)
        for partition in all_partitions
    )
    best_gain, best = max(scored, key=lambda item: item[0])
    tolerance = 1e-12
    return HeaderConditionalScore(
        observed_gain,
        len(scored),
        sum(gain >= observed_gain - tolerance for gain, _ in scored),
        best_gain,
        best,
    )


def body_streams(streams: Mapping[str, Sequence[int]]) -> dict[str, tuple[int, ...]]:
    return {name: tuple(streams[name][1:]) for name in MESSAGE_ORDER}


def body_row_shapes() -> dict[str, tuple[int, ...]]:
    """Return accepted visual-row lengths after the one-trigram header is removed."""

    return {
        name: (lengths[0] - 1, *lengths[1:])
        for name, lengths in ROW_PAIR_TRIGRAM_LENGTHS.items()
    }
