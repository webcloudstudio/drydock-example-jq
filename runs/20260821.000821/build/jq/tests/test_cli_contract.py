import json
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def invoke(program: str, payload: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(ROOT / "jq"), "-c", program],
        input=payload,
        capture_output=True,
        text=True,
        env={**os.environ},
        check=False,
    )


def test_cli_round_trip() -> None:
    values = [{"a": 1}, [2, 3], "text"]
    result = invoke(".", "\n".join(json.dumps(value) for value in values) + "\n")
    assert result.returncode == 0
    assert [json.loads(line) for line in result.stdout.splitlines()] == values


def test_cli_compile_status() -> None:
    assert invoke("{", "null\n").returncode == 3


def test_cli_runtime_status_preserves_partial_output() -> None:
    result = invoke("1, error", "null\n")
    assert result.returncode == 5
    assert [json.loads(line) for line in result.stdout.splitlines()] == [1]


def test_readme_documents_interface_and_verification() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for token in ("./jq -c", "stdin", "stdout", "exit", "3", "5", "sh sources/full_test.sh"):
        assert token in readme
