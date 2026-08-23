"""Focused coverage for CORE-002 stream composition semantics."""

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).parents[1]


def run(program: str, value: object = None) -> list[object]:
    result = subprocess.run(
        [str(ROOT / "jq"), "-c", program],
        input=json.dumps(value) + "\n",
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    return [json.loads(line) for line in result.stdout.splitlines()]


def test_pipe_evaluates_right_filter_for_each_left_output() -> None:
    assert run("[1, 2, 3] | .[]") == [1, 2, 3]


def test_comma_preserves_left_then_right_order() -> None:
    assert run("(.a, .b, .a)", {"a": 1, "b": 2}) == [1, 2, 1]


def test_array_collects_all_generator_outputs() -> None:
    assert run("[.[] | . + 1]", [1, 2, 3]) == [[2, 3, 4]]


def test_object_values_form_a_cartesian_product() -> None:
    assert run("{a: (1, 2), b: (3, 4)}") == [
        {"a": 1, "b": 3},
        {"a": 1, "b": 4},
        {"a": 2, "b": 3},
        {"a": 2, "b": 4},
    ]


def test_binary_operands_form_a_cartesian_product() -> None:
    assert run("(1, 2) + (10, 20)") == [11, 21, 12, 22]


def test_argument_streams_form_an_ordered_cartesian_product() -> None:
    assert run("[range(0, 1; 3, 4)]") == [
        [0, 1, 2, 0, 1, 2, 3, 1, 2, 1, 2, 3]
    ]
