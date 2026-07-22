#!/usr/bin/env python3
"""Run the second wide slice of the ninth Eye-cipher pass."""

from __future__ import annotations

import argparse
import random

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.ninth_second import (
    EAST5_TRAIL_ORDER,
    FEATURE_VARIANTS,
    FIRST_CONTEXTS,
    KEY_PHRASE,
    LAST_CONTEXTS,
    TRAILER_ALPHABET,
    affine_body_permutations,
    audit_category_pair,
    best_carry_markov_score,
    carry_held_out_score,
    category_tape,
    checksum_preserving_body_permutation,
    keyed_alphabet,
    permute_body_labels,
    trailer_categories,
    transition_feature_context_score,
    transition_feature_held_out_score,
    worldline_score,
)


def corrected_upper(values, observed) -> float:
    return (sum(value >= observed for value in values) + 1) / (len(values) + 1)


def exact_upper(values, observed) -> tuple[int, int, float]:
    hits = sum(value >= observed for value in values)
    return hits, len(values), hits / len(values)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--controls", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=0xE1E)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    streams = {
        name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
    }
    bodies = {name: streams[name][1:] for name in MESSAGE_ORDER}

    print("A. trailer-category XGAK")
    print(
        "  keyed-alphabet=",
        keyed_alphabet(KEY_PHRASE, "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"),
        " expected=",
        TRAILER_ALPHABET,
        sep="",
    )
    for q_on_back, split_back_digits in (
        (False, False),
        (True, False),
        (False, True),
        (True, True),
    ):
        categories = trailer_categories(
            q_on_back=q_on_back,
            split_back_digits=split_back_digits,
        )
        print(
            "  categories Q-"
            + ("back" if q_on_back else "front")
            + (" split-digits" if split_back_digits else "")
            + ": "
            + " | ".join(
                "".join(
                    symbol for symbol in TRAILER_ALPHABET if symbol in group
                )
                for group in categories
            )
        )
        digit_tape = category_tape("123456789", categories)
        print("  nine-digit category tape:", digit_tape)
        for left, right in (
            ("EAST", "WEST"),
            ("COPPER", "SILVER"),
            ("FROZEN", "MOLTEN"),
        ):
            audit = audit_category_pair(left, right, categories)
            print(
                f"  {left}/{right}: {audit.left_tape}/{audit.right_tape} "
                f"mismatches={audit.mismatches}"
            )
    waite = "SUBLIME THAT WHICH IS THE LOWEST, AND MAKE THAT WHICH IS THE HIGHEST, THE LOWEST."
    unsupported = sorted(
        {
            symbol
            for symbol, category in zip(
                waite, category_tape(waite, trailer_categories()), strict=True
            )
            if category is None
        }
    )
    print("  literal Waite unsupported symbols:", repr("".join(unsupported)))
    print(
        "  normalized THATWHICH tape:",
        category_tape("THATWHICH", trailer_categories()),
    )

    print("K. base-five borrow automaton and digit-feature ablation")
    last_to_first = carry_held_out_score(streams, LAST_CONTEXTS, FIRST_CONTEXTS)
    markov = best_carry_markov_score(streams)
    observed_features = {
        variant: (
            transition_feature_context_score(streams, variant),
            transition_feature_held_out_score(
                streams, variant, FIRST_CONTEXTS, LAST_CONTEXTS
            ),
        )
        for variant in FEATURE_VARIANTS
    }
    feature_overall_controls = {variant: [] for variant in FEATURE_VARIANTS}
    feature_held_controls = {variant: [] for variant in FEATURE_VARIANTS}
    last_to_first_controls = []
    markov_controls = []
    for _ in range(args.controls):
        permutation = list(range(83))
        rng.shuffle(permutation)
        control = permute_body_labels(streams, permutation)
        for variant in FEATURE_VARIANTS:
            feature_overall_controls[variant].append(
                transition_feature_context_score(control, variant).matches
            )
            feature_held_controls[variant].append(
                transition_feature_held_out_score(
                    control,
                    variant,
                    FIRST_CONTEXTS,
                    LAST_CONTEXTS,
                ).test.matches
            )
        last_to_first_controls.append(
            carry_held_out_score(control, LAST_CONTEXTS, FIRST_CONTEXTS).test.matches
        )
        markov_controls.append(best_carry_markov_score(control).gain)
    for variant in FEATURE_VARIANTS:
        feature_overall, feature_held = observed_features[variant]
        overall_controls = feature_overall_controls[variant]
        held_controls = feature_held_controls[variant]
        print(
            f"  {variant}: overall={feature_overall.matches}/"
            f"{feature_overall.comparisons} "
            f"convention={feature_overall.convention} "
            f"arbitrary-tail={corrected_upper(overall_controls, feature_overall.matches):.6f} "
            f"null={min(overall_controls)}..{max(overall_controls)}; "
            f"first->last train={feature_held.train.matches}/"
            f"{feature_held.train.comparisons} "
            f"convention={feature_held.train.convention} "
            f"test={feature_held.test.matches}/{feature_held.test.comparisons} "
            f"tail={corrected_upper(held_controls, feature_held.test.matches):.6f} "
            f"null={min(held_controls)}..{max(held_controls)}"
        )
    print(
        f"  borrow_pair last->first: train={last_to_first.train.matches}/"
        f"{last_to_first.train.comparisons} "
        f"convention={last_to_first.train.convention} "
        f"test={last_to_first.test.matches}/{last_to_first.test.comparisons} "
        f"tail={corrected_upper(last_to_first_controls, last_to_first.test.matches):.6f} "
        f"null={min(last_to_first_controls)}..{max(last_to_first_controls)}"
    )
    print(
        f"  Markov-gain={markov.gain:.6f} convention={markov.convention} "
        f"tail={corrected_upper(markov_controls, markov.gain):.6f} "
        f"null={min(markov_controls):.6f}..{max(markov_controls):.6f}"
    )

    print("  checksum-preserving subgroup controls")
    subgroup_overall = {variant: [] for variant in ("borrow_pair", "independent_pair")}
    subgroup_held = {variant: [] for variant in ("borrow_pair", "independent_pair")}
    for _ in range(args.controls):
        permutation = checksum_preserving_body_permutation(streams, rng)
        control = permute_body_labels(streams, permutation)
        for variant in subgroup_overall:
            subgroup_overall[variant].append(
                transition_feature_context_score(control, variant).matches
            )
            subgroup_held[variant].append(
                transition_feature_held_out_score(
                    control,
                    variant,
                    FIRST_CONTEXTS,
                    LAST_CONTEXTS,
                ).test.matches
            )
    for variant in subgroup_overall:
        feature_overall, feature_held = observed_features[variant]
        print(
            f"    {variant}: overall-tail="
            f"{corrected_upper(subgroup_overall[variant], feature_overall.matches):.6f} "
            f"null={min(subgroup_overall[variant])}..{max(subgroup_overall[variant])}; "
            f"held-tail={corrected_upper(subgroup_held[variant], feature_held.test.matches):.6f} "
            f"null={min(subgroup_held[variant])}..{max(subgroup_held[variant])}"
        )

    print("  exhaustive affine F_83 controls")
    affine_overall = {variant: [] for variant in ("borrow_pair", "independent_pair")}
    affine_held = {variant: [] for variant in ("borrow_pair", "independent_pair")}
    for permutation in affine_body_permutations():
        control = permute_body_labels(streams, permutation)
        for variant in affine_overall:
            affine_overall[variant].append(
                transition_feature_context_score(control, variant).matches
            )
            affine_held[variant].append(
                transition_feature_held_out_score(
                    control,
                    variant,
                    FIRST_CONTEXTS,
                    LAST_CONTEXTS,
                ).test.matches
            )
    for variant in affine_overall:
        feature_overall, feature_held = observed_features[variant]
        overall_hits, total, overall_tail = exact_upper(
            affine_overall[variant], feature_overall.matches
        )
        held_hits, _, held_tail = exact_upper(
            affine_held[variant], feature_held.test.matches
        )
        print(
            f"    {variant}: overall={overall_hits}/{total}={overall_tail:.6f}; "
            f"held={held_hits}/{total}={held_tail:.6f}"
        )

    print("N. one-worldline checkpoints")
    for isomorphic in (False, True):
        label = "isomorphic" if isomorphic else "literal"
        for order_name, order in (
            ("canonical", MESSAGE_ORDER),
            ("east5-trail", EAST5_TRAIL_ORDER),
        ):
            score = worldline_score(bodies, order, isomorphic=isomorphic)
            print(
                f"  {label} {order_name}: score={score.score} "
                f"tail={score.exact_tail:.6f} best={score.best_score} "
                f"best-order={','.join(score.best_order)}"
            )


if __name__ == "__main__":
    main()
