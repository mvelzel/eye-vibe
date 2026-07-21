import unittest

from eye_mystery.deck_selected import (
    ACTIONS,
    decode_base_selected_action,
    selected_action_indices,
)


class SelectedCardDeckTests(unittest.TestCase):
    def test_action_indices_are_permutations(self) -> None:
        for action in ACTIONS:
            for rank in range(7):
                self.assertEqual(
                    tuple(sorted(selected_action_indices(7, action, rank))),
                    tuple(range(7)),
                )

    def test_identity_base_examples(self) -> None:
        labels = (2, 2, 1)
        expected = {
            "move-to-front": (2, 0, 2),
            "move-to-back": (2, 3, 1),
            "cut-to-card": (2, 0, 3),
            "cut-after-card": (2, 3, 2),
            "reverse-prefix": (2, 0, 1),
            "reverse-suffix": (2, 3, 1),
        }
        for action, plaintext in expected.items():
            self.assertEqual(
                decode_base_selected_action(labels, range(4), action),
                plaintext,
            )

    def test_nontrivial_base_is_applied_before_selection(self) -> None:
        self.assertEqual(
            decode_base_selected_action((0, 2), (1, 2, 3, 0), "move-to-front"),
            (3, 1),
        )


if __name__ == "__main__":
    unittest.main()
