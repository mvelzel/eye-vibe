"""Geometry checks for Noita's giant-dollar reward sprite.

The recent Gate/Eye discussion points to a near mirror relation in the two
curves of ``giant_dollar.png``.  This module keeps the measurement deliberately
small: it derives the always-opaque centre stem, records the contiguous opaque
run on either side, and exhaustively scans fixed-length row windows.  It does
not assign Eye-cipher semantics to the resulting widths.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Sequence

from PIL import Image


Mask = tuple[tuple[bool, ...], ...]


def file_sha256(path: Path) -> str:
    """Return a lowercase SHA-256 digest for one asset."""

    return sha256(path.read_bytes()).hexdigest()


def load_alpha_mask(path: Path) -> Mask:
    """Read an image as a rectangular opaque/transparent mask."""

    image = Image.open(path).convert("RGBA")
    return tuple(
        tuple(image.getpixel((x, y))[3] > 0 for x in range(image.width))
        for y in range(image.height)
    )


def dimensions(mask: Mask) -> tuple[int, int]:
    """Return ``(width, height)`` after validating rectangularity."""

    if not mask or not mask[0]:
        raise ValueError("mask must be non-empty")
    width = len(mask[0])
    if any(len(row) != width for row in mask):
        raise ValueError("mask must be rectangular")
    return width, len(mask)


def always_opaque_columns(mask: Mask) -> tuple[int, ...]:
    """Columns whose alpha is nonzero on every authored row."""

    width, _ = dimensions(mask)
    return tuple(x for x in range(width) if all(row[x] for row in mask))


def contiguous_width(mask: Mask, row: int, anchor: int, step: int) -> int:
    """Count opaque pixels from ``anchor`` in horizontal direction ``step``."""

    width, height = dimensions(mask)
    if not 0 <= row < height or not 0 <= anchor < width:
        raise IndexError("row or anchor lies outside mask")
    if step not in (-1, 1):
        raise ValueError("step must be -1 or +1")
    result = 0
    x = anchor
    while 0 <= x < width and mask[row][x]:
        result += 1
        x += step
    return result


def centre_run_widths(mask: Mask) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Measure runs outwards from the two edges of the invariant centre stem."""

    columns = always_opaque_columns(mask)
    if not columns or columns != tuple(range(columns[0], columns[-1] + 1)):
        raise ValueError("always-opaque columns do not form one centre stem")
    left_anchor, right_anchor = columns[0], columns[-1]
    _, height = dimensions(mask)
    left = tuple(contiguous_width(mask, y, left_anchor, -1) for y in range(height))
    right = tuple(contiguous_width(mask, y, right_anchor, 1) for y in range(height))
    return left, right


@dataclass(frozen=True)
class WindowComparison:
    """One alignment of a left and right width window."""

    left_start: int
    right_start: int
    right_reversed: bool
    length: int
    equal_rows: int
    absolute_difference: int
    mismatches: tuple[tuple[int, int, int], ...]


def compare_windows(
    left: Sequence[int],
    right: Sequence[int],
    *,
    left_start: int,
    right_start: int,
    length: int,
    right_reversed: bool,
) -> WindowComparison:
    """Compare one pair of width windows and retain every mismatch."""

    if length < 1:
        raise ValueError("length must be positive")
    if not 0 <= left_start <= len(left) - length:
        raise ValueError("left window lies outside sequence")
    if not 0 <= right_start <= len(right) - length:
        raise ValueError("right window lies outside sequence")
    left_window = tuple(left[left_start : left_start + length])
    right_window = tuple(right[right_start : right_start + length])
    if right_reversed:
        right_window = tuple(reversed(right_window))
    mismatches = tuple(
        (index, left_value, right_value)
        for index, (left_value, right_value) in enumerate(
            zip(left_window, right_window, strict=True)
        )
        if left_value != right_value
    )
    return WindowComparison(
        left_start=left_start,
        right_start=right_start,
        right_reversed=right_reversed,
        length=length,
        equal_rows=length - len(mismatches),
        absolute_difference=sum(
            abs(left_value - right_value)
            for left_value, right_value in zip(
                left_window, right_window, strict=True
            )
        ),
        mismatches=mismatches,
    )


def scan_windows(
    left: Sequence[int], right: Sequence[int], *, length: int
) -> tuple[WindowComparison, ...]:
    """Enumerate every start pair and both right-hand orientations."""

    if length < 1 or length > min(len(left), len(right)):
        raise ValueError("length must fit both sequences")
    return tuple(
        compare_windows(
            left,
            right,
            left_start=left_start,
            right_start=right_start,
            length=length,
            right_reversed=right_reversed,
        )
        for left_start in range(len(left) - length + 1)
        for right_start in range(len(right) - length + 1)
        for right_reversed in (False, True)
    )


def best_comparisons(
    comparisons: Sequence[WindowComparison],
) -> tuple[WindowComparison, ...]:
    """Select maximum equality, breaking that score only by absolute error."""

    if not comparisons:
        raise ValueError("comparisons must be non-empty")
    best_score = max(
        (comparison.equal_rows, -comparison.absolute_difference)
        for comparison in comparisons
    )
    return tuple(
        comparison
        for comparison in comparisons
        if (comparison.equal_rows, -comparison.absolute_difference) == best_score
    )
