import math
import unittest

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.entropy_pivot import (
    lag_autocorrelation,
    mod_five_counts,
    rolling_entropies,
    shannon_entropy,
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


if __name__ == "__main__":
    unittest.main()
