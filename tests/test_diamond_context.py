import unittest

from eye_mystery.diamond_context import (
    HELDOUT_CONTEXTS,
    TRAIN_CONTEXTS,
    accepted_streams,
    context_quotient_score,
    permuted_streams,
    quotient_values,
    rank_digits,
    split_score,
)


class DiamondContextTests(unittest.TestCase):
    def test_rank_digits_use_natural_base_five_coordinate(self) -> None:
        self.assertEqual(rank_digits(0), (0, 0, 0))
        self.assertEqual(rank_digits(31), (1, 1, 1))
        self.assertEqual(rank_digits(82), (3, 1, 2))

    def test_squared_quotient_collapses_planted_changed_pair(self) -> None:
        # (y=111,x=000) and (y=000,x=111) both emit (1,1,1).
        streams = {
            "left": (31, 0),
            "right": (0, 31),
        }
        spec = ("plant", "left", 0, "right", 0, 2)
        score = context_quotient_score(streams, spec)
        self.assertEqual(score.agreements, 3)
        self.assertEqual(score.eligible_coordinates, 3)
        self.assertTrue(score.exact)
        self.assertEqual(
            context_quotient_score(
                streams,
                spec,
                transform="base25",
            ).agreements,
            0,
        )

    def test_fully_copied_pair_is_excluded(self) -> None:
        streams = {
            "left": (31, 0),
            "right": (31, 0),
        }
        score = context_quotient_score(
            streams,
            ("copy", "left", 0, "right", 0, 2),
        )
        self.assertEqual(score.agreements, 0)
        self.assertEqual(score.eligible_coordinates, 0)
        self.assertFalse(score.exact)

    def test_odd_record_uses_authored_zero_pad(self) -> None:
        self.assertEqual(quotient_values((31,), transform="squared"), (1, 1, 1))

    def test_global_relabel_preserves_every_stream_equality(self) -> None:
        streams = accepted_streams()
        permutation = tuple(reversed(range(83)))
        relabelled = permuted_streams(streams, permutation)
        for name, stream in streams.items():
            for left in range(len(stream)):
                for right in range(left + 1, len(stream)):
                    self.assertEqual(
                        stream[left] == stream[right],
                        relabelled[name][left] == relabelled[name][right],
                    )

    def test_real_context_splits_have_nontrivial_denominators(self) -> None:
        streams = accepted_streams()
        training = split_score(streams, TRAIN_CONTEXTS)
        heldout = split_score(streams, HELDOUT_CONTEXTS)
        self.assertGreater(training.eligible_coordinates, 0)
        self.assertGreater(heldout.eligible_coordinates, 0)


if __name__ == "__main__":
    unittest.main()

