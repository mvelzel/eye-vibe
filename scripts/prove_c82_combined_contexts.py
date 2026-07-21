#!/usr/bin/env python3
"""Exclude C83:C82 using two strong, independent isomorph families."""

from __future__ import annotations

from collections import Counter

from eye_mystery.affine_linear import (
    analyze_fixed_multipliers,
    enumerate_multiplier_cases,
)
from test_affine_isomorph_embedding import (
    first_three_contexts,
    last_family_contexts,
)


def main() -> None:
    last_contexts = last_family_contexts()[:2]
    first_context = first_three_contexts()[0]
    last_cases = tuple(
        enumerate_multiplier_cases(last_contexts, hidden_order=82)
    )
    last_counts = Counter(case.status for case in last_cases)
    open_pairs = tuple(
        case.multipliers for case in last_cases if case.status == "open"
    )
    print("stage 1 contexts:", ", ".join(c.name for c in last_contexts))
    print("multiplier pairs:", len(last_cases))
    for status in ("inconsistent", "forced_collision", "open"):
        print(f"{status}: {last_counts[status]}")
    print("open multiplier pairs:", open_pairs)

    extension_counts: Counter[str] = Counter()
    for pair in open_pairs:
        for multiplier in range(1, 83):
            case = analyze_fixed_multipliers(
                last_contexts + (first_context,), pair + (multiplier,)
            )
            extension_counts[case.status] += 1
    print("stage 2 context:", first_context.name)
    print("multiplier extensions:", len(open_pairs) * 82)
    for status in ("inconsistent", "forced_collision", "open"):
        print(f"{status}: {extension_counts[status]}")
    if extension_counts["open"]:
        raise SystemExit("certificate failed: a multiplier extension remains open")


if __name__ == "__main__":
    main()
