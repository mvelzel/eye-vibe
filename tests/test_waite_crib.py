import unittest

from eye_mystery.corpus import MESSAGES, trigram_values
from scripts.check_waite_m3_suffix import (
    EAST2_RAW_OFFSET,
    WAITE_M3_SUFFIX,
    repeated_substring_checks,
)
from scripts.search_waite_that_which import (
    common_gap_strings,
    TARGETS,
    align_source,
    cross_incompatibility_count,
    normalize_ocr,
    maximal_common_gap_strings,
    phrase_offsets,
)
from scripts.search_waite_sparse_decks import (
    WAITE_M3_BODY,
    relation_conflicts,
)
from scripts.classify_that_which_windows import (
    PAIRS,
    common_right_prefix,
    pair_maximal_context,
    pair_right_prefix,
    patterns,
)
from scripts.calibrate_waite_gap_fingerprint import matched_blocks
from scripts.test_two_symbol_memory import (
    conditioned_null,
    delayed_common_end,
    delayed_patterns,
)
from scripts.analyze_delayed_isomorph_groups import find_groups, scan_lengths


class WaiteCribTests(unittest.TestCase):
    def test_suffix_fills_east2_exactly(self) -> None:
        east2 = trigram_values(MESSAGES["east2"])
        self.assertEqual(len(WAITE_M3_SUFFIX), 81)
        self.assertEqual(EAST2_RAW_OFFSET + len(WAITE_M3_SUFFIX), len(east2))

    def test_repeated_substrings_are_isomorph_compatible(self) -> None:
        east2 = trigram_values(MESSAGES["east2"])[EAST2_RAW_OFFSET:]
        checks = repeated_substring_checks(WAITE_M3_SUFFIX, east2)
        self.assertTrue(checks)
        self.assertTrue(all(item.compatible for item in checks))

        longest = max(checks, key=lambda item: item.length)
        self.assertEqual(longest.text, "E THAT WHICH IS THE ")
        self.assertEqual(longest.length, 20)
        self.assertEqual((longest.first, longest.second), (6, 41))

    def test_ocr_normalization_undoes_line_wraps(self) -> None:
        text = "that which is exal-\n ted  above"
        self.assertEqual(normalize_ocr(text), "THAT WHICH IS EXALTED ABOVE")

    def test_common_gap_source_fingerprint(self) -> None:
        texts = (
            "ABCDE" + "X" * 5 + "ABCDE",
            "ABCDE" + "Y" * 7 + "ABCDE",
        )
        self.assertIn("ABCDE", common_gap_strings(texts, (10, 12), 5))
        length, strings = maximal_common_gap_strings(
            texts, (10, 12), limit=10
        )
        self.assertEqual(length, 5)
        self.assertIn("ABCDE", strings)

    def test_matched_control_blocks_do_not_cross_unique_tail(self) -> None:
        self.assertEqual(
            matched_blocks(("ABCDE", "FGHIJ"), 4),
            ("ABCD", "E\ue000FG", "HIJ\ue001"),
        )

    def test_source_alignment_uses_complete_message_window(self) -> None:
        target = TARGETS[2]
        source = (
            "X" * target.first_offset
            + WAITE_M3_SUFFIX
            + " trailing source text"
        )
        self.assertEqual(phrase_offsets(source), (53, 88))
        alignments = align_source("synthetic", source, target)
        self.assertEqual(len(alignments), 1)
        self.assertEqual(
            len(trigram_values(MESSAGES["east2"])),
            len(alignments[0].plaintext) + 1,
        )

    def test_cross_compatibility_detects_pattern_conflict(self) -> None:
        total, conflicts = cross_incompatibility_count(
            "ABCA",
            (1, 2, 3, 1),
            "ABCA",
            (4, 5, 6, 7),
        )
        self.assertEqual(total, 1)
        self.assertEqual(conflicts, 1)

    def test_waite_body_fills_message_after_marker(self) -> None:
        self.assertEqual(
            len(WAITE_M3_BODY),
            len(trigram_values(MESSAGES["east2"])) - 1,
        )

    def test_relation_conflicts_characterize_injective_mapping(self) -> None:
        self.assertEqual(relation_conflicts("ABCA", (7, 2, 9, 7)), (0, 0, 0))
        total, same, distinct = relation_conflicts("ABCA", (7, 2, 9, 4))
        self.assertEqual((total, same, distinct), (1, 1, 0))
        total, same, distinct = relation_conflicts("ABCD", (7, 2, 9, 7))
        self.assertEqual((total, same, distinct), (1, 0, 1))

    def test_six_windows_split_after_ten_symbols(self) -> None:
        self.assertEqual(common_right_prefix(), 10)
        self.assertEqual(len(set(patterns(right=10))), 1)
        self.assertEqual(len(set(patterns(right=11))), 2)

    def test_pairwise_isomorph_extents(self) -> None:
        self.assertEqual(
            tuple(pair_right_prefix(*pair) for pair in PAIRS),
            (19, 26, 26),
        )
        self.assertEqual(
            tuple(pair_maximal_context(*pair) for pair in PAIRS),
            ((7, 19), (7, 26), (6, 26)),
        )

    def test_two_symbol_trim_restores_delayed_isomorphism(self) -> None:
        self.assertEqual(delayed_common_end(0), 10)
        self.assertEqual(delayed_common_end(1), 10)
        self.assertEqual(delayed_common_end(2), 17)
        self.assertEqual(len(set(delayed_patterns(2, 14))), 1)
        self.assertEqual(len(set(delayed_patterns(2, 17))), 1)
        self.assertEqual(len(set(delayed_patterns(2, 18))), 2)

    def test_conditioned_null_is_seeded_and_bounded(self) -> None:
        first = conditioned_null(
            trials=20,
            maximum_extension=2,
            trim=2,
            seed=7,
            batch_size=7,
        )
        second = conditioned_null(
            trials=20,
            maximum_extension=2,
            trim=2,
            seed=7,
            batch_size=7,
        )
        self.assertEqual(first, second)
        self.assertTrue(all(0 <= value <= 20 for value in first))

    def test_delayed_group_scan_recovers_famous_six_windows(self) -> None:
        groups = find_groups(
            base_length=9,
            minimum_occurrences=3,
            minimum_repeat_excess=2,
        )
        famous = next(
            item for item in groups if item.equality_pattern == "A.B.CB.AC"
        )
        self.assertEqual(len(famous.occurrences), 6)
        self.assertEqual(famous.common_ends, (10, 10, 17))
        self.assertEqual(famous.trim_two_gain, 7)

    def test_delayed_gain_has_no_independent_repeat_rich_replication(self) -> None:
        groups = scan_lengths(
            range(6, 15),
            minimum_occurrences=3,
            minimum_repeat_excess=2,
        )
        positive = [item for item in groups if item.trim_two_gain > 0]
        self.assertTrue(positive)
        self.assertEqual(max(item.trim_two_gain for item in positive), 7)
        self.assertEqual(
            len({item.relative_occurrence_signature for item in positive}),
            1,
        )


if __name__ == "__main__":
    unittest.main()
