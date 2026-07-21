#!/usr/bin/env python3
"""Give a dependency-free exhaustive certificate against C83:C41."""

from __future__ import annotations

from collections import Counter

from eye_mystery.affine_linear import enumerate_multiplier_cases
from test_affine_isomorph_embedding import last_family_contexts


def main() -> None:
    contexts = last_family_contexts()[:2]
    cases = tuple(enumerate_multiplier_cases(contexts, hidden_order=41))
    counts = Counter(case.status for case in cases)
    print("contexts:", ", ".join(context.name for context in contexts))
    print("multiplier pairs:", len(cases))
    for status in ("inconsistent", "forced_collision", "open"):
        print(f"{status}: {counts[status]}")
    print("non-inconsistent cases (a, c; first forced collision):")
    for case in cases:
        if case.status != "inconsistent":
            print(case.multipliers, case.collisions[0] if case.collisions else "OPEN")
    if counts["open"]:
        raise SystemExit("certificate failed: at least one multiplier pair remains open")


if __name__ == "__main__":
    main()
