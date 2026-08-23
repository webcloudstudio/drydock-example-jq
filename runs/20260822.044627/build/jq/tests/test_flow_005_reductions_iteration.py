from jq_interpreter.evaluator import evaluate
from jq_interpreter.parser import parse


def outputs(program: str, value: object) -> list[object]:
    return list(evaluate(parse(program), value))


def test_first_is_a_path_expression_for_pick() -> None:
    assert outputs("pick(first)", [1, 2]) == [[1]]


def test_composed_first_path_expression_for_pick() -> None:
    assert outputs("pick(first|first)", [[10, 20], 30]) == [[[10]]]


def test_reduce_accumulates_generator_values_in_order() -> None:
    assert outputs("reduce .[] as $item (0; . + $item)", [1, 2, 3]) == [6]


def test_foreach_extracts_each_intermediate_state() -> None:
    assert outputs("foreach .[] as $item (0; . + $item; [$item, . * 2])", [1, 2, 3]) == [
        [1, 2],
        [2, 6],
        [3, 12],
    ]


def test_limit_skip_and_nth_operate_on_streams() -> None:
    assert outputs("[limit(2; .[])]", [1, 2, 3]) == [[1, 2]]
    assert outputs("[skip(2; .[])]", [1, 2, 3]) == [[3]]
    assert outputs("nth(1; .[])", [1, 2, 3]) == [2]
