"""Parse and align Noita's twelve authored Wall Message PNG assets.

The source files are tiny RGBA PNGs laid out on a 5-by-7 cell grid.  A rune
occupies a 4-by-4 bitmap inside each cell.  The decoder is intentionally
standard-library-only so the evidence does not depend on an image editor's
interpretation of invisible RGB channels.
"""

from __future__ import annotations

import binascii
import struct
import zlib
from collections import defaultdict
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
CELL_WIDTH = 5
CELL_HEIGHT = 7
RUNE_WIDTH = 4
RUNE_HEIGHT = 4
RUNE_TOP = 1


@dataclass(frozen=True)
class WallAssetSpec:
    filename: str
    map_id: str
    world_x: int
    world_y: int


# Authored order in data/biome/_pixel_scenes.xml.
WALL_ASSET_SPECS = (
    WallAssetSpec("boss_arena.png", "G1", 3425, 12650),
    WallAssetSpec("boss_arena_under.png", "G2", 2976, 13692),
    WallAssetSpec("boss_arena_under_right.png", "G3", 4238, 15055),
    WallAssetSpec("completely_random.png", "G4", -5400, 21887),
    WallAssetSpec("completely_random_2.png", "G5", 4256, 26954),
    WallAssetSpec("fungal_caverns_1.png", "G6", 3419, 2652),
    WallAssetSpec("holy_mountain_1.png", "G7", 1785, 1325),
    WallAssetSpec("jungle_right.png", "G8", 2806, 6614),
    WallAssetSpec("mountain_text.png", "G9", 700, -440),
    WallAssetSpec("under_the_wand_cave.png", "G10", -4448, 4487),
    WallAssetSpec("vault_inside.png", "G11", -2120, 8446),
    WallAssetSpec("crypt_left.png", "G12", -4129, 10533),
)


@dataclass(frozen=True)
class PngChunk:
    kind: str
    length: int
    crc32: int


@dataclass(frozen=True)
class RgbaImage:
    width: int
    height: int
    pixels: bytes
    chunks: tuple[PngChunk, ...]

    def pixel(self, x: int, y: int) -> tuple[int, int, int, int]:
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise IndexError((x, y))
        offset = 4 * (y * self.width + x)
        return tuple(self.pixels[offset : offset + 4])  # type: ignore[return-value]


@dataclass(frozen=True)
class RuneCell:
    column: int
    row: int
    mask: int
    classes: tuple[int, ...]

    @property
    def active(self) -> bool:
        return self.mask != 0

    @property
    def allocated(self) -> bool:
        return any(value != 0 for value in self.classes)


@dataclass(frozen=True)
class WallGrid:
    spec: WallAssetSpec
    image: RgbaImage
    rows: tuple[tuple[RuneCell, ...], ...]

    @property
    def columns(self) -> int:
        return self.image.width // CELL_WIDTH


@dataclass(frozen=True)
class AlignedLine:
    text: str
    offset: int
    cells: tuple[RuneCell, ...]


@dataclass(frozen=True)
class AlignedWall:
    grid: WallGrid
    lines: tuple[AlignedLine, ...]


def _paeth(left: int, above: int, upper_left: int) -> int:
    prediction = left + above - upper_left
    distances = (
        abs(prediction - left),
        abs(prediction - above),
        abs(prediction - upper_left),
    )
    return (left, above, upper_left)[distances.index(min(distances))]


def decode_rgba_png(data: bytes) -> RgbaImage:
    """Decode an 8-bit, non-interlaced RGBA PNG and validate every CRC."""

    if not data.startswith(PNG_SIGNATURE):
        raise ValueError("invalid PNG signature")
    position = len(PNG_SIGNATURE)
    chunks: list[PngChunk] = []
    idat = bytearray()
    width = height = None
    while position < len(data):
        if position + 12 > len(data):
            raise ValueError("truncated PNG chunk")
        length = struct.unpack(">I", data[position : position + 4])[0]
        kind_bytes = data[position + 4 : position + 8]
        payload_start = position + 8
        payload_end = payload_start + length
        if payload_end + 4 > len(data):
            raise ValueError("truncated PNG payload")
        payload = data[payload_start:payload_end]
        expected_crc = struct.unpack(">I", data[payload_end : payload_end + 4])[0]
        actual_crc = binascii.crc32(kind_bytes + payload) & 0xFFFFFFFF
        if actual_crc != expected_crc:
            raise ValueError(f"bad {kind_bytes!r} CRC")
        kind = kind_bytes.decode("ascii")
        chunks.append(PngChunk(kind, length, expected_crc))
        if kind == "IHDR":
            if length != 13:
                raise ValueError("invalid IHDR length")
            (
                width,
                height,
                bit_depth,
                color_type,
                compression,
                filtering,
                interlace,
            ) = struct.unpack(">IIBBBBB", payload)
            if (bit_depth, color_type, compression, filtering, interlace) != (
                8,
                6,
                0,
                0,
                0,
            ):
                raise ValueError("only 8-bit non-interlaced RGBA PNGs are supported")
        elif kind == "IDAT":
            idat.extend(payload)
        elif kind == "IEND":
            if length != 0 or payload_end + 4 != len(data):
                raise ValueError("invalid IEND")
            break
        position = payload_end + 4
    if width is None or height is None:
        raise ValueError("missing IHDR")

    encoded = zlib.decompress(bytes(idat))
    stride = width * 4
    if len(encoded) != height * (stride + 1):
        raise ValueError("unexpected decompressed PNG size")
    decoded = bytearray(height * stride)
    source_offset = 0
    for y in range(height):
        filter_type = encoded[source_offset]
        source_offset += 1
        source = encoded[source_offset : source_offset + stride]
        source_offset += stride
        target_offset = y * stride
        for x, value in enumerate(source):
            left = decoded[target_offset + x - 4] if x >= 4 else 0
            above = decoded[target_offset + x - stride] if y else 0
            upper_left = (
                decoded[target_offset + x - stride - 4] if y and x >= 4 else 0
            )
            if filter_type == 0:
                result = value
            elif filter_type == 1:
                result = value + left
            elif filter_type == 2:
                result = value + above
            elif filter_type == 3:
                result = value + ((left + above) // 2)
            elif filter_type == 4:
                result = value + _paeth(left, above, upper_left)
            else:
                raise ValueError(f"unsupported PNG filter {filter_type}")
            decoded[target_offset + x] = result & 0xFF
    return RgbaImage(width, height, bytes(decoded), tuple(chunks))


def _pixel_class(pixel: tuple[int, int, int, int]) -> int:
    red, green, blue, alpha = pixel
    if alpha:
        if alpha != 255:
            raise ValueError(f"unexpected partial alpha {pixel}")
        return 2
    if (red, green, blue) == (0, 0, 0):
        return 0
    if (red, green, blue) == (255, 255, 255):
        return 1
    raise ValueError(f"unexpected transparent pixel {pixel}")


def parse_wall_grid(path: Path, spec: WallAssetSpec) -> WallGrid:
    image = decode_rgba_png(path.read_bytes())
    if image.width % CELL_WIDTH or image.height % CELL_HEIGHT:
        raise ValueError(f"{path.name} is not a 5-by-7 cell grid")
    rows = []
    for row in range(image.height // CELL_HEIGHT):
        cells = []
        for column in range(image.width // CELL_WIDTH):
            classes = tuple(
                _pixel_class(
                    image.pixel(
                        column * CELL_WIDTH + x,
                        row * CELL_HEIGHT + y,
                    )
                )
                for y in range(CELL_HEIGHT)
                for x in range(CELL_WIDTH)
            )
            mask = 0
            for y in range(RUNE_HEIGHT):
                for x in range(RUNE_WIDTH):
                    pixel = image.pixel(
                        column * CELL_WIDTH + x,
                        row * CELL_HEIGHT + RUNE_TOP + y,
                    )
                    if pixel[3]:
                        mask |= 1 << (y * RUNE_WIDTH + x)
            opaque_indices = {
                index for index, value in enumerate(classes) if value == 2
            }
            allowed_indices = {
                (RUNE_TOP + y) * CELL_WIDTH + x
                for y in range(RUNE_HEIGHT)
                for x in range(RUNE_WIDTH)
            }
            if not opaque_indices <= allowed_indices:
                raise ValueError(f"ink outside rune box at {column},{row}")
            cells.append(RuneCell(column, row, mask, classes))
        rows.append(tuple(cells))
    return WallGrid(spec, image, tuple(rows))


def load_wall_grids(directory: Path) -> tuple[WallGrid, ...]:
    return tuple(
        parse_wall_grid(directory / spec.filename, spec)
        for spec in WALL_ASSET_SPECS
    )


def align_wall(grid: WallGrid, lines: tuple[str, ...]) -> AlignedWall:
    """Align translated surface lines to the exact cell geometry.

    Spaces are genuine empty cells.  A line offset is accepted only if every
    non-space character lands on ink, every space lands on an empty cell, and
    there is no ink outside the proposed surface line.
    """

    if len(lines) > len(grid.rows):
        raise ValueError(
            f"{grid.spec.map_id}: {len(lines)} text lines for {len(grid.rows)} rows"
        )
    trailing_rows = grid.rows[len(lines) :]
    if any(cell.active for cells in trailing_rows for cell in cells):
        raise ValueError(f"{grid.spec.map_id}: ink after final surface line")
    result = []
    for row, (cells, text) in enumerate(
        zip(grid.rows[: len(lines)], lines, strict=True)
    ):
        candidates = []
        for offset in range(len(cells) - len(text) + 1):
            if any(cell.active for cell in cells[:offset]):
                continue
            if any(cell.active for cell in cells[offset + len(text) :]):
                continue
            if all(
                cell.active == (character != " ")
                for cell, character in zip(
                    cells[offset : offset + len(text)],
                    text,
                    strict=True,
                )
            ):
                candidates.append(offset)
        if len(candidates) != 1:
            raise ValueError(
                f"{grid.spec.map_id} row {row}: offsets {candidates!r} for {text!r}"
            )
        offset = candidates[0]
        result.append(
            AlignedLine(text, offset, cells[offset : offset + len(text)])
        )
    return AlignedWall(grid, tuple(result))


def rune_codebook(
    walls: Iterable[AlignedWall],
) -> dict[str, int]:
    """Return the exact one-character-to-one-mask surface codebook."""

    by_character: dict[str, set[int]] = defaultdict(set)
    by_mask: dict[int, set[str]] = defaultdict(set)
    for wall in walls:
        for line in wall.lines:
            for character, cell in zip(line.text, line.cells, strict=True):
                if character == " ":
                    if cell.active:
                        raise ValueError("space aligned to active rune")
                    continue
                character = character.upper()
                by_character[character].add(cell.mask)
                by_mask[cell.mask].add(character)
    ambiguous_characters = {
        character: masks
        for character, masks in by_character.items()
        if len(masks) != 1
    }
    ambiguous_masks = {
        mask: characters for mask, characters in by_mask.items() if len(characters) != 1
    }
    if ambiguous_characters or ambiguous_masks:
        raise ValueError(
            f"ambiguous codebook: chars={ambiguous_characters}, masks={ambiguous_masks}"
        )
    return {character: next(iter(masks)) for character, masks in by_character.items()}


def normalized_occurrence_classes(
    walls: Iterable[AlignedWall],
) -> Mapping[str, frozenset[tuple[int, ...]]]:
    """Return complete normalized 5-by-7 cell templates for each symbol."""

    occurrences: dict[str, set[tuple[int, ...]]] = defaultdict(set)
    for wall in walls:
        for line in wall.lines:
            for character, cell in zip(line.text, line.cells, strict=True):
                character = character.upper()
                occurrences[character].add(cell.classes)
    return {
        character: frozenset(classes)
        for character, classes in occurrences.items()
    }


def xor_mask(text: str, codebook: Mapping[str, int]) -> int:
    result = 0
    for character in text:
        if character != " ":
            result ^= codebook[character.upper()]
    return result


def xor_codebook_hits(
    segments: Iterable[str],
    codebook: Mapping[str, int],
) -> tuple[tuple[str, str], ...]:
    """Return segments whose XOR is itself an authored surface rune."""

    inverse = {mask: character for character, mask in codebook.items()}
    if len(inverse) != len(codebook):
        raise ValueError("codebook masks are not unique")
    result = []
    for segment in segments:
        mask = xor_mask(segment, codebook)
        if mask in inverse:
            result.append((segment, inverse[mask]))
    return tuple(result)


def mask_rows(mask: int) -> tuple[int, int, int, int]:
    return tuple((mask >> (4 * row)) & 0xF for row in range(4))  # type: ignore[return-value]
