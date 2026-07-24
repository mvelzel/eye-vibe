#!/usr/bin/env python3
"""Inventory executable 9/42/83/101 arithmetic signatures in a Noita WAK."""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from eye_mystery.lua_arithmetic_signatures import (
    TARGET_CARDINALITIES,
    scan_wak_arithmetic_signatures,
)
from eye_mystery.wak import WakArchive


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    args = parser.parse_args()

    hits = scan_wak_arithmetic_signatures(WakArchive.open(args.archive))
    counts = Counter((hit.cardinality, hit.kind) for hit in hits)
    for cardinality in sorted(TARGET_CARDINALITIES):
        fields = [
            f"{kind}={counts[cardinality, kind]}"
            for kind in (
                "modulo",
                "random_domain",
                "random_partition",
                "numeric_for",
            )
        ]
        print(cardinality, " ".join(fields))
    print("lookup-flow hits", sum(hit.feeds_lookup for hit in hits))
    for hit in hits:
        if (
            hit.cardinality in (42, 83)
            or hit.kind != "random_domain"
            or hit.feeds_lookup
        ):
            print(
                f"{hit.cardinality:>3} {hit.kind:<16} "
                f"lookup={str(hit.feeds_lookup).lower():<5} "
                f"{hit.path}:{hit.line} {hit.detail} :: {hit.source}"
            )


if __name__ == "__main__":
    main()
