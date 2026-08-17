import json
import subprocess


def run(program: str, value: object) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["./jq", "-c", program],
        input=json.dumps(value) + "\n",
        capture_output=True,
        text=True,
    )


def values(result: subprocess.CompletedProcess[str]) -> list[object]:
    return [json.loads(line) for line in result.stdout.splitlines()]


def test_defined_or_uses_fallback_only_when_left_stream_has_no_truthy_value():
    result = run("(false, null, 4) // 9", None)
    assert result.returncode == 0
    assert values(result) == [4]


def test_conditionals_use_jq_truthiness_for_each_condition_output():
    result = run("[if .[] then 1 else 0 end]", [False, None, [], 2])
    assert result.returncode == 0
    assert values(result) == [[0, 0, 1, 1]]


def test_any_and_all_consume_predicate_stream_once_and_preserve_empty_identity():
    result = run("[any(not), all(not)]", [])
    assert result.returncode == 0
    assert values(result) == [[False, True]]


def test_optional_suppresses_runtime_error_without_suppressing_other_stream_values():
    result = run("[.[] | (tonumber)?]", ["1", "bad", 2])
    assert result.returncode == 0
    assert values(result) == [[1, 2]]


def test_uncaught_runtime_error_has_runtime_exit_code():
    result = run("1 / 0", None)
    assert result.returncode == 5


def test_syntax_error_has_compile_exit_code():
    result = run("if true then", None)
    assert result.returncode == 3
