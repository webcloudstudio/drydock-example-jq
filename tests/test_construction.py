import io
import json

import jq


def evaluate(program: str, value: object) -> tuple[int, list[object]]:
    output = io.StringIO()
    status = jq.run(["-c", program], io.StringIO(json.dumps(value) + "\n"), output)
    return status, [json.loads(line) for line in output.getvalue().splitlines()]


def test_array_constructor_collects_generator_outputs() -> None:
    assert evaluate("[.[]]", [1, 2, 3]) == (0, [[1, 2, 3]])


def test_empty_array_constructor() -> None:
    assert evaluate("[]", None) == (0, [[]])


def test_object_constructor_evaluates_values_against_input() -> None:
    assert evaluate("{name: .name, count: .items | length}", {"name": "example", "items": [1, 2]}) == (
        0,
        [{"name": "example", "count": 2}],
    )


def test_object_value_generator_expands_in_order() -> None:
    assert evaluate("{value: .[]}", [4, 5]) == (0, [{"value": 4}, {"value": 5}])


def test_object_dynamic_key_is_evaluated_at_runtime() -> None:
    assert evaluate("{(.key): .value}", {"key": "chosen", "value": 9}) == (0, [{"chosen": 9}])


def test_object_value_generators_form_cartesian_product() -> None:
    assert evaluate("{a: (1,2), b: (3,4)}", None) == (
        0,
        [{"a": 1, "b": 3}, {"a": 1, "b": 4}, {"a": 2, "b": 3}, {"a": 2, "b": 4}],
    )


def test_constant_non_string_object_key_is_compile_error() -> None:
    assert evaluate("{(0): 1}", None)[0] == 3
