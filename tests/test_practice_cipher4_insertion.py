import unittest

from eye_mystery.practice_cipher4_insertion import arithmetic_phase_candidates


class PracticeCipher4InsertionTests(unittest.TestCase):
    def test_periodic_sum_insertions_are_recovered(self) -> None:
        stream = [22 + (index * 11) % 57 for index in range(180)]
        for index in range(3, len(stream), 7):
            first = stream[index - 2] - 22
            second = stream[index - 1] - 22
            stream[index] = 22 + (first + second) % 57
        candidates = arithmetic_phase_candidates(
            (stream,),
            maximum_period=7,
            minimum_support=20,
        )
        planted = next(
            candidate
            for candidate in candidates
            if (
                candidate.coordinate,
                candidate.relation,
                candidate.period,
                candidate.phase,
            )
            == ("rank57", "sum_mod", 7, 1)
        )
        self.assertEqual(planted.hits, planted.support)


if __name__ == "__main__":
    unittest.main()
