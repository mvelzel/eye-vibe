from __future__ import annotations

import unittest

from eye_mystery.practice_cipher3_third import (
    FactorMatch,
    IsomorphicEvidence,
    RecurrenceScreen,
    _affine_run,
    _isomorphic_run,
    affine_factor_inventory,
    berlekamp_massey_complexity,
    compression_audit,
    inverse_bwt,
    lz78_phrase_count,
    move_to_front_decode,
    recurrence_residuals,
    select_recurrence,
    strongest_isomorphic_evidence,
)
from eye_mystery.practice_cipher3_wide import load_cipher3


class PracticeCipher3ThirdPrimitiveTests(unittest.TestCase):
    def test_affine_run_recovers_map_and_stops_at_mismatch(self) -> None:
        source = (2, 5, 9, 14, 20)
        target = tuple((7 * value + 11) % 83 for value in source)
        changed = target[:-1] + ((target[-1] + 1) % 83,)
        self.assertEqual(_affine_run(source, changed, 0, 0), (4, 7, 11))

    def test_isomorphic_run_uses_both_directions_of_bijection(self) -> None:
        self.assertEqual(
            _isomorphic_run((1, 2, 1, 3), (8, 9, 8, 7), 0, 0),
            4,
        )
        self.assertEqual(
            _isomorphic_run((1, 2, 3), (8, 8, 9), 0, 0),
            1,
        )

    def test_recurrence_residuals_recover_planted_order_two(self) -> None:
        sequence = [3, 7]
        residuals = (5, 9, 5, 9, 5, 9)
        for residual in residuals:
            sequence.append((4 * sequence[-1] + 2 * sequence[-2] + residual) % 83)
        self.assertEqual(
            recurrence_residuals((sequence,), (4, 2), body=False),
            residuals,
        )

    def test_berlekamp_massey_recovers_geometric_complexity_one(self) -> None:
        sequence = tuple(3 * pow(7, index, 83) % 83 for index in range(30))
        self.assertEqual(berlekamp_massey_complexity(sequence), 1)

    def test_move_to_front_round_trip_fixture(self) -> None:
        # Ranks 2, 0, 1 decode from [0,1,2,...] to 2,2,0.
        self.assertEqual(move_to_front_decode((2, 0, 1)), (2, 2, 0))

    def test_inverse_bwt_known_fixture(self) -> None:
        # BWT("banana") = "nnbaaa" with primary row 3.
        encoded = tuple(map(ord, "nnbaaa"))
        self.assertEqual(
            "".join(map(chr, inverse_bwt(encoded, 3))),
            "banana",
        )

    def test_lz78_phrase_count_is_label_invariant(self) -> None:
        self.assertEqual(
            lz78_phrase_count((1, 2, 1, 2, 1, 3)),
            lz78_phrase_count((9, 8, 9, 8, 9, 7)),
        )


class PracticeCipher3ThirdCorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.streams = load_cipher3()

    def test_known_affine_branch_is_excluded_from_inventory(self) -> None:
        matches = affine_factor_inventory(
            self.streams,
            minimum_length=20,
            exclude_known_branch=False,
        )
        self.assertEqual(
            (
                matches[0].left,
                matches[0].right,
                matches[0].left_start,
                matches[0].right_start,
                matches[0].length,
                matches[0].multiplier,
                matches[0].offset,
            ),
            ("A4", "A5", 1, 1, 43, 1, 0),
        )
        self.assertEqual(
            affine_factor_inventory(
                self.streams,
                minimum_length=20,
                exclude_known_branch=True,
            ),
            (),
        )

    def test_recurrence_screens_are_deterministic(self) -> None:
        self.assertEqual(
            select_recurrence(self.streams, order=1, body=True),
            RecurrenceScreen(1, True, (53,), 77, 83, 83, 83),
        )
        self.assertEqual(
            select_recurrence(self.streams, order=2, body=True),
            RecurrenceScreen(2, True, (70, 34), 75, 83, 83, 83),
        )

    def test_nondisclosed_isomorphs_have_only_two_repeat_constraints(self) -> None:
        evidence = strongest_isomorphic_evidence(self.streams)
        self.assertEqual(
            evidence,
            IsomorphicEvidence(
                FactorMatch("C3", "C5", 76, 147, 28, 1, -1, -1),
                distinct_values=26,
                repeated_constraints=2,
            ),
        )

    def test_compression_audit_covers_all_bodies(self) -> None:
        audit = compression_audit(self.streams)
        self.assertEqual(audit.events, 2229)
        self.assertEqual(audit.adjacent_doubles, 0)
        self.assertEqual(audit.direct_lz78_phrases, 1588)
        self.assertEqual(audit.inverse_bwt_valid_messages, 15)
        self.assertEqual(audit.inverse_bwt_lz78_phrases, 1255)
        self.assertEqual(audit.mtf_decoded_unique, 83)
        self.assertEqual(audit.mtf_message_maximum_unique, 80)


if __name__ == "__main__":
    unittest.main()
