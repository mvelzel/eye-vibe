#!/usr/bin/env python3
"""Audit bijective header-ordered reranking of the visible 83-word codebook."""

from eye_mystery.header_order_ideal import (
    ROUTES,
    audit_visible_rerank,
    score_visible_route,
)


def main() -> None:
    print("real visible-rerank route scores:")
    for route in ROUTES:
        score = score_visible_route(route)
        print(
            f"  {route}: train={score.training_agreements}/"
            f"{score.training_length} holdout={score.holdout_agreements}/"
            f"{score.holdout_length}"
        )
        for context in (*score.training, *score.holdout):
            print(
                f"    {context.name}: "
                f"{context.agreements}/{context.length}"
            )

    audit = audit_visible_rerank()
    observed = audit.observed
    print(
        f"selected={observed.route} "
        f"train={observed.training_agreements}/{observed.training_length} "
        f"holdout={observed.holdout_agreements}/{observed.holdout_length}"
    )
    print(
        f"holdout_tail={audit.holdout_tail_count}/{audit.control_count}="
        f"{audit.holdout_tail:.9f} "
        f"control_max={audit.maximum_control_holdout}"
    )
    print("holdout histogram:")
    for score, count in audit.holdout_histogram:
        print(f"  {score}: {count}")


if __name__ == "__main__":
    main()
