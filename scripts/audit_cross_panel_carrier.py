#!/usr/bin/env python3
"""Run the frozen cross-panel carrier screens."""

from eye_mystery.cross_panel_carrier import (
    audit_affine,
    audit_eye_arithmetic,
)
from eye_mystery.gap_anchor import FINAL_MESSAGES


def main() -> None:
    for class_term in (False, True):
        print("affine class_term", class_term)
        for panel in FINAL_MESSAGES:
            result = audit_affine(panel, with_class_term=class_term)
            print(result)
    print("base5 eye arithmetic")
    for panel in FINAL_MESSAGES:
        print(audit_eye_arithmetic(panel))


if __name__ == "__main__":
    main()

