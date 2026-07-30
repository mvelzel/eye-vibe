"""Exact parser for Noita's mysterious Alchemist cell diagram.

The asset contains two aligned one-hot tapes.  This module recovers their
geometry without interpreting the resulting records as an Eye cipher.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

from .noita_wall_assets import RgbaImage, decode_rgba_png


EXPECTED_SHA256 = (
    "545b4b57c9d046f8bb59828ae0d3669f3a1bde3f7d46419c79281677c905733a"
)
TRANSPARENT = (0, 0, 0, 0)
DARK = (28, 29, 36, 255)
GOLD = (93, 86, 56, 255)


@dataclass(frozen=True)
class BandSpec:
    cell_x: int
    cell_y: int
    columns: int
    group_pitch: int

    @property
    def separator_x_offset(self) -> int:
        return 3 * self.columns


TOP_BAND = BandSpec(cell_x=153, cell_y=203, columns=8, group_pitch=26)
BOTTOM_BAND = BandSpec(cell_x=189, cell_y=217, columns=5, group_pitch=17)
GROUPS = 8


@dataclass(frozen=True)
class HotCell:
    row: int
    column: int


@dataclass(frozen=True)
class AlchemistRecord:
    group: int
    top_row: int
    top_column: int
    bottom_row: int
    bottom_column: int


@dataclass(frozen=True)
class AlchemistDiagram:
    image: RgbaImage
    records: tuple[AlchemistRecord, ...]


@dataclass(frozen=True)
class OrientedRecord:
    group: int
    top_row: int
    top_column: int
    bottom_row: int
    bottom_column: int


@dataclass(frozen=True)
class DiagramVariant:
    reverse_groups: bool
    reverse_columns: bool
    complement_rows: bool = False


def _cell_index(row: int, column: int, columns: int, linearization: str) -> int:
    if linearization == "row-major":
        return row * columns + column
    if linearization == "column-major":
        return 2 * column + row
    raise ValueError("linearization must be 'row-major' or 'column-major'")


def _rectangle(x: int, y: int, width: int, height: int) -> set[tuple[int, int]]:
    return {
        (target_x, target_y)
        for target_y in range(y, y + height)
        for target_x in range(x, x + width)
    }


def _expected_band_pixels(spec: BandSpec) -> set[tuple[int, int]]:
    expected: set[tuple[int, int]] = set()
    for group in range(GROUPS):
        group_x = spec.cell_x + group * spec.group_pitch
        for row in range(2):
            for column in range(spec.columns):
                expected |= _rectangle(
                    group_x + 3 * column,
                    spec.cell_y + 3 * row,
                    2,
                    2,
                )
        if group < GROUPS - 1:
            separator_x = group_x + spec.separator_x_offset
            expected |= _rectangle(separator_x, spec.cell_y - 1, 1, 7)
    return expected


def _parse_band(image: RgbaImage, spec: BandSpec) -> tuple[HotCell, ...]:
    hot_cells = []
    for group in range(GROUPS):
        group_x = spec.cell_x + group * spec.group_pitch
        gold = []
        for row in range(2):
            for column in range(spec.columns):
                colors = {
                    image.pixel(group_x + 3 * column + dx, spec.cell_y + 3 * row + dy)
                    for dy in range(2)
                    for dx in range(2)
                }
                if len(colors) != 1 or not colors <= {DARK, GOLD}:
                    raise ValueError(
                        f"nonuniform cell in group {group}, row {row}, column {column}"
                    )
                if GOLD in colors:
                    gold.append(HotCell(row, column))
        if len(gold) != 1:
            raise ValueError(f"group {group} contains {len(gold)} gold cells")
        if group < GROUPS - 1:
            separator_x = group_x + spec.separator_x_offset
            if any(
                image.pixel(separator_x, y) != DARK
                for y in range(spec.cell_y - 1, spec.cell_y + 6)
            ):
                raise ValueError(f"invalid separator after group {group}")
        hot_cells.append(gold[0])
    return tuple(hot_cells)


def parse_alchemist_diagram(path: Path) -> AlchemistDiagram:
    """Validate the complete PNG and return its sixteen one-hot selections."""

    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        raise ValueError(f"unexpected asset SHA-256 {digest}")
    image = decode_rgba_png(data)
    if (image.width, image.height) != (512, 512):
        raise ValueError(f"unexpected image dimensions {(image.width, image.height)}")

    expected_opaque = _expected_band_pixels(TOP_BAND) | _expected_band_pixels(
        BOTTOM_BAND
    )
    actual_opaque = {
        (x, y)
        for y in range(image.height)
        for x in range(image.width)
        if image.pixel(x, y)[3]
    }
    if actual_opaque != expected_opaque:
        missing = len(expected_opaque - actual_opaque)
        extra = len(actual_opaque - expected_opaque)
        raise ValueError(f"opaque geometry mismatch: {missing} missing, {extra} extra")

    palette: dict[tuple[int, int, int, int], int] = {}
    for y in range(image.height):
        for x in range(image.width):
            color = image.pixel(x, y)
            palette[color] = palette.get(color, 0) + 1
    if palette != {TRANSPARENT: 261_214, DARK: 866, GOLD: 64}:
        raise ValueError(f"unexpected exact palette {palette}")

    top = _parse_band(image, TOP_BAND)
    bottom = _parse_band(image, BOTTOM_BAND)
    records = tuple(
        AlchemistRecord(
            group=group,
            top_row=top[group].row,
            top_column=top[group].column,
            bottom_row=bottom[group].row,
            bottom_column=bottom[group].column,
        )
        for group in range(GROUPS)
    )
    if sorted(record.top_column for record in records) != list(range(GROUPS)):
        raise ValueError("upper gold columns are not a permutation of 0..7")
    if tuple(record.top_row for record in records) not in (
        (0, 1, 0, 1, 0, 1, 0, 1),
        (1, 0, 1, 0, 1, 0, 1, 0),
    ):
        raise ValueError("upper hot rows do not alternate")
    if any(record.top_row == record.bottom_row for record in records):
        raise ValueError("upper and lower hot rows are not complementary")
    return AlchemistDiagram(image, records)


def orient_records(
    diagram: AlchemistDiagram, variant: DiagramVariant
) -> tuple[OrientedRecord, ...]:
    """Apply only the frozen global group, column, and row ambiguities."""

    source = (
        tuple(reversed(diagram.records))
        if variant.reverse_groups
        else diagram.records
    )
    records = []
    for group, record in enumerate(source):
        top_row = 1 - record.top_row if variant.complement_rows else record.top_row
        bottom_row = (
            1 - record.bottom_row if variant.complement_rows else record.bottom_row
        )
        records.append(
            OrientedRecord(
                group=group,
                top_row=top_row,
                top_column=(
                    7 - record.top_column
                    if variant.reverse_columns
                    else record.top_column
                ),
                bottom_row=bottom_row,
                bottom_column=(
                    4 - record.bottom_column
                    if variant.reverse_columns
                    else record.bottom_column
                ),
            )
        )
    return tuple(records)


def lower_tape(
    diagram: AlchemistDiagram, variant: DiagramVariant
) -> tuple[int, ...]:
    return tuple(record.bottom_column for record in orient_records(diagram, variant))


def upper_permutation(
    diagram: AlchemistDiagram, variant: DiagramVariant
) -> tuple[int, ...]:
    return tuple(record.top_column for record in orient_records(diagram, variant))


def sorted_direction_table(
    diagram: AlchemistDiagram, variant: DiagramVariant
) -> tuple[int, ...]:
    """Return lower columns indexed by the corresponding upper column."""

    records = sorted(orient_records(diagram, variant), key=lambda record: record.top_column)
    return tuple(record.bottom_column for record in records)


def upper_digit_tape(
    diagram: AlchemistDiagram,
    variant: DiagramVariant,
    *,
    linearization: str = "row-major",
) -> tuple[int, ...]:
    """Interpret each one-hot 2-by-8 group as a digit in ``0..15``."""

    return tuple(
        _cell_index(record.top_row, record.top_column, 8, linearization)
        for record in orient_records(diagram, variant)
    )


def lower_digit_tape(
    diagram: AlchemistDiagram,
    variant: DiagramVariant,
    *,
    linearization: str = "row-major",
) -> tuple[int, ...]:
    """Interpret each one-hot 2-by-5 group as a digit in ``0..9``."""

    return tuple(
        _cell_index(record.bottom_row, record.bottom_column, 5, linearization)
        for record in orient_records(diagram, variant)
    )


def hexadecimal_text(
    diagram: AlchemistDiagram,
    variant: DiagramVariant,
    *,
    linearization: str = "row-major",
) -> str:
    return "".join(
        format(value, "X")
        for value in upper_digit_tape(
            diagram, variant, linearization=linearization
        )
    )


def decimal_text(
    diagram: AlchemistDiagram,
    variant: DiagramVariant,
    *,
    linearization: str = "row-major",
) -> str:
    return "".join(
        str(value)
        for value in lower_digit_tape(
            diagram, variant, linearization=linearization
        )
    )
