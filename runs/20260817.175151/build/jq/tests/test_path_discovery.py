import io
import json

import jq


def evaluate(program: str, value: object) -> tuple[int, list[object]]:
    output = io.StringIO()
    status = jq.run(["-c", program], io.StringIO(json.dumps(value) + "\n"), output)
    return status, [json.loads(line) for line in output.getvalue().splitlines()]


def test_path_materializes_exact_nested_location() -> None:
    assert evaluate('[path(.a[0].b), getpath(["a", 0, "b"])]', {"a": [{"b": 7}]}) == (
        0,
        [[["a", 0, "b"], 7]],
    )


def test_path_preserves_nonexistent_exact_location() -> None:
    assert evaluate('path(.missing[2].value)', None) == (0, [["missing", 2, "value"]])


def test_paths_excludes_root_and_walks_depth_first() -> None:
    assert evaluate('[paths]', {"a": [1, {"b": 2}]}) == (
        0,
        [[["a"], ["a", 0], ["a", 1], ["a", 1, "b"]]],
    )


def test_paths_applies_node_filter() -> None:
    assert evaluate('[paths(type == "number")]', {"a": [1, "x", 3]}) == (
        0,
        [[["a", 0], ["a", 2]]],
    )


def test_getpath_returns_null_for_missing_components_and_reads_many_paths() -> None:
    assert evaluate('getpath(["a", "b"], ["a", "c"], ["missing"])', {"a": {"b": 0, "c": 1}}) == (
        0,
        [0, 1, None],
    )


def test_getpath_returns_null_after_a_scalar_component() -> None:
    assert evaluate('getpath(["a", "b", 0])', {"a": {"b": 3}}) == (0, [None])
