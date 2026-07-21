import unittest

from eye_mystery.noita_secret_messages import (
    SECRET_MESSAGES,
    letters_only,
    words_only,
)


class NoitaSecretMessageTests(unittest.TestCase):
    def test_exact_message_set_and_census(self) -> None:
        self.assertEqual(tuple(SECRET_MESSAGES), tuple(f"G{i}" for i in range(1, 13)))
        self.assertEqual(len(letters_only(SECRET_MESSAGES["G1"])), 623)
        self.assertEqual(len(letters_only(SECRET_MESSAGES["G9"])), 52)
        self.assertEqual(
            sum(len(letters_only(text)) for text in SECRET_MESSAGES.values()),
            1946,
        )

    def test_normalization_preserves_word_boundaries_only(self) -> None:
        self.assertEqual(words_only("Why?  It's here."), "why it s here")
        self.assertEqual(letters_only("Why?  It's here."), "whyitshere")


if __name__ == "__main__":
    unittest.main()
