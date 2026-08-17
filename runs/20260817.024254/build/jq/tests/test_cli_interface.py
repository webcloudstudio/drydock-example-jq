import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).parents[1]

def run(program: str, text: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([str(ROOT / "jq"), "-c", program], input=text, text=True, capture_output=True)

def test_multiple_json_texts_preserve_order() -> None:
    result = run(".value", '{"value":1}\n{"value":2}\n{"value":3}\n')
    assert result.returncode == 0
    assert [json.loads(line) for line in result.stdout.splitlines()] == [1, 2, 3]

def test_generator_emits_one_line_per_result() -> None:
    result = run("range(3)", "null\n")
    assert result.returncode == 0
    assert [json.loads(line) for line in result.stdout.splitlines()] == [0, 1, 2]

def test_compile_and_runtime_statuses_are_distinct() -> None:
    assert run("unknown", "null\n").returncode == 3
    assert run("error", "null\n").returncode == 5


def test_compile_failure_reports_on_stderr_only() -> None:
    result = run("{", "null\n")
    assert result.returncode == 3
    assert result.stderr
    assert result.stdout == ""


def test_runtime_failure_reports_on_stderr_only() -> None:
    result = run("error", "null\n")
    assert result.returncode == 5
    assert result.stderr
    assert result.stdout == ""


def test_runtime_failure_preserves_prior_generator_output() -> None:
    result = run("1, error", "null\n")
    assert result.returncode == 5
    assert [json.loads(line) for line in result.stdout.splitlines()] == [1]
    assert result.stderr
