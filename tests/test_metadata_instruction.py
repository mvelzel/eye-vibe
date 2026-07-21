import unittest

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.metadata_instruction import (
    branch_exit_records,
    corrected_exit_residues,
)


class MetadataInstructionTests(unittest.TestCase):
    def setUp(self) -> None:
        order = MESSAGE_ORDER[-1:] + MESSAGE_ORDER[:-1]
        self.bodies = {
            name: trigram_values(MESSAGES[name])[1:] for name in order
        }

    def test_breadth_first_records_are_exact(self) -> None:
        records = branch_exit_records(self.bodies)
        self.assertEqual(tuple(record.depth for record in records), (2, 5, 24, 9, 20))
        self.assertEqual(
            tuple(record.exit_labels for record in records),
            ((49, 48), (2, 69, 23), (80, 29, 69), (2, 78), (33, 77, 60)),
        )

    def test_depth_corrected_sums_form_paired_identity(self) -> None:
        records = branch_exit_records(self.bodies)
        self.assertEqual(corrected_exit_residues(records), (99, 99, 0, 89, 89))


if __name__ == "__main__":
    unittest.main()
