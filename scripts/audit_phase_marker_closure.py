#!/usr/bin/env python3
"""Reproduce the frozen phase-marker closure audit."""

from __future__ import annotations

from eye_mystery.phase_marker_closure import (
    audit_conditional,
    closure_observation,
    pair_marker_matches,
    phase_closure_metrics,
    phase_topology_observation,
    scan_observed_repairs,
)


def ratio(numerator: int, denominator: int) -> str:
    return f"{numerator}/{denominator} = {numerator / denominator:.9f}"


def main() -> None:
    metrics = phase_closure_metrics()
    observed = closure_observation()
    audit = audit_conditional()
    print(f"phase_metrics: {metrics}")
    print(f"observed: {observed}")
    print(f"topology: {phase_topology_observation()}")
    print(f"pair_marker_matches: {pair_marker_matches()}")
    print(f"nonself: {ratio(audit.nonself, audit.assignments)}")
    print(f"self_to_phase: {ratio(audit.self_to_phase, audit.assignments)}")
    print(f"full: {ratio(audit.full, audit.assignments)}")
    print(
        "full_and_source_delta: "
        f"{ratio(audit.full_and_source_delta, audit.assignments)}"
    )
    print(
        "full_topology: "
        f"{ratio(audit.full_topology, audit.assignments)}"
    )
    print(
        "self_to_phase_given_nonself: "
        f"{ratio(audit.self_to_phase, audit.nonself)}"
    )
    print(
        "full_given_self_to_phase: "
        f"{ratio(audit.full, audit.self_to_phase)}"
    )
    print(
        "full_given_nonself: "
        f"{ratio(audit.full, audit.nonself)}"
    )
    print(
        "broad_natural: "
        f"{ratio(audit.broad_natural, audit.assignments)}"
    )
    print(
        "broad_permuted: "
        f"{ratio(audit.broad_permuted, audit.assignments)}"
    )
    print(
        "factoradic_survivors: "
        f"{audit.factoradic_survivors}; matching="
        f"{audit.matching_factoradic_survivors}"
    )
    print(
        "all_shift_natural_hits: "
        f"{scan_observed_repairs(permute_target=False)}"
    )
    print(
        "all_shift_permuted_hits: "
        f"{scan_observed_repairs(permute_target=True)}"
    )


if __name__ == "__main__":
    main()
