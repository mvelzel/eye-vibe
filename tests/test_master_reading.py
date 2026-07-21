import unittest

from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER
from eye_mystery.master_reading import master_rule_values, visual_triangles
from eye_mystery.metrics import adjacent_doubles


class MasterReadingTests(unittest.TestCase):
    def test_visual_reconstruction_and_validation(self) -> None:
        self.assertEqual(visual_triangles((2, 0, 3, 1, 4, 2)), ((2, 3, 0), (4, 2, 1)))
        with self.assertRaises(ValueError):
            visual_triangles((0, 1))

    def test_published_transform_realizes_all_125_values(self) -> None:
        streams = tuple(master_rule_values(MESSAGES[name]) for name in MESSAGE_ORDER)
        self.assertEqual(
            tuple(stream[0] for stream in streams),
            (4, 8, 46, 28, 99, 56, 101, 103, 81),
        )
        self.assertEqual(
            {value for stream in streams for value in stream},
            set(range(125)),
        )
        self.assertEqual(adjacent_doubles(streams), 9)
        downward = {value for stream in streams for value in stream[::2]}
        upward = {value for stream in streams for value in stream[1::2]}
        self.assertEqual((len(downward), len(upward), len(downward & upward)), (83, 83, 41))


if __name__ == "__main__":
    unittest.main()
