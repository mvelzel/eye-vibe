#!/usr/bin/env python3
"""Test the Cauldron Room's fixed sand texture as an 83-by-26 sieve."""

from __future__ import annotations

import argparse
import hashlib
import math
import random
from collections import Counter
from io import BytesIO
from pathlib import Path

import numpy as np
from PIL import Image

from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, ROW_PAIR_TRIGRAM_LENGTHS
from eye_mystery.texture_sieve import boundary_trimmed_masks
from eye_mystery.blood_sieve import split_row_pair_values
from eye_mystery.wak import WakArchive


SCORE_TABLE = np.array(
    [
        4
        if byte == 32
        else 3
        if 65 <= byte <= 90 or 97 <= byte <= 122
        else 1
        if byte in b".,;:'!?-()\n\r" or 48 <= byte <= 57
        else 0
        if 32 <= byte <= 126
        else -4
        for byte in range(256)
    ],
    dtype=np.int16,
)


def eye_events() -> tuple[np.ndarray, np.ndarray]:
    positions = []
    values = []
    for name in MESSAGE_ORDER:
        for row in split_row_pair_values(
            MESSAGES[name], ROW_PAIR_TRIGRAM_LENGTHS[name]
        ):
            positions.extend(range(len(row)))
            values.extend(row)
    return np.asarray(positions), np.asarray(values)


def best_packed_score(
    bases: np.ndarray, *, include_alternating: bool = True
):
    """Scan the same bounded byte framings used for the blood-mask test."""

    variants = []
    descriptions = []
    alternating = np.arange(bases.shape[1], dtype=np.uint8) & 1
    mask_variants = [("static", bases)]
    if include_alternating:
        mask_variants.append(("alternating", bases ^ alternating))
    for mask_name, masked in mask_variants:
        for reverse in (False, True):
            oriented = masked[:, ::-1] if reverse else masked
            for invert in (False, True):
                variants.append(1 - oriented if invert else oriented)
                descriptions.extend(
                    (mask_name, reverse, invert) for _ in range(len(bases))
                )
    streams = np.concatenate(variants, axis=0).astype(np.uint16)
    best = None
    for width in (7, 8):
        for lsb in (False, True):
            weights = 1 << np.arange(width, dtype=np.uint16)
            if not lsb:
                weights = weights[::-1]
            for offset in range(width):
                usable = (streams.shape[1] - offset) // width * width
                chunks = streams[:, offset : offset + usable].reshape(
                    len(streams), -1, width
                )
                data = np.sum(chunks * weights, axis=2).astype(np.uint8)
                raw = SCORE_TABLE[data].sum(axis=1)
                normalized = raw / data.shape[1]
                index = int(np.argmax(normalized))
                candidate = (
                    float(normalized[index]),
                    int(raw[index]),
                    index,
                    width,
                    lsb,
                    offset,
                    bytes(data[index]),
                )
                if best is None or candidate[:2] > best[:2]:
                    best = candidate
    assert best is not None
    block = best[2] // len(bases)
    base_index = best[2] % len(bases)
    return best, descriptions[block * len(bases) + base_index], base_index


def bases_for_values(
    masks: np.ndarray,
    positions: np.ndarray,
    values: np.ndarray,
) -> np.ndarray:
    return masks[:, positions, values]


def byte_diagnostics(data: bytes) -> str:
    counts = Counter(data)
    entropy = -sum(
        count / len(data) * math.log2(count / len(data))
        for count in counts.values()
    )
    return (
        f"distinct={len(counts)} entropy={entropy:.4f} "
        f"most_common={counts.most_common(5)}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("texture", type=Path)
    parser.add_argument("--archive", type=Path)
    parser.add_argument("--null-trials", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=482160)
    args = parser.parse_args()

    raw = args.texture.read_bytes()
    image = Image.open(args.texture).convert("RGB")
    colours = Counter(map(tuple, np.asarray(image).reshape(-1, 3)))
    if len(colours) != 2:
        raise SystemExit(f"expected two colours, found {len(colours)}")
    foreground = min(colours, key=colours.get)
    rows = tuple(
        tuple(int(image.getpixel((x, y)) == foreground) for x in range(image.width))
        for y in range(image.height)
    )
    variants = boundary_trimmed_masks(rows)
    masks = np.asarray([variant.rows for variant in variants], dtype=np.uint8)
    positions, values = eye_events()
    bases = bases_for_values(masks, positions, values)
    best, transform, base_index = best_packed_score(bases)
    static_best, static_transform, static_base_index = best_packed_score(
        bases, include_alternating=False
    )

    print(
        f"texture={args.texture} size={image.width}x{image.height} "
        f"pixels={image.width * image.height} colours={dict(colours)}"
    )
    print(
        f"sha256={hashlib.sha256(raw).hexdigest()} foreground={foreground} "
        f"foreground_pixels={colours[foreground]} excess_over_83x26="
        f"{image.width * image.height - 83 * 26}"
    )
    print(f"distinct natural 26x83 masks={len(variants)}")
    print(
        f"best normalized text score={best[0]:.6f} raw={best[1]} "
        f"mask={variants[base_index].name} stream_transform={transform} "
        f"width={best[3]} lsb_first={best[4]} offset={best[5]}"
    )
    print("bytes repr:", repr(best[6]))
    print("byte diagnostics:", byte_diagnostics(best[6]))
    print(
        f"best static-only score={static_best[0]:.6f} raw={static_best[1]} "
        f"mask={variants[static_base_index].name} "
        f"stream_transform={static_transform} width={static_best[3]} "
        f"lsb_first={static_best[4]} offset={static_best[5]}"
    )
    print("static bytes repr:", repr(static_best[6]))
    print("static byte diagnostics:", byte_diagnostics(static_best[6]))
    natural_hit_counts = bases.sum(axis=1)
    print(
        f"selected foreground bits across {bases.shape[1]} Eye symbols: "
        f"min={int(natural_hit_counts.min())} "
        f"median={float(np.median(natural_hit_counts)):g} "
        f"max={int(natural_hit_counts.max())}"
    )

    rng = random.Random(args.seed)
    alphabet = list(range(83))
    null_scores = []
    null_static_scores = []
    null_min_hits = []
    for _trial in range(args.null_trials):
        rng.shuffle(alphabet)
        shuffled_values = np.asarray(alphabet, dtype=np.int16)[values]
        null_bases = bases_for_values(masks, positions, shuffled_values)
        null_best, _transform, _base_index = best_packed_score(null_bases)
        null_static, _transform, _base_index = best_packed_score(
            null_bases, include_alternating=False
        )
        null_scores.append(null_best[0])
        null_static_scores.append(null_static[0])
        null_min_hits.append(int(null_bases.sum(axis=1).min()))
    exceed = sum(score >= best[0] for score in null_scores)
    print(
        f"global-alphabet-permutation null: exceed={exceed}/{args.null_trials} "
        f"p={(exceed + 1) / (args.null_trials + 1):.6f} "
        f"mean={sum(null_scores) / len(null_scores):.6f} "
        f"min={min(null_scores):.6f} max={max(null_scores):.6f}"
    )
    static_exceed = sum(score >= static_best[0] for score in null_static_scores)
    print(
        f"static-only null: exceed={static_exceed}/{args.null_trials} "
        f"p={(static_exceed + 1) / (args.null_trials + 1):.6f} "
        f"mean={sum(null_static_scores) / len(null_static_scores):.6f} "
        f"min={min(null_static_scores):.6f} "
        f"max={max(null_static_scores):.6f}"
    )
    observed_min_hits = int(natural_hit_counts.min())
    hit_tail = sum(count <= observed_min_hits for count in null_min_hits)
    print(
        f"minimum-hit null: <=observed={hit_tail}/{args.null_trials} "
        f"p={(hit_tail + 1) / (args.null_trials + 1):.6f} "
        f"mean={sum(null_min_hits) / len(null_min_hits):.3f} "
        f"min={min(null_min_hits)} max={max(null_min_hits)}"
    )

    if args.archive is not None:
        archive = WakArchive.open(args.archive)
        target_area = image.width * image.height
        target_dimensions = image.size
        rows = []
        errors = 0
        for entry in archive.entries:
            if not entry.path.lower().endswith(".png"):
                continue
            try:
                with Image.open(BytesIO(archive.read(entry))) as candidate:
                    width, height = candidate.size
            except OSError:
                errors += 1
                continue
            rows.append((entry.path, width, height, width * height))
        material_rows = [
            row for row in rows if row[0].startswith("data/materials_gfx/")
        ]
        for label, candidates in (("all", rows), ("materials_gfx", material_rows)):
            exact_dimensions = [
                row for row in candidates if row[1:3] == target_dimensions
            ]
            exact_area = [row for row in candidates if row[3] == target_area]
            within_two = [
                row for row in candidates if abs(row[3] - 83 * 26) <= 2
            ]
            within_ten = [
                row for row in candidates if abs(row[3] - 83 * 26) <= 10
            ]
            print(
                f"archive area calibration ({label}): decoded={len(candidates)} "
                f"exact_dimensions={len(exact_dimensions)} "
                f"exact_area={len(exact_area)} within_83x26±2={len(within_two)} "
                f"within_83x26±10={len(within_ten)}"
            )
            for path, width, height, area in within_two:
                print(f"  {path} {width}x{height} area={area}")
        print(f"archive png decode errors={errors}")


if __name__ == "__main__":
    main()
