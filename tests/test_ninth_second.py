from __future__ import annotations

import unittest
from random import Random

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.ninth_causal import equality_signature
from eye_mystery.ninth_second import (
    FIRST_CONTEXTS,
    KEY_PHRASE,
    LAST_CONTEXTS,
    TRAILER_ALPHABET,
    affine_body_permutations,
    audit_category_pair,
    best_carry_markov_score,
    borrow_state,
    carry_context_score,
    carry_held_out_score,
    category_tape,
    checksum_preserving_body_permutation,
    isomorphic_suffix_prefix,
    keyed_alphabet,
    literal_suffix_prefix,
    overlap_weights,
    permute_body_labels,
    trailer_categories,
    transition_feature_context_score,
    transition_feature_held_out_score,
    transition_feature_state,
)


class NinthSecondUnitTests(unittest.TestCase):
    def test_keyed_alphabet_and_categories_partition_a_to_z_zero_to_nine(self) -> None:
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        self.assertEqual(keyed_alphabet(KEY_PHRASE, alphabet), TRAILER_ALPHABET)
        for q_on_back in (False, True):
            groups = trailer_categories(q_on_back=q_on_back)
            self.assertEqual(set().union(*groups), set(alphabet))
            self.assertEqual(sum(map(len, groups)), len(alphabet))

    def test_documented_funny_obstacle_examples_do_not_preserve_categories(self) -> None:
        groups = trailer_categories()
        expected = {
            ("EAST", "WEST"): (0,),
            ("COPPER", "SILVER"): (0, 1, 3),
            ("FROZEN", "MOLTEN"): (0, 1, 3),
        }
        for pair, mismatches in expected.items():
            self.assertEqual(audit_category_pair(*pair, groups).mismatches, mismatches)
        self.assertEqual(len(set(category_tape("0123456789", groups))), 1)

    def test_borrow_bits_follow_the_selected_processing_order(self) -> None:
        # 20=(0,4,0), 6=(0,1,1): processing middle then low borrows once,
        # then the incoming borrow is absorbed by the low digit.
        self.assertEqual(borrow_state(20, 6, (1, 2, 0), reverse=False), 1)
        self.assertEqual(borrow_state(20, 6, (1, 2, 0), reverse=True), 2)

    def test_independent_comparison_ablation_removes_borrow_propagation(self) -> None:
        self.assertEqual(
            transition_feature_state(
                25,
                0,
                (0, 2, 1),
                reverse=False,
                variant="borrow_pair",
            ),
            3,
        )
        self.assertEqual(
            transition_feature_state(
                25,
                0,
                (0, 2, 1),
                reverse=False,
                variant="independent_pair",
            ),
            1,
        )

    def test_suffix_prefix_overlap_requires_real_equality_evidence(self) -> None:
        left = (5, 1, 2, 1, 2, 3)
        right = (9, 8, 9, 8, 7, 6)
        self.assertEqual(literal_suffix_prefix(left, right), 0)
        self.assertEqual(isomorphic_suffix_prefix(left, right), 5)
        self.assertEqual(
            isomorphic_suffix_prefix((1, 2, 3, 4), (8, 7, 6, 5)), 0
        )


class NinthSecondCorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.streams = {
            name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
        }
        cls.bodies = {name: cls.streams[name][1:] for name in MESSAGE_ORDER}

    def test_carry_scores_are_stable(self) -> None:
        overall = carry_context_score(self.streams)
        first_to_last = carry_held_out_score(
            self.streams, FIRST_CONTEXTS, LAST_CONTEXTS
        )
        last_to_first = carry_held_out_score(
            self.streams, LAST_CONTEXTS, FIRST_CONTEXTS
        )
        markov = best_carry_markov_score(self.streams)
        self.assertEqual(
            (overall.matches, overall.comparisons, overall.convention),
            (63, 141, ((0, 2, 1), True)),
        )
        self.assertEqual(
            (
                first_to_last.train.matches,
                first_to_last.test.matches,
                first_to_last.train.convention,
            ),
            (27, 35, ((2, 0, 1), True)),
        )
        self.assertEqual(
            (
                last_to_first.train.matches,
                last_to_first.test.matches,
                last_to_first.train.convention,
            ),
            (38, 22, ((0, 2, 1), False)),
        )
        self.assertAlmostEqual(markov.gain, 153.962785, places=5)

    def test_digit_feature_ablation_scores_are_stable(self) -> None:
        expected = {
            "borrow_pair": (63, 35, ((0, 2, 1), True)),
            "borrow_first": (90, 51, ((0, 1, 2), False)),
            "borrow_second": (91, 46, ((0, 2, 1), False)),
            "borrow_triple": (31, 15, ((0, 2, 1), True)),
            "independent_pair": (63, 35, ((0, 2, 1), True)),
            "change_pair": (76, 45, ((1, 2, 0), False)),
        }
        for variant, (overall_matches, held_matches, convention) in expected.items():
            overall = transition_feature_context_score(self.streams, variant)
            held = transition_feature_held_out_score(
                self.streams,
                variant,
                FIRST_CONTEXTS,
                LAST_CONTEXTS,
            )
            self.assertEqual(overall.matches, overall_matches)
            self.assertEqual(held.test.matches, held_matches)
            self.assertEqual(overall.convention, convention)
        self.assertEqual(
            transition_feature_held_out_score(
                self.streams,
                "independent_pair",
                FIRST_CONTEXTS,
                LAST_CONTEXTS,
            ).train.convention,
            ((0, 2, 1), True),
        )

    def test_body_label_control_keeps_headers_and_equality(self) -> None:
        permutation = tuple(reversed(range(83)))
        control = permute_body_labels(self.streams, permutation)
        for name in MESSAGE_ORDER:
            self.assertEqual(control[name][0], self.streams[name][0])
            self.assertEqual(
                equality_signature(control[name][1:]),
                equality_signature(self.streams[name][1:]),
            )

    def test_matched_control_preserves_diagonal_sums_and_marker_labels(self) -> None:
        permutation = checksum_preserving_body_permutation(
            self.streams, Random(20260722)
        )
        control = permute_body_labels(self.streams, permutation)
        for name in ("east1", "east3", "east5"):
            self.assertEqual(sum(control[name]), sum(self.streams[name]))
        for name in MESSAGE_ORDER:
            marker = self.streams[name][0]
            self.assertEqual(permutation[marker], marker)

    def test_affine_control_family_is_complete(self) -> None:
        controls = affine_body_permutations()
        self.assertEqual(len(controls), 82 * 83)
        self.assertEqual(len(set(controls)), 82 * 83)

    def test_no_direct_worldline_overlap_exists_between_any_panels(self) -> None:
        literal = overlap_weights(self.bodies, isomorphic=False)
        isomorphic = overlap_weights(self.bodies, isomorphic=True)
        self.assertEqual(max(literal.values()), 0)
        self.assertEqual(max(isomorphic.values()), 0)


if __name__ == "__main__":
    unittest.main()
