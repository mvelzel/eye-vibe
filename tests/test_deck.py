import unittest

from eye_mystery.deck import (
    move_to_back_decode,
    move_to_front_decode,
    reverse_prefix_decode,
    ranks_to_labels,
    rotate_to_front_decode,
    swap_with_front_decode,
    transpose_decode,
)


class DeckTests(unittest.TestCase):
    def test_move_to_front(self) -> None:
        self.assertEqual(move_to_front_decode([2, 2, 1], range(4)), (2, 0, 2))

    def test_move_to_back(self) -> None:
        self.assertEqual(move_to_back_decode([2, 2, 1], range(4)), (2, 3, 1))

    def test_transpose(self) -> None:
        self.assertEqual(transpose_decode([2, 2, 1], range(4)), (2, 1, 2))

    def test_swap_with_front(self) -> None:
        self.assertEqual(swap_with_front_decode([2, 2, 1], range(4)), (2, 0, 1))

    def test_reverse_prefix(self) -> None:
        self.assertEqual(reverse_prefix_decode([2, 2, 1], range(4)), (2, 0, 1))

    def test_rotate_to_front(self) -> None:
        self.assertEqual(rotate_to_front_decode([2, 2, 1], range(4)), (2, 0, 3))

    def test_rank_instruction_inverse(self) -> None:
        labels = [2, 2, 1]
        ranks = move_to_front_decode(labels, range(4))
        self.assertEqual(ranks_to_labels(ranks, range(4), "move-to-front"), tuple(labels))


if __name__ == "__main__":
    unittest.main()
