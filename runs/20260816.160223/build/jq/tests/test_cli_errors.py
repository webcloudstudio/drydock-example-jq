import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).parent.parent
JQ = ROOT / "jq"


def invoke(program: str, input_text: str = "null\n") -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(JQ), "-c", program],
        input=input_text,
        capture_output=True,
        text=True,
    )


def test_compile_error_uses_exit_status_three():
    result = invoke("{")

    assert result.returncode == 3
    assert result.stdout == ""


def test_runtime_error_uses_exit_status_five():
    result = invoke("error")

    assert result.returncode == 5


def test_runtime_error_preserves_values_emitted_before_failure():
    result = invoke("1, error")

    assert result.returncode == 5
    assert [json.loads(line) for line in result.stdout.splitlines()] == [1]


def test_runtime_type_failure_is_not_reported_as_process_failure():
    result = invoke('"text" + 1')

    assert result.returncode == 5


def test_readme_documents_interface_and_verification_command():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    assert "./jq -c '<program>'" in readme
    assert "sh sources/full_test.sh" in readme
    assert "standard input" in readme
    assert "standard output" in readme
