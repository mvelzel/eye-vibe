#!/usr/bin/env python3
"""Reproduce the frozen 5x5 state-table transform screen."""

from __future__ import annotations

from eye_mystery.state_table_screen import audit_coordinates, audit_visible


def main() -> None:
    for translated in (False, True):
        audit = audit_coordinates(translated=translated)
        print(
            f"coordinate translated={translated}: "
            f"models={audit.models} max_exact={audit.maximum_exact} "
            f"exact_witnesses={len(audit.exact_witnesses)} "
            f"max_offset={audit.maximum_modal_offset} "
            f"offset_witnesses={len(audit.offset_witnesses)}"
        )
        print(f"  exact examples: {audit.exact_witnesses[:3]}")
        print(f"  offset examples: {audit.offset_witnesses[:3]}")
    for independent in (False, True):
        audit = audit_visible(independent_eyes=independent)
        print(
            f"visible independent={independent}: "
            f"models={audit.models} max_exact={audit.maximum_exact} "
            f"exact_witnesses={len(audit.exact_witnesses)} "
            f"max_training={audit.maximum_training} "
            f"training_cobest={audit.training_cobest} "
            f"heldout={audit.training_cobest_heldout}"
        )
        print(f"  exact examples: {audit.exact_witnesses[:3]}")


if __name__ == "__main__":
    main()
