"""Gap-pattern extraction for causal-isomorph analysis."""

from __future__ import annotations

from collections import Counter, defaultdict
from collections.abc import Sequence
from math import log10


def pattern(sequence: Sequence[int]) -> str:
    counts = Counter(sequence)
    labels = {}
    result = []
    for value in sequence:
        if counts[value] < 2:
            result.append(".")
        else:
            if value not in labels:
                labels[value] = chr(ord("A") + len(labels))
            result.append(labels[value])
    return "".join(result)


def repeated_patterns(
    messages: Sequence[Sequence[int]], max_length: int = 41
) -> dict[str, tuple[tuple[int, int], ...]]:
    occurrences: dict[str, list[tuple[int, int]]] = defaultdict(list)
    for length in range(2, max_length + 1):
        for message_index, message in enumerate(messages):
            for position in range(len(message) - length + 1):
                candidate = pattern(message[position : position + length])
                internal_repeats = len(candidate.replace(".", "")) - len(set(candidate) - {"."})
                if internal_repeats >= 2:
                    occurrences[candidate].append((message_index, position))
    return {
        candidate: tuple(positions)
        for candidate, positions in occurrences.items()
        if len(positions) >= 2
    }


def score(candidate: str, instances: int, alphabet_size: int = 83) -> float:
    """Negative log10 random probability used by the public viewer."""
    symbols = set(candidate) - {"."}
    internal_repeats = len(candidate.replace(".", "")) - len(symbols)
    return instances * internal_repeats * log10(alphabet_size)
