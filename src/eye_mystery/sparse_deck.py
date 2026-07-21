"""A concrete sparse-deck implementation of symmetric-group GAK.

Each plaintext instruction swaps its selected position with the top, then
performs a fixed non-top transposition assigned to that instruction.  Because
the second swap cannot touch the top, emitting before or after it is
equivalent.  The deck is reset for each message.
"""

from __future__ import annotations

from collections.abc import Sequence


Swap = tuple[int, int]


def no_swap_rules(size: int) -> tuple[Swap, ...]:
    if size < 2:
        raise ValueError("deck must contain at least two cards")
    return ((1, 1),) * size


def _validate_rules(rules: Sequence[Swap]) -> None:
    size = len(rules)
    if size < 2:
        raise ValueError("deck must contain at least two cards")
    if any(
        not 0 < left < size or not 0 < right < size
        for left, right in rules
    ):
        raise ValueError("hidden swaps must use non-top deck positions")


def _validate_rule_sequences(
    rules: Sequence[Sequence[Swap]],
) -> None:
    size = len(rules)
    if size < 2:
        raise ValueError("deck must contain at least two cards")
    if any(
        not 0 < left < size or not 0 < right < size
        for rule in rules
        for left, right in rule
    ):
        raise ValueError("hidden swaps must use non-top deck positions")


def _swap(
    deck: list[int], positions: list[int], left: int, right: int
) -> None:
    if left == right:
        return
    left_card = deck[left]
    right_card = deck[right]
    deck[left], deck[right] = right_card, left_card
    positions[left_card], positions[right_card] = right, left


def decode_sparse_deck(
    ciphertext: Sequence[int], rules: Sequence[Swap]
) -> tuple[int, ...]:
    """Decode one message under fixed plaintext-selected hidden swaps."""

    _validate_rules(rules)
    size = len(rules)
    if any(not 0 <= card < size for card in ciphertext):
        raise ValueError("ciphertext card is outside the deck")
    deck = list(range(size))
    positions = list(range(size))
    plaintext = []
    for card in ciphertext:
        instruction = positions[card]
        plaintext.append(instruction)
        _swap(deck, positions, 0, instruction)
        _swap(deck, positions, *rules[instruction])
    return tuple(plaintext)


def decode_sparse_deck_hidden_sequences(
    ciphertext: Sequence[int], rules: Sequence[Sequence[Swap]]
) -> tuple[int, ...]:
    """Decode with any fixed sequence of non-top swaps per instruction."""

    _validate_rule_sequences(rules)
    size = len(rules)
    if any(not 0 <= card < size for card in ciphertext):
        raise ValueError("ciphertext card is outside the deck")
    deck = list(range(size))
    positions = list(range(size))
    plaintext = []
    for card in ciphertext:
        instruction = positions[card]
        plaintext.append(instruction)
        _swap(deck, positions, 0, instruction)
        for hidden_swap in rules[instruction]:
            _swap(deck, positions, *hidden_swap)
    return tuple(plaintext)


def encrypt_sparse_deck(
    plaintext: Sequence[int], rules: Sequence[Swap]
) -> tuple[int, ...]:
    """Encrypt one message under fixed plaintext-selected hidden swaps."""

    _validate_rules(rules)
    size = len(rules)
    if any(not 0 <= instruction < size for instruction in plaintext):
        raise ValueError("plaintext instruction is outside the deck")
    deck = list(range(size))
    positions = list(range(size))
    ciphertext = []
    for instruction in plaintext:
        _swap(deck, positions, 0, instruction)
        ciphertext.append(deck[0])
        _swap(deck, positions, *rules[instruction])
    return tuple(ciphertext)


def encrypt_sparse_deck_hidden_sequences(
    plaintext: Sequence[int], rules: Sequence[Sequence[Swap]]
) -> tuple[int, ...]:
    """Encrypt with any fixed sequence of non-top swaps per instruction."""

    _validate_rule_sequences(rules)
    size = len(rules)
    if any(not 0 <= instruction < size for instruction in plaintext):
        raise ValueError("plaintext instruction is outside the deck")
    deck = list(range(size))
    positions = list(range(size))
    ciphertext = []
    for instruction in plaintext:
        _swap(deck, positions, 0, instruction)
        ciphertext.append(deck[0])
        for hidden_swap in rules[instruction]:
            _swap(deck, positions, *hidden_swap)
    return tuple(ciphertext)
