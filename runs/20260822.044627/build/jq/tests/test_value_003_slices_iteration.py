"""Executable coverage for VALUE-003 slices and collection iteration."""

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).parents[1]
EXECUTABLE = ROOT / "jq"


def run_jq(program: str, value: object) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(EXECUTABLE), "-c", program],
        input=json.dumps(value) + "\n",
        text=True,
        capture_output=True,
        check=False,
    )


def outputs(result: subprocess.CompletedProcess[str]) -> list[object]:
    return [json.loads(line) for line in result.stdout.splitlines()]


def test_array_slices_round_fractional_and_negative_bounds() -> None:
    result = run_jq(".[1.2:4.1], .[-3:], .[99:]", [0, 1, 2, 3, 4])
    assert result.returncode == 0
    assert outputs(result) == [[1, 2, 3, 4], [2, 3, 4], []]


def test_string_slices_use_unicode_codepoints_and_clamp_bounds() -> None:
    result = run_jq(".[1:3], .[:-2], .[20:]", "a😀bcde")
    assert result.returncode == 0
    assert outputs(result) == ["😀b", "a😀bc", ""]


def test_slicing_null_is_null_and_empty_ranges_are_empty() -> None:
    result = run_jq(".[:3], .[3:2]", None)
    assert result.returncode == 0
    assert outputs(result) == [None, None]


def test_array_and_object_iteration_preserves_order_and_multiplicity() -> None:
    result = run_jq(".[], .obj[]", {"obj": {"a": 1, "b": 1}})
    assert result.returncode == 0
    assert outputs(result) == [{"a": 1, "b": 1}, 1, 1]

    result = run_jq(".items[] | .name", {"items": [{"name": "a"}, {"name": "b"}]})
    assert result.returncode == 0
    assert outputs(result) == ["a", "b"]

    result = run_jq(".[]", {"a": 1, "b": 1})
    assert result.returncode == 0
    assert outputs(result) == [1, 1]


def test_optional_iteration_suppresses_invalid_inputs() -> None:
    result = run_jq("[.[] | .[]?]", [1, None, [], {"x": 2}, True])
    assert result.returncode == 0
    assert outputs(result) == [[2]]
