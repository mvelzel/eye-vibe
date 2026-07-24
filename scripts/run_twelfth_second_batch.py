#!/usr/bin/env python3
"""Run the second lateral batch of the twelfth Eye novelty horizon."""

from __future__ import annotations

import argparse
import random
from statistics import mean

from eye_mystery.corpus import MESSAGES
from eye_mystery.factoradic_headers import P_MESSAGES
from eye_mystery.ninth_causal import transition_edges
from eye_mystery.twelfth_novelty import context_mappings, eye_bodies
from eye_mystery.twelfth_second import (
    HEADER_PARTITION,
    affine_plane_selection,
    all_line_digraph_triples,
    all_transducer_partition_scores,
    line_digraph_closure,
    physical_action_candidates,
    physical_action_score,
    raw_phase_indicators,
    raw_phase_score,
    raw_transducer_unconditioned_score,
    rotate_phase_indicators,
    shuffle_aligned_panel_values,
    shuffle_mapping_targets,
    shuffle_trigrams_within_row_pairs,
)
from eye_mystery.twelfth_novelty import shuffle_visual_rows


def corrected_upper(values: list[float | int], observed: float | int) -> float:
    return (sum(value >= observed for value in values) + 1) / (len(values) + 1)


def describe(values: list[float | int]) -> str:
    return f"{min(values):.6g}..{max(values):.6g}, mean={mean(values):.6g}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--controls", type=int, default=200)
    parser.add_argument("--seed", type=int, default=0xE1E1202)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    bodies = eye_bodies()

    print("F. visible-symbol line-digraph closure")
    full = line_digraph_closure(transition_edges(bodies))
    triple_scores = all_line_digraph_triples(bodies)
    observed_line = next(
        score
        for score in triple_scores
        if frozenset(score.training) == frozenset(P_MESSAGES)
    )
    line_rank = sum(
        score.f1 >= observed_line.f1 - 1e-15
        for score in triple_scores
    )
    print(
        f"  full: hidden-states={full.hidden_states}; "
        f"present={full.present_edges}; predicted={full.predicted_edges}; "
        f"forced-absent={full.false_positive_edges}"
    )
    print(
        f"  P->Q: hidden-states={observed_line.hidden_states}; "
        f"novel-predictions={observed_line.novel_predictions}; "
        f"novel-truth={observed_line.novel_truth}; hits={observed_line.hits}; "
        f"precision={observed_line.precision:.6f}; "
        f"recall={observed_line.recall:.6f}; f1={observed_line.f1:.6f}; "
        f"rank={line_rank}/{len(triple_scores)}"
    )

    print("H. rejected raw phases")
    indicators = raw_phase_indicators(MESSAGES)
    observed_phase = raw_phase_score(indicators)
    rotation_controls = [
        raw_phase_score(rotate_phase_indicators(indicators, rng))
        for _ in range(args.controls)
    ]
    marker_controls = [max(score.marker_hits) for score in rotation_controls]
    row_controls = [max(score.row_hits) for score in rotation_controls]
    joint_controls = [
        max(score.marker_hits) >= max(observed_phase.marker_hits)
        and max(score.row_hits) >= max(observed_phase.row_hits)
        for score in rotation_controls
    ]
    occupancy_controls = []
    strict_occupancy_controls = []
    for _ in range(args.controls):
        shuffled_messages = shuffle_visual_rows(MESSAGES, rng)
        occupancy_controls.append(
            max(raw_phase_score(raw_phase_indicators(shuffled_messages)).totals)
        )
        strict_messages = shuffle_trigrams_within_row_pairs(MESSAGES, rng)
        strict_occupancy_controls.append(
            max(raw_phase_score(raw_phase_indicators(strict_messages)).totals)
        )
    print(
        f"  total-hidden={observed_phase.totals}; "
        f"within-row-shuffle max-total upper-tail="
        f"{corrected_upper(occupancy_controls, max(observed_phase.totals)):.6f}; "
        f"null={describe(occupancy_controls)}; "
        f"accepted-trigram upper-tail="
        f"{corrected_upper(strict_occupancy_controls, max(observed_phase.totals)):.6f}; "
        f"strict-null={describe(strict_occupancy_controls)}"
    )
    print(
        f"  marker={observed_phase.marker_hits}/{observed_phase.marker_positions}; "
        f"familywise upper-tail="
        f"{corrected_upper(marker_controls, max(observed_phase.marker_hits)):.6f}; "
        f"null={describe(marker_controls)}"
    )
    print(
        f"  row={observed_phase.row_hits}/{observed_phase.row_positions}; "
        f"familywise upper-tail="
        f"{corrected_upper(row_controls, max(observed_phase.row_hits)):.6f}; "
        f"null={describe(row_controls)}; "
        f"joint-max tail={(sum(joint_controls) + 1) / (args.controls + 1):.6f}"
    )

    print("I. AG(2,3) panel line sums")
    observed_planes = {
        prime: affine_plane_selection(bodies, prime)
        for prime in (5, 83)
    }
    plane_controls = {5: [], 83: []}
    for _ in range(args.controls):
        shuffled = shuffle_aligned_panel_values(bodies, rng)
        for prime in plane_controls:
            plane_controls[prime].append(
                affine_plane_selection(shuffled, prime)
            )
    for prime, observed in observed_planes.items():
        heldout_controls = [
            score.selected_heldout for score in plane_controls[prime]
        ]
        training_controls = [
            score.selected_training for score in plane_controls[prime]
        ]
        print(
            f"  F{prime}: natural train/heldout="
            f"{observed.natural_training}/{observed.natural_heldout}; "
            f"selected train/heldout="
            f"{observed.selected_training}/{observed.selected_heldout}; "
            f"grid={observed.selected_grid}; "
            f"heldout upper-tail="
            f"{corrected_upper(heldout_controls, observed.selected_heldout):.6f}; "
            f"heldout-null={describe(heldout_controls)}; "
            f"training-null={describe(training_controls)}"
        )

    print("J. bounded physical shuffle actions")
    mappings = context_mappings()[6:]
    candidates = physical_action_candidates()
    observed_actions = physical_action_score(mappings, candidates)
    action_controls = [
        physical_action_score(
            shuffle_mapping_targets(mappings, rng), candidates
        )
        for _ in range(args.controls)
    ]
    common_controls = [score.common_support for score in action_controls]
    separate_controls = [
        sum(score.per_context_supports) for score in action_controls
    ]
    print(
        f"  candidates={observed_actions.candidates}; "
        f"common={observed_actions.common_action} "
        f"support={observed_actions.common_support}/117; "
        f"upper-tail="
        f"{corrected_upper(common_controls, observed_actions.common_support):.6f}; "
        f"null={describe(common_controls)}"
    )
    print(
        f"  per-context={observed_actions.per_context_supports}; "
        f"exact={observed_actions.exact_contexts}/7; "
        f"sum-upper-tail="
        f"{corrected_upper(separate_controls, sum(observed_actions.per_context_supports)):.6f}; "
        f"null={describe(separate_controls)}"
    )

    print("K. two-register header-controlled transducer")
    partition_scores = all_transducer_partition_scores()
    observed_transducer = next(
        score
        for partition, score in partition_scores
        if frozenset(partition) == frozenset(HEADER_PARTITION)
    )
    unconditioned = raw_transducer_unconditioned_score()
    transducer_rank = sum(
        score.accuracy >= observed_transducer.accuracy - 1e-15
        for _, score in partition_scores
    )
    best = max(
        partition_scores,
        key=lambda item: item[1].accuracy,
    )
    print(
        f"  header={observed_transducer.correct}/{observed_transducer.predictions} "
        f"accuracy={observed_transducer.accuracy:.6f}; "
        f"rank={transducer_rank}/{len(partition_scores)}"
    )
    print(
        f"  unconditioned={unconditioned.correct}/{unconditioned.predictions} "
        f"accuracy={unconditioned.accuracy:.6f}; "
        f"best={best[1].correct}/{best[1].predictions} "
        f"accuracy={best[1].accuracy:.6f}; "
        f"best-partition={best[0]}"
    )


if __name__ == "__main__":
    main()
