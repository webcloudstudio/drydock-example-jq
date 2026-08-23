"""Focused coverage for jq truthiness, equality, and total ordering."""

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


def test_only_false_and_null_are_falsey() -> None:
    result = run("false, null, 0, 1, \"\", [], {} | if . then 1 else 0 end")
    assert result.returncode == 0
    assert outputs(result) == [0, 0, 1, 1, 1, 1, 1]


def test_numeric_equality_ignores_integer_float_representation() -> None:
    result = run("1 == 1.0")
    assert result.returncode == 0
    assert outputs(result) == [True]


def test_equality_is_strict_across_types() -> None:
    result = run("true == 1, 1 != \"1\"")
    assert result.returncode == 0
    assert outputs(result) == [False, True]


def test_object_equality_ignores_insertion_order() -> None:
    result = run('{"a":1,"b":{"x":2,"y":3}} == {"b":{"y":3,"x":2},"a":1}')
    assert result.returncode == 0
    assert outputs(result) == [True]


def test_comparison_uses_jq_total_type_order() -> None:
    result = run('[null, false, true, 0, "a", [], {}] | sort')
    assert result.returncode == 0
    assert outputs(result) == [[None, False, True, 0, "a", [], {}]]


def test_arrays_and_objects_compare_lexicographically() -> None:
    result = run("[1,2] < [1,3], {a:1} < {a:2}, {b:1} > {a:99}")
    assert result.returncode == 0
    assert outputs(result) == [True, True, True]


def test_boolean_operators_are_generator_aware() -> None:
    result = run("(true, false) and (true, false), (true, false) or false")
    assert result.returncode == 0
    assert outputs(result) == [True, False, False, True, False]


def test_not_condition_is_applied_to_each_array_member() -> None:
    result = run("[any(not), all(not)]", [])
    assert result.returncode == 0
    assert outputs(result) == [[False, True]]

    result = run("[any(not), all(not)]", [False])
    assert result.returncode == 0
    assert outputs(result) == [[True, True]]
