import random
import unittest

from eye_mystery.fourteenth_selector import (
    EyeSelectorSpec,
    base5_digits,
    global_relabel,
    interleave_selector_lanes,
    render_selector,
    selector_coordinates,
    selector_specs,
)
from eye_mystery.practice_cipher4_routes import canonical_pattern


class FourteenthSelectorTests(unittest.TestCase):
    def test_base5_digits_round_trip_complete_cube(self) -> None:
        for value in range(125):
            a, b, c = base5_digits(value)
            self.assertEqual(25 * a + 5 * b + c, value)

    def test_catalog_is_complete_and_unique(self) -> None:
        specs = selector_specs()
        self.assertEqual(3 * (32 + 120 * 32), len(specs))
        self.assertEqual(len(specs), len(set(specs)))

    def test_selector_interleave_round_trip(self) -> None:
        selectors = (0, 1, 4, 2, 3, 0, 4, 1, 2, 3)
        lanes = (
            (2, 3),
            (5, 6),
            (7, 8),
            (9, 10),
            (11, 12),
        )
        values = interleave_selector_lanes(
            lanes, selectors, selector_index=2
        )
        spec = EyeSelectorSpec(
            2, "separate", tuple(range(5)), 0
        )
        self.assertEqual(tuple(lanes), render_selector(values, spec))

    def test_payload_field_order_is_pattern_equivalent(self) -> None:
        values = tuple(range(83))
        for selector_index in range(3):
            payload, _ = selector_coordinates(values, selector_index)
            indexes = tuple(
                index for index in range(3) if index != selector_index
            )
            reversed_payload = []
            for value in values:
                digits = base5_digits(value)
                reversed_payload.append(
                    5 * digits[indexes[1]] + digits[indexes[0]]
                )
            self.assertEqual(
                canonical_pattern(payload),
                canonical_pattern(reversed_payload),
            )

    def test_global_relabel_preserves_equality_skeleton(self) -> None:
        streams = {
            "a": (1, 7, 1, 22, 7),
            "b": (22, 1, 9, 9),
        }
        labels = list(range(83))
        random.Random(17).shuffle(labels)
        relabeled = global_relabel(streams, labels)
        self.assertEqual(
            canonical_pattern(streams["a"] + streams["b"]),
            canonical_pattern(relabeled["a"] + relabeled["b"]),
        )


if __name__ == "__main__":
    unittest.main()
