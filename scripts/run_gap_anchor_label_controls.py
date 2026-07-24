#!/usr/bin/env python3
"""Run frozen global-label controls for the gap-anchor relation."""

from eye_mystery.gap_anchor import gap_anchor_label_audit


def main() -> None:
    audit = gap_anchor_label_audit()
    print(
        "body-only",
        f"exact=({1 + audit.body_only_exact_matches}/{1 + audit.controls})"
        f"={audit.body_only_exact_tail:.9f}",
        f"broad=({1 + audit.body_only_broad_matches}/{1 + audit.controls})"
        f"={audit.body_only_broad_tail:.9f}",
    )
    print(
        "joint",
        f"exact=({1 + audit.joint_exact_matches}/{1 + audit.controls})"
        f"={audit.joint_exact_tail:.9f}",
        f"broad=({1 + audit.joint_broad_matches}/{1 + audit.controls})"
        f"={audit.joint_broad_tail:.9f}",
    )
    print(f"natural_coordinate_passes={audit.natural_coordinate_passes}")


if __name__ == "__main__":
    main()
