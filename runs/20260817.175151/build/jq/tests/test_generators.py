import io
import json

import jq


def evaluate(program: str, value: object) -> tuple[int, list[object]]:
    output = io.StringIO()
    status = jq.run(["-c", program], io.StringIO(json.dumps(value) + "\n"), output)
    return status, [json.loads(line) for line in output.getvalue().splitlines()]


def test_identity_preserves_nested_value() -> None:
    value = {"items": [1, 2], "ok": True}
    assert evaluate(".", value) == (0, [value])


def test_literals_ignore_input_and_preserve_order() -> None:
    assert evaluate('"hello", 42, true, null', {"ignored": True}) == (
        0,
        ["hello", 42, True, None],
    )


def test_comma_preserves_duplicates_and_left_to_right_order() -> None:
    assert evaluate("1,1,2", None) == (0, [1, 1, 2])


def test_pipe_runs_downstream_for_every_upstream_value() -> None:
    assert evaluate(".[] | .", [1, 2, 3]) == (0, [1, 2, 3])


def test_pipe_forms_cartesian_stream_when_downstream_is_a_comma() -> None:
    assert evaluate(".[] | (., .)", [1, 2]) == (0, [1, 1, 2, 2])


def test_empty_emits_no_values() -> None:
    assert evaluate("empty", None) == (0, [])


def test_empty_does_not_consume_adjacent_generator_values() -> None:
    assert evaluate("1, empty, 2", None) == (0, [1, 2])


def test_object_field_access_returns_value_and_missing_field_is_null() -> None:
    assert evaluate(".name, .missing", {"name": "jq"}) == (0, ["jq", None])


def test_array_iteration_preserves_order_and_multiplicity() -> None:
    assert evaluate(".[]", ["a", "b", "c"]) == (0, ["a", "b", "c"])


def test_dynamic_index_and_negative_index() -> None:
    assert evaluate(".[1], .[-1]", [10, 20, 30]) == (0, [20, 30])
    assert evaluate(".[\"name\"]", {"name": "jq"}) == (0, ["jq"])


def test_slices_support_omitted_and_negative_bounds() -> None:
    assert evaluate(".[1:3], .[:-1], .[-2:]", [0, 1, 2, 3]) == (
        0, [[1, 2], [0, 1, 2], [2, 3]]
    )


def test_optional_access_suppresses_invalid_iteration_and_chained_indexing() -> None:
    assert evaluate(".[]?", [1, [], {"x": 2}]) == (0, [1, [], {"x": 2}])
    assert evaluate(".foo?.bar?", {"foo": 1}) == (0, [])
