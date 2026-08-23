"""Focused coverage for CORE-003 runtime error and empty-stream semantics."""

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).parents[1]


def run(program: str, value: object = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(ROOT / "jq"), "-c", program],
        input=json.dumps(value) + "\n",
        text=True,
        capture_output=True,
        check=False,
    )


def test_empty_produces_no_values_and_succeeds() -> None:
    result = run("empty")
    assert result.returncode == 0
    assert result.stdout == ""


def test_optional_suppresses_runtime_error() -> None:
    result = run('error("x")?')
    assert result.returncode == 0
    assert result.stdout == ""


def test_try_catch_turns_error_value_into_output() -> None:
    result = run('try error("x") catch .')
    assert result.returncode == 0
    assert [json.loads(line) for line in result.stdout.splitlines()] == ["x"]


def test_uncaught_runtime_error_has_runtime_exit_status() -> None:
    result = run('error("x")')
    assert result.returncode == 5


def test_values_before_runtime_error_are_preserved() -> None:
    result = run('1, error("x"), 2')
    assert result.returncode == 5
    assert [json.loads(line) for line in result.stdout.splitlines()] == [1]


def test_nth_does_not_consume_unneeded_failing_generator_output() -> None:
    result = run('nth(1; 0,1,error("foo"))')
    assert result.returncode == 0
    assert [json.loads(line) for line in result.stdout.splitlines()] == [1]
