import unittest

from eye_mystery.body_bwt import (
    body_bwt_null_counts,
    concatenate_bodies,
    eye_bodies,
    lf_cycle_lengths,
    single_cycle_deletions,
)


class BodyBwtTests(unittest.TestCase):
    def test_canonical_bodies_have_one_fixed_point(self) -> None:
        stream = concatenate_bodies(eye_bodies())
        self.assertEqual(len(stream), 1027)
        self.assertEqual(lf_cycle_lengths(stream), (1026, 1))
        self.assertEqual(
            single_cycle_deletions(),
            (
                (440, "east3", 22, 74),
                (483, "east3", 65, 70),
                (841, "west4", 46, 66),
            ),
        )

    def test_seeded_structure_preserving_null(self) -> None:
        self.assertEqual(
            body_bwt_null_counts(),
            {
                "trials": 10_000,
                "max_cycle_at_least_observed": 15,
                "exact_observed_cycles": 10,
                "single_cycle": 5,
            },
        )


if __name__ == "__main__":
    unittest.main()
