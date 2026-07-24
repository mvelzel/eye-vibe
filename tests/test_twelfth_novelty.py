from __future__ import annotations

import unittest

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES
from eye_mystery.factoradic_headers import compose
from eye_mystery.twelfth_novelty import (
    ADJACENT_S6,
    EDGE_ORIENTATIONS,
    IDENTITY_S6,
    apply_mobius,
    context_mappings,
    coxeter_scan,
    edge_path_score,
    edge_path_split,
    eye_bodies,
    eye_streams,
    fit_mobius,
    hodge_features,
    hodge_score,
    interpolate_polynomial,
    maximum_mobius_support,
    polynomial_share_score,
    projective_context_score,
)


class TwelfthNoveltyPrimitiveTests(unittest.TestCase):
    def test_mobius_fit_recovers_planted_map(self) -> None:
        prime = 83
        planted = (7, 11, 3, 5)
        sources = (1, 4, 12, 31, 72)
        mapping = {
            source: apply_mobius(planted, source, prime)
            for source in sources
        }
        self.assertNotIn(None, mapping.values())
        fitted = fit_mobius(tuple(mapping.items())[:3], prime)
        self.assertIsNotNone(fitted)
        self.assertEqual(
            tuple(apply_mobius(fitted, source, prime) for source in sources),
            tuple(mapping.values()),
        )
        support, _ = maximum_mobius_support(mapping, prime)
        self.assertEqual(support, len(mapping))

    def test_adjacent_generators_obey_coxeter_relations(self) -> None:
        for generator in ADJACENT_S6:
            self.assertEqual(compose(generator, generator), IDENTITY_S6)
        self.assertEqual(
            compose(ADJACENT_S6[0], ADJACENT_S6[2]),
            compose(ADJACENT_S6[2], ADJACENT_S6[0]),
        )
        left = compose(
            ADJACENT_S6[0],
            compose(ADJACENT_S6[1], ADJACENT_S6[0]),
        )
        right = compose(
            ADJACENT_S6[1],
            compose(ADJACENT_S6[0], ADJACENT_S6[1]),
        )
        self.assertEqual(left, right)

    def test_directed_edge_path_recovers_planted_joins(self) -> None:
        # 1->2, 2->3, 3->4 in row-major edge numbering.
        bodies = {"planted": (11, 21, 31)}
        score = edge_path_score(bodies, (False, False, False))
        self.assertEqual((score.joins, score.eligible), (2, 2))

    def test_polynomial_interpolation_recovers_quadratic(self) -> None:
        prime = 83
        xs = (2, 7, 13, 29)
        ys = tuple((5 + 3 * x + 11 * x * x) % prime for x in xs)
        self.assertEqual(interpolate_polynomial(xs, ys, prime), (5, 3, 11))

    def test_constant_field_has_zero_hodge_stencil(self) -> None:
        field = {
            (2 * column + row % 2, row): 0
            for row in range(6)
            for column in range(8)
        }
        features = hodge_features(field)
        self.assertTrue(features)
        self.assertEqual(set(features.values()), {(0, 0)})


class TwelfthNoveltyCorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.streams = eye_streams()
        cls.bodies = eye_bodies()

    def test_projective_support_is_prefix_contaminated_then_weak(self) -> None:
        mappings = context_mappings()
        all_score = projective_context_score(mappings, 83)
        tail_score = projective_context_score(mappings[6:], 83)
        self.assertEqual(
            all_score.maximum_supports,
            (20, 20, 5, 5, 18, 18, 4, 4, 4, 3, 6, 5, 5),
        )
        self.assertEqual(tail_score.maximum_supports, (4, 4, 4, 3, 6, 5, 5))
        self.assertEqual(tail_score.exact_contexts, 0)

    def test_header_conditioned_coxeter_frozen_scores(self) -> None:
        score = coxeter_scan()
        self.assertEqual(
            score.natural_context_scores,
            (1, 3, 0, 0, 5, 8, 0, 0, 1, 0, 0, 3, 3),
        )
        self.assertEqual(
            score.natural_distinct_states,
            (26, 23, 25, 25, 27, 28, 25, 25, 26),
        )
        self.assertEqual(
            (
                score.best_total,
                score.selected_training,
                score.selected_heldout,
            ),
            (27, 20, 4),
        )

    def test_natural_nine_edge_path_counts(self) -> None:
        split = edge_path_split(self.bodies)
        self.assertEqual(len(split.all_scores), len(EDGE_ORIENTATIONS))
        self.assertEqual(
            (
                split.selected_orientation,
                split.training_joins,
                split.training_eligible,
                split.heldout_joins,
                split.heldout_eligible,
            ),
            ((False, False, False), 50, 388, 75, 589),
        )

    def test_polynomial_share_histograms(self) -> None:
        markers = {name: self.streams[name][0] for name in MESSAGE_ORDER}
        self.assertEqual(
            polynomial_share_score(
                self.bodies, markers, 83
            ).degree_histogram,
            ((7, 2), (8, 71)),
        )
        self.assertEqual(
            polynomial_share_score(
                self.bodies, markers, 101
            ).degree_histogram,
            ((7, 1), (8, 72)),
        )

    def test_hodge_corpus_score_is_frozen(self) -> None:
        score = hodge_score(MESSAGES)
        self.assertEqual(
            (
                score.vertices,
                score.distinct_features,
                score.zero_features,
                score.nontrivial_aligned_pairs,
                score.aligned_feature_agreements,
            ),
            (2274, 94, 112, 8302, 228),
        )


if __name__ == "__main__":
    unittest.main()
