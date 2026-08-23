"""Focused regression coverage for FLOW-001 typed operators."""

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).parents[1]


def run_jq(program: str, value: object = None) -> tuple[int, list[object]]:
    result = subprocess.run(
        [str(ROOT / "jq"), "-c", program],
        input=json.dumps(value) + "\n",
        capture_output=True,
        text=True,
    )
    return result.returncode, [json.loads(line) for line in result.stdout.splitlines()]


def test_typed_arithmetic_excludes_booleans() -> None:
    for program in ("true + 1", "true - 1", "true * 2", "true / 2", "true % 2"):
        code, output = run_jq(program)
        assert code == 5
        assert output == []


def test_structural_merge_repetition_and_string_division() -> None:
    code, output = run_jq('{"a":{"x":1}} * {"a":{"y":2}}')
    assert code == 0
    assert output == [{"a": {"x": 1, "y": 2}}]

    code, output = run_jq('"ab" * 3')
    assert code == 0
    assert output == ["ababab"]

    code, output = run_jq('"abc" / ""')
    assert code == 0
    assert output == [["a", "b", "c"]]


def test_arithmetic_update_assignment_uses_typed_merge() -> None:
    code, output = run_jq('.value += {"b": 2}', {"value": {"a": 1}})
    assert code == 0
    assert output == [{"value": {"a": 1, "b": 2}}]

