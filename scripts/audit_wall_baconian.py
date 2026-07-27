#!/usr/bin/env python3
"""Audit developer-plausible Baconian readings of Noita's Wall Messages."""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from eye_mystery.corpus import MESSAGES, trigram_values
from eye_mystery.noita_wall_assets import (
    align_wall,
    load_wall_grids,
    rune_codebook,
)
from eye_mystery.noita_wall_messages import load_wall_message_lines
from eye_mystery.wall_baconian import scan_baconian, tokenize_wall


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("asset_directory", type=Path)
    parser.add_argument("surface_text", type=Path)
    parser.add_argument("--top", type=int, default=20)
    args = parser.parse_args()

    line_records = load_wall_message_lines(args.surface_text)
    lines_by_id = dict(line_records)
    grids = load_wall_grids(args.asset_directory)
    walls = tuple(
        align_wall(grid, lines_by_id[grid.spec.map_id])
        for grid in grids
    )
    codebook = rune_codebook(walls)
    words_by_id = {
        map_id: tokenize_wall(map_id, lines)
        for map_id, lines in line_records
    }
    specs = {grid.spec.map_id: grid.spec for grid in grids}
    numeric = tuple(f"G{index}" for index in range(1, 13))
    artifact = tuple(map_id for map_id, _ in line_records)
    orders = {
        "numeric": numeric,
        "numeric-reverse": tuple(reversed(numeric)),
        "artifact": artifact,
        "artifact-reverse": tuple(reversed(artifact)),
        "world-x": tuple(sorted(numeric, key=lambda map_id: specs[map_id].world_x)),
        "world-x-reverse": tuple(
            sorted(numeric, key=lambda map_id: specs[map_id].world_x, reverse=True)
        ),
        "world-y": tuple(sorted(numeric, key=lambda map_id: specs[map_id].world_y)),
        "world-y-reverse": tuple(
            sorted(numeric, key=lambda map_id: specs[map_id].world_y, reverse=True)
        ),
    }
    word_count = sum(map(len, words_by_id.values()))
    you_forms = Counter(
        word.normalized
        for words in words_by_id.values()
        for word in words
        if word.normalized.startswith("you")
    )
    print(f"wall_words={word_count}")
    print(f"west1_glyphs={len(trigram_values(MESSAGES['west1']))}")
    print(f"five_times_west1={5 * len(trigram_values(MESSAGES['west1']))}")
    print(f"you_prefix={sum(you_forms.values())} forms={dict(you_forms)}")
    print("orders:")
    for name, order in orders.items():
        print(f"  {name:<18} {' '.join(order)}")

    candidates = scan_baconian(words_by_id, orders, codebook)
    ranked = sorted(
        candidates,
        key=lambda candidate: (
            candidate.invalid,
            candidate.monogram_chi_square,
            candidate.order_name,
            candidate.rule_name,
        ),
    )
    print(f"models={len(candidates)}")
    print(f"zero_invalid={sum(candidate.invalid == 0 for candidate in candidates)}")
    print("top candidates:")
    for candidate in ranked[: args.top]:
        print(
            f"  invalid={candidate.invalid:>2} "
            f"chi2={candidate.monogram_chi_square:>9.3f} "
            f"order={candidate.order_name:<18} "
            f"rule={candidate.rule_name:<18} "
            f"reverse={int(candidate.reverse_bits)} invert={int(candidate.inverted)}"
        )
        print(f"    {candidate.decoded}")


if __name__ == "__main__":
    main()
