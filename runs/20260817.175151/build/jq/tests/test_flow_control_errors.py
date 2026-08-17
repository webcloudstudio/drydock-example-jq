import io
import json

import jq


def evaluate(program: str, value: object) -> tuple[int, list[object]]:
    output = io.StringIO()
    status = jq.run(["-c", program], io.StringIO(json.dumps(value) + "\n"), output)
    return status, [json.loads(line) for line in output.getvalue().splitlines()]


def test_conditionals_use_only_false_and_null_as_false() -> None:
    program = '[.[] | if . then "yes" else "no" end]'
    assert evaluate(program, [0, [], "", False, None]) == (0, [["yes", "yes", "yes", "no", "no"]])


def test_elif_chain_and_missing_else_preserve_input() -> None:
    assert evaluate('if . == 0 then "zero" elif . == 1 then "one" else "many" end', 2) == (0, ["many"])
    assert evaluate("if false then 1 elif false then 2 end", 7) == (0, [7])


def test_try_catch_receives_error_value_and_try_without_catch_is_empty() -> None:
    assert evaluate('try error("bad") catch .', None) == (0, ["bad"])
    assert evaluate("[try .missing]", True) == (0, [[]])


def test_optional_operator_suppresses_type_errors_but_keeps_missing_object_field() -> None:
    assert evaluate("[.[] | .foo?]", [1, {}, {"foo": 3}]) == (0, [[None, 3]])


def test_label_break_stops_only_the_labeled_generator() -> None:
    program = '[(label $out | .[] | if . > 1 then break $out else . end), "done"]'
    assert evaluate(program, [0, 1, 2]) == (0, [[0, 1, "done"]])


def test_unhandled_error_has_runtime_status_and_preserves_prior_output() -> None:
    assert evaluate("1, error", None) == (5, [1])


def test_halt_and_halt_error_have_control_statuses() -> None:
    assert evaluate("1, halt, 2", None) == (0, [1])
    assert evaluate("halt_error(7)", None)[0] == 7
