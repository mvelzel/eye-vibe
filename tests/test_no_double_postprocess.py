import unittest

from eye_mystery.no_double_postprocess import no_double_postprocess_witnesses


class NoDoublePostprocessTests(unittest.TestCase):
    def test_function_triple_is_recovered(self) -> None:
        witnesses = no_double_postprocess_witnesses(
            {"plant": (5, 7, 2, 12, 35, 20)}
        )
        self.assertTrue(
            any(
                witness.message == "plant"
                and witness.position == 0
                and witness.model.startswith("function-triple-raw")
                for witness in witnesses
            )
        )

    def test_multiplier_signature_is_recovered(self) -> None:
        witnesses = no_double_postprocess_witnesses(
            {"plant": (1, 3, 2, 5, 40)}
        )
        self.assertIn(
            "multiples-original-3,2,5",
            tuple(witness.model for witness in witnesses),
        )


if __name__ == "__main__":
    unittest.main()
