import unittest

from eye_mystery.corpus import MESSAGE_ORDER
from eye_mystery.source_message_tree import (
    SourceEntry,
    eye_lengths,
    message_tree_matches,
    message_tree_partials,
)


class SourceMessageTreeTests(unittest.TestCase):
    def test_finds_synthetic_complete_tree(self) -> None:
        lengths = eye_lengths()
        upper = "AB" + "U" * 22
        lower5 = "ABLLL"
        lower9 = lower5 + "N" * 4
        lower20 = lower9 + "D" * 11
        prefixes = {
            "east1": upper,
            "west1": upper,
            "east2": upper,
            "west2": lower5,
            "east3": lower9,
            "west3": lower5,
            "east4": lower20,
            "west4": lower20,
            "east5": lower20,
        }
        fillers = {
            "east1": "C",
            "west1": "D",
            "east2": "E",
            "west2": "F",
            "east3": "G",
            "west3": "H",
            "east4": "I",
            "west4": "J",
            "east5": "K",
        }
        entries = [
            SourceEntry(
                name,
                prefixes[name]
                + fillers[name] * (lengths[name] - len(prefixes[name])),
            )
            for name in MESSAGE_ORDER
        ]
        matches = message_tree_matches(entries)
        self.assertEqual(len(matches), 1)
        self.assertEqual(tuple(matches[0].by_name()), MESSAGE_ORDER)
        partials = message_tree_partials(entries)
        self.assertEqual(partials.upper24, (upper,))
        self.assertEqual(partials.deep20, (lower20,))
        self.assertEqual(partials.nested9, (lower20,))
        self.assertEqual(partials.lower6, (lower20,))
        self.assertEqual(partials.roots, ((upper, lower20),))

    def test_rejects_wrong_root(self) -> None:
        lengths = eye_lengths()
        entries = [
            SourceEntry(name, chr(65 + index) * lengths[name])
            for index, name in enumerate(MESSAGE_ORDER)
        ]
        self.assertEqual(message_tree_matches(entries), ())


if __name__ == "__main__":
    unittest.main()
