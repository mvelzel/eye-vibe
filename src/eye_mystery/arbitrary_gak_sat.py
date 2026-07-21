"""Known-plaintext recovery for a small arbitrary-permutation deck cipher.

The ordinary GAK convention used here is::

    new_deck[i] = old_deck[operation[plaintext_symbol][i]]
    ciphertext = new_deck[0]

Every message resets to the same initial deck.  The solver is intentionally a
calibration tool: arbitrary permutations can admit many witness keys, so a SAT
result proves feasibility, not uniqueness or plaintext recovery.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass


Permutation = tuple[int, ...]


@dataclass(frozen=True)
class GAKWitness:
    """One exact key recovered for the observed plaintext alphabet."""

    initial_deck: Permutation
    operations: tuple[Permutation, ...]


def apply_operation(deck: Sequence[int], operation: Sequence[int]) -> Permutation:
    """Apply a position permutation on the right."""

    if len(deck) != len(operation):
        raise ValueError("deck and operation sizes differ")
    return tuple(deck[position] for position in operation)


def encrypt_messages(
    plaintexts: Sequence[Sequence[int]],
    initial_deck: Sequence[int],
    operations: Sequence[Sequence[int]],
) -> tuple[Permutation, ...]:
    """Encrypt messages from a common reset deck and emit the top card."""

    size = len(initial_deck)
    if sorted(initial_deck) != list(range(size)):
        raise ValueError("initial deck is not a permutation")
    if any(sorted(operation) != list(range(size)) for operation in operations):
        raise ValueError("every operation must be a deck permutation")

    ciphertexts: list[Permutation] = []
    for plaintext in plaintexts:
        deck = tuple(initial_deck)
        ciphertext: list[int] = []
        for symbol in plaintext:
            if not 0 <= symbol < len(operations):
                raise ValueError("plaintext symbol is outside the operation alphabet")
            deck = apply_operation(deck, operations[symbol])
            ciphertext.append(deck[0])
        ciphertexts.append(tuple(ciphertext))
    return tuple(ciphertexts)


def _canonical_initial_deck(size: int, top_card: int) -> Permutation:
    """Choose one representative under position relabelling that fixes top.

    A simultaneous conjugation of both operations can permute all non-top
    positions without changing any emitted card.  For a fixed initial top
    card, placing the other cards in sorted order removes that irrelevant
    ``(size - 1)!`` symmetry.
    """

    if not 0 <= top_card < size:
        raise ValueError("initial top card is outside the deck")
    remainder = tuple(card for card in range(size) if card != top_card)
    return (top_card, *remainder)


def recover_known_plaintext_witness(
    plaintexts: Sequence[Sequence[int]],
    ciphertexts: Sequence[Sequence[int]],
    *,
    deck_size: int,
    plaintext_alphabet_size: int,
    initial_top_card: int,
    timeout_ms: int = 30_000,
) -> tuple[str, GAKWitness | None]:
    """Recover one arbitrary-permutation witness with Z3.

    ``initial_top_card`` selects a canonical representative of the otherwise
    position-conjugate reset states.  Callers may enumerate all deck labels if
    it is unknown.  The returned status is ``sat``, ``unsat``, or ``unknown``.
    Z3 is imported lazily so the rest of the project does not depend on it.
    """

    try:
        import z3  # type: ignore[import-not-found]
    except ImportError as error:  # pragma: no cover - environment dependent
        raise RuntimeError("recover_known_plaintext_witness requires z3-solver") from error

    if len(plaintexts) != len(ciphertexts):
        raise ValueError("plaintext and ciphertext message counts differ")
    if any(len(plain) != len(cipher) for plain, cipher in zip(plaintexts, ciphertexts, strict=True)):
        raise ValueError("plaintext and ciphertext lengths differ")
    if deck_size < 2 or plaintext_alphabet_size < 1:
        raise ValueError("alphabet sizes must be positive")
    if any(not 0 <= value < deck_size for cipher in ciphertexts for value in cipher):
        raise ValueError("ciphertext card is outside the deck")
    if any(
        not 0 <= value < plaintext_alphabet_size
        for plaintext in plaintexts
        for value in plaintext
    ):
        raise ValueError("plaintext symbol is outside the operation alphabet")

    solver = z3.Solver()
    solver.set(timeout=timeout_ms)
    # The extra representable value is needed for the strict upper bound when
    # ``deck_size`` itself is a power of two.
    width = max(1, deck_size.bit_length())
    operations = [
        [z3.BitVec(f"p_{symbol}_{position}", width) for position in range(deck_size)]
        for symbol in range(plaintext_alphabet_size)
    ]
    for operation in operations:
        solver.add(z3.Distinct(operation))
        solver.add(
            *(z3.ULT(value, z3.BitVecVal(deck_size, width)) for value in operation)
        )

    initial_deck = _canonical_initial_deck(deck_size, initial_top_card)

    def select(values: Sequence[object], index: object) -> object:
        # A finite-width conditional multiplexer avoids the cubic Boolean
        # matrix multiplication used by the first community CNF prototype.
        selected = values[-1]
        for position in range(deck_size - 2, -1, -1):
            selected = z3.If(
                index == z3.BitVecVal(position, width), values[position], selected
            )
        return selected

    for message_index, (plaintext, ciphertext) in enumerate(
        zip(plaintexts, ciphertexts, strict=True)
    ):
        previous: Sequence[object] = tuple(
            z3.BitVecVal(card, width) for card in initial_deck
        )
        for offset, (symbol, emitted) in enumerate(zip(plaintext, ciphertext, strict=True)):
            current = [
                z3.BitVec(f"s_{message_index}_{offset}_{position}", width)
                for position in range(deck_size)
            ]
            operation = operations[symbol]
            solver.add(
                *(
                    current[position] == select(previous, operation[position])
                    for position in range(deck_size)
                )
            )
            solver.add(current[0] == z3.BitVecVal(emitted, width))
            previous = current

    result = solver.check()
    if result == z3.unsat:
        return "unsat", None
    if result != z3.sat:
        return "unknown", None

    model = solver.model()
    recovered = tuple(
        tuple(model.eval(value).as_long() for value in operation)
        for operation in operations
    )
    witness = GAKWitness(initial_deck, recovered)
    if encrypt_messages(plaintexts, witness.initial_deck, witness.operations) != tuple(
        tuple(ciphertext) for ciphertext in ciphertexts
    ):
        raise AssertionError("solver witness failed exact forward replay")
    return "sat", witness
