#!/usr/bin/env python3
"""Run the frozen held-out desert paired-record quotient audit."""

from __future__ import annotations

import argparse

from eye_mystery.diamond_context import (
    CONTROL_SEED,
    run_diamond_context_audit,
)


def print_split(label, score) -> None:
    print(
        f"{label}: {score.agreements}/{score.eligible_coordinates} "
        f"exact={score.exact_contexts}/{len(score.contexts)}"
    )
    for context in score.contexts:
        print(
            f"  {context.name}: "
            f"{context.agreements}/{context.eligible_coordinates} "
            f"exact={context.exact}"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--controls", type=int, default=50_000)
    parser.add_argument(
        "--seed",
        type=lambda text: int(text, 0),
        default=CONTROL_SEED,
    )
    args = parser.parse_args()

    audit = run_diamond_context_audit(
        controls=args.controls,
        seed=args.seed,
    )
    print_split("squared training", audit.training)
    print_split("squared held out", audit.heldout)
    print_split("base25 training", audit.base25_training)
    print_split("base25 held out", audit.base25_heldout)
    print("relative x-order held-out scores:", audit.relative_order_scores)
    print(
        "document order:",
        f"rank={audit.document_order_rank}/6",
        f"ties={audit.document_order_ties}",
    )
    print("controls:", audit.controls)
    print("control hits:", audit.control_hits)
    print("inclusive tail:", f"{audit.tail:.9f}")
    print("passes:", audit.passes)
    print("control range:", audit.control_distribution[0][0], audit.control_distribution[-1][0])


if __name__ == "__main__":
    main()

