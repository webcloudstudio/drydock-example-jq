import json, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).parent.parent
def run(program, value):
    return subprocess.run([sys.executable, str(ROOT / "jq"), "-c", program], input=json.dumps(value)+"\n", capture_output=True, text=True)
def test_identity_runtime():
    result = run(".", None); assert result.returncode == 0; assert [json.loads(x) for x in result.stdout.splitlines()] == [None]
def test_array_iteration_preserves_generator_order():
    result = run("[.[]]", [1,2,3]); assert result.returncode == 0; assert [json.loads(x) for x in result.stdout.splitlines()] == [[1,2,3]]
def test_compile_error_exit_code(): assert run("[", {}).returncode == 3

def test_cli_adds_one_and_emits_compact_json():
    result = run(". + 1", 41)
    assert result.returncode == 0
    assert [json.loads(line) for line in result.stdout.splitlines()] == [42]

def test_cli_processes_newline_delimited_inputs_in_order():
    result = subprocess.run(
        [sys.executable, str(ROOT / "jq"), "-c", "."],
        input="1\n2\n3\n", capture_output=True, text=True,
    )
    assert result.returncode == 0
    assert [json.loads(line) for line in result.stdout.splitlines()] == [1, 2, 3]

def test_cli_emits_each_generator_result_as_a_line():
    result = run(".[]", ["a", "b", "c"])
    assert result.returncode == 0
    assert [json.loads(line) for line in result.stdout.splitlines()] == ["a", "b", "c"]
