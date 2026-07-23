#!/usr/bin/env python3
"""Test whether pair/triple remainders follow a small payload-side rule."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from eye_mystery.practice_cipher4 import cyclic_differences
from eye_mystery.practice_cipher4_selector_prediction import (
    attribute_prediction,
    audit_selector_prediction,
)


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data",
        type=Path,
        default=ROOT / "artifacts/practice-sdlwdr/cipher4.json",
    )
    parser.add_argument("--controls", type=int, default=1_000)
    parser.add_argument("--seed", type=int, default=0x53444C5744520405)
    parser.add_argument("--top", type=int, default=12)
    parser.add_argument(
        "--null-mode",
        action="append",
        choices=(
            "selector",
            "within-q",
            "circular-selector",
            "paired-rank",
        ),
        dest="null_modes",
        help="repeatable; defaults to all four declared null models",
    )
    args = parser.parse_args()
    null_modes = args.null_modes or (
        "selector",
        "within-q",
        "circular-selector",
        "paired-rank",
    )

    messages = json.loads(args.data.read_text())
    ranks = tuple(
        tuple(value - 22 for value in cyclic_differences(message))
        for message in messages
    )
    for width, payload_modulus in ((2, 29), (3, 19)):
        quotient = tuple(
            tuple(rank // width for rank in stream) for stream in ranks
        )
        selector = tuple(
            tuple(rank % width for rank in stream) for stream in ranks
        )
        print(f"\nWIDTH={width} PAYLOAD={payload_modulus}")
        for null_mode in null_modes:
            audit = audit_selector_prediction(
                quotient,
                selector,
                selector_size=width,
                payload_modulus=payload_modulus,
                controls=args.controls,
                seed=args.seed ^ width,
                null_mode=null_mode,
            )
            print(
                f"null={null_mode} best={audit.best.spec.name}"
                f"{audit.best.spec.phase or ''} "
                f"gain={audit.best.gain_bits_per_symbol:.9f} "
                f"accuracy={audit.best.accuracy:.9f} "
                f"baseline={audit.best.baseline_accuracy:.9f} "
                f"evaluated={audit.best.evaluated}"
            )
            print(
                f"  selected-null={audit.null_minimum:.9f}.."
                f"{audit.null_maximum:.9f} mean={audit.null_mean:.9f} "
                f"upper={audit.corrected_upper_tail:.9f}"
            )
            if null_mode == null_modes[0]:
                for score in audit.scores[: args.top]:
                    print(
                        f"  {score.spec.name}{score.spec.phase or ''}: "
                        f"gain={score.gain_bits_per_symbol:+.9f} "
                        f"accuracy={score.accuracy:.6f} "
                        f"baseline={score.baseline_accuracy:.6f} "
                        f"n={score.evaluated}"
                    )
        attribution = attribute_prediction(
            quotient,
            selector,
            spec=audit.best.spec,
            selector_size=width,
            payload_modulus=payload_modulus,
            width=width,
        )
        print(
            "  attribution: "
            f"exact-rank-bigram="
            f"{attribution.correct_seen_context_exact_bigram}/"
            f"{attribution.seen_context_exact_bigram}; "
            f"new-rank-bigram="
            f"{attribution.correct_seen_context_new_bigram}/"
            f"{attribution.seen_context_new_bigram}; "
            f"unseen-context={attribution.correct_unseen_context}/"
            f"{attribution.unseen_context}; "
            f"exact-rank-trigram={attribution.correct_exact_trigram}/"
            f"{attribution.exact_trigram}"
        )


if __name__ == "__main__":
    main()
