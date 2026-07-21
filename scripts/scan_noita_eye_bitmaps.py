#!/usr/bin/env python3
"""Search every WAK PNG for exact solid-colour copies of native Eye glyphs.

The five 11x7 masks below are recovered from the current executable's bitmap
constructor at virtual address 0x61e880.  A match may use any foreground and
background colours.  Integer scales use nearest-neighbour expansion, matching
Noita's ordinary pixel-art treatment without introducing threshold choices.

This optional visual-asset scan requires Pillow and NumPy.
"""

from __future__ import annotations

import argparse
from io import BytesIO
from pathlib import Path

import numpy as np
from PIL import Image, UnidentifiedImageError

from eye_mystery.wak import WakArchive


GLYPH_ROWS = (
    (
        "....###....",
        "..##...##..",
        ".#...#...#.",
        "#...###...#",
        ".#...#...#.",
        "..##...##..",
        "....###....",
    ),
    (
        "....###....",
        "..##.#.##..",
        ".#..###..#.",
        "#....#....#",
        ".#.......#.",
        "..##...##..",
        "....###....",
    ),
    (
        "....###....",
        "..##...##..",
        ".#....#..#.",
        "#....###..#",
        ".#....#..#.",
        "..##...##..",
        "....###....",
    ),
    (
        "....###....",
        "..##...##..",
        ".#.......#.",
        "#....#....#",
        ".#..###..#.",
        "..##.#.##..",
        "....###....",
    ),
    (
        "....###....",
        "..##...##..",
        ".#..#....#.",
        "#..###....#",
        ".#..#....#.",
        "..##...##..",
        "....###....",
    ),
)

GLYPH_NAMES = ("centre", "up", "right", "down", "left")


def masks(max_scale: int) -> tuple[tuple[int, tuple[tuple[str, np.ndarray], ...]], ...]:
    by_scale = []
    bases = tuple(
        (
            name,
            np.array([[value == "#" for value in row] for row in rows]),
        )
        for name, rows in zip(GLYPH_NAMES, GLYPH_ROWS, strict=True)
    )
    for scale in range(1, max_scale + 1):
        scaled = []
        for name, base in bases:
            scaled.append(
                (name, np.repeat(np.repeat(base, scale, axis=0), scale, axis=1))
            )
        by_scale.append((scale, tuple(scaled)))
    return tuple(by_scale)


def exact_solid_colour_hits(
    pixels: np.ndarray, named_masks: tuple[tuple[str, np.ndarray], ...]
) -> tuple[tuple[str, int, int, tuple[int, int, int, int]], ...]:
    """Find windows exactly equal to any same-sized solid-colour Eye mask."""
    mask = named_masks[0][1]
    image_height, image_width, _ = pixels.shape
    height, width = mask.shape
    output_height = image_height - height + 1
    output_width = image_width - width + 1
    if output_height <= 0 or output_width <= 0:
        return ()

    common_foreground = np.logical_and.reduce([item[1] for item in named_masks])
    common_background = np.logical_and.reduce([~item[1] for item in named_masks])
    foreground = np.argwhere(common_foreground)
    background = np.argwhere(common_background)
    # Use well-separated on/off samples before inspecting complete windows.
    foreground_samples = foreground[
        np.linspace(0, len(foreground) - 1, min(12, len(foreground)), dtype=int)
    ]
    background_samples = background[
        np.linspace(0, len(background) - 1, min(12, len(background)), dtype=int)
    ]
    anchor_y, anchor_x = foreground_samples[0]
    anchor = pixels[
        anchor_y : anchor_y + output_height,
        anchor_x : anchor_x + output_width,
    ]
    candidates = anchor[:, :, 3] != 0
    for sample_y, sample_x in foreground_samples[1:]:
        sample = pixels[
            sample_y : sample_y + output_height,
            sample_x : sample_x + output_width,
        ]
        candidates &= np.all(sample == anchor, axis=2)
    for sample_y, sample_x in background_samples:
        sample = pixels[
            sample_y : sample_y + output_height,
            sample_x : sample_x + output_width,
        ]
        candidates &= ~np.all(sample == anchor, axis=2)

    hits = []
    for y, x in np.argwhere(candidates):
        window = pixels[y : y + height, x : x + width]
        colour = window[anchor_y, anchor_x]
        equality_mask = np.all(window == colour, axis=2)
        for name, candidate_mask in named_masks:
            if np.array_equal(equality_mask, candidate_mask):
                hits.append((name, int(x), int(y), tuple(map(int, colour))))
    return tuple(hits)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    parser.add_argument("--max-scale", type=int, default=4)
    args = parser.parse_args()
    if args.max_scale < 1:
        raise SystemExit("--max-scale must be positive")

    archive = WakArchive.open(args.archive)
    png_entries = tuple(
        entry for entry in archive.entries if entry.path.lower().endswith(".png")
    )
    templates = masks(args.max_scale)
    print(
        f"pngs={len(png_entries)} templates={5 * len(templates)}",
        flush=True,
    )
    decoded = 0
    errors = 0
    total_hits = 0
    for entry_index, entry in enumerate(png_entries, 1):
        try:
            with Image.open(BytesIO(archive.read(entry))) as image:
                pixels = np.asarray(image.convert("RGBA"))
        except (OSError, UnidentifiedImageError) as error:
            errors += 1
            print(
                f"decode-error path={entry.path} "
                f"type={type(error).__name__} detail={error}",
                flush=True,
            )
            continue
        decoded += 1
        for scale, named_masks in templates:
            for name, x, y, colour in exact_solid_colour_hits(pixels, named_masks):
                total_hits += 1
                print(
                    f"{entry.path} glyph={name} scale={scale} "
                    f"x={x} y={y} rgba={colour}",
                    flush=True,
                )
        if entry_index % 500 == 0:
            print(f"progress={entry_index}/{len(png_entries)}", flush=True)
    print(f"decoded={decoded} errors={errors} hits={total_hits}", flush=True)


if __name__ == "__main__":
    main()
