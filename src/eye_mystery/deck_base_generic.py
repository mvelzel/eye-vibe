"""Fast decoding for a fixed deck permutation followed by a top swap."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass


def validate_permutation(permutation: Sequence[int]) -> None:
    if tuple(sorted(permutation)) != tuple(range(len(permutation))):
        raise ValueError("base must be a permutation of 0..n-1")


def compose(left: Sequence[int], right: Sequence[int]) -> tuple[int, ...]:
    """Compose new-position-to-old-position permutations as ``left ∘ right``."""
    if len(left) != len(right):
        raise ValueError("permutations must have equal lengths")
    validate_permutation(left)
    validate_permutation(right)
    return tuple(left[right[index]] for index in range(len(left)))


def permutation_power(
    permutation: Sequence[int], exponent: int
) -> tuple[int, ...]:
    if exponent < 0:
        raise ValueError("exponent must be nonnegative")
    validate_permutation(permutation)
    result = tuple(range(len(permutation)))
    base = tuple(permutation)
    while exponent:
        if exponent & 1:
            result = compose(result, base)
        base = compose(base, base)
        exponent //= 2
    return result


@dataclass(frozen=True)
class BaseOrbitTables:
    inverse_powers: tuple[tuple[int, ...], ...]
    top_coordinates: tuple[int, ...]
    coordinates_at_positions: tuple[tuple[int, ...], ...]


@dataclass(frozen=True)
class PermutationCycleOracle:
    """Evaluate arbitrary powers of one permutation in constant time."""

    cycles: tuple[tuple[int, ...], ...]
    cycle_of: tuple[int, ...]
    offset_of: tuple[int, ...]

    def power(self, value: int, exponent: int) -> int:
        cycle = self.cycles[self.cycle_of[value]]
        return cycle[(self.offset_of[value] + exponent) % len(cycle)]


def build_cycle_oracle(permutation: Sequence[int]) -> PermutationCycleOracle:
    validate_permutation(permutation)
    size = len(permutation)
    cycles: list[tuple[int, ...]] = []
    cycle_of = [-1] * size
    offset_of = [-1] * size
    for start in range(size):
        if cycle_of[start] >= 0:
            continue
        cycle = []
        value = start
        while cycle_of[value] < 0:
            cycle_of[value] = len(cycles)
            offset_of[value] = len(cycle)
            cycle.append(value)
            value = permutation[value]
        cycles.append(tuple(cycle))
    return PermutationCycleOracle(
        tuple(cycles), tuple(cycle_of), tuple(offset_of)
    )


def decode_base_top_swap_with_cycles(
    ciphertext: Sequence[int],
    base: Sequence[int],
    initial_coordinates: Sequence[int] | None = None,
) -> tuple[int, ...]:
    """Decode a common-base/top-swap stream without storing every base power."""

    validate_permutation(base)
    size = len(base)
    if any(not 0 <= card < size for card in ciphertext):
        raise ValueError("ciphertext card is outside the deck")
    oracle = build_cycle_oracle(base)
    if initial_coordinates is None:
        coordinate_of = list(range(size))
    else:
        validate_permutation(initial_coordinates)
        if len(initial_coordinates) != size:
            raise ValueError("initial coordinate map has the wrong size")
        coordinate_of = list(initial_coordinates)
    card_at_coordinate = [0] * size
    for card, coordinate in enumerate(coordinate_of):
        card_at_coordinate[coordinate] = card

    instructions = []
    for step, card in enumerate(ciphertext, start=1):
        card_coordinate = coordinate_of[card]
        position = oracle.power(card_coordinate, -step)
        instructions.append(position)

        top_coordinate = oracle.power(0, step)
        if top_coordinate != card_coordinate:
            top_card = card_at_coordinate[top_coordinate]
            coordinate_of[top_card] = card_coordinate
            coordinate_of[card] = top_coordinate
            card_at_coordinate[top_coordinate] = card
            card_at_coordinate[card_coordinate] = top_card
    return tuple(instructions)


def build_base_orbit_tables(
    base: Sequence[int], steps: int
) -> BaseOrbitTables:
    """Precompute coordinate-to-position maps for successive base powers."""
    if steps < 0:
        raise ValueError("steps must be nonnegative")
    validate_permutation(base)
    size = len(base)
    base_inverse = [0] * size
    for new_position, old_position in enumerate(base):
        base_inverse[old_position] = new_position
    inverse = tuple(range(size))
    inverse_powers = [inverse]
    top_coordinates = [0]
    coordinates_at_positions = [tuple(range(size))]
    for _ in range(steps):
        inverse = tuple(
            base_inverse[inverse[coordinate]] for coordinate in range(size)
        )
        inverse_powers.append(inverse)
        coordinates = [0] * size
        for coordinate, position in enumerate(inverse):
            coordinates[position] = coordinate
        coordinates_at_positions.append(tuple(coordinates))
        top_coordinates.append(coordinates[0])
    return BaseOrbitTables(
        tuple(inverse_powers),
        tuple(top_coordinates),
        tuple(coordinates_at_positions),
    )


def decode_base_top_swap_hidden_with_tables(
    ciphertext: Sequence[int],
    tables: BaseOrbitTables,
    hidden_swap: Callable[[int, int], tuple[int, int]],
) -> tuple[int, ...]:
    """Decode a top swap followed by a plaintext-selected non-top swap."""

    return decode_base_top_swap_hidden_sequence_with_tables(
        ciphertext, tables, (hidden_swap,)
    )


def decode_base_top_swap_hidden_sequence_with_tables(
    ciphertext: Sequence[int],
    tables: BaseOrbitTables,
    hidden_swaps: Sequence[Callable[[int, int], tuple[int, int]]],
) -> tuple[int, ...]:
    """Decode a top swap followed by several deterministic hidden swaps."""

    size = len(tables.inverse_powers[0])
    coordinate_of = list(range(size))
    card_at_coordinate = list(range(size))
    instructions = []

    def swap_coordinates(left: int, right: int) -> None:
        if left == right:
            return
        left_card = card_at_coordinate[left]
        right_card = card_at_coordinate[right]
        card_at_coordinate[left], card_at_coordinate[right] = right_card, left_card
        coordinate_of[left_card], coordinate_of[right_card] = right, left

    for step, card in enumerate(ciphertext, start=1):
        card_coordinate = coordinate_of[card]
        position = tables.inverse_powers[step][card_coordinate]
        instructions.append(position)
        swap_coordinates(tables.top_coordinates[step], card_coordinate)

        coordinates = tables.coordinates_at_positions[step]
        for hidden_swap in hidden_swaps:
            left_position, right_position = hidden_swap(position, size)
            if not 0 < left_position < size or not 0 < right_position < size:
                raise ValueError(
                    "hidden swap must use non-top deck positions"
                )
            swap_coordinates(
                coordinates[left_position], coordinates[right_position]
            )
    return tuple(instructions)


def decode_base_top_swap_with_tables(
    ciphertext: Sequence[int],
    tables: BaseOrbitTables,
    initial_coordinates: Sequence[int] | None = None,
) -> tuple[int, ...]:
    """Decode using tables shared across messages with the same reset state."""
    size = len(tables.inverse_powers[0])
    if len(ciphertext) >= len(tables.inverse_powers):
        raise ValueError("orbit tables do not cover the ciphertext length")
    if any(not 0 <= card < size for card in ciphertext):
        raise ValueError("ciphertext card is outside the deck")

    if initial_coordinates is None:
        coordinate_of = list(range(size))
    else:
        validate_permutation(initial_coordinates)
        if len(initial_coordinates) != size:
            raise ValueError("initial coordinate map has the wrong size")
        coordinate_of = list(initial_coordinates)
    card_at_coordinate = [0] * size
    for card, coordinate in enumerate(coordinate_of):
        card_at_coordinate[coordinate] = card
    instructions = []
    for step, card in enumerate(ciphertext, start=1):
        inverse_power = tables.inverse_powers[step]
        card_coordinate = coordinate_of[card]
        position = inverse_power[card_coordinate]
        instructions.append(position)

        top_coordinate = tables.top_coordinates[step]
        if top_coordinate != card_coordinate:
            top_card = card_at_coordinate[top_coordinate]
            coordinate_of[top_card] = card_coordinate
            coordinate_of[card] = top_coordinate
            card_at_coordinate[top_coordinate] = card
            card_at_coordinate[card_coordinate] = top_card
    return tuple(instructions)


def decode_base_top_swap(
    ciphertext: Sequence[int], base: Sequence[int]
) -> tuple[int, ...]:
    """Decode ``apply base; swap(top, instruction); emit top``.

    ``base[j]`` is the old position whose card moves to new position ``j``.
    Sparse top swaps are stored in a coordinate frame that advances by one
    power of ``base`` per symbol, avoiding a full 83-card shuffle each step.
    The initial deck has card ``j`` at position ``j``.
    """
    tables = build_base_orbit_tables(base, len(ciphertext))
    return decode_base_top_swap_with_tables(ciphertext, tables)


def encrypt_base_top_swap(
    plaintext: Sequence[int], base: Sequence[int]
) -> tuple[int, ...]:
    """Materialize the corresponding common-base-plus-top-swap encryption."""

    validate_permutation(base)
    size = len(base)
    if any(not 0 <= position < size for position in plaintext):
        raise ValueError("plaintext instruction is outside the deck")
    deck = list(range(size))
    ciphertext = []
    for position in plaintext:
        deck = [deck[base[index]] for index in range(size)]
        deck[0], deck[position] = deck[position], deck[0]
        ciphertext.append(deck[0])
    return tuple(ciphertext)
