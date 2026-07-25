from __future__ import annotations

import unittest

from eye_mystery.factoradic_headers import compose, inverse, lexicographic_unrank
from eye_mystery.gate_plus3_transfer import (
    ROWS,
    audit_conditional,
    audit_observed,
    complete_transfer,
    control_edge,
    header_ranks,
    quotient_pair,
    scan_observed_shifts,
    shared_quotient,
)


class GatePlus3TransferTests(unittest.TestCase):
    def test_control_edges_and_observed_transfer(self) -> None:
        ranks = header_ranks()
        self.assertEqual(control_edge(ranks["east4"]), (0, 0))
        transfers = complete_transfer(ranks, ROWS[2], ROWS[0])
        self.assertIsNotNone(transfers)
        assert transfers is not None
        self.assertEqual(
            tuple(
                (
                    transfer.source_name,
                    transfer.source_rank,
                    transfer.target_name,
                    transfer.target_rank,
                )
                for transfer in transfers
            ),
            (
                ("west4", 77, "west1", 80),
                ("east5", 33, "east2", 36),
            ),
        )

    def test_quotients_round_trip(self) -> None:
        for source, target in ((77, 80), (33, 36)):
            left, right = quotient_pair(source, target)
            source_permutation = lexicographic_unrank(source)
            target_permutation = lexicographic_unrank(target)
            self.assertEqual(compose(left, source_permutation), target_permutation)
            self.assertEqual(compose(source_permutation, right), target_permutation)
            self.assertEqual(
                left,
                compose(target_permutation, inverse(source_permutation)),
            )

    def test_broken_target_is_not_complete(self) -> None:
        ranks = header_ranks()
        broken = dict(ranks)
        broken["east2"] = 35
        self.assertIsNone(complete_transfer(broken, ROWS[2], ROWS[0]))

    def test_synthetic_complete_transfer_with_shared_quotient(self) -> None:
        planted = {
            "east1": 55,
            "west1": 63,
            "east2": 36,
            "west2": 76,
            "east3": 34,
            "west3": 33,
            "east4": 27,
            "west4": 52,
            "east5": 60,
        }
        transfers = complete_transfer(planted, ROWS[2], ROWS[0])
        self.assertIsNotNone(transfers)
        assert transfers is not None
        self.assertEqual(len(transfers), 2)
        self.assertIsNotNone(shared_quotient(transfers, side="left"))

    def test_observed_shared_quotient_is_computed_consistently(self) -> None:
        observed = audit_observed()
        left = shared_quotient(observed.transfers, side="left")
        right = shared_quotient(observed.transfers, side="right")
        self.assertEqual(left, observed.shared_left)
        self.assertEqual(right, observed.shared_right)
        self.assertIsNone(left)
        self.assertIsNone(right)

    def test_conditional_universe_and_shift_scan_are_stable(self) -> None:
        audit = audit_conditional()
        self.assertEqual(
            (
                audit.assignments,
                audit.exact_complete,
                audit.exact_complete_self_absent,
                audit.exact_shared_left,
                audit.exact_shared_right,
                audit.exact_shared_either,
                audit.broad_any_complete,
                audit.broad_any_complete_shared,
                audit.broad_max_hits_at_least_observed,
                audit.broad_max_fraction_complete,
            ),
            (12096, 372, 283, 0, 0, 0, 492, 0, 954, 492),
        )
        hits = scan_observed_shifts()
        self.assertEqual(
            tuple(
                (
                    hit.shift,
                    hit.source_row,
                    hit.target_row,
                    hit.transfer_count,
                    hit.shared_left,
                    hit.shared_right,
                )
                for hit in hits
            ),
            ((3, 3, 1, 2, False, False),),
        )


if __name__ == "__main__":
    unittest.main()
