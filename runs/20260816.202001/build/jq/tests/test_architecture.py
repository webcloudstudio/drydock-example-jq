import inspect
import json
import subprocess
import sys
from pathlib import Path
import unittest

import jq_lexer
import jq_parser
import jq_runtime


ROOT = Path(__file__).resolve().parents[1]


class ArchitectureTests(unittest.TestCase):
    def test_public_module_contracts(self) -> None:
        self.assertTrue(callable(jq_lexer.tokenize))
        self.assertTrue(callable(jq_parser.parse))
        self.assertTrue(callable(jq_runtime.evaluate))
        self.assertTrue(inspect.isgeneratorfunction(jq_runtime.evaluate))

    def test_generator_preserves_comma_order(self) -> None:
        program = jq_parser.parse("1, .")
        self.assertEqual(list(jq_runtime.evaluate(program, 2)), [1, 2])

    def test_cli_compact_output(self) -> None:
        result = subprocess.run(
            [str(ROOT / "jq"), "-c", "."],
            input='{"a": 1}\n', text=True, capture_output=True, check=False,
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout), {"a": 1})

    def test_cli_compile_failure_status(self) -> None:
        result = subprocess.run(
            [str(ROOT / "jq"), "-c", "("],
            input="null\n", text=True, capture_output=True, check=False,
        )
        self.assertEqual(result.returncode, 3)


if __name__ == "__main__":
    unittest.main()
