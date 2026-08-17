import io
import json

import jq


def run_filter(program: str, payload: object) -> tuple[int, list[object]]:
    output = io.StringIO()
    status = jq.run(["-c", program], io.StringIO(json.dumps(payload) + "\n"), output)
    return status, [json.loads(line) for line in output.getvalue().splitlines()]


def test_parser_precedence_executes_grouped_arithmetic() -> None:
    assert run_filter("(1 + 2) * 3", None) == (0, [9])


def test_parser_constructs_nested_array_and_object() -> None:
    payload = {"x": 1}
    assert run_filter("{value: ., items: [., 2]}", payload) == (0, [{"value": payload, "items": [payload, 2]}])


def test_parser_rejects_unterminated_object() -> None:
    assert run_filter("{a: 1", None)[0] == 3


def test_parser_supports_pipe_and_field_indexing() -> None:
    assert run_filter(".items[] | .name", {"items": [{"name": "a"}, {"name": "b"}]}) == (0, ["a", "b"])


def test_parser_supports_conditional() -> None:
    assert run_filter('if . > 1 then "large" else "small" end', 2) == (0, ["large"])
