import io
import json

import jq


def evaluate(program: str, value: object) -> tuple[int, list[object]]:
    output = io.StringIO()
    status = jq.run(["-c", program], io.StringIO(json.dumps(value) + "\n"), output)
    return status, [json.loads(line) for line in output.getvalue().splitlines()]


def test_binding_is_lexical_and_reusable() -> None:
    assert evaluate(".bar as $x | .foo | . + $x", {"foo": 10, "bar": 200}) == (0, [210])


def test_nested_array_and_object_patterns_bind_missing_array_values() -> None:
    assert evaluate(". as [$a, {c:$c}] | [$a,$c]", [2, {"c": 4}]) == (0, [[2, 4]])
    assert evaluate(".[] as [$a,$b] | [$a,$b]", [[0], [0, 1]]) == (0, [[0, None], [0, 1]])


def test_object_pattern_shorthand_uses_binding_name_as_key() -> None:
    assert evaluate(". as {$a, $b} | [$a,$b]", {"a": 1, "b": 2}) == (0, [[1, 2]])


def test_destructuring_alternatives_backtrack_on_shape() -> None:
    program = ". as {a:$a} ?// [$b] | [$a,$b]"
    assert evaluate(program, [3]) == (0, [[None, 3]])
    assert evaluate(program, {"a": 2}) == (0, [[2, None]])


def test_binding_does_not_escape_parenthesized_scope() -> None:
    status, _ = evaluate("(. as $x | $x) | $x", 1)
    assert status == 3
