import json
import subprocess
from pathlib import Path

import pytest

from jq_interpreter.errors import CompileError
from jq_interpreter.parser import parse


ROOT = Path(__file__).parents[1]


def run(program: str, value: object) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(ROOT / "jq"), "-c", program],
        input=json.dumps(value) + "\n",
        text=True,
        capture_output=True,
        check=False,
    )


def test_unicode_json_escapes_are_decoded() -> None:
    result = run(r'"Aa\r\n\t\b\f\u03bc"', None)
    assert result.returncode == 0
    assert json.loads(result.stdout) == "Aa\r\n\t\b\fμ"


def test_interpolation_uses_filter_output() -> None:
    result = run(r'"inter\("pol" + "ation")"', None)
    assert result.returncode == 0
    assert json.loads(result.stdout) == "interpolation"


@pytest.mark.parametrize(
    ("program", "value", "expected"),
    [
        ("@uri", "μ", "%CE%BC"),
        ("@base64", "foóbar\n", "Zm/Ds2Jhcgo="),
        ('@html "<b>\\(.)</b>"', "<script>hax</script>", "<b>&lt;script&gt;hax&lt;/script&gt;</b>"),
    ],
)
def test_format_literals(program: str, value: object, expected: str) -> None:
    result = run(program, value)
    assert result.returncode == 0
    assert json.loads(result.stdout) == expected


def test_invalid_escape_is_compile_failure() -> None:
    with pytest.raises(CompileError):
        parse(r'"u\vw"')

