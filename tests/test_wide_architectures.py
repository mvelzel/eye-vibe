import unittest

from eye_mystery.wide_architectures import (
    aligned_determinant_zero_count,
    best_affine_recurrence,
    best_affine_recurrence_from_counts,
    best_debruijn_overlap,
    debruijn_overlap_score,
    full_grid_hamming_chi_square,
    header_moment_scores,
    trigram_hamming_profile,
    trie_transition_counts,
)


class WideArchitectureTests(unittest.TestCase):
    def test_debruijn_overlap_recovers_a_literal_path(self) -> None:
        stream = (7, 38, 69)  # 012 -> 123 -> 234 in base five
        self.assertEqual(
            debruijn_overlap_score((stream,), (0, 1, 2)),
            (2, 2),
        )
        self.assertEqual(best_debruijn_overlap((stream,)).matches, 2)

    def test_base_five_hamming_profile_counts_changed_eyes(self) -> None:
        stream = (0, 1, 6, 32)  # 000, 001, 011, 112
        self.assertEqual(trigram_hamming_profile((stream,)), (2, 1, 0))
        self.assertGreater(
            full_grid_hamming_chi_square((2, 1, 0)),
            0,
        )

    def test_affine_recurrence_recovers_a_planted_stream(self) -> None:
        values = [4]
        for _ in range(20):
            values.append((2 * values[-1] + 3) % 83)
        result = best_affine_recurrence((tuple(values),))
        self.assertEqual(result.matches, 20)
        self.assertEqual((result.multiplier, result.translation), (2, 3))

    def test_trie_transition_counts_merge_only_copied_prefix_nodes(self) -> None:
        counts = trie_transition_counts(((1, 2, 3), (1, 2, 4), (1, 5)))
        self.assertEqual(
            counts,
            {(1, 2): 1, (2, 3): 1, (2, 4): 1, (1, 5): 1},
        )
        result = best_affine_recurrence_from_counts(counts, modulus=7)
        self.assertEqual(result.transitions, 4)

    def test_aligned_determinants_detect_dependent_rows(self) -> None:
        order = tuple(f"m{index}" for index in range(9))
        streams = {
            name: (1, 2, 3) if index < 6 else (2, 4, 6)
            for index, name in enumerate(order)
        }
        self.assertEqual(
            aligned_determinant_zero_count(
                streams, order, modulus=83, start=0
            ),
            (3, 3),
        )

    def test_polynomial_header_checksum_finds_fixed_rule(self) -> None:
        streams = {
            "a": (77, 1, 2, 3),
            "b": (68, 4, 5, 6),
        }
        scores = header_moment_scores(streams, moduli=(83,), degrees=(0,))
        negative = next(score for score in scores if score.sign == -1)
        self.assertEqual(negative.matches, 2)
        self.assertEqual(negative.matched_names, ("a", "b"))


if __name__ == "__main__":
    unittest.main()
