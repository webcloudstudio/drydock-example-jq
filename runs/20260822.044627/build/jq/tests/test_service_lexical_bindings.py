"""Focused coverage for jq's lexical value-binding semantics."""

import json
import subprocess
from pathlib import Path

from jq_interpreter.evaluator import evaluate
from jq_interpreter.parser import parse


ROOT = Path(__file__).parents[1]


def outputs(program: str, value: object) -> list[object]:
    return list(evaluate(parse(program), value))


def test_binding_reuses_each_generated_value_in_order() -> None:
    assert outputs("[1, 2, 3][] as $x | [$x, $x]", None) == [
        [1, 1],
        [2, 2],
        [3, 3],
    ]


def test_nested_binding_shadows_only_the_inner_scope() -> None:
    assert outputs("1 as $x | (2 as $x | $x), $x", None) == [2, 1]


def test_array_and_object_patterns_bind_missing_members_to_null() -> None:
    assert outputs(". as [$a, $b] | [$a, $b]", [7]) == [[7, None]]
    assert outputs(". as {present: $a, absent: $b} | [$a, $b]", {"present": 7}) == [[7, None]]


def test_keyword_can_be_used_as_a_binding_name() -> None:
    assert outputs("42 as $if | $if", None) == [42]


def test_binding_does_not_escape_parenthesized_scope() -> None:
    result = subprocess.run(
        [str(ROOT / "jq"), "-c", "(. as $x | $x) | $x"],
        input="null\n",
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 3
    assert json.loads(result.stdout or "[]") == []


def test_destructuring_alternative_retries_after_continuation_error() -> None:
    assert outputs(
        '[[3]] | .[] as [$a] ?// [$b] | '
        'if $a != null then error("err") else {$a, $b} end',
        None,
    ) == [{"a": None, "b": 3}]


def test_final_destructuring_alternative_error_is_not_suppressed() -> None:
    result = subprocess.run(
        [str(ROOT / "jq"), "-c", ". as [$a] ?// {a: $b} | error"],
        input='{"a": 1}\n',
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 5
