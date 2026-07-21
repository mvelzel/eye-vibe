#!/usr/bin/env python3
"""Test the strongest Eye isomorph contexts against both affine GAK groups."""

from __future__ import annotations

import argparse

from eye_mystery.affine_embedding import (
    context_from_sequences,
    find_affine_embedding_graph,
)
from eye_mystery.corpus import MESSAGES, trigram_values


def segment(name: str, start: int, length: int) -> tuple[int, ...]:
    return trigram_values(MESSAGES[name])[start : start + length]


def first_three_contexts():
    # The first three are the 18-character A.....BCD.ED.BE.CA family.  Their
    # inner nine characters also account for three instances of A.B.CB.AC.
    anchor = segment("west1", 34, 18)
    contexts = [
        context_from_sequences("gap30", anchor, segment("west1", 64, 18)),
        context_from_sequences("west1-east2", anchor, segment("east2", 39, 18)),
        context_from_sequences("west1-east2-late", anchor, segment("east2", 74, 18)),
        # The remaining non-identical same-text instance in the sixfold
        # A.B.CB.AC family.
        context_from_sequences(
            "east1-gap28", segment("east1", 40, 9), segment("east1", 68, 9)
        ),
    ]
    return tuple(contexts)


def last_family_contexts():
    # The 30-character AB...C...C......D.A...E...EB.D family in East 4,
    # West 4, and East 5 contains three of the four instances of the nested
    # 25-character A...A......B.....C...C..B family.  East 3 supplies its
    # fourth instance.
    anchor = segment("east4", 68, 30)
    return (
        context_from_sequences("east4-west4", anchor, segment("west4", 71, 30)),
        context_from_sequences("east4-east5", anchor, segment("east5", 69, 30)),
        context_from_sequences(
            "east4-east3", segment("east4", 73, 25), segment("east3", 64, 25)
        ),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout-ms", type=int, default=300_000)
    parser.add_argument(
        "--families", choices=("first", "last", "combined"), default="combined"
    )
    args = parser.parse_args()
    if args.families == "first":
        contexts = first_three_contexts()
    elif args.families == "last":
        contexts = last_family_contexts()
    else:
        contexts = first_three_contexts() + last_family_contexts()
    print(
        f"families={args.families} contexts={len(contexts)} "
        f"mappings={sum(len(c.pairs) for c in contexts)}"
    )
    for hidden_order in (41, 82):
        outcome, embedding, reason = find_affine_embedding_graph(
            contexts, hidden_order=hidden_order, timeout_ms=args.timeout_ms
        )
        print(f"C83:C{hidden_order}: {outcome}")
        if reason:
            print("  reason:", reason)
        if embedding:
            for name, parameters in embedding.transformations.items():
                print(f"  {name}: a={parameters[0]} b={parameters[1]}")


if __name__ == "__main__":
    main()
