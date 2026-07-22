"""Second breadth slice: trailer categories, carry states, and worldlines."""

from __future__ import annotations

import math
from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from itertools import permutations
from random import Random

from eye_mystery.corpus import MESSAGE_ORDER
from eye_mystery.ninth_causal import CONTEXT_SPECS, equality_signature
from eye_mystery.trie_checksum import random_signature_preserving_relabeling


KEY_PHRASE = "A BAD MAGIC CARD TRICK"
TRAILER_ALPHABET = "ABDMGICRTKEFHJLNOPQSUVWXYZ0123456789"
NORMAL_FRONT = frozenset("ABKEFHJLNOPQ")
NONSTANDARD_FRONT = frozenset("DMGICRT")
BACK = frozenset("SUVWXYZ0123456789")

EAST5_TRAIL_ORDER = (
    "east5",
    "east1",
    "west1",
    "east2",
    "west2",
    "east3",
    "west3",
    "east4",
    "west4",
)

NONLITERAL_CONTEXTS = CONTEXT_SPECS[6:]
FIRST_CONTEXTS = NONLITERAL_CONTEXTS[:4]
LAST_CONTEXTS = NONLITERAL_CONTEXTS[4:]
DIGIT_ORDERS = tuple(permutations(range(3)))
BORROW_CONVENTIONS = tuple(
    (order, reverse) for order in DIGIT_ORDERS for reverse in (False, True)
)
FEATURE_VARIANTS = (
    "borrow_pair",
    "borrow_first",
    "borrow_second",
    "borrow_triple",
    "independent_pair",
    "change_pair",
)


def keyed_alphabet(key_phrase: str, alphabet: str) -> str:
    """Return an ordinary first-occurrence keyed alphabet."""

    result = []
    for symbol in key_phrase.upper() + alphabet.upper():
        if symbol in alphabet and symbol not in result:
            result.append(symbol)
    return "".join(result)


def trailer_categories(
    *, q_on_back: bool = False, split_back_digits: bool = False
) -> tuple[frozenset[str], ...]:
    normal = NORMAL_FRONT - ({"Q"} if q_on_back else set())
    back = BACK | ({"Q"} if q_on_back else set())
    if split_back_digits:
        return (
            frozenset(normal),
            NONSTANDARD_FRONT,
            frozenset(symbol for symbol in back if symbol.isalpha()),
            frozenset(symbol for symbol in back if symbol.isdigit()),
        )
    return frozenset(normal), NONSTANDARD_FRONT, frozenset(back)


def category_tape(
    text: str, categories: Sequence[frozenset[str]]
) -> tuple[int | None, ...]:
    lookup = {
        symbol: index for index, category in enumerate(categories) for symbol in category
    }
    return tuple(lookup.get(symbol) for symbol in text.upper())


@dataclass(frozen=True)
class CategoryPairAudit:
    left: str
    right: str
    left_tape: tuple[int | None, ...]
    right_tape: tuple[int | None, ...]
    mismatches: tuple[int, ...]


def audit_category_pair(
    left: str, right: str, categories: Sequence[frozenset[str]]
) -> CategoryPairAudit:
    if len(left) != len(right):
        raise ValueError("category-pair strings must have equal length")
    left_tape = category_tape(left, categories)
    right_tape = category_tape(right, categories)
    return CategoryPairAudit(
        left,
        right,
        left_tape,
        right_tape,
        tuple(
            index
            for index, (first, second) in enumerate(
                zip(left_tape, right_tape, strict=True)
            )
            if first != second
        ),
    )


def base5_digits(value: int) -> tuple[int, int, int]:
    if value not in range(125):
        raise ValueError("three base-five digits require a value in 0..124")
    return value // 25, value // 5 % 5, value % 5


def borrow_state(
    source: int,
    target: int,
    order: Sequence[int],
    *,
    reverse: bool,
) -> int:
    """Serialize the first two borrows under one digit-processing order."""

    if tuple(sorted(order)) != (0, 1, 2):
        raise ValueError("digit order must be a permutation of 0,1,2")
    if reverse:
        source, target = target, source
    source_digits = base5_digits(source)
    target_digits = base5_digits(target)
    borrow = 0
    bits = []
    for offset, digit in enumerate(order):
        borrow = int(target_digits[digit] - source_digits[digit] - borrow < 0)
        if offset < 2:
            bits.append(borrow)
    return bits[0] + 2 * bits[1]


def transition_feature_state(
    source: int,
    target: int,
    order: Sequence[int],
    *,
    reverse: bool,
    variant: str,
) -> int:
    """Encode one frozen digitwise transition-feature variant.

    ``borrow_pair`` is the originally proposed feature.  The other variants
    are an ablation suite: either borrow bit alone, all three propagated bits,
    the first two comparisons without propagation, and the first two equality
    change bits.
    """

    if tuple(sorted(order)) != (0, 1, 2):
        raise ValueError("digit order must be a permutation of 0,1,2")
    if variant not in FEATURE_VARIANTS:
        raise ValueError(f"unknown transition-feature variant: {variant}")
    if reverse:
        source, target = target, source
    source_digits = base5_digits(source)
    target_digits = base5_digits(target)

    borrow = 0
    borrow_bits = []
    for digit in order:
        borrow = int(target_digits[digit] - source_digits[digit] - borrow < 0)
        borrow_bits.append(borrow)
    if variant == "borrow_pair":
        return borrow_bits[0] + 2 * borrow_bits[1]
    if variant == "borrow_first":
        return borrow_bits[0]
    if variant == "borrow_second":
        return borrow_bits[1]
    if variant == "borrow_triple":
        return sum(bit << index for index, bit in enumerate(borrow_bits))

    selected = order[:2]
    if variant == "independent_pair":
        bits = tuple(
            int(target_digits[digit] < source_digits[digit])
            for digit in selected
        )
    else:
        bits = tuple(
            int(target_digits[digit] != source_digits[digit])
            for digit in selected
        )
    return bits[0] + 2 * bits[1]


def borrow_table(order: Sequence[int], *, reverse: bool) -> tuple[int, ...]:
    return tuple(
        borrow_state(source, target, order, reverse=reverse)
        for source in range(83)
        for target in range(83)
    )


BORROW_TABLES = {
    convention: borrow_table(convention[0], reverse=convention[1])
    for convention in BORROW_CONVENTIONS
}

FEATURE_TABLES = {
    variant: {
        convention: tuple(
            transition_feature_state(
                source,
                target,
                convention[0],
                reverse=convention[1],
                variant=variant,
            )
            for source in range(83)
            for target in range(83)
        )
        for convention in BORROW_CONVENTIONS
    }
    for variant in FEATURE_VARIANTS
}


def borrow_tape(sequence: Sequence[int], convention) -> tuple[int, ...]:
    table = BORROW_TABLES[convention]
    return tuple(
        table[83 * source + target]
        for source, target in zip(sequence, sequence[1:])
    )


def transition_feature_tape(
    sequence: Sequence[int], convention, variant: str
) -> tuple[int, ...]:
    table = FEATURE_TABLES[variant][convention]
    return tuple(
        table[83 * source + target]
        for source, target in zip(sequence, sequence[1:])
    )


@dataclass(frozen=True)
class CarryContextScore:
    matches: int
    comparisons: int
    convention: tuple[tuple[int, int, int], bool]


def carry_context_score(
    streams: Mapping[str, Sequence[int]],
    specs=NONLITERAL_CONTEXTS,
    *,
    convention=None,
) -> CarryContextScore:
    """Count exact borrow-state matches across frozen isomorph contexts."""

    conventions = BORROW_CONVENTIONS if convention is None else (convention,)
    best = None
    for candidate in conventions:
        matches = comparisons = 0
        for _, left, left_start, right, right_start, length in specs:
            left_tape = borrow_tape(
                streams[left][left_start : left_start + length], candidate
            )
            right_tape = borrow_tape(
                streams[right][right_start : right_start + length], candidate
            )
            matches += sum(
                first == second
                for first, second in zip(left_tape, right_tape, strict=True)
            )
            comparisons += len(left_tape)
        score = CarryContextScore(matches, comparisons, candidate)
        if best is None or score.matches > best.matches:
            best = score
    assert best is not None
    return best


def transition_feature_context_score(
    streams: Mapping[str, Sequence[int]],
    variant: str,
    specs=NONLITERAL_CONTEXTS,
    *,
    convention=None,
) -> CarryContextScore:
    """Count state agreements for one member of the frozen ablation suite."""

    conventions = BORROW_CONVENTIONS if convention is None else (convention,)
    best = None
    for candidate in conventions:
        matches = comparisons = 0
        for _, left, left_start, right, right_start, length in specs:
            left_tape = transition_feature_tape(
                streams[left][left_start : left_start + length],
                candidate,
                variant,
            )
            right_tape = transition_feature_tape(
                streams[right][right_start : right_start + length],
                candidate,
                variant,
            )
            matches += sum(
                first == second
                for first, second in zip(left_tape, right_tape, strict=True)
            )
            comparisons += len(left_tape)
        score = CarryContextScore(matches, comparisons, candidate)
        if best is None or score.matches > best.matches:
            best = score
    assert best is not None
    return best


@dataclass(frozen=True)
class CarryHeldOutScore:
    train: CarryContextScore
    test: CarryContextScore


def carry_held_out_score(streams, train_specs, test_specs) -> CarryHeldOutScore:
    train = carry_context_score(streams, train_specs)
    test = carry_context_score(
        streams, test_specs, convention=train.convention
    )
    return CarryHeldOutScore(train, test)


def transition_feature_held_out_score(
    streams, variant: str, train_specs, test_specs
) -> CarryHeldOutScore:
    train = transition_feature_context_score(streams, variant, train_specs)
    test = transition_feature_context_score(
        streams,
        variant,
        test_specs,
        convention=train.convention,
    )
    return CarryHeldOutScore(train, test)


def carry_markov_gain(
    streams: Mapping[str, Sequence[int]],
    convention,
    *,
    alpha: float = 0.5,
) -> float:
    """LOO log gain of first-order carry states over an i.i.d. model."""

    tapes = {
        name: borrow_tape(streams[name][1:], convention)
        for name in MESSAGE_ORDER
    }
    gain = 0.0
    for held_out in MESSAGE_ORDER:
        states: Counter[int] = Counter()
        bigrams: Counter[tuple[int, int]] = Counter()
        total = 0
        for name, tape in tapes.items():
            if name == held_out:
                continue
            states.update(tape)
            bigrams.update(zip(tape, tape[1:]))
            total += len(tape)
        held_tape = tapes[held_out]
        for previous, current in zip(held_tape, held_tape[1:]):
            conditional = (bigrams[previous, current] + alpha) / (
                states[previous] + 4 * alpha
            )
            independent = (states[current] + alpha) / (total + 4 * alpha)
            gain += math.log(conditional / independent)
    return gain


@dataclass(frozen=True)
class CarryMarkovScore:
    gain: float
    convention: tuple[tuple[int, int, int], bool]


def best_carry_markov_score(streams) -> CarryMarkovScore:
    best = None
    for convention in BORROW_CONVENTIONS:
        score = CarryMarkovScore(carry_markov_gain(streams, convention), convention)
        if best is None or score.gain > best.gain:
            best = score
    assert best is not None
    return best


def permute_body_labels(
    streams: Mapping[str, Sequence[int]], permutation: Sequence[int]
) -> dict[str, tuple[int, ...]]:
    if tuple(sorted(permutation)) != tuple(range(83)):
        raise ValueError("body-label control requires a permutation of 0..82")
    return {
        name: (stream[0],) + tuple(permutation[value] for value in stream[1:])
        for name, stream in streams.items()
    }


def label_count_vector(values: Sequence[int]) -> tuple[int, ...]:
    counts = Counter(values)
    return tuple(counts[value] for value in range(83))


def checksum_preserving_body_permutation(
    streams: Mapping[str, Sequence[int]], rng: Random
) -> tuple[int, ...]:
    """Draw from the subgroup preserving the three known diagonal sums.

    Equal full-message count triples may be permuted.  All nine marker labels
    are fixed globally, so relabeling bodies preserves the complete authored
    messages' integer sums, not only their residues modulo 101.
    """

    diagonal = tuple(
        label_count_vector(streams[name]) for name in ("east1", "east3", "east5")
    )
    fixed_markers = tuple(streams[name][0] for name in MESSAGE_ORDER)
    return random_signature_preserving_relabeling(
        83,
        diagonal,
        rng,
        fixed_labels=fixed_markers,
    )


def affine_body_permutations() -> tuple[tuple[int, ...], ...]:
    """Return the complete affine group ``x -> a*x+b`` over F_83."""

    return tuple(
        tuple((multiplier * value + offset) % 83 for value in range(83))
        for multiplier in range(1, 83)
        for offset in range(83)
    )


def literal_suffix_prefix(left: Sequence[int], right: Sequence[int]) -> int:
    best = 0
    for length in range(1, min(len(left), len(right)) + 1):
        if tuple(left[-length:]) == tuple(right[:length]):
            best = length
    return best


def isomorphic_suffix_prefix(
    left: Sequence[int], right: Sequence[int], *, minimum_validations: int = 2
) -> int:
    """Longest suffix/prefix isomorph with repeated-equality evidence."""

    best = 0
    for length in range(1, min(len(left), len(right)) + 1):
        left_window = left[-length:]
        right_window = right[:length]
        left_validations = length - len(set(left_window))
        right_validations = length - len(set(right_window))
        if min(left_validations, right_validations) < minimum_validations:
            continue
        if equality_signature(left_window) == equality_signature(right_window):
            best = length
    return best


def overlap_weights(
    bodies: Mapping[str, Sequence[int]], *, isomorphic: bool
) -> dict[tuple[str, str], int]:
    function = isomorphic_suffix_prefix if isomorphic else literal_suffix_prefix
    return {
        (left, right): function(bodies[left], bodies[right])
        for left in bodies
        for right in bodies
        if left != right
    }


def path_score(order: Sequence[str], weights: Mapping[tuple[str, str], int]) -> int:
    return sum(weights[left, right] for left, right in zip(order, order[1:]))


@dataclass(frozen=True)
class WorldlineScore:
    order: tuple[str, ...]
    score: int
    orders: int
    at_least_observed: int
    best_score: int
    best_order: tuple[str, ...]

    @property
    def exact_tail(self) -> float:
        return self.at_least_observed / self.orders


def worldline_score(
    bodies: Mapping[str, Sequence[int]],
    order: Sequence[str],
    *,
    isomorphic: bool,
) -> WorldlineScore:
    names = tuple(bodies)
    if set(order) != set(names) or len(order) != len(names):
        raise ValueError("worldline order must contain every panel once")
    weights = overlap_weights(bodies, isomorphic=isomorphic)
    observed = path_score(order, weights)
    at_least = 0
    best_score = -1
    best_order = names
    count = 0
    for candidate in permutations(names):
        score = path_score(candidate, weights)
        count += 1
        at_least += score >= observed
        if score > best_score:
            best_score = score
            best_order = candidate
    return WorldlineScore(
        tuple(order), observed, count, at_least, best_score, best_order
    )
