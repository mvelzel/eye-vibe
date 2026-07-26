"""Exact visible-state permutation-action screen for the Eye corpus.

If the current visible value is the complete cipher state, every plaintext
action induces a permutation of the 83 values.  Observed transitions can then
share an action precisely when their edges coexist in one partial permutation.
Repeated-plaintext contexts additionally force aligned transitions to use the
same action.
"""

from __future__ import annotations

import math
from collections import Counter, defaultdict
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.ninth_causal import CONTEXT_SPECS


Event = tuple[str, int]
Context = tuple[str, int, str, int, int]


class _UnionFind:
    def __init__(self, values: Sequence[Event]) -> None:
        self.parent = {value: value for value in values}

    def find(self, value: Event) -> Event:
        parent = self.parent[value]
        if parent != value:
            self.parent[value] = self.find(parent)
        return self.parent[value]

    def union(self, left: Event, right: Event) -> None:
        left_root = self.find(left)
        right_root = self.find(right)
        if left_root != right_root:
            self.parent[right_root] = left_root


@dataclass(frozen=True)
class VisibleActionAudit:
    transition_events: int
    unique_edges: int
    repeated_edge_events: int
    maximum_edge_multiplicity: int
    maximum_distinct_outdegree: int
    maximum_distinct_indegree: int
    effective_uniform_choices: float
    expected_unique_edges_26: float
    expected_unique_edges_42: float
    event_classes: int
    aligned_classes: int
    internally_conflicting_classes: int
    conflict_pairs: int
    lower_bound: int
    constructed_actions: int
    exact_minimum: bool
    color_by_event: Mapping[Event, int]


@dataclass(frozen=True)
class PivotFreedomAudit:
    """Local freedom after naming actions at a maximum-degree source."""

    pivot_source: int
    pivot_targets: tuple[int, ...]
    anchored_classes: int
    nonanchor_classes: int
    one_step_mutable_nonanchors: int
    forced_nonanchors: int
    minimum_available_colors_nonanchor: int
    maximum_available_colors_nonanchor: int
    available_color_histogram: tuple[tuple[int, int], ...]


def canonical_streams() -> dict[str, tuple[int, ...]]:
    """Return the nine accepted body streams with metadata markers removed."""
    return {
        name: trigram_values(MESSAGES[name])[1:]
        for name in MESSAGE_ORDER
    }


def canonical_full_streams() -> dict[str, tuple[int, ...]]:
    """Return the accepted streams including each metadata marker."""
    return {
        name: trigram_values(MESSAGES[name])
        for name in MESSAGE_ORDER
    }


def canonical_contexts() -> tuple[Context, ...]:
    """Return the seven registered nonliteral body contexts."""
    return tuple(
        (left, left_start, right, right_start, length)
        for (
            _name,
            left,
            left_start,
            right,
            right_start,
            length,
        ) in CONTEXT_SPECS[6:]
    )


def canonical_full_contexts() -> tuple[Context, ...]:
    """Return the nonliteral contexts in marker-inclusive coordinates."""
    return tuple(
        (left, left_start + 1, right, right_start + 1, length)
        for left, left_start, right, right_start, length in canonical_contexts()
    )


def _events(streams: Mapping[str, Sequence[int]]) -> tuple[Event, ...]:
    return tuple(
        (name, index)
        for name, stream in streams.items()
        for index in range(len(stream) - 1)
    )


def _effective_choices(visits: Counter[int], target: int) -> float:
    def expected(choices: float) -> float:
        return sum(
            choices * (1 - (1 - 1 / choices) ** count)
            for count in visits.values()
        )

    low = 1.000001
    high = 82.0
    if target == sum(visits.values()):
        return math.inf
    while expected(high) < target and high < 1e12:
        high *= 2
    if not expected(low) <= target <= expected(high):
        raise ValueError("target edge count is outside the uniform-choice range")
    for _ in range(100):
        middle = (low + high) / 2
        if expected(middle) < target:
            low = middle
        else:
            high = middle
    return (low + high) / 2


def _expected_unique(visits: Counter[int], choices: int) -> float:
    return sum(
        choices * (1 - (1 - 1 / choices) ** count)
        for count in visits.values()
    )


def _action_classes(
    streams: Mapping[str, Sequence[int]],
    contexts: Sequence[Context],
) -> tuple[
    tuple[Event, ...],
    dict[Event, int],
    tuple[tuple[tuple[int, int], ...], ...],
]:
    events = _events(streams)
    union_find = _UnionFind(events)
    for left, left_start, right, right_start, length in contexts:
        if left_start + length > len(streams[left]):
            raise ValueError("left context exceeds its stream")
        if right_start + length > len(streams[right]):
            raise ValueError("right context exceeds its stream")
        for offset in range(length - 1):
            union_find.union(
                (left, left_start + offset),
                (right, right_start + offset),
            )

    roots = sorted({union_find.find(event) for event in events})
    class_by_root = {root: index for index, root in enumerate(roots)}
    class_by_event = {
        event: class_by_root[union_find.find(event)]
        for event in events
    }
    edges_by_class: list[list[tuple[int, int]]] = [
        [] for _ in roots
    ]
    for name, index in events:
        edge = (streams[name][index], streams[name][index + 1])
        edges_by_class[class_by_event[(name, index)]].append(edge)
    return (
        events,
        class_by_event,
        tuple(tuple(edges) for edges in edges_by_class),
    )


def _conflict_graph(
    edges_by_class: Sequence[Sequence[tuple[int, int]]],
) -> tuple[tuple[frozenset[int], ...], int]:
    by_source: dict[int, dict[int, set[int]]] = defaultdict(
        lambda: defaultdict(set)
    )
    by_target: dict[int, dict[int, set[int]]] = defaultdict(
        lambda: defaultdict(set)
    )
    internal_conflicts = 0
    for class_index, edges in enumerate(edges_by_class):
        forward: dict[int, int] = {}
        reverse: dict[int, int] = {}
        conflict = False
        for source, target in edges:
            if source in forward and forward[source] != target:
                conflict = True
            if target in reverse and reverse[target] != source:
                conflict = True
            forward[source] = target
            reverse[target] = source
            by_source[source][target].add(class_index)
            by_target[target][source].add(class_index)
        internal_conflicts += conflict

    conflicts: set[tuple[int, int]] = set()
    for grouped in (by_source, by_target):
        for value_groups in grouped.values():
            groups = tuple(value_groups.values())
            for left_index, left in enumerate(groups):
                for right in groups[left_index + 1 :]:
                    conflicts.update(
                        (min(a, b), max(a, b))
                        for a in left
                        for b in right
                        if a != b
                    )

    adjacency = [set() for _ in edges_by_class]
    for left, right in conflicts:
        adjacency[left].add(right)
        adjacency[right].add(left)
    return tuple(frozenset(neighbors) for neighbors in adjacency), internal_conflicts


def _dsatur(adjacency: Sequence[frozenset[int]]) -> tuple[int, ...]:
    colors: dict[int, int] = {}
    saturation = [set() for _ in adjacency]
    uncolored = set(range(len(adjacency)))
    while uncolored:
        vertex = max(
            uncolored,
            key=lambda value: (
                len(saturation[value]),
                len(adjacency[value]),
                -value,
            ),
        )
        used = {
            colors[neighbor]
            for neighbor in adjacency[vertex]
            if neighbor in colors
        }
        color = 0
        while color in used:
            color += 1
        colors[vertex] = color
        uncolored.remove(vertex)
        for neighbor in adjacency[vertex]:
            if neighbor in uncolored:
                saturation[neighbor].add(color)
    return tuple(colors[index] for index in range(len(adjacency)))


def audit_visible_actions(
    streams: Mapping[str, Sequence[int]] | None = None,
    contexts: Sequence[Context] | None = None,
) -> VisibleActionAudit:
    """Construct and validate the minimum action cover when the bounds meet."""
    if streams is None:
        streams = canonical_streams()
    if contexts is None:
        contexts = canonical_contexts()

    events, class_by_event, edges_by_class = _action_classes(streams, contexts)
    adjacency, internal_conflicts = _conflict_graph(edges_by_class)
    class_colors = _dsatur(adjacency)
    constructed_actions = max(class_colors, default=-1) + 1

    edges = [
        (streams[name][index], streams[name][index + 1])
        for name, index in events
    ]
    edge_counts = Counter(edges)
    outgoing: dict[int, set[int]] = defaultdict(set)
    incoming: dict[int, set[int]] = defaultdict(set)
    visits: Counter[int] = Counter()
    for source, target in edges:
        outgoing[source].add(target)
        incoming[target].add(source)
        visits[source] += 1
    lower_bound = max(
        max(map(len, outgoing.values()), default=0),
        max(map(len, incoming.values()), default=0),
    )

    color_by_event = {
        event: class_colors[class_index]
        for event, class_index in class_by_event.items()
    }
    unique_edges = len(edge_counts)
    return VisibleActionAudit(
        transition_events=len(events),
        unique_edges=unique_edges,
        repeated_edge_events=len(events) - unique_edges,
        maximum_edge_multiplicity=max(edge_counts.values(), default=0),
        maximum_distinct_outdegree=max(map(len, outgoing.values()), default=0),
        maximum_distinct_indegree=max(map(len, incoming.values()), default=0),
        effective_uniform_choices=_effective_choices(visits, unique_edges),
        expected_unique_edges_26=_expected_unique(visits, 26),
        expected_unique_edges_42=_expected_unique(visits, 42),
        event_classes=len(edges_by_class),
        aligned_classes=sum(len(edges) > 1 for edges in edges_by_class),
        internally_conflicting_classes=internal_conflicts,
        conflict_pairs=sum(map(len, adjacency)) // 2,
        lower_bound=lower_bound,
        constructed_actions=constructed_actions,
        exact_minimum=internal_conflicts == 0
        and constructed_actions == lower_bound,
        color_by_event=color_by_event,
    )


def audit_pivot_freedom(
    streams: Mapping[str, Sequence[int]] | None = None,
    contexts: Sequence[Context] | None = None,
) -> PivotFreedomAudit:
    """Measure exact one-vertex recoloring freedom after fixing action names.

    A source with one distinct target per action makes its outgoing classes a
    maximum clique.  Naming those targets fixes the otherwise arbitrary action
    labels.  If another class can then change color while every other class is
    held fixed, that class is certainly not part of a coloring backbone.
    """
    if streams is None:
        streams = canonical_streams()
    if contexts is None:
        contexts = canonical_contexts()

    _events_value, _class_by_event, edges_by_class = _action_classes(
        streams,
        contexts,
    )
    adjacency, internal_conflicts = _conflict_graph(edges_by_class)
    class_colors = _dsatur(adjacency)
    action_count = max(class_colors, default=-1) + 1
    if internal_conflicts:
        raise ValueError("aligned event classes contain an internal conflict")

    outgoing: dict[int, set[int]] = defaultdict(set)
    for stream in streams.values():
        for source, target in zip(stream, stream[1:]):
            outgoing[source].add(target)
    pivot_sources = tuple(
        source
        for source, targets in outgoing.items()
        if len(targets) == action_count
    )
    if len(pivot_sources) != 1:
        raise ValueError("there is not exactly one maximum-outdegree pivot")
    pivot_source = pivot_sources[0]

    target_to_class: dict[int, int] = {}
    for class_index, edges in enumerate(edges_by_class):
        for source, target in edges:
            if source != pivot_source:
                continue
            previous = target_to_class.setdefault(target, class_index)
            if previous != class_index:
                raise ValueError("one pivot edge occurs in multiple classes")
    pivot_targets = tuple(sorted(target_to_class))
    if len(pivot_targets) != action_count:
        raise ValueError("the pivot does not expose every action")

    anchor_by_class = {
        target_to_class[target]: color
        for color, target in enumerate(pivot_targets)
    }
    old_to_anchored = {
        class_colors[class_index]: color
        for class_index, color in anchor_by_class.items()
    }
    if len(old_to_anchored) != action_count:
        raise ValueError("the constructed coloring does not separate the pivot")
    anchored_colors = tuple(
        old_to_anchored[color]
        for color in class_colors
    )

    available_counts = []
    mutable = 0
    for class_index, neighbors in enumerate(adjacency):
        if class_index in anchor_by_class:
            continue
        neighbor_colors = {
            anchored_colors[neighbor]
            for neighbor in neighbors
        }
        available = set(range(action_count)) - neighbor_colors
        if anchored_colors[class_index] not in available:
            raise AssertionError("constructed coloring is invalid")
        available_counts.append(len(available))
        if len(available) > 1:
            mutable += 1

    histogram = Counter(available_counts)
    nonanchors = len(adjacency) - len(anchor_by_class)
    return PivotFreedomAudit(
        pivot_source=pivot_source,
        pivot_targets=pivot_targets,
        anchored_classes=len(anchor_by_class),
        nonanchor_classes=nonanchors,
        one_step_mutable_nonanchors=mutable,
        forced_nonanchors=nonanchors - mutable,
        minimum_available_colors_nonanchor=min(available_counts, default=0),
        maximum_available_colors_nonanchor=max(available_counts, default=0),
        available_color_histogram=tuple(sorted(histogram.items())),
    )
