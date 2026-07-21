from __future__ import annotations

import unittest

from eye_mystery.s3_context import last_family_s3_context_audit


class S3ContextTests(unittest.TestCase):
    def test_direct_header_generators_do_not_fit_body_context_maps(self) -> None:
        result = last_family_s3_context_audit()
        self.assertEqual((result.first_size, result.second_size), (25, 25))
        self.assertEqual(len(result.first_square), 7)
        self.assertEqual(len(result.first_square_violations), 7)
        self.assertEqual(len(result.second_square), 8)
        self.assertEqual(len(result.second_square_violations), 8)
        self.assertEqual(result.braid_conflict, (31, 41, 69))
        self.assertFalse(result.coxeter_assignment_survives)


if __name__ == "__main__":
    unittest.main()
