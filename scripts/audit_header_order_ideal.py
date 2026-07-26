#!/usr/bin/env python3
"""Audit the factoradic-header order-ideal omission channel."""

from eye_mystery.header_order_ideal import (
    MESSAGE_ORDER,
    ROUTES,
    audit_header_order_ideal,
    header_eye_order,
    score_route,
)


def main() -> None:
    print("header-induced eye orders:")
    for name in MESSAGE_ORDER:
        orders = " ".join(
            f"{route}={header_eye_order(name, route)}"
            for route in ROUTES
        )
        print(f"  {name}: {orders}")

    print("real route scores:")
    for route in ROUTES:
        score = score_route(route)
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

    audit = audit_header_order_ideal()
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
    print(
        f"support={audit.observed_support} uses42={audit.observed_uses_42} "
        f"support_lower_tail={audit.support_lower_tail_count}/"
        f"{audit.control_count}={audit.support_lower_tail:.9f}"
    )
    print("holdout histogram:")
    for score, count in audit.holdout_histogram:
        print(f"  {score}: {count}")


if __name__ == "__main__":
    main()
