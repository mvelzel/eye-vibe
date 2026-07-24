from __future__ import annotations

import unittest

from eye_mystery.hidden_geometry import (
    ChordConstraint,
    FIRST_FAMILY_NAMES,
    LAST_FAMILY_NAMES,
    chord_classes,
    chord_constraints,
    constraint_holds,
    last_short_core,
    linear_core_certificate,
    repair_hidden_geometry,
    repair_hidden_geometry_classes,
    solve_hidden_geometry,
    solve_hidden_geometry_boolean,
    z3_available,
)


class HiddenGeometryUnitTests(unittest.TestCase):
    def test_unsigned_constraint_accepts_both_orientations(self) -> None:
        coordinates = (0, 7, 19, 12)
        forward = ChordConstraint("x", 1, 0, 0, 1, 3, 2)
        reverse = ChordConstraint("x", 1, 0, 0, 1, 2, 3)
        self.assertTrue(constraint_holds(forward, coordinates, modulus=23))
        self.assertTrue(constraint_holds(reverse, coordinates, modulus=23))

    def test_corpus_constraint_inventory(self) -> None:
        constraints = chord_constraints()
        self.assertEqual(len(constraints), 141)
        self.assertEqual(len({label for item in constraints for label in item.labels}), 71)
        self.assertEqual(
            len(chord_constraints(names=FIRST_FAMILY_NAMES)), 59
        )
        self.assertEqual(
            len(chord_constraints(names=LAST_FAMILY_NAMES)), 82
        )
        classes = chord_classes(constraints)
        self.assertEqual((len(classes), sum(map(len, classes))), (44, 185))

    def test_repair_finds_a_small_planted_witness(self) -> None:
        planted = (
            ChordConstraint("p", 1, 0, 0, 1, 2, 3),
            ChordConstraint("p", 1, 1, 0, 2, 1, 3),
        )
        result = repair_hidden_geometry(
            planted,
            modulus=5,
            restarts=5,
            steps_per_restart=100,
            seed=7,
        )
        self.assertTrue(result.complete)
        class_result = repair_hidden_geometry_classes(
            planted,
            modulus=5,
            restarts=5,
            steps_per_restart=100,
            seed=7,
        )
        self.assertTrue(class_result.complete)

    def test_last_family_short_core_is_exact_and_deletion_minimal(self) -> None:
        core = last_short_core()
        self.assertEqual(len(core), 8)
        certificate = linear_core_certificate(core)
        self.assertEqual(
            (
                certificate.labels,
                certificate.orientation_branches,
                certificate.forced_collision_branches,
            ),
            (11, 256, 256),
        )
        self.assertTrue(all(count > 0 for count in certificate.deletion_survivors))

    @unittest.skipUnless(z3_available(), "optional z3 package is unavailable")
    def test_solver_accepts_a_planted_instance(self) -> None:
        planted = (
            ChordConstraint("p", 1, 0, 0, 1, 2, 3),
            ChordConstraint("p", 1, 1, 0, 2, 1, 3),
        )
        result = solve_hidden_geometry(planted, modulus=5, timeout_ms=5_000)
        self.assertEqual(result.outcome, "sat")
        boolean_result = solve_hidden_geometry_boolean(
            planted, modulus=5, timeout_ms=5_000
        )
        self.assertEqual(boolean_result.outcome, "sat")

    @unittest.skipUnless(z3_available(), "optional z3 package is unavailable")
    def test_solver_rejects_an_equidistant_triangle_on_odd_prime(self) -> None:
        impossible = (
            ChordConstraint("n", 1, 0, 0, 1, 0, 2),
            ChordConstraint("n", 1, 1, 0, 1, 1, 2),
        )
        result = solve_hidden_geometry(
            impossible,
            modulus=5,
            timeout_ms=5_000,
            extract_core=True,
        )
        self.assertEqual(result.outcome, "unsat")
        self.assertEqual(len(result.core), 2)


if __name__ == "__main__":
    unittest.main()
