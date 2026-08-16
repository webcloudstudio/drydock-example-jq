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


def decoded(result: subprocess.CompletedProcess[str]) -> list[object]:
    return [json.loads(line) for line in result.stdout.splitlines()]


def test_identity_and_literals_compose_in_stream_order() -> None:
    result = invoke("., 3", {"x": 7})
    assert result.returncode == 0
    assert decoded(result) == [{"x": 7}, 3]


def test_collection_gathers_iteration_outputs() -> None:
    result = invoke("[.[]]", [1, 2, 3])
    assert result.returncode == 0
    assert decoded(result) == [[1, 2, 3]]


def test_chained_field_computed_index_and_iteration_use_their_base() -> None:
    result = invoke("[.name, .items[1], [.items[]]]", {"items": [4, 5], "name": "jq"})
    assert result.returncode == 0
    assert decoded(result) == [["jq", 5, [4, 5]]]


def test_optional_access_suppresses_invalid_base_access() -> None:
    result = invoke("[.missing?, .missing[0]?, .missing[]?]", {})
    assert result.returncode == 0
    assert decoded(result) == [[None, None]]


def test_array_and_string_slices_support_negative_and_omitted_bounds() -> None:
    array_result = invoke(".[1:4]", [0, 1, 2, 3, 4])
    string_result = invoke(".[-2:]", "abcdef")
    assert array_result.returncode == 0
    assert string_result.returncode == 0
    assert decoded(array_result) == [[1, 2, 3]]
    assert decoded(string_result) == ["ef"]
