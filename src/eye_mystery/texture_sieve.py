"""Natural binary-table readings of a nearly 83-by-26 texture.

The fixed ``earth.png`` material tile is 48 by 45, hence 2,160 pixels: two
more than ``83 * 26``.  These helpers enumerate only the dihedral image
orientations and the three ways to remove two boundary pixels before reshaping
the remaining bits as a 26-position by 83-symbol lookup table.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass


BitRows = tuple[tuple[int, ...], ...]


@dataclass(frozen=True)
class TextureMask:
    name: str
    rows: BitRows


def _validate_rows(rows: Sequence[Sequence[int]]) -> BitRows:
    result = tuple(tuple(row) for row in rows)
    if not result or not result[0]:
        raise ValueError("texture must be non-empty")
    if any(len(row) != len(result[0]) for row in result):
        raise ValueError("texture rows must have equal width")
    if any(bit not in (0, 1) for row in result for bit in row):
        raise ValueError("texture must contain only zero and one")
    return result


def dihedral_orientations(rows: Sequence[Sequence[int]]) -> tuple[TextureMask, ...]:
    """Return the distinct rotations/reflections of a rectangular bit image."""

    base = _validate_rows(rows)

    def horizontal(value: BitRows) -> BitRows:
        return tuple(tuple(reversed(row)) for row in value)

    def vertical(value: BitRows) -> BitRows:
        return tuple(reversed(value))

    def transpose(value: BitRows) -> BitRows:
        return tuple(tuple(row[index] for row in value) for index in range(len(value[0])))

    transposed = transpose(base)
    candidates = (
        ("identity", base),
        ("flip-x", horizontal(base)),
        ("flip-y", vertical(base)),
        ("rotate-180", horizontal(vertical(base))),
        ("transpose", transposed),
        ("transpose-flip-x", horizontal(transposed)),
        ("transpose-flip-y", vertical(transposed)),
        ("transpose-rotate-180", horizontal(vertical(transposed))),
    )
    seen: set[BitRows] = set()
    result = []
    for name, candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        result.append(TextureMask(name, candidate))
    return tuple(result)


def boundary_trimmed_masks(
    rows: Sequence[Sequence[int]],
    *,
    output_rows: int = 26,
    output_columns: int = 83,
) -> tuple[TextureMask, ...]:
    """Orient, remove boundary padding, and reshape a binary texture.

    Exactly ``input_size - output_rows*output_columns`` pixels must be removed.
    Only prefix/suffix removals are considered, so a two-pixel excess yields
    the three splits ``0+2``, ``1+1``, and ``2+0``.
    """

    if output_rows < 1 or output_columns < 1:
        raise ValueError("output dimensions must be positive")
    orientations = dihedral_orientations(rows)
    input_size = sum(len(row) for row in orientations[0].rows)
    output_size = output_rows * output_columns
    excess = input_size - output_size
    if excess < 0:
        raise ValueError("texture is smaller than the requested table")

    seen: set[BitRows] = set()
    result = []
    for orientation in orientations:
        flat = tuple(bit for row in orientation.rows for bit in row)
        for prefix in range(excess + 1):
            suffix = excess - prefix
            end = len(flat) - suffix if suffix else len(flat)
            trimmed = flat[prefix:end]
            reshaped = tuple(
                trimmed[start : start + output_columns]
                for start in range(0, len(trimmed), output_columns)
            )
            if len(reshaped) != output_rows or any(
                len(row) != output_columns for row in reshaped
            ):
                raise AssertionError("internal reshape error")
            if reshaped in seen:
                continue
            seen.add(reshaped)
            result.append(
                TextureMask(
                    f"{orientation.name}/drop={prefix}+{suffix}", reshaped
                )
            )
    return tuple(result)


def lookup_bits(
    mask: Sequence[Sequence[int]],
    positions: Sequence[int],
    values: Sequence[int],
) -> tuple[int, ...]:
    """Read one table bit for every aligned position and symbol value."""

    table = _validate_rows(mask)
    if len(positions) != len(values):
        raise ValueError("positions and values must have equal length")
    if any(not 0 <= position < len(table) for position in positions):
        raise ValueError("position is outside the table")
    if any(not 0 <= value < len(table[0]) for value in values):
        raise ValueError("value is outside the table")
    return tuple(table[position][value] for position, value in zip(positions, values))
