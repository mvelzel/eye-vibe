import unittest

from eye_mystery.visible_action_coloring import (
    audit_pivot_freedom,
    audit_visible_actions,
    canonical_full_contexts,
    canonical_full_streams,
)


class VisibleActionColoringTests(unittest.TestCase):
    def test_two_permutation_plant_is_recovered(self) -> None:
        streams = {
            "left": (0, 1, 3, 2),
            "right": (2, 3, 1, 0),
        }
        contexts = (("left", 0, "right", 0, 4),)
        audit = audit_visible_actions(streams, contexts)
        self.assertEqual(audit.internally_conflicting_classes, 0)
        self.assertEqual(audit.lower_bound, 2)
        self.assertEqual(audit.constructed_actions, 2)
        self.assertTrue(audit.exact_minimum)

    def test_conflicting_aligned_action_is_rejected(self) -> None:
        streams = {
            "left": (0, 1),
            "right": (0, 2),
        }
        contexts = (("left", 0, "right", 0, 2),)
        audit = audit_visible_actions(streams, contexts)
        self.assertEqual(audit.internally_conflicting_classes, 1)
        self.assertFalse(audit.exact_minimum)

    def test_eye_action_cover_is_exactly_nineteen(self) -> None:
        audit = audit_visible_actions()
        self.assertEqual(audit.transition_events, 1018)
        self.assertEqual(audit.unique_edges, 843)
        self.assertEqual(audit.event_classes, 877)
        self.assertEqual(audit.aligned_classes, 54)
        self.assertEqual(audit.internally_conflicting_classes, 0)
        self.assertEqual(audit.conflict_pairs, 12561)
        self.assertEqual(audit.lower_bound, 19)
        self.assertEqual(audit.constructed_actions, 19)
        self.assertTrue(audit.exact_minimum)

    def test_eye_pivot_has_no_nontrivial_one_step_backbone(self) -> None:
        audit = audit_pivot_freedom()
        self.assertEqual(audit.pivot_source, 26)
        self.assertEqual(
            audit.pivot_targets,
            (
                8,
                13,
                14,
                19,
                23,
                28,
                30,
                45,
                48,
                54,
                57,
                59,
                62,
                63,
                68,
                76,
                77,
                78,
                79,
            ),
        )
        self.assertEqual(audit.anchored_classes, 19)
        self.assertEqual(audit.nonanchor_classes, 858)
        self.assertEqual(audit.one_step_mutable_nonanchors, 858)
        self.assertEqual(audit.forced_nonanchors, 0)
        self.assertEqual(audit.minimum_available_colors_nonanchor, 2)
        self.assertEqual(audit.maximum_available_colors_nonanchor, 14)

    def test_marker_inclusion_does_not_create_the_result(self) -> None:
        streams = canonical_full_streams()
        contexts = canonical_full_contexts()
        audit = audit_visible_actions(streams, contexts)
        freedom = audit_pivot_freedom(streams, contexts)
        self.assertEqual(audit.constructed_actions, 19)
        self.assertTrue(audit.exact_minimum)
        self.assertEqual(freedom.nonanchor_classes, 867)
        self.assertEqual(freedom.one_step_mutable_nonanchors, 867)


if __name__ == "__main__":
    unittest.main()
