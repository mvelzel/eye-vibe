"""Discover the nested common-prefix structure of the nine Eye messages."""

from __future__ import annotations

from collections import defaultdict
from collections import deque
from collections.abc import Mapping, Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class PrefixCluster:
    members: tuple[str, ...]
    length: int


def _common_length(
    members: Sequence[str], streams: Mapping[str, Sequence[int]], start: int
) -> int:
    limit = min(len(streams[name]) for name in members) - start
    length = 0
    while length < limit:
        values = {streams[name][start + length] for name in members}
        if len(values) != 1:
            break
        length += 1
    return length


def prefix_clusters(
    streams: Mapping[str, Sequence[int]], *, start: int = 0
) -> tuple[PrefixCluster, ...]:
    """Return every non-singleton internal node in the prefix trie."""

    if len(streams) < 2:
        return ()
    order = tuple(streams)
    result: list[PrefixCluster] = []

    def visit(members: tuple[str, ...], depth: int) -> None:
        shared = _common_length(members, streams, start + depth)
        total = depth + shared
        result.append(PrefixCluster(members, total))
        groups: dict[int | None, list[str]] = defaultdict(list)
        for name in members:
            index = start + total
            value = streams[name][index] if index < len(streams[name]) else None
            groups[value].append(name)
        for group in groups.values():
            if len(group) >= 2 and len(group) < len(members):
                visit(tuple(group), total)

    visit(order, 0)
    return tuple(result)


def breadth_first_prefix_clusters(
    streams: Mapping[str, Sequence[int]], *, start: int = 0
) -> tuple[PrefixCluster, ...]:
    """Return trie nodes breadth-first, preserving input order among siblings."""

    if len(streams) < 2:
        return ()
    queue = deque([(tuple(streams), 0)])
    result: list[PrefixCluster] = []
    while queue:
        members, depth = queue.popleft()
        total = depth + _common_length(members, streams, start + depth)
        result.append(PrefixCluster(members, total))
        groups: dict[int | None, list[str]] = defaultdict(list)
        for name in members:
            index = start + total
            value = streams[name][index] if index < len(streams[name]) else None
            groups[value].append(name)
        for group in groups.values():
            if len(group) >= 2 and len(group) < len(members):
                queue.append((tuple(group), total))
    return tuple(result)


def leaf_exit_labels(
    streams: Mapping[str, Sequence[int]], *, start: int = 0
) -> dict[str, int]:
    """Return the first edge that leaves the deepest shared-prefix cluster.

    The result is one structurally selected label per stream: the label that
    first makes that leaf unique within the compressed prefix tree.
    """

    clusters = prefix_clusters(streams, start=start)
    result = {}
    for name, stream in streams.items():
        containing = [cluster for cluster in clusters if name in cluster.members]
        depth = max((cluster.length for cluster in containing), default=0)
        index = start + depth
        if index >= len(stream):
            raise ValueError(f"stream {name!r} ends at an internal trie node")
        result[name] = stream[index]
    return result


def serialize_trie_edges(
    streams: Mapping[str, Sequence[int]],
    order: Sequence[str],
    *,
    start: int = 0,
    breadth_first: bool,
) -> tuple[int, ...]:
    """Emit every distinct edge of a collection's prefix trie exactly once.

    ``order`` does not change which edges are emitted; it fixes the order of
    sibling branches.  This makes the otherwise branching Eye-message trie
    reproducibly serializable for tests inspired by Cessation's fragment
    merging step.
    """

    if set(order) != set(streams) or len(order) != len(streams):
        raise ValueError("order must contain every stream name exactly once")
    rank = {name: index for index, name in enumerate(order)}
    root: dict[str, object] = {"children": {}, "members": set()}
    for name, stream in streams.items():
        node = root
        node["members"].add(name)  # type: ignore[union-attr]
        for value in stream[start:]:
            children = node["children"]  # type: ignore[assignment]
            if value not in children:
                children[value] = {"children": {}, "members": set()}
            node = children[value]
            node["members"].add(name)

    def sorted_children(node: dict[str, object]):
        children = node["children"]
        return sorted(
            children.items(),
            key=lambda item: min(rank[name] for name in item[1]["members"]),
        )

    output: list[int] = []
    if breadth_first:
        queue = deque([root])
        while queue:
            node = queue.popleft()
            for value, child in sorted_children(node):
                output.append(value)
                queue.append(child)
    else:

        def visit(node: dict[str, object]) -> None:
            for value, child in sorted_children(node):
                output.append(value)
                visit(child)

        visit(root)
    return tuple(output)
