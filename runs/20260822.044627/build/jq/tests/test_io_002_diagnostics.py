import json
import subprocess
import sys


def run(program: str, input_text: str = "null\n") -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "jq", "-c", program],
        input=input_text,
        capture_output=True,
        text=True,
        check=False,
    )


def test_debug_preserves_stdout_and_writes_a_diagnostic() -> None:
    result = run("debug")

    assert result.returncode == 0
    assert [json.loads(line) for line in result.stdout.splitlines()] == [None]
    assert json.loads(result.stderr) == ["DEBUG:", None]


def test_debug_with_messages_preserves_input_once() -> None:
    result = run('debug("message", 2)')

    assert result.returncode == 0
    assert [json.loads(line) for line in result.stdout.splitlines()] == [None]
    assert result.stderr.splitlines() == ['["DEBUG:","message"]', '["DEBUG:",2]']


def test_stderr_preserves_value_without_mixing_channels() -> None:
    result = run("stderr")

    assert result.returncode == 0
    assert [json.loads(line) for line in result.stdout.splitlines()] == [None]
    assert result.stderr == "null"


def test_halt_error_emits_raw_value_and_stops_after_partial_output() -> None:
    result = run('1, ("failed" | halt_error(7))')

    assert result.returncode == 7
    assert [json.loads(line) for line in result.stdout.splitlines()] == [1]
    assert result.stderr == "failed"
