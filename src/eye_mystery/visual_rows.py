"""Reconstruct and superimpose the two-dimensional Eye Message rows.

The accepted reading stream alternates downward and upward triangles.  For a
complete pair of visual rows, six consecutive stream digits ``a..f`` came
from top positions ``a,b,f`` and bottom positions ``c,e,d``.  A final
downward triangle contributes two top positions and one bottom position.
"""

from collections.abc import Iterable, Sequence


def visual_rows(
    message: Sequence[int], row_pair_trigram_lengths: Sequence[int]
) -> tuple[tuple[int, ...], ...]:
    """Undo the accepted interleave and return alternating top/bottom rows."""
    rows: list[tuple[int, ...]] = []
    cursor = 0
    for trigram_length in row_pair_trigram_lengths:
        digit_length = 3 * trigram_length
        chunk = message[cursor : cursor + digit_length]
        if len(chunk) != digit_length:
            raise ValueError("row-pair lengths exceed the message")
        cursor += digit_length

        top: list[int] = []
        bottom: list[int] = []
        complete_pairs, trailing_triangle = divmod(trigram_length, 2)
        for index in range(complete_pairs):
            a, b, c, d, e, f = chunk[6 * index : 6 * index + 6]
            top.extend((a, b, f))
            bottom.extend((c, e, d))
        if trailing_triangle:
            a, b, c = chunk[-3:]
            top.extend((a, b))
            bottom.append(c)
        rows.extend((tuple(top), tuple(bottom)))

    if cursor != len(message):
        raise ValueError("row-pair lengths do not consume the message")
    return tuple(rows)


def interleave_visual_rows(rows: Sequence[Sequence[int]]) -> tuple[int, ...]:
    """Convert alternating top/bottom rows back to the accepted stream."""
    if len(rows) % 2:
        raise ValueError("visual rows must occur in top/bottom pairs")

    message: list[int] = []
    for pair_index in range(0, len(rows), 2):
        top = rows[pair_index]
        bottom = rows[pair_index + 1]
        if len(top) not in (len(bottom), len(bottom) + 1):
            raise ValueError("invalid top/bottom row lengths")

        full_blocks, top_remainder = divmod(len(top), 3)
        bottom_blocks, bottom_remainder = divmod(len(bottom), 3)
        if full_blocks != bottom_blocks:
            raise ValueError("visual rows have different complete-block counts")
        for block in range(full_blocks):
            top_chunk = top[3 * block : 3 * block + 3]
            bottom_chunk = bottom[3 * block : 3 * block + 3]
            message.extend(
                (
                    top_chunk[0],
                    top_chunk[1],
                    bottom_chunk[0],
                    bottom_chunk[2],
                    bottom_chunk[1],
                    top_chunk[2],
                )
            )
        if (top_remainder, bottom_remainder) == (2, 1):
            message.extend((top[-2], top[-1], bottom[-1]))
        elif (top_remainder, bottom_remainder) != (0, 0):
            raise ValueError("invalid trailing visual triangle")
    return tuple(message)


def direction_mask_rows(
    messages: Iterable[Sequence[Sequence[int]]],
) -> tuple[tuple[int, ...], ...]:
    """Superimpose aligned visual messages as bitmasks of eye directions."""
    materialized = tuple(messages)
    if not materialized:
        return ()
    height = max(len(rows) for rows in materialized)
    result: list[tuple[int, ...]] = []
    for row_index in range(height):
        width = max(
            (len(rows[row_index]) for rows in materialized if row_index < len(rows)),
            default=0,
        )
        row: list[int] = []
        for column in range(width):
            mask = 0
            for rows in materialized:
                if row_index < len(rows) and column < len(rows[row_index]):
                    mask |= 1 << rows[row_index][column]
            row.append(mask)
        result.append(tuple(row))
    return tuple(result)
