"""Acceptance coverage for conformance asset staging."""

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "sources"))

import run_conformance as harness


class Conf001AcceptanceTests(unittest.TestCase):
    def test_authoritative_corpus_and_exclusions(self) -> None:
        cases = harness.parse_corpus(harness.CORPUS.read_text(encoding="utf-8"))
        excluded = harness.apply_exclusions(
            cases,
            harness.parse_exclusions(harness.EXCLUSIONS),
        )

        self.assertEqual(len(cases), 550)
        self.assertEqual(len(excluded), 13)
        self.assertTrue(harness.CORPUS.is_file())
        self.assertTrue(harness.EXCLUSIONS.is_file())


if __name__ == "__main__":
    unittest.main()
