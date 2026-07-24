from __future__ import annotations

import unittest

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.factoradic_headers import P_MESSAGES, Q_MESSAGES, compose
from eye_mystery.hidden_geometry import context_sequences
from eye_mystery.seventh_wide import renderer_body_tape
from eye_mystery.sixteenth_second import (
    DUADS,
    ONE125,
    PENTADS,
    SYNTHEMES,
    Field125Spec,
    GF125Representation,
    NecklaceSpec,
    OuterSpec,
    apply_mobius,
    audit_necklaces,
    audit_outer_actions,
    duval_factor_count,
    field125_specs,
    f125_inv,
    f125_mul,
    fit_mobius_three,
    gf125_representations,
    least_rotation_index,
    mobius_context_score,
    outer_automorphism,
    outer_specs,
    primitive_period,
)


def cycle_lengths(permutation: tuple[int, ...]) -> tuple[int, ...]:
    seen = set()
    lengths = []
    for start in range(len(permutation)):
        if start in seen:
            continue
        current = start
        length = 0
        while current not in seen:
            seen.add(current)
            current = permutation[current]
            length += 1
        lengths.append(length)
    return tuple(sorted(lengths))


class SixteenthSecondTests(unittest.TestCase):
    def test_duad_syntheme_pentad_counts(self) -> None:
        self.assertEqual((15, 15, 6), (
            len(DUADS),
            len(SYNTHEMES),
            len(PENTADS),
        ))
        self.assertEqual(1440, len(outer_specs()))

    def test_outer_map_is_a_homomorphism_and_not_inner(self) -> None:
        transposition = (1, 0, 2, 3, 4, 5)
        three_cycle = (1, 2, 0, 3, 4, 5)
        self.assertEqual((2, 2, 2), cycle_lengths(outer_automorphism(transposition)))
        self.assertEqual(
            outer_automorphism(compose(transposition, three_cycle)),
            compose(
                outer_automorphism(transposition),
                outer_automorphism(three_cycle),
            ),
        )

    def test_booth_rotation_and_word_diagnostics(self) -> None:
        self.assertEqual(2, least_rotation_index((2, 3, 0, 1)))
        self.assertEqual(2, primitive_period((0, 1, 0, 1)))
        self.assertEqual(4, primitive_period((0, 1, 0, 2)))
        self.assertGreaterEqual(duval_factor_count((2, 1, 0, 1, 2)), 1)

    def test_exactly_40_irreducible_cubics(self) -> None:
        self.assertEqual(40, len(field125_specs()))
        self.assertEqual(120, len(gf125_representations()))
        for field in field125_specs():
            value = (1, 2, 3)
            self.assertEqual(ONE125, f125_mul(value, f125_inv(value, field), field))

    def test_mobius_fit_recovers_planted_map(self) -> None:
        representation = GF125Representation(Field125Spec(0, 1, 1), 1)
        coefficients = ((1, 0, 1), (0, 2, 3), (0, 1, 0), (1, 1, 1))
        edges = []
        for source in range(125):
            target = apply_mobius(source, representation, coefficients)
            if target is not None:
                edges.append((source, target))
            if len(edges) == 6:
                break
        recovered = fit_mobius_three(edges[:3], representation)
        self.assertIsNotNone(recovered)
        assert recovered is not None
        self.assertEqual(
            tuple(target for _, target in edges),
            tuple(apply_mobius(source, representation, recovered) for source, _ in edges),
        )

    def test_eye_outer_action_result_is_frozen(self) -> None:
        streams = {
            name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
        }
        headers = {name: streams[name][0] for name in MESSAGE_ORDER}
        tapes = {
            name: renderer_body_tape(name, streams[name])
            for name in MESSAGE_ORDER
        }
        masks = {
            name: tuple(value == 5 for value in tapes[name])
            for name in MESSAGE_ORDER
        }
        audit = audit_outer_actions(
            tapes,
            headers,
            masks,
            train_names=P_MESSAGES,
            heldout_names=Q_MESSAGES,
        )
        self.assertEqual(OuterSpec(3, "header"), audit.selected.spec)
        self.assertEqual((53, 977), (
            audit.selected.training_mismatches,
            audit.selected.training_symbols,
        ))
        self.assertEqual((364, 2190), (
            audit.selected.heldout_mismatches,
            audit.selected.heldout_symbols,
        ))
        self.assertEqual((), audit.exact_training_specs)

    def test_eye_necklace_result_is_frozen(self) -> None:
        streams = {
            name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
        }
        headers = {name: streams[name][0] for name in MESSAGE_ORDER}
        tapes = {
            name: renderer_body_tape(name, streams[name])
            for name in MESSAGE_ORDER
        }
        selected, scores = audit_necklaces(
            tapes,
            headers,
            train_names=P_MESSAGES,
            heldout_names=Q_MESSAGES,
        )
        self.assertEqual(NecklaceSpec("header", False), selected.spec)
        self.assertEqual((0, 0), (
            selected.training_canonical,
            selected.heldout_canonical,
        ))
        self.assertTrue(
            all(score.training_canonical == score.heldout_canonical == 0 for score in scores)
        )
        self.assertTrue(
            all(panel.primitive for panel in (*selected.training, *selected.heldout))
        )

    def test_selected_eye_gf125_scores_are_frozen(self) -> None:
        representation = GF125Representation(Field125Spec(2, 2, 3), 1)
        scores = tuple(
            mobius_context_score(name, source, target, representation)
            for name, source, target in context_sequences()
        )
        self.assertEqual(
            ((8, 18), (6, 18), (9, 18), (6, 9), (7, 30), (7, 30), (7, 25)),
            tuple((score.matches, score.edges) for score in scores),
        )
        self.assertTrue(all(not score.exact for score in scores))


if __name__ == "__main__":
    unittest.main()
