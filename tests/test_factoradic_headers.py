from __future__ import annotations

import unittest

from eye_mystery.factoradic_headers import (
    TARGET_NEWLINE_PREIMAGES,
    graph_conditioned_audit,
    header_ranks,
    inverse,
    is_p_d4_event,
    lexicographic_unrank,
    observed_signature,
)


class FactoradicHeaderTests(unittest.TestCase):
    def test_header_ranks_come_directly_from_canonical_corpus(self) -> None:
        self.assertEqual(
            tuple(header_ranks().values()),
            (50, 80, 36, 76, 63, 34, 27, 77, 33),
        )

    def test_lexicographic_unranking_examples(self) -> None:
        self.assertEqual(lexicographic_unrank(0), (0, 1, 2, 3, 4, 5))
        self.assertEqual(lexicographic_unrank(50), (0, 3, 1, 4, 2, 5))
        self.assertEqual(lexicographic_unrank(719), (5, 4, 3, 2, 1, 0))

    def test_observed_p_and_q_signature(self) -> None:
        signature = observed_signature()
        self.assertTrue(
            is_p_d4_event(
                dict(
                    zip(
                        ("east1", "west1", "east2"),
                        signature.permutations[:3],
                        strict=True,
                    )
                )
            )
        )
        self.assertEqual(inverse(signature.permutations[0]), signature.permutations[2])
        self.assertEqual(signature.p_group_order, 8)
        self.assertEqual(signature.p_group_ranks, (0, 6, 26, 36, 50, 60, 80, 86))
        self.assertEqual(signature.q_group_order, 120)
        self.assertEqual(signature.newline_preimages, TARGET_NEWLINE_PREIMAGES)
        self.assertEqual((signature.east_q_cosets, signature.west_q_cosets), (3, 1))

    def test_graph_conditioned_enumeration(self) -> None:
        audit = graph_conditioned_audit()
        self.assertEqual(
            (
                audit.all_assignments,
                audit.in_range,
                audit.distinct_ranks,
                audit.typed,
                audit.p_d4,
                audit.q_s5,
                audit.p_d4_and_q_s5,
                audit.full,
            ),
            (22680, 15120, 12096, 6, 136, 80, 4, 2),
        )
        self.assertEqual(
            audit.survivors,
            (
                (0, 0, 1, 1, 3, 4, 2, 2, 3),
                (0, 0, 1, 2, 3, 4, 2, 1, 3),
            ),
        )


if __name__ == "__main__":
    unittest.main()
