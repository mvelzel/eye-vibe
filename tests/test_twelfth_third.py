from __future__ import annotations

import unittest

from eye_mystery.ninth_causal import transition_edges
from eye_mystery.twelfth_novelty import context_mappings, eye_bodies
from eye_mystery.twelfth_third import (
    FIVE_ARY_FILTERS,
    apply_projective_mobius,
    convolutional_syndrome_count,
    fit_projective_mobius,
    leading_singular_energy_fraction,
    primitive_generator_supports,
    select_signed_projective_center,
    select_convolutional_filter,
)


class TwelfthThirdPrimitiveTests(unittest.TestCase):
    def test_disjoint_matching_has_one_over_n_spectral_fraction(self) -> None:
        edges = ((0, 3), (1, 4), (2, 5))
        self.assertAlmostEqual(
            leading_singular_energy_fraction(edges, alphabet_size=6),
            1 / 3,
        )

    def test_complete_rectangle_has_rank_one_spectral_fraction(self) -> None:
        edges = tuple((source, target) for source in range(2) for target in range(2, 5))
        self.assertAlmostEqual(
            leading_singular_energy_fraction(edges, alphabet_size=5),
            1.0,
        )

    def test_normalized_filter_family_has_124_unique_members(self) -> None:
        self.assertEqual(len(FIVE_ARY_FILTERS), 124)
        self.assertEqual(len(set(FIVE_ARY_FILTERS)), 124)
        self.assertTrue(
            all(
                coefficients[0] == 1 and coefficients[-1] != 0
                for coefficients in FIVE_ARY_FILTERS
            )
        )

    def test_planted_recurrence_has_only_zero_syndromes(self) -> None:
        # x[n] + x[n-1] = 0 mod 5.
        messages = {"planted": (1, 4, 1, 4, 1, 4)}
        score = convolutional_syndrome_count(
            (1, 1),
            ("planted",),
            messages=messages,
            starts={"planted": 1},
        )
        self.assertEqual((score.zeros, score.positions), (5, 5))

    def test_projective_fit_handles_infinity(self) -> None:
        # x -> 1/x swaps zero and infinity and fixes one.
        matrix = fit_projective_mobius(
            ((0, None), (None, 0), (1, 1)),
            41,
        )
        self.assertIsNotNone(matrix)
        assert matrix is not None
        self.assertIsNone(apply_projective_mobius(matrix, 0, 41))
        self.assertEqual(apply_projective_mobius(matrix, None, 41), 0)
        self.assertEqual(apply_projective_mobius(matrix, 1, 41), 1)


class TwelfthThirdCorpusTests(unittest.TestCase):
    def test_corpus_spectral_score_is_frozen(self) -> None:
        score = leading_singular_energy_fraction(
            transition_edges(eye_bodies())
        )
        self.assertAlmostEqual(score, 0.1513166097198497)

    def test_corpus_convolutional_selection_is_frozen(self) -> None:
        selected = select_convolutional_filter()
        self.assertEqual(selected.coefficients, (1, 2, 2, 1))
        self.assertEqual(
            (selected.training.zeros, selected.training.positions),
            (177, 726),
        )
        self.assertEqual(
            (selected.heldout.zeros, selected.heldout.positions),
            (385, 1875),
        )

    def test_signed_projective_generator_choices_are_coordinate_isomorphs(self) -> None:
        mappings = context_mappings()[6:]
        selected = select_signed_projective_center(mappings)
        self.assertEqual(
            selected,
            type(selected)(
                center=39,
                relation_sizes=(13, 13, 13, 6, 25, 25, 22),
                supports=(5, 5, 5, 4, 7, 7, 6),
            ),
        )
        support_vectors = primitive_generator_supports(
            mappings,
            selected.center,
        )
        self.assertEqual(len(support_vectors), 40)
        self.assertEqual(len(set(support_vectors)), 1)


if __name__ == "__main__":
    unittest.main()
