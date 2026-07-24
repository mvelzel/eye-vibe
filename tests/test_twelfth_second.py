from __future__ import annotations

import unittest

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES
from eye_mystery.factoradic_headers import P_MESSAGES
from eye_mystery.ninth_causal import transition_edges
from eye_mystery.twelfth_novelty import context_mappings, eye_bodies
from eye_mystery.twelfth_second import (
    HEADER_PARTITION,
    affine_plane_selection,
    all_line_digraph_triples,
    all_transducer_partition_scores,
    cross_phase_values,
    line_digraph_closure,
    line_sum_closures,
    physical_action_candidates,
    physical_action_score,
    raw_phase_indicators,
    raw_phase_score,
    raw_suffix_starts,
    raw_transducer_partition_score,
    raw_transducer_unconditioned_score,
    shuffle_trigrams_within_row_pairs,
)


class TwelfthSecondPrimitiveTests(unittest.TestCase):
    def test_line_digraph_closure_forces_composable_transition(self) -> None:
        closure = line_digraph_closure(((0, 1),), alphabet_size=3)
        self.assertIn((0, 1), closure.predictions)
        self.assertEqual(closure.present_edges, 1)

    def test_cross_phases_use_boundary_digits(self) -> None:
        # Accepted 012 | 340 gives crossing trigrams 123 and 234.
        phase_one, phase_two = cross_phase_values((0, 1, 2, 3, 4, 0))
        self.assertEqual(phase_one, (25 * 1 + 5 * 2 + 3,))
        self.assertEqual(phase_two, (25 * 2 + 5 * 3 + 4,))

    def test_strict_phase_control_preserves_row_parity_trigram_multisets(self) -> None:
        import random

        shuffled = shuffle_trigrams_within_row_pairs(
            MESSAGES, random.Random(12)
        )
        for name in MESSAGE_ORDER:
            original = MESSAGES[name]
            replacement = shuffled[name]
            self.assertEqual(len(original), len(replacement))
            original_trigrams = [
                tuple(original[index : index + 3])
                for index in range(0, len(original), 3)
            ]
            replacement_trigrams = [
                tuple(replacement[index : index + 3])
                for index in range(0, len(replacement), 3)
            ]
            for parity in range(2):
                self.assertEqual(
                    sorted(original_trigrams[parity::2]),
                    sorted(replacement_trigrams[parity::2]),
                )

    def test_constant_affine_plane_closes_all_parallel_classes(self) -> None:
        self.assertEqual(line_sum_closures((7,) * 9, 83), 4)

    def test_physical_action_dictionary_is_unique(self) -> None:
        candidates = physical_action_candidates(11)
        self.assertEqual(
            len(candidates),
            len({permutation for _, permutation in candidates}),
        )
        self.assertTrue(
            all(
                tuple(sorted(permutation)) == tuple(range(11))
                for _, permutation in candidates
            )
        )

    def test_raw_transducer_predicts_identical_periodic_streams(self) -> None:
        messages = {
            name: (0, 1, 2, 0, 1, 2, 0, 1, 2)
            for name in MESSAGE_ORDER
        }
        partition = tuple(
            frozenset(MESSAGE_ORDER[start : start + 3])
            for start in range(0, 9, 3)
        )
        score = raw_transducer_partition_score(
            partition,
            messages=messages,
            starts={name: 2 for name in MESSAGE_ORDER},
        )
        self.assertEqual(score.correct, score.predictions)


class TwelfthSecondCorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bodies = eye_bodies()

    def test_full_line_digraph_closure_collapses_to_one_state(self) -> None:
        closure = line_digraph_closure(transition_edges(self.bodies))
        self.assertEqual(
            (
                closure.hidden_states,
                closure.present_edges,
                closure.predicted_edges,
                closure.false_positive_edges,
            ),
            (1, 843, 6889, 6046),
        )

    def test_p_header_split_is_rank_one_but_low_precision(self) -> None:
        scores = all_line_digraph_triples(self.bodies)
        observed = next(
            score
            for score in scores
            if frozenset(score.training) == frozenset(P_MESSAGES)
        )
        self.assertEqual(
            (
                observed.hidden_states,
                observed.novel_predictions,
                observed.novel_truth,
                observed.hits,
            ),
            (16, 5377, 594, 496),
        )
        self.assertEqual(
            sum(score.f1 >= observed.f1 - 1e-15 for score in scores),
            1,
        )

    def test_rejected_phase_counts_are_frozen(self) -> None:
        score = raw_phase_score(raw_phase_indicators(MESSAGES))
        self.assertEqual(
            (
                score.totals,
                score.marker_hits,
                score.marker_positions,
                score.row_hits,
                score.row_positions,
            ),
            ((314, 312), (0, 3), 9, (16, 5), 34),
        )

    def test_affine_plane_observed_selections(self) -> None:
        score5 = affine_plane_selection(self.bodies, 5)
        score83 = affine_plane_selection(self.bodies, 83)
        self.assertEqual(
            (
                score5.natural_training,
                score5.natural_heldout,
                score5.selected_training,
                score5.selected_heldout,
            ),
            (1, 6, 6, 7),
        )
        self.assertEqual(
            (
                score83.natural_training,
                score83.natural_heldout,
                score83.selected_training,
                score83.selected_heldout,
            ),
            (0, 1, 0, 1),
        )

    def test_physical_actions_do_not_complete_a_context(self) -> None:
        score = physical_action_score(
            context_mappings()[6:], physical_action_candidates()
        )
        self.assertEqual(
            (
                score.candidates,
                score.common_support,
                score.per_context_supports,
                score.exact_contexts,
            ),
            (373, 5, (2, 2, 2, 1, 2, 2, 3), 0),
        )

    def test_header_transducer_is_not_top_ranked(self) -> None:
        scores = all_transducer_partition_scores()
        observed = next(
            score
            for partition, score in scores
            if frozenset(partition) == frozenset(HEADER_PARTITION)
        )
        unconditioned = raw_transducer_unconditioned_score()
        self.assertEqual(
            (observed.correct, observed.predictions),
            (626, 2601),
        )
        self.assertEqual(
            (unconditioned.correct, unconditioned.predictions),
            (628, 2601),
        )
        self.assertEqual(
            sum(score.accuracy >= observed.accuracy - 1e-15 for _, score in scores),
            81,
        )

    def test_raw_suffix_starts_are_frozen_by_existing_prefix_tree(self) -> None:
        self.assertEqual(
            raw_suffix_starts(),
            {
                "east1": 78,
                "west1": 78,
                "east2": 78,
                "west2": 21,
                "east3": 33,
                "west3": 21,
                "east4": 66,
                "west4": 66,
                "east5": 66,
            },
        )


if __name__ == "__main__":
    unittest.main()
