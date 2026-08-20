import unittest
from pathlib import Path


METADATA = Path(__file__).parents[1] / "METADATA.md"


class MetadataContractTests(unittest.TestCase):
    def test_declares_executable_and_approved_runtime(self) -> None:
        text = METADATA.read_text(encoding="utf-8")
        self.assertIn("./jq", text)
        self.assertIn("Python", text)
        self.assertIn("standard library", text)

    def test_declares_compact_filter_interface(self) -> None:
        text = METADATA.read_text(encoding="utf-8")
        self.assertIn("-c", text)
        self.assertIn("standard input", text)
        self.assertIn("standard output", text)


if __name__ == "__main__":
    unittest.main()
