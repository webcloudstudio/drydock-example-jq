"""Acceptance coverage for JSON stream input and compact output."""

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).parents[1]
EXECUTABLE = ROOT / "jq"


def run_jq(program: str, input_text: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(EXECUTABLE), "-c", program],
        input=input_text,
        capture_output=True,
        text=True,
        check=False,
    )


def test_multiple_input_values_are_processed_in_order() -> None:
    inputs = "1\n2\n3\n"
    result = run_jq(".", inputs)
    assert result.returncode == 0
    assert result.stdout.splitlines() == inputs.splitlines()


def test_generator_outputs_preserve_order_and_multiplicity() -> None:
    result = run_jq(".[]", "[1,2,3]\n")
    assert result.returncode == 0
    assert result.stdout.splitlines() == ["1", "2", "3"]


def test_objects_are_compact_single_line_json() -> None:
    input_text = '{"a": 1, "b": [2, 3]}\n'
    result = run_jq(".", input_text)
    assert result.returncode == 0
    assert json.loads(result.stdout) == json.loads(input_text)
    assert len(result.stdout.splitlines()) == 1


def test_multiline_and_unicode_json_values_are_decoded() -> None:
    result = run_jq(".", '{\n  "answer": "μ"\n}\n[1, 2]\n')
    assert result.returncode == 0
    assert [json.loads(line) for line in result.stdout.splitlines()] == [
        {"answer": "μ"},
        [1, 2],
    ]
