"""Standard physical-deck permutations for structured S_n searches."""

from __future__ import annotations

from collections import deque
from collections.abc import Iterator
from math import gcd


def interleave(size: int, split: int, *, right_first: bool = False) -> tuple[int, ...]:
    if not 0 < split < size:
        raise ValueError("split must divide the deck into two nonempty packets")
    packets = (deque(range(split)), deque(range(split, size)))
    turn = 1 if right_first else 0
    result = []
    while packets[0] or packets[1]:
        if packets[turn]:
            result.append(packets[turn].popleft())
        else:
            result.append(packets[1 - turn].popleft())
        turn = 1 - turn
    return tuple(result)


def mongean(
    size: int, *, first_to_top: bool = False, reverse_source: bool = False
) -> tuple[int, ...]:
    source = range(size - 1, -1, -1) if reverse_source else range(size)
    pile: deque[int] = deque()
    put_on_top = first_to_top
    for card in source:
        if put_on_top:
            pile.appendleft(card)
        else:
            pile.append(card)
        put_on_top = not put_on_top
    return tuple(pile)


def josephus(size: int, step: int, *, offset: int = 0) -> tuple[int, ...]:
    if step <= 0:
        raise ValueError("step must be positive")
    remaining = list(range(size))
    result = []
    index = offset % size
    while remaining:
        index = (index + step - 1) % len(remaining)
        result.append(remaining.pop(index))
    return tuple(result)


def affine_with_fixed_card(
    size: int, fixed: int, multiplier: int, offset: int
) -> tuple[int, ...]:
    if not 0 <= fixed < size:
        raise ValueError("fixed card must be a deck position")
    active = tuple(position for position in range(size) if position != fixed)
    modulus = len(active)
    if gcd(multiplier, modulus) != 1:
        raise ValueError("multiplier must be invertible modulo size-1")
    result = list(range(size))
    for index, new_position in enumerate(active):
        result[new_position] = active[(multiplier * index + offset) % modulus]
    return tuple(result)


def affine_with_removed_dummy(
    size: int, multiplier: int, offset: int, *, dummy: int | None = None
) -> tuple[int, ...]:
    modulus = size + 1
    if dummy is None:
        dummy = size
    if not 0 <= dummy < modulus:
        raise ValueError("dummy must be a position in the size+1 deck")
    if gcd(multiplier, modulus) != 1:
        raise ValueError("multiplier must be invertible modulo size+1")
    order = tuple((multiplier * position + offset) % modulus for position in range(modulus))
    return tuple(card if card < dummy else card - 1 for card in order if card != dummy)


def is_affine_mod_size(permutation: tuple[int, ...]) -> bool:
    size = len(permutation)
    offset = permutation[0]
    multiplier = (permutation[1] - offset) % size
    return multiplier != 0 and all(
        value == (multiplier * index + offset) % size
        for index, value in enumerate(permutation)
    )


def standard_base_candidates(size: int = 83) -> Iterator[tuple[str, tuple[int, ...]]]:
    """Yield named non-duplicate standard shuffles, including near-size affines."""
    seen: set[tuple[int, ...]] = set()

    def emit(name: str, permutation: tuple[int, ...]):
        if permutation not in seen:
            seen.add(permutation)
            return name, permutation
        return None

    for split in sorted({size // 2, (size + 1) // 2}):
        for right_first in (False, True):
            candidate = emit(
                f"interleave-s{split}-{'R' if right_first else 'L'}",
                interleave(size, split, right_first=right_first),
            )
            if candidate:
                yield candidate
    for first_to_top in (False, True):
        for reverse_source in (False, True):
            candidate = emit(
                f"mongean-{'T' if first_to_top else 'B'}-"
                f"{'rev' if reverse_source else 'fwd'}",
                mongean(
                    size,
                    first_to_top=first_to_top,
                    reverse_source=reverse_source,
                ),
            )
            if candidate:
                yield candidate
    for step in range(2, size):
        candidate = emit(f"josephus-{step}", josephus(size, step))
        if candidate:
            yield candidate
    for fixed in (0, size - 1):
        modulus = size - 1
        for multiplier in range(1, modulus):
            if gcd(multiplier, modulus) != 1:
                continue
            for offset in range(modulus):
                candidate = emit(
                    f"affine-{modulus}-fixed{fixed}-{multiplier}-{offset}",
                    affine_with_fixed_card(
                        size, fixed, multiplier, offset
                    ),
                )
                if candidate:
                    yield candidate
    modulus = size + 1
    for multiplier in range(1, modulus):
        if gcd(multiplier, modulus) != 1:
            continue
        for offset in range(modulus):
            candidate = emit(
                f"affine-{modulus}-dummy-{multiplier}-{offset}",
                affine_with_removed_dummy(size, multiplier, offset),
            )
            if candidate:
                yield candidate
