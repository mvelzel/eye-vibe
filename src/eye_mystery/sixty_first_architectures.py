"""Finite `42+41` architecture screens for the Eye corpus."""

from __future__ import annotations

from collections import Counter, deque
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from functools import lru_cache
from itertools import product

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.factoradic_headers import (
    header_ranks,
    inverse,
    lexicographic_unrank,
)
from eye_mystery.header_order_ideal import affine_label_maps
from eye_mystery.ninth_causal import CONTEXT_SPECS


ALPHABET_SIZE = 83
PLAINTEXT_SIZE = 42
GROUPS = 6
PHASES = 7
NONLITERAL_CONTEXTS = CONTEXT_SPECS[6:]
TRAINING_CONTEXTS = NONLITERAL_CONTEXTS[:4]
HOLDOUT_CONTEXTS = NONLITERAL_CONTEXTS[4:]
INCIDENCE_VARIANTS = tuple(
    product(("end-singleton", "start-singleton"), ("header", "inverse-header"))
)
TREE_LAYOUTS = ("breadth-first", "preorder", "inorder", "postorder")


@lru_cache(maxsize=1)
def canonical_streams() -> dict[str, tuple[int, ...]]:
    return {
        name: tuple(trigram_values(MESSAGES[name]))
        for name in MESSAGE_ORDER
    }


def incidence_rank(value: int, endpoint: str) -> int:
    """Quotient 42 cells and 41 dividers under one endpoint convention."""

    if value not in range(ALPHABET_SIZE):
        raise ValueError("value must lie in 0..82")
    if endpoint == "end-singleton":
        return value // 2
    if endpoint == "start-singleton":
        return 0 if value == 0 else 1 + (value - 1) // 2
    raise ValueError(f"unknown endpoint convention {endpoint!r}")


@lru_cache(maxsize=None)
def incidence_table(name: str, endpoint: str, route: str) -> tuple[int, ...]:
    """Apply one message header to the six groups of a `6x7` tape."""

    operation = lexicographic_unrank(header_ranks()[name])
    if route == "inverse-header":
        operation = inverse(operation)
    elif route != "header":
        raise ValueError(f"unknown route {route!r}")
    output = []
    for value in range(ALPHABET_SIZE):
        rank = incidence_rank(value, endpoint)
        group, phase = divmod(rank, PHASES)
        output.append(PHASES * operation[group] + phase)
    return tuple(output)


@dataclass(frozen=True)
class ContextCount:
    name: str
    matches: int
    comparisons: int


@dataclass(frozen=True)
class IncidenceScore:
    endpoint: str
    route: str
    training: tuple[ContextCount, ...]
    holdout: tuple[ContextCount, ...]

    @property
    def training_matches(self) -> int:
        return sum(context.matches for context in self.training)

    @property
    def training_comparisons(self) -> int:
        return sum(context.comparisons for context in self.training)

    @property
    def holdout_matches(self) -> int:
        return sum(context.matches for context in self.holdout)

    @property
    def holdout_comparisons(self) -> int:
        return sum(context.comparisons for context in self.holdout)


def _incidence_contexts(
    specs: Sequence[tuple[str, str, int, str, int, int]],
    streams: Mapping[str, Sequence[int]],
    endpoint: str,
    route: str,
    label_map: Sequence[int],
) -> tuple[ContextCount, ...]:
    results = []
    for context_name, left, left_start, right, right_start, length in specs:
        left_table = incidence_table(left, endpoint, route)
        right_table = incidence_table(right, endpoint, route)
        matches = sum(
            left_table[label_map[streams[left][left_start + offset]]]
            == right_table[label_map[streams[right][right_start + offset]]]
            for offset in range(length)
        )
        results.append(ContextCount(context_name, matches, length))
    return tuple(results)


def incidence_score(
    endpoint: str,
    route: str,
    *,
    label_map: Sequence[int] = tuple(range(ALPHABET_SIZE)),
    streams: Mapping[str, Sequence[int]] | None = None,
) -> IncidenceScore:
    if sorted(label_map) != list(range(ALPHABET_SIZE)):
        raise ValueError("label map must permute 0..82")
    streams = canonical_streams() if streams is None else streams
    return IncidenceScore(
        endpoint,
        route,
        _incidence_contexts(
            TRAINING_CONTEXTS,
            streams,
            endpoint,
            route,
            label_map,
        ),
        _incidence_contexts(
            HOLDOUT_CONTEXTS,
            streams,
            endpoint,
            route,
            label_map,
        ),
    )


def selected_incidence_score(
    *,
    label_map: Sequence[int] = tuple(range(ALPHABET_SIZE)),
    streams: Mapping[str, Sequence[int]] | None = None,
) -> IncidenceScore:
    scores = tuple(
        incidence_score(
            endpoint,
            route,
            label_map=label_map,
            streams=streams,
        )
        for endpoint, route in INCIDENCE_VARIANTS
    )
    return max(
        scores,
        key=lambda score: (
            score.training_matches,
            -INCIDENCE_VARIANTS.index((score.endpoint, score.route)),
        ),
    )


@dataclass(frozen=True)
class IncidenceAudit:
    observed: IncidenceScore
    controls: int
    holdout_tail_count: int
    maximum_control_holdout: int
    holdout_histogram: tuple[tuple[int, int], ...]

    @property
    def holdout_tail(self) -> float:
        return self.holdout_tail_count / self.controls


def audit_incidence_tape() -> IncidenceAudit:
    observed = selected_incidence_score()
    control_scores = tuple(
        selected_incidence_score(label_map=label_map).holdout_matches
        for label_map in affine_label_maps()
    )
    return IncidenceAudit(
        observed,
        len(control_scores),
        sum(value >= observed.holdout_matches for value in control_scores),
        max(control_scores),
        tuple(sorted(Counter(control_scores).items())),
    )


@dataclass(eq=False)
class _TreeNode:
    leaves: int
    left: "_TreeNode | None" = None
    right: "_TreeNode | None" = None

    @property
    def is_leaf(self) -> bool:
        return self.left is None


def _balanced_tree(leaves: int) -> _TreeNode:
    if leaves < 1:
        raise ValueError("a tree must have at least one leaf")
    if leaves == 1:
        return _TreeNode(1)
    left_leaves = leaves // 2
    return _TreeNode(
        leaves,
        _balanced_tree(left_leaves),
        _balanced_tree(leaves - left_leaves),
    )


def _tree_order(root: _TreeNode, layout: str) -> tuple[_TreeNode, ...]:
    if layout == "breadth-first":
        output = []
        pending = deque((root,))
        while pending:
            node = pending.popleft()
            output.append(node)
            if not node.is_leaf:
                assert node.left is not None and node.right is not None
                pending.extend((node.left, node.right))
        return tuple(output)
    if root.is_leaf:
        return (root,)
    assert root.left is not None and root.right is not None
    left = _tree_order(root.left, layout)
    right = _tree_order(root.right, layout)
    if layout == "preorder":
        return (root,) + left + right
    if layout == "inorder":
        return left + (root,) + right
    if layout == "postorder":
        return left + right + (root,)
    raise ValueError(f"unknown tree layout {layout!r}")


@lru_cache(maxsize=None)
def tree_distance_table(layout: str) -> tuple[tuple[int, ...], ...]:
    """Return all-pairs distances under one canonical 83-node numbering."""

    root = _balanced_tree(PLAINTEXT_SIZE)
    order = _tree_order(root, layout)
    if len(order) != ALPHABET_SIZE:
        raise AssertionError("42 leaves must make exactly 83 nodes")
    labels = {node: index for index, node in enumerate(order)}
    adjacency = [set() for _ in range(ALPHABET_SIZE)]

    def connect(node: _TreeNode) -> None:
        if node.is_leaf:
            return
        assert node.left is not None and node.right is not None
        parent = labels[node]
        for child in (node.left, node.right):
            child_label = labels[child]
            adjacency[parent].add(child_label)
            adjacency[child_label].add(parent)
            connect(child)

    connect(root)
    distances = []
    for source in range(ALPHABET_SIZE):
        row = [-1] * ALPHABET_SIZE
        row[source] = 0
        pending = deque((source,))
        while pending:
            node = pending.popleft()
            for target in adjacency[node]:
                if row[target] < 0:
                    row[target] = row[node] + 1
                    pending.append(target)
        if any(value < 0 for value in row):
            raise AssertionError("tree must be connected")
        distances.append(tuple(row))
    return tuple(distances)


@dataclass(frozen=True)
class TreeScore:
    layout: str
    training: tuple[ContextCount, ...]
    holdout: tuple[ContextCount, ...]

    @property
    def training_matches(self) -> int:
        return sum(context.matches for context in self.training)

    @property
    def training_comparisons(self) -> int:
        return sum(context.comparisons for context in self.training)

    @property
    def holdout_matches(self) -> int:
        return sum(context.matches for context in self.holdout)

    @property
    def holdout_comparisons(self) -> int:
        return sum(context.comparisons for context in self.holdout)


def _tree_contexts(
    specs: Sequence[tuple[str, str, int, str, int, int]],
    streams: Mapping[str, Sequence[int]],
    layout: str,
    label_map: Sequence[int],
) -> tuple[ContextCount, ...]:
    distances = tree_distance_table(layout)
    results = []
    for context_name, left, left_start, right, right_start, length in specs:
        comparisons = max(0, length - 1)
        matches = sum(
            distances[
                label_map[streams[left][left_start + offset]]
            ][
                label_map[streams[left][left_start + offset + 1]]
            ]
            == distances[
                label_map[streams[right][right_start + offset]]
            ][
                label_map[streams[right][right_start + offset + 1]]
            ]
            for offset in range(comparisons)
        )
        results.append(ContextCount(context_name, matches, comparisons))
    return tuple(results)


def tree_score(
    layout: str,
    *,
    label_map: Sequence[int] = tuple(range(ALPHABET_SIZE)),
    streams: Mapping[str, Sequence[int]] | None = None,
) -> TreeScore:
    if sorted(label_map) != list(range(ALPHABET_SIZE)):
        raise ValueError("label map must permute 0..82")
    streams = canonical_streams() if streams is None else streams
    return TreeScore(
        layout,
        _tree_contexts(TRAINING_CONTEXTS, streams, layout, label_map),
        _tree_contexts(HOLDOUT_CONTEXTS, streams, layout, label_map),
    )


def selected_tree_score(
    *,
    label_map: Sequence[int] = tuple(range(ALPHABET_SIZE)),
    streams: Mapping[str, Sequence[int]] | None = None,
) -> TreeScore:
    scores = tuple(
        tree_score(layout, label_map=label_map, streams=streams)
        for layout in TREE_LAYOUTS
    )
    return max(
        scores,
        key=lambda score: (
            score.training_matches,
            -TREE_LAYOUTS.index(score.layout),
        ),
    )


@dataclass(frozen=True)
class TreeAudit:
    observed: TreeScore
    controls: int
    holdout_tail_count: int
    maximum_control_holdout: int
    holdout_histogram: tuple[tuple[int, int], ...]

    @property
    def holdout_tail(self) -> float:
        return self.holdout_tail_count / self.controls


def audit_tree_geometry() -> TreeAudit:
    observed = selected_tree_score()
    control_scores = tuple(
        selected_tree_score(label_map=label_map).holdout_matches
        for label_map in affine_label_maps()
    )
    return TreeAudit(
        observed,
        len(control_scores),
        sum(value >= observed.holdout_matches for value in control_scores),
        max(control_scores),
        tuple(sorted(Counter(control_scores).items())),
    )


def root_swap_label_map(layout: str) -> tuple[int, ...]:
    """Return the distance-preserving automorphism swapping root subtrees."""

    root = _balanced_tree(PLAINTEXT_SIZE)
    order = _tree_order(root, layout)
    labels = {node: index for index, node in enumerate(order)}
    mapping: dict[_TreeNode, _TreeNode] = {}

    def pair(left: _TreeNode, right: _TreeNode) -> None:
        if left.leaves != right.leaves:
            raise ValueError("root subtrees are not isomorphic")
        mapping[left] = right
        mapping[right] = left
        if not left.is_leaf:
            assert (
                left.left is not None
                and left.right is not None
                and right.left is not None
                and right.right is not None
            )
            pair(left.left, right.left)
            pair(left.right, right.right)

    mapping[root] = root
    assert root.left is not None and root.right is not None
    pair(root.left, root.right)
    return tuple(labels[mapping[node]] for node in order)


@dataclass(frozen=True)
class PacketSpec:
    size: int
    descending: bool
    side: str
    reverse: bool
    timing: str


PACKET_SPECS = tuple(
    PacketSpec(size, descending, side, reverse, timing)
    for size, descending, side, reverse, timing in product(
        (26, 27, 36, 42),
        (False, True),
        ("prefix", "suffix"),
        (False, True),
        ("before", "after"),
    )
)


def _initial_deck(spec: PacketSpec) -> tuple[int, ...]:
    deck = tuple(range(ALPHABET_SIZE))
    return tuple(reversed(deck)) if spec.descending else deck


def _eligible(deck: Sequence[int], spec: PacketSpec) -> tuple[int, ...]:
    if spec.side == "prefix":
        return tuple(deck[: spec.size])
    if spec.side == "suffix":
        return tuple(deck[-spec.size :])
    raise ValueError(f"unknown packet side {spec.side!r}")


def _move_packet(deck: Sequence[int], spec: PacketSpec) -> tuple[int, ...]:
    if spec.side == "prefix":
        packet = tuple(deck[: spec.size])
        rest = tuple(deck[spec.size :])
        if spec.reverse:
            packet = tuple(reversed(packet))
        return rest + packet
    if spec.side == "suffix":
        packet = tuple(deck[-spec.size :])
        rest = tuple(deck[: -spec.size])
        if spec.reverse:
            packet = tuple(reversed(packet))
        return packet + rest
    raise ValueError(f"unknown packet side {spec.side!r}")


def decode_packet_message(
    ciphertext: Sequence[int],
    spec: PacketSpec,
) -> tuple[int, ...]:
    """Decode until the first card outside the eligible packet."""

    deck = _initial_deck(spec)
    plaintext = []
    for card in ciphertext:
        if spec.timing == "after":
            deck = _move_packet(deck, spec)
        elif spec.timing != "before":
            raise ValueError(f"unknown output timing {spec.timing!r}")
        eligible = _eligible(deck, spec)
        try:
            plaintext.append(eligible.index(card))
        except ValueError:
            break
        if spec.timing == "before":
            deck = _move_packet(deck, spec)
    return tuple(plaintext)


def encode_packet_message(
    plaintext: Sequence[int],
    spec: PacketSpec,
) -> tuple[int, ...]:
    deck = _initial_deck(spec)
    ciphertext = []
    for rank in plaintext:
        if rank not in range(spec.size):
            raise ValueError("plaintext rank lies outside the eligible packet")
        if spec.timing == "after":
            deck = _move_packet(deck, spec)
        elif spec.timing != "before":
            raise ValueError(f"unknown output timing {spec.timing!r}")
        ciphertext.append(_eligible(deck, spec)[rank])
        if spec.timing == "before":
            deck = _move_packet(deck, spec)
    return tuple(ciphertext)


@dataclass(frozen=True)
class PacketScore:
    spec: PacketSpec
    valid_prefixes: tuple[int, ...]
    total_valid: int
    total_events: int

    @property
    def complete(self) -> bool:
        return self.total_valid == self.total_events


def score_packet_spec(
    spec: PacketSpec,
    *,
    streams: Mapping[str, Sequence[int]] | None = None,
) -> PacketScore:
    streams = canonical_streams() if streams is None else streams
    valid = tuple(
        len(decode_packet_message(streams[name], spec))
        for name in MESSAGE_ORDER
    )
    return PacketScore(
        spec,
        valid,
        sum(valid),
        sum(len(streams[name]) for name in MESSAGE_ORDER),
    )


def audit_packet_family() -> tuple[PacketScore, ...]:
    return tuple(
        sorted(
            (score_packet_spec(spec) for spec in PACKET_SPECS),
            key=lambda score: (
                -score.total_valid,
                score.spec.size,
                score.spec.descending,
                score.spec.side,
                score.spec.reverse,
                score.spec.timing,
            ),
        )
    )
