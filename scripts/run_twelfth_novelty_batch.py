#!/usr/bin/env python3
"""Run the first mixed batch of the twelfth Eye-cipher novelty horizon."""

from __future__ import annotations

import argparse
import random
from statistics import mean

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES
from eye_mystery.twelfth_novelty import (
    build_coxeter_context_table,
    context_mappings,
    coxeter_scan,
    edge_path_split,
    eye_bodies,
    eye_streams,
    hodge_score,
    polynomial_share_score,
    projective_context_score,
    relabel_bodies_as_edges,
    shuffle_panel_columns,
    shuffle_visual_rows,
    shuffled_context_targets,
    shuffled_header_sources,
)


def corrected_tail(
    controls: list[float | int], observed: float | int, *, lower: bool
) -> float:
    extreme = sum(
        value <= observed if lower else value >= observed
        for value in controls
    )
    return (extreme + 1) / (len(controls) + 1)


def describe(values: list[float | int]) -> str:
    return f"{min(values):.6g}..{max(values):.6g}, mean={mean(values):.6g}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--controls", type=int, default=200)
    parser.add_argument("--seed", type=int, default=0xE1E12)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    streams = eye_streams()
    bodies = eye_bodies()
    mappings = context_mappings()

    print("A. projective context maps")
    # The first six contexts consist of a copied prefix plus a different
    # marker and are reported descriptively.  The frozen test is the seven
    # nonliteral contexts.
    for prime in (83, 101):
        all_score = projective_context_score(mappings, prime)
        observed = projective_context_score(mappings[6:], prime)
        controls = [
            projective_context_score(
                shuffled_context_targets(mappings[6:], rng), prime
            )
            for _ in range(args.controls)
        ]
        extras = [score.extra_support for score in controls]
        print(
            f"  F{prime}: all-support={all_score.maximum_supports}; "
            f"nonliteral-support={observed.maximum_supports}; "
            f"exact={observed.exact_contexts}/7; "
            f"extra-over-three={observed.extra_support}; "
            f"upper-tail={corrected_tail(extras, observed.extra_support, lower=False):.6f}; "
            f"null={describe(extras)}"
        )

    print("B. header-conditioned Coxeter words")
    table = build_coxeter_context_table()
    observed_coxeter = coxeter_scan(table=table)
    coxeter_controls = [
        coxeter_scan(shuffled_header_sources(rng), table=table)
        for _ in range(args.controls)
    ]
    total_controls = [score.best_total for score in coxeter_controls]
    heldout_controls = [score.selected_heldout for score in coxeter_controls]
    print(
        f"  natural-contexts={observed_coxeter.natural_context_scores}; "
        f"natural-body-state-counts={observed_coxeter.natural_distinct_states}"
    )
    print(
        f"  scanned-best-total={observed_coxeter.best_total}/252 "
        f"assignment={observed_coxeter.best_total_assignment}; "
        f"upper-tail={corrected_tail(total_controls, observed_coxeter.best_total, lower=False):.6f}; "
        f"null={describe(total_controls)}"
    )
    print(
        f"  train-selected={observed_coxeter.selected_training}/104 "
        f"assignment={observed_coxeter.selected_assignment}; "
        f"heldout={observed_coxeter.selected_heldout}/148; "
        f"heldout-upper-tail={corrected_tail(heldout_controls, observed_coxeter.selected_heldout, lower=False):.6f}; "
        f"null={describe(heldout_controls)}"
    )

    print("C. natural nine-state directed-edge code")
    observed_edge = edge_path_split(bodies)
    edge_controls = [
        edge_path_split(relabel_bodies_as_edges(bodies, rng))
        for _ in range(args.controls)
    ]
    edge_total_controls = [
        max(score.joins for score in split.all_scores)
        for split in edge_controls
    ]
    edge_heldout_controls = [split.heldout_joins for split in edge_controls]
    print(
        "  orientations="
        + ", ".join(
            f"{score.orientation}:{score.joins}/{score.eligible}"
            for score in observed_edge.all_scores
        )
    )
    print(
        f"  train-selected={observed_edge.selected_orientation} "
        f"{observed_edge.training_joins}/{observed_edge.training_eligible}; "
        f"heldout={observed_edge.heldout_joins}/{observed_edge.heldout_eligible}; "
        f"heldout-upper-tail={corrected_tail(edge_heldout_controls, observed_edge.heldout_joins, lower=False):.6f}; "
        f"null={describe(edge_heldout_controls)}"
    )
    observed_edge_total = max(
        score.joins for score in observed_edge.all_scores
    )
    print(
        f"  scanned-best-total={observed_edge_total}; "
        f"upper-tail={corrected_tail(edge_total_controls, observed_edge_total, lower=False):.6f}; "
        f"null={describe(edge_total_controls)}"
    )

    print("D. cross-panel polynomial shares")
    markers = {name: streams[name][0] for name in MESSAGE_ORDER}
    observed_polynomial = {
        prime: polynomial_share_score(bodies, markers, prime)
        for prime in (83, 101)
    }
    polynomial_controls = {83: [], 101: []}
    for _ in range(args.controls):
        shuffled = shuffle_panel_columns(bodies, rng)
        for prime in polynomial_controls:
            polynomial_controls[prime].append(
                polynomial_share_score(shuffled, markers, prime)
            )
    for prime, observed in observed_polynomial.items():
        degree7 = [score.at_most(7) for score in polynomial_controls[prime]]
        degree6 = [score.at_most(6) for score in polynomial_controls[prime]]
        print(
            f"  F{prime}: columns={observed.columns}; "
            f"degrees={observed.degree_histogram}; "
            f"degree<=7 upper-tail="
            f"{corrected_tail(degree7, observed.at_most(7), lower=False):.6f} "
            f"null={describe(degree7)}; "
            f"degree<=6={observed.at_most(6)} "
            f"upper-tail={corrected_tail(degree6, observed.at_most(6), lower=False):.6f}"
        )

    print("E. spatial Hodge defects")
    observed_hodge = hodge_score(MESSAGES)
    hodge_controls = [
        hodge_score(shuffle_visual_rows(MESSAGES, rng))
        for _ in range(args.controls)
    ]
    distinct_controls = [score.distinct_features for score in hodge_controls]
    zero_controls = [score.zero_rate for score in hodge_controls]
    agreement_controls = [
        score.aligned_agreement_rate for score in hodge_controls
    ]
    print(
        f"  vertices={observed_hodge.vertices}; "
        f"distinct={observed_hodge.distinct_features} "
        f"lower-tail={corrected_tail(distinct_controls, observed_hodge.distinct_features, lower=True):.6f} "
        f"null={describe(distinct_controls)}"
    )
    print(
        f"  zero={observed_hodge.zero_features} "
        f"rate={observed_hodge.zero_rate:.6f} "
        f"upper-tail={corrected_tail(zero_controls, observed_hodge.zero_rate, lower=False):.6f} "
        f"null={describe(zero_controls)}"
    )
    print(
        f"  nontrivial-aligned={observed_hodge.nontrivial_aligned_pairs}; "
        f"feature-agreements={observed_hodge.aligned_feature_agreements}; "
        f"rate={observed_hodge.aligned_agreement_rate:.6f}; "
        f"upper-tail={corrected_tail(agreement_controls, observed_hodge.aligned_agreement_rate, lower=False):.6f}; "
        f"null={describe(agreement_controls)}"
    )


if __name__ == "__main__":
    main()
