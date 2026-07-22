#!/usr/bin/env python3
"""Run the first cheap batch of the frozen tenth Eye-cipher horizon."""

from __future__ import annotations

import argparse
import random

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.ninth_causal import (
    degree_preserving_edge_swaps,
    deepest_leaf_depths,
    shuffle_after_leaf_exits,
    transition_edges,
)
from eye_mystery.ninth_second import (
    checksum_preserving_body_permutation,
    permute_body_labels,
)
from eye_mystery.tenth_wide import (
    DIFFERENTIAL_VARIANTS,
    FIRST_CONTEXTS,
    NONLITERAL_CONTEXTS,
    branch_differential_score,
    context_graph_score,
    context_mappings,
    directed_color_refinement,
    in_faro_position,
    multiplicative_order,
    ordinal_score_family,
    out_faro_position,
    riffle_held_out_score,
    riffle_score,
    shuffled_context_mappings_fixed_points,
)


FIRST_FAMILY = ("east1", "west1", "east2")
LAST_FAMILY = ("east4", "west4", "east5")


def corrected_upper(values, observed) -> float:
    return (sum(value >= observed for value in values) + 1) / (len(values) + 1)


def corrected_lower(values, observed) -> float:
    return (sum(value <= observed for value in values) + 1) / (len(values) + 1)


def selected_empirical_tail(observed, controls, *, higher: bool):
    """Reselect unlike/discrete families by leave-one-control-out ranks."""

    values_by_key = {
        key: [control[key] for control in controls] for key in observed
    }

    def hits(values, target):
        if higher:
            return sum(value >= target for value in values)
        return sum(value <= target for value in values)

    observed_hits = {
        key: hits(values_by_key[key], observed[key]) for key in observed
    }
    selected = min(observed_hits, key=observed_hits.get)
    selected_hits = observed_hits[selected]

    control_selected_hits = []
    for index, control in enumerate(controls):
        control_selected_hits.append(
            min(
                hits(values_by_key[key], control[key]) - 1
                for key in observed
            )
        )
    corrected_hits = sum(
        value <= selected_hits for value in control_selected_hits
    )
    count = len(controls)
    return (
        selected,
        (selected_hits + 1) / (count + 1),
        (corrected_hits + 1) / (count + 1),
        min(control_selected_hits),
        max(control_selected_hits),
    )


def stripped_suffixes(bodies):
    depths = deepest_leaf_depths(bodies)
    return {
        name: tuple(body[depths[name] + 1 :])
        for name, body in bodies.items()
    }


def subset(streams, names):
    return {name: streams[name] for name in names}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--controls", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=0x10E1)
    args = parser.parse_args()
    if args.controls < 1:
        parser.error("--controls must be positive")
    rng = random.Random(args.seed)

    streams = {
        name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
    }
    bodies = {name: stream[1:] for name, stream in streams.items()}
    suffixes = stripped_suffixes(bodies)

    print("F. ordinal-pattern echoes")
    ordinal_observed = ordinal_score_family(suffixes)
    ordinal_first = ordinal_score_family(subset(suffixes, FIRST_FAMILY))
    ordinal_last = ordinal_score_family(subset(suffixes, LAST_FAMILY))
    ordinal_controls = []
    ordinal_first_controls = []
    ordinal_last_controls = []
    for _ in range(args.controls):
        permutation = checksum_preserving_body_permutation(streams, rng)
        control_streams = permute_body_labels(streams, permutation)
        control_bodies = {
            name: stream[1:] for name, stream in control_streams.items()
        }
        control_suffixes = stripped_suffixes(control_bodies)
        ordinal_controls.append(ordinal_score_family(control_suffixes))
        ordinal_first_controls.append(
            ordinal_score_family(subset(control_suffixes, FIRST_FAMILY))
        )
        ordinal_last_controls.append(
            ordinal_score_family(subset(control_suffixes, LAST_FAMILY))
        )
    selected, individual_tail, tail, null_min, null_max = selected_empirical_tail(
        ordinal_observed,
        ordinal_controls,
        higher=True,
    )
    train_selected, train_tail, _, _, _ = selected_empirical_tail(
        ordinal_first,
        ordinal_first_controls,
        higher=True,
    )
    held_values = [control[train_selected] for control in ordinal_last_controls]
    print(
        f"  selected={selected} collisions={ordinal_observed[selected]} "
        f"individual-tail={individual_tail:.6f} corrected-tail={tail:.6f} "
        f"control-selected-hits={null_min}..{null_max}"
    )
    print(
        f"  first-family selector={train_selected} train-tail={train_tail:.6f}; "
        f"last-family collisions={ordinal_last[train_selected]} "
        f"tail={corrected_upper(held_values, ordinal_last[train_selected]):.6f} "
        f"null={min(held_values)}..{max(held_values)}"
    )

    print("G. riffle/Gilbreath rising sequences")
    mappings = context_mappings(streams, NONLITERAL_CONTEXTS)
    first_count = len(FIRST_CONTEXTS)
    observed_riffle = riffle_score(mappings)
    observed_riffle_held = riffle_held_out_score(
        mappings[:first_count], mappings[first_count:]
    )
    riffle_controls = []
    riffle_held_controls = []
    for _ in range(args.controls):
        control = shuffled_context_mappings_fixed_points(mappings, rng)
        riffle_controls.append(riffle_score(control).rising_sequences)
        riffle_held_controls.append(
            riffle_held_out_score(
                control[:first_count], control[first_count:]
            ).test.rising_sequences
        )
    print(
        f"  overall={observed_riffle.rising_sequences}/"
        f"{observed_riffle.edges} convention={observed_riffle.convention} "
        f"tail={corrected_lower(riffle_controls, observed_riffle.rising_sequences):.6f} "
        f"null={min(riffle_controls)}..{max(riffle_controls)}"
    )
    print(
        f"  first->last: train={observed_riffle_held.train.rising_sequences}/"
        f"{observed_riffle_held.train.edges} "
        f"convention={observed_riffle_held.train.convention}; "
        f"test={observed_riffle_held.test.rising_sequences}/"
        f"{observed_riffle_held.test.edges} "
        f"tail={corrected_lower(riffle_held_controls, observed_riffle_held.test.rising_sequences):.6f} "
        f"null={min(riffle_held_controls)}..{max(riffle_held_controls)}"
    )

    print("H. 84-card Faro sentinel")
    out_matches = sum(
        out_faro_position(position) == 2 * position % 83
        for position in range(83)
    )
    print(
        f"  non-sentinel out-Faro matches x->2x mod83: {out_matches}/83; "
        f"sentinel 83->{out_faro_position(83)}; order(2)={multiplicative_order(2, 83)}"
    )
    print(
        f"  in-Faro moves sentinel 83->{in_faro_position(83)}; "
        "a hidden/duplicate output rule is therefore required"
    )

    print("J. graph cover / bisimulation quotient")
    edges = transition_edges(bodies)
    refinement = directed_color_refinement(edges)
    refinement_controls = []
    for _ in range(args.controls):
        control_edges = degree_preserving_edge_swaps(
            edges,
            rng,
            attempts=10 * len(edges),
        )
        refinement_controls.append(directed_color_refinement(control_edges).classes)
    print(
        f"  classes={refinement.classes}/83 singletons={refinement.singleton_classes} "
        f"largest={refinement.largest_class} iterations={refinement.iterations} "
        f"lower-tail={corrected_lower(refinement_controls, refinement.classes):.6f} "
        f"null={min(refinement_controls)}..{max(refinement_controls)}"
    )
    withheld = {}
    for name in MESSAGE_ORDER:
        training = {other: body for other, body in bodies.items() if other != name}
        withheld[name] = directed_color_refinement(transition_edges(training)).classes
    print("  leave-one-panel-out class counts:", withheld)

    print("K. differential branch trails")
    differential_observed = {
        variant: branch_differential_score(bodies, variant).repeated_mass
        for variant in DIFFERENTIAL_VARIANTS
    }
    differential_controls = []
    for _ in range(args.controls):
        control = shuffle_after_leaf_exits(bodies, rng)
        differential_controls.append(
            {
                variant: branch_differential_score(control, variant).repeated_mass
                for variant in DIFFERENTIAL_VARIANTS
            }
        )
    for variant in DIFFERENTIAL_VARIANTS:
        score = branch_differential_score(bodies, variant)
        values = [control[variant] for control in differential_controls]
        print(
            f"  {variant}: repeated={score.repeated_mass}/{score.observations} "
            f"support={score.union_support} summed-support={score.summed_support} "
            f"rank={score.support_rank} tail="
            f"{corrected_upper(values, score.repeated_mass):.6f} "
            f"null={min(values)}..{max(values)}"
        )
    selected, individual_tail, tail, null_min, null_max = selected_empirical_tail(
        differential_observed,
        differential_controls,
        higher=True,
    )
    print(
        f"  selected={selected} individual-tail={individual_tail:.6f} "
        f"corrected-tail={tail:.6f} "
        f"control-selected-hits={null_min}..{null_max}"
    )

    print("L. context-map holonomy")
    graph = context_graph_score()
    print(
        f"  semantic window graph: vertices={graph.vertices} edges={graph.edges} "
        f"components={graph.components} cycle-rank={graph.cycle_rank}"
    )
    print(
        "  no independently observed loop exists; arbitrary label-space words "
        "reduce to the previously negative partial-group closure"
    )


if __name__ == "__main__":
    main()
