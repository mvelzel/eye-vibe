from __future__ import annotations

import random
import unittest
from collections import Counter

from eye_mystery.synchronizing_bridge import (
    EAST_PAIR,
    BridgeSpec,
    audit_controls,
    bridge_metrics,
    bridge_segments,
    bridge_specs,
    canonical_streams,
    late_context_profiles,
    observed_metrics,
    shuffle_one_bridge,
)


class SynchronizingBridgeTests(unittest.TestCase):
    def test_boundaries_are_derived_from_canonical_records(self) -> None:
        specs = bridge_specs()
        self.assertEqual(
            {
                name: (
                    spec.anchor_start_trimmed,
                    spec.anchor_value,
                    spec.endpoint_full,
                    spec.late_entry_full,
                    spec.length,
                )
                for name, spec in specs.items()
            },
            {
                "east4": (16, 75, 48, 68, 20),
                "west4": (18, 81, 50, 71, 21),
                "east5": (17, 48, 49, 69, 20),
            },
        )

    def test_observed_piecewise_state_trace(self) -> None:
        metrics = observed_metrics()
        self.assertEqual(metrics.triple_lcp, 17)
        self.assertTrue(metrics.east_complete)
        self.assertTrue(metrics.east_switch)
        self.assertTrue(metrics.joint)
        self.assertEqual(
            metrics.signatures[0],
            metrics.signatures[2],
        )
        self.assertEqual(
            metrics.signatures[0][:17],
            metrics.signatures[1][:17],
        )

    def test_published_late_contexts_are_partial_bijections(self) -> None:
        profiles = late_context_profiles()
        self.assertEqual(set(profiles), {"last-west4", "last-east5"})
        self.assertTrue(
            all(profile.first_conflict is None for profile in profiles.values())
        )

    def test_shuffle_preserves_bridge_nuisances(self) -> None:
        streams = canonical_streams()
        spec = bridge_specs()["east4"]
        shuffled = shuffle_one_bridge(
            streams["east4"],
            spec,
            random.Random(1234),
        )
        self.assertEqual(Counter(shuffled), Counter(streams["east4"]))
        self.assertEqual(shuffled[spec.endpoint_full], spec.anchor_value)
        self.assertEqual(
            shuffled[: spec.endpoint_full],
            streams["east4"][: spec.endpoint_full],
        )
        self.assertEqual(
            shuffled[spec.late_entry_full :],
            streams["east4"][spec.late_entry_full :],
        )
        self.assertFalse(
            any(left == right for left, right in zip(shuffled, shuffled[1:]))
        )

    def test_synthetic_plant_and_broken_heldout(self) -> None:
        signature = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 4, 11, 3, 6, 12, 13)
        east4 = signature + (4, 14, 15)
        east5 = tuple(value + 20 for value in signature) + (24, 34, 35)
        west4 = signature + (14, 15, 16, 8)
        planted = bridge_metrics(
            {
                "east4": east4,
                "west4": west4,
                "east5": east5,
            },
            (4, 77),
        )
        self.assertEqual(planted.triple_lcp, 17)
        self.assertTrue(planted.east_complete)
        self.assertTrue(planted.east_switch)
        self.assertTrue(planted.joint)

        broken_west = list(west4)
        broken_west[11] = 70
        broken = bridge_metrics(
            {
                "east4": east4,
                "west4": tuple(broken_west),
                "east5": east5,
            },
            (4, 77),
        )
        self.assertEqual(broken.triple_lcp, 11)
        self.assertFalse(broken.joint)

    def test_small_control_audit_runs(self) -> None:
        audit = audit_controls(controls=199, seed=99)
        self.assertEqual(audit.controls, 199)
        self.assertTrue(audit.observed.joint)
        self.assertEqual(
            (
                audit.triple_lcp_exceedances,
                audit.east_complete_exceedances,
                audit.east_switch_exceedances,
                audit.joint_exceedances,
                audit.conditioned_w4_exceedances,
                audit.broad_lcp_exceedances,
                audit.broad_pair_exceedances,
                audit.broad_joint_exceedances,
            ),
            (0, 0, 0, 0, 0, 0, 0, 0),
        )


if __name__ == "__main__":
    unittest.main()
