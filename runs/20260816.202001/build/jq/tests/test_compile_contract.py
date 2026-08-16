import subprocess
import unittest

import jq_parser


class CompileContractTests(unittest.TestCase):
    def test_compile_api_rejects_static_invalid_source(self) -> None:
        with self.assertRaises(Exception):
            jq_parser.parse(". as [] | null")

    def test_compile_api_returns_ast_for_valid_source(self) -> None:
        self.assertIsNotNone(jq_parser.parse("."))

    def test_cli_compile_failure_uses_status_three_and_no_stdout(self) -> None:
        result = subprocess.run(
            ["./jq", "-c", "{"],
            input="null\n",
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 3)
        self.assertEqual(result.stdout, "")

    def test_cli_compile_diagnostics_are_on_stderr(self) -> None:
        result = subprocess.run(
            ["./jq", "-c", "{"],
            input="null\n",
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 3)
        self.assertNotEqual(result.stderr, "")
        self.assertEqual(result.stdout, "")

    def test_runtime_failure_remains_status_five(self) -> None:
        result = subprocess.run(
            ["./jq", "-c", ".[]"],
            input="1\n",
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 5)
        self.assertEqual(result.stdout, "")

    def test_break_requires_a_label(self) -> None:
        with self.assertRaises(jq_parser.ParseError):
            jq_parser.parse(". as $foo | break $foo")


if __name__ == "__main__":
    unittest.main()
