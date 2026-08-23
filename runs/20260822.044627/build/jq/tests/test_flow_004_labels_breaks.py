import pytest

from jq_interpreter.errors import CompileError
from jq_interpreter.evaluator import evaluate
from jq_interpreter.parser import parse


def outputs(program: str, value: object) -> list[object]:
    return list(evaluate(parse(program), value))


def test_break_requires_a_lexically_visible_label() -> None:
    with pytest.raises(CompileError):
        parse("break $out, label $out | 1")


def test_break_does_not_use_a_label_in_a_sibling_scope() -> None:
    with pytest.raises(CompileError):
        parse("(break $out), (label $out | 1)")


def test_break_terminates_only_the_matching_label_scope() -> None:
    assert outputs(
        '[label $out | .[] | if . > 1 then break $out else . end, "after"]',
        [0, 1, 2],
    ) == [[0, "after", 1, "after"]]


def test_nested_labels_propagate_break_to_the_nearest_matching_label() -> None:
    assert outputs(
        '[label $outer | (label $inner | (1, break $inner, 2)), 3, break $outer, 4]',
        None,
    ) == [[1, 3]]
