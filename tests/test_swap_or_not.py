from __future__ import annotations

import unittest

from eye_mystery.affine_embedding import Context
from eye_mystery.swap_or_not import (
    audit_endpoint_fit,
    edge_matches_forms,
    endpoint_forms,
)


class SwapOrNotTest(unittest.TestCase):
    def test_endpoint_forms_match_three_round_expansion(self) -> None:
        forms = endpoint_forms((5, 17, 42))
        self.assertEqual(
            forms,
            {
                (1, 0),
                (-1, 5),
                (-1, 17),
                (1, 12),
                (-1, 42),
                (1, 37),
                (1, 25),
                (-1, 30),
            },
        )

    def test_planted_endpoint_context_is_recovered(self) -> None:
        keys = (5, 17)
        forms = tuple(endpoint_forms(keys))
        pairs = tuple(
            (left, (sign * left + constant) % 83)
            for left, (sign, constant) in zip(range(4), forms)
        )
        audit = audit_endpoint_fit(Context("plant", pairs), 2)
        self.assertTrue(audit.compatible)
        self.assertGreater(audit.full_key_tuples, 0)

    def test_incompatible_edges_fail_relaxed_endpoint_test(self) -> None:
        context = Context("negative", ((0, 1), (1, 3), (2, 7), (3, 12)))
        audit = audit_endpoint_fit(context, 1)
        self.assertFalse(audit.compatible)
        self.assertEqual(audit.full_key_tuples, 0)

    def test_edge_match_uses_visible_modular_coordinates(self) -> None:
        self.assertTrue(edge_matches_forms(80, 2, {(1, 5)}))
        self.assertTrue(edge_matches_forms(80, 8, {(-1, 5)}))
        self.assertFalse(edge_matches_forms(80, 9, {(-1, 5)}))


if __name__ == "__main__":
    unittest.main()
