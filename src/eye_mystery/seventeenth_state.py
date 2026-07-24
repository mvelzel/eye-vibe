"""State-reconstruction probes from the seventeenth wide horizon."""

from __future__ import annotations

import random
from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

import numpy as np

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.factoradic_headers import P_MESSAGES
from eye_mystery.fifteenth_second import NATURAL_OPENING_TRIMS


SIZE = 83
Q_MESSAGES = tuple(name for name in MESSAGE_ORDER if name not in P_MESSAGES)
HANKEL_DEPTHS = ((1, 1), (2, 1), (1, 2))
HANKEL_PRIMES = (83, 101, 257)


def eye_bodies(
    *,
    prefix_trimmed: bool,
) -> dict[str, tuple[int, ...]]:
    """Return markerless bodies, optionally after known copied openings."""

    bodies = {
        name: tuple(trigram_values(MESSAGES[name])[1:])
        for name in MESSAGE_ORDER
    }
    if not prefix_trimmed:
        return bodies
    return {
        name: body[NATURAL_OPENING_TRIMS[name] :]
        for name, body in bodies.items()
    }


def transition_matrix(
    streams: Mapping[str, Sequence[int]],
    names: Sequence[str],
    *,
    support: bool,
    size: int = SIZE,
) -> tuple[tuple[int, ...], ...]:
    """Build a directed support or multiplicity matrix."""

    counts: Counter[tuple[int, int]] = Counter(
        (left, right)
        for name in names
        for left, right in zip(streams[name], streams[name][1:])
    )
    return tuple(
        tuple(
            int((left, right) in counts)
            if support
            else counts[left, right]
            for right in range(size)
        )
        for left in range(size)
    )


def coarsest_equitable_partition(
    matrix: Sequence[Sequence[int]],
) -> tuple[tuple[int, ...], ...]:
    """Return the coarsest directed equitable partition by exact refinement."""

    size = len(matrix)
    if any(len(row) != size for row in matrix):
        raise ValueError("transition matrix must be square")
    colors = [0] * size
    while True:
        blocks = tuple(
            tuple(index for index, color in enumerate(colors) if color == value)
            for value in sorted(set(colors))
        )
        signatures = []
        for vertex in range(size):
            outgoing = tuple(
                sum(matrix[vertex][target] for target in block)
                for block in blocks
            )
            incoming = tuple(
                sum(matrix[source][vertex] for source in block)
                for block in blocks
            )
            signatures.append((colors[vertex], outgoing, incoming))
        ordered = {
            signature: index
            for index, signature in enumerate(sorted(set(signatures)))
        }
        refined = [ordered[signature] for signature in signatures]
        if refined == colors:
            break
        colors = refined
    return tuple(
        tuple(index for index, color in enumerate(colors) if color == value)
        for value in sorted(set(colors))
    )


def partition_is_equitable(
    matrix: Sequence[Sequence[int]],
    partition: Sequence[Sequence[int]],
) -> bool:
    """Check directed in/out block counts for every pair of fiber vertices."""

    for block in partition:
        if not block:
            return False
        reference = block[0]
        reference_signature = (
            tuple(
                sum(matrix[reference][target] for target in target_block)
                for target_block in partition
            ),
            tuple(
                sum(matrix[source][reference] for source in source_block)
                for source_block in partition
            ),
        )
        for vertex in block[1:]:
            signature = (
                tuple(
                    sum(matrix[vertex][target] for target in target_block)
                    for target_block in partition
                ),
                tuple(
                    sum(matrix[source][vertex] for source in source_block)
                    for source_block in partition
                ),
            )
            if signature != reference_signature:
                return False
    return True


@dataclass(frozen=True)
class FibrationAudit:
    support: bool
    prefix_trimmed: bool
    training_blocks: int
    training_singletons: int
    training_largest_block: int
    complete_blocks: int
    complete_singletons: int
    complete_largest_block: int
    training_partition_survives_complete: bool


def fibration_audit() -> tuple[FibrationAudit, ...]:
    """Audit P-selected and all-panel exact equitable quotients."""

    audits = []
    for prefix_trimmed in (False, True):
        streams = eye_bodies(prefix_trimmed=prefix_trimmed)
        for support in (True, False):
            training_matrix = transition_matrix(
                streams,
                P_MESSAGES,
                support=support,
            )
            complete_matrix = transition_matrix(
                streams,
                MESSAGE_ORDER,
                support=support,
            )
            training = coarsest_equitable_partition(training_matrix)
            complete = coarsest_equitable_partition(complete_matrix)
            audits.append(
                FibrationAudit(
                    support,
                    prefix_trimmed,
                    len(training),
                    sum(len(block) == 1 for block in training),
                    max(map(len, training)),
                    len(complete),
                    sum(len(block) == 1 for block in complete),
                    max(map(len, complete)),
                    partition_is_equitable(complete_matrix, training),
                )
            )
    return tuple(audits)


def planted_regular_cover(
    *,
    base_size: int = 5,
    fiber_size: int = 3,
) -> tuple[tuple[tuple[int, ...], ...], tuple[tuple[int, ...], ...]]:
    """Return a planted directed lift and its intended fiber partition."""

    if base_size < 2 or fiber_size < 2:
        raise ValueError("plant dimensions must both be at least two")
    size = base_size * fiber_size
    matrix = [[0] * size for _ in range(size)]
    for source_base in range(base_size):
        for target_base in range(source_base + 1):
            offset = (source_base + 2 * target_base) % fiber_size
            for fiber in range(fiber_size):
                source = source_base * fiber_size + fiber
                target = (
                    target_base * fiber_size
                    + (fiber + offset) % fiber_size
                )
                matrix[source][target] = 1
    partition = tuple(
        tuple(base * fiber_size + fiber for fiber in range(fiber_size))
        for base in range(base_size)
    )
    return tuple(tuple(row) for row in matrix), partition


Word = tuple[int, ...]


def reset_local_word_counts(
    streams: Mapping[str, Sequence[int]],
    names: Sequence[str],
    *,
    max_length: int,
) -> Counter[Word]:
    """Count words without allowing a word to cross a reset boundary."""

    if max_length < 0:
        raise ValueError("maximum word length cannot be negative")
    counts: Counter[Word] = Counter()
    counts[()] = sum(len(streams[name]) + 1 for name in names)
    for name in names:
        stream = tuple(streams[name])
        for length in range(1, max_length + 1):
            for start in range(len(stream) - length + 1):
                counts[stream[start : start + length]] += 1
    return counts


def hankel_vocabulary(
    counts: Mapping[Word, int],
    *,
    max_length: int,
) -> tuple[Word, ...]:
    """Return the empty word followed by observed words in lexical order."""

    return ((),) + tuple(
        sorted(
            word
            for word, count in counts.items()
            if count and 1 <= len(word) <= max_length
        )
    )


def empirical_hankel_matrix(
    streams: Mapping[str, Sequence[int]],
    names: Sequence[str],
    depth: tuple[int, int],
) -> tuple[tuple[int, ...], ...]:
    """Build one reset-local empirical Hankel block."""

    row_depth, column_depth = depth
    if row_depth < 1 or column_depth < 1:
        raise ValueError("Hankel depths must be positive")
    counts = reset_local_word_counts(
        streams,
        names,
        max_length=row_depth + column_depth,
    )
    rows = hankel_vocabulary(counts, max_length=row_depth)
    columns = hankel_vocabulary(counts, max_length=column_depth)
    return tuple(
        tuple(counts.get(prefix + suffix, 0) for suffix in columns)
        for prefix in rows
    )


def modular_rank(
    matrix: Sequence[Sequence[int]],
    prime: int,
) -> int:
    """Compute exact matrix rank over a prime field."""

    if prime < 2:
        raise ValueError("field modulus must be at least two")
    if not matrix:
        return 0
    width = len(matrix[0])
    if any(len(row) != width for row in matrix):
        raise ValueError("matrix must be rectangular")
    values = np.asarray(matrix, dtype=np.int64) % prime
    height = values.shape[0]
    rank = 0
    for column in range(width):
        candidates = np.flatnonzero(values[rank:, column])
        if not len(candidates):
            continue
        pivot = rank + int(candidates[0])
        if pivot != rank:
            values[[rank, pivot]] = values[[pivot, rank]]
        inverse = pow(int(values[rank, column]), -1, prime)
        values[rank] = values[rank] * inverse % prime
        if rank + 1 < height:
            factors = values[rank + 1 :, column].copy()
            values[rank + 1 :] = (
                values[rank + 1 :]
                - factors[:, np.newaxis] * values[rank]
            ) % prime
        rank += 1
        if rank == height:
            break
    return rank


@dataclass(frozen=True)
class HankelBlock:
    depth: tuple[int, int]
    rows: int
    columns: int
    ranks: tuple[int, ...]
    normalized_deficits: tuple[float, ...]
    score: float

    @property
    def all_fields_deficient(self) -> bool:
        return all(deficit > 0 for deficit in self.normalized_deficits)


@dataclass(frozen=True)
class HankelSplit:
    blocks: tuple[HankelBlock, ...]
    selected_depth: tuple[int, int]

    @property
    def selected(self) -> HankelBlock:
        return next(
            block for block in self.blocks
            if block.depth == self.selected_depth
        )

    @property
    def all_depths_and_fields_deficient(self) -> bool:
        return all(block.all_fields_deficient for block in self.blocks)


def evaluate_hankel_split(
    streams: Mapping[str, Sequence[int]],
    names: Sequence[str],
) -> HankelSplit:
    """Evaluate the complete frozen family on one panel split."""

    blocks = []
    for depth in HANKEL_DEPTHS:
        matrix = empirical_hankel_matrix(streams, names, depth)
        rows = len(matrix)
        columns = len(matrix[0]) if matrix else 0
        ranks = tuple(modular_rank(matrix, prime) for prime in HANKEL_PRIMES)
        denominator = min(rows, columns)
        deficits = tuple(
            1.0 - rank / denominator
            for rank in ranks
        )
        blocks.append(
            HankelBlock(
                depth,
                rows,
                columns,
                ranks,
                deficits,
                min(deficits),
            )
        )
    selected = max(
        blocks,
        key=lambda block: (block.score, -HANKEL_DEPTHS.index(block.depth)),
    )
    return HankelSplit(tuple(blocks), selected.depth)


def shuffle_without_adjacent_doubles(
    stream: Sequence[int],
    rng: random.Random,
    *,
    max_attempts: int = 10000,
) -> tuple[int, ...]:
    """Shuffle one multiset, rejecting arrangements with adjacent doubles."""

    source = tuple(stream)
    if any(
        count > (len(source) + 1) // 2
        for count in Counter(source).values()
    ):
        raise ValueError("no adjacent-double arrangement exists")
    candidate = list(source)
    for _ in range(max_attempts):
        rng.shuffle(candidate)
        if all(left != right for left, right in zip(candidate, candidate[1:])):
            return tuple(candidate)
    raise RuntimeError("failed to sample a no-adjacent-double shuffle")


def shuffled_streams(
    streams: Mapping[str, Sequence[int]],
    rng: random.Random,
) -> dict[str, tuple[int, ...]]:
    """Independently shuffle every registered message."""

    return {
        name: shuffle_without_adjacent_doubles(streams[name], rng)
        for name in MESSAGE_ORDER
    }


def periodic_hankel_plant(
    *,
    period: Sequence[int] | None = None,
) -> dict[str, tuple[int, ...]]:
    """Generate a deterministic low-state plant at the Eye body lengths."""

    if period is None:
        period = tuple(
            value
            for leaf in range(9, 27)
            for value in ((leaf - 9) % 9, leaf)
        )
    period = tuple(period)
    if len(period) < 2 or any(
        left == right
        for left, right in zip(period, period[1:] + period[:1])
    ):
        raise ValueError("plant period must be cyclically no-double")
    lengths = {
        name: len(body)
        for name, body in eye_bodies(prefix_trimmed=True).items()
    }
    return {
        name: tuple(
            period[(index + offset) % len(period)]
            for offset in range(lengths[name])
        )
        for index, name in enumerate(MESSAGE_ORDER)
    }


@dataclass(frozen=True)
class HankelAudit:
    training: HankelSplit
    heldout: HankelSplit
    controls: int
    exceedances: int
    corrected_upper_tail: float
    control_selected_depths: tuple[tuple[tuple[int, int], int], ...]
    heldout_rank_excess: int

    @property
    def passes_rank_gate(self) -> bool:
        return (
            self.training.selected.all_fields_deficient
            and self.heldout.selected.all_fields_deficient
            and self.corrected_upper_tail <= 0.01
            and self.heldout_rank_excess == 0
        )


def hankel_control_audit(
    streams: Mapping[str, Sequence[int]],
    *,
    controls: int = 200,
    seed: int = 0x17C0,
) -> HankelAudit:
    """Run the complete frozen P-selection/Q-transfer control."""

    if controls < 1:
        raise ValueError("at least one control is required")
    training = evaluate_hankel_split(streams, P_MESSAGES)
    heldout = evaluate_hankel_split(streams, Q_MESSAGES)
    real_score = heldout.selected.score
    rng = random.Random(seed)
    exceedances = 0
    selected_depths: Counter[tuple[int, int]] = Counter()
    for _ in range(controls):
        shuffled = shuffled_streams(streams, rng)
        control_training = evaluate_hankel_split(shuffled, P_MESSAGES)
        control_heldout = evaluate_hankel_split(shuffled, Q_MESSAGES)
        selected_depths[control_training.selected_depth] += 1
        control_score = next(
            block.score
            for block in control_heldout.blocks
            if block.depth == control_training.selected_depth
        )
        exceedances += control_score >= real_score

    p_dimension = max(training.blocks[0].ranks)
    q_dimension = max(heldout.blocks[0].ranks)
    return HankelAudit(
        training,
        heldout,
        controls,
        exceedances,
        (1 + exceedances) / (1 + controls),
        tuple(
            (depth, selected_depths[depth])
            for depth in HANKEL_DEPTHS
            if selected_depths[depth]
        ),
        max(0, q_dimension - p_dimension),
    )
