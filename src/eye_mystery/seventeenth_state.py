"""State-reconstruction probes from the seventeenth wide horizon."""

from __future__ import annotations

from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.factoradic_headers import P_MESSAGES
from eye_mystery.fifteenth_second import NATURAL_OPENING_TRIMS


SIZE = 83
Q_MESSAGES = tuple(name for name in MESSAGE_ORDER if name not in P_MESSAGES)


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
