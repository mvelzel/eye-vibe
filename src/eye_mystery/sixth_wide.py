"""Low-capacity probes for the sixth breadth-first Eye expansion."""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from itertools import permutations
from math import log

from .affine_embedding import Context


def fixed_width_digits(value: int, base: int, width: int) -> tuple[int, ...]:
    """Return one fixed-width most-significant-first digit vector."""

    if base < 2 or width < 1 or not 0 <= value < base**width:
        raise ValueError("value does not fit the requested digit vector")
    output = [0] * width
    for index in range(width - 1, -1, -1):
        output[index] = value % base
        value //= base
    return tuple(output)


def linear_system_consistent(
    coefficients: Sequence[Sequence[int]],
    targets: Sequence[int],
    modulus: int,
) -> bool:
    """Test consistency by row-reducing an augmented matrix over a prime."""

    if len(coefficients) != len(targets):
        raise ValueError("coefficient and target row counts differ")
    if not coefficients:
        return True
    width = len(coefficients[0])
    if any(len(row) != width for row in coefficients):
        raise ValueError("coefficient rows have different widths")
    matrix = [
        [value % modulus for value in row] + [target % modulus]
        for row, target in zip(coefficients, targets, strict=True)
    ]
    pivot_row = 0
    for column in range(width):
        pivot = next(
            (row for row in range(pivot_row, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        inverse = pow(matrix[pivot_row][column], -1, modulus)
        matrix[pivot_row] = [value * inverse % modulus for value in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or matrix[row][column] == 0:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                (left - factor * right) % modulus
                for left, right in zip(matrix[row], matrix[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return not any(
        all(value == 0 for value in row[:width]) and row[width] != 0
        for row in matrix
    )


@dataclass(frozen=True)
class LiteralAffineFit:
    context: str
    pairs: int
    sentinel_edges: int
    consistent: bool


def literal_affine_context_fit(
    context: Context,
    *,
    modulus: int,
    dimension: int,
    label_limit: int | None = None,
) -> LiteralAffineFit:
    """Fit ``y=A*x+b`` to literal digit coordinates in one context.

    Edges touching labels at or above ``label_limit`` are reported as
    sentinels and omitted. By default every point in the complete vector space
    is eligible.
    """

    space = modulus**dimension
    limit = space if label_limit is None else label_limit
    eligible = tuple(
        (left, right)
        for left, right in context.pairs
        if left < limit and right < limit
    )
    sentinels = len(context.pairs) - len(eligible)
    coefficients = [
        fixed_width_digits(left, modulus, dimension) + (1,)
        for left, _ in eligible
    ]
    targets = [fixed_width_digits(right, modulus, dimension) for _, right in eligible]
    consistent = all(
        linear_system_consistent(
            coefficients,
            [target[coordinate] for target in targets],
            modulus,
        )
        for coordinate in range(dimension)
    )
    return LiteralAffineFit(context.name, len(eligible), sentinels, consistent)


def polynomial_hash(values: Sequence[int], base: int, modulus: int) -> int:
    """Return ``sum(values[i] * base**i)`` modulo ``modulus``."""

    total = 0
    power = 1
    for value in values:
        total = (total + value * power) % modulus
        power = power * base % modulus
    return total


@dataclass(frozen=True)
class PolynomialRule:
    matches: int
    modulus: int
    reverse: bool
    kind: str
    base: int | None
    sign: int | None


def best_polynomial_header_rule(
    streams: Sequence[Sequence[int]],
) -> PolynomialRule:
    """Select the frozen global-base and header-as-root rule family."""

    if any(len(stream) < 2 for stream in streams):
        raise ValueError("every stream needs a header and body")
    best = PolynomialRule(-1, 83, False, "", None, None)
    for modulus in (83, 101):
        for reverse in (False, True):
            directed = [tuple(reversed(stream[1:])) if reverse else tuple(stream[1:]) for stream in streams]
            for base in range(modulus):
                hashes = [polynomial_hash(body, base, modulus) for body in directed]
                for sign in (-1, 1):
                    matches = sum(
                        (stream[0] + sign * body_hash) % modulus == 0
                        for stream, body_hash in zip(streams, hashes, strict=True)
                    )
                    candidate = PolynomialRule(
                        matches, modulus, reverse, "global-base", base, sign
                    )
                    if candidate.matches > best.matches:
                        best = candidate
            matches = sum(
                polynomial_hash(body, stream[0] % modulus, modulus) == 0
                for stream, body in zip(streams, directed, strict=True)
            )
            candidate = PolynomialRule(
                matches, modulus, reverse, "header-root", None, None
            )
            if candidate.matches > best.matches:
                best = candidate
    return best


@dataclass(frozen=True)
class CompletionFit:
    missing: int
    transitions: int
    constant: int
    component_order: tuple[int, int, int]

    @property
    def fraction(self) -> float:
        return self.missing / self.transitions if self.transitions else 0.0


def best_missing_completion(
    streams: Iterable[Sequence[int]],
) -> CompletionFit:
    """Select ``z=k-x-y`` and a component order by missing-cube hits."""

    pairs = tuple(
        (left, right)
        for stream in streams
        for left, right in zip(stream, stream[1:])
    )
    best = CompletionFit(-1, len(pairs), 0, (0, 1, 2))
    for constant in range(5):
        for order in permutations(range(3)):
            missing = 0
            for left, right in pairs:
                left_digits = fixed_width_digits(left, 5, 3)
                right_digits = fixed_width_digits(right, 5, 3)
                result = tuple(
                    (constant - left_digits[index] - right_digits[index]) % 5
                    for index in order
                )
                value = 25 * result[0] + 5 * result[1] + result[2]
                missing += value >= 83
            candidate = CompletionFit(missing, len(pairs), constant, order)
            if candidate.missing > best.missing:
                best = candidate
    return best


def erase_neutral_word(value: int, neutral: int = 0) -> tuple[int, ...]:
    """Delete a neutral direction from one base-five trigram."""

    return tuple(
        digit for digit in fixed_width_digits(value, 5, 3) if digit != neutral
    )


def cancel_direction_word(value: int) -> tuple[int, ...]:
    """Delete centre and freely cancel native opposite directions."""

    inverse = {1: 3, 3: 1, 2: 4, 4: 2}
    stack: list[int] = []
    for digit in erase_neutral_word(value):
        if stack and inverse[digit] == stack[-1]:
            stack.pop()
        else:
            stack.append(digit)
    return tuple(stack)


@dataclass(frozen=True)
class WordInventory:
    full_classes: int
    visible_classes: int
    unused_classes: int
    shared_classes: int


def word_inventory(reducer) -> WordInventory:
    full = {reducer(value) for value in range(125)}
    visible = {reducer(value) for value in range(83)}
    unused = {reducer(value) for value in range(83, 125)}
    return WordInventory(len(full), len(visible), len(unused), len(visible & unused))


def column_label_mutual_information(rows: Sequence[Sequence[int]]) -> float:
    """Mutual information between fixed column index and numeric label."""

    if not rows:
        return 0.0
    width = len(rows[0])
    if width < 1 or any(len(row) != width for row in rows):
        raise ValueError("rows must be nonempty and equally wide")
    joint = Counter(
        (column, label)
        for row in rows
        for column, label in enumerate(row)
    )
    label_counts = Counter(label for row in rows for label in row)
    total = len(rows) * width
    information = 0.0
    for (column, label), count in joint.items():
        joint_probability = count / total
        column_probability = 1 / width
        label_probability = label_counts[label] / total
        information += joint_probability * log(
            joint_probability / (column_probability * label_probability), 2
        )
    return information


def column_collision_score(
    training: Sequence[Sequence[int]],
    held_out: Sequence[Sequence[int]],
) -> int:
    """Score held-out cells by same-column label counts in training rows."""

    if not training or not held_out:
        return 0
    width = len(training[0])
    if any(len(row) != width for row in tuple(training) + tuple(held_out)):
        raise ValueError("training and held-out rows must share one width")
    counts = Counter(
        (column, label)
        for row in training
        for column, label in enumerate(row)
    )
    return sum(
        counts[column, label]
        for row in held_out
        for column, label in enumerate(row)
    )


def relabel_streams(
    streams: Mapping[str, Sequence[int]], mapping: Sequence[int]
) -> dict[str, tuple[int, ...]]:
    return {
        name: tuple(mapping[value] for value in stream)
        for name, stream in streams.items()
    }
