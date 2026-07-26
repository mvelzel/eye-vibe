#!/usr/bin/env python3
"""Run the frozen `42+41` Eye architecture batch."""

from eye_mystery.sixty_first_architectures import (
    INCIDENCE_VARIANTS,
    TREE_LAYOUTS,
    audit_incidence_tape,
    audit_packet_family,
    audit_tree_geometry,
    incidence_score,
    tree_score,
)


def main() -> None:
    print("A. six-by-seven incidence tape")
    for endpoint, route in INCIDENCE_VARIANTS:
        score = incidence_score(endpoint, route)
        print(
            f"  {endpoint} {route}: "
            f"train={score.training_matches}/{score.training_comparisons} "
            f"holdout={score.holdout_matches}/{score.holdout_comparisons}"
        )
        print(
            "    "
            + " ".join(
                f"{context.name}={context.matches}/{context.comparisons}"
                for context in (*score.training, *score.holdout)
            )
        )
    incidence = audit_incidence_tape()
    print(
        f"  selected={incidence.observed.endpoint}/"
        f"{incidence.observed.route} "
        f"train={incidence.observed.training_matches}/"
        f"{incidence.observed.training_comparisons} "
        f"holdout={incidence.observed.holdout_matches}/"
        f"{incidence.observed.holdout_comparisons} "
        f"tail={incidence.holdout_tail_count}/{incidence.controls}="
        f"{incidence.holdout_tail:.9f} "
        f"control-max={incidence.maximum_control_holdout}"
    )

    print("B. balanced 42-leaf binary tree")
    for layout in TREE_LAYOUTS:
        score = tree_score(layout)
        print(
            f"  {layout}: "
            f"train={score.training_matches}/{score.training_comparisons} "
            f"holdout={score.holdout_matches}/{score.holdout_comparisons}"
        )
        print(
            "    "
            + " ".join(
                f"{context.name}={context.matches}/{context.comparisons}"
                for context in (*score.training, *score.holdout)
            )
        )
    tree = audit_tree_geometry()
    print(
        f"  selected={tree.observed.layout} "
        f"train={tree.observed.training_matches}/"
        f"{tree.observed.training_comparisons} "
        f"holdout={tree.observed.holdout_matches}/"
        f"{tree.observed.holdout_comparisons} "
        f"tail={tree.holdout_tail_count}/{tree.controls}="
        f"{tree.holdout_tail:.9f} "
        f"control-max={tree.maximum_control_holdout}"
    )

    print("C. first-N packet XGAK")
    packet_scores = audit_packet_family()
    for score in packet_scores[:12]:
        spec = score.spec
        print(
            f"  N={spec.size} "
            f"{'descending' if spec.descending else 'ascending'} "
            f"{spec.side} "
            f"{'reverse' if spec.reverse else 'preserve'} "
            f"{spec.timing}: "
            f"valid={score.total_valid}/{score.total_events} "
            f"prefixes={score.valid_prefixes}"
        )
    print(
        f"  complete candidates="
        f"{sum(score.complete for score in packet_scores)}/"
        f"{len(packet_scores)}"
    )


if __name__ == "__main__":
    main()
