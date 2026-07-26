import unittest

from eye_mystery.petri_triangle_order import (
    EYE_ACCEPTED_ORDERS,
    PETRI_SOURCE_ORDERS,
    global_orientation_matches,
    orientation_signature,
    signed_double_area,
)


class PetriTriangleOrderTests(unittest.TestCase):
    def test_frozen_coordinates_have_expected_exact_areas(self) -> None:
        self.assertEqual(
            {
                name: signed_double_area(value)
                for name, value in PETRI_SOURCE_ORDERS.items()
            },
            {"up": 4, "down": -4},
        )
        self.assertEqual(
            {
                name: signed_double_area(value)
                for name, value in EYE_ACCEPTED_ORDERS.items()
            },
            {"down": 4, "up": 4},
        )

    def test_source_alternates_winding_but_eye_order_does_not(self) -> None:
        self.assertEqual(
            orientation_signature(PETRI_SOURCE_ORDERS), {"up": 1, "down": -1}
        )
        self.assertEqual(
            orientation_signature(EYE_ACCEPTED_ORDERS), {"down": 1, "up": 1}
        )

    def test_no_single_global_symmetry_transfers_both_orders(self) -> None:
        self.assertEqual(global_orientation_matches(), ())

    def test_orientation_sign_is_translation_invariant(self) -> None:
        translated = tuple((x + 19, y - 7) for x, y in PETRI_SOURCE_ORDERS["up"])
        self.assertEqual(
            signed_double_area(translated),
            signed_double_area(PETRI_SOURCE_ORDERS["up"]),
        )


if __name__ == "__main__":
    unittest.main()
