"""CP-SAT completion of fixed ordinary-GAK equality constraints.

Instead of tracking every card through every deck update, this formulation
builds one prefix trie of all reversed interval words.  Equal output cards
force a trie endpoint to state zero; unequal cards force it away from zero.
Shared action tables are complete permutations, so a SAT model is an exact
finite group action.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from eye_mystery.arbitrary_gak_sat import encrypt_messages
from eye_mystery.free_group_gak import (
    FreeGroupAudit,
    FreeGroupGAKWitness,
    _constraint_words,
    _decks_for_outputs,
)


def _constraint_trie(
    fixed_words: Sequence[Sequence[int]],
    nonfixed_words: Sequence[Sequence[int]],
) -> tuple[
    tuple[tuple[int, int, int], ...],
    tuple[int, ...],
    tuple[int, ...],
]:
    children: dict[tuple[int, int], int] = {}
    edges: list[tuple[int, int, int]] = []
    next_node = 1

    def insert(word: Sequence[int]) -> int:
        nonlocal next_node
        node = 0
        for letter in word:
            key = (node, letter)
            if key not in children:
                children[key] = next_node
                edges.append((node, letter, next_node))
                next_node += 1
            node = children[key]
        return node

    fixed_endpoints = tuple(insert(word) for word in fixed_words)
    nonfixed_endpoints = tuple(insert(word) for word in nonfixed_words)
    return tuple(edges), fixed_endpoints, nonfixed_endpoints


def recover_cp_sat_free_group_completion(
    plaintexts: Sequence[Sequence[int]],
    ciphertexts: Sequence[Sequence[int]],
    *,
    deck_size: int,
    plaintext_alphabet_size: int,
    timeout_seconds: float = 30.0,
    num_workers: int = 8,
    pinned_audit: FreeGroupAudit | None = None,
    break_state_symmetry: bool = True,
    operation_hints: Sequence[Sequence[int]] | None = None,
) -> tuple[str, FreeGroupGAKWitness | None]:
    """Complete a fixed schedule to a replayable finite permutation action."""

    try:
        from ortools.sat.python import cp_model
    except ImportError as error:  # pragma: no cover - optional dependency
        raise RuntimeError("CP-SAT completion requires OR-Tools") from error

    plains = tuple(tuple(plaintext) for plaintext in plaintexts)
    ciphers = tuple(tuple(ciphertext) for ciphertext in ciphertexts)
    if len(plains) != len(ciphers) or any(
        len(plaintext) != len(ciphertext)
        for plaintext, ciphertext in zip(plains, ciphers, strict=True)
    ):
        raise ValueError("plaintext and ciphertext shapes differ")
    if deck_size < 2 or plaintext_alphabet_size < 1:
        raise ValueError("alphabet sizes must be positive")
    if any(
        not 0 <= symbol < plaintext_alphabet_size
        for plaintext in plains
        for symbol in plaintext
    ):
        raise ValueError("plaintext symbol is outside the action alphabet")
    if any(
        not 0 <= card < deck_size
        for ciphertext in ciphers
        for card in ciphertext
    ):
        raise ValueError("ciphertext card is outside the deck")

    fixed_words, nonfixed_words = _constraint_words(plains, ciphers)
    edges, fixed_endpoints, nonfixed_endpoints = _constraint_trie(
        fixed_words,
        nonfixed_words,
    )
    node_count = 1 + max(
        (target for _, _, target in edges),
        default=0,
    )
    model = cp_model.CpModel()
    operations = tuple(
        tuple(
            model.new_int_var(
                0,
                deck_size - 1,
                f"operation_{symbol}_{position}",
            )
            for position in range(deck_size)
        )
        for symbol in range(plaintext_alphabet_size)
    )
    for operation in operations:
        model.add_all_different(operation)
    if operation_hints is not None:
        if (
            len(operation_hints) != plaintext_alphabet_size
            or any(len(row) != deck_size for row in operation_hints)
        ):
            raise ValueError("operation hint shape differs from the model")
        for variables, values in zip(
            operations, operation_hints, strict=True
        ):
            for variable, value in zip(variables, values, strict=True):
                model.add_hint(variable, value)

    states = tuple(
        model.new_int_var(0, deck_size - 1, f"trie_state_{node}")
        for node in range(node_count)
    )
    model.add(states[0] == 0)
    for source, letter, target in edges:
        model.add_element(
            states[source],
            operations[letter - 1],
            states[target],
        )
    for endpoint in fixed_endpoints:
        model.add(states[endpoint] == 0)
    for endpoint in nonfixed_endpoints:
        model.add(states[endpoint] != 0)

    if pinned_audit is not None:
        if pinned_audit.core_states > deck_size:
            raise ValueError("pinned audit exceeds the deck")
        for source, letter, target in pinned_audit.transitions:
            if letter > 0:
                model.add(operations[letter - 1][source] == target)
    elif break_state_symmetry and node_count > 1:
        # Value precedence: a newly encountered trie node may use zero, an
        # existing positive state, or exactly the next unused positive label.
        # Every solution is conjugate (fixing zero) to one in this form.
        maximum = model.new_int_var(0, deck_size - 1, "max_state_0")
        model.add(maximum == 0)
        for node in range(1, node_count):
            model.add(states[node] <= maximum + 1)
            next_maximum = model.new_int_var(
                0,
                deck_size - 1,
                f"max_state_{node}",
            )
            model.add_max_equality(
                next_maximum,
                (maximum, states[node]),
            )
            maximum = next_maximum

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = timeout_seconds
    solver.parameters.num_search_workers = num_workers
    solver.parameters.random_seed = 31072026
    result = solver.solve(model)
    if result == cp_model.INFEASIBLE:
        return "unsat", None
    if result not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        return "unknown", None

    recovered_operations = tuple(
        tuple(solver.value(value) for value in operation)
        for operation in operations
    )
    decks = _decks_for_outputs(
        plains,
        ciphers,
        recovered_operations,
        deck_size=deck_size,
    )
    if decks is None:
        raise AssertionError("CP-SAT group action did not induce valid decks")
    witness = FreeGroupGAKWitness(
        initial_decks=decks,
        operations=recovered_operations,
        plaintexts=plains,
    )
    replay = tuple(
        encrypt_messages((plaintext,), deck, recovered_operations)[0]
        for plaintext, deck in zip(plains, decks, strict=True)
    )
    if replay != ciphers:
        raise AssertionError("CP-SAT group witness failed exact replay")
    return "sat", witness
