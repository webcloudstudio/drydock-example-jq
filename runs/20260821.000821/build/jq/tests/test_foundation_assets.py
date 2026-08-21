import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "sources"))

import run_conformance as harness


class FoundationAssetsTest(unittest.TestCase):
    def test_corpus_and_exclusions_are_consistent(self) -> None:
        cases = harness.parse_corpus(harness.CORPUS.read_text(encoding="utf-8"))
        excluded = harness.apply_exclusions(
            cases, harness.parse_exclusions(harness.EXCLUSIONS)
        )
        self.assertEqual(len(cases), 550)
        self.assertEqual(len(excluded), 13)

    def test_required_assets_and_parser_interfaces_are_staged(self) -> None:
        required = {
            "jq-manual.txt",
            "jq.test",
            "parser.y",
            "lexer.l",
            "builtin.jq",
            "run_conformance.py",
            "full_test.sh",
            "exclusions.txt",
        }
        self.assertTrue(all((ROOT / "sources" / name).is_file() for name in required))
        self.assertTrue(callable(harness.parse_corpus))
        self.assertTrue(callable(harness.parse_exclusions))
        self.assertTrue(callable(harness.apply_exclusions))


if __name__ == "__main__":
    unittest.main()
