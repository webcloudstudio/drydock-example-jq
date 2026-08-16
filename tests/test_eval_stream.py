import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).parent.parent


def invoke(program: str, value: object) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(ROOT / "jq"), "-c", program],
        input=json.dumps(value) + "\n",
        capture_output=True,
        text=True,
    )


def outputs(result: subprocess.CompletedProcess[str]) -> list[object]:
    return [json.loads(line) for line in result.stdout.splitlines()]


def test_stream_fanout_preserves_every_value_and_order() -> None:
    result = invoke(".[]", [1, 2, 3])
    assert result.returncode == 0
    assert outputs(result) == [1, 2, 3]


def test_pipeline_runs_downstream_once_per_upstream_value() -> None:
    result = invoke(".[] | . * 2", [1, 2, 3])
    assert result.returncode == 0
    assert outputs(result) == [2, 4, 6]


def test_empty_stream_completes_without_output() -> None:
    result = invoke("empty", None)
    assert result.returncode == 0
    assert result.stdout == ""


def test_comma_stream_is_left_to_right_for_each_binding() -> None:
    result = invoke(".[] as $x | ($x, $x + 1)", [10, 20])
    assert result.returncode == 0
    assert outputs(result) == [10, 11, 20, 21]


def test_outputs_before_a_later_generator_error_are_retained() -> None:
    result = invoke(".[1, 0/0]", ["first", "second"])
    assert result.returncode == 5
    assert outputs(result) == ["second"]
