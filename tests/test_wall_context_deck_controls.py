from __future__ import annotations

import os
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class WallContextDeckControlTests(unittest.TestCase):
    def test_combined_screen_and_matched_control_execute(self) -> None:
        environment = dict(os.environ)
        environment["PYTHONPATH"] = str(ROOT / "src")
        completed = subprocess.run(
            (
                sys.executable,
                str(ROOT / "scripts" / "audit_wall_context_deck_controls.py"),
                "--controls",
                "1",
                "--seed",
                "0x83a11",
            ),
            cwd=ROOT,
            env=environment,
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn("models=480", completed.stdout)
        self.assertIn("observed_all_seven=30", completed.stdout)
        self.assertIn("observed_bridge_joint=25", completed.stdout)
        self.assertIn(
            "null=one common random permutation of 83 Wall context rows",
            completed.stdout,
        )


if __name__ == "__main__":
    unittest.main()
