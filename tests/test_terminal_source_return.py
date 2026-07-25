from __future__ import annotations

import unittest

from eye_mystery.terminal_source_return import (
    all_pair_marker_hits,
    audit_compatible_returns,
    audit_conditional,
    compatible_aligned_marker_hits,
    compatible_classes,
    directed_difference,
    fixed_source_repeat_hits,
    source_any_marker_hits,
    terminal_source_observation,
)


class TerminalSourceReturnTests(unittest.TestCase):
    def test_observed_terminal_source_return(self) -> None:
        observed = terminal_source_observation()
        self.assertEqual(observed.class_id, 15)
        self.assertEqual(
            observed.labels,
            (("east4", 40), ("west4", 67), ("east5", 21)),
        )
        self.assertEqual((observed.from_panel, observed.to_panel), ("east4", "west4"))
        self.assertEqual(observed.difference, 27)
        self.assertEqual(observed.return_header, 27)
        self.assertTrue(observed.closes)

    def test_compatible_relabeling_probability(self) -> None:
        self.assertEqual(compatible_classes("east4"), (1, 5, 15))
        self.assertEqual(compatible_classes("west4"), (0, 1, 5, 15))
        audit = audit_compatible_returns()
        self.assertEqual(audit.tested_pairs, 12)
        self.assertEqual(
            audit.target_hits,
            ((15, 15, 40, 67),),
        )
        self.assertEqual(
            (audit.exact_probability.numerator, audit.exact_probability.denominator),
            (1, 12),
        )

    def test_fixed_and_broad_hit_inventories(self) -> None:
        fixed = fixed_source_repeat_hits()
        self.assertEqual(len(fixed), 1)
        self.assertEqual(
            (
                fixed[0].class_id,
                fixed[0].from_panel,
                fixed[0].to_panel,
                fixed[0].difference,
                fixed[0].markers,
            ),
            (15, "east4", "west4", 27, ("east4",)),
        )
        self.assertEqual(
            tuple(
                (
                    hit.class_id,
                    hit.from_panel,
                    hit.to_panel,
                    hit.difference,
                    hit.markers,
                )
                for hit in source_any_marker_hits()
            ),
            (
                (5, "west4", "east4", 77, ("west4",)),
                (15, "east4", "west4", 27, ("east4",)),
            ),
        )
        self.assertEqual(
            tuple(
                (
                    hit.class_id,
                    hit.from_panel,
                    hit.to_panel,
                    hit.difference,
                    hit.markers,
                )
                for hit in all_pair_marker_hits()
            ),
            (
                (5, "west4", "east4", 77, ("west4",)),
                (20, "east5", "east4", 36, ("east2",)),
                (15, "east4", "west4", 27, ("east4",)),
            ),
        )
        self.assertEqual(
            len(compatible_aligned_marker_hits()),
            2,
        )

    def test_synthetic_direction_and_perturbation(self) -> None:
        self.assertEqual(directed_difference(40, 67), 27)
        self.assertEqual(directed_difference(67, 40), 56)
        self.assertEqual(directed_difference(40, 68), 28)

    def test_conditional_counts(self) -> None:
        audit = audit_conditional()
        self.assertEqual(
            (
                audit.assignments,
                audit.return_header,
                audit.return_and_topology,
                audit.return_terminal_topology,
            ),
            (12096, 2532, 2, 1),
        )


if __name__ == "__main__":
    unittest.main()
