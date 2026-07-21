from random import Random
import unittest

from eye_mystery.trie_checksum import random_signature_preserving_relabeling


class SignatureRelabelingTests(unittest.TestCase):
    def test_random_mapping_preserves_constraints_and_fixed_labels(self) -> None:
        vectors = (
            (1, 1, 0, 0, 2, 2),
            (3, 3, 4, 4, 5, 5),
        )
        mapping = random_signature_preserving_relabeling(
            6,
            vectors,
            Random(3),
            fixed_labels=(1,),
        )
        self.assertEqual(set(mapping), set(range(6)))
        self.assertEqual(mapping[1], 1)
        for vector in vectors:
            before = sum(label * count for label, count in enumerate(vector))
            after = sum(mapping[label] * count for label, count in enumerate(vector))
            self.assertEqual(before, after)
        for label, replacement in enumerate(mapping):
            self.assertEqual(
                tuple(vector[label] for vector in vectors),
                tuple(vector[replacement] for vector in vectors),
            )


if __name__ == "__main__":
    unittest.main()
