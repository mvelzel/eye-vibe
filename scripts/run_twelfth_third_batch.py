#!/usr/bin/env python3
"""Run the final finite batch of the twelfth Eye novelty horizon."""

from __future__ import annotations

import argparse
import random
from concurrent.futures import ProcessPoolExecutor
from statistics import mean

from eye_mystery.corpus import MESSAGES
from eye_mystery.ninth_causal import (
    degree_preserving_edge_swaps,
    transition_edges,
)
from eye_mystery.twelfth_novelty import (
    context_mappings,
    eye_bodies,
    shuffled_context_targets,
)
from eye_mystery.twelfth_second import shuffle_trigrams_within_row_pairs
from eye_mystery.twelfth_third import (
    FIVE_ARY_FILTERS,
    SignedProjectiveScore,
    leading_singular_energy_fraction,
    primitive_generator_supports,
    select_signed_projective_center,
    select_convolutional_filter,
    signed_projective_scan_reaches,
)


def projective_control_reaches(
    task: tuple[tuple[dict[int, int], ...], SignedProjectiveScore],
) -> bool:
    mappings, threshold = task
    return signed_projective_scan_reaches(mappings, threshold)


def corrected_upper(values: list[float], observed: float) -> float:
    return (sum(value >= observed for value in values) + 1) / (len(values) + 1)


def describe(values: list[float]) -> str:
    return f"{min(values):.6g}..{max(values):.6g}, mean={mean(values):.6g}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--controls", type=int, default=200)
    parser.add_argument("--seed", type=int, default=0xE1E1203)
    parser.add_argument("--swap-attempts-per-edge", type=int, default=20)
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()
    # Keep the newly restored G lane from perturbing the already frozen L/M
    # controls merely by consuming pseudorandom numbers first.
    projective_rng = random.Random(args.seed)
    mechanism_rng = random.Random(args.seed)

    print("G. signed projective quotient")
    mappings = context_mappings()[6:]
    observed_projective = select_signed_projective_center(mappings)
    projective_tasks = [
        (
            shuffled_context_targets(mappings, projective_rng),
            observed_projective,
        )
        for _ in range(args.controls)
    ]
    if args.workers < 1:
        parser.error("--workers must be positive")
    if args.workers == 1:
        projective_controls = list(
            map(projective_control_reaches, projective_tasks)
        )
    else:
        with ProcessPoolExecutor(max_workers=args.workers) as executor:
            projective_controls = list(
                executor.map(projective_control_reaches, projective_tasks)
            )
    generator_supports = primitive_generator_supports(
        mappings,
        observed_projective.center,
    )
    print(
        f"  centers=83; selected={observed_projective.center}; "
        f"relation-sizes={observed_projective.relation_sizes}; "
        f"supports={observed_projective.supports}; "
        f"exact={observed_projective.exact_contexts}/7; "
        f"extra-over-three={observed_projective.extra_support}"
    )
    print(
        f"  lexicographic selected-score upper-tail="
        f"{(sum(projective_controls) + 1) / (args.controls + 1):.6f}; "
        f"nulls-at-least-observed={sum(projective_controls)}/{args.controls}; "
        f"primitive-root-coordinate-supports={len(set(generator_supports))}"
    )

    print("L. directed-transition spectral concentration")
    edges = transition_edges(eye_bodies())
    observed_spectral = leading_singular_energy_fraction(edges)
    spectral_controls = [
        leading_singular_energy_fraction(
            degree_preserving_edge_swaps(
                edges,
                mechanism_rng,
                attempts=args.swap_attempts_per_edge * len(edges),
            )
        )
        for _ in range(args.controls)
    ]
    print(
        f"  edges={len(edges)}; leading-energy={observed_spectral:.9f}; "
        f"upper-tail={corrected_upper(spectral_controls, observed_spectral):.6f}; "
        f"degree-null={describe(spectral_controls)}"
    )

    print("M. five-ary convolutional syndrome")
    observed_convolution = select_convolutional_filter()
    convolution_controls = [
        select_convolutional_filter(
            messages=shuffle_trigrams_within_row_pairs(
                MESSAGES,
                mechanism_rng,
            )
        )
        for _ in range(args.controls)
    ]
    heldout_controls = [
        selection.heldout.zero_rate for selection in convolution_controls
    ]
    training_controls = [
        selection.training.zero_rate for selection in convolution_controls
    ]
    print(
        f"  family={len(FIVE_ARY_FILTERS)}; "
        f"selected={observed_convolution.coefficients}; "
        f"training={observed_convolution.training.zeros}/"
        f"{observed_convolution.training.positions} "
        f"rate={observed_convolution.training.zero_rate:.9f}; "
        f"training-null={describe(training_controls)}"
    )
    print(
        f"  heldout={observed_convolution.heldout.zeros}/"
        f"{observed_convolution.heldout.positions} "
        f"rate={observed_convolution.heldout.zero_rate:.9f}; "
        f"corrected-upper-tail="
        f"{corrected_upper(heldout_controls, observed_convolution.heldout.zero_rate):.6f}; "
        f"heldout-null={describe(heldout_controls)}"
    )


if __name__ == "__main__":
    main()
