"""Executable coverage for VALUE-002 field and index access."""

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


def test_field_access_returns_value_and_null_for_missing_field() -> None:
    result = run_jq(".present, .missing", {"present": 7})
    assert result.returncode == 0
    assert outputs(result) == [7, None]


def test_chained_and_quoted_field_access() -> None:
    result = run_jq('.nested."special.key"', {"nested": {"special.key": "ok"}})
    assert result.returncode == 0
    assert outputs(result) == ["ok"]


def test_array_and_string_index_access_support_negative_indices() -> None:
    result = run_jq(".[-1], .[1], .[99]", ["a", "b", "c"])
    assert result.returncode == 0
    assert outputs(result) == ["c", "b", None]

    string_result = run_jq(".[-1], .[1]", "abc")
    assert string_result.returncode == 0
    assert outputs(string_result) == ["c", "b"]


def test_optional_access_suppresses_type_errors_but_keeps_valid_values() -> None:
    result = run_jq("[.[] | .value?]", [1, {"value": 2}, {}])
    assert result.returncode == 0
    assert outputs(result) == [[2, None]]


def test_non_string_object_index_is_an_access_error() -> None:
    result = run_jq(".[1]", {"1": "not an implicit conversion"})
    assert result.returncode == 5


def test_non_optional_access_on_scalar_is_a_runtime_error() -> None:
    result = run_jq(".field", 1)
    assert result.returncode == 5
