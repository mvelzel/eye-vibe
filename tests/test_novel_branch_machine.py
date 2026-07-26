import unittest

from eye_mystery.novel_branch_machine import (
    affine_column_screen,
    access_discipline_audit,
    axis_marker_audit,
    branch_assignment_baseline,
    branch_checksum_observation,
    carry_rewrite_observation,
    closed_disagreement_windows,
    header_scalar_branch_observation,
    systematic_code_audit,
    third_axis_roles,
    transition_cover_audit,
)


class NovelBranchMachineTests(unittest.TestCase):
    def test_closed_disagreement_windows_ignores_open_tail(self) -> None:
        windows = closed_disagreement_windows(
            (0, 1, 2, 9, 4, 6),
            (0, 7, 8, 9, 4, 5),
        )
        self.assertEqual(len(windows), 1)
        self.assertEqual((windows[0].start, windows[0].end), (1, 3))
        self.assertEqual(windows[0].difference, -12)

    def test_third_axis_roles_form_clockwise_scope_cycle(self) -> None:
        roles = third_axis_roles()
        self.assertEqual(
            (roles.loop, roles.source_mate, roles.target_mate),
            ("east4", "west4", "east5"),
        )
        self.assertEqual(roles.role_directions, (1, 2, 3, 4))
        self.assertTrue(roles.complete)
        self.assertTrue(roles.clockwise_from_up)

    def test_closed_branch_checks_exchange_scope_controls(self) -> None:
        observation = branch_checksum_observation()
        self.assertEqual(
            tuple((window.start, window.end) for window in observation.windows),
            ((30, 33), (34, 36)),
        )
        self.assertEqual(observation.predicted_differences, (3, 2))
        self.assertEqual(observation.observed_differences, (3, 2))
        self.assertTrue(observation.reciprocal_controls)

    def test_first_branch_is_gate_plus3_carry_rewrite(self) -> None:
        observation = carry_rewrite_observation()
        self.assertEqual(observation.common_tokens, (25,))
        self.assertEqual(observation.source_residual, (2, 20))
        self.assertEqual(observation.target_residual, (3, 16))
        self.assertEqual(observation.coordinate_residual, (0, 1, -2))
        self.assertEqual(observation.weighted_residual, 3)
        self.assertEqual(observation.repair_class, 3)
        self.assertTrue(observation.repaired)

    def test_broad_four_term_assignment_baseline(self) -> None:
        baseline = branch_assignment_baseline()
        self.assertEqual(baseline.assignments, 303600)
        self.assertEqual(baseline.difference3, 7568)
        self.assertEqual(baseline.difference3_with_term3, 1092)

    def test_strict_access_families_close(self) -> None:
        audit = access_discipline_audit()
        self.assertEqual(audit.repeat_order, (5, 0, 20, 1, 15))
        self.assertEqual(audit.first_order, (0, 1, 5, 15, 20))
        self.assertFalse(audit.laminar_stack)
        self.assertFalse(audit.fifo_queue)
        self.assertFalse(audit.endpoint_deque)
        self.assertEqual(audit.first_deque_failure, 5)

    def test_affine_positive_control_recovers_holdouts(self) -> None:
        plant = tuple(
            (2 * (class_id // 5) + 3 * (class_id % 5) + 4) % 5
            for class_id in range(25)
        )
        screen = affine_column_screen(plant)
        self.assertEqual(screen.maximum_training_matches, 23)
        self.assertEqual(screen.cobest_models, 1)
        self.assertEqual(screen.cobest_both_holdouts, 1)

    def test_real_systematic_code_fails_exact_gates(self) -> None:
        audit = systematic_code_audit()
        self.assertEqual(
            max(
                screen.maximum_training_matches
                for screen in audit.affine_screens
            ),
            11,
        )
        self.assertTrue(
            all(
                screen.cobest_both_holdouts == 0
                for screen in audit.affine_screens
            )
        )
        self.assertEqual(audit.maximum_output_pair_coverage, 19)
        self.assertEqual(audit.complete_output_pairs, ())

    def test_common_trace_is_edge_simple_but_untyped(self) -> None:
        audit = transition_cover_audit()
        self.assertEqual(
            (audit.length, audit.classes, audit.transitions),
            (30, 25, 29),
        )
        self.assertEqual(audit.distinct_transitions, 29)
        self.assertEqual(audit.repeated_transitions, ())

    def test_axis_marker_numeric_holdout_fails_both_models(self) -> None:
        audit = axis_marker_audit()
        self.assertEqual(
            audit.labels,
            (
                (2, (("east4", 4), ("west4", 37), ("east5", 60))),
                (3, (("east4", 56), ("west4", 19), ("east5", 5))),
            ),
        )
        self.assertEqual(audit.direction_matches, 0)
        self.assertEqual(audit.scope_matches, 0)
        self.assertEqual(
            tuple(
                (
                    hit.class_id,
                    hit.source,
                    hit.target,
                    hit.difference,
                    hit.markers,
                )
                for hit in audit.broad_hits
            ),
            (
                (2, "east4", "west4", 33, ("east5",)),
                (2, "west4", "east4", 50, ("east1",)),
                (2, "east5", "east4", 27, ("east4",)),
            ),
        )

    def test_headers_type_the_label_invariant_branch(self) -> None:
        observation = header_scalar_branch_observation()
        self.assertEqual(
            observation.header_digits,
            (
                ("east4", (1, 0, 2)),
                ("west4", (3, 0, 2)),
                ("east5", (1, 1, 3)),
            ),
        )
        self.assertEqual(observation.source_scalar, 2)
        self.assertEqual(observation.target_scalar, 3)
        self.assertEqual(observation.positive_header_digits, (1, 2, 3))
        self.assertEqual(observation.repeated_third_directions, (1, 2, 3))
        self.assertEqual(observation.absent_third_directions, (4,))
        self.assertTrue(observation.source_role_matches_scalar)
        self.assertTrue(observation.target_role_matches_scalar)
        self.assertTrue(observation.reciprocal_checks_match_scalars)
        self.assertTrue(observation.used_digit_set_matches_repeats)


if __name__ == "__main__":
    unittest.main()
