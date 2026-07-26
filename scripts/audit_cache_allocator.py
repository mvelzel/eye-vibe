#!/usr/bin/env python3
"""Run the frozen adaptive cache/allocator screen."""

from eye_mystery.cache_allocator_screen import (
    audit_panel,
    identifiability_certificate,
)
from eye_mystery.gap_anchor import FINAL_MESSAGES


def main() -> None:
    certificate = identifiability_certificate()
    print("identifiability", certificate)
    for affine in (False, True):
        print("affine_target", affine)
        for message in FINAL_MESSAGES:
            screen = audit_panel(message, affine_target=affine)
            print(
                message,
                "models",
                screen.models,
                "max_training",
                screen.maximum_training_matches,
                "cobest",
                screen.cobest_models,
                "perfect",
                screen.cobest_with_perfect_training,
                "best_representative_holdout",
                screen.maximum_cobest_holdout_matches,
            )
            for witness in screen.witnesses[:3]:
                print(" ", witness)


if __name__ == "__main__":
    main()

