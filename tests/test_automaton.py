import unittest

from eye_mystery.automaton import OPERATIONS, readout_pattern, trace


class AutomatonTests(unittest.TestCase):
    def test_operation_orders_and_periodic_readout(self) -> None:
        message = (0, 1, 2, 3, 4, 0, 1, 2, 3)
        states = trace(message)
        expected = []
        state = tuple(range(25))
        for offset in range(0, len(message), 3):
            for eye in message[offset : offset + 3]:
                state = OPERATIONS[eye](state)
            expected.append(state)
        self.assertEqual(states, tuple(expected))
        self.assertEqual(
            readout_pattern(states, (2, 18, 2)),
            (states[0][2], states[1][18], states[2][2]),
        )

    def test_periodic_readout_rejects_invalid_patterns(self) -> None:
        states = trace((0, 1, 2))
        with self.assertRaises(ValueError):
            readout_pattern(states, ())
        with self.assertRaises(ValueError):
            readout_pattern(states, (25,))


if __name__ == "__main__":
    unittest.main()
