"""Behavioral tests for the ordered, stream-valued evaluator."""

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).parents[1]


def run(program: str, input_value: object = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(ROOT / "jq"), "-c", program],
        input=json.dumps(input_value) + "\n",
        text=True,
        capture_output=True,
        check=False,
    )


def outputs(result: subprocess.CompletedProcess[str]) -> list[object]:
    assert result.returncode == 0, result.stderr
    return [json.loads(line) for line in result.stdout.splitlines()]


def test_identity_is_a_single_value_stream() -> None:
    assert outputs(run(".")) == [None]


def test_empty_is_a_zero_value_stream() -> None:
    assert outputs(run("empty")) == []


def test_iterator_preserves_array_order_and_multiplicity() -> None:
    assert outputs(run(".[]", [1, 1, 2])) == [1, 1, 2]


def test_pipe_backtracks_right_filter_for_each_left_value() -> None:
    assert outputs(run(".[] | range(.)", [0, 1, 3])) == [0, 0, 1, 2]


def test_comma_preserves_branch_order_inside_collection() -> None:
    assert outputs(run("[1, empty, 2, 2]")) == [[1, 2, 2]]


def test_range_supports_one_two_and_three_argument_forms() -> None:
    assert outputs(run("[range(3), range(2; 4), range(0; 5; 2)]")) == [
        [0, 1, 2, 2, 3, 0, 2, 4]
    ]


def test_range_argument_streams_form_a_cartesian_product() -> None:
    assert outputs(run("[range(0, 1; 3, 4)]")) == [[0, 1, 2, 0, 1, 2, 3, 1, 2, 1, 2, 3]]


def test_tostream_emits_depth_first_leaf_and_close_records() -> None:
    assert outputs(run("tostream", [0, [1, {"a": 2}]])) == [
        [[0], 0], [[1, 0], 1], [[1, 1, "a"], 2], [[1, 1]], [[1]], [[]]
    ]


def test_fromstream_reconstructs_streamed_values() -> None:
    program = "fromstream(1|truncate_stream([[0],\"a\"],[[1,0],\"b\"],[[1,0]],[[1]]))"
    assert outputs(run(program, None)) == [["b"]]


def test_truncate_stream_drops_prefix_paths_and_preserves_record_shape() -> None:
    program = "truncate_stream([[0],\"a\"],[[1,0],\"b\"],[[1,0]],[[1]])"
    assert outputs(run(program, 1)) == [[[0], "b"], [[0]]]
