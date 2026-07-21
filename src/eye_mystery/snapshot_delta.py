"""Fixed-coordinate diagnostics for the Eye message sibling branches."""

from __future__ import annotations

from collections import Counter
from collections.abc import Mapping, Sequence
from itertools import combinations


DEEPEST_SIBLING_TRIOS = (
    ("east1", "west1", "east2"),
    ("east4", "west4", "east5"),
)

DEEPEST_EXIT_DEPTHS = {
    "east1": 24,
    "west1": 24,
    "east2": 24,
    "east4": 20,
    "west4": 20,
    "east5": 20,
}


def levenshtein_distance(left: Sequence[int], right: Sequence[int]) -> int:
    """Return unit-cost insertion, deletion, and substitution distance."""
    previous = list(range(len(right) + 1))
    for left_index, left_value in enumerate(left, 1):
        current = [left_index]
        for right_index, right_value in enumerate(right, 1):
            current.append(
                min(
                    current[-1] + 1,
                    previous[right_index] + 1,
                    previous[right_index - 1] + (left_value != right_value),
                )
            )
        previous = current
    return previous[-1]


def fixed_coordinate_cost(left: Sequence[int], right: Sequence[int]) -> int:
    """Cost of substitutions at fixed indices plus trailing truncation."""
    return sum(a != b for a, b in zip(left, right)) + abs(len(left) - len(right))


def gap_advantage(left: Sequence[int], right: Sequence[int]) -> int:
    """How many edits a free alignment saves over fixed coordinates."""
    return fixed_coordinate_cost(left, right) - levenshtein_distance(left, right)


def deepest_sibling_gap_advantages(
    streams: Mapping[str, Sequence[int]],
) -> tuple[int, ...]:
    """Return the six pairwise advantages in the two deepest sibling trios."""
    return tuple(
        gap_advantage(streams[left], streams[right])
        for trio in DEEPEST_SIBLING_TRIOS
        for left, right in combinations(trio, 2)
    )


def equality_runs(
    left: Sequence[int], right: Sequence[int], *, start: int
) -> tuple[tuple[int, int], ...]:
    """Return inclusive fixed-coordinate equality runs after a branch point."""
    matches = [
        index
        for index in range(start, min(len(left), len(right)))
        if left[index] == right[index]
    ]
    runs: list[list[int]] = []
    for index in matches:
        if not runs or index != runs[-1][-1] + 1:
            runs.append([index])
        else:
            runs[-1].append(index)
    return tuple((run[0], run[-1]) for run in runs)


def equality_partition(values: Sequence[int]) -> int:
    """Encode the five set partitions of three aligned values as ``0..4``.

    ``0`` is all equal; ``1``, ``2``, and ``3`` identify the equal pair
    ``01``, ``02``, or ``12``; and ``4`` is all distinct.
    """
    if len(values) != 3:
        raise ValueError("an equality partition needs exactly three values")
    first, second, third = values
    if first == second == third:
        return 0
    if first == second:
        return 1
    if first == third:
        return 2
    if second == third:
        return 3
    return 4


def partition_tape(streams: Sequence[Sequence[int]]) -> tuple[int, ...]:
    """Return five-state equality partitions at every shared coordinate."""
    if len(streams) != 3:
        raise ValueError("a partition tape needs exactly three streams")
    return tuple(equality_partition(values) for values in zip(*streams))


def deepest_equality_geometry(
    streams: Mapping[str, Sequence[int]], *, width: int = 26
) -> tuple[int, float, int, int]:
    """Summarize later equality columns and run ends for the sibling trios.

    The result is ``(hit_count, column_chi_square, run_end_count,
    near_record_edge_count)``.  A run start and end are both included, even for
    singleton runs, because both could have been an authored edit boundary.
    """
    if width < 4:
        raise ValueError("record width must be at least four")
    columns: list[int] = []
    run_ends: list[int] = []
    for trio in DEEPEST_SIBLING_TRIOS:
        start = DEEPEST_EXIT_DEPTHS[trio[0]]
        for left, right in combinations(trio, 2):
            columns.extend(
                index % width
                for index in range(
                    start, min(len(streams[left]), len(streams[right]))
                )
                if streams[left][index] == streams[right][index]
            )
            for run_start, run_end in equality_runs(
                streams[left], streams[right], start=start
            ):
                run_ends.extend((run_start % width, run_end % width))
    counts = Counter(columns)
    expected = len(columns) / width
    chi_square = (
        sum((counts[column] - expected) ** 2 / expected for column in range(width))
        if expected
        else 0.0
    )
    near_edges = {0, 1, width - 2, width - 1}
    return (
        len(columns),
        chi_square,
        len(run_ends),
        sum(column in near_edges for column in run_ends),
    )
