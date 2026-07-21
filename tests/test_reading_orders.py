import unittest

from eye_mystery.corpus import MESSAGES, trigram_values
from eye_mystery.reading_orders import is_canonical_range, values_for_orders


class ReadingOrderTests(unittest.TestCase):
    def test_identity_reproduces_canonical_values(self) -> None:
        order = (0, 1, 2)
        values = values_for_orders(MESSAGES["east1"], order, order)
        self.assertEqual(values, trigram_values(MESSAGES["east1"]))

    def test_canonical_range(self) -> None:
        self.assertTrue(is_canonical_range(range(83)))
        self.assertFalse(is_canonical_range(range(82)))


if __name__ == "__main__":
    unittest.main()
