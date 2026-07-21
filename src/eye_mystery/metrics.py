"""Small, dependency-free statistics used by the experiments."""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Sequence
from math import log2


def index_of_coincidence(values: Iterable[int], alphabet_size: int | None = None) -> float:
    """Return IoC normalized so uniform data scores approximately 1.0."""
    counts = Counter(values)
    length = sum(counts.values())
    if length < 2:
        return 0.0
    size = alphabet_size or len(counts)
    return size * sum(count * (count - 1) for count in counts.values()) / (length * (length - 1))


def entropy(values: Iterable[int]) -> float:
    counts = Counter(values)
    length = sum(counts.values())
    if not length:
        return 0.0
    return -sum((count / length) * log2(count / length) for count in counts.values())


def adjacent_doubles(messages: Iterable[Sequence[int]]) -> int:
    return sum(
        left == right
        for message in messages
        for left, right in zip(message, message[1:])
    )


def common_prefix_length(left: Sequence[int], right: Sequence[int], start: int = 0) -> int:
    length = 0
    for a, b in zip(left[start:], right[start:]):
        if a != b:
            break
        length += 1
    return length

