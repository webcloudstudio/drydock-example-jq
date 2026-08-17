"""Deterministic contract tests for the foundational project documents."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class FoundationContractTests(unittest.TestCase):
    def test_architecture_contract(self) -> None:
        text = (ROOT / "ARCHITECTURE.md").read_text(encoding="utf-8")
        required = [
            "standalone executable named `jq`",
            "Exit status `0`",
            "Exit status `3`",
            "Exit status `5`",
            "Generators are the primary runtime abstraction",
        ]
        for token in required:
            self.assertIn(token, text)

    def test_architecture_stack_and_boundaries(self) -> None:
        text = (ROOT / "ARCHITECTURE.md").read_text(encoding="utf-8")
        self.assertIn("Python 3.11 or newer, standard library only", text)
        self.assertIn("POSIX `sh`", text)
        self.assertIn("third-party or system jq implementation", text)
        for module in ("Lexer", "Parser", "Runtime", "Values", "Paths", "Builtins"):
            self.assertIn(f"| {module} |", text)

    def test_metadata_declares_cli_delivery_contract(self) -> None:
        fields: dict[str, str] = {}
        for line in (ROOT / "METADATA.md").read_text(encoding="utf-8").splitlines():
            if ":" in line and not line.startswith("#"):
                key, value = line.split(":", 1)
                fields[key] = value.strip()

        self.assertEqual(fields["display_name"], "jq Interpreter")
        self.assertEqual(fields["project_shape"], "cli")
        self.assertEqual(fields["executable"], "./jq")
        self.assertEqual(fields["stack"], "Python 3.11+ standard library; POSIX sh")
        self.assertEqual(fields["runtime_dependencies"], "none")
        self.assertEqual(fields["compile_exit_code"], "3")
        self.assertEqual(fields["runtime_exit_code"], "5")


if __name__ == "__main__":
    unittest.main()
