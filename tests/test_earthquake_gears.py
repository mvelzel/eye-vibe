from __future__ import annotations

import shutil
import unittest

from eye_mystery.earthquake_gears import (
    active_counts,
    allowed_increment_pairs,
    audit_direct_rank,
    direct_parameter_candidates,
    simulate_positions,
    solve_hidden_gear_with_z3,
    solve_relaxed_pairs_with_z3,
    verify_hidden_witness,
    weighted_increment,
)


class EarthquakeGearTests(unittest.TestCase):
    def test_authored_band_counts_and_reverse(self) -> None:
        self.assertEqual((17, 9, 13), active_counts(0, 17))
        self.assertEqual((17, 9, 13), active_counts(0, 17, direction=-1))
        self.assertEqual(39, weighted_increment(0, 17))
        for distance in range(1, 30):
            self.assertEqual(
                {
                    active_counts(phase, distance, direction=1)
                    for phase in range(34)
                },
                {
                    active_counts(phase, distance, direction=-1)
                    for phase in range(34)
                },
            )

    def test_direct_detector_recovers_a_plant(self) -> None:
        distances = (3, 5, 1, 7, 2, 4)
        source = simulate_positions(
            distances,
            phase=2,
            start=11,
        )
        target = simulate_positions(
            distances,
            phase=19,
            start=44,
        )
        audit = audit_direct_rank(
            (("plant", source, target),),
            plaintext_alphabet_size=8,
            directions=(1,),
            scales=(1,),
        )
        self.assertTrue(audit.complete)
        self.assertEqual(6, audit.best_matched_transitions)

    def test_equal_weight_same_distance_pair_family(self) -> None:
        pairs = allowed_increment_pairs(plaintext_alphabet_size=26)
        self.assertEqual(159, len(pairs))
        self.assertIn((39, 39), pairs)

    def test_all_weight_direct_screen_recovers_a_plant(self) -> None:
        weights = (1, 7, 11)
        distances = (3, 5, 1, 7)
        source = simulate_positions(
            distances,
            phase=2,
            start=11,
            weights=weights,
        )
        target = simulate_positions(
            distances,
            phase=19,
            start=44,
            weights=weights,
        )
        screen = direct_parameter_candidates(
            (("plant", source, target),),
            plaintext_alphabet_size=8,
            scales=(1,),
        )
        self.assertTrue(screen.compatible)
        self.assertIn((1, 7, 11), screen.survivors)

    @unittest.skipUnless(shutil.which("z3"), "z3 executable unavailable")
    def test_relaxed_pair_detector_recovers_a_plant(self) -> None:
        distances = (3, 5, 1, 7, 2, 4)
        source = simulate_positions(distances, phase=2, start=11)
        target = simulate_positions(distances, phase=19, start=44)
        contexts = (("plant", source, target),)
        result = solve_relaxed_pairs_with_z3(
            contexts,
            plaintext_alphabet_size=8,
            timeout_ms=10_000,
        )
        self.assertEqual("sat", result.status)
        self.assertIsNotNone(result.coordinates)

    @unittest.skipUnless(shutil.which("z3"), "z3 executable unavailable")
    def test_hidden_solver_witness_replays(self) -> None:
        distances = (2,)
        source = simulate_positions(
            distances,
            phase=4,
            start=3,
            weights=(1, 7, 11),
        )
        target = simulate_positions(
            distances,
            phase=23,
            start=51,
            weights=(1, 7, 11),
        )
        contexts = (("plant", source, target),)
        result = solve_hidden_gear_with_z3(
            contexts,
            plaintext_alphabet_size=2,
            direction=1,
            weights=(1, 7, 11),
            timeout_ms=10_000,
        )
        self.assertEqual("sat", result.status)
        self.assertIsNotNone(result.witness)
        assert result.witness is not None
        self.assertTrue(
            verify_hidden_witness(contexts, result.witness, direction=1)
        )


if __name__ == "__main__":
    unittest.main()
