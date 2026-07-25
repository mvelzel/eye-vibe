from __future__ import annotations

import random
import unittest

from eye_mystery.phase_overlap import (
    audit_controls,
    ledger_target,
    new_class_positions,
    observed_overlap_metrics,
    overlap_metrics,
    overlap_type_profile,
    panel_overlap_profiles,
    sample_overlap_edges,
)


class PhaseOverlapTests(unittest.TestCase):
    def test_observed_profiles_and_target(self) -> None:
        profiles = panel_overlap_profiles()
        self.assertEqual(
            profiles["east4"].observed_edges,
            ((0, 7), (7, 24), (8, 0), (14, 23), (15, 20)),
        )
        self.assertEqual(
            profiles["west4"].observed_edges,
            ((1, 9), (10, 12), (12, 10), (14, 20)),
        )
        self.assertEqual(
            profiles["east5"].observed_edges,
            ((7, 24), (10, 21)),
        )
        target = ledger_target()
        self.assertEqual(
            (
                target.old_class,
                target.common_phase,
                target.new_class,
                target.east_newline_preimage,
                target.new_position,
            ),
            (7, 17, 24, 4, 28),
        )
        self.assertEqual(new_class_positions("east4", 24), (28,))
        self.assertEqual(new_class_positions("east5", 24), (28,))

    def test_observed_target_is_the_only_shared_edge(self) -> None:
        metrics = observed_overlap_metrics()
        self.assertTrue(metrics.east_target)
        self.assertTrue(metrics.east_only)
        self.assertTrue(metrics.shared_offset17)
        self.assertTrue(metrics.any_shared_edge)
        self.assertEqual(
            metrics.shared_edges,
            ((("east4", "east5"), (7, 24)),),
        )

    def test_randomizer_preserves_every_overlap_type(self) -> None:
        rng = random.Random(44)
        for profile in panel_overlap_profiles().values():
            sampled = sample_overlap_edges(profile, rng)
            self.assertEqual(len(sampled), len(profile.observed_edges))
            self.assertEqual(
                overlap_type_profile(profile, sampled),
                profile.type_counts(),
            )
            self.assertEqual(
                len({left for left, _right in sampled}),
                len(sampled),
            )
            self.assertEqual(
                len({right for _left, right in sampled}),
                len(sampled),
            )

    def test_synthetic_target_and_broken_panel(self) -> None:
        planted = overlap_metrics(
            {
                "east4": ((7, 24), (1, 2)),
                "west4": ((3, 4),),
                "east5": ((7, 24), (5, 6)),
            }
        )
        self.assertTrue(planted.east_target)
        self.assertTrue(planted.east_only)
        broken = overlap_metrics(
            {
                "east4": ((7, 24), (1, 2)),
                "west4": ((3, 4),),
                "east5": ((7, 23), (5, 6)),
            }
        )
        self.assertFalse(broken.east_target)

    def test_small_control_audit_runs(self) -> None:
        audit = audit_controls(controls=199, seed=55)
        self.assertEqual(audit.controls, 199)
        self.assertTrue(audit.observed.east_target)
        self.assertEqual(
            (
                audit.exact_east_target_probability.numerator,
                audit.exact_east_target_probability.denominator,
            ),
            (3, 33800),
        )


if __name__ == "__main__":
    unittest.main()
