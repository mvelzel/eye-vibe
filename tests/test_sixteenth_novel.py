from __future__ import annotations

import unittest

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.factoradic_headers import P_MESSAGES, Q_MESSAGES
from eye_mystery.hidden_geometry import context_sequences
from eye_mystery.seventh_wide import renderer_body_tape
from eye_mystery.sixteenth_novel import (
    PROJECTIVE_POINTS,
    DyckSpec,
    Field25Spec,
    RowCodeSpec,
    accepted_projective_multiplicities,
    apply_projective_matrix,
    audit_dyck_syntax,
    audit_rotor_router,
    audit_row_codes,
    base5_rank,
    canonical_cycle,
    cycle_word_compatible,
    dyck_scan,
    field25_specs,
    f25_inv,
    f25_mul,
    projective_context_score,
    projective_context_audit,
    projective_point_scalar,
    row_code_coefficients,
)


class SixteenthNovelTests(unittest.TestCase):
    def test_projective_plane_has_31_points_and_visible_full_support(self) -> None:
        self.assertEqual(31, len(PROJECTIVE_POINTS))
        multiplicities = accepted_projective_multiplicities()
        self.assertEqual(82, sum(multiplicities))
        self.assertEqual(17, multiplicities.count(2))
        self.assertEqual(8, multiplicities.count(3))
        self.assertEqual(6, multiplicities.count(4))
        self.assertEqual(42, sum(4 - value for value in multiplicities))

    def test_projective_scalar_multiples_share_a_point(self) -> None:
        first = base5_rank((1, 2, 3))
        second = base5_rank((2, 4, 1))
        first_point, first_scalar = projective_point_scalar(first)
        second_point, second_scalar = projective_point_scalar(second)
        self.assertEqual(first_point, second_point)
        self.assertEqual((1, 2), (first_scalar, second_scalar))

    def test_projective_matrix_preserves_incidence(self) -> None:
        matrix = ((1, 1, 0), (0, 1, 1), (1, 0, 1))
        source = tuple(base5_rank(point) for point in PROJECTIVE_POINTS)
        target = tuple(apply_projective_matrix(value, matrix) for value in source)
        score = projective_context_score("plant", source, target)
        self.assertTrue(score.incidence_exact)
        self.assertGreater(score.triple_comparisons, 0)

    def test_dyck_scan_accepts_a_typed_prefix_and_rejects_mismatch(self) -> None:
        spec = DyckSpec("header", "aligned")
        # Header rank zero orders renderer symbols naturally.
        valid = dyck_scan((0, 1, 4, 2), 0, spec)
        self.assertTrue(valid.valid)
        self.assertEqual(2, valid.final_depth)
        invalid = dyck_scan((0, 1, 3), 0, spec)
        self.assertFalse(invalid.valid)
        self.assertEqual(2, invalid.contradiction_index)

    def test_rotor_cycles_are_rotation_invariant(self) -> None:
        cycle = canonical_cycle((2, 3, 4, 0, 1))
        self.assertEqual((0, 1, 2, 3, 4), cycle)
        self.assertTrue(cycle_word_compatible((3, 4, 0, 1, 2, 3), cycle))
        self.assertFalse(cycle_word_compatible((3, 4, 1), cycle))

    def test_exactly_ten_irreducible_quadratics_define_fields(self) -> None:
        fields = field25_specs()
        self.assertEqual(10, len(fields))
        for field in fields:
            for value in ((0, 1), (1, 0), (2, 3), (4, 4)):
                inverse = f25_inv(value, field)
                self.assertEqual((0, 1), f25_mul(value, inverse, field))

    def test_row_code_recovers_a_constant_extended_word(self) -> None:
        spec = RowCodeSpec(Field25Spec(0, 2), (0, 1), False, 0)
        # Pair (2,3) is constant in every column; the third eye is nuisance.
        row = tuple(base5_rank((2, 3, index % 5)) for index in range(26))
        self.assertEqual(((2, 3),), row_code_coefficients(row, spec))

    def test_eye_projective_contexts_all_fail_bijection(self) -> None:
        scores = projective_context_audit(context_sequences())
        self.assertEqual(7, len(scores))
        self.assertTrue(
            all(not score.functional or not score.injective for score in scores)
        )
        self.assertEqual(
            (
                (False, False),
                (False, True),
                (False, False),
                (True, False),
                (False, False),
                (False, False),
                (False, False),
            ),
            tuple((score.functional, score.injective) for score in scores),
        )

    def test_eye_dyck_result_is_frozen(self) -> None:
        streams = {
            name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
        }
        headers = {name: streams[name][0] for name in MESSAGE_ORDER}
        tapes = {
            name: renderer_body_tape(name, streams[name])
            for name in MESSAGE_ORDER
        }
        selected, _ = audit_dyck_syntax(
            tapes,
            headers,
            train_names=P_MESSAGES,
            heldout_names=Q_MESSAGES,
        )
        self.assertEqual(DyckSpec("header", "aligned"), selected.spec)
        self.assertEqual((5, 977), (
            selected.training_prefix,
            selected.training_symbols,
        ))
        self.assertEqual((26, 2190), (
            selected.heldout_prefix,
            selected.heldout_symbols,
        ))
        self.assertEqual((0, 0), (
            selected.training_valid_panels,
            selected.heldout_valid_panels,
        ))

    def test_eye_rotor_result_is_frozen(self) -> None:
        raw_bodies = {
            name: MESSAGES[name][3:] for name in MESSAGE_ORDER
        }
        audit = audit_rotor_router(
            raw_bodies,
            train_names=P_MESSAGES,
            heldout_names=Q_MESSAGES,
        )
        self.assertFalse(audit.training.exact)
        self.assertIsNone(audit.heldout)
        assert audit.training.contradiction is not None
        self.assertEqual(
            ("east1", 0, (1, 1, 2, 0, 1)),
            (
                audit.training.contradiction.panel,
                audit.training.contradiction.current,
                audit.training.contradiction.prefix,
            ),
        )

    def test_eye_f25_row_code_result_is_frozen(self) -> None:
        streams = {
            name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
        }
        audit = audit_row_codes(
            streams,
            train_names=P_MESSAGES,
            heldout_names=Q_MESSAGES,
        )
        self.assertEqual(
            RowCodeSpec(Field25Spec(0, 2), (0, 1), False, 0),
            audit.selected,
        )
        self.assertEqual((0, 10), (
            audit.training.exact_rows,
            audit.training.rows,
        ))
        self.assertEqual((0, 24), (
            audit.heldout.exact_rows,
            audit.heldout.rows,
        ))
        self.assertEqual((), audit.exact_training_specs)


if __name__ == "__main__":
    unittest.main()
