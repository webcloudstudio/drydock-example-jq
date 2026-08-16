import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).parent.parent


def invoke(program: str, input_text: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(ROOT / "jq"), "-c", program],
        input=input_text,
        capture_output=True,
        text=True,
    )


def decoded(result: subprocess.CompletedProcess[str]) -> list[object]:
    return [json.loads(line) for line in result.stdout.splitlines()]


def test_binary_arguments_are_cartesian_and_left_to_right() -> None:
    result = invoke(".[] + .[]", "[1, 2]\n")
    assert result.returncode == 0
    assert decoded(result) == [2, 3, 3, 4]


def test_range_arguments_are_cartesian() -> None:
    result = invoke("range(0, 1; 3, 4)", "null\n")
    assert result.returncode == 0
    assert decoded(result) == [0, 1, 2, 0, 1, 2, 3, 1, 2, 1, 2, 3]


def test_array_constructor_collects_generator_outputs() -> None:
    result = invoke("[.[], .[] + 1]", "[2, 4]\n")
    assert result.returncode == 0
    assert decoded(result) == [[2, 4, 3, 5]]


def test_function_parameters_keep_filter_cartesian_semantics() -> None:
    result = invoke("def f(a; b): a + b; f(.[]; .[])", "[1, 2]\n")
    assert result.returncode == 0
    assert decoded(result) == [2, 3, 3, 4]


def test_multiple_input_arrays_do_not_cross_mix() -> None:
    result = invoke(".[]", "[2]\n[5]\n")
    assert result.returncode == 0
    assert decoded(result) == [2, 5]
