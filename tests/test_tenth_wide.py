from __future__ import annotations

import unittest

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.ninth_causal import transition_edges
from eye_mystery.tenth_wide import (
    DIFFERENTIAL_VARIANTS,
    branch_differential_score,
    context_graph_score,
    context_mappings,
    directed_color_refinement,
    in_faro_position,
    multiplicative_order,
    ordinal_cross_collisions,
    ordinal_pattern,
    out_faro_position,
    riffle_score,
    rising_sequences,
)


class TenthWideUnitTests(unittest.TestCase):
    def test_tie_aware_ordinal_pattern(self) -> None:
        self.assertEqual(ordinal_pattern((9, 2, 9, 4)), (2, 0, 2, 1))
        streams = {"a": (1, 4, 2), "b": (10, 40, 20), "c": (4, 1, 2)}
        self.assertEqual(
            ordinal_cross_collisions(
                streams,
                length=3,
                projection=("full", (0, 1, 2)),
            ),
            1,
        )

    def test_rising_sequences_count_descents_in_authored_order(self) -> None:
        mapping = {0: 0, 1: 2, 2: 4, 3: 1, 4: 3}
        self.assertEqual(rising_sequences(mapping, ((0, 1, 2), False)), 2)
        self.assertEqual(
            riffle_score((mapping,), convention=((0, 1, 2), False)).rising_sequences,
            2,
        )

    def test_84_card_out_faro_is_multiplication_by_two_mod_83(self) -> None:
        self.assertTrue(
            all(out_faro_position(position) == 2 * position % 83 for position in range(83))
        )
        self.assertEqual(out_faro_position(83), 83)
        self.assertEqual(multiplicative_order(2, 83), 82)
        self.assertNotEqual(in_faro_position(83), 83)

    def test_color_refinement_keeps_a_directed_cycle_in_one_class(self) -> None:
        score = directed_color_refinement(((0, 1), (1, 2), (2, 0)), alphabet_size=3)
        self.assertEqual(score.classes, 1)
        self.assertEqual(score.largest_class, 3)

    def test_constant_branch_difference_has_small_support(self) -> None:
        bodies = {
            "a": (0, 1, 2, 3),
            "b": (0, 1, 7, 8),
            "c": (0, 1, 12, 13),
        }
        score = branch_differential_score(bodies, "middle")
        self.assertEqual(score.branches, 1)
        self.assertLess(score.summed_support, score.observations)

    def test_context_cycle_rank_distinguishes_tree_and_triangle(self) -> None:
        tree = (
            ("a", "m1", 0, "m2", 0, 3),
            ("b", "m1", 0, "m3", 0, 3),
        )
        triangle = tree + (("c", "m2", 0, "m3", 0, 3),)
        self.assertEqual(context_graph_score(tree).cycle_rank, 0)
        self.assertEqual(context_graph_score(triangle).cycle_rank, 1)


class TenthWideCorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.streams = {
            name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
        }
        cls.bodies = {name: stream[1:] for name, stream in cls.streams.items()}

    def test_eye_context_graph_has_no_semantic_loop(self) -> None:
        score = context_graph_score()
        self.assertEqual(
            (score.vertices, score.edges, score.components, score.cycle_rank),
            (11, 7, 4, 0),
        )

    def test_corpus_diagnostics_are_well_formed(self) -> None:
        mappings = context_mappings(self.streams)
        self.assertEqual(tuple(map(len, mappings)), (13, 13, 13, 6, 25, 25, 22))
        refinement = directed_color_refinement(transition_edges(self.bodies))
        self.assertEqual(len(refinement.colors), 83)
        for variant in DIFFERENTIAL_VARIANTS:
            score = branch_differential_score(self.bodies, variant)
            self.assertEqual(score.branches, 5)
            self.assertGreater(score.observations, 0)


if __name__ == "__main__":
    unittest.main()
