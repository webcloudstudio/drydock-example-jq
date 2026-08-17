import io
import json

import jq


def evaluate(program: str, value: object) -> tuple[int, list[object]]:
    output = io.StringIO()
    status = jq.run(["-c", program], io.StringIO(json.dumps(value) + "\n"), output)
    return status, [json.loads(line) for line in output.getvalue().splitlines()]


def test_zero_argument_function_and_recursion() -> None:
    program = "def fac: if . == 1 then 1 else . * (. - 1 | fac) end; fac"
    assert evaluate(program, 4) == (0, [24])


def test_filter_argument_runs_against_function_input() -> None:
    assert evaluate("def f(a): a | . + 1; f(.)", 2) == (0, [3])


def test_value_argument_is_evaluated_and_bound() -> None:
    assert evaluate("def f($x): $x + .; f(3)", 2) == (0, [5])


def test_multiple_filter_arguments_preserve_generator_products() -> None:
    program = "def f(a;b): [a,b]; f(.[0]; .[1])"
    assert evaluate(program, [1, 2]) == (0, [[1, 2]])


def test_arity_specific_redefinition_does_not_replace_other_arity() -> None:
    program = "def f: . + 1; def f(a): a + . + 11; [f, f(20)]"
    assert evaluate(program, 1) == (0, [[2, 32]])


def test_recursive_function_can_capture_lexical_value() -> None:
    program = (
        "def addn($n): if . == 0 then $n "
        "else . - 1 | addn($n + 1) end; addn(0)"
    )
    assert evaluate(program, 3) == (0, [3])
