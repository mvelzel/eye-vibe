#!/usr/bin/env python3
"""Run the frozen checksum-quotient self-pointer audit."""

from eye_mystery.checksum_self_pointer import (
    CONSTRUCTION_LEDGER,
    TYPED_TARGETS,
    run_audit,
)


def main() -> None:
    audit = run_audit()
    print("checksum quotient profiles")
    for item in audit.profiles:
        ledger_hits = tuple(
            distance
            for distance in item.distances
            if distance in CONSTRUCTION_LEDGER
        )
        print(
            f"  {item.name}: sum={item.total} quotient={item.quotient} "
            f"positions={item.positions} distances={item.distances} "
            f"ledger-hits={ledger_hits}"
        )
    print(f"typed targets: {TYPED_TARGETS}")
    exact = audit.exact_typed_probability
    print(
        f"exact typed conditional probability: "
        f"{exact.numerator}/{exact.denominator}={float(exact):.12f}"
    )
    print(
        f"permutation conditional probability: "
        f"{audit.permutation_numerator}/{audit.permutation_denominator}="
        f"{float(audit.permutation_probability):.12f}"
    )
    for label, observed, probability in (
        (
            "typed coordinate",
            audit.typed_coordinate_observed,
            audit.typed_coordinate_probability,
        ),
        (
            "any-hit assignment",
            audit.any_hit_assignment_observed,
            audit.any_hit_assignment_probability,
        ),
        (
            "all-hit assignment",
            audit.all_hit_assignment_observed,
            audit.all_hit_assignment_probability,
        ),
    ):
        print(
            f"{label}: observed={observed} null-event-rate="
            f"{probability.numerator}/{probability.denominator}="
            f"{float(probability):.12f}"
        )
    print(f"circular packets: {audit.circular_packets}")
    for label, probability in (
        ("all-six ledger containment", audit.ledger_containment_probability),
        ("typed packet sums", audit.packet_sum_probability),
        ("packet-sum permutation", audit.packet_sum_permutation_probability),
    ):
        print(
            f"{label} conditional probability: "
            f"{probability.numerator}/{probability.denominator}="
            f"{float(probability):.12f}"
        )
    print("six-panel holdout")
    for item, packet in zip(
        audit.holdout_profiles,
        audit.holdout_packets,
        strict=True,
    ):
        print(
            f"  {item.name}: sum={item.total} q={item.quotient} "
            f"r={item.remainder} positions={item.positions} packet={packet}"
        )
    holdout_probability = audit.holdout_ledger_probability
    print(
        f"  viable={audit.holdout_viable} "
        f"in-ledger={audit.holdout_in_ledger} "
        f"conditional-ledger-rate="
        f"{holdout_probability.numerator}/{holdout_probability.denominator}="
        f"{float(holdout_probability):.12f}"
    )
    residual_probability = audit.header_residual_assignment_probability
    print(
        "header residuals: observed=(30,18,3) "
        f"assignment-rate={residual_probability.numerator}/"
        f"{residual_probability.denominator}="
        f"{float(residual_probability):.12f}"
    )


if __name__ == "__main__":
    main()
