"""Regression coverage for filter and value function parameters."""

from jq_interpreter.evaluator import evaluate
from jq_interpreter.parser import parse


def outputs(program: str, value: object) -> list[object]:
    return list(evaluate(parse(program), value))


def test_filter_parameter_is_reusable_and_lazy() -> None:
    assert outputs("def twice(f): f | f; twice(.*2)", 5) == [20]


def test_filter_parameter_preserves_generator_cartesian_products() -> None:
    assert outputs("def pair(f; g): [f, g]; pair(1; 2)", None) == [[1, 2]]
    assert outputs("def pair(f; g): f + g; pair((1, 2); (3, 4))", None) == [
        4,
        5,
        5,
        6,
    ]


def test_value_parameter_captures_call_site_values() -> None:
    assert outputs("def add($x): .foo + $x; add(.foo)", {"foo": 2}) == [4]


def test_value_parameters_form_a_cartesian_product() -> None:
    assert outputs("def pair($x; $y): [$x, $y]; pair((1, 2); (3, 4))", None) == [
        [1, 3],
        [1, 4],
        [2, 3],
        [2, 4],
    ]


def test_filter_and_value_parameters_can_be_mixed() -> None:
    assert outputs("def add_to(f; $x): f + $x; add_to(.; 2)", 3) == [5]


def test_function_arities_are_independent() -> None:
    program = "def f: 0; def f(x): x + 1; [f, f(4)]"
    assert outputs(program, None) == [[0, 5]]


def test_function_captures_definition_scope_instead_of_call_scope() -> None:
    program = "1 as $x | def f: $x; 2 as $x | f"
    assert outputs(program, None) == [1]


def test_recursive_function_uses_its_own_definition() -> None:
    program = "def fac: if . == 1 then 1 else . * (. - 1 | fac) end; [.[] | fac]"
    assert outputs(program, [1, 2, 3, 4]) == [[1, 2, 6, 24]]


def test_redefinition_does_not_rebind_an_earlier_function_body() -> None:
    program = "def f: 1; def g: f; def f: 2; [g, f]"
    assert outputs(program, None) == [[1, 2]]
