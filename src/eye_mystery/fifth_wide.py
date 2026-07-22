"""Bounded statistics for the fifth wide Eye-architecture fan-out."""

from __future__ import annotations

from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from itertools import permutations


def directed_edge_reuse(streams: Sequence[Sequence[int]]) -> tuple[int, int, int]:
    """Return repeated, total, and distinct directed-transition counts."""
    edges = [
        (left, right)
        for stream in streams
        for left, right in zip(stream, stream[1:])
    ]
    distinct = len(set(edges))
    return len(edges) - distinct, len(edges), distinct


@dataclass(frozen=True)
class CellularFit:
    correct: int
    samples: int
    radius: int
    shift: int
    contexts: int

    @property
    def accuracy(self) -> float:
        return self.correct / self.samples if self.samples else 0.0


@dataclass(frozen=True)
class CellularCrossValidation:
    correct: int
    covered: int
    samples: int

    @property
    def accuracy(self) -> float:
        return self.correct / self.covered if self.covered else 0.0

    @property
    def coverage(self) -> float:
        return self.covered / self.samples if self.samples else 0.0


def best_cellular_fit(
    row_pairs: Sequence[tuple[Sequence[int], Sequence[int]]],
    *,
    maximum_radius: int = 3,
    maximum_shift: int = 2,
) -> CellularFit:
    """Fit one deterministic top-neighborhood to shifted-bottom rule."""
    best = CellularFit(-1, 1, 0, 0, 0)
    for radius in range(maximum_radius + 1):
        for shift in range(-maximum_shift, maximum_shift + 1):
            followers: dict[tuple[int, ...], Counter[int]] = {}
            samples = 0
            for top, bottom in row_pairs:
                for center in range(radius, len(top) - radius):
                    target = center + shift
                    if not 0 <= target < len(bottom):
                        continue
                    context = tuple(top[center - radius : center + radius + 1])
                    followers.setdefault(context, Counter())[bottom[target]] += 1
                    samples += 1
            candidate = CellularFit(
                sum(max(counts.values()) for counts in followers.values()),
                samples,
                radius,
                shift,
                len(followers),
            )
            if candidate.accuracy > best.accuracy:
                best = candidate
    return best


def cellular_leave_one_pair_out(
    row_pairs: Sequence[tuple[Sequence[int], Sequence[int]]],
    *,
    radius: int,
    shift: int,
) -> CellularCrossValidation:
    """Test a fixed local rule only where other row pairs observed its context."""
    correct = covered = samples = 0
    for held_out, (test_top, test_bottom) in enumerate(row_pairs):
        followers: dict[tuple[int, ...], Counter[int]] = {}
        for pair_index, (top, bottom) in enumerate(row_pairs):
            if pair_index == held_out:
                continue
            for center in range(radius, len(top) - radius):
                target = center + shift
                if not 0 <= target < len(bottom):
                    continue
                context = tuple(top[center - radius : center + radius + 1])
                followers.setdefault(context, Counter())[bottom[target]] += 1
        for center in range(radius, len(test_top) - radius):
            target = center + shift
            if not 0 <= target < len(test_bottom):
                continue
            samples += 1
            context = tuple(
                test_top[center - radius : center + radius + 1]
            )
            if context not in followers:
                continue
            prediction = followers[context].most_common(1)[0][0]
            covered += 1
            correct += prediction == test_bottom[target]
    return CellularCrossValidation(correct, covered, samples)


def radix_values(digits: Sequence[int], source_base: int, target_base: int) -> tuple[int, ...]:
    """Interpret ``digits`` as one integer and expand it in ``target_base``."""
    if source_base < 2 or target_base < 2:
        raise ValueError("radices must be at least two")
    if any(not 0 <= digit < source_base for digit in digits):
        raise ValueError("digit outside source radix")
    value = 0
    for digit in digits:
        value = value * source_base + digit
    output = []
    while value:
        value, digit = divmod(value, target_base)
        output.append(digit)
    return tuple(reversed(output or [0]))


def printable_fraction(values: Sequence[int]) -> float:
    if not values:
        return 0.0
    return sum(value in (9, 10, 13) or 32 <= value <= 126 for value in values) / len(values)


@dataclass(frozen=True)
class RadixFit:
    fraction: float
    target_base: int
    reversed_digits: bool
    printable: int
    length: int


def best_radix_fit(streams: Sequence[Sequence[int]]) -> RadixFit:
    best = RadixFit(-1.0, 128, False, 0, 0)
    for target_base in (128, 256):
        for reversed_digits in (False, True):
            output = tuple(
                value
                for stream in streams
                for value in radix_values(
                    tuple(reversed(stream)) if reversed_digits else stream,
                    83,
                    target_base,
                )
            )
            printable = sum(
                value in (9, 10, 13) or 32 <= value <= 126 for value in output
            )
            candidate = RadixFit(
                printable / len(output),
                target_base,
                reversed_digits,
                printable,
                len(output),
            )
            if candidate.fraction > best.fraction:
                best = candidate
    return best


def base_five_digits(value: int) -> tuple[int, int, int]:
    if not 0 <= value < 125:
        raise ValueError("value outside a three-digit base-five word")
    return value // 25, (value // 5) % 5, value % 5


@dataclass(frozen=True)
class SortFit:
    agreement: int
    comparisons: int
    component_order: tuple[int, int, int]
    descending: bool

    @property
    def fraction(self) -> float:
        return self.agreement / self.comparisons if self.comparisons else 0.0


def inversion_count(values: Sequence[tuple[int, ...]]) -> int:
    return sum(
        values[left] > values[right]
        for left in range(len(values))
        for right in range(left + 1, len(values))
    )


def best_stable_sort_fit(rows: Sequence[Sequence[int]]) -> SortFit:
    """Select one component order and one global monotone orientation."""
    best = SortFit(-1, 1, (0, 1, 2), False)
    comparisons = sum(len(row) * (len(row) - 1) // 2 for row in rows)
    for order in permutations(range(3)):
        inversions = sum(
            inversion_count(
                tuple(
                    tuple(base_five_digits(value)[index] for index in order)
                    for value in row
                )
            )
            for row in rows
        )
        for descending, agreement in (
            (False, comparisons - inversions),
            (True, inversions),
        ):
            candidate = SortFit(agreement, comparisons, order, descending)
            if candidate.fraction > best.fraction:
                best = candidate
    return best


GRID_OPERATIONS = {
    "sum": lambda left, right: (left + right) % 5,
    "left-minus-right": lambda left, right: (left - right) % 5,
    "right-minus-left": lambda left, right: (right - left) % 5,
    "negative-sum": lambda left, right: (-left - right) % 5,
    "product": lambda left, right: left * right % 5,
    "half-sum": lambda left, right: 3 * (left + right) % 5,
    "minimum": min,
    "maximum": max,
}


@dataclass(frozen=True)
class GridFit:
    matches: int
    samples: int
    operation: str


GridRecord = tuple[int, int, int]


def best_grid_fit(records: Sequence[GridRecord]) -> GridFit:
    """Fit one digitwise operation to target/left/right value triples."""
    best = GridFit(-1, len(records), "")
    for name, operation in GRID_OPERATIONS.items():
        matches = 0
        for target, left, right in records:
            target_digits = base_five_digits(target)
            left_digits = base_five_digits(left)
            right_digits = base_five_digits(right)
            output = tuple(
                operation(left_digit, right_digit)
                for left_digit, right_digit in zip(
                    left_digits, right_digits, strict=True
                )
            )
            matches += output == target_digits
        candidate = GridFit(matches, len(records), name)
        if candidate.matches > best.matches:
            best = candidate
    return best


def turtle_bounding_area(directions: Sequence[int]) -> int:
    """Return the visited bounding-box area of native centre/cardinal moves."""
    moves = {0: (0, 0), 1: (0, -1), 2: (1, 0), 3: (0, 1), 4: (-1, 0)}
    if any(direction not in moves for direction in directions):
        raise ValueError("unknown Eye direction")
    x = y = 0
    minimum_x = maximum_x = 0
    minimum_y = maximum_y = 0
    for direction in directions:
        delta_x, delta_y = moves[direction]
        x += delta_x
        y += delta_y
        minimum_x = min(minimum_x, x)
        maximum_x = max(maximum_x, x)
        minimum_y = min(minimum_y, y)
        maximum_y = max(maximum_y, y)
    return (maximum_x - minimum_x + 1) * (maximum_y - minimum_y + 1)


def rotate(values: Sequence[int], amount: int) -> tuple[int, ...]:
    if not values:
        return ()
    amount %= len(values)
    return tuple(values[amount:]) + tuple(values[:amount])


def relabel_streams(
    streams: Mapping[str, Sequence[int]], mapping: Sequence[int]
) -> dict[str, tuple[int, ...]]:
    return {
        name: tuple(mapping[value] for value in stream)
        for name, stream in streams.items()
    }
