from __future__ import annotations

import random
import unittest

from eye_mystery.arbitrary_gak_sat import encrypt_messages
from eye_mystery.corpus import MESSAGES, trigram_values
from eye_mystery.gak_fixed_point import find_stabilizer_contradictions
from scripts.check_waite_m3_suffix import EAST2_RAW_OFFSET, WAITE_M3_SUFFIX


class GAKFixedPointTests(unittest.TestCase):
    def test_detects_a_planted_fixed_point_contradiction(self) -> None:
        # Under one repeated operation, equal outputs followed by a different
        # output are impossible: the operation has already fixed the top.
        contradictions = find_stabilizer_contradictions(
            "AAAA",
            (0, 0, 1, 0),
        )
        self.assertTrue(contradictions)

    def test_valid_random_gak_fixture_has_no_contradiction(self) -> None:
        rng = random.Random(270727)
        size = 9
        initial = tuple(range(size))
        operations = []
        for _ in range(4):
            operation = list(range(size))
            rng.shuffle(operation)
            operations.append(tuple(operation))
        plaintext = tuple(rng.randrange(4) for _ in range(40))
        ciphertext = encrypt_messages((plaintext,), initial, operations)[0]
        self.assertEqual(
            find_stabilizer_contradictions(plaintext, ciphertext),
            (),
        )

    def test_waite_suffix_has_a_five_observation_certificate(self) -> None:
        ciphertext = trigram_values(MESSAGES["east2"])[EAST2_RAW_OFFSET:]
        contradictions = find_stabilizer_contradictions(
            WAITE_M3_SUFFIX,
            ciphertext,
        )
        self.assertEqual(len(contradictions), 4)
        shortest = contradictions[0]
        self.assertEqual(shortest.observation_offsets, (20, 25, 64, 68, 73))
        self.assertEqual("".join(shortest.first.word), "EST,")
        self.assertFalse(shortest.first.fixes_top)
        self.assertEqual("".join(shortest.second.word), " THE ")
        self.assertTrue(shortest.second.fixes_top)
        self.assertEqual("".join(shortest.combined.word), "EST, THE ")
        self.assertTrue(shortest.combined.fixes_top)


if __name__ == "__main__":
    unittest.main()
