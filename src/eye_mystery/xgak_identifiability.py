"""Exact counterexamples for ciphertext-only XGAK action inference."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class XGAKRun:
    """Ciphertext and final deck under one reset XGAK run."""

    ciphertext: tuple[int, ...]
    final_deck: tuple[int, ...]


@dataclass(frozen=True)
class ReconvergenceCounterexample:
    """Two observationally identical keys with different hidden relations."""

    plaintexts: tuple[tuple[int, ...], ...]
    ciphertexts: tuple[tuple[int, ...], ...]
    equal_operations: tuple[tuple[int, ...], ...]
    unequal_operations: tuple[tuple[int, ...], ...]
    output_positions: tuple[int, ...]
    equal_model_finals_equal: bool
    unequal_model_finals_equal: bool


def run_xgak(
    plaintext: Sequence[int],
    operations: Sequence[Sequence[int]],
    output_positions: Sequence[int],
) -> XGAKRun:
    """Run identity-reset XGAK, emitting after each selected permutation."""

    deck_size = len(operations[0])
    if deck_size < 2:
        raise ValueError("deck_size must be at least two")
    if len(operations) != len(output_positions):
        raise ValueError("every operation needs one output position")
    expected = set(range(deck_size))
    if any(set(operation) != expected for operation in operations):
        raise ValueError("operations must be deck permutations")
    if any(not 0 <= position < deck_size for position in output_positions):
        raise ValueError("output position is outside the deck")
    if any(not 0 <= symbol < len(operations) for symbol in plaintext):
        raise ValueError("plaintext symbol is outside the operation alphabet")

    deck = list(range(deck_size))
    ciphertext = []
    for symbol in plaintext:
        operation = operations[symbol]
        deck = [deck[source] for source in operation]
        ciphertext.append(deck[output_positions[symbol]])
    return XGAKRun(tuple(ciphertext), tuple(deck))


def one_swap_reconvergence_counterexample() -> ReconvergenceCounterexample:
    """Return a planted ambiguity using only one hidden transposition.

    Both keys produce the same two ciphertext paths. The paths share a prefix,
    diverge, contain no adjacent doubles, and emit the same final card. Under
    one key their composed actions finish in the same state; under the other
    they do not. The equality of operations A and B also changes.
    """

    deck_size = 6
    identity = tuple(range(deck_size))
    hidden_swap = (0, 1, 2, 3, 5, 4)
    equal_operations = (identity, identity, identity)
    unequal_operations = (hidden_swap, identity, identity)
    output_positions = (1, 2, 3)
    # C A B C A versus C B C B A.
    plaintexts = ((2, 0, 1, 2, 0), (2, 1, 2, 1, 0))

    equal_runs = tuple(
        run_xgak(plaintext, equal_operations, output_positions)
        for plaintext in plaintexts
    )
    unequal_runs = tuple(
        run_xgak(plaintext, unequal_operations, output_positions)
        for plaintext in plaintexts
    )
    equal_ciphertexts = tuple(run.ciphertext for run in equal_runs)
    unequal_ciphertexts = tuple(run.ciphertext for run in unequal_runs)
    if equal_ciphertexts != unequal_ciphertexts:
        raise AssertionError("counterexample keys must be observationally equal")
    return ReconvergenceCounterexample(
        plaintexts,
        equal_ciphertexts,
        equal_operations,
        unequal_operations,
        output_positions,
        equal_runs[0].final_deck == equal_runs[1].final_deck,
        unequal_runs[0].final_deck == unequal_runs[1].final_deck,
    )
