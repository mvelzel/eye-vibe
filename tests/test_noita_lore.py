import unittest

from eye_mystery.corpus import MESSAGES
from eye_mystery.noita_lore import ORB_LORE_KEYS, absolute_sum_key, letters_only


class NoitaLoreTests(unittest.TestCase):
    def test_has_nine_nonempty_creation_lore_keys(self) -> None:
        self.assertEqual(len(ORB_LORE_KEYS), 9)
        self.assertEqual(len({name for name, _ in ORB_LORE_KEYS}), 9)
        self.assertTrue(all(key.isalpha() and key.isupper() for _, key in ORB_LORE_KEYS))

    def test_normalization_preserves_finnish_letters(self) -> None:
        self.assertEqual(letters_only("Yö, jäät!"), "YÖJÄÄT")

    def test_absolute_lore_index_is_reproducible_on_verified_corpus(self) -> None:
        output = absolute_sum_key(MESSAGES["west4"][:45], ORB_LORE_KEYS[0][1])
        self.assertEqual(output, "KEENKESIKISKKKS")


if __name__ == "__main__":
    unittest.main()
