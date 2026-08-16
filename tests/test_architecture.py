import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).parent.parent


def run(program: str, value: object) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ROOT / "jq"), "-c", program],
        input=json.dumps(value) + "\n",
        capture_output=True,
        text=True,
        check=False,
    )


def test_identity_runtime():
    result = run(".", None)
    assert result.returncode == 0
    assert [json.loads(line) for line in result.stdout.splitlines()] == [None]


def test_array_iteration_preserves_generator_order():
    result = run("[.[]]", [1, 2, 3])
    assert result.returncode == 0
    assert [json.loads(line) for line in result.stdout.splitlines()] == [[1, 2, 3]]


def test_compile_error_exit_code():
    assert run("[", {}).returncode == 3
