import unittest

from eye_mystery.bwt_mtf import (
    inverse_move_to_front,
    raw_eye_bwt_mtf_audit,
)


class BwtMtfTests(unittest.TestCase):
    def test_inverse_move_to_front(self) -> None:
        self.assertEqual(
            inverse_move_to_front((1, 1, 0, 2), (0, 1, 2)),
            (1, 0, 0, 2),
        )

    def test_raw_eye_pipeline_has_no_first_message_roundtrip(self) -> None:
        audit = raw_eye_bwt_mtf_audit()
        self.assertEqual(audit["candidates"], 2160)
        self.assertEqual(audit["maximum_roundtrips"], 0)
        self.assertEqual(audit["histogram"], ((0, 2160),))
        self.assertEqual(audit["complete"], ())


if __name__ == "__main__":
    unittest.main()
