"""Focused coverage for JSON conversion and jq output format filters."""

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).parents[1]
EXECUTABLE = ROOT / "jq"


def run_jq(program: str, value: object) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(EXECUTABLE), "-c", program],
        input=json.dumps(value, ensure_ascii=False) + "\n",
        text=True,
        capture_output=True,
        check=False,
    )


def output(program: str, value: object) -> object:
    result = run_jq(program, value)
    assert result.returncode == 0
    return json.loads(result.stdout)


def test_json_conversion_round_trip_and_tostring() -> None:
    assert output("[tostring, tojson | fromjson]", {"a": [1, "μ"]}) == [
        '{"a":[1,"μ"]}',
        {"a": [1, "μ"]},
    ]


def test_html_uri_and_uri_decode_escape_unicode_and_reserved_characters() -> None:
    assert output("@html", "<&>'\"μ") == "&lt;&amp;&gt;&apos;&quot;μ"
    assert output("@uri", "μ /?") == "%CE%BC%20%2F%3F"
    assert output("@urid", "%CE%BC%20%2F%3F") == "μ /?"


def test_csv_and_tsv_handle_nulls_quotes_and_control_escapes() -> None:
    value = [None, False, 3, 'a,"b', "line\n tab\t\\"]
    assert output("@csv", value) == ',false,3,"a,""b","line\n tab\t\\"'
    assert output("@tsv", value) == "\tfalse\t3\ta,\"b\tline\\n tab\\t\\\\"


def test_shell_format_quotes_each_array_argument() -> None:
    assert output("@sh", ["a", "O'Hara", 2, None]) == "'a' 'O'\\''Hara' '2' ''"
    assert output("@sh", "hello world") == "'hello world'"


def test_base64_round_trip_and_invalid_input_is_runtime_failure() -> None:
    encoded = output("@base64", "foóbar\n")
    assert encoded == "Zm/Ds2Jhcgo="
    assert output("@base64d", encoded) == "foóbar\n"

    result = run_jq("@base64d", "%not-base64")
    assert result.returncode == 5


def test_format_interpolation_escapes_only_interpolated_values() -> None:
    assert output('@uri "https://example.test/?q=\\(.)"', "what is jq?") == (
        "https://example.test/?q=what%20is%20jq%3F"
    )
