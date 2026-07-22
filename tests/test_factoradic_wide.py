from __future__ import annotations

import unittest

from eye_mystery.factoradic_wide import (
    PERMUTATIONS,
    canonical_streams,
    cycle_type,
    fold_product,
    mapped_bodies,
    moving_delimiter_scores,
    quotient,
    wide_scores,
)
from eye_mystery.factoradic_headers import compose, inverse


class FactoradicWideTests(unittest.TestCase):
    def test_body_relabeling_preserves_headers_and_lengths(self) -> None:
        streams = canonical_streams()
        mapping = tuple(reversed(range(83)))
        bodies = mapped_bodies(streams, mapping)
        for name, stream in streams.items():
            self.assertEqual(len(bodies[name]), len(stream) - 1)
            self.assertEqual(bodies[name][0], mapping[stream[1]])

    def test_product_and_quotient_conventions(self) -> None:
        left = PERMUTATIONS[50]
        right = PERMUTATIONS[36]
        self.assertEqual(fold_product((50, 36), act_left=True), compose(right, left))
        self.assertEqual(fold_product((50, 36), act_left=False), compose(left, right))
        self.assertEqual(quotient(left, right, 2), inverse(quotient(left, right, 0)))

    def test_cycle_type_includes_fixed_points(self) -> None:
        self.assertEqual(cycle_type((0, 2, 1, 3, 5, 4)), (2, 2, 1, 1))

    def test_observed_wide_fixture(self) -> None:
        streams = canonical_streams()
        result = wide_scores(streams, tuple(range(83)))
        self.assertEqual(result.quotients.transitions, 1018)
        self.assertEqual(result.cosets.transitions, 1018)
        self.assertGreaterEqual(result.running_state_distinct, 9)
        delimiters = moving_delimiter_scores()
        self.assertEqual(tuple(row.direction for row in delimiters), ("forward", "inverse"))
        self.assertTrue(all(row.rows > 80 for row in delimiters))


if __name__ == "__main__":
    unittest.main()
