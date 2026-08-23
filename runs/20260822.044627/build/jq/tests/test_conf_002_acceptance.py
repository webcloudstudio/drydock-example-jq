"""Acceptance coverage for scoped, machine-readable conformance verification."""

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
RUNNER = ROOT / "sources" / "run_conformance.py"


class Conf002AcceptanceTests(unittest.TestCase):
    def test_runner_exposes_scoped_machine_readable_candidate_contract(self) -> None:
        source = RUNNER.read_text(encoding="utf-8")

        self.assertTrue(RUNNER.is_file())
        self.assertIn("JQ", source)
        self.assertIn("--select", source)
        self.assertIn("--json", source)

    def test_scoped_run_executes_cases_and_reports_json(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(RUNNER),
                "--select",
                r"reduce",
                "--json",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            env={**os.environ, "JQ": str(ROOT / "jq")},
            check=False,
        )

        report = json.loads(result.stdout)
        tally = report["summary"]
        self.assertGreater(sum(tally.values()), 0)
        self.assertEqual(tally["fail"], 0)
        self.assertEqual(tally["error"], 0)
        self.assertEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
