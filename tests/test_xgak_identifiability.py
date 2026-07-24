import unittest

from eye_mystery.xgak_identifiability import (
    one_swap_reconvergence_counterexample,
    run_xgak,
)


class XGAKIdentifiabilityTests(unittest.TestCase):
    def test_one_swap_reconvergence_is_observationally_ambiguous(self) -> None:
        case = one_swap_reconvergence_counterexample()
        self.assertEqual(
            case.ciphertexts,
            ((3, 1, 2, 3, 1), (3, 2, 3, 2, 1)),
        )
        self.assertTrue(
            all(
                left != right
                for ciphertext in case.ciphertexts
                for left, right in zip(ciphertext, ciphertext[1:])
            )
        )
        self.assertEqual(case.ciphertexts[0][0], case.ciphertexts[1][0])
        self.assertEqual(case.ciphertexts[0][-1], case.ciphertexts[1][-1])
        self.assertEqual(
            case.equal_operations[0],
            case.equal_operations[1],
        )
        self.assertNotEqual(
            case.unequal_operations[0],
            case.unequal_operations[1],
        )
        self.assertTrue(case.equal_model_finals_equal)
        self.assertFalse(case.unequal_model_finals_equal)

    def test_rejects_nonpermutation_operation(self) -> None:
        with self.assertRaisesRegex(ValueError, "permutations"):
            run_xgak((0,), ((0, 0),), (0,))


if __name__ == "__main__":
    unittest.main()
