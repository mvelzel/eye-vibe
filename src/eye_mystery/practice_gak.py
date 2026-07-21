"""Small exact models for controlled group-autokey/deck practice puzzles."""

from collections.abc import Iterable, Sequence


def mongean_shuffle(deck: Sequence[int]) -> tuple[int, ...]:
    """Draw from the top, alternately placing cards atop and under a new stack."""
    shuffled: list[int] = []
    for index, card in enumerate(deck):
        if index % 2:
            shuffled.append(card)
        else:
            shuffled.insert(0, card)
    return tuple(shuffled)


def mongean_cut_step(deck: Sequence[int], cut: int) -> tuple[int, ...]:
    """Apply one Mongean shuffle followed by a top-to-bottom cut."""
    if not 0 <= cut <= len(deck):
        raise ValueError("cut must fall within the deck")
    shuffled = mongean_shuffle(deck)
    return shuffled[cut:] + shuffled[:cut]


def encrypt_mongean_cuts(
    cuts: Iterable[int], *, deck_size: int = 83
) -> tuple[int, ...]:
    """Emit the top card after every Mongean-and-cut state update."""
    deck = tuple(range(deck_size))
    ciphertext: list[int] = []
    for cut in cuts:
        deck = mongean_cut_step(deck, cut)
        ciphertext.append(deck[0])
    return tuple(ciphertext)


def recover_mongean_cuts(
    ciphertext: Iterable[int],
    *,
    candidate_cuts: Iterable[int] = range(1, 27),
    deck_size: int = 83,
) -> tuple[tuple[int, ...], ...]:
    """Recover all locally possible cuts, requiring a unique state path.

    A tuple is returned for every ciphertext position so ambiguity remains
    explicit.  State propagation stops if a position has anything other than
    one candidate because the next deck would otherwise branch.
    """
    candidates = tuple(candidate_cuts)
    deck = tuple(range(deck_size))
    recovered: list[tuple[int, ...]] = []
    for output in ciphertext:
        shuffled = mongean_shuffle(deck)
        matches = tuple(cut for cut in candidates if shuffled[cut % deck_size] == output)
        recovered.append(matches)
        if len(matches) != 1:
            break
        cut = matches[0] % deck_size
        deck = shuffled[cut:] + shuffled[:cut]
    return tuple(recovered)
