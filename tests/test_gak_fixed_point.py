from __future__ import annotations

import random
import unittest

from eye_mystery.arbitrary_gak_sat import encrypt_messages
from eye_mystery.corpus import MESSAGES, trigram_values
from eye_mystery.gak_fixed_point import find_stabilizer_contradictions
from eye_mystery.gak_fixed_point import (
    combined_word_spans,
    find_stabilizer_contradictions_from_spans,
    find_word_status_conflicts,
)
from scripts.check_waite_m3_suffix import EAST2_RAW_OFFSET, WAITE_M3_SUFFIX
from scripts.classify_that_which_windows import WINDOWS


class GAKFixedPointTests(unittest.TestCase):
    def test_detects_a_planted_fixed_point_contradiction(self) -> None:
        # Under one repeated operation, equal outputs followed by a different
        # output are impossible: the operation has already fixed the top.
        contradictions = find_stabilizer_contradictions(
            "AAAA",
            (0, 0, 1, 0),
        )
        self.assertTrue(contradictions)

    def test_valid_random_gak_fixture_has_no_contradiction(self) -> None:
        rng = random.Random(270727)
        size = 9
        initial = tuple(range(size))
        operations = []
        for _ in range(4):
            operation = list(range(size))
            rng.shuffle(operation)
            operations.append(tuple(operation))
        plaintext = tuple(rng.randrange(4) for _ in range(40))
        ciphertext = encrypt_messages((plaintext,), initial, operations)[0]
        self.assertEqual(
            find_stabilizer_contradictions(plaintext, ciphertext),
            (),
        )

    def test_cross_trace_status_conflict_is_detected(self) -> None:
        spans = combined_word_spans(
            ("XB", "YB"),
            ((0, 0), (0, 1)),
            trace_names=("fixed", "nonfixed"),
        )
        conflicts = find_word_status_conflicts(spans)
        self.assertEqual(len(conflicts), 1)
        self.assertEqual(conflicts[0].fixed.word, ("B",))
        self.assertEqual(conflicts[0].fixed.trace, "fixed")
        self.assertEqual(conflicts[0].nonfixed.trace, "nonfixed")

    def test_cross_trace_subgroup_closure_violation_is_detected(self) -> None:
        spans = combined_word_spans(
            ("XB", "YC", "ZBC"),
            ((0, 0), (1, 1), (2, 3, 4)),
            trace_names=("b", "c", "bc"),
        )
        contradictions = find_stabilizer_contradictions_from_spans(spans)
        closure = next(
            item
            for item in contradictions
            if item.first.word == ("B",)
            and item.second.word == ("C",)
            and item.combined.word == ("B", "C")
        )
        self.assertTrue(closure.first.fixes_top)
        self.assertTrue(closure.second.fixes_top)
        self.assertFalse(closure.combined.fixes_top)

    def test_waite_suffix_has_a_five_observation_certificate(self) -> None:
        ciphertext = trigram_values(MESSAGES["east2"])[EAST2_RAW_OFFSET:]
        contradictions = find_stabilizer_contradictions(
            WAITE_M3_SUFFIX,
            ciphertext,
        )
        self.assertEqual(len(contradictions), 4)
        shortest = contradictions[0]
        self.assertEqual(shortest.observation_offsets, (20, 25, 64, 68, 73))
        self.assertEqual("".join(shortest.first.word), "EST,")
        self.assertFalse(shortest.first.fixes_top)
        self.assertEqual("".join(shortest.second.word), " THE ")
        self.assertTrue(shortest.second.fixes_top)
        self.assertEqual("".join(shortest.combined.word), "EST, THE ")
        self.assertTrue(shortest.combined.fixes_top)

    def test_that_which_has_three_consistent_top_stabilizer_words(self) -> None:
        phrase = "THAT WHICH"
        ciphertexts = tuple(
            trigram_values(MESSAGES[window.message])[
                window.offset : window.offset + len(phrase)
            ]
            for window in WINDOWS
        )
        spans = combined_word_spans(
            (phrase,) * len(ciphertexts),
            ciphertexts,
            trace_names=tuple(
                f"{window.message}:{window.offset}"
                for window in WINDOWS
            ),
        )
        self.assertEqual(find_word_status_conflicts(spans), ())
        self.assertEqual(
            find_stabilizer_contradictions_from_spans(spans),
            (),
        )
        self.assertEqual(
            {
                "".join(span.word)
                for span in spans
                if span.fixes_top
            },
            {"HAT WHI", "T W", "WHIC"},
        )


if __name__ == "__main__":
    unittest.main()
