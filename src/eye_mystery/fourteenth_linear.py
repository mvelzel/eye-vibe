"""Exact shared linear-generator tests for the fourteenth Eye horizon."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from itertools import permutations

from eye_mystery.fourteenth_selector import base5_digits


@dataclass(frozen=True)
class LinearRepresentation:
    name: str
    modulus: int


@dataclass(frozen=True)
class LinearSystemResult:
    consistent: bool
    rank: int
    augmented_rank: int
    variables: int
    equations: int
    solution: tuple[int, ...] | None

    @property
    def unique(self) -> bool:
        return self.consistent and self.rank == self.variables


@dataclass(frozen=True)
class RecurrenceFit:
    representation: LinearRepresentation
    order: int
    system: LinearSystemResult
    heldout_matches: int
    heldout_equations: int

    @property
    def heldout_fraction(self) -> float:
        if not self.heldout_equations:
            return 0.0
        return self.heldout_matches / self.heldout_equations


def representations() -> tuple[LinearRepresentation, ...]:
    return (
        LinearRepresentation("rank-f83", 83),
        LinearRepresentation("difference-f83", 83),
        *(
            LinearRepresentation(
                "digits-" + "".join(map(str, order)) + "-f5",
                5,
            )
            for order in permutations(range(3))
        ),
    )


def render_representation(
    values: Sequence[int], representation: LinearRepresentation
) -> tuple[int, ...]:
    if representation.name == "rank-f83":
        if any(value not in range(83) for value in values):
            raise ValueError("rank representation requires values 0..82")
        return tuple(values)
    if representation.name == "difference-f83":
        if any(value not in range(83) for value in values):
            raise ValueError("rank representation requires values 0..82")
        return tuple(
            (right - left) % 83
            for left, right in zip(values, values[1:])
        )
    if representation.name.startswith("digits-"):
        order_text = representation.name.removeprefix("digits-").split("-")[0]
        order = tuple(map(int, order_text))
        if sorted(order) != [0, 1, 2]:
            raise ValueError("digit representation has invalid component order")
        return tuple(
            digit
            for value in values
            for digit in (
                base5_digits(value)[index]
                for index in order
            )
        )
    raise ValueError(f"unknown representation: {representation.name}")


def _row_reduce(
    rows: Sequence[Sequence[int]],
    rhs: Sequence[int],
    modulus: int,
) -> LinearSystemResult:
    if len(rows) != len(rhs):
        raise ValueError("row and right-hand-side counts differ")
    variables = len(rows[0]) if rows else 0
    if any(len(row) != variables for row in rows):
        raise ValueError("coefficient rows have different widths")
    matrix = [
        [value % modulus for value in row] + [target % modulus]
        for row, target in zip(rows, rhs, strict=True)
    ]
    pivot_columns: list[int] = []
    pivot_row = 0
    for column in range(variables):
        selected = next(
            (
                row
                for row in range(pivot_row, len(matrix))
                if matrix[row][column] % modulus
            ),
            None,
        )
        if selected is None:
            continue
        matrix[pivot_row], matrix[selected] = (
            matrix[selected],
            matrix[pivot_row],
        )
        inverse = pow(matrix[pivot_row][column], -1, modulus)
        matrix[pivot_row] = [
            value * inverse % modulus
            for value in matrix[pivot_row]
        ]
        for row in range(len(matrix)):
            if row == pivot_row:
                continue
            factor = matrix[row][column] % modulus
            if factor:
                matrix[row] = [
                    (left - factor * right) % modulus
                    for left, right in zip(
                        matrix[row], matrix[pivot_row], strict=True
                    )
                ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == len(matrix):
            break

    inconsistent = any(
        all(value % modulus == 0 for value in row[:-1])
        and row[-1] % modulus != 0
        for row in matrix
    )
    augmented_rank = len(pivot_columns) + int(inconsistent)
    solution = None
    if not inconsistent:
        values = [0] * variables
        for row, column in enumerate(pivot_columns):
            values[column] = matrix[row][-1] % modulus
        solution = tuple(values)
    return LinearSystemResult(
        not inconsistent,
        len(pivot_columns),
        augmented_rank,
        variables,
        len(rows),
        solution,
    )


def recurrence_system(
    streams: Sequence[Sequence[int]],
    order: int,
    modulus: int,
) -> LinearSystemResult:
    """Solve one homogeneous-coefficient recurrence shared by all streams."""

    if order < 1:
        raise ValueError("recurrence order must be positive")
    rows = []
    rhs = []
    for stream in streams:
        if any(value not in range(modulus) for value in stream):
            raise ValueError("stream value lies outside the finite field")
        for index in range(order, len(stream)):
            rows.append(
                tuple(
                    stream[index - lag]
                    for lag in range(1, order + 1)
                )
            )
            rhs.append(stream[index])
    return _row_reduce(rows, rhs, modulus)


def recurrence_matches(
    streams: Sequence[Sequence[int]],
    coefficients: Sequence[int],
    modulus: int,
) -> tuple[int, int]:
    matches = 0
    equations = 0
    order = len(coefficients)
    for stream in streams:
        for index in range(order, len(stream)):
            predicted = sum(
                coefficient * stream[index - lag]
                for lag, coefficient in enumerate(coefficients, start=1)
            ) % modulus
            matches += predicted == stream[index]
            equations += 1
    return matches, equations


def fit_shared_recurrence(
    streams: Mapping[str, Sequence[int]],
    representation: LinearRepresentation,
    order: int,
    *,
    train_names: Sequence[str],
    heldout_names: Sequence[str],
) -> RecurrenceFit:
    rendered = {
        name: render_representation(values, representation)
        for name, values in streams.items()
    }
    system = recurrence_system(
        tuple(rendered[name] for name in train_names),
        order,
        representation.modulus,
    )
    matches = equations = 0
    if system.solution is not None:
        matches, equations = recurrence_matches(
            tuple(rendered[name] for name in heldout_names),
            system.solution,
            representation.modulus,
        )
    return RecurrenceFit(
        representation,
        order,
        system,
        matches,
        equations,
    )


def scan_shared_recurrences(
    streams: Mapping[str, Sequence[int]],
    *,
    train_names: Sequence[str],
    heldout_names: Sequence[str],
    maximum_order: int = 32,
) -> tuple[RecurrenceFit, ...]:
    return tuple(
        fit_shared_recurrence(
            streams,
            representation,
            order,
            train_names=train_names,
            heldout_names=heldout_names,
        )
        for representation in representations()
        for order in range(1, maximum_order + 1)
    )


def generate_recurrence(
    coefficients: Sequence[int],
    seed: Sequence[int],
    length: int,
    modulus: int,
) -> tuple[int, ...]:
    if len(seed) != len(coefficients):
        raise ValueError("seed length must equal recurrence order")
    if length < len(seed):
        raise ValueError("length is shorter than the seed")
    output = [value % modulus for value in seed]
    while len(output) < length:
        output.append(
            sum(
                coefficient * output[-lag]
                for lag, coefficient in enumerate(coefficients, start=1)
            )
            % modulus
        )
    return tuple(output)
