import io
import json

import jq


def evaluate(program: str, value: object) -> tuple[int, list[object]]:
    output = io.StringIO()
    status = jq.run(["-c", program], io.StringIO(json.dumps(value) + "\n"), output)
    return status, [json.loads(line) for line in output.getvalue().splitlines()]


def test_addition_accepts_numbers_strings_arrays_objects_and_null_identity() -> None:
    assert evaluate(". + 2", 3) == (0, [5])
    assert evaluate("\"a\" + \"b\"", None) == (0, ["ab"])
    assert evaluate("[1] + [2]", None) == (0, [[1, 2]])
    assert evaluate('{"a":1} + {"b":2}', None) == (0, [{"a": 1, "b": 2}])
    assert evaluate("null + .", {"a": 1}) == (0, [{"a": 1}])


def test_equality_is_type_aware_but_numbers_are_numeric() -> None:
    assert evaluate("true == 1", None) == (0, [False])
    assert evaluate("1 == 1.0", None) == (0, [True])
    assert evaluate('{"a":1,"b":[true]} == {"b":[true],"a":1}', None) == (0, [True])


def test_truthiness_only_false_and_null_are_falsey() -> None:
    program = '[null, false, 0, "", []] | map(if . then true else false end)'
    assert evaluate(program, None) == (0, [[False, False, True, True, True]])


def test_defined_or_uses_fallback_for_missing_false_and_null_values() -> None:
    assert evaluate(".missing // 7", {}) == (0, [7])
    assert evaluate("false // 7, null // 8, 0 // 9", None) == (0, [7, 8, 0])


def test_arithmetic_operator_boundaries_and_zero_errors() -> None:
    assert evaluate("[10 / 2, -6 % 7, \"x\" * 3, \"a,b\" / \",\"]", None) == (
        0, [[5.0, -6.0, "xxx", ["a", "b"]]]
    )
    assert evaluate("1 / 0", None)[0] == 5
    assert evaluate("1 % 0", None)[0] == 5
    assert evaluate("\"x\" - 1", None)[0] == 5


def test_logical_operators_return_booleans() -> None:
    assert evaluate("0 and []", None) == (0, [True])
    assert evaluate("null or false", None) == (0, [False])
    assert evaluate("not", 0) == (0, [False])
