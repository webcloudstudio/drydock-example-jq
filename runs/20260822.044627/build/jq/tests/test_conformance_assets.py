"""In-process validation for the immutable conformance asset staging."""

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
SOURCES = ROOT / "sources"
sys.path.insert(0, str(SOURCES))

import run_conformance as harness


class ConformanceAssetTests(unittest.TestCase):
    def test_pinned_corpus_and_exclusions_are_consistent(self) -> None:
        cases = harness.parse_corpus(harness.CORPUS.read_text(encoding="utf-8"))
        excluded = harness.apply_exclusions(
            cases,
            harness.parse_exclusions(harness.EXCLUSIONS),
        )

        self.assertEqual(len(cases), 550)
        self.assertEqual(len(excluded), 13)

    def test_harness_uses_staged_canonical_paths(self) -> None:
        self.assertTrue((SOURCES / "jq.test").is_file())
        self.assertTrue((SOURCES / "exclusions.txt").is_file())
        self.assertTrue((SOURCES / "run_conformance.py").is_file())
        self.assertEqual(harness.CORPUS, (SOURCES / "jq.test").resolve())
        self.assertEqual(harness.EXCLUSIONS, (SOURCES / "exclusions.txt").resolve())

    def test_all_imported_asset_files_are_nonempty(self) -> None:
        expected = {
            "builtin.jq",
            "exclusions.txt",
            "full_test.sh",
            "jq-manual.txt",
            "jq.test",
            "lexer.l",
            "parser.y",
            "run_conformance.py",
        }
        self.assertEqual(
            {path.name for path in SOURCES.iterdir() if path.is_file()},
            expected,
        )
        for name in expected:
            self.assertGreater((SOURCES / name).stat().st_size, 0)


if __name__ == "__main__":
    unittest.main()
