from pathlib import Path

from eye_mystery.noita_wall_assets import (
    WALL_ASSET_SPECS,
    align_wall,
    load_wall_grids,
    normalized_occurrence_classes,
    rune_codebook,
    xor_codebook_hits,
)
from eye_mystery.noita_wall_messages import load_wall_message_lines


ROOT = Path(__file__).parents[1]
ASSET_DIRECTORY = (
    ROOT / "artifacts/wall-messages/raw/data/biome_impl/hidden"
)
TEXT_PATH = ROOT / "artifacts/noita-wall-messages-en.txt"


def _aligned_walls():
    lines_by_id = dict(load_wall_message_lines(TEXT_PATH))
    return tuple(
        align_wall(grid, lines_by_id[grid.spec.map_id])
        for grid in load_wall_grids(ASSET_DIRECTORY)
    )


def test_wall_assets_are_the_complete_static_rgba_set():
    grids = load_wall_grids(ASSET_DIRECTORY)
    assert tuple(grid.spec for grid in grids) == WALL_ASSET_SPECS
    assert all(
        tuple(chunk.kind for chunk in grid.image.chunks)
        == ("IHDR", "IDAT", "IEND")
        for grid in grids
    )
    assert [(grid.columns, len(grid.rows)) for grid in grids] == [
        (65, 15),
        (45, 8),
        (36, 12),
        (40, 3),
        (48, 6),
        (33, 3),
        (39, 3),
        (49, 4),
        (33, 3),
        (49, 4),
        (49, 5),
        (65, 5),
    ]


def test_surface_text_aligns_uniquely_and_has_a_bijective_codebook():
    walls = _aligned_walls()
    assert [
        len(wall.grid.rows) - len(wall.lines)
        for wall in walls
    ] == [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1]
    codebook = rune_codebook(walls)
    assert len(codebook) == 29
    assert set(codebook) == set("ABCDEFGHIJKLMNOPRSTUVWXY!',.?")
    assert len(set(codebook.values())) == 29


def test_no_symbol_has_an_occurrence_level_cell_variant():
    occurrences = normalized_occurrence_classes(_aligned_walls())
    assert occurrences
    assert all(len(templates) == 1 for templates in occurrences.values())


def test_xor_does_not_decode_messages_or_lines_to_authored_runes():
    walls = _aligned_walls()
    codebook = rune_codebook(walls)
    messages = tuple(
        "".join(line.text for line in wall.lines)
        for wall in walls
    )
    lines = tuple(line.text for wall in walls for line in wall.lines)
    assert xor_codebook_hits(messages, codebook) == ()
    assert xor_codebook_hits(lines, codebook) == ()
