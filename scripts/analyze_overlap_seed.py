#!/usr/bin/env python3
"""Analyze the exact Eye Message superpositions at world seed 239847392."""

from __future__ import annotations

import argparse
from collections import Counter
from collections.abc import Sequence
import random

from eye_mystery.corpus import MESSAGES, ROW_PAIR_TRIGRAM_LENGTHS
from eye_mystery.visual_rows import (
    direction_mask_rows,
    interleave_visual_rows,
    visual_rows,
)


OVERLAP_WORLD_SEED = 239_847_392
PLACEMENT_XOR_SALT = 0x0E4BC7E0


def render_masks(rows: tuple[tuple[int, ...], ...]) -> str:
    """Render nonempty masks as base-32 digits, preserving the row layout."""
    alphabet = "0123456789abcdefghijklmnopqrstuv"
    return "\n".join("".join(alphabet[value] for value in row) for row in rows)


def remap_mask(mask: int, direction_map: Sequence[int]) -> int:
    """Apply an old-direction to new-direction permutation to a mask."""
    return sum(1 << direction_map[old] for old in range(5) if mask & (1 << old))


def traversals(rows: tuple[tuple[int, ...], ...]) -> dict[str, tuple[int, ...]]:
    """Return the small set of readings supported by the displayed geometry."""
    row_major = tuple(value for row in rows for value in row)
    row_reverse = tuple(value for row in rows for value in reversed(row))
    bottom_up = tuple(value for row in reversed(rows) for value in row)
    bottom_up_reverse = tuple(value for row in reversed(rows) for value in reversed(row))
    boustrophedon = tuple(
        value
        for index, row in enumerate(rows)
        for value in (row if index % 2 == 0 else tuple(reversed(row)))
    )
    accepted = interleave_visual_rows(rows)
    return {
        "rows-LR": row_major,
        "rows-RL": row_reverse,
        "bottom-LR": bottom_up,
        "bottom-RL": bottom_up_reverse,
        "boustrophedon": boustrophedon,
        "accepted": accepted,
        "accepted-reversed": tuple(reversed(accepted)),
    }


def pack_five_bit(values: Sequence[int], least_significant_bit_first: bool) -> bytes:
    """Pack a sequence of five-bit values into a conventional byte stream."""
    bits: list[int] = []
    indexes = range(5) if least_significant_bit_first else range(4, -1, -1)
    for value in values:
        bits.extend((value >> index) & 1 for index in indexes)
    return bytes(
        sum(bit << (7 - offset) for offset, bit in enumerate(bits[index : index + 8]))
        for index in range(0, len(bits) - 7, 8)
    )


def printable_count(data: bytes) -> int:
    return sum(byte in (9, 10, 13) or 32 <= byte <= 126 for byte in data)


def square_direction_maps() -> tuple[tuple[int, ...], ...]:
    # Centre stays centre; the four cardinal directions admit the eight square
    # rotations/reflections visible on screen.
    rotations = (
        (0, 1, 2, 3, 4),
        (0, 2, 3, 4, 1),
        (0, 3, 4, 1, 2),
        (0, 4, 1, 2, 3),
    )
    reflection = (0, 1, 4, 3, 2)
    direction_maps: list[tuple[int, ...]] = []
    for rotation in rotations:
        direction_maps.append(rotation)
        direction_maps.append(tuple(rotation[reflection[index]] for index in range(5)))
    return tuple(direction_maps)


def direct_decode_candidates(
    rows: tuple[tuple[int, ...], ...]
) -> list[tuple[int, str, str]]:
    """Enumerate direct byte readings under visible square symmetries."""
    direction_maps = square_direction_maps()

    ranked: list[tuple[int, str, str]] = []
    for traversal_name, values in traversals(rows).items():
        for map_index, direction_map in enumerate(direction_maps):
            remapped = tuple(remap_mask(value, direction_map) for value in values)
            for bit_order in ("msb", "lsb"):
                data = pack_five_bit(remapped, bit_order == "lsb")
                ranked.append(
                    (
                        printable_count(data),
                        f"{traversal_name}/D4-{map_index}/{bit_order}",
                        data[:48].decode("ascii", errors="replace"),
                    )
                )
    return ranked


def direct_decode_report(
    rows: tuple[tuple[int, ...], ...], null_trials: int, rng: random.Random
) -> None:
    ranked = direct_decode_candidates(rows)
    best = sorted(ranked, reverse=True)[:3]
    denominator = len(pack_five_bit(next(iter(traversals(rows).values())), False))
    print("  best direct 5-bit-to-byte readings:")
    for printable, description, preview in best:
        print(f"    {printable}/{denominator} printable {description}: {preview!r}")

    for name in ("rows-LR", "accepted"):
        values = traversals(rows)[name]
        one_based = "".join(chr(64 + value) if 1 <= value <= 26 else " " for value in values)
        zero_based = "".join(chr(65 + value) if 0 <= value <= 25 else " " for value in values)
        print(f"  {name} direct letters (1=A): {one_based[:120]!r}")
        print(f"  {name} direct letters (0=A): {zero_based[:120]!r}")

    if null_trials:
        widths = tuple(len(row) for row in rows)
        flat = [value for row in rows for value in row]
        null_scores: list[int] = []
        for _ in range(null_trials):
            rng.shuffle(flat)
            cursor = 0
            shuffled_rows = []
            for width in widths:
                shuffled_rows.append(tuple(flat[cursor : cursor + width]))
                cursor += width
            null_scores.append(
                max(candidate[0] for candidate in direct_decode_candidates(tuple(shuffled_rows)))
            )
        observed = best[0][0]
        exceedances = sum(score >= observed for score in null_scores)
        ordered = sorted(null_scores)
        print(
            "  shuffled-position null for best printable count: "
            f"observed={observed}, median={ordered[len(ordered) // 2]}, "
            f"range={ordered[0]}..{ordered[-1]}, "
            f"p={(exceedances + 1) / (null_trials + 1):.4f} "
            f"({null_trials} trials)"
        )


def report(
    side: str, names: tuple[str, ...], null_trials: int, rng: random.Random
) -> None:
    sources = tuple(
        visual_rows(MESSAGES[name], ROW_PAIR_TRIGRAM_LENGTHS[name]) for name in names
    )
    masks = direction_mask_rows(sources)
    flat = tuple(value for row in masks for value in row)
    counts = Counter(flat)
    popcounts = Counter(value.bit_count() for value in flat)
    singleton = sum(count for value, count in counts.items() if value.bit_count() == 1)

    print(f"{side}: {', '.join(names)}")
    print(f"  seed: {OVERLAP_WORLD_SEED} = 0x{PLACEMENT_XOR_SALT:08x}")
    print(f"  geometry: {len(masks)} rows, widths {[len(row) for row in masks]}")
    print(f"  cells: {len(flat)}; distinct direction masks: {len(counts)}")
    print(f"  mask alphabet: {sorted(counts)}")
    print(f"  masks missing from 1..31: {sorted(set(range(1, 32)) - counts.keys())}")
    print(f"  directions per cell: {dict(sorted(popcounts.items()))}")
    print(f"  singleton cells: {singleton}/{len(flat)}")
    print("  base-32 mask rendering (bits are engine directions 0..4):")
    print(render_masks(masks))
    direct_decode_report(masks, null_trials, rng)
    print()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--null-trials", type=int, default=0)
    args = parser.parse_args()
    if OVERLAP_WORLD_SEED != PLACEMENT_XOR_SALT:
        raise AssertionError("the degenerate seed is the XOR salt itself")
    rng = random.Random(0x0E4BC7E0)
    report(
        "east",
        ("east1", "east2", "east3", "east4", "east5"),
        args.null_trials,
        rng,
    )
    report(
        "west",
        ("west1", "west2", "west3", "west4"),
        args.null_trials,
        rng,
    )


if __name__ == "__main__":
    main()
