import pytest

from jq_interpreter import Interpreter
from jq_interpreter.errors import RuntimeError as JqRuntimeError


def outputs(program: str, value: object) -> list[object]:
    return list(Interpreter(program).run([value]))


def test_getpath_returns_null_for_missing_nested_members() -> None:
    assert outputs('getpath(["a", "missing"])', {"a": {}}) == [None]


def test_setpath_builds_immutable_mixed_containers() -> None:
    original = None
    assert outputs('setpath(["a", 0, "b"]; 2)', original) == [{"a": [{"b": 2}]}]
    assert original is None


def test_setpath_negative_index_updates_existing_array() -> None:
    assert outputs('setpath([-1]; 9)', [1, 2]) == [[1, 9]]


def test_delpaths_removes_multiple_paths_without_shifting_targets() -> None:
    assert outputs('delpaths([[1], [3]])', [0, 1, 2, 3, 4]) == [[0, 2, 4]]


def test_setpath_rejects_boolean_path_components() -> None:
    with pytest.raises(JqRuntimeError):
        outputs('setpath([true]; 1)', None)


def test_delpaths_rejects_non_array_path_entries() -> None:
    with pytest.raises(JqRuntimeError):
        outputs('delpaths([1])', {})


def test_plain_assignment_uses_root_rhs_and_all_values() -> None:
    assert outputs('.a = .b', {'a': 1, 'b': 2}) == [{'a': 2, 'b': 2}]
    assert outputs('(.a, .b) = range(2)', {}) == [
        {'a': 0, 'b': 0},
        {'a': 1, 'b': 1},
    ]


def test_update_assignment_uses_selected_value() -> None:
    assert outputs('.foo |= . + 1', {'foo': 4}) == [{'foo': 5}]


def test_empty_update_deletes_selected_array_members() -> None:
    assert outputs('.[] |= empty', [0, 1, 2, 3]) == [[]]


def test_arithmetic_assignment_uses_root_rhs() -> None:
    assert outputs('.foo += .foo', {'foo': 2}) == [{'foo': 4}]


def test_slice_assignment_normalizes_negative_bounds() -> None:
    assert outputs('.[-3:-1] = [9]', [0, 1, 2, 3, 4]) == [[0, 1, 9, 4]]


def test_slice_assignment_clamps_out_of_range_bounds() -> None:
    assert outputs('.[-99:99] = [7]', [0, 1, 2]) == [[7]]


def test_deep_setpath_reports_path_limit() -> None:
    with pytest.raises(JqRuntimeError):
        outputs('setpath([range(10001) | 0]; 1)', None)
