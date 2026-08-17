import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(program: str, payload: str = "null\n") -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(ROOT / "jq"), "-c", program],
        input=payload,
        text=True,
        capture_output=True,
    )


class ParserTests(unittest.TestCase):
 def test_arithmetic_precedence_and_grouping(self) -> None:
    result = run("1 + 2 * 2")
    assert result.returncode == 0
    assert json.loads(result.stdout) == 5
    grouped = run("(1 + 2) * 2")
    assert grouped.returncode == 0
    assert json.loads(grouped.stdout) == 6


 def test_definition_and_binding_construct_executable_ast(self) -> None:
    result = run("def inc: . + 1; 4 | inc")
    assert result.returncode == 0
    assert json.loads(result.stdout) == 5

    bound = run(". as $x | [$x, $x + 1]", "7\n")
    assert bound.returncode == 0
    assert json.loads(bound.stdout) == [7, 8]


 def test_reduce_construct_preserves_generator_iteration(self) -> None:
    result = run("reduce .[] as $x (0; . + $x)", "[1, 2, 3]\n")
    assert result.returncode == 0
    assert json.loads(result.stdout) == 6


 def test_malformed_program_has_compile_exit_status(self) -> None:
    result = run("{")
    assert result.returncode == 3


 def test_runtime_error_has_runtime_exit_status(self) -> None:
    result = run("1 / 0")
    assert result.returncode == 5


if __name__ == "__main__":
    unittest.main()
