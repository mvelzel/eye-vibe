#!/usr/bin/env python3
"""Screen every contiguous 83-glyph window of Noita's runic font.

The window and sort key are selected from the shipped font before Eye output
is scored.  This deliberately finite screen asks whether a runic-atlas subset
can supply one of the small reversible deck machines already calibrated in the
repository; it is not a plaintext search.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from audit_ingame_interfaces import DEFAULT_FONT, DEFAULT_WAK, _contexts
from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, trigram_values
from eye_mystery.deck import ranks_to_labels
from eye_mystery.wak import WakArchive
from screen_source_deck_families import decoder_families

SIZE = 83


def glyphs(font: Path) -> list[dict[str, int]]:
    output: list[dict[str, int]] = []
    for block in re.findall(r"<QuadChar\b[^>]*>", font.read_text(errors="replace")):
        attrs = dict(re.findall(r'(\w+)="([^"]+)"', block))
        required = ("id", "rect_w", "rect_x", "offset_x", "offset_y", "rect_h")
        if all(key in attrs for key in required):
            output.append({key: int(attrs[key]) for key in required})
    return output


def run(font: Path) -> tuple[int, int, tuple[int, int, int, int], list[str]]:
    entries = glyphs(font)
    if len(entries) < SIZE:
        raise ValueError(f"font has only {len(entries)} glyphs")
    bodies = {name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER}
    rows: list[tuple[int, int, int, int, int, str, bool, str, str]] = []
    seen: set[tuple[int, ...]] = set()
    metrics = ("id", "rect_w", "rect_x", "offset_x", "offset_y", "rect_h")
    for start in range(len(entries) - SIZE + 1):
        window = entries[start : start + SIZE]
        for metric in metrics:
            for reverse in (False, True):
                deck = tuple(
                    sorted(
                        range(SIZE),
                        key=lambda index: (window[index][metric], index),
                        reverse=reverse,
                    )
                )
                if deck in seen:
                    continue
                seen.add(deck)
                for family, decoder in decoder_families():
                    if family == "identity":
                        continue
                    operation = "transpose" if family.startswith("transpose-") else family
                    distance = int(family.split("-", 1)[1]) if operation == "transpose" else 1
                    labels = {name: tuple(decoder(stream, deck)) for name, stream in bodies.items()}
                    rows.append((*_contexts(labels), start, metric, reverse, family, "label"))
                    rank_labels = {
                        name: ranks_to_labels(stream, deck, operation, distance)
                        for name, stream in bodies.items()
                    }
                    rows.append((*_contexts(rank_labels), start, metric, reverse, family, "rank"))
    rows.sort(key=lambda row: (-row[0], -row[1], -row[2], -row[3], row[4:]))
    best = rows[0][:4]
    top = [" ".join(map(str, row)) for row in rows[:20]]
    return len(seen), len(rows), best, top


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--font", type=Path, default=DEFAULT_FONT)
    parser.add_argument("--wak", type=Path, default=DEFAULT_WAK)
    args = parser.parse_args()
    # Opening the archive here guards that the reported font belongs to the
    # installed release being audited; the screen itself only needs the font.
    WakArchive.open(args.wak)
    decks, rows, best, top = run(args.font)
    print(f"font_glyphs={len(glyphs(args.font))} unique_decks={decks} dynamic_rows={rows}")
    print(f"best_train_heldout_literal={best}")
    print("\n".join(top))


if __name__ == "__main__":
    main()
