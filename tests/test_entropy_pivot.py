import math
import unittest

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.entropy_pivot import (
    best_period_scan,
    exact_pivot_rows,
    glyph_projections,
    lag_autocorrelation,
    lag_match_count,
    mod_five_counts,
    period_scan_control,
    rolling_entropies,
    shannon_entropy,
    shuffle_glyph_positions,
)


class EntropyPivotTests(unittest.TestCase):
    def test_entropy_known_distributions(self) -> None:
        self.assertEqual(shannon_entropy((0, 0, 0, 0, 0)), 0.0)
        self.assertAlmostEqual(shannon_entropy((0, 1, 2, 3, 4)), math.log2(5))

    def test_window_five_entropy_has_only_partition_values(self) -> None:
        possible = {
            round(shannon_entropy(values), 12)
            for values in (
                (0, 0, 0, 0, 0),
                (0, 0, 0, 0, 1),
                (0, 0, 0, 1, 1),
                (0, 0, 0, 1, 2),
                (0, 0, 1, 1, 2),
                (0, 0, 1, 2, 3),
                (0, 1, 2, 3, 4),
            )
        }
        for message in MESSAGES.values():
            self.assertTrue(
                {round(value, 12) for value in rolling_entropies(message, 5)}
                <= possible
            )

    def test_no_universal_entropy_collapse_at_index_25(self) -> None:
        for streams in (
            MESSAGES,
            {
                name: tuple(value % 5 for value in trigram_values(MESSAGES[name]))
                for name in MESSAGE_ORDER
            },
        ):
            changes = []
            for name in MESSAGE_ORDER:
                entropy = rolling_entropies(streams[name], 5)
                changes.append(entropy[25] - entropy[24])
            self.assertTrue(any(change >= 0 for change in changes))
            self.assertTrue(any(change != changes[0] for change in changes[1:]))

    def test_helpers(self) -> None:
        self.assertEqual(mod_five_counts((0, 1, 2, 3, 4, 5)), (2, 1, 1, 1, 1))
        self.assertAlmostEqual(lag_autocorrelation((0, 1, 2, 0, 1, 2), 3), 1.0)
        self.assertEqual(
            lag_match_count((0, 1, 0, 1, 0), start=0, stop=5, lag=2),
            3,
        )

    def test_exact_index_25_claim_fails_every_natural_projection(self) -> None:
        projections = glyph_projections(MESSAGES)
        for streams in projections.values():
            rows = exact_pivot_rows(streams)
            self.assertFalse(all(row.uniform for row in rows.values()))
            self.assertFalse(all(row.periodic for row in rows.values()))

    def test_period_scan_reselects_projection_lag_and_cut(self) -> None:
        projections = {
            "bad": {
                name: tuple(
                    (index // 2 + MESSAGE_ORDER.index(name)) % 5
                    for index in range(50)
                )
                for name in MESSAGE_ORDER
            },
            "planted": {
                name: tuple(range(15)) + (0, 1, 2, 3, 4) * 7
                for name in MESSAGE_ORDER
            },
        }
        best = best_period_scan(
            projections,
            lags=(2, 5),
            minimum_cut=5,
            block_length=25,
        )
        self.assertEqual((best.projection, best.lag, best.cut), ("planted", 5, 15))
        self.assertEqual(best.matches, best.comparisons)

    def test_shuffle_preserves_complete_glyph_multisets(self) -> None:
        from random import Random

        shuffled = shuffle_glyph_positions(MESSAGES, Random(1))
        for name in MESSAGE_ORDER:
            before = tuple(
                MESSAGES[name][offset : offset + 3]
                for offset in range(0, len(MESSAGES[name]), 3)
            )
            after = tuple(
                shuffled[name][offset : offset + 3]
                for offset in range(0, len(shuffled[name]), 3)
            )
            self.assertCountEqual(before, after)

    def test_control_is_deterministic(self) -> None:
        observed, controls = period_scan_control(
            MESSAGES,
            lags=(5,),
            trials=3,
            seed=7,
        )
        self.assertEqual((observed.projection, observed.lag, observed.cut), ("first_eye", 5, 42))
        self.assertEqual(observed.matches, 62)
        self.assertEqual(controls, (62, 65, 65))


if __name__ == "__main__":
    unittest.main()
