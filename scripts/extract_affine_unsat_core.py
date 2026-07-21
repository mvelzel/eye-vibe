#!/usr/bin/env python3
"""Extract irreducible edge cores from the last-family affine contradiction."""

from __future__ import annotations

import argparse

from eye_mystery.affine_embedding import find_affine_mapping_unsat_core
from test_affine_isomorph_embedding import last_family_contexts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--hidden-order", type=int, choices=(41, 82), default=41)
    parser.add_argument("--timeout-ms", type=int, default=300_000)
    parser.add_argument(
        "--all-three",
        action="store_true",
        help="include the conditional nested East 4 to East 3 context",
    )
    parser.add_argument(
        "--raw-core",
        action="store_true",
        help="report Z3's first core without deletion minimization",
    )
    args = parser.parse_args()
    contexts = last_family_contexts()
    if not args.all_three:
        contexts = contexts[:2]
    outcome, core, reason = find_affine_mapping_unsat_core(
        contexts,
        hidden_order=args.hidden_order,
        timeout_ms=args.timeout_ms,
        minimize=not args.raw_core,
    )
    print(f"C83:C{args.hidden_order}: {outcome}; core edges={len(core)}")
    if reason:
        print("reason:", reason)
    for mapping in core:
        print(f"{mapping.context}: {mapping.left} -> {mapping.right}")


if __name__ == "__main__":
    main()
