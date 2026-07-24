#!/usr/bin/env python3
"""Run the exact early-row transfer feasibility audit."""

from eye_mystery.row_record_transfer import (
    FINAL_ANCHORS,
    FINAL_HEADERS,
    FINAL_ORDERS,
    FINAL_TARGET_RANKS,
    audit_all_rows,
    slot_headers,
)
from eye_mystery.gap_anchor import ordinal_ranks


def main() -> None:
    if slot_headers(FINAL_ANCHORS, FINAL_ORDERS) != FINAL_HEADERS:
        raise AssertionError("known final anchors fail the frozen slot rule")
    if ordinal_ranks(FINAL_ANCHORS) != FINAL_TARGET_RANKS:
        raise AssertionError("known final anchors fail the frozen target ranks")

    print("known final calibration:")
    print(f"  anchors={FINAL_ANCHORS}")
    print(f"  headers={slot_headers(FINAL_ANCHORS, FINAL_ORDERS)}")
    print(f"  ranks={ordinal_ranks(FINAL_ANCHORS)}")
    print()
    for result in audit_all_rows():
        print(f"{result.name}:")
        print(f"  headers={result.headers}")
        print(f"  orders={result.orders}")
        print(f"  target_ranks={result.target_ranks}")
        print(f"  feasible={result.feasible_count}")
        print(f"  distinct_feasible={result.distinct_feasible_count}")
        print(f"  attainable_ranks={result.attainable_rank_patterns}")
        print(f"  target_rank_count={result.target_rank_count}")
        print(f"  example={result.example}")
        print(
            "  complete_grammar_feasible="
            f"{result.complete_grammar_feasible}"
        )
        print()


if __name__ == "__main__":
    main()
