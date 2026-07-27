#!/usr/bin/env python3
"""Reproduce the bounded Wall/header context-selection audit."""

from __future__ import annotations

import argparse
from pathlib import Path

from eye_mystery.wall_header_clue import (
    direct_context_table_audit,
    fixed_ordered_word_probability,
    natural_context_reads,
    odd_east_checksums,
    wall_header_counts,
)
from eye_mystery.noita_wall_messages import load_wall_message_lines


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("surface_text", type=Path)
    args = parser.parse_args()

    lines_by_id = dict(load_wall_message_lines(args.surface_text))
    counts = wall_header_counts(lines_by_id)
    checksums = odd_east_checksums()

    print("COUNT/HEADER CORRESPONDENCE")
    print(
        f"wall={counts.header_tuple} "
        f"(periods, literal-you+omissions, questions)"
    )
    print(
        f"literal-you={counts.literal_you} "
        f"omitted-you={counts.omitted_you} "
        f"expanded-you={counts.expanded_you}"
    )
    print(f"eye={tuple(record.header for record in checksums)}")
    for record in checksums:
        print(
            f"  {record.message}: header={record.header} "
            f"sum={record.total} "
            f"divmod101=({record.quotient},{record.remainder})"
        )

    print("\nCONTEXT SENSITIVITY FAMILY")
    for read in natural_context_reads(lines_by_id):
        print(
            f"{read.order_name:<18} {read.indexing:<10} "
            f"{read.direction:<9} {read.phrase}"
        )

    target = ("and", "created", "god")
    probability = fixed_ordered_word_probability(lines_by_id, target)
    print("\nDESCRIPTIVE FIXED-TARGET MULTISET CALCULATION")
    print(
        f"target={' '.join(word.upper() for word in target)} "
        f"probability={probability} ({float(probability):.10f})"
    )
    print("warning=post-hoc target; this is not a discovery p-value")

    print("\nDIRECT 83-ENTRY TABLE CONSUMER")
    for field in ("previous", "following", "token"):
        audit = direct_context_table_audit(lines_by_id, field=field)
        print(
            f"{field}: unique={audit.unique_outputs}/83 "
            f"canonical-pattern={audit.expected_pattern} "
            f"preserved={audit.preserved_windows}/6 "
            f"common-after-map={audit.common_pattern}"
        )
        print(f"  mapped-patterns={audit.window_patterns}")
        if field == "previous":
            for message, words in audit.message_prefixes:
                print(f"  {message}: {' '.join(words)}")


if __name__ == "__main__":
    main()
