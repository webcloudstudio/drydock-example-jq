"""Boundary tests for the foundational interpreter architecture."""

import json
import subprocess
import sys
import unittest
from pathlib import Path

from jq_interpreter import CompileError, Interpreter, MODULE_BOUNDARIES
from jq_interpreter.architecture import COMPILE_EXIT, RUNTIME_EXIT
from jq_interpreter.runtime import EvaluationContext
from jq_interpreter.paths import Path as JsonPath, get_path

ROOT = Path(__file__).parents[1]
EXECUTABLE = ROOT / "jq"


class ArchitectureTests(unittest.TestCase):
    def test_module_boundaries_name_each_foundational_subsystem(self) -> None:
        modules = {boundary.module for boundary in MODULE_BOUNDARIES}
        self.assertTrue({
            "jq",
            "jq_interpreter.lexer",
            "jq_interpreter.parser",
            "jq_interpreter.evaluator",
            "jq_interpreter.runtime",
            "jq_interpreter.builtins",
        } <= modules)

    def test_each_input_gets_isolated_evaluation_context(self) -> None:
        first = EvaluationContext()
        second = EvaluationContext()
        first.bindings["answer"] = 42
        self.assertEqual(second.bindings, {})

    def test_diagnostics_use_declared_process_exit_contract(self) -> None:
        self.assertEqual((COMPILE_EXIT, RUNTIME_EXIT), (3, 5))

    def test_special_numeric_literals_are_emitted_as_json_null(self) -> None:
        result = subprocess.run(
            [sys.executable, str(EXECUTABLE), "-c", "nan, infinite"],
            input="null\n",
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.splitlines(), ["null", "null"])

    def test_unicode_is_decoded_and_compactly_reencoded(self) -> None:
        result = subprocess.run(
            [sys.executable, str(EXECUTABLE), "-c", "."],
            input='"\\u03bc"\n',
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout), "μ")

    def test_identity_preserves_order_and_multiplicity(self) -> None:
        outputs = list(Interpreter(".").run([1, 2, 2]))
        self.assertEqual(outputs, [1, 2, 2])

    def test_compile_failure_is_distinct(self) -> None:
        with self.assertRaises(CompileError):
            Interpreter("not-a-filter")

    def test_path_read_does_not_mutate_value(self) -> None:
        value = {"nested": {"answer": 42}}
        self.assertEqual(get_path(value, JsonPath(("nested", "answer"))), 42)
        self.assertEqual(value, {"nested": {"answer": 42}})

    def test_executable_streams_compact_json_lines(self) -> None:
        result = subprocess.run(
            [sys.executable, str(EXECUTABLE), "-c", "."],
            input='{"a": 1}\n[2, 3]\n',
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(
            [json.loads(line) for line in result.stdout.splitlines()],
            [{"a": 1}, [2, 3]],
        )

    def test_executable_reports_compile_exit_three(self) -> None:
        result = subprocess.run(
            [sys.executable, str(EXECUTABLE), "-c", "x"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 3)

    def test_executable_reports_runtime_exit_five(self) -> None:
        result = subprocess.run(
            [sys.executable, str(EXECUTABLE), "-c", "error"],
            input="null\n",
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 5)
        self.assertNotEqual(result.stderr, "")

    def test_runtime_failure_keeps_prior_generator_output(self) -> None:
        result = subprocess.run(
            [sys.executable, str(EXECUTABLE), "-c", "1, error"],
            input="null\n",
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 5)
        self.assertEqual(result.stdout.splitlines(), ["1"])
        self.assertNotEqual(result.stderr, "")

    def test_runtime_diagnostic_is_not_written_to_stdout(self) -> None:
        result = subprocess.run(
            [sys.executable, str(EXECUTABLE), "-c", "error"],
            input="null\n",
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 5)
        self.assertEqual(result.stdout, "")
        self.assertNotEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
