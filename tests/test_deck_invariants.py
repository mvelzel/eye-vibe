import unittest

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.deck_invariants import (
    forced_adaptive_rank_count,
    repeated_working_set_ranks,
)


class DeckInvariantTests(unittest.TestCase):
    def test_working_set_ranks(self) -> None:
        self.assertEqual(
            repeated_working_set_ranks((1, 2, 3, 2, 1)),
            (1, 2),
        )

    def test_eye_rank_lower_bound_is_label_invariant(self) -> None:
        messages = tuple(
            trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
        )
        self.assertEqual(forced_adaptive_rank_count(messages), 59)
        self.assertEqual(
            forced_adaptive_rank_count(messages, skip_first=True), 59
        )


if __name__ == "__main__":
    unittest.main()
