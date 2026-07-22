"""Key-free quadratic-character projections of the Eye transitions.

Because 83 is prime and ``83 % 4 == 3``, every nonzero difference is either a
quadratic residue or non-residue and negating it changes that class.  The Eye
corpus has no adjacent equal symbols, so every transition therefore supplies
one canonical orientation bit without selecting a primitive root.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass


EYE_MODULUS = 83


def legendre_bit(value: int, *, modulus: int = EYE_MODULUS) -> int:
    """Return 0 for a nonzero square and 1 for a non-square modulo ``modulus``."""

    value %= modulus
    if value == 0:
        raise ValueError("the quadratic character of zero is not a bit")
    character = pow(value, (modulus - 1) // 2, modulus)
    if character == 1:
        return 0
    if character == modulus - 1:
        return 1
    raise ValueError("modulus must be an odd prime for this projection")


def transition_bits(stream: Sequence[int], *, drop_header: bool = False) -> tuple[int, ...]:
    """Project adjacent differences to Legendre bits.

    ``drop_header`` removes the transition from the distinct first/header value
    into the common body and begins with differences wholly inside the body.
    """

    values = stream[1:] if drop_header else stream
    return tuple(
        legendre_bit(right - left)
        for left, right in zip(values, values[1:])
    )


@dataclass(frozen=True)
class RepeatContext:
    """One frozen family of repeated/isomorphic ciphertext windows."""

    name: str
    length: int
    occurrences: tuple[tuple[str, int], ...]


@dataclass(frozen=True)
class ComplementFit:
    """Best equal-or-complement fit of transition bits in repeat contexts."""

    matches: int
    comparisons: int
    exact_occurrences: int
    compared_occurrences: int


def complement_fit(
    streams: Mapping[str, Sequence[int]], contexts: Sequence[RepeatContext]
) -> ComplementFit:
    """Compare every context with its reference, allowing one XOR bit per copy.

    An affine relabelling of field values multiplies all differences by one
    constant.  Its Legendre projection is consequently either identical or
    complemented throughout the window.  This is only a necessary diagnostic;
    it does not assume that the complete context map is affine.
    """

    matches = comparisons = exact_occurrences = compared_occurrences = 0
    for context in contexts:
        reference_name, reference_start = context.occurrences[0]
        reference = transition_bits(
            streams[reference_name][
                reference_start : reference_start + context.length
            ]
        )
        for name, start in context.occurrences[1:]:
            candidate = transition_bits(streams[name][start : start + context.length])
            if len(candidate) != len(reference):
                raise ValueError("repeat context extends outside a stream")
            same = sum(left == right for left, right in zip(reference, candidate, strict=True))
            best = max(same, len(reference) - same)
            matches += best
            comparisons += len(reference)
            exact_occurrences += best == len(reference)
            compared_occurrences += 1
    return ComplementFit(matches, comparisons, exact_occurrences, compared_occurrences)


def concatenate_bits(
    streams: Mapping[str, Sequence[int]],
    order: Sequence[str],
    *,
    drop_header: bool,
) -> tuple[int, ...]:
    """Concatenate within-message transition bits without inventing cut edges."""

    return tuple(
        bit
        for name in order
        for bit in transition_bits(streams[name], drop_header=drop_header)
    )


def grouped_values(
    bits: Sequence[int],
    width: int,
    *,
    offset: int = 0,
    least_significant_first: bool = False,
) -> tuple[int, ...]:
    """Pack complete fixed-width groups after an explicit bit offset."""

    if width < 1:
        raise ValueError("width must be positive")
    if offset not in range(width):
        raise ValueError("offset must lie within one group")
    values = []
    for start in range(offset, len(bits) - width + 1, width):
        group = bits[start : start + width]
        if least_significant_first:
            group = tuple(reversed(group))
        value = 0
        for bit in group:
            if bit not in (0, 1):
                raise ValueError("bit streams may contain only zero and one")
            value = 2 * value + bit
        values.append(value)
    return tuple(values)


def plausible_ascii_count(values: Sequence[int]) -> int:
    """Count conservative text bytes: letters, digits, whitespace, punctuation."""

    return sum(
        value in (9, 10, 13)
        or 32 <= value <= 126
        for value in values
    )


@dataclass(frozen=True)
class BinaryTextFit:
    """Best fixed-width ASCII rendering within a frozen small scan."""

    plausible: int
    characters: int
    order_name: str
    drop_header: bool
    width: int
    offset: int
    reversed_stream: bool
    inverted: bool
    least_significant_first: bool
    values: tuple[int, ...]

    @property
    def rate(self) -> float:
        return self.plausible / self.characters if self.characters else 0.0


def best_binary_text_fit(
    streams: Mapping[str, Sequence[int]],
    orders: Mapping[str, Sequence[str]],
) -> BinaryTextFit:
    """Scan only 7/8-bit ASCII conventions over independently selected orders."""

    best: BinaryTextFit | None = None
    for order_name, order in orders.items():
        for drop_header in (False, True):
            raw = concatenate_bits(streams, order, drop_header=drop_header)
            for reversed_stream in (False, True):
                oriented = tuple(reversed(raw)) if reversed_stream else raw
                for inverted in (False, True):
                    bits = tuple(1 - bit for bit in oriented) if inverted else oriented
                    for width in (7, 8):
                        for offset in range(width):
                            for least_significant_first in (False, True):
                                values = grouped_values(
                                    bits,
                                    width,
                                    offset=offset,
                                    least_significant_first=least_significant_first,
                                )
                                candidate = BinaryTextFit(
                                    plausible_ascii_count(values),
                                    len(values),
                                    order_name,
                                    drop_header,
                                    width,
                                    offset,
                                    reversed_stream,
                                    inverted,
                                    least_significant_first,
                                    values,
                                )
                                if best is None or (
                                    candidate.rate,
                                    candidate.plausible,
                                    -candidate.width,
                                ) > (best.rate, best.plausible, -best.width):
                                    best = candidate
    assert best is not None
    return best
