from __future__ import annotations

import unittest

from eye_mystery.factoradic_headers import header_ranks
from eye_mystery.phase_marker_closure import (
    audit_conditional,
    closure_observation,
    full_closure,
    natural_repair,
    pair_marker_matches,
    phase_closure_metrics,
    phase_topology_observation,
    scan_observed_repairs,
)
from eye_mystery.gate_plus3_transfer import ROWS


class PhaseMarkerClosureTests(unittest.TestCase):
    def test_observed_phase_metrics_and_closure(self) -> None:
        metrics = phase_closure_metrics()
        self.assertEqual(metrics.bridge_lengths, (20, 21, 20))
        self.assertEqual(metrics.old_common_length, 17)
        self.assertEqual(
            metrics.old_pair_lcps,
            (
                (("east4", "west4"), 17),
                (("east4", "east5"), 20),
                (("west4", "east5"), 17),
            ),
        )
        self.assertEqual(metrics.late_common_length, 30)
        self.assertEqual(
            metrics.late_pair_lcps,
            (
                (("east4", "west4"), 34),
                (("east4", "east5"), 30),
                (("west4", "east5"), 30),
            ),
        )
        observed = closure_observation()
        self.assertEqual(observed.source, (27, 77, 33))
        self.assertEqual(observed.shifted, (30, 80, 36))
        self.assertEqual(observed.repaired, (50, 80, 36))
        self.assertEqual(observed.target, (50, 80, 36))
        self.assertTrue(observed.closes)
        topology = phase_topology_observation()
        self.assertEqual(
            topology.edges,
            (
                ("east4", (0, 0)),
                ("west4", (0, 2)),
                ("east5", (1, 0)),
            ),
        )
        self.assertEqual(topology.loop, "east4")
        self.assertEqual(topology.target_pair, ("east4", "east5"))
        self.assertEqual(topology.source_pair, ("east4", "west4"))
        self.assertEqual(topology.old_longest_pair, topology.target_pair)
        self.assertEqual(topology.late_longest_pair, topology.source_pair)
        self.assertEqual((topology.old_extension, topology.late_extension), (3, 4))
        self.assertTrue(topology.scope_switch_matches)
        self.assertTrue(topology.mate_extensions_match)
        self.assertEqual(
            (
                topology.phase_total,
                topology.first_self_rank,
                topology.source_pair_delta,
                topology.late_pair_boundary,
                topology.late_boundary_markers,
            ),
            (50, 50, 50, 34, ("west3",)),
        )

    def test_planted_closure_and_broken_target(self) -> None:
        planted = dict(header_ranks())
        planted.update(
            {
                "east4": 27,
                "west4": 60,
                "east5": 70,
                "east1": 50,
                "west1": 63,
                "east2": 73,
            }
        )
        self.assertTrue(full_closure(planted))
        self.assertTrue(
            natural_repair(
                planted,
                ROWS[2],
                ROWS[0],
                self_index=0,
                bridge_length=20,
            )
        )
        broken = dict(planted)
        broken["west1"] = 64
        self.assertFalse(full_closure(broken))

    def test_observed_all_shift_scan_is_unique(self) -> None:
        natural = scan_observed_repairs(permute_target=False)
        permuted = scan_observed_repairs(permute_target=True)
        self.assertEqual(len(natural), 1)
        self.assertEqual(len(permuted), 1)
        for hit in natural + permuted:
            self.assertEqual(
                (
                    hit.shift,
                    hit.source_row,
                    hit.target_row,
                    hit.self_index,
                    hit.bridge_length,
                ),
                (3, 3, 1, 0, 20),
            )

    def test_conditional_counts_and_factoradic_selection(self) -> None:
        audit = audit_conditional()
        self.assertEqual(
            (
                audit.assignments,
                audit.nonself,
                audit.self_to_phase,
                audit.full,
                audit.full_and_source_delta,
                audit.full_topology,
                audit.broad_natural,
                audit.broad_permuted,
                audit.factoradic_survivors,
                audit.matching_factoradic_survivors,
            ),
            (
                12096,
                372,
                66,
                22,
                4,
                2,
                34,
                34,
                2,
                ((0, 0, 1, 1, 3, 4, 2, 2, 3),),
            ),
        )

    def test_extended_pair_boundary_is_marker_34(self) -> None:
        self.assertEqual(
            pair_marker_matches(),
            (
                (("east4", "west4"), 34, ("west3",)),
                (("east4", "east5"), 30, ()),
                (("west4", "east5"), 30, ()),
            ),
        )


if __name__ == "__main__":
    unittest.main()
