from jq_interpreter.evaluator import evaluate
from jq_interpreter.parser import parse


def outputs(program: str, value: object) -> list[object]:
    return list(evaluate(parse(program), value))


def test_while_emits_qualifying_values_until_condition_fails() -> None:
    assert outputs("while(. < 10; . * 2)", 1) == [1, 2, 4, 8]


def test_until_emits_only_the_first_value_satisfying_condition() -> None:
    assert outputs("until(. >= 10; . * 2)", 1) == [16]


def test_repeat_preserves_outputs_before_its_terminating_error() -> None:
    assert outputs("[repeat(. * 2, error)?]", 1) == [
        [2]
    ]


def test_recurse_with_condition_is_depth_first() -> None:
    assert outputs("recurse(. * .; . < 20)", 2) == [2, 4, 16]


def test_recursive_descent_visits_containers_and_leaves_in_order() -> None:
    assert outputs("..", {"a": [1, {"b": 2}]}) == [
        {"a": [1, {"b": 2}]},
        [1, {"b": 2}],
        1,
        {"b": 2},
        2,
    ]
