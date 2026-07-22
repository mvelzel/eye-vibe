from __future__ import annotations

import unittest

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.seventh_wide import (
    base5_digits,
    bwt_last_column,
    bwt_mtf_score,
    change_score,
    change_masks,
    comparison_signatures,
    gap_score,
    next_occurrence_distances,
    ordinal_permutation,
    ordinal_score,
    permute_six_blocks,
    pointer_score,
    renderer_body_tape,
    shortest_gap_bits,
    six_block_score,
)


class SeventhWideUnitTests(unittest.TestCase):
    def test_terminated_bwt_matches_banana_example(self) -> None:
        banana = (1, 0, 2, 0, 2, 0)

        self.assertEqual(
            bwt_last_column(banana, (0, 1, 2, 3, 4, 5)),
            (0, 2, 2, 1, 6, 0, 0),
        )

    def test_renderer_tape_removes_spatial_header_eyes(self) -> None:
        stream = trigram_values(MESSAGES["east1"])
        tape = renderer_body_tape("east1", stream)

        self.assertEqual(
            sum(value != 5 for value in tape),
            len(MESSAGES["east1"]) - 3,
        )
        self.assertEqual(tape.count(5), 8)

    def test_six_block_transposition_preserves_tail(self) -> None:
        self.assertEqual(
            permute_six_blocks(tuple(range(8)), (5, 4, 3, 2, 1, 0)),
            (5, 4, 3, 2, 1, 0, 6, 7),
        )

    def test_hidden_gap_bit_uses_unique_shortest_mod101_path(self) -> None:
        self.assertEqual(shortest_gap_bits((80, 2, 20, 30)), (1, 0, 0))
        self.assertEqual(shortest_gap_bits((2, 80)), (1,))

    def test_change_and_comparison_channels_keep_coordinate_order(self) -> None:
        values = (0, 1, 6, 31)

        self.assertEqual(
            tuple(map(base5_digits, values)),
            ((0, 0, 0), (0, 0, 1), (0, 1, 1), (1, 1, 1)),
        )
        self.assertEqual(change_masks(values), (1, 2, 4))
        self.assertEqual(comparison_signatures(values), (14, 16, 22))

    def test_temporal_pointer_distances_follow_occurrence_order(self) -> None:
        self.assertEqual(next_occurrence_distances((4, 1, 4, 4, 1)), (2, 3, 1))

    def test_ordinal_permutation(self) -> None:
        self.assertEqual(ordinal_permutation((40, 10, 30, 20)), (3, 0, 2, 1))


class SeventhWideCorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.streams = {
            name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
        }

    def test_observed_scores_are_stable(self) -> None:
        bwt = bwt_mtf_score(self.streams)
        block = six_block_score(self.streams)
        gap = gap_score(self.streams)
        change = change_score(self.streams)
        pointer = pointer_score(self.streams)
        ordinal = ordinal_score(self.streams)

        self.assertEqual(bwt.symbols, 3 * (1036 - 9) + 86 + 9)
        self.assertEqual((bwt.runs, bwt.route), (2523, "inverse"))
        self.assertEqual(block.transitions, 1027 - 9)
        self.assertEqual(
            (block.adjacent_equal, block.repeated_bigrams, block.route),
            (10, 106, "header"),
        )
        self.assertEqual(
            (gap.compressed_bytes, gap.runs, gap.ones, gap.bits),
            (132, 250, 173, 1018),
        )
        self.assertEqual(
            (change.compressed_bytes, change.runs, change.route),
            (385, 711, "change-mask"),
        )
        self.assertEqual(
            (pointer.compressed_bytes, pointer.events, pointer.support),
            (413, 469, 92),
        )
        self.assertEqual(ordinal.eligible_windows, 873)
        self.assertEqual(
            (ordinal.matches, ordinal.initial_matches, ordinal.route),
            (1, 0, "inverse"),
        )


if __name__ == "__main__":
    unittest.main()
