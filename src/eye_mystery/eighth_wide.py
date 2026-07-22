"""Structural probes for the eighth breadth-first Eye-cipher batch."""

from __future__ import annotations

from collections import Counter, defaultdict, deque
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from eye_mystery.corpus import MESSAGE_ORDER, ROW_PAIR_TRIGRAM_LENGTHS
from eye_mystery.seventh_wide import base5_digits


VISIBLE = frozenset(range(83))


@dataclass(frozen=True)
class CodebookScore:
    minimum_distance: int
    distance_one_pairs: int
    valid_splices: int
    splices: int
    distinct_splice_words: int


def codebook_score() -> CodebookScore:
    """Audit Hamming distance and cross-boundary closure of values 0..82."""

    words = {value: base5_digits(value) for value in VISIBLE}
    distances = Counter()
    for left in range(83):
        for right in range(left + 1, 83):
            distance = sum(
                first != second
                for first, second in zip(words[left], words[right], strict=True)
            )
            distances[distance] += 1

    valid = 0
    splice_words = set()
    for left in range(83):
        for right in range(83):
            first = words[left][1:] + words[right][:1]
            second = words[left][2:] + words[right][:2]
            for word in (first, second):
                value = 25 * word[0] + 5 * word[1] + word[2]
                valid += value in VISIBLE
                splice_words.add(value)
    return CodebookScore(
        min(distances),
        distances[1],
        valid,
        2 * 83 * 83,
        len(splice_words),
    )


def accepted_rows(
    streams: Mapping[str, Sequence[int]], *, length: int
) -> tuple[tuple[int, ...], ...]:
    """Return accepted-order authored records with exactly ``length`` tokens."""

    result = []
    for name in MESSAGE_ORDER:
        cursor = 0
        for row_length in ROW_PAIR_TRIGRAM_LENGTHS[name]:
            row = tuple(streams[name][cursor : cursor + row_length])
            if len(row) != row_length:
                raise ValueError("record lengths exceed message")
            cursor += row_length
            if row_length == length:
                result.append(row)
        if cursor != len(streams[name]):
            raise ValueError("record lengths do not consume message")
    return tuple(result)


@dataclass(frozen=True)
class PacketScore:
    unique_26: int
    records_26: int
    unique_83: int
    blocks_83: int


def packet_score(streams: Mapping[str, Sequence[int]]) -> PacketScore:
    """Count coupon coverage in frozen 26- and 83-token packets."""

    records = accepted_rows(streams, length=26)
    blocks = tuple(tuple(streams[name][1:84]) for name in MESSAGE_ORDER)
    if any(len(block) != 83 for block in blocks):
        raise ValueError("every body must contain one complete phase-zero 83 block")
    return PacketScore(
        sum(len(set(record)) for record in records),
        len(records),
        sum(len(set(block)) for block in blocks),
        len(blocks),
    )


class DisjointSet:
    def __init__(self, size: int) -> None:
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, value: int) -> int:
        while self.parent[value] != value:
            self.parent[value] = self.parent[self.parent[value]]
            value = self.parent[value]
        return value

    def union(self, left: int, right: int) -> None:
        left = self.find(left)
        right = self.find(right)
        if left == right:
            return
        if self.rank[left] < self.rank[right]:
            left, right = right, left
        self.parent[right] = left
        if self.rank[left] == self.rank[right]:
            self.rank[left] += 1


@dataclass(frozen=True)
class CocycleScore:
    repeated_bigram_types: int
    repeated_bigram_occurrences: int
    quotient_nodes: int
    constraints: int
    components: int
    contradictions: int


def cocycle_score(
    streams: Mapping[str, Sequence[int]], *, modulus: int = 101
) -> CocycleScore:
    """Test whether repeated-bigram state identifications admit a potential."""

    bodies = {name: tuple(streams[name][1:]) for name in MESSAGE_ORDER}
    starts: dict[str, int] = {}
    cursor = 0
    for name in MESSAGE_ORDER:
        starts[name] = cursor
        cursor += len(bodies[name]) + 1
    dsu = DisjointSet(cursor)

    occurrences: dict[tuple[int, int], list[tuple[str, int]]] = defaultdict(list)
    for name in MESSAGE_ORDER:
        for position, pair in enumerate(zip(bodies[name], bodies[name][1:])):
            occurrences[pair].append((name, position))
    repeated = {pair: items for pair, items in occurrences.items() if len(items) > 1}
    for items in repeated.values():
        reference_name, reference_position = items[0]
        reference = starts[reference_name] + reference_position
        for name, position in items[1:]:
            node = starts[name] + position
            for offset in range(3):
                dsu.union(reference + offset, node + offset)

    roots = {dsu.find(index) for index in range(cursor)}
    root_ids = {root: index for index, root in enumerate(sorted(roots))}
    constraints = set()
    for name in MESSAGE_ORDER:
        for position, value in enumerate(bodies[name]):
            left = root_ids[dsu.find(starts[name] + position)]
            right = root_ids[dsu.find(starts[name] + position + 1)]
            constraints.add((left, right, value % modulus))

    adjacency: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for left, right, weight in constraints:
        adjacency[left].append((right, weight))
        adjacency[right].append((left, -weight % modulus))
    potentials: dict[int, int] = {}
    components = 0
    for start in range(len(root_ids)):
        if start in potentials:
            continue
        components += 1
        potentials[start] = 0
        queue = deque((start,))
        while queue:
            left = queue.popleft()
            for right, weight in adjacency[left]:
                expected = (potentials[left] + weight) % modulus
                if right not in potentials:
                    potentials[right] = expected
                    queue.append(right)

    contradictions = sum(
        (potentials[right] - potentials[left] - weight) % modulus != 0
        for left, right, weight in constraints
    )
    return CocycleScore(
        len(repeated),
        sum(len(items) for items in repeated.values()),
        len(root_ids),
        len(constraints),
        components,
        contradictions,
    )


def nonoverlapping_pair_count(
    sequences: Sequence[Sequence[int]], pair: tuple[int, int]
) -> int:
    count = 0
    for sequence in sequences:
        index = 0
        while index + 1 < len(sequence):
            if (sequence[index], sequence[index + 1]) == pair:
                count += 1
                index += 2
            else:
                index += 1
    return count


def nonoverlapping_pair_counts(
    sequences: Sequence[Sequence[int]],
) -> Counter[tuple[int, int]]:
    """Count every pair under the same left-to-right replacement policy.

    Occurrences of ``(a,b)`` cannot overlap unless ``a == b``. Distinct-token
    pairs can therefore use their adjacent counts directly; equal-token pairs
    contribute ``floor(run_length/2)`` per maximal run.
    """

    result: Counter[tuple[int, int]] = Counter()
    for sequence in sequences:
        result.update(
            (left, right)
            for left, right in zip(sequence, sequence[1:])
            if left != right
        )
        start = 0
        while start < len(sequence):
            end = start + 1
            while end < len(sequence) and sequence[end] == sequence[start]:
                end += 1
            replacements = (end - start) // 2
            if replacements:
                result[(sequence[start], sequence[start])] += replacements
            start = end
    return result


def replace_pair(
    sequences: Sequence[Sequence[int]], pair: tuple[int, int], symbol: int
) -> tuple[tuple[int, ...], ...]:
    output = []
    for sequence in sequences:
        rewritten = []
        index = 0
        while index < len(sequence):
            if index + 1 < len(sequence) and (
                sequence[index], sequence[index + 1]
            ) == pair:
                rewritten.append(symbol)
                index += 2
            else:
                rewritten.append(sequence[index])
                index += 1
        output.append(tuple(rewritten))
    return tuple(output)


@dataclass(frozen=True)
class GrammarScore:
    original_symbols: int
    final_stream_symbols: int
    rules: int
    encoded_symbols: int
    savings: int


def repair_score(streams: Mapping[str, Sequence[int]]) -> GrammarScore:
    """Run deterministic net-positive RePair across nine separate bodies."""

    sequences = tuple(tuple(streams[name][1:]) for name in MESSAGE_ORDER)
    original = sum(map(len, sequences))
    next_symbol = 83
    rules = 0
    while True:
        counts = nonoverlapping_pair_counts(sequences)
        if not counts:
            break
        count, pair = min(
            ((count, pair) for pair, count in counts.items()),
            key=lambda item: (-item[0], item[1]),
        )
        if count < 3:
            break
        sequences = replace_pair(sequences, pair, next_symbol)
        next_symbol += 1
        rules += 1
    final_stream = sum(map(len, sequences))
    encoded = final_stream + 2 * rules
    return GrammarScore(original, final_stream, rules, encoded, original - encoded)
