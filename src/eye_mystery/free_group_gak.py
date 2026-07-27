"""Free-group stabilizer screen and constructive ordinary-GAK witnesses.

For an ordinary GAK, equal ciphertext cards at two times mean that the
intervening operation word fixes position zero. All such words generate a
subgroup of the free group on the plaintext actions. Stallings folding decides
whether any observed unequal-card word is forced into that subgroup.

When the folded core fits the deck, its partial inverse automaton can be
completed to permutations. A successful completion gives a full GAK key and
independent starting deck for every trace.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
import random
from typing import Any

from eye_mystery.arbitrary_gak_sat import encrypt_messages
from eye_mystery.gak_fixed_point import combined_word_spans


@dataclass(frozen=True)
class FreeGroupAudit:
    """Exact subgroup-membership result for a collection of aligned traces."""

    core_states: int
    fixed_words: int
    nonfixed_words: int
    forced_nonfix_words: tuple[tuple[int, ...], ...]
    transitions: tuple[tuple[int, int, int], ...]


@dataclass(frozen=True)
class FreeGroupGAKWitness:
    """One exact ordinary-GAK realization of all supplied equality patterns."""

    initial_decks: tuple[tuple[int, ...], ...]
    operations: tuple[tuple[int, ...], ...]
    plaintexts: tuple[tuple[int, ...], ...]


class _UnionFind:
    def __init__(self, size: int) -> None:
        self.parent = list(range(size))

    def find(self, value: int) -> int:
        while self.parent[value] != value:
            self.parent[value] = self.parent[self.parent[value]]
            value = self.parent[value]
        return value

    def union(self, left: int, right: int) -> bool:
        left = self.find(left)
        right = self.find(right)
        if left == right:
            return False
        if left > right:
            left, right = right, left
        self.parent[right] = left
        return True


def _inverse(letter: int) -> int:
    return -letter


def _fold_words(
    words: Sequence[Sequence[int]],
) -> tuple[int, tuple[tuple[int, int, int], ...]]:
    edges: list[tuple[int, int, int]] = []
    next_vertex = 1
    for word in words:
        if not word:
            continue
        source = 0
        for offset, letter in enumerate(word):
            target = 0 if offset == len(word) - 1 else next_vertex
            if target:
                next_vertex += 1
            edges.append((source, letter, target))
            edges.append((target, _inverse(letter), source))
            source = target

    return _fold_edges(next_vertex, edges)


def _fold_edges(
    vertex_count: int,
    edges: Sequence[tuple[int, int, int]],
    merges: Sequence[tuple[int, int]] = (),
) -> tuple[int, tuple[tuple[int, int, int], ...]]:
    union_find = _UnionFind(vertex_count)
    for left, right in merges:
        union_find.union(left, right)
    while True:
        outgoing: dict[tuple[int, int], int] = {}
        changed = False
        for raw_source, letter, raw_target in edges:
            source = union_find.find(raw_source)
            target = union_find.find(raw_target)
            key = (source, letter)
            if key in outgoing:
                changed |= union_find.union(outgoing[key], target)
            else:
                outgoing[key] = target
        if not changed:
            break

    roots = sorted({union_find.find(vertex) for vertex in range(vertex_count)})
    base_root = union_find.find(0)
    ordered_roots = (base_root, *(root for root in roots if root != base_root))
    labels = {root: index for index, root in enumerate(ordered_roots)}
    folded = {
        (
            labels[union_find.find(source)],
            letter,
            labels[union_find.find(target)],
        )
        for source, letter, target in edges
    }
    return len(ordered_roots), tuple(sorted(folded))


def _walk(
    transitions: dict[tuple[int, int], int],
    word: Sequence[int],
) -> int | None:
    state = 0
    for letter in word:
        key = (state, letter)
        if key not in transitions:
            return None
        state = transitions[key]
    return state


def audit_free_group_gak(
    plaintexts: Sequence[Sequence[int]],
    ciphertexts: Sequence[Sequence[int]],
) -> FreeGroupAudit:
    """Apply exact free-subgroup closure to all endpoint observations."""

    plains = tuple(tuple(plaintext) for plaintext in plaintexts)
    ciphers = tuple(tuple(ciphertext) for ciphertext in ciphertexts)
    spans = combined_word_spans(plains, ciphers)
    fixed = tuple(span for span in spans if span.fixes_top)
    nonfixed = tuple(span for span in spans if not span.fixes_top)
    # Deck-operation composition evaluates a chronological interval in reverse
    # transition order. Letters are shifted by one so their signed inverses
    # remain distinct when plaintext symbol zero is present.
    fixed_words = tuple(
        tuple(symbol + 1 for symbol in reversed(span.word)) for span in fixed
    )
    core_states, transition_rows = _fold_words(fixed_words)
    transitions = {
        (source, letter): target
        for source, letter, target in transition_rows
    }
    forced = []
    for span in nonfixed:
        word = tuple(symbol + 1 for symbol in reversed(span.word))
        if _walk(transitions, word) == 0:
            forced.append(tuple(span.word))
    return FreeGroupAudit(
        core_states,
        len(fixed),
        len(nonfixed),
        tuple(sorted(set(forced), key=lambda word: (len(word), word))),
        transition_rows,
    )


def _constraint_words(
    plaintexts: Sequence[Sequence[int]],
    ciphertexts: Sequence[Sequence[int]],
) -> tuple[tuple[tuple[int, ...], ...], tuple[tuple[int, ...], ...]]:
    spans = combined_word_spans(plaintexts, ciphertexts)
    fixed = tuple(
        tuple(symbol + 1 for symbol in reversed(span.word))
        for span in spans
        if span.fixes_top
    )
    nonfixed = tuple(
        tuple(symbol + 1 for symbol in reversed(span.word))
        for span in spans
        if not span.fixes_top
    )
    return fixed, nonfixed


def _forced_words(
    transitions: Sequence[tuple[int, int, int]],
    nonfixed_words: Sequence[Sequence[int]],
) -> tuple[tuple[int, ...], ...]:
    transition_map = {
        (source, letter): target for source, letter, target in transitions
    }
    return tuple(
        word for word in nonfixed_words if _walk(transition_map, word) == 0
    )


def compress_free_group_audit(
    plaintexts: Sequence[Sequence[int]],
    ciphertexts: Sequence[Sequence[int]],
    *,
    target_states: int,
    attempts: int = 100,
    proposals_per_step: int = 2_000,
    seed: int = 0,
) -> FreeGroupAudit | None:
    """Randomly enlarge the stabilizer without violating observed nonmembers."""

    if target_states < 1:
        raise ValueError("target_states must be positive")
    base = audit_free_group_gak(plaintexts, ciphertexts)
    if base.forced_nonfix_words:
        return None
    _, nonfixed_words = _constraint_words(plaintexts, ciphertexts)
    rng = random.Random(seed)
    for _attempt in range(attempts):
        state_count = base.core_states
        transitions = base.transitions
        while state_count > target_states:
            accepted = False
            for _proposal in range(proposals_per_step):
                left, right = rng.sample(range(state_count), 2)
                new_count, new_transitions = _fold_edges(
                    state_count,
                    transitions,
                    ((left, right),),
                )
                if new_count >= state_count:
                    continue
                if _forced_words(new_transitions, nonfixed_words):
                    continue
                state_count = new_count
                transitions = new_transitions
                accepted = True
                break
            if not accepted:
                break
        if state_count <= target_states:
            return FreeGroupAudit(
                state_count,
                base.fixed_words,
                base.nonfixed_words,
                (),
                transitions,
            )
    return None


def _completion(
    audit: FreeGroupAudit,
    *,
    deck_size: int,
    plaintext_alphabet_size: int,
    rng: random.Random,
) -> tuple[tuple[int, ...], ...]:
    if audit.core_states > deck_size:
        raise ValueError("folded subgroup core exceeds the deck")
    partial = {
        (source, letter - 1): target
        for source, letter, target in audit.transitions
        if letter > 0
    }
    operations = []
    for symbol in range(plaintext_alphabet_size):
        operation: list[int | None] = [None] * deck_size
        used_targets = set()
        for source in range(audit.core_states):
            key = (source, symbol)
            if key in partial:
                operation[source] = partial[key]
                used_targets.add(partial[key])
        missing_sources = [
            source for source, target in enumerate(operation) if target is None
        ]
        missing_targets = [
            target for target in range(deck_size) if target not in used_targets
        ]
        rng.shuffle(missing_targets)
        for source, target in zip(
            missing_sources, missing_targets, strict=True
        ):
            operation[source] = target
        operations.append(tuple(value for value in operation if value is not None))
    return tuple(operations)


def _decks_for_outputs(
    plaintexts: Sequence[Sequence[int]],
    ciphertexts: Sequence[Sequence[int]],
    operations: Sequence[Sequence[int]],
    *,
    deck_size: int,
) -> tuple[tuple[int, ...], ...] | None:
    identity = tuple(range(deck_size))
    origin_traces = encrypt_messages(plaintexts, identity, operations)
    decks = []
    for origins, ciphertext in zip(origin_traces, ciphertexts, strict=True):
        card_by_origin: dict[int, int] = {}
        origin_by_card: dict[int, int] = {}
        for origin, card in zip(origins, ciphertext, strict=True):
            if (
                origin in card_by_origin
                and card_by_origin[origin] != card
            ) or (
                card in origin_by_card
                and origin_by_card[card] != origin
            ):
                return None
            card_by_origin[origin] = card
            origin_by_card[card] = origin
        remaining_cards = [
            card for card in range(deck_size) if card not in origin_by_card
        ]
        deck: list[int | None] = [None] * deck_size
        for origin, card in card_by_origin.items():
            deck[origin] = card
        for origin, card in zip(
            (index for index, card in enumerate(deck) if card is None),
            remaining_cards,
            strict=True,
        ):
            deck[origin] = card
        decks.append(tuple(card for card in deck if card is not None))
    return tuple(decks)


def _complete_direct_permutation(
    model: Any,
    transitions: Sequence[tuple[Any, Any]],
    *,
    deck_size: int,
) -> tuple[int, ...]:
    partial: dict[int, int] = {}
    used_targets: set[int] = set()
    for source_expression, target_expression in transitions:
        source = model.eval(source_expression, model_completion=True).as_long()
        target = model.eval(target_expression, model_completion=True).as_long()
        if source in partial and partial[source] != target:
            raise AssertionError("model violates operation functionality")
        if target in used_targets and partial.get(source) != target:
            raise AssertionError("model violates operation injectivity")
        partial[source] = target
        used_targets.add(target)
    partial.update(
        zip(
            (source for source in range(deck_size) if source not in partial),
            (target for target in range(deck_size) if target not in used_targets),
            strict=True,
        )
    )
    return tuple(partial[source] for source in range(deck_size))


def construct_free_group_gak_witness(
    plaintexts: Sequence[Sequence[int]],
    ciphertexts: Sequence[Sequence[int]],
    *,
    deck_size: int,
    plaintext_alphabet_size: int,
    completion_trials: int = 1_000,
    seed: int = 0,
    compression_attempts: int = 100,
) -> tuple[FreeGroupAudit, FreeGroupGAKWitness | None]:
    """Complete a compatible folded core to full replayable permutations."""

    plains = tuple(tuple(plaintext) for plaintext in plaintexts)
    ciphers = tuple(tuple(ciphertext) for ciphertext in ciphertexts)
    audit = audit_free_group_gak(plains, ciphers)
    if audit.forced_nonfix_words:
        return audit, None
    if audit.core_states > deck_size:
        compressed = compress_free_group_audit(
            plains,
            ciphers,
            target_states=deck_size,
            attempts=compression_attempts,
            seed=seed,
        )
        if compressed is None:
            return audit, None
        audit = compressed
    rng = random.Random(seed)
    for _trial in range(completion_trials):
        operations = _completion(
            audit,
            deck_size=deck_size,
            plaintext_alphabet_size=plaintext_alphabet_size,
            rng=rng,
        )
        decks = _decks_for_outputs(
            plains,
            ciphers,
            operations,
            deck_size=deck_size,
        )
        if decks is None:
            continue
        witness = FreeGroupGAKWitness(decks, operations, plains)
        replay = tuple(
            encrypt_messages((plaintext,), deck, operations)[0]
            for plaintext, deck in zip(plains, decks, strict=True)
        )
        if replay != ciphers:
            raise AssertionError("free-group GAK witness failed exact replay")
        return audit, witness
    return audit, None


def recover_fixed_schedule_gak_with_z3(
    plaintexts: Sequence[Sequence[int]],
    ciphertexts: Sequence[Sequence[int]],
    *,
    deck_size: int,
    plaintext_alphabet_size: int,
    pinned_audit: FreeGroupAudit | None = None,
    timeout_ms: int = 60_000,
    replay_deck_size: int | None = None,
) -> tuple[str, FreeGroupGAKWitness | None]:
    """Complete fixed schedules using only their top-origin equality classes."""

    try:
        import z3  # type: ignore[import-not-found]
    except ImportError as error:  # pragma: no cover - environment dependent
        raise RuntimeError("fixed-schedule GAK recovery requires z3-solver") from error

    plains = tuple(tuple(plaintext) for plaintext in plaintexts)
    ciphers = tuple(tuple(ciphertext) for ciphertext in ciphertexts)
    full_deck_size = replay_deck_size or deck_size
    if full_deck_size < deck_size:
        raise ValueError("replay deck cannot be smaller than the active action")
    if any(
        len(set(ciphertext)) > deck_size for ciphertext in ciphers
    ):
        raise ValueError("active action has too few positions for a trace")
    if len(plains) != len(ciphers) or any(
        len(plaintext) != len(ciphertext)
        for plaintext, ciphertext in zip(plains, ciphers, strict=True)
    ):
        raise ValueError("plaintext and ciphertext shapes differ")
    solver = z3.Solver()
    solver.set(timeout=timeout_ms)
    width = max(1, deck_size.bit_length())
    position_sort = z3.BitVecSort(width)
    position_limit = z3.BitVecVal(deck_size, width)
    operations = tuple(
        z3.Function(f"origin_op_{symbol}", position_sort, position_sort)
        for symbol in range(plaintext_alphabet_size)
    )
    inverses = tuple(
        z3.Function(f"origin_inv_{symbol}", position_sort, position_sort)
        for symbol in range(plaintext_alphabet_size)
    )
    transition_records: list[list[tuple[Any, Any]]] = [
        [] for _ in range(plaintext_alphabet_size)
    ]
    if pinned_audit is not None:
        if pinned_audit.core_states > deck_size:
            raise ValueError("pinned audit exceeds the deck")
        for source, letter, target in pinned_audit.transitions:
            if letter > 0:
                symbol = letter - 1
                source_value = z3.BitVecVal(source, width)
                target_value = z3.BitVecVal(target, width)
                solver.add(
                    operations[symbol](source_value) == target_value,
                    inverses[symbol](target_value) == source_value,
                )
                transition_records[symbol].append(
                    (source_value, target_value)
                )

    for trace_index, (plaintext, ciphertext) in enumerate(
        zip(plains, ciphers, strict=True)
    ):
        origins: list[Any] = []
        for offset in range(len(plaintext)):
            origin: Any = z3.BitVecVal(0, width)
            for layer, symbol in enumerate(reversed(plaintext[: offset + 1])):
                old_origin = origin
                origin = z3.BitVec(
                    f"origin_{trace_index}_{offset}_{layer}",
                    width,
                )
                solver.add(
                    origin == operations[symbol](old_origin),
                    z3.ULT(origin, position_limit),
                    inverses[symbol](origin) == old_origin,
                )
                transition_records[symbol].append((old_origin, origin))
            origins.append(origin)
        first_by_card: dict[int, Any] = {}
        for origin, card in zip(origins, ciphertext, strict=True):
            if card in first_by_card:
                solver.add(origin == first_by_card[card])
            else:
                first_by_card[card] = origin
        if len(first_by_card) > 1:
            solver.add(z3.Distinct(*first_by_card.values()))

    result = solver.check()
    if result == z3.unsat:
        return "unsat", None
    if result != z3.sat:
        return "unknown", None
    model = solver.model()
    active_operations = tuple(
        _complete_direct_permutation(model, records, deck_size=deck_size)
        for records in transition_records
    )
    recovered_operations = tuple(
        (
            operation
            if full_deck_size == deck_size
            else (*operation, *range(deck_size, full_deck_size))
        )
        for operation in active_operations
    )
    decks = _decks_for_outputs(
        plains,
        ciphers,
        recovered_operations,
        deck_size=full_deck_size,
    )
    if decks is None:
        raise AssertionError("SAT origin model did not induce valid decks")
    witness = FreeGroupGAKWitness(decks, recovered_operations, plains)
    replay = tuple(
        encrypt_messages((plaintext,), deck, recovered_operations)[0]
        for plaintext, deck in zip(plains, decks, strict=True)
    )
    if replay != ciphers:
        raise AssertionError("fixed-schedule GAK witness failed exact replay")
    return "sat", witness
