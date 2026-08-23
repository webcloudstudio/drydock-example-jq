from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_filter(program: str, value: object) -> tuple[int, list[object]]:
    result = subprocess.run(
        [str(ROOT / "jq"), "-c", program],
        input=json.dumps(value),
        capture_output=True,
        text=True,
        check=False,
    )
    outputs = [json.loads(line) for line in result.stdout.splitlines()]
    return result.returncode, outputs


def test_abs_preserves_non_numeric_values() -> None:
    code, outputs = run_filter("abs", "abc")
    assert code == 0
    assert outputs == ["abc"]
