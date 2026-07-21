"""Initial-order-independent invariants for adaptive deck ciphers."""

from __future__ import annotations

from collections.abc import Sequence


def repeated_working_set_ranks(ciphertext: Sequence[int]) -> tuple[int, ...]:
    """Return forced move-to-front ranks at repeated-symbol occurrences.

    After a card is moved to the front, its rank when it next appears is the
    number of distinct other cards accessed in between.  This does not depend
    on the unknown initial ordering of the deck.
    """
    previous: dict[int, int] = {}
    ranks = []
    for index, symbol in enumerate(ciphertext):
        if symbol in previous:
            ranks.append(len(set(ciphertext[previous[symbol] + 1 : index])))
        previous[symbol] = index
    return tuple(ranks)


def forced_adaptive_rank_count(
    messages: Sequence[Sequence[int]], *, skip_first: bool = False
) -> int:
    """Lower-bound the instruction alphabet for move-to-front/back ciphers."""
    ranks = {
        rank
        for message in messages
        for rank in repeated_working_set_ranks(message[1:] if skip_first else message)
    }
    return len(ranks)
