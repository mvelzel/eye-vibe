"""Direct Eye-alphabet reading of Veska's separated upper/lower marks."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations
from string import ascii_lowercase

from .calling_codes import CALLING_CODE_REGIONS


Point = tuple[int, int]
Component = frozenset[Point]
EYE_MODULUS = 83
ASCII_OFFSET = 32


def is_orthogonal_plus(component: Component) -> bool:
    if len(component) != 5:
        return False
    for x, y in component:
        expected = {
            (x, y),
            (x - 1, y),
            (x + 1, y),
            (x, y - 1),
            (x, y + 1),
        }
        if component == expected:
            return True
    return False


def upper_component_sizes(components: tuple[Component, ...]) -> tuple[int, ...]:
    ordered = sorted(components, key=lambda component: min(x for x, _ in component))
    return tuple(len(component) for component in ordered)


def lower_plus_increment(components: tuple[Component, ...]) -> int | None:
    pluses = tuple(
        component for component in components if is_orthogonal_plus(component)
    )
    singletons = tuple(component for component in components if len(component) == 1)
    if len(pluses) != 1 or len(singletons) != len(components) - 1:
        return None
    plus = pluses[0]
    if any(
        min(x for x, _ in singleton) <= max(x for x, _ in plus)
        for singleton in singletons
    ):
        return None
    return len(singletons)


def decimal_component_number(sizes: tuple[int, ...]) -> int:
    if not sizes or any(size not in range(10) for size in sizes):
        raise ValueError("component sizes must be one decimal digit each")
    return int("".join(map(str, sizes)))


def eye_increment_text(number: int, increment: int) -> str:
    return "".join(
        chr(value % EYE_MODULUS + ASCII_OFFSET)
        for value in (number, number + increment)
    )


@dataclass(frozen=True)
class GateLocaleReading:
    component_sizes: tuple[int, ...]
    number: int
    increment: int
    text: str


def gate_locale_reading(
    upper_components: tuple[Component, ...],
    lower_components: tuple[Component, ...],
) -> GateLocaleReading | None:
    increment = lower_plus_increment(lower_components)
    if increment is None:
        return None
    sizes = upper_component_sizes(upper_components)
    number = decimal_component_number(sizes)
    return GateLocaleReading(
        sizes, number, increment, eye_increment_text(number, increment)
    )


def permutation_texts(
    sizes: tuple[int, ...], increment: int
) -> tuple[tuple[tuple[int, ...], str], ...]:
    return tuple(
        (ordering, eye_increment_text(decimal_component_number(ordering), increment))
        for ordering in permutations(sizes)
    )


def geographic_region_codes() -> frozenset[str]:
    return frozenset(
        region
        for regions in CALLING_CODE_REGIONS.values()
        for region in regions
        if len(region) == 2
    )


def increment_residue_census(increment: int) -> tuple[int, tuple[tuple[int, str], ...]]:
    regions = geographic_region_codes()
    pairs = tuple(
        (residue, eye_increment_text(residue, increment))
        for residue in range(EYE_MODULUS)
    )
    lowercase = sum(
        all(character in ascii_lowercase for character in text)
        for _, text in pairs
    )
    region_pairs = tuple(
        (residue, text) for residue, text in pairs if text.upper() in regions
    )
    return lowercase, region_pairs
