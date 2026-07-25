from __future__ import annotations

import random
import unittest
from collections import Counter

from eye_mystery.row2_phase_transfer import (
    OPENING_EXIT,
    ROW2_MESSAGES,
    audit_controls,
    initial_common_phase,
    phase_starts,
    predicted_suffixes,
    row2_bodies,
    shuffle_post_opening,
    transfer_metrics,
)


class Row2PhaseTransferTests(unittest.TestCase):
    def test_budget_predicts_suffixes_and_starts(self) -> None:
        bodies = row2_bodies()
        suffixes = predicted_suffixes()
        self.assertEqual(suffixes, (4, 3, 4))
        self.assertEqual(initial_common_phase(bodies), 6)
        assert suffixes is not None
        self.assertEqual(phase_starts(bodies, suffixes), (15, 14, 15))

    def test_observed_transfer_replicates_piecewise_trace(self) -> None:
        metrics = transfer_metrics(row2_bodies())
        self.assertEqual(metrics.old_common, 6)
        self.assertEqual(metrics.pair_bridge_length, 10)
        self.assertTrue(metrics.pair_complete)
        self.assertTrue(metrics.pair_switch)
        self.assertEqual(metrics.new_common, 7)
        self.assertTrue(metrics.joint)

    def test_shuffle_preserves_registered_nuisances(self) -> None:
        body = row2_bodies()["west2"]
        shuffled = shuffle_post_opening(body, random.Random(88))
        self.assertEqual(shuffled[:OPENING_EXIT], body[:OPENING_EXIT])
        self.assertEqual(Counter(shuffled), Counter(body))
        self.assertFalse(
            any(left == right for left, right in zip(shuffled, shuffled[1:]))
        )

    def test_synthetic_plant_and_broken_new_phase(self) -> None:
        opening = (0, 1, 2, 3, 4)
        west2 = opening + tuple(range(10, 20)) + (
            10, 21, 22, 23, 24, 25, 26, 10, 27, 28
        )
        east3 = opening + (30, 31, 32, 33, 34, 35, 31, 36, 37) + (
            40, 41, 42, 43, 44, 45, 46, 47, 48, 49
        )
        west3 = opening + tuple(range(50, 60)) + (
            70, 61, 62, 63, 64, 65, 66, 67, 68, 69
        )
        bodies = {
            "west2": west2,
            "east3": east3,
            "west3": west3,
        }
        metrics = transfer_metrics(bodies, suffixes=(4, 3, 4))
        self.assertTrue(metrics.pair_complete)
        self.assertTrue(metrics.pair_switch)
        self.assertEqual(metrics.new_common, 7)
        self.assertTrue(metrics.joint)

        broken = dict(bodies)
        east = list(east3)
        east[14 + 3] = east[14]
        broken["east3"] = tuple(east)
        self.assertLess(
            transfer_metrics(broken, suffixes=(4, 3, 4)).new_common,
            7,
        )

    def test_small_control_audit_runs(self) -> None:
        audit = audit_controls(controls=199, seed=123)
        self.assertEqual(audit.controls, 199)
        self.assertTrue(audit.observed.joint)
        self.assertEqual(
            (
                audit.new_common_exceedances,
                audit.pair_complete_exceedances,
                audit.pair_switch_exceedances,
                audit.joint_exceedances,
                audit.broad_new_common_exceedances,
                audit.broad_joint_exceedances,
            ),
            (98, 37, 10, 3, 147, 83),
        )



if __name__ == "__main__":
    unittest.main()
