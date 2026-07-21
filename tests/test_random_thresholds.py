import unittest

from eye_mystery.random_thresholds import (
    scan_blob_thresholds,
    successful_outcomes,
)


class RandomThresholdTests(unittest.TestCase):
    def test_finds_whitespace_variants_and_every_match(self) -> None:
        hits = scan_blob_thresholds(
            (
                (
                    "data/a.lua",
                    b"if Random(0,100) < 83 then end\n"
                    b"if Random ( 0, 100 ) <= 82 then end\n",
                ),
                ("data/b.lua", b"if Random(1,100) < 83 then end"),
            )
        )
        self.assertEqual(
            [(hit.path, hit.operator, hit.threshold) for hit in hits],
            [
                ("data/a.lua", "<", 83),
                ("data/a.lua", "<=", 82),
            ],
        )

    def test_83_branch_selects_the_visible_eye_range_exactly(self) -> None:
        outcomes = successful_outcomes("<", 83)
        self.assertEqual(outcomes, tuple(range(83)))
        self.assertEqual(len(outcomes), 83)

    def test_other_comparison_directions_use_the_same_inclusive_domain(self) -> None:
        self.assertEqual(successful_outcomes("<=", 0), (0,))
        self.assertEqual(successful_outcomes(">", 99), (100,))
        self.assertEqual(successful_outcomes(">=", 100), (100,))
        with self.assertRaises(ValueError):
            successful_outcomes("=", 50)


if __name__ == "__main__":
    unittest.main()
