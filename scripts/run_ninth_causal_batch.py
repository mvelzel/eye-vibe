#!/usr/bin/env python3
"""Run the first breadth batch of the ninth causal Eye-cipher portfolio."""

from __future__ import annotations

import argparse
import random

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.ninth_causal import (
    CONTEXT_SPECS,
    body_streams,
    branch_influence_score,
    common_base_score,
    degree_preserving_edge_swaps,
    deepest_leaf_depths,
    forbidden_support_score,
    header_conditional_gain,
    header_conditional_score,
    header_groups,
    invariant_transition_features,
    message_automorphisms,
    partial_bijection_iff_same_equality_signature,
    shuffled_context_mappings,
    shuffle_after_leaf_exits,
    synchronization_profile,
    three_by_three_partitions,
    transition_edges,
)
from eye_mystery.progression_certificate import context_mapping


def context_data(streams):
    mappings = []
    segments = []
    for name, left, left_start, right, right_start, length in CONTEXT_SPECS:
        mappings.append(
            context_mapping(left, left_start, right, right_start, length)
        )
        segments.append(
            (
                name,
                streams[left][left_start : left_start + length],
                streams[right][right_start : right_start + length],
            )
        )
    return tuple(mappings), tuple(segments)


def corrected_tail(values, observed, *, lower: bool) -> float:
    extreme = sum(value <= observed if lower else value >= observed for value in values)
    return (extreme + 1) / (len(values) + 1)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--controls", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=0xE1E)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    streams = {
        name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
    }
    bodies = body_streams(streams)
    mappings, segments = context_data(streams)

    print("C. common-base assignment lower bound")
    for label, selected in (
        ("all-contexts", mappings),
        # The first six maps are literal copied prefixes.  This second result
        # is the admissible test of locality beyond that known identity mass.
        ("nonliteral-isomorphs", mappings[6:]),
    ):
        common = common_base_score(selected)
        common_controls = [
            common_base_score(shuffled_context_mappings(selected, rng)).agreements
            for _ in range(args.controls)
        ]
        print(
            f"  {label}: agreements={common.agreements}/{common.edges} "
            f"disagreements={common.disagreements} "
            f"upper-tail={corrected_tail(common_controls, common.agreements, lower=False):.6f} "
            f"null-range={min(common_controls)}..{max(common_controls)}"
        )

    print("E. branch-intervention influence")
    branch = branch_influence_score(bodies)
    branch_controls = [
        branch_influence_score(shuffle_after_leaf_exits(bodies, rng))
        for _ in range(args.controls)
    ]
    print(
        f"  branches={branch.branches} active-columns={branch.active_columns} "
        f"GF2-rank={branch.gf2_rank} Boolean-rank={branch.boolean_rank} "
        f"nested-pairs={branch.nested_pairs}"
    )
    for field, lower in (
        ("active_columns", True),
        ("gf2_rank", True),
        ("boolean_rank", True),
        ("nested_pairs", False),
    ):
        observed = getattr(branch, field)
        controls = [getattr(score, field) for score in branch_controls]
        print(
            f"  {field}-tail={corrected_tail(controls, observed, lower=lower):.6f} "
            f"null-range={min(controls)}..{max(controls)}"
        )

    print("F. synchronization/observability")
    profiles = []
    for name, left, right in segments:
        assert partial_bijection_iff_same_equality_signature(left, right)
        profile = synchronization_profile(left, right)
        profiles.append(profile)
        print(
            f"  {name:<18} length={profile.length:>2} edges={profile.edges:>2} "
            f"validations={profile.validation_positions:>2} "
            f"first-validation={profile.first_validation!s:>4} "
            f"last-new={profile.last_new_edge:>2} conflict={profile.first_conflict}"
        )
    print(
        "  identity: a full partial bijection exists iff the two equality "
        "signatures are identical; these selected contexts add no independent "
        "synchronization observable"
    )

    print("G. equality-skeleton automorphisms")
    exact_automorphisms = message_automorphisms(bodies, truncate=False)
    truncated_automorphisms = message_automorphisms(bodies, truncate=True)
    print(
        f"  full-path group-order={len(exact_automorphisms)} "
        f"common-98-coordinate group-order={len(truncated_automorphisms)}"
    )

    print("H. forbidden-transition support")
    edges = transition_edges(bodies)
    forbidden = forbidden_support_score(edges)
    forbidden_controls = []
    current = edges
    for _ in range(args.controls):
        current = degree_preserving_edge_swaps(
            current, rng, attempts=20 * len(edges)
        )
        forbidden_controls.append(forbidden_support_score(current))
    print(
        f"  present={forbidden.present_edges} absent-GF2-rank={forbidden.absent_rank} "
        f"distinct-rows={forbidden.distinct_absent_rows} "
        f"rectangle-lower-bound={forbidden.row_pattern_lower_bound}"
    )
    for field, lower in (
        ("absent_rank", True),
        ("distinct_absent_rows", True),
        ("row_pattern_lower_bound", True),
    ):
        observed = getattr(forbidden, field)
        controls = [getattr(score, field) for score in forbidden_controls]
        print(
            f"  {field}-tail={corrected_tail(controls, observed, lower=lower):.6f} "
            f"null-range={min(controls)}..{max(controls)}"
        )

    print("L. header-class conditional dynamics")
    conditional = header_conditional_score(bodies)
    print(
        f"  LOO-log-gain={conditional.observed_gain:.6f} "
        f"exact-tail={conditional.exact_tail:.6f} "
        f"rank={conditional.at_least_observed}/{conditional.partitions} "
        f"best={conditional.best_gain:.6f}"
    )
    print(
        "  best-groups="
        + " | ".join(",".join(sorted(group)) for group in conditional.best_groups)
    )
    depths = deepest_leaf_depths(bodies)
    partitions = three_by_three_partitions(tuple(bodies))
    for boundary, starts in (
        ("full", {name: 0 for name in bodies}),
        ("leaf-exit", depths),
    ):
        features = {
            name: invariant_transition_features(body, start=starts[name])
            for name, body in bodies.items()
        }
        for alpha in (0.1, 0.5, 1.0, 2.0):
            gain = header_conditional_gain(
                features, header_groups(), alpha=alpha
            )
            rank = sum(
                header_conditional_gain(features, partition, alpha=alpha)
                >= gain - 1e-12
                for partition in partitions
            )
            print(
                f"  sensitivity boundary={boundary} alpha={alpha:.1f} "
                f"gain={gain:.6f} rank={rank}/280"
            )


if __name__ == "__main__":
    main()
