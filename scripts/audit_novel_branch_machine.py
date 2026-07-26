#!/usr/bin/env python3
"""Run the frozen axis-typed branch-machine screens."""

from eye_mystery.novel_branch_machine import (
    access_discipline_audit,
    axis_marker_audit,
    branch_assignment_baseline,
    branch_checksum_observation,
    carry_rewrite_observation,
    header_scalar_branch_observation,
    systematic_code_audit,
    third_axis_roles,
    transition_cover_audit,
)


def main() -> None:
    roles = third_axis_roles()
    print("third-axis roles")
    print(roles)

    checks = branch_checksum_observation()
    print("branch checks")
    print(
        f"controls source={checks.source_direction} "
        f"target={checks.target_direction}"
    )
    print(
        f"predicted={checks.predicted_differences} "
        f"observed={checks.observed_differences} "
        f"reciprocal={checks.reciprocal_controls}"
    )
    for window in checks.windows:
        print(window)

    rewrite = carry_rewrite_observation()
    print("carry rewrite")
    print(rewrite)

    baseline = branch_assignment_baseline()
    print("assignment baseline")
    print(baseline)
    print(
        f"difference3={baseline.difference3 / baseline.assignments:.9f} "
        "difference3_with_term3="
        f"{baseline.difference3_with_term3 / baseline.assignments:.9f}"
    )

    print("strict access")
    print(access_discipline_audit())

    systematic = systematic_code_audit()
    print("systematic code")
    for screen in systematic.affine_screens:
        print(screen)
    print(
        f"maximum_output_pair_coverage="
        f"{systematic.maximum_output_pair_coverage}/25"
    )
    print(f"complete_output_pairs={systematic.complete_output_pairs}")

    print("transition cover")
    print(transition_cover_audit())

    print("axis marker holdout")
    markers = axis_marker_audit()
    print(f"labels={markers.labels}")
    print(
        f"direction={markers.direction_matches}/2 "
        f"{markers.direction_model}"
    )
    print(f"scope={markers.scope_matches}/2 {markers.scope_model}")
    print(f"broad_hits={markers.broad_hits}")

    print("header scalar branch")
    print(header_scalar_branch_observation())


if __name__ == "__main__":
    main()
