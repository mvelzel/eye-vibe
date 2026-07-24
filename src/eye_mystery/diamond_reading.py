"""Reproduce defektu's desert-glyph "Diamond Readings" transforms.

The construction consumes accepted Eye trigrams in pairs.  The first trigram
supplies ``y`` components in order 021, the second supplies ``x`` components
in order 120, and an all-zero second trigram pads odd-length messages.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Sequence
from itertools import permutations


Trig = tuple[int, int, int]

Y_ORDER = (0, 2, 1)
X_ORDER = (1, 2, 0)
COMPONENT_ORDERS = tuple(permutations(range(3)))


def pair_trigrams(message: Sequence[int]) -> tuple[tuple[Trig, Trig], ...]:
    """Return the document's ``(y, x)`` trigram pairs with zero padding."""

    if len(message) % 3:
        raise ValueError("eye stream length must be divisible by three")
    trigrams = [
        tuple(message[start : start + 3]) for start in range(0, len(message), 3)
    ]
    if len(trigrams) % 2:
        trigrams.append((0, 0, 0))
    return tuple(zip(trigrams[::2], trigrams[1::2], strict=True))


def component_pairs(
    message: Sequence[int],
    *,
    x_order: Trig = X_ORDER,
    y_order: Trig = Y_ORDER,
) -> tuple[tuple[int, int], ...]:
    """Return the three aligned ``(x, y)`` pairs from every trigram pair."""

    result = []
    for y_trigram, x_trigram in pair_trigrams(message):
        result.extend(
            (x_trigram[x_index], y_trigram[y_index])
            for x_index, y_index in zip(x_order, y_order, strict=True)
        )
    return tuple(result)


def base25_reading(
    message: Sequence[int],
    *,
    x_order: Trig = X_ORDER,
    y_order: Trig = Y_ORDER,
) -> tuple[int, ...]:
    """Apply Method 1, ``5*x + y``."""

    return tuple(
        5 * x + y
        for x, y in component_pairs(
            message,
            x_order=x_order,
            y_order=y_order,
        )
    )


def squared_reading(
    message: Sequence[int],
    *,
    x_order: Trig = X_ORDER,
    y_order: Trig = Y_ORDER,
) -> tuple[int, ...]:
    """Apply Method 2, ``x**2 + y``."""

    return tuple(
        x * x + y
        for x, y in component_pairs(
            message,
            x_order=x_order,
            y_order=y_order,
        )
    )


def collision_pairs(values: Sequence[int]) -> int:
    """Return the ordered equal-symbol pair count used in the Phi IoC."""

    return sum(count * (count - 1) for count in Counter(values).values())


def index_of_coincidence(values: Sequence[int]) -> float:
    """Return the unnormalised index of coincidence."""

    if len(values) < 2:
        raise ValueError("IoC requires at least two symbols")
    return collision_pairs(values) / (len(values) * (len(values) - 1))


def uniform_pair_baseline(transform: str) -> float:
    """Return exact IoC for 25 equiprobable input pairs under a transform."""

    if transform == "base25":
        values = [5 * x + y for x in range(5) for y in range(5)]
    elif transform == "squared":
        values = [x * x + y for x in range(5) for y in range(5)]
    else:
        raise ValueError(f"unknown transform {transform!r}")
    counts = Counter(values)
    return sum((count / 25) ** 2 for count in counts.values())


def shuffled_x_pairs(
    message: Sequence[int],
    permutation: Sequence[int],
) -> tuple[tuple[Trig, Trig], ...]:
    """Reassociate real x trigrams while keeping an authored zero pad fixed."""

    pairs = pair_trigrams(message)
    y_trigrams = tuple(y for y, _ in pairs)
    x_trigrams = tuple(x for _, x in pairs)
    real_count = len(message) // 6
    if sorted(permutation) != list(range(real_count)):
        raise ValueError("permutation must cover every real x trigram once")
    shuffled = tuple(x_trigrams[index] for index in permutation)
    if len(x_trigrams) > real_count:
        shuffled += (x_trigrams[-1],)
    return tuple(zip(y_trigrams, shuffled, strict=True))


def squared_from_pairs(
    pairs: Sequence[tuple[Trig, Trig]],
    *,
    relative_order: Trig,
) -> tuple[int, ...]:
    """Score a relative x-to-y component alignment on prepared pairs."""

    return tuple(
        x_trigram[x_index] ** 2 + y_trigram[y_index]
        for y_trigram, x_trigram in pairs
        for y_index, x_index in enumerate(relative_order)
    )
