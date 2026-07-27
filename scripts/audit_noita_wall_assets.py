#!/usr/bin/env python3
"""Reproduce the structural audit of Noita's twelve Wall Message PNGs."""

from __future__ import annotations

import argparse
import hashlib
import re
from collections import Counter, defaultdict
from pathlib import Path

from eye_mystery.noita_wall_assets import (
    align_wall,
    load_wall_grids,
    mask_rows,
    normalized_occurrence_classes,
    rune_codebook,
    xor_codebook_hits,
    xor_mask,
)
from eye_mystery.noita_wall_messages import load_wall_message_lines


def printable_mask(mask: int) -> str:
    return "/".join(
        "".join("#" if row & (1 << column) else "." for column in range(4))
        for row in mask_rows(mask)
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("asset_directory", type=Path)
    parser.add_argument("surface_text", type=Path)
    args = parser.parse_args()

    lines_by_id = dict(load_wall_message_lines(args.surface_text))
    grids = load_wall_grids(args.asset_directory)
    walls = tuple(
        align_wall(grid, lines_by_id[grid.spec.map_id])
        for grid in grids
    )
    codebook = rune_codebook(walls)
    occurrences = normalized_occurrence_classes(walls)

    print("ASSETS")
    for wall in walls:
        path = args.asset_directory / wall.grid.spec.filename
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        print(
            f"{wall.grid.spec.map_id:>3} {wall.grid.spec.filename:<29} "
            f"{wall.grid.columns:>2}x{len(wall.grid.rows):<2} "
            f"world=({wall.grid.spec.world_x:>6},{wall.grid.spec.world_y:>6}) "
            f"chunks={','.join(chunk.kind for chunk in wall.grid.image.chunks)} "
            f"sha256={digest}"
        )

    print("\nLAYOUT")
    print(
        "exact-leading-offset-total="
        f"{sum(line.offset for wall in walls for line in wall.lines)}"
    )
    for wall in walls:
        print(wall.grid.spec.map_id)
        for row, cells in enumerate(wall.grid.rows):
            allocated = [cell.column for cell in cells if cell.allocated]
            active = sum(cell.active for cell in cells)
            interval = (
                f"{min(allocated)}..{max(allocated)}"
                if allocated
                else "-"
            )
            if row < len(wall.lines):
                line = wall.lines[row]
                print(
                    f"  row={row:>2} allocated={interval:<7} "
                    f"active={active:>2} offset={line.offset:>2} "
                    f"len={len(line.text):>2} text={line.text}"
                )
            else:
                print(
                    f"  row={row:>2} allocated={interval:<7} "
                    f"active={active:>2} terminal"
                )

    frequencies = Counter(
        character.upper()
        for wall in walls
        for line in wall.lines
        for character in line.text
        if character != " "
    )
    print("\nCODEBOOK")
    for character in sorted(codebook):
        mask = codebook[character]
        print(
            f"{character!r:>3} mask={mask:04x} "
            f"rows={''.join(f'{row:x}' for row in mask_rows(mask))} "
            f"weight={mask.bit_count():>2} count={frequencies[character]:>3} "
            f"cell_variants={len(occurrences[character])} "
            f"{printable_mask(mask)}"
        )

    equal_counts: dict[int, list[str]] = defaultdict(list)
    for character, count in frequencies.items():
        equal_counts[count].append(character)
    print("\nEQUAL FREQUENCIES")
    for count, characters in sorted(equal_counts.items()):
        if len(characters) > 1:
            print(f"{count:>3}: {' '.join(sorted(characters))}")

    print("\nXOR")
    global_mask = 0
    pixel_sums = [0] * 16
    for wall in walls:
        text = "".join(line.text for line in wall.lines)
        mask = xor_mask(text, codebook)
        global_mask ^= mask
        print(
            f"{wall.grid.spec.map_id:>3} mask={mask:04x} "
            f"weight={mask.bit_count():>2} {printable_mask(mask)}"
        )
    for character, count in frequencies.items():
        mask = codebook[character]
        for bit in range(16):
            if mask & (1 << bit):
                pixel_sums[bit] += count
    print(
        f"ALL mask={global_mask:04x} weight={global_mask.bit_count():>2} "
        f"{printable_mask(global_mask)}"
    )
    segments = {
        "message": tuple(
            "".join(line.text for line in wall.lines)
            for wall in walls
        ),
        "line": tuple(
            line.text
            for wall in walls
            for line in wall.lines
        ),
        "clause": tuple(
            clause
            for wall in walls
            for line in wall.lines
            for clause in re.split(r"[,.?!]+", line.text)
            if clause.strip()
        ),
        "word": tuple(
            match.group()
            for wall in walls
            for line in wall.lines
            for match in re.finditer(r"[A-Za-z]+(?:'[A-Za-z]+)?", line.text)
        ),
    }
    print("exact authored-rune XOR hits:")
    for name, items in segments.items():
        hits = xor_codebook_hits(items, codebook)
        print(
            f"  {name:<7} segments={len(items):>3} hits={len(hits):>2} "
            f"{hits}"
        )
    print("pixel sums:")
    for row in range(4):
        print("  " + " ".join(f"{pixel_sums[4 * row + column]:>4}" for column in range(4)))


if __name__ == "__main__":
    main()
