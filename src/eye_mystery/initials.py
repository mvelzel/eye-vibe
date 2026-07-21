"""Structural facts about the nine exceptional initial trigrams."""

from __future__ import annotations

from functools import reduce
from collections import Counter
from itertools import combinations, permutations, product
from math import gcd, prod
import random

from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, trigram_values


_DIRECTION_STEPS = {
    0: (0, 0),
    1: (-1, 0),
    2: (0, 1),
    3: (1, 0),
    4: (0, -1),
}


def initial_digits() -> tuple[tuple[int, int, int], ...]:
    return tuple(tuple(MESSAGES[name][:3]) for name in MESSAGE_ORDER)  # type: ignore[return-value]


def initial_values() -> tuple[int, ...]:
    return tuple(trigram_values(MESSAGES[name])[0] for name in MESSAGE_ORDER)


def message_sums() -> tuple[int, ...]:
    return tuple(sum(trigram_values(MESSAGES[name])) for name in MESSAGE_ORDER)


def body_sums() -> tuple[int, ...]:
    return tuple(
        sum(trigram_values(MESSAGES[name])[1:]) for name in MESSAGE_ORDER
    )


def triple_gcds() -> tuple[tuple[int, tuple[int, int, int]], ...]:
    totals = message_sums()
    return tuple(
        (reduce(gcd, (totals[index] for index in indices)), indices)
        for indices in combinations(range(len(totals)), 3)
    )


def falling(n: int, k: int) -> int:
    return prod(range(n - k + 1, n + 1))


def chain_null_probability() -> float:
    """Fixed-rule null for the seven links before the unpaired East 5 item.

    Values are independently uniform over the canonical 0..82 trigram set.
    The event at each link is first base-five digit = next middle digit + 1.
    """
    values = tuple(range(83))
    first = [value // 25 for value in values]
    middle = [(value // 5) % 5 for value in values]
    one_link = sum(a == b + 1 for a in first for b in middle) / 83**2
    return one_link**7


def circular_successor_links() -> tuple[bool, ...]:
    """Test the marker rule on all nine circular canonical-order edges."""

    digits = initial_digits()
    return tuple(
        digits[index][0] == digits[(index + 1) % len(digits)][1] + 1
        for index in range(len(digits))
    )


def perfect_successor_rotation() -> tuple[str, ...] | None:
    """Return the unique cyclic rotation whose eight linear links all work."""

    digits = initial_digits()
    solutions = []
    for rotation in range(len(digits)):
        order = tuple(range(rotation, len(digits))) + tuple(range(rotation))
        if all(
            digits[order[index]][0]
            == digits[order[index + 1]][1] + 1
            for index in range(len(order) - 1)
        ):
            solutions.append(tuple(MESSAGE_ORDER[index] for index in order))
    return solutions[0] if len(solutions) == 1 else None


def trace_marker_digit(
    start_name: str, digit_index: int
) -> tuple[tuple[str, ...], int | None]:
    """Follow one marker-eye direction through the canonical 3x3 panel grid.

    The returned direction is the eye value that leaves the grid, or ``None``
    when the route reaches a stationary cell or a cycle.
    """

    if start_name not in MESSAGE_ORDER:
        raise ValueError(f"unknown message: {start_name}")
    if digit_index not in range(3):
        raise ValueError("digit index must be 0, 1, or 2")
    digits = dict(zip(MESSAGE_ORDER, initial_digits(), strict=True))
    position = divmod(MESSAGE_ORDER.index(start_name), 3)
    path: list[str] = []
    visited: set[tuple[int, int]] = set()
    while position not in visited:
        visited.add(position)
        index = 3 * position[0] + position[1]
        name = MESSAGE_ORDER[index]
        path.append(name)
        direction = digits[name][digit_index]
        row_step, column_step = _DIRECTION_STEPS[direction]
        if (row_step, column_step) == (0, 0):
            return tuple(path), None
        next_position = position[0] + row_step, position[1] + column_step
        if not (0 <= next_position[0] < 3 and 0 <= next_position[1] < 3):
            return tuple(path), direction
        position = next_position
    return tuple(path), None


def marker_grid_exit_signatures() -> tuple[
    tuple[int | None, int | None, int | None], ...
]:
    """Return the three route exits for every start in the 3x3 grid."""

    return tuple(
        tuple(trace_marker_digit(name, digit)[1] for digit in range(3))
        for name in MESSAGE_ORDER
    )  # type: ignore[return-value]


def _grid_exit_direction(
    digits: tuple[tuple[int, int, int], ...],
    start: int,
    digit_index: int,
) -> int | None:
    position = divmod(start, 3)
    visited = set()
    while position not in visited:
        visited.add(position)
        direction = digits[3 * position[0] + position[1]][digit_index]
        row_step, column_step = _DIRECTION_STEPS[direction]
        if (row_step, column_step) == (0, 0):
            return None
        next_position = (
            position[0] + row_step,
            position[1] + column_step,
        )
        if not (
            0 <= next_position[0] < 3 and 0 <= next_position[1] < 3
        ):
            return direction
        position = next_position
    return None


def _grid_exit_signature(
    digits: tuple[tuple[int, int, int], ...], start: int
) -> tuple[int | None, int | None, int | None]:
    return tuple(
        _grid_exit_direction(digits, start, digit) for digit in range(3)
    )  # type: ignore[return-value]


def marker_grid_permutation_null_counts(
    *, hold_east5_marker: bool = False
) -> tuple[int, tuple[int, ...], int]:
    """Exact marker-shuffle null for the post-hoc ``NES`` grid event.

    The first count is the number of assignments where the fixed East 5 grid
    cell exits north/east/south.  The histogram counts assignments by the
    number of all nine starting cells with that signature.  Optionally the
    observed East 5 marker is held in its cell while the other eight move.
    """

    observed = initial_digits()
    if hold_east5_marker:
        assignments = (
            assignment + (observed[-1],)
            for assignment in permutations(observed[:-1])
        )
    else:
        assignments = permutations(observed)
    target = (1, 2, 3)
    fixed_start = 0
    histogram = [0] * 10
    total = 0

    for assignment in assignments:
        complete = sum(
            _grid_exit_signature(assignment, start) == target
            for start in range(9)
        )
        fixed_start += _grid_exit_signature(assignment, 8) == target
        histogram[complete] += 1
        total += 1
    return fixed_start, tuple(histogram), total


def simulate_marker_grid_events(
    trials: int, *, seed: int = 20260721
) -> tuple[int, int, int, int]:
    """Simulate fixed and increasingly post-hoc marker-grid route events."""

    if trials < 1:
        raise ValueError("trials must be positive")
    rng = random.Random(seed)
    target = (1, 2, 3)
    fixed = 0
    any_start = 0
    three_target_starts = 0
    three_equal_distinct_exits = 0
    for _ in range(trials):
        digits = tuple(
            (value // 25, (value // 5) % 5, value % 5)
            for value in rng.sample(range(83), 9)
        )
        signatures = tuple(
            _grid_exit_signature(digits, start) for start in range(9)
        )
        target_count = signatures.count(target)
        fixed += signatures[8] == target
        any_start += target_count > 0
        three_target_starts += target_count >= 3
        distinct_exit_counts = Counter(
            signature
            for signature in signatures
            if None not in signature and len(set(signature)) == 3
        )
        three_equal_distinct_exits += bool(
            distinct_exit_counts
            and max(distinct_exit_counts.values()) >= 3
        )
    return (
        fixed,
        any_start,
        three_target_starts,
        three_equal_distinct_exits,
    )


def circular_chain_event_counts() -> tuple[int, int]:
    """Exact null count for at least eight of nine circular fixed-rule links.

    The 83 trigrams occupy 17 `(first, middle)` digit categories.  Fifteen
    categories have five possible final digits; `(3,0)` has five and `(3,1)`
    has three.  Enumerating only category sequences with eight or nine forced
    links gives an exact without-replacement count.
    """

    multiplicities = {
        (first, middle): 5
        for first in range(3)
        for middle in range(5)
    }
    multiplicities[3, 0] = 5
    multiplicities[3, 1] = 3

    def weight(categories: tuple[tuple[int, int], ...]) -> int:
        counts = Counter(categories)
        return prod(
            falling(multiplicities.get(category, 0), count)
            for category, count in counts.items()
        )

    all_nine = sum(
        weight(
            tuple(
                (first_digits[index], first_digits[index - 1] - 1)
                for index in range(9)
            )
        )
        for first_digits in product((1, 2, 3), repeat=9)
    )

    # Force edges 0→1 through 7→8 and require the closing 8→0 edge to fail.
    one_designated_failure = 0
    for first_eight in product((1, 2, 3), repeat=8):
        for first_middle in range(5):
            for final_first in range(4):
                if final_first == first_middle + 1:
                    continue
                categories = (
                    (first_eight[0], first_middle),
                    *(
                        (first_eight[index], first_eight[index - 1] - 1)
                        for index in range(1, 8)
                    ),
                    (final_first, first_eight[7] - 1),
                )
                one_designated_failure += weight(categories)

    favorable = all_nine + 9 * one_designated_failure
    return favorable, falling(83, 9)


def simulate_any_circular_digit_rule(
    trials: int, *, seed: int = 20260721
) -> tuple[int, int]:
    """Count fixed and post-hoc digit-rule events in random marker sets."""

    if trials < 1:
        raise ValueError("trials must be positive")
    rng = random.Random(seed)
    fixed = 0
    any_rule = 0
    for _ in range(trials):
        digits = tuple(
            (value // 25, (value // 5) % 5, value % 5)
            for value in rng.sample(range(83), 9)
        )
        fixed += (
            sum(
                digits[index][0]
                == digits[(index + 1) % 9][1] + 1
                for index in range(9)
            )
            >= 8
        )
        found = False
        for left_digit in range(3):
            for right_digit in range(3):
                deltas = Counter(
                    digits[index][left_digit]
                    - digits[(index + 1) % 9][right_digit]
                    for index in range(9)
                )
                if max(deltas.values()) >= 8:
                    found = True
                    break
            if found:
                break
        any_rule += found
    return fixed, any_rule


def marker_summary() -> dict[str, object]:
    values = initial_values()
    digits = initial_digits()
    eligible_gcd = [value for value in range(83) if gcd(value, 66) > 1]
    gcd_results = triple_gcds()
    largest_triple_gcd = max(value for value, _ in gcd_results)
    checksum_targets = tuple((-total) % 101 for total in body_sums())
    return {
        "digits": digits,
        "values": values,
        "all_above_26": all(value > 26 for value in values),
        "above_26_without_replacement_probability": falling(56, 9) / falling(83, 9),
        "gcd_with_66": tuple(gcd(value, 66) for value in values),
        "gcd_without_replacement_probability": falling(len(eligible_gcd), 9)
        / falling(83, 9),
        "seven_link_chain": tuple(
            digits[index][0] == digits[index + 1][1] + 1
            for index in range(7)
        ),
        "last_link": digits[7][0] == digits[8][1] + 1,
        "chain_null_probability": chain_null_probability(),
        "circular_successor_links": circular_successor_links(),
        "perfect_successor_rotation": perfect_successor_rotation(),
        "circular_chain_event_counts": circular_chain_event_counts(),
        "message_sums": message_sums(),
        "sums_divisible_by_101": tuple(
            MESSAGE_ORDER[index]
            for index, total in enumerate(message_sums())
            if total % 101 == 0
        ),
        "largest_triple_gcd": largest_triple_gcd,
        "largest_triple_gcd_groups": tuple(
            tuple(MESSAGE_ORDER[index] for index in indices)
            for value, indices in gcd_results
            if value == largest_triple_gcd
        ),
        "body_checksum_targets_mod_101": checksum_targets,
        "marker_checksum_offsets_mod_101": tuple(
            (marker - target) % 101
            for marker, target in zip(values, checksum_targets, strict=True)
        ),
    }
