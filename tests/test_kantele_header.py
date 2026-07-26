import unittest

from eye_mystery.kantele_header import (
    KANTELE_SONGS,
    best_route,
    kantele_header_audit,
    song_hits,
    transformed_body_tape,
)


class KanteleHeaderTests(unittest.TestCase):
    def test_executable_song_fixture_marks_fragment_boundaries(self) -> None:
        tape = (
            *KANTELE_SONGS["portal"],
            5,
            1,
            *KANTELE_SONGS["bomb"],
            5,
            *KANTELE_SONGS["worm"],
        )
        hits = song_hits(tape)
        by_name = {hit.song: hit for hit in hits}
        self.assertTrue(by_name["portal"].exact_fragment)
        self.assertFalse(by_name["bomb"].begins_fragment)
        self.assertTrue(by_name["bomb"].ends_fragment)
        self.assertTrue(by_name["worm"].exact_fragment)

    def test_transformed_tapes_stay_in_renderer_alphabet(self) -> None:
        for route in ("identity", "header", "inverse-header"):
            for name in (
                "east1",
                "west1",
                "east2",
                "west2",
                "east3",
                "west3",
                "east4",
                "west4",
                "east5",
            ):
                tape = transformed_body_tape(name, route=route)
                self.assertTrue(tape)
                self.assertLessEqual(max(tape), 5)

    def test_control_group_contains_observation(self) -> None:
        audit = kantele_header_audit()
        self.assertEqual(audit.control_count, 120)
        self.assertGreaterEqual(audit.exact_tail_count, 1)
        self.assertGreaterEqual(
            audit.maximum_control_score,
            audit.observed.selection_score,
        )
        self.assertEqual(best_route(), audit.observed)


if __name__ == "__main__":
    unittest.main()
