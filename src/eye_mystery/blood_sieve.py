"""Test the Meditation Chamber blood pool as an 83 by 26 sieve.

The raw scene bitmap uses colour ``(131, 0, 0)`` for the pool.  Its bounding
box is exactly 83 pixels wide by 26 pixels high, matching the canonical Eye
Message alphabet and the maximum number of trigrams in a visual row-pair.
The runs below are the blood-coloured pixels in each row, expressed as
half-open coordinates relative to that bounding box.  Row 5 contains one
non-blood pixel at x=13, so retaining runs rather than merely the outer span
matters for an exact test.
"""

from collections.abc import Sequence

from .corpus import trigram_values


BLOOD_ROW_RUNS: tuple[tuple[tuple[int, int], ...], ...] = (
    ((0, 83),),
    ((0, 78),),
    ((0, 76),),
    ((0, 73),),
    ((0, 71),),
    ((1, 13), (14, 68)),
    ((1, 63),),
    ((1, 61),),
    ((1, 58),),
    ((1, 56),),
    ((2, 53),),
    ((2, 51),),
    ((2, 48),),
    ((3, 43),),
    ((3, 41),),
    ((4, 38),),
    ((4, 36),),
    ((4, 33),),
    ((4, 28),),
    ((4, 26),),
    ((5, 23),),
    ((5, 21),),
    ((5, 18),),
    ((5, 16),),
    ((5, 13),),
    ((6, 8),),
)


def split_row_pair_values(
    message: Sequence[int], row_pair_trigram_lengths: Sequence[int]
) -> tuple[tuple[int, ...], ...]:
    """Return canonical values split at the displayed row-pair boundaries."""
    values = trigram_values(tuple(message))
    rows: list[tuple[int, ...]] = []
    cursor = 0
    for length in row_pair_trigram_lengths:
        row = values[cursor : cursor + length]
        if len(row) != length:
            raise ValueError("row-pair lengths exceed the message")
        rows.append(row)
        cursor += length
    if cursor != len(values):
        raise ValueError("row-pair lengths do not consume the message")
    return tuple(rows)


def sieve_row_pair(
    values: Sequence[int], *, mirror_values: bool = False, reverse_positions: bool = False
) -> tuple[int, ...]:
    """Classify ``(trigram value, position)`` points by the blood-pool mask."""
    if len(values) > len(BLOOD_ROW_RUNS):
        raise ValueError("a row-pair cannot contain more than 26 values")

    bits: list[int] = []
    for position, raw_value in enumerate(values):
        if not 0 <= raw_value < 83:
            raise ValueError("trigram values must be in 0..82")
        value = 82 - raw_value if mirror_values else raw_value
        row_index = 25 - position if reverse_positions else position
        bits.append(
            int(any(start <= value < end for start, end in BLOOD_ROW_RUNS[row_index]))
        )
    return tuple(bits)


def sieve_message(
    message: Sequence[int],
    row_pair_trigram_lengths: Sequence[int],
    *,
    mirror_values: bool = False,
    reverse_positions: bool = False,
) -> tuple[int, ...]:
    """Apply the mask to every row-pair and concatenate the resulting bits."""
    rows = split_row_pair_values(message, row_pair_trigram_lengths)
    return tuple(
        bit
        for row in rows
        for bit in sieve_row_pair(
            row,
            mirror_values=mirror_values,
            reverse_positions=reverse_positions,
        )
    )


def pack_chunks(
    bits: Sequence[int],
    *,
    width: int,
    offset: int = 0,
    least_significant_first: bool = False,
) -> tuple[int, ...]:
    """Pack complete fixed-width chunks; incomplete trailing bits are ignored."""
    if width < 1:
        raise ValueError("width must be positive")
    if not 0 <= offset < width:
        raise ValueError("offset must be smaller than width")
    result: list[int] = []
    usable = bits[offset : offset + (len(bits) - offset) // width * width]
    for index in range(0, len(usable), width):
        chunk = usable[index : index + width]
        value = 0
        for bit_index, bit in enumerate(chunk):
            if bit not in (0, 1):
                raise ValueError("bits must be zero or one")
            shift = bit_index if least_significant_first else width - 1 - bit_index
            value |= bit << shift
        result.append(value)
    return tuple(result)


def pack_bits(
    bits: Sequence[int], *, offset: int = 0, least_significant_first: bool = False
) -> bytes:
    """Pack complete octets after ``offset``; incomplete trailing bits are ignored."""
    return bytes(
        pack_chunks(
            bits,
            width=8,
            offset=offset,
            least_significant_first=least_significant_first,
        )
    )
