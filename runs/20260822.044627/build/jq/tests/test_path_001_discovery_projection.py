from jq_interpreter import Interpreter


def outputs(program: str, value: object) -> list[object]:
    return list(Interpreter(program).run([value]))


def test_paths_predicate_preserves_nested_paths_and_order() -> None:
    assert outputs("[paths(type == \"number\")]", [1, [[], {"a": 2}], {"a": [True, 3]}]) == [
        [[0], [1, 1, "a"], [2, "a", 1]]
    ]


def test_path_recursive_descent_includes_root_then_children() -> None:
    assert outputs("[path(..)]", {"a": [{"b": 1}]}) == [
        [[], ["a"], ["a", 0], ["a", 0, "b"]]
    ]


def test_pick_materializes_missing_object_branches_as_null() -> None:
    assert outputs("pick(.a, .b.c, .x)", {"a": 1, "b": {"c": 2}, "e": 4}) == [
        {"a": 1, "b": {"c": 2}, "x": None}
    ]
