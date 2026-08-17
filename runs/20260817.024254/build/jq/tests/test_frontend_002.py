import json
import subprocess


def run(program: str, value: object) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["./jq", "-c", program], input=json.dumps(value) + "\n",
        capture_output=True, text=True,
    )


def outputs(result: subprocess.CompletedProcess[str]) -> list[object]:
    return [json.loads(line) for line in result.stdout.splitlines()]


def test_arithmetic_precedence_constructs_executable_ast():
    result = run("1 + 2 * 2", None)
    assert result.returncode == 0
    assert outputs(result) == [5]


def test_collection_pipeline_preserves_generated_values():
    result = run("[.[] | . + 1]", [1, 2, 3])
    assert result.returncode == 0
    assert outputs(result) == [[2, 3, 4]]


def test_unterminated_object_is_compile_failure():
    result = run("{", None)
    assert result.returncode == 3


def test_assignment_update_constructs_and_executes_path():
    result = run(".count += 1", {"count": 1})
    assert result.returncode == 0
    assert outputs(result) == [{"count": 2}]


def test_unbound_binding_is_a_compile_failure():
    result = run(".field, 42, $value", {"field": 7})
    assert result.returncode == 3


def test_as_binding_is_available_in_pipeline_body():
    result = run(". as $value | $value", 7)
    assert result.returncode == 0
    assert outputs(result) == [7]
