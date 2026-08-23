"""Coverage for jq collection ordering and keyed reductions."""

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).parents[1]


def run(program: str, value: object) -> list[object]:
    result = subprocess.run(
        [str(ROOT / "jq"), "-c", program],
        input=json.dumps(value) + "\n",
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    return [json.loads(line) for line in result.stdout.splitlines()]


def test_sort_uses_structural_jq_ordering() -> None:
    assert run("sort", [True, {}, "a", None, [1], 2, False]) == [
        [None, False, True, 2, "a", [1], {}]
    ]


def test_unique_collapses_numeric_equivalents() -> None:
    assert run("unique", [2, 1.0, 1, 2.0, 3]) == [[1.0, 2, 3]]


def test_sort_by_compares_all_values_generated_by_key_filter() -> None:
    value = [{"a": 1, "b": 2}, {"a": 1, "b": 1}, {"a": 0, "b": 9}]
    assert run("sort_by(.a, .b)", value) == [[
        {"a": 0, "b": 9}, {"a": 1, "b": 1}, {"a": 1, "b": 2}
    ]]


def test_group_by_keeps_equal_keys_together_and_input_order_stable() -> None:
    value = [{"key": 2, "id": "a"}, {"key": 1, "id": "b"}, {"key": 2, "id": "c"}]
    assert run("group_by(.key)", value) == [[
        [{"key": 1, "id": "b"}],
        [{"key": 2, "id": "a"}, {"key": 2, "id": "c"}],
    ]]


def test_keyed_extrema_use_first_minimum_and_last_maximum_tie() -> None:
    value = [{"key": 1, "id": "first"}, {"key": 1, "id": "last"}]
    assert run("[min_by(.key), max_by(.key)]", value) == [[
        {"key": 1, "id": "first"}, {"key": 1, "id": "last"}
    ]]


def test_empty_extrema_return_null() -> None:
    assert run("[min, max, min_by(.), max_by(.)]", []) == [[None, None, None, None]]
