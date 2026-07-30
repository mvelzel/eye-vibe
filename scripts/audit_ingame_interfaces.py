#!/usr/bin/env python3
"""Audit source-selected in-game interface orders against Eye isomorphs.

This is a bounded provenance screen, not a key search.  It extracts ordered
names from concrete Noita interfaces (materials, actions, persistent flags,
magic numbers, debug keycodes, translation keys, WAK path families, and the
loose rune font), turns each source into a deterministic 83-card ordering,
and runs the already-calibrated small deck transitions.  Every transition is
checked against a planted rank stream before Eye contexts are scored.
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, trigram_values
from eye_mystery.deck import ranks_to_labels
from eye_mystery.ninth_causal import CONTEXT_SPECS, equality_signature
from eye_mystery.wak import WakArchive
from screen_source_deck_families import decoder_families


SIZE = 83
DEFAULT_WAK = Path(
    "/Users/mvelzel/Library/Application Support/CrossOver/Bottles/Steam/"
    "drive_c/Program Files (x86)/Steam/steamapps/common/Noita/data/data.wak"
)
DEFAULT_DATA = DEFAULT_WAK.parent
DEFAULT_FONT = DEFAULT_DATA / "fonts/font_pixel_runes.xml"


def _unique(values: list[str]) -> list[str]:
    out: list[str] = []
    for value in values:
        if value and value not in out:
            out.append(value)
    return out


def source_decks(label: str, values: list[str]) -> list[tuple[str, tuple[int, ...]]]:
    """Build only deterministic orderings from the first 83 source entries."""

    values = _unique(values)
    if len(values) < SIZE:
        return []
    first = values[:SIZE]
    return [
        (f"{label}-source", tuple(range(SIZE))),
        (f"{label}-lex", tuple(sorted(range(SIZE), key=lambda i: (first[i], i)))),
        (
            f"{label}-len",
            tuple(sorted(range(SIZE), key=lambda i: (len(first[i]), first[i], i))),
        ),
        (
            f"{label}-revlex",
            tuple(sorted(range(SIZE), key=lambda i: (first[i], i), reverse=True)),
        ),
        (
            f"{label}-revlen",
            tuple(
                sorted(
                    range(SIZE),
                    key=lambda i: (len(first[i]), first[i], i),
                    reverse=True,
                )
            ),
        ),
    ]


def _read(archive: WakArchive, by_path: dict[str, object], path: str) -> str:
    entry = by_path[path]
    return archive.read(entry).decode("utf-8", errors="replace")  # type: ignore[arg-type]


def extract_decks(archive: WakArchive, data_root: Path) -> list[tuple[str, tuple[int, ...]]]:
    by_path = {entry.path: entry for entry in archive.entries}
    decks: list[tuple[str, tuple[int, ...]]] = []

    def regex(path: str, expression: str, flags: int = 0) -> list[str]:
        return [m[0] if isinstance(m, tuple) else m for m in re.findall(expression, _read(archive, by_path, path), flags)]

    decks += source_decks(
        "materials",
        regex(
            "data/materials.xml",
            r'<(?:CellData|CellDataChild)\b[^>]*?\bname="([^"]+)"',
        ),
    )
    decks += source_decks(
        "actions",
        regex("data/scripts/gun/gun_actions.lua", r'\bid\s*=\s*"([A-Za-z0-9_]+)"'),
    )
    decks += source_decks(
        "magic-numbers",
        regex("data/magic_numbers.xml", r'\b([A-Z][A-Z0-9_]+)\s*=\s*"'),
    )
    decks += source_decks(
        "keycodes",
        regex("data/scripts/debug/keycodes.lua", r"^([A-Za-z0-9_]+)\s*=\s*[0-9]+", re.MULTILINE),
    )

    lua_text = "\n".join(
        archive.read(entry).decode("utf-8", errors="replace")
        for entry in archive.entries
        if entry.path.endswith(".lua")
    )
    decks += source_decks(
        "flags",
        re.findall(
            r"(?:AddFlagPersistent|GameAddFlagRun|HasFlagPersistent|GameHasFlagRun)"
            r"\s*\(\s*[\"']([^\"']+)",
            lua_text,
        ),
    )

    translation = data_root / "translations/common.csv"
    if translation.exists():
        keys = [row[0] for row in csv.reader(translation.read_text(errors="replace").splitlines()) if row and row[0]]
        decks += source_decks("translation", keys)

    for label, predicate in (
        ("paths-books", lambda path: "book" in path.lower()),
        ("paths-music", lambda path: any(k in path.lower() for k in ("music", "kantele", "ocarina", "rune"))),
        ("paths-intro", lambda path: "intro" in path.lower()),
    ):
        decks += source_decks(label, [entry.path for entry in archive.entries if predicate(entry.path)])

    if DEFAULT_FONT.exists():
        chars = [
            (int(char_id), int(width), int(rect_x))
            for char_id, width, rect_x in re.findall(
                r'<QuadChar id="(\d+)"[^>]*?rect_w="(\d+)"[^>]*?rect_x="(\d+)"',
                DEFAULT_FONT.read_text(errors="replace"),
            )
        ][:SIZE]
        if len(chars) == SIZE:
            decks.extend(
                [
                    ("font-width", tuple(sorted(range(SIZE), key=lambda i: (chars[i][1], chars[i][0])))),
                    ("font-width-reverse", tuple(sorted(range(SIZE), key=lambda i: (chars[i][1], chars[i][0]), reverse=True))),
                    ("font-x", tuple(sorted(range(SIZE), key=lambda i: (chars[i][2], chars[i][0])))),
                ]
            )

    seen: set[tuple[int, ...]] = set()
    unique: list[tuple[str, tuple[int, ...]]] = []
    for name, deck in decks:
        if deck not in seen:
            if sorted(deck) != list(range(SIZE)):
                raise AssertionError(name)
            seen.add(deck)
            unique.append((name, deck))
    return unique


def _contexts(streams: dict[str, tuple[int, ...]]) -> tuple[int, int, int, int]:
    iso: list[bool] = []
    literal: list[bool] = []
    for _, left, left_start, right, right_start, length in CONTEXT_SPECS[6:]:
        l = streams[left][left_start : left_start + length]
        r = streams[right][right_start : right_start + length]
        iso.append(equality_signature(l) == equality_signature(r))
        literal.append(l == r)
    return sum(iso[:-1]), int(iso[-1]), sum(literal[:-1]), int(literal[-1])


def run(archive: WakArchive, data_root: Path) -> tuple[int, int, tuple[int, int, int, int], tuple[str, ...]]:
    decks = extract_decks(archive, data_root)
    bodies = {name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER}
    rows: list[tuple[int, int, int, int, str, str, str]] = []
    for deck_name, deck in decks:
        for family, decoder in decoder_families():
            if family == "identity":
                continue
            operation = "transpose" if family.startswith("transpose-") else family
            distance = int(family.split("-", 1)[1]) if family.startswith("transpose-") else 1
            probe = tuple((index * 17 + 3) % SIZE for index in range(37))
            planted = ranks_to_labels(probe, deck, operation, distance)
            if tuple(decoder(planted, deck)) != probe:
                raise AssertionError((deck_name, family))
            label_streams = {name: tuple(decoder(stream, deck)) for name, stream in bodies.items()}
            rank_streams = {name: ranks_to_labels(stream, deck, operation, distance) for name, stream in bodies.items()}
            rows.append((*_contexts(label_streams), deck_name, family, "label"))
            rows.append((*_contexts(rank_streams), deck_name, family, "rank"))
    rows.sort(key=lambda row: (-row[0], -row[1], -row[2], -row[3], row[4], row[5], row[6]))
    return len(decks), len(rows), rows[0][:4], tuple(" ".join(map(str, row)) for row in rows[:20])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", nargs="?", type=Path, default=DEFAULT_WAK)
    parser.add_argument("--data-root", type=Path, default=DEFAULT_DATA)
    args = parser.parse_args()
    archive = WakArchive.open(args.archive)
    count, rows, best, top = run(archive, args.data_root)
    print(f"decks={count} dynamic_rows={rows} best_train_heldout_literal={best}")
    for row in top:
        print(row)


if __name__ == "__main__":
    main()
