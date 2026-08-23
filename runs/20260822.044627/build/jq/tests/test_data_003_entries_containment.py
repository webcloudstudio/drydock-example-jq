"""Behavioral coverage for object entries, membership, and containment."""

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).parents[1]


def run(program: str, value: object) -> list[object]:
    result = subprocess.run(
        [str(ROOT / "jq"), "-c", program],
        input=json.dumps(value) + "\n",
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    return [json.loads(line) for line in result.stdout.splitlines()]


def test_keys_sort_objects_but_keys_unsorted_preserves_insertion_order() -> None:
    assert run("[keys, keys_unsorted]", {"b": 2, "a": 1, "c": 3}) == [
        [["a", "b", "c"], ["b", "a", "c"]]
    ]


def test_has_and_in_distinguish_object_keys_from_array_indices() -> None:
    assert run("[has(1), has(1.5)]", ["zero", "one"]) == [[True, False]]
    assert run("1 | in({\"1\":0})", None) == [False]
    assert run("1 | in([0,1])", None) == [True]


def test_contains_and_inside_recurse_through_objects_and_arrays() -> None:
    value = {"foo": 12, "bar": [1, 2, {"nested": 3}]}
    return_values = run(
        "[contains({foo:12, bar:[{nested:3}]}), "
        "inside({foo:12, bar:[1,2,{nested:3, extra:4}]})]",
        value,
    )
    assert return_values == [[True, True]]


def test_entry_conversion_accepts_supported_aliases_and_transforms_keys() -> None:
    assert run(
        "to_entries | map(.key |= \"KEY_\" + .) | from_entries",
        {"a": 1, "b": 2},
    ) == [{"KEY_a": 1, "KEY_b": 2}]


def test_with_entries_drops_empty_results_and_keeps_first_value() -> None:
    assert run(
        "with_entries(if .key == \"drop\" then empty else .value |= . + 1 end)",
        {"keep": 1, "drop": 2},
    ) == [{"keep": 2}]


def test_index_utilities_cover_overlaps_empty_search_and_insertion_points() -> None:
    assert run('[indices("aba"), index("aba"), rindex("aba"), index("")]', "xababababa") == [
        [[1, 3, 5, 7], 1, 7, None]
    ]
    assert run('[bsearch(0,1,2,3,4)]', [1, 2, 3]) == [[-1, 0, 1, 2, -4]]


def test_quantifiers_and_membership_use_all_generated_values() -> None:
    assert run('[any((false,true); .), all((true,false); .)]', None) == [[True, False]]
    assert run('[IN(range(10;20); range(10)), IN(range(5;20); range(10))]', None) == [
        [False, True]
    ]
