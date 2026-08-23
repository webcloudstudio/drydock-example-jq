"""Focused coverage for jq's value and numeric boundary behavior."""

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).parents[1]
EXECUTABLE = ROOT / "jq"


def run_jq(program: str, input_text: str = "null\n") -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(EXECUTABLE), "-c", program],
        input=input_text,
        capture_output=True,
        text=True,
        check=False,
    )


def json_lines(result: subprocess.CompletedProcess[str]) -> list[object]:
    return [json.loads(line) for line in result.stdout.splitlines()]


def test_non_finite_values_are_null_at_the_json_output_boundary() -> None:
    result = run_jq("[nan, infinite, -infinite, {value: nan}]")
    assert result.returncode == 0
    assert json_lines(result) == [[None, None, None, {"value": None}]]


def test_tojson_and_fromjson_preserve_json_value_structure() -> None:
    result = run_jq("[.[] | tojson | fromjson]", '["text", 1, [true, null]]\n')
    assert result.returncode == 0
    assert json_lines(result) == [["text", 1, [True, None]]]


def test_fromjson_accepts_nan_and_serializes_it_as_null() -> None:
    result = run_jq("fromjson | [., isnan]", '"nan"\n')
    assert result.returncode == 0
    assert json_lines(result) == [[None, True]]


def test_nan_is_not_a_valid_array_key_for_has() -> None:
    result = run_jq("has(nan)", "[0,1,2]\n")
    assert result.returncode == 0
    assert json_lines(result) == [False]


def test_large_exponent_literal_remains_a_numeric_value() -> None:
    result = run_jq("[1E+1000, -1E+1000 | tojson]")
    assert result.returncode == 0
    assert json_lines(result) == [[
        "1.7976931348623157e+308",
        "-1.7976931348623157e+308",
    ]]
