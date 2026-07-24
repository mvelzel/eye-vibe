"""Exact tiny-instance feasibility for ordinary GAK with unknown plaintext.

The model follows the convention used by :mod:`eye_mystery.arbitrary_gak_sat`:

``new_deck[i] = old_deck[operation[plaintext_symbol][i]]``

and emits ``new_deck[0]``.  The reset deck is the identity ordering.  To model
the usual double-ciphertext-free construction, every operation must move a
non-top position to the top, i.e. ``operation[0] != 0``.

This implementation deliberately enumerates operation sets.  It is complete
for tiny decks and useful as a calibration oracle, but it is not presented as
an Eye-scale solver.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from itertools import combinations, permutations
from math import comb, factorial

from .arbitrary_gak_sat import Permutation, apply_operation


@dataclass(frozen=True)
class UnknownGAKWitness:
    """One operation set and one plaintext schedule producing a ciphertext."""

    operations: tuple[Permutation, ...]
    plaintext: tuple[int, ...]


@dataclass(frozen=True)
class UnknownGAKResult:
    """Result of a bounded complete-or-prefix operation-set enumeration."""

    status: str
    witness: UnknownGAKWitness | None
    operation_sets_checked: int
    total_operation_sets: int


def replay_unknown_gak(
    plaintext: Sequence[int],
    operations: Sequence[Sequence[int]],
    *,
    deck_size: int,
) -> tuple[int, ...]:
    """Replay one unknown-plaintext witness from the identity reset deck."""

    deck = tuple(range(deck_size))
    ciphertext = []
    for symbol in plaintext:
        if not 0 <= symbol < len(operations):
            raise ValueError("plaintext symbol is outside the operation set")
        deck = apply_operation(deck, operations[symbol])
        ciphertext.append(deck[0])
    return tuple(ciphertext)


def _candidate_operations(
    deck_size: int, *, require_top_change: bool
) -> tuple[Permutation, ...]:
    candidates = permutations(range(deck_size))
    if require_top_change:
        return tuple(operation for operation in candidates if operation[0] != 0)
    return tuple(candidates)


def top_changing_operation_count(deck_size: int) -> int:
    """Count permutations whose new top card comes from a non-top position."""

    if deck_size < 2:
        raise ValueError("deck_size must be at least two")
    return (deck_size - 1) * factorial(deck_size - 1)


def top_changing_operation_set_count(deck_size: int, alphabet_size: int) -> int:
    """Count unordered decryptable operation sets with distinct top sources."""

    if deck_size < 2:
        raise ValueError("deck_size must be at least two")
    if not 1 <= alphabet_size <= deck_size - 1:
        return 0
    return comb(deck_size - 1, alphabet_size) * (
        factorial(deck_size - 1) ** alphabet_size
    )


def arbitrary_length_no_double_witness(
    length: int, *, deck_size: int
) -> tuple[tuple[int, ...], UnknownGAKWitness]:
    """Construct an ordinary one-operation GAK with no adjacent doubles.

    A one-position rotation has no top fixed point and may be repeated
    indefinitely.  This is a constructive proof that the no-double observation
    alone places no finite capacity bound on an ordinary GAK.
    """

    if length < 0:
        raise ValueError("length must be nonnegative")
    if deck_size < 2:
        raise ValueError("deck_size must be at least two")
    operation = tuple(range(1, deck_size)) + (0,)
    plaintext = (0,) * length
    witness = UnknownGAKWitness((operation,), plaintext)
    ciphertext = replay_unknown_gak(
        plaintext,
        witness.operations,
        deck_size=deck_size,
    )
    if any(left == right for left, right in zip(ciphertext, ciphertext[1:])):
        raise AssertionError("rotation witness unexpectedly produced a double")
    return ciphertext, witness


def recover_unknown_plaintext_bruteforce(
    ciphertext: Sequence[int],
    *,
    deck_size: int,
    operation_alphabet_size: int,
    require_top_change: bool = True,
    require_unique_top_sources: bool = True,
    max_operation_sets: int | None = None,
) -> UnknownGAKResult:
    """Decide a tiny unknown-plaintext GAK instance by exact enumeration.

    Plaintext-symbol names are irrelevant, so operation sets are enumerated as
    unordered combinations.  For a fixed set, dynamic programming retains one
    plaintext prefix for every reachable deck state consistent with the
    observed ciphertext prefix.

    ``unsat`` is returned only after every operation set has been checked.
    When ``max_operation_sets`` truncates the enumeration, failure to find a
    witness is reported as ``unknown``.
    """

    if deck_size < 2:
        raise ValueError("deck_size must be at least two")
    if operation_alphabet_size < 1:
        raise ValueError("operation_alphabet_size must be positive")
    if max_operation_sets is not None and max_operation_sets < 1:
        raise ValueError("max_operation_sets must be positive")
    if any(not 0 <= value < deck_size for value in ciphertext):
        raise ValueError("ciphertext card is outside the deck")

    operations = _candidate_operations(
        deck_size, require_top_change=require_top_change
    )
    if operation_alphabet_size > len(operations):
        return UnknownGAKResult("unsat", None, 0, 0)

    if require_unique_top_sources:
        available_top_sources = deck_size - int(require_top_change)
        if operation_alphabet_size > available_top_sources:
            return UnknownGAKResult("unsat", None, 0, 0)
        total = comb(available_top_sources, operation_alphabet_size) * (
            factorial(deck_size - 1) ** operation_alphabet_size
        )
    else:
        total = comb(len(operations), operation_alphabet_size)
    checked = 0
    for operation_set in combinations(operations, operation_alphabet_size):
        if require_unique_top_sources and len(
            {operation[0] for operation in operation_set}
        ) != len(operation_set):
            continue
        if max_operation_sets is not None and checked >= max_operation_sets:
            return UnknownGAKResult("unknown", None, checked, total)
        checked += 1

        # One schedule is sufficient for each state: future reachability
        # depends only on the deck, not on the path used to reach it.
        states: dict[Permutation, tuple[int, ...]] = {
            tuple(range(deck_size)): ()
        }
        for emitted in ciphertext:
            following: dict[Permutation, tuple[int, ...]] = {}
            for deck, schedule in states.items():
                for symbol, operation in enumerate(operation_set):
                    next_deck = apply_operation(deck, operation)
                    if next_deck[0] == emitted and next_deck not in following:
                        following[next_deck] = (*schedule, symbol)
            states = following
            if not states:
                break

        if states:
            plaintext = next(iter(states.values()))
            witness = UnknownGAKWitness(operation_set, plaintext)
            if replay_unknown_gak(
                witness.plaintext,
                witness.operations,
                deck_size=deck_size,
            ) != tuple(ciphertext):
                raise AssertionError("enumerated GAK witness failed replay")
            return UnknownGAKResult("sat", witness, checked, total)

    return UnknownGAKResult("unsat", None, checked, total)


def minimum_operation_alphabet(
    ciphertext: Sequence[int],
    *,
    deck_size: int,
    maximum: int,
    require_top_change: bool = True,
    require_unique_top_sources: bool = True,
    max_operation_sets: int | None = None,
) -> tuple[int | None, tuple[UnknownGAKResult, ...]]:
    """Return the first feasible operation-alphabet size through ``maximum``."""

    if maximum < 1:
        raise ValueError("maximum must be positive")
    results = []
    for size in range(1, maximum + 1):
        result = recover_unknown_plaintext_bruteforce(
            ciphertext,
            deck_size=deck_size,
            operation_alphabet_size=size,
            require_top_change=require_top_change,
            require_unique_top_sources=require_unique_top_sources,
            max_operation_sets=max_operation_sets,
        )
        results.append(result)
        if result.status == "sat":
            return size, tuple(results)
        if result.status == "unknown":
            break
    return None, tuple(results)
