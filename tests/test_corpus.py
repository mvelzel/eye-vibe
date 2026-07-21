import unittest

from eye_mystery.corpus import (
    MESSAGES,
    MESSAGE_ORDER,
    ROW_PAIR_TRIGRAM_LENGTHS,
    trigram_values,
)
from eye_mystery.metrics import adjacent_doubles, common_prefix_length


class CorpusTests(unittest.TestCase):
    def test_visual_row_pair_lengths_partition_messages(self) -> None:
        self.assertEqual(set(ROW_PAIR_TRIGRAM_LENGTHS), set(MESSAGE_ORDER))
        for name in MESSAGE_ORDER:
            lengths = ROW_PAIR_TRIGRAM_LENGTHS[name]
            self.assertTrue(all(length == 26 for length in lengths[:-1]))
            self.assertEqual(sum(lengths), len(trigram_values(MESSAGES[name])))

    def test_known_message_lengths(self) -> None:
        self.assertEqual(
            [len(trigram_values(MESSAGES[name])) for name in MESSAGE_ORDER],
            [99, 103, 118, 102, 137, 124, 119, 120, 114],
        )

    def test_complete_contiguous_alphabet(self) -> None:
        symbols = {
            value
            for name in MESSAGE_ORDER
            for value in trigram_values(MESSAGES[name])
        }
        self.assertEqual(symbols, set(range(83)))

    def test_no_adjacent_doubles(self) -> None:
        streams = [trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER]
        self.assertEqual(adjacent_doubles(streams), 0)

    def test_family_prefixes_after_indicator(self) -> None:
        streams = {name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER}
        self.assertEqual(common_prefix_length(streams["east1"], streams["west1"], 1), 24)
        self.assertEqual(common_prefix_length(streams["east1"], streams["east2"], 1), 24)
        self.assertEqual(common_prefix_length(streams["east4"], streams["west4"], 1), 20)
        self.assertEqual(common_prefix_length(streams["east4"], streams["east5"], 1), 20)


if __name__ == "__main__":
    unittest.main()
