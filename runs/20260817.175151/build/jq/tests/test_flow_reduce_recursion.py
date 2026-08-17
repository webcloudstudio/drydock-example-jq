import io
import json

import jq


def evaluate(program: str, value: object) -> tuple[int, list[object]]:
    output = io.StringIO()
    status = jq.run(["-c", program], io.StringIO(json.dumps(value) + "\n"), output)
    return status, [json.loads(line) for line in output.getvalue().splitlines()]


def test_reduce_accumulates_generator_outputs_in_order() -> None:
    assert evaluate("reduce .[] as $x (0; . + $x)", [1, 2, 4]) == (0, [7])


def test_reduce_destructures_each_item() -> None:
    program = "reduce .[] as [$i, $j] (0; . + $i - $j)"
    assert evaluate(program, [[2, 1], [5, 3], [6, 4]]) == (0, [5])


def test_foreach_emits_intermediate_accumulators() -> None:
    assert evaluate("foreach .[] as $x (0; . + $x; .)", [1, 2, 3]) == (0, [1, 3, 6])


def test_range_supports_direction_and_step() -> None:
    assert evaluate("[range(5;0;-2)]", None) == (0, [[5, 3, 1]])
    assert evaluate("[range(0;5;-1)]", None) == (0, [[]])


def test_limit_and_skip_bound_stream_consumption() -> None:
    assert evaluate("[limit(3; .[])]", [1, 2, 3, 4]) == (0, [[1, 2, 3]])
    assert evaluate("[skip(2; .[])]", [1, 2, 3, 4]) == (0, [[3, 4]])


def test_iteration_and_recursive_generators_preserve_order() -> None:
    assert evaluate("[while(. < 10; . * 2)]", 1) == (0, [[1, 2, 4, 8]])
    assert evaluate("[until(. >= 10; . * 2)]", 1) == (0, [[16]])
    assert evaluate("[..]", [1, [2]]) == (0, [[[1, [2]], 1, [2], 2]])


def test_negative_stream_counts_are_runtime_errors() -> None:
    assert evaluate("limit(-1; .)", None)[0] == 5
    assert evaluate("skip(-1; .)", None)[0] == 5
    assert evaluate("nth(-1; .)", None)[0] == 5
