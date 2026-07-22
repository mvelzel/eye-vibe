#!/usr/bin/env python3
"""Run structural tests and provenance gates from the eighth wide batch."""

from __future__ import annotations

import argparse
from pathlib import Path
from random import Random
import re

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.eighth_wide import (
    codebook_score,
    cocycle_score,
    packet_score,
    repair_score,
)
from eye_mystery.language_null import prefix_tree_parity_shuffle


RNG_CALL = re.compile(r"\b(?:math\.random|Random|ProceduralRandom[fi]?)\s*\(")
RNG_DEFINITION = re.compile(
    r"\bfunction\s+(?:math\.)?(?:random|Random|ProceduralRandom[fi]?)\s*\("
)


def attach_headers(
    streams: dict[str, tuple[int, ...]], bodies: dict[str, tuple[int, ...]]
) -> dict[str, tuple[int, ...]]:
    return {name: (streams[name][0], *bodies[name]) for name in MESSAGE_ORDER}


def rng_inventory(root: Path) -> tuple[int, int, int]:
    """Count Lua files, engine RNG calls, and in-data RNG definitions."""

    files = calls = definitions = 0
    for path in root.rglob("*.lua"):
        files += 1
        text = path.read_text(errors="ignore")
        calls += len(RNG_CALL.findall(text))
        definitions += len(RNG_DEFINITION.findall(text))
    return files, calls, definitions


def corrected(hits: int, controls: int) -> str:
    return f"{hits + 1}/{controls + 1} = {(hits + 1)/(controls + 1):.6f}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--controls", type=int, default=2_000)
    parser.add_argument("--seed", type=int, default=20260722)
    parser.add_argument("--data-root", type=Path)
    parser.add_argument("--early-data-root", type=Path)
    args = parser.parse_args()

    streams = {name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER}
    bodies = {name: stream[1:] for name, stream in streams.items()}
    observed_g = codebook_score()
    observed_h = packet_score(streams)
    observed_i = cocycle_score(streams)
    observed_j = repair_score(streams)

    generator = Random(args.seed)
    packet_hits = grammar_hits = 0
    packet_ranges = [[], []]
    grammar_range = []
    for _ in range(args.controls):
        shuffled_bodies = prefix_tree_parity_shuffle(
            bodies, bodies, generator, start=0
        )
        shuffled = attach_headers(streams, shuffled_bodies)
        packet = packet_score(shuffled)
        grammar = repair_score(shuffled)
        packet_hits += (
            packet.unique_26 >= observed_h.unique_26
            and packet.unique_83 >= observed_h.unique_83
        )
        grammar_hits += grammar.savings >= observed_j.savings
        packet_ranges[0].append(packet.unique_26)
        packet_ranges[1].append(packet.unique_83)
        grammar_range.append(grammar.savings)

    print("G synchronizing/error codebook:", observed_g)
    print("  exact decision: reject literal correcting/comma-free code")
    print("H without-replacement packets:", observed_h)
    print("  joint corrected upper tail:", corrected(packet_hits, args.controls))
    print(
        "  control ranges unique26/unique83:",
        (min(packet_ranges[0]), max(packet_ranges[0])),
        (min(packet_ranges[1]), max(packet_ranges[1])),
    )
    print("I repeated-bigram Z101 cocycle:", observed_i)
    print("  exact decision:", "pass" if not observed_i.contradictions else "reject")
    print("J deterministic RePair grammar:", observed_j)
    print("  corrected upper tail:", corrected(grammar_hits, args.controls))
    print("  control savings range:", (min(grammar_range), max(grammar_range)))

    print("K eligible RNG provenance gate:")
    for label, root in (
        ("current", args.data_root),
        ("early", args.early_data_root),
    ):
        if root:
            print(" ", label, root, rng_inventory(root))
        else:
            print(" ", label, "not supplied")
    print("  engine RNG call sites do not supply an in-data implementation")
    print("L authored range-model gate:")
    print("  prior exact table inventory: no 42/101 table; only duplicated gun_names at 83")


if __name__ == "__main__":
    main()
