import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).parent.parent


def invoke(program: str, value: object = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(ROOT / "jq"), "-c", program],
        input=json.dumps(value) + "\n",
        capture_output=True,
        text=True,
    )


def test_malformed_programs_fail_before_execution():
    for program in ("{", "}", "1 +", "if true then 1"):
        assert invoke(program).returncode == 3


def test_undefined_variable_and_break_label_are_compile_errors():
    assert invoke(". as $known | $missing").returncode == 3
    assert invoke("break $missing").returncode == 3


def test_constant_non_string_object_key_is_compile_error():
    assert invoke("{(0): 1}").returncode == 3


def test_dynamic_object_key_and_bound_value_remain_valid():
    result = invoke(". as $value | {(.a): $value}", {"a": "key"})
    assert result.returncode == 0
    assert json.loads(result.stdout) == {"key": {"a": "key"}}


def test_label_scope_is_static_and_break_stops_label_stream():
    assert invoke("label $out | break $out").returncode == 0
    assert invoke("label $out | . as $x | break $x").returncode == 3
