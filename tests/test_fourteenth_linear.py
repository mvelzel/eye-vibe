import unittest

from eye_mystery.fourteenth_linear import (
    LinearRepresentation,
    fit_shared_recurrence,
    generate_recurrence,
    recurrence_system,
    render_representation,
    representations,
)


class FourteenthLinearTests(unittest.TestCase):
    def test_representation_catalog_is_fixed_and_unique(self) -> None:
        catalog = representations()
        self.assertEqual(8, len(catalog))
        self.assertEqual(len(catalog), len(set(catalog)))
        self.assertEqual(
            {"rank-f83", "difference-f83"},
            {item.name for item in catalog if item.modulus == 83},
        )
        self.assertEqual(
            6, sum(item.modulus == 5 for item in catalog)
        )

    def test_digit_serialization_respects_component_order(self) -> None:
        representation = LinearRepresentation("digits-201-f5", 5)
        self.assertEqual(
            (3, 2, 1, 4, 0, 2),
            render_representation((58, 14), representation),
        )

    def test_shared_solver_recovers_unique_planted_recurrence(self) -> None:
        coefficients = (2, 5, 7)
        streams = (
            generate_recurrence(coefficients, (1, 2, 3), 40, 83),
            generate_recurrence(coefficients, (4, 8, 15), 40, 83),
            generate_recurrence(coefficients, (16, 23, 42), 40, 83),
        )
        result = recurrence_system(streams[:2], 3, 83)
        self.assertTrue(result.unique)
        self.assertEqual(coefficients, result.solution)

    def test_fit_predicts_independent_seed(self) -> None:
        coefficients = (2, 5, 7)
        streams = {
            name: generate_recurrence(coefficients, seed, 40, 83)
            for name, seed in {
                "a": (1, 2, 3),
                "b": (4, 8, 15),
                "c": (16, 23, 42),
            }.items()
        }
        fit = fit_shared_recurrence(
            streams,
            LinearRepresentation("rank-f83", 83),
            3,
            train_names=("a", "b"),
            heldout_names=("c",),
        )
        self.assertTrue(fit.system.unique)
        self.assertEqual(coefficients, fit.system.solution)
        self.assertEqual(fit.heldout_equations, fit.heldout_matches)

    def test_inconsistent_system_is_detected(self) -> None:
        result = recurrence_system(((1, 2, 4, 8), (1, 2, 4, 9)), 1, 83)
        self.assertFalse(result.consistent)
        self.assertGreater(result.augmented_rank, result.rank)


if __name__ == "__main__":
    unittest.main()
