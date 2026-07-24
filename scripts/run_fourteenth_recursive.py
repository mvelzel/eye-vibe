#!/usr/bin/env python3
"""Run the frozen recursive branch-check Eye audit."""

from __future__ import annotations

import argparse
from collections import Counter
import random

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.fourteenth_recursive import (
    audit_recursive_checks,
    planted_branch_dictionary,
)
from eye_mystery.trie_checksum import (
    random_signature_preserving_relabeling,
)


def count_vector(values) -> tuple[int, ...]:
    counts = Counter(values)
    return tuple(counts[label] for label in range(83))


def describe(label, audit) -> None:
    print(label)
    print(f"  branches={len(audit.branch_paths)}")
    print(f"  paths={audit.branch_paths}")
    print(
        f"  loo={audit.leave_one_out_correct}/"
        f"{len(audit.branch_paths)}"
    )
    print(f"  heldout_rules={tuple(rule.name for rule in audit.heldout_rules)}")
    print(f"  heldout_values={audit.heldout_values}")
    print(f"  selected={audit.selected_rule.name}")
    print(
        f"  selected_branch_values={audit.selected_branch_values}; "
        f"zeros={audit.selected_branch_zeros}"
    )
    print(f"  root={audit.root_value}; root_zero={audit.root_zero}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--controls", type=int, default=2_000)
    parser.add_argument("--seed", type=int, default=0x5452494543484543)
    parser.add_argument("--positive-only", action="store_true")
    args = parser.parse_args()

    planted = audit_recursive_checks(planted_branch_dictionary())
    describe("PLANTED", planted)
    if args.positive_only:
        return

    streams = {
        name: trigram_values(MESSAGES[name])
        for name in MESSAGE_ORDER
    }
    bodies = {name: stream[1:] for name, stream in streams.items()}
    observed = audit_recursive_checks(bodies)
    describe("OBSERVED", observed)
    if (
        observed.leave_one_out_correct != len(observed.branch_paths)
        or not observed.root_zero
    ):
        print("  controls=not-run; exact data gate failed")
        return

    diagonal = tuple(
        count_vector(streams[name])
        for name in ("east1", "east3", "east5")
    )
    markers = tuple(streams[name][0] for name in MESSAGE_ORDER)
    rng = random.Random(args.seed)
    joint = 0
    for _ in range(args.controls):
        mapping = random_signature_preserving_relabeling(
            83,
            diagonal,
            rng,
            fixed_labels=markers,
        )
        relabeled = {
            name: tuple(mapping[value] for value in body)
            for name, body in bodies.items()
        }
        control = audit_recursive_checks(relabeled)
        joint += (
            control.leave_one_out_correct
            >= observed.leave_one_out_correct
            and control.root_zero
        )
    print(
        f"  joint_controls={joint}/{args.controls}; "
        f"upper={(1 + joint) / (1 + args.controls):.9f}"
    )


if __name__ == "__main__":
    main()
