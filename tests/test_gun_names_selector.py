import unittest

from eye_mystery.gun_names_selector import (
    a1z26_length,
    alphabetical_deck,
    first_letter,
    indexed_letter,
    last_letter,
    map_messages,
)


class GunNamesSelectorTests(unittest.TestCase):
    def test_natural_features(self) -> None:
        self.assertEqual(first_letter(0, "Type x"), 19)
        self.assertEqual(last_letter(0, "Type x"), 23)
        self.assertEqual(a1z26_length(0, "Type x"), 4)
        self.assertEqual(indexed_letter(2)(2, "Online"), 11)

    def test_maps_whole_or_body(self) -> None:
        mapping = tuple(index % 26 for index in range(83))
        messages = {"m": (1, 2, 82)}
        self.assertEqual(
            map_messages(messages, mapping, omit_marker=False)["m"],
            (1, 2, 4),
        )
        self.assertEqual(
            map_messages(messages, mapping, omit_marker=True)["m"],
            (2, 4),
        )

    def test_alphabetical_deck_is_a_permutation(self) -> None:
        names = tuple(f"word-{82 - index:02}" for index in range(83))
        self.assertEqual(alphabetical_deck(names)[:3], (82, 81, 80))
        self.assertEqual(alphabetical_deck(names, reverse=True)[:3], (0, 1, 2))


if __name__ == "__main__":
    unittest.main()
