"""Cheap probes for the seventh breadth-first Eye-cipher funnel."""

from __future__ import annotations

from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from math import log2
import zlib

from eye_mystery.corpus import MESSAGE_ORDER, ROW_PAIR_TRIGRAM_LENGTHS
from eye_mystery.factoradic_headers import inverse, lexicographic_unrank
from eye_mystery.visual_rows import visual_rows


SENTINEL = 6


def base5_digits(value: int) -> tuple[int, int, int]:
    if value not in range(125):
        raise ValueError("value must fit one base-five trigram")
    return value // 25, value // 5 % 5, value % 5


def raw_digits(values: Sequence[int]) -> tuple[int, ...]:
    return tuple(digit for value in values for digit in base5_digits(value))


def renderer_body_tape(name: str, stream: Sequence[int]) -> tuple[int, ...]:
    """Return exact visual-row tape after removing the three header eyes.

    In renderer order, the first trigram's first two eyes begin the first top
    row and its third eye begins the first bottom row.  Removing the first
    three *linear* symbols would therefore be wrong.
    """

    rows = list(visual_rows(raw_digits(stream), ROW_PAIR_TRIGRAM_LENGTHS[name]))
    rows[0] = rows[0][2:]
    rows[1] = rows[1][1:]
    result: list[int] = []
    for row in rows:
        result.extend(row)
        result.append(5)
    return tuple(result)


def suffix_array(values: Sequence[int]) -> tuple[int, ...]:
    """Construct a suffix array by deterministic prefix doubling."""

    if not values:
        return ()
    order = list(range(len(values)))
    ranks = list(values)
    width = 1
    while True:
        order.sort(
            key=lambda index: (
                ranks[index],
                ranks[index + width] if index + width < len(values) else -1,
            )
        )
        next_ranks = [0] * len(values)
        for position in range(1, len(order)):
            previous = order[position - 1]
            current = order[position]
            previous_key = (
                ranks[previous],
                ranks[previous + width]
                if previous + width < len(values)
                else -1,
            )
            current_key = (
                ranks[current],
                ranks[current + width]
                if current + width < len(values)
                else -1,
            )
            next_ranks[current] = next_ranks[previous] + (current_key != previous_key)
        ranks = next_ranks
        if ranks[order[-1]] == len(values) - 1:
            return tuple(order)
        width *= 2


def bwt_last_column(
    values: Sequence[int], alphabet_order: Sequence[int]
) -> tuple[int, ...]:
    """Return the terminated BWT last column under one six-symbol order."""

    if sorted(alphabet_order) != list(range(6)):
        raise ValueError("alphabet order must permute renderer symbols 0..5")
    if any(value not in range(6) for value in values):
        raise ValueError("renderer tape contains a symbol outside 0..5")
    rank = {symbol: position + 1 for position, symbol in enumerate(alphabet_order)}
    text = tuple(rank[value] for value in values) + (0,)
    augmented = tuple(values) + (SENTINEL,)
    return tuple(
        augmented[index - 1] if index else SENTINEL
        for index in suffix_array(text)
    )


def move_to_front(values: Sequence[int], alphabet_order: Sequence[int]) -> tuple[int, ...]:
    """Encode a BWT column with sentinel-first move-to-front ranks."""

    alphabet = [SENTINEL, *alphabet_order]
    output = []
    for value in values:
        rank = alphabet.index(value)
        output.append(rank)
        alphabet.insert(0, alphabet.pop(rank))
    return tuple(output)


def run_count(values: Sequence[int]) -> int:
    return sum(index == 0 or value != values[index - 1] for index, value in enumerate(values))


@dataclass(frozen=True)
class BwtMtfScore:
    runs: int
    mtf_zeros: int
    route: str
    symbols: int


def bwt_mtf_score(streams: Mapping[str, Sequence[int]]) -> BwtMtfScore:
    """Select header order or inverse globally by minimum BWT run count."""

    candidates = []
    for route in ("header", "inverse"):
        runs = zeros = symbols = 0
        for name in MESSAGE_ORDER:
            permutation = lexicographic_unrank(streams[name][0])
            order = permutation if route == "header" else inverse(permutation)
            column = bwt_last_column(renderer_body_tape(name, streams[name]), order)
            mtf = move_to_front(column, order)
            runs += run_count(column)
            zeros += mtf.count(0)
            symbols += len(column)
        candidates.append(BwtMtfScore(runs, zeros, route, symbols))
    return min(candidates, key=lambda score: (score.runs, -score.mtf_zeros, score.route))


def permute_six_blocks(values: Sequence[int], order: Sequence[int]) -> tuple[int, ...]:
    """Permute positions in each complete six-token block; preserve the tail."""

    if sorted(order) != list(range(6)):
        raise ValueError("block order must permute 0..5")
    complete = len(values) // 6 * 6
    output = []
    for start in range(0, complete, 6):
        block = values[start : start + 6]
        output.extend(block[index] for index in order)
    output.extend(values[complete:])
    return tuple(output)


@dataclass(frozen=True)
class BlockScore:
    adjacent_equal: int
    repeated_bigrams: int
    route: str
    transitions: int


def six_block_score(streams: Mapping[str, Sequence[int]]) -> BlockScore:
    """Select one global header/inverse positional convention."""

    candidates = []
    for route in ("header", "inverse"):
        bigrams = []
        adjacent_equal = transitions = 0
        for name in MESSAGE_ORDER:
            permutation = lexicographic_unrank(streams[name][0])
            order = permutation if route == "header" else inverse(permutation)
            transformed = permute_six_blocks(streams[name][1:], order)
            pairs = tuple(zip(transformed, transformed[1:]))
            bigrams.extend(pairs)
            adjacent_equal += sum(left == right for left, right in pairs)
            transitions += len(pairs)
        candidates.append(
            BlockScore(
                adjacent_equal,
                len(bigrams) - len(set(bigrams)),
                route,
                transitions,
            )
        )
    return max(
        candidates,
        key=lambda score: (score.adjacent_equal, score.repeated_bigrams, score.route),
    )


def shortest_gap_bits(values: Sequence[int], *, modulus: int = 101) -> tuple[int, ...]:
    """Mark transitions whose shortest mod-101 path crosses hidden 83..100."""

    result = []
    for left, right in zip(values, values[1:]):
        forward = (right - left) % modulus
        displacement = forward if forward <= modulus // 2 else forward - modulus
        step = 1 if displacement > 0 else -1
        interior = tuple(
            (left + step * offset) % modulus
            for offset in range(1, abs(displacement))
        )
        result.append(int(any(value >= 83 for value in interior)))
    return tuple(result)


def pack_bits(bits: Sequence[int]) -> bytes:
    """Pack a bit sequence MSB-first, including its final partial byte."""

    output = bytearray()
    for start in range(0, len(bits), 8):
        value = 0
        for bit in bits[start : start + 8]:
            if bit not in (0, 1):
                raise ValueError("bit stream contains a value outside 0/1")
            value = 2 * value + bit
        value <<= 8 - len(bits[start : start + 8])
        output.append(value)
    return bytes(output)


@dataclass(frozen=True)
class GapScore:
    compressed_bytes: int
    runs: int
    ones: int
    bits: int


def gap_score(streams: Mapping[str, Sequence[int]]) -> GapScore:
    bits = tuple(
        bit
        for name in MESSAGE_ORDER
        for bit in shortest_gap_bits(streams[name][1:])
    )
    return GapScore(
        len(zlib.compress(pack_bits(bits), level=9)),
        run_count(bits),
        sum(bits),
        len(bits),
    )


def change_masks(values: Sequence[int]) -> tuple[int, ...]:
    """Encode which of the three base-five coordinates changed."""

    result = []
    for left, right in zip(values, values[1:]):
        left_digits = base5_digits(left)
        right_digits = base5_digits(right)
        mask = sum(
            (left_digit != right_digit) << (2 - index)
            for index, (left_digit, right_digit) in enumerate(
                zip(left_digits, right_digits, strict=True)
            )
        )
        result.append(mask)
    return tuple(result)


def comparison_signatures(values: Sequence[int]) -> tuple[int, ...]:
    """Encode per-eye less/equal/greater comparisons as one base-three value."""

    result = []
    for left, right in zip(values, values[1:]):
        value = 0
        for left_digit, right_digit in zip(
            base5_digits(left), base5_digits(right), strict=True
        ):
            sign = 0 if right_digit < left_digit else 1 if right_digit == left_digit else 2
            value = 3 * value + sign
        result.append(value)
    return tuple(result)


@dataclass(frozen=True)
class ChangeScore:
    compressed_bytes: int
    runs: int
    route: str
    symbols: int


def change_score(streams: Mapping[str, Sequence[int]]) -> ChangeScore:
    """Select the frozen mask/comparison family by byte compression."""

    candidates = []
    for route, transform in (
        ("change-mask", change_masks),
        ("comparison-sign", comparison_signatures),
    ):
        values = tuple(
            value
            for name in MESSAGE_ORDER
            for value in transform(streams[name][1:])
        )
        candidates.append(
            ChangeScore(
                len(zlib.compress(bytes(values), level=9)),
                run_count(values),
                route,
                len(values),
            )
        )
    return min(candidates, key=lambda score: (score.compressed_bytes, score.runs, score.route))


def next_occurrence_distances(values: Sequence[int]) -> tuple[int, ...]:
    """For each repeated occurrence, emit the forward distance to its next use."""

    next_position: dict[int, int] = {}
    reversed_output = []
    for position in range(len(values) - 1, -1, -1):
        value = values[position]
        if value in next_position:
            reversed_output.append(next_position[value] - position)
        next_position[value] = position
    return tuple(reversed(reversed_output))


def entropy(values: Sequence[int]) -> float:
    if not values:
        return 0.0
    counts = Counter(values)
    return -sum(
        count / len(values) * log2(count / len(values))
        for count in counts.values()
    )


@dataclass(frozen=True)
class PointerScore:
    compressed_bytes: int
    entropy: float
    events: int
    support: int


def pointer_score(streams: Mapping[str, Sequence[int]]) -> PointerScore:
    distances = tuple(
        distance
        for name in MESSAGE_ORDER
        for distance in next_occurrence_distances(streams[name][1:])
    )
    if max(distances, default=0) > 255:
        raise ValueError("pointer distance does not fit one byte")
    return PointerScore(
        len(zlib.compress(bytes(distances), level=9)),
        entropy(distances),
        len(distances),
        len(set(distances)),
    )


def ordinal_permutation(values: Sequence[int]) -> tuple[int, ...]:
    """Return the relative numeric order of distinct values."""

    if len(set(values)) != len(values):
        raise ValueError("ordinal permutation requires distinct values")
    ordered = sorted(values)
    ranks = {value: rank for rank, value in enumerate(ordered)}
    return tuple(ranks[value] for value in values)


@dataclass(frozen=True)
class OrdinalScore:
    matches: int
    initial_matches: int
    sliding_matches: int
    eligible_windows: int
    route: str


def ordinal_score(streams: Mapping[str, Sequence[int]]) -> OrdinalScore:
    """Select header or inverse as a six-value ordinal-pattern target."""

    candidates = []
    for route in ("header", "inverse"):
        initial_matches = sliding_matches = eligible = 0
        for name in MESSAGE_ORDER:
            body = streams[name][1:]
            header = lexicographic_unrank(streams[name][0])
            target = header if route == "header" else inverse(header)
            first_distinct = tuple(dict.fromkeys(body))[:6]
            initial_matches += ordinal_permutation(first_distinct) == target
            for start in range(len(body) - 5):
                window = body[start : start + 6]
                if len(set(window)) < 6:
                    continue
                eligible += 1
                sliding_matches += ordinal_permutation(window) == target
        candidates.append(
            OrdinalScore(
                initial_matches + sliding_matches,
                initial_matches,
                sliding_matches,
                eligible,
                route,
            )
        )
    return max(
        candidates,
        key=lambda score: (score.matches, score.initial_matches, score.route),
    )
