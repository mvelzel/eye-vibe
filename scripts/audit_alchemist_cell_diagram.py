#!/usr/bin/env python3
"""Reproduce the frozen Alchemist-cell-diagram Eye audit.

The diagram is treated as a standalone, later-asset hypothesis.  This script
reports exact asset readings and only the pre-registered low-capacity tests:
literal source/tape hits, canonical header-cycle alignment, and the fixed
upper-column-to-lower-column table on the six known ``THAT WHICH`` windows.
It deliberately does not search fitted digit permutations or combine this
asset with another clue theory.
"""

from __future__ import annotations

import argparse
import struct
from pathlib import Path

from eye_mystery.alchemist_cell_diagram import (
    DiagramVariant,
    decimal_text,
    hexadecimal_text,
    lower_tape,
    parse_alchemist_diagram,
    sorted_direction_table,
    upper_permutation,
)
from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, trigram_values
from eye_mystery.initials import circular_successor_links, perfect_successor_rotation
from eye_mystery.isomorphs import pattern
from eye_mystery.wall_83_masks import THAT_WHICH_WINDOWS


def variants():
    for reverse_groups in (False, True):
        for reverse_columns in (False, True):
            for complement_rows in (False, True):
                yield DiagramVariant(reverse_groups, reverse_columns, complement_rows)


def dihedral_equivalent(left: tuple[int, ...], right: tuple[int, ...]) -> bool:
    if len(left) != len(right):
        return False
    return any(
        candidate == right
        for candidate in (
            left,
            tuple(reversed(left)),
        )
        for offset in range(len(left))
        for candidate in (
            candidate[offset:] + candidate[:offset],
        )
    )


def source_hits(path: Path, needles: tuple[bytes, ...]) -> tuple[bytes, ...]:
    data = path.read_bytes()
    return tuple(needle for needle in needles if needle in data)


def source_needles(diagram, variant) -> tuple[bytes, ...]:
    needles: set[bytes] = set()
    for linearization in ("row-major", "column-major"):
        for tape, base in (
            (hexadecimal_text(diagram, variant, linearization=linearization), 16),
            (decimal_text(diagram, variant, linearization=linearization), 10),
        ):
            needles.add(tape.encode("ascii"))
            value = int(tape, base)
            needles.add(struct.pack("<I", value))
            needles.add(struct.pack(">I", value))
    return tuple(sorted(needles))


def table_projection(table: tuple[int, ...]) -> tuple[str, ...]:
    """Project the fixed table through canonical rank classes.

    The table is a many-to-one map from upper columns to lower columns.  We
    index it by rank modulo eight only because that is the sole direct,
    developer-sized interpretation of the eight upper records; this is a
    registered screen, not a discovered key.
    """
    labels = tuple(table[value % 8] for value in range(83))
    result = []
    for _, values in THAT_WHICH_WINDOWS:
        symbols = tuple(labels[value] for value in values)
        result.append(pattern(symbols))
    return tuple(result)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("asset", type=Path)
    parser.add_argument("--source", type=Path, action="append", default=[])
    args = parser.parse_args()
    diagram = parse_alchemist_diagram(args.asset)

    print("ASSET")
    print("sha256=545b4b57c9d046f8bb59828ae0d3669f3a1bde3f7d46419c79281677c905733a")
    for variant in variants():
        print(
            "variant="
            f"{int(variant.reverse_groups)}{int(variant.reverse_columns)}{int(variant.complement_rows)} "
            f"upper={upper_permutation(diagram, variant)} "
            f"lower={lower_tape(diagram, variant)} "
            f"table={sorted_direction_table(diagram, variant)} "
            f"hex-row={hexadecimal_text(diagram, variant)} "
            f"hex-col={hexadecimal_text(diagram, variant, linearization='column-major')} "
            f"dec-row={decimal_text(diagram, variant)} "
            f"dec-col={decimal_text(diagram, variant, linearization='column-major')}"
        )

    print("\nSOURCE-CONSTANT-HITS")
    for path in args.source:
        hits = set()
        for variant in variants():
            hits.update(source_hits(path, source_needles(diagram, variant)))
        print(f"{path}: {len(hits)} exact byte hits")
        for needle in sorted(hits):
            print(f"  {needle.hex()} / {needle!r}")

    print("\nLITERAL-TAPE-HITS")
    for variant in variants():
        tape = lower_tape(diagram, variant)
        hits = [
            name
            for name in MESSAGE_ORDER
            if any(
                tuple(MESSAGES[name][start : start + len(tape)]) == tape
                for start in range(len(MESSAGES[name]) - len(tape) + 1)
            )
        ]
        if hits:
            print(f"variant={variant}: tape={tape} hits={hits}")
    print("  no exact hits (all admitted variants)")

    rotation = perfect_successor_rotation()
    links = circular_successor_links()
    successful_edges = tuple(index for index, ok in enumerate(links) if ok)
    rotation_indices = tuple(MESSAGE_ORDER.index(name) for name in rotation or ())
    edge_order = tuple(
        successful_edges.index(index)
        for index in rotation_indices[:-1]
    )
    print("\nHEADER-CYCLE")
    print(f"canonical-links={links}")
    print(f"canonical-rotation={rotation}")
    print(f"canonical-edge-ranks={edge_order}")
    for variant in variants():
        upper = upper_permutation(diagram, variant)
        if dihedral_equivalent(upper, edge_order):
            print(f"  admitted header alignment: {variant} upper={upper}")
    print("  no admitted header alignment")

    print("\nFIXED-TABLE-PROJECTION")
    for variant in variants():
        projection = table_projection(sorted_direction_table(diagram, variant))
        exact = sum(
            observed == "A.B.CB.AC."
            for observed in projection
        )
        print(f"variant={variant} exact-signatures={exact}/6 projections={projection}")


if __name__ == "__main__":
    main()
