"""Focused tests for the TEXT-001 string builtin surface."""

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
    outputs = [json.loads(line) for line in result.stdout.splitlines()]
    return result.returncode, outputs


def test_empty_separator_splits_unicode_codepoints() -> None:
    assert run_jq('split("")', "aμ😀") == (0, [["a", "μ", "😀"]])


def test_ascii_case_conversion_preserves_non_ascii() -> None:
    assert run_jq("ascii_downcase, ascii_upcase", "Abc Éé") == (0, ["abc Éé", "ABC Éé"])


def test_unicode_trim_and_codepoint_round_trip() -> None:
    assert run_jq("trim", "\u2003 μ \u2003") == (0, ["μ"])
    assert run_jq("explode | implode", "hé😀") == (0, ["hé😀"])


def test_string_predicates_and_join() -> None:
    assert run_jq('[startswith("pre"), endswith("fix")]', "prefix") == (0, [[True, True]])
    assert run_jq('join("-")', ["a", 2, None, False]) == (0, ["a-2--false"])


def test_string_builtins_reject_non_string_inputs() -> None:
    assert run_jq('startswith("x")', 3)[0] == 5
    assert run_jq('split(",")', 3)[0] == 5
