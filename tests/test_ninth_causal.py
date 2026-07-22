from __future__ import annotations

import random
import unittest
from collections import Counter

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.ninth_causal import (
    CONTEXT_SPECS,
    _hungarian_minimum,
    body_streams,
    boolean_rank_small_rows,
    branch_influence_score,
    common_base_score,
    degree_preserving_edge_swaps,
    forbidden_support_score,
    header_conditional_score,
    message_automorphisms,
    partial_bijection_iff_same_equality_signature,
    synchronization_profile,
    three_by_three_partitions,
    transition_edges,
)
from eye_mystery.progression_certificate import context_mapping


class NinthCausalUnitTests(unittest.TestCase):
    def test_hungarian_assignment_is_global_not_greedy(self) -> None:
        costs = ((0, 1, 1), (0, 9, 9), (9, 0, 9))
        assignment = _hungarian_minimum(costs)
        self.assertEqual(
            sum(costs[row][column] for row, column in enumerate(assignment)),
            1,
        )

    def test_partial_bijection_is_exactly_equality_isomorphism(self) -> None:
        self.assertTrue(
            partial_bijection_iff_same_equality_signature(
                (8, 2, 8, 5, 2), (7, 1, 7, 9, 1)
            )
        )
        conflict = synchronization_profile((8, 2, 8), (7, 1, 9))
        self.assertEqual(conflict.first_conflict, 2)
        self.assertTrue(
            partial_bijection_iff_same_equality_signature(
                (8, 2, 8), (7, 1, 9)
            )
        )

    def test_small_boolean_rank_is_exact(self) -> None:
        # Three unit rows require three rectangles; two identical rows need one.
        self.assertEqual(boolean_rank_small_rows((0b001, 0b010, 0b100)), 3)
        self.assertEqual(boolean_rank_small_rows((0b101, 0b101)), 1)

    def test_directed_swaps_preserve_degrees_and_no_loops(self) -> None:
        edges = frozenset(((0, 1), (0, 2), (1, 2), (2, 0), (3, 0), (3, 1)))
        shuffled = degree_preserving_edge_swaps(
            edges, random.Random(12), attempts=1000
        )
        self.assertFalse(any(left == right for left, right in shuffled))
        self.assertEqual(
            Counter(left for left, _ in edges),
            Counter(left for left, _ in shuffled),
        )
        self.assertEqual(
            Counter(right for _, right in edges),
            Counter(right for _, right in shuffled),
        )

    def test_three_by_three_partitions_are_unique(self) -> None:
        partitions = three_by_three_partitions(tuple("abcdefghi"))
        normalized = {
            frozenset(partition) for partition in partitions
        }
        self.assertEqual((len(partitions), len(normalized)), (280, 280))


class NinthCausalCorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.streams = {
            name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
        }
        cls.bodies = body_streams(cls.streams)
        cls.mappings = tuple(
            context_mapping(left, left_start, right, right_start, length)
            for _, left, left_start, right, right_start, length in CONTEXT_SPECS
        )

    def test_common_base_identity_mass_and_decontaminated_score(self) -> None:
        all_contexts = common_base_score(self.mappings)
        nonliteral = common_base_score(self.mappings[6:])
        self.assertEqual(
            (all_contexts.agreements, all_contexts.edges), (108, 209)
        )
        self.assertEqual(
            (nonliteral.agreements, nonliteral.edges), (36, 117)
        )

    def test_branch_influence_is_full_rank_and_not_nested(self) -> None:
        score = branch_influence_score(self.bodies)
        self.assertEqual(
            (
                score.branches,
                score.active_columns,
                score.gf2_rank,
                score.boolean_rank,
                score.nested_pairs,
            ),
            (5, 54, 5, 5, 0),
        )

    def test_equality_skeleton_has_no_message_symmetry(self) -> None:
        self.assertEqual(len(message_automorphisms(self.bodies, truncate=False)), 1)
        self.assertEqual(len(message_automorphisms(self.bodies, truncate=True)), 1)

    def test_forbidden_support_is_high_rank(self) -> None:
        score = forbidden_support_score(transition_edges(self.bodies))
        self.assertEqual(
            (
                score.present_edges,
                score.absent_rank,
                score.distinct_absent_rows,
                score.row_pattern_lower_bound,
            ),
            (843, 82, 83, 7),
        )

    def test_header_classes_do_not_improve_held_out_prediction(self) -> None:
        score = header_conditional_score(self.bodies)
        self.assertAlmostEqual(score.observed_gain, -3.408916, places=5)
        self.assertEqual(
            (score.at_least_observed, score.partitions), (2, 280)
        )
        self.assertLess(score.best_gain, 0.0)


if __name__ == "__main__":
    unittest.main()
