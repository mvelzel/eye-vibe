from __future__ import annotations

import unittest

from eye_mystery.conformance_grid import marker_control_edge
from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.s3_transducer import (
    calibrate_body_assignments,
    scan_s3_direction_transducers,
)


class S3TransducerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        bodies = tuple(MESSAGES[name][3:] for name in MESSAGE_ORDER)
        cls.edges = tuple(
            marker_control_edge(trigram_values(MESSAGES[name])[0])
            for name in MESSAGE_ORDER
        )
        cls.scan = scan_s3_direction_transducers(bodies, cls.edges)

    def test_unique_eight_of_nine_fit(self) -> None:
        self.assertEqual(
            self.scan.match_histogram,
            ((0, 112), (1, 460), (2, 1035), (3, 1211), (4, 878),
             (5, 430), (6, 161), (7, 32), (8, 1)),
        )
        self.assertEqual(self.scan.best_match_count, 8)
        self.assertEqual(len(self.scan.best_models), 1)
        best = self.scan.best_models[0]
        self.assertEqual(best.eye_order, (2, 1, 0))
        self.assertEqual(
            best.direction_operations,
            ((1, 2, 0), (2, 1, 0), (0, 1, 2), (2, 0, 1), (0, 2, 1)),
        )
        self.assertEqual(best.body_outputs[6], (2, 1, 0))

    def test_near_fit_is_ordinary_under_intact_body_reassignment(self) -> None:
        result = calibrate_body_assignments(self.scan.all_outputs, self.edges)
        self.assertEqual(result.total, 362_880)
        self.assertEqual(result.below_eight, 5_976)
        self.assertEqual(result.exactly_eight, 282_468)
        self.assertEqual(result.all_nine, 74_436)


if __name__ == "__main__":
    unittest.main()
