"""Literal source-entry matching for the nine-message prefix tree."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass

from .corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from .prefix_hierarchy import PrefixCluster, prefix_clusters


@dataclass(frozen=True)
class SourceEntry:
    source: str
    text: str


@dataclass(frozen=True)
class MessageTreeMatch:
    entries: tuple[SourceEntry, ...]

    def by_name(self) -> dict[str, SourceEntry]:
        return dict(zip(MESSAGE_ORDER, self.entries, strict=True))


@dataclass(frozen=True)
class MessageTreePartials:
    upper24: tuple[str, ...]
    deep20: tuple[str, ...]
    nested9: tuple[str, ...]
    lower6: tuple[str, ...]
    roots: tuple[tuple[str, str], ...]


def eye_lengths(*, include_markers: bool = False) -> dict[str, int]:
    return {
        name: len(trigram_values(MESSAGES[name])) - (0 if include_markers else 1)
        for name in MESSAGE_ORDER
    }


def message_tree_matches(
    entries: Iterable[SourceEntry],
    *,
    include_markers: bool = False,
    limit: int = 100,
) -> tuple[MessageTreeMatch, ...]:
    """Find exact-length entries realizing the complete observed prefix tree."""

    lengths = eye_lengths(include_markers=include_markers)
    by_length: dict[int, list[SourceEntry]] = defaultdict(list)
    for entry in entries:
        by_length[len(entry.text)].append(entry)
    by_name = {name: by_length[length] for name, length in lengths.items()}

    def index(name: str, prefix_length: int) -> dict[str, list[SourceEntry]]:
        result: dict[str, list[SourceEntry]] = defaultdict(list)
        for entry in by_name[name]:
            result[entry.text[:prefix_length]].append(entry)
        return result

    west1_24 = index("west1", 24)
    east2_24 = index("east2", 24)
    west4_20 = index("west4", 20)
    east5_20 = index("east5", 20)
    east3_9 = index("east3", 9)
    west2_5 = index("west2", 5)
    west3_5 = index("west3", 5)
    matches = []
    expected_clusters = (
        PrefixCluster(MESSAGE_ORDER, 2),
        PrefixCluster(("east1", "west1", "east2"), 24),
        PrefixCluster(
            ("west2", "east3", "west3", "east4", "west4", "east5"),
            5,
        ),
        PrefixCluster(("east3", "east4", "west4", "east5"), 9),
        PrefixCluster(("east4", "west4", "east5"), 20),
    )

    for east1 in by_name["east1"]:
        upper = east1.text[:24]
        upper_pairs = tuple(
            (west1, east2)
            for west1 in west1_24.get(upper, ())
            for east2 in east2_24.get(upper, ())
        )
        for east4 in by_name["east4"]:
            lower20 = east4.text[:20]
            if upper[:2] != lower20[:2] or upper[:3] == lower20[:3]:
                continue
            for west1, east2 in upper_pairs:
                for west4 in west4_20.get(lower20, ()):
                    for east5 in east5_20.get(lower20, ()):
                        lower9 = lower20[:9]
                        for east3 in east3_9.get(lower9, ()):
                            lower5 = lower20[:5]
                            for west2 in west2_5.get(lower5, ()):
                                for west3 in west3_5.get(lower5, ()):
                                    ordered = (
                                        east1,
                                        west1,
                                        east2,
                                        west2,
                                        east3,
                                        west3,
                                        east4,
                                        west4,
                                        east5,
                                    )
                                    streams = {
                                        name: entry.text
                                        for name, entry in zip(
                                            MESSAGE_ORDER, ordered, strict=True
                                        )
                                    }
                                    if prefix_clusters(streams) != expected_clusters:
                                        continue
                                    matches.append(MessageTreeMatch(ordered))
                                    if len(matches) >= limit:
                                        return tuple(matches)
    return tuple(matches)


def message_tree_partials(
    entries: Iterable[SourceEntry], *, include_markers: bool = False
) -> MessageTreePartials:
    """Report increasingly strong exact-length prefix-tree components."""

    lengths = eye_lengths(include_markers=include_markers)
    by_name: dict[str, list[str]] = {name: [] for name in MESSAGE_ORDER}
    length_to_name = {length: name for name, length in lengths.items()}
    for entry in entries:
        name = length_to_name.get(len(entry.text))
        if name is not None:
            by_name[name].append(entry.text)

    def prefixes(name: str, length: int) -> set[str]:
        return {text[:length] for text in by_name[name]}

    upper24 = sorted(
        prefixes("east1", 24)
        & prefixes("west1", 24)
        & prefixes("east2", 24)
    )
    deep20 = sorted(
        prefixes("east4", 20)
        & prefixes("west4", 20)
        & prefixes("east5", 20)
    )
    east3_9 = prefixes("east3", 9)
    west2_5 = prefixes("west2", 5)
    west3_5 = prefixes("west3", 5)
    nested9 = [prefix for prefix in deep20 if prefix[:9] in east3_9]
    lower6 = [
        prefix
        for prefix in nested9
        if prefix[:5] in west2_5 and prefix[:5] in west3_5
    ]
    roots = [
        (upper, lower)
        for upper in upper24
        for lower in lower6
        if upper[:2] == lower[:2] and upper[:3] != lower[:3]
    ]
    return MessageTreePartials(
        tuple(upper24),
        tuple(deep20),
        tuple(nested9),
        tuple(lower6),
        tuple(roots),
    )
