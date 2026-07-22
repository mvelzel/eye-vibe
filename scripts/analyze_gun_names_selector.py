#!/usr/bin/env python3
"""Test Noita's exact 83-entry wand-name table as an Eye lookup selector."""

from __future__ import annotations

import argparse
import hashlib
import random
from pathlib import Path

from eye_mystery.asset_tables import assigned_string_list
from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, trigram_values
from eye_mystery.gun_names_selector import (
    FEATURES,
    alphabetical_deck,
    best_natural_score,
    feature_map,
    map_messages,
    permutation_control,
    score_messages,
)
from eye_mystery.ngram import TetragramModel
from eye_mystery.practice_cipher5 import (
    decode_dynamic_substitution,
    recursive_increasing_chunk_reversal,
)
from eye_mystery.wak import WakArchive


PATHS = (
    "data/scripts/gun/procedural/gun_procedural.lua",
    "data/scripts/gun/procedural/gun_procedural_better.lua",
    "data/scripts/gun/procedural/gun_utilities.lua",
    "data/scripts/gun/procedural/wand_petri.lua",
)


def letters(values: tuple[int, ...]) -> str:
    return "".join(chr(ord("A") + value) for value in values)


def dynamic_reading(
    names: tuple[str, ...],
    messages: dict[str, tuple[int, ...]],
    *,
    reverse: bool,
    omit_marker: bool,
    operations: tuple[tuple[int, ...], ...],
) -> tuple[int, ...]:
    deck = alphabetical_deck(names, reverse=reverse)
    start = 1 if omit_marker else 0
    return tuple(
        value
        for message in messages.values()
        for value in decode_dynamic_substitution(
            message[start:], operations, initial_deck=deck
        )
    )


def best_dynamic_range_fit(
    names: tuple[str, ...],
    messages: dict[str, tuple[int, ...]],
    operations: tuple[tuple[int, ...], ...],
) -> tuple[int, bool, bool, tuple[int, ...]]:
    best = (-1, False, False, ())
    for reverse in (False, True):
        for omit_marker in (False, True):
            decoded = dynamic_reading(
                names,
                messages,
                reverse=reverse,
                omit_marker=omit_marker,
                operations=operations,
            )
            candidate = (sum(value < 42 for value in decoded), reverse, omit_marker, decoded)
            if candidate[0] > best[0]:
                best = candidate
    return best


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    parser.add_argument("corpus", type=Path)
    parser.add_argument("--controls", type=int, default=10_000)
    parser.add_argument("--seed", type=int, default=0x83A101)
    parser.add_argument(
        "--historical-lua",
        action="append",
        default=[],
        type=Path,
        help="compare an unpacked historical Lua copy of gun_names",
    )
    args = parser.parse_args()

    archive = WakArchive.open(args.archive)
    by_path = {entry.path: entry for entry in archive.entries}
    tables = []
    for path in PATHS:
        text = archive.read(by_path[path]).decode("utf-8")
        tables.append(assigned_string_list(text, "gun_names"))
    if any(table != tables[0] for table in tables[1:]):
        raise RuntimeError("the four installed gun_names copies differ")
    names = tables[0]
    digest = hashlib.sha256("\0".join(names).encode()).hexdigest()

    messages = {
        name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
    }
    model = TetragramModel.train(args.corpus.read_text(errors="ignore"))
    observed, feature_name, omit_marker = best_natural_score(names, messages, model)
    _, windows = score_messages(
        model,
        map_messages(
            messages,
            feature_map(names, dict(FEATURES)[feature_name]),
            omit_marker=omit_marker,
        ),
    )
    _, at_least, controls = permutation_control(
        names,
        messages,
        model,
        controls=args.controls,
        seed=args.seed,
    )

    print(f"installed copies: {len(PATHS)} identical")
    for path in PATHS:
        print(f"  {path}")
    print(f"entry count: {len(names)}")
    print(f"NUL-joined SHA-256: {digest}")
    for historical_path in args.historical_lua:
        historical = assigned_string_list(
            historical_path.read_text(errors="ignore"), "gun_names"
        )
        historical_digest = hashlib.sha256(
            "\0".join(historical).encode()
        ).hexdigest()
        print(
            f"historical copy: {historical_path} :: count={len(historical)} "
            f"digest={historical_digest} identical={historical == names}"
        )
    print("index endpoints: 0=Deadly 40=Special 41=Unique 42=Mega 82=Online")
    print(
        f"selected natural reading: {feature_name}; "
        f"marker={'omitted' if omit_marker else 'included'}"
    )
    print(f"selected score/window: {observed / windows:.6f}")
    print(
        f"table-permutation corrected upper tail: "
        f"{at_least + 1}/{controls + 1} = {(at_least + 1)/(controls + 1):.6f}"
    )
    print("selected/core previews (first 48 letters of each message):")
    preview_names = {"first-letter", "last-letter", "A1Z26-length", feature_name}
    for current_feature_name, feature in FEATURES:
        if current_feature_name not in preview_names:
            continue
        mapping = feature_map(names, feature)
        print(f"  {current_feature_name}")
        for name in MESSAGE_ORDER:
            rendered = letters(tuple(mapping[value] for value in messages[name]))
            print(f"    {name:<5} {rendered[:48]}")

    operations = tuple(
        recursive_increasing_chunk_reversal(83, index) for index in range(83)
    )
    valid, reverse, dynamic_omit_marker, decoded = best_dynamic_range_fit(
        names, messages, operations
    )
    generator = random.Random(args.seed ^ 0x5)
    dynamic_controls = min(args.controls, 2_000)
    dynamic_at_least = 0
    shuffled = list(names)
    for _ in range(dynamic_controls):
        generator.shuffle(shuffled)
        control_valid, _, _, _ = best_dynamic_range_fit(
            tuple(shuffled), messages, operations
        )
        dynamic_at_least += control_valid >= valid
    print("practice-cipher-5 dynamic-shuffle transfer:")
    print(
        f"  selected deck={'reverse alphabetical' if reverse else 'alphabetical'}; "
        f"marker={'omitted' if dynamic_omit_marker else 'included'}"
    )
    print(f"  values in proposed 42-symbol plaintext range: {valid}/{len(decoded)}")
    print(
        f"  corrected table-permutation upper tail: "
        f"{dynamic_at_least + 1}/{dynamic_controls + 1} = "
        f"{(dynamic_at_least + 1)/(dynamic_controls + 1):.6f}"
    )


if __name__ == "__main__":
    main()
