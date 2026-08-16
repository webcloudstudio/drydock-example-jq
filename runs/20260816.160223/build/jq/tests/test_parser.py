import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent.parent

def invoke(program, value):
    return subprocess.run([str(ROOT / "jq"), "-c", program], input=json.dumps(value) + "\n", capture_output=True, text=True)

def values(result):
    return [json.loads(line) for line in result.stdout.splitlines()]

def test_parser_builds_pipeline_array_and_arithmetic_ast_at_cli_boundary():
    result = invoke("[.[] | . + 1]", [1, 2, 3])
    assert result.returncode == 0
    assert values(result) == [[2, 3, 4]]

def test_parser_builds_object_precedence_and_string_interpolation():
    result = invoke('{value: (.x + 1), text: "item \\(.x)"}', {"x": 4})
    assert result.returncode == 0
    assert values(result) == [{"value": 5, "text": "item 4"}]

def test_parser_builds_definitions_bindings_and_reduce():
    result = invoke("def inc: . + 1; reduce .[] as $x (0; . + $x) | inc", [1, 2, 3])
    assert result.returncode == 0
    assert values(result) == [7]

def test_parser_rejects_unclosed_constructor_with_compile_status():
    assert invoke("[", {}).returncode == 3

def test_parser_rejects_unbound_variables_at_compile_time():
    assert invoke("$missing", {}).returncode == 3
