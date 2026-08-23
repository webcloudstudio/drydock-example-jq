"""Focused coverage for FLOW-002 boolean and alternative operators."""

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).parents[1]


def run(program: str, value: object = None) -> tuple[int, list[object]]:
    result = subprocess.run(
        [str(ROOT / "jq"), "-c", program],
        input=json.dumps(value) + "\n",
        text=True,
        capture_output=True,
        check=False,
    )
    return result.returncode, [json.loads(line) for line in result.stdout.splitlines()]


def test_alternative_keeps_all_truthy_left_outputs_without_default() -> None:
    code, output = run("(null, false, 1, 2) // 9")
    assert code == 0
    assert output == [1, 2]


def test_alternative_uses_right_generator_only_when_left_has_no_truthy_output() -> None:
    code, output = run("(null, false) // (1, 2)")
    assert code == 0
    assert output == [1, 2]


def test_alternative_assignment_replaces_falsey_paths() -> None:
    code, output = run(".items[] //= 7", {"items": [None, False, 2]})
    assert code == 0
    assert output == [{"items": [7, 7, 2]}]


def test_boolean_short_circuit_does_not_evaluate_unneeded_operand() -> None:
    code, output = run("false and error(\"bad\"), true or error(\"bad\")")
    assert code == 0
    assert output == [False, True]
