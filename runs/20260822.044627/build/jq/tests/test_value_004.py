"""Deterministic coverage for type, numeric, conversion, and math primitives."""

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).parents[1]


def run_jq(program: str, input_value: object = None) -> tuple[int, list[object]]:
    process = subprocess.run(
        [str(ROOT / "jq"), "-c", program],
        input=json.dumps(input_value) + "\n",
        capture_output=True,
        text=True,
    )
    outputs = [json.loads(line) for line in process.stdout.splitlines()]
    return process.returncode, outputs


def test_type_length_and_utf8_byte_length() -> None:
    code, output = run_jq("[type, length, \"μ\" | utf8bytelength]", ["a", "b"])
    assert code == 0
    assert output == [["array", 2, 2]]


def test_numeric_predicates_and_conversions() -> None:
    programs = [
        ("infinite|isinfinite", None, [True]),
        ("nan|isnan", None, [True]),
        ("1|isfinite", None, [True]),
        ("1|isnormal", None, [True]),
        ('"true"|toboolean', None, [True]),
        ('"1.5"|tonumber', None, [1.5]),
        ("4|tostring", None, ["4"]),
    ]
    for program, input_value, expected in programs:
        code, output = run_jq(program, input_value)
        assert code == 0
        assert output == expected


def test_math_functions_and_invalid_conversion_exit_runtime() -> None:
    code, output = run_jq("[sqrt, floor, sin, pow(2; 3)]", 9.9)
    assert code == 0
    assert output == [[3.146426544510455, 9, -0.45753589377532133, 8]]

    code, output = run_jq("tonumber", "not-a-number")
    assert code == 5
    assert output == []
