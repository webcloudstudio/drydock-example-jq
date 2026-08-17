import os
import importlib.util
import subprocess
import sys
from pathlib import Path


def test_conformance_assets_enumerate_without_running_cases() -> None:
    root = Path(__file__).resolve().parent.parent
    result = subprocess.run(
        [sys.executable, "sources/run_conformance.py", "--list"],
        cwd=root,
        capture_output=True,
        text=True,
        env={**os.environ, "JQ": str(root / "jq")},
        check=False,
    )

    assert result.returncode == 0

    spec = importlib.util.spec_from_file_location("conformance_runner", root / "sources" / "run_conformance.py")
    assert spec is not None and spec.loader is not None
    runner = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = runner
    spec.loader.exec_module(runner)
    cases = runner.parse_corpus((root / "sources" / "jq.test").read_text(encoding="utf-8"))
    excluded = runner.apply_exclusions(cases, runner.parse_exclusions(root / "sources" / "exclusions.txt"))
    assert len(cases) == 550
    assert len(excluded) == 13

    harness = (root / "sources" / "run_conformance.py").read_text(encoding="utf-8")
    assert "def parse_corpus" in harness
