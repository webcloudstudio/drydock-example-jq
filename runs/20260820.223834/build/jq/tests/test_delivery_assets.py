import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "sources"))
import run_conformance as harness


class DeliveryAssetTests(unittest.TestCase):
    def test_corpus_and_exclusions_are_authoritative(self) -> None:
        cases = harness.parse_corpus(
            harness.CORPUS.read_text(encoding="utf-8")
        )
        excluded = harness.apply_exclusions(
            cases, harness.parse_exclusions(harness.EXCLUSIONS)
        )

        self.assertEqual(len(cases), 550)
        self.assertEqual(len(excluded), 13)

    def test_harness_exposes_staged_interfaces(self) -> None:
        self.assertTrue(harness.CORPUS.is_file())
        self.assertTrue(harness.EXCLUSIONS.is_file())
        self.assertTrue(callable(harness.parse_corpus))
        self.assertTrue(callable(harness.apply_exclusions))


if __name__ == "__main__":
    unittest.main()
