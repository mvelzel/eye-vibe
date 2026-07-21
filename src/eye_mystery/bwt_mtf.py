"""Exact audit of a raw-eye move-to-front plus BWT interpretation."""

from __future__ import annotations

from itertools import permutations

from .corpus import MESSAGE_ORDER, MESSAGES
from .marker_bwt import cyclic_bwt, inverse_cyclic_bwt


def inverse_move_to_front(
    ranks: tuple[int, ...], initial: tuple[int, ...]
) -> tuple[int, ...]:
    """Decode move-to-front ranks using an explicit initial list."""

    deck = list(initial)
    output = []
    for rank in ranks:
        if rank not in range(len(deck)):
            raise ValueError("move-to-front rank is outside the initial list")
        symbol = deck.pop(rank)
        output.append(symbol)
        deck.insert(0, symbol)
    return tuple(output)


def raw_eye_bwt_mtf_audit() -> dict[str, object]:
    """Exhaust natural five-symbol MTF lists and marker primary rows.

    Each body is interpreted at the individual-eye level: its values ``0..4``
    are inverse-MTF decoded, and the result is treated as a cyclic BWT last
    column.  All 120 initial lists, six marker digit orders, and zero/one-index
    adjustments are checked.  A candidate only advances to the next message
    after an exact BWT round trip.
    """

    histogram: dict[int, int] = {}
    complete = []
    for initial in permutations(range(5)):
        last_columns = {
            name: inverse_move_to_front(MESSAGES[name][3:], initial)
            for name in MESSAGE_ORDER
        }
        for marker_order in permutations(range(3)):
            for adjustment in (-1, 0, 1):
                roundtrips = 0
                for name in MESSAGE_ORDER:
                    marker = MESSAGES[name][:3]
                    primary = (
                        25 * marker[marker_order[0]]
                        + 5 * marker[marker_order[1]]
                        + marker[marker_order[2]]
                        + adjustment
                    )
                    last_column = last_columns[name]
                    if primary not in range(len(last_column)):
                        break
                    plaintext = inverse_cyclic_bwt(last_column, primary)
                    if cyclic_bwt(plaintext) != (last_column, primary):
                        break
                    roundtrips += 1
                histogram[roundtrips] = histogram.get(roundtrips, 0) + 1
                if roundtrips == len(MESSAGE_ORDER):
                    complete.append((initial, marker_order, adjustment))
    return {
        "candidates": 120 * 6 * 3,
        "maximum_roundtrips": max(histogram),
        "histogram": tuple(sorted(histogram.items())),
        "complete": tuple(complete),
    }
