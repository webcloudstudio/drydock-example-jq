"""Regression coverage for FLOW-003 conditional and exception semantics."""

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


def outputs(result: subprocess.CompletedProcess[str]) -> list[object]:
    return [json.loads(line) for line in result.stdout.splitlines()]


def test_if_evaluates_each_condition_result_in_order() -> None:
    result = run("if (true, false, true) then 1 else 2 end")
    assert result.returncode == 0
    assert outputs(result) == [1, 2, 1]


def test_if_without_else_preserves_the_original_input() -> None:
    result = run("if false then 1 end", 7)
    assert result.returncode == 0
    assert outputs(result) == [7]


def test_elif_selects_the_first_truthy_condition_for_each_result() -> None:
    result = run('if . == 0 then "zero" elif . == 1 then "one" else "many" end', 1)
    assert result.returncode == 0
    assert outputs(result) == ["one"]


def test_try_catch_preserves_outputs_before_the_error() -> None:
    result = run('try (1, error("boom"), 2) catch .')
    assert result.returncode == 0
    assert outputs(result) == [1, "boom"]


def test_try_without_catch_suppresses_the_error() -> None:
    result = run('try error("boom")')
    assert result.returncode == 0
    assert outputs(result) == []


def test_optional_preserves_outputs_before_a_later_error() -> None:
    result = run('(1, error("boom"), 2)?')
    assert result.returncode == 0
    assert outputs(result) == [1]


def test_uncaught_error_after_output_keeps_partial_stdout_and_status() -> None:
    result = run('1, error("boom"), 2')
    assert result.returncode == 5
    assert outputs(result) == [1]
