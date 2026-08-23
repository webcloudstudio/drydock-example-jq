"""Focused tests for the TEXT-003 regular-expression filters."""

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).parents[1]


def run_jq(program: str, input_value: object) -> tuple[int, list[object]]:
    result = subprocess.run(
        [str(ROOT / "jq"), "-c", program],
        input=json.dumps(input_value, ensure_ascii=False) + "\n",
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode, [json.loads(line) for line in result.stdout.splitlines()]


def test_test_maps_flags_and_global_match_emits_offsets() -> None:
    assert run_jq('[test("foo"), test("foo"; "i")]', "FOO") == (0, [[False, True]])
    assert run_jq('[match("foo"; "g")]', "foo bar foo") == (0, [[
        {"offset": 0, "length": 3, "string": "foo", "captures": []},
        {"offset": 8, "length": 3, "string": "foo", "captures": []},
    ]])


def test_named_and_unnamed_captures_are_preserved() -> None:
    assert run_jq('match("(?<word>[a-z]+)-(\\\\d+)")', "abc-12") == (0, [{
        "offset": 0, "length": 6, "string": "abc-12",
        "captures": [
            {"offset": 0, "length": 3, "string": "abc", "name": "word"},
            {"offset": 4, "length": 2, "string": "12", "name": None},
        ],
    }])
    assert run_jq('capture("(?<word>[a-z]+)-(?<number>\\\\d+)")', "abc-12") == (0, [{"word": "abc", "number": "12"}])


def test_scan_and_regex_split_preserve_stream_order() -> None:
    assert run_jq('[scan("(a+)(b+)")]', "abaabbaaabbb") == (0, [[['a', 'b'], ['aa', 'bb'], ['aaa', 'bbb']]])
    assert run_jq('split(", *"; null)', "ab,cd, ef") == (0, [["ab", "cd", "ef"]])
    assert run_jq('[splits(", *")]', "ab,cd,   ef") == (0, [["ab", "cd", "ef"]])


def test_substitution_interpolates_named_captures_and_supports_streams() -> None:
    assert run_jq('gsub("(?<x>.)[^a]*"; "+\\(.x)-")', "Abcabc") == (0, ["+A-+a-"])
    assert run_jq('[sub("(?<a>.)"; "\\(.a|ascii_upcase)", "\\(.a|ascii_downcase)")]', "aB") == (0, [["AB", "aB"]])


def test_regex_filters_reject_non_string_input() -> None:
    assert run_jq('test("x")', 3)[0] == 5
