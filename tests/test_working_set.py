from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/check_working_set.py"
SPEC = importlib.util.spec_from_file_location("check_working_set", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class WorkingSetTests(unittest.TestCase):
    def test_compact_working_set_is_valid(self) -> None:
        self.assertEqual(MODULE.validate(), ())


if __name__ == "__main__":
    unittest.main()

