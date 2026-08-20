# FEATURE: Core Generators

| Field | Value |
|-------|-------|
| Version | 20260820 V1 |
| Description | Evaluate jq filters as ordered zero-, one-, or many-value streams. |
| Depends On | FEATURE-Frontend-Diagnostics.md |
| Provides | ordered generator evaluation, pipeline composition, backtracking |
| Consumes | jq AST and filter grammar |

## Scope

The evaluator treats every filter as a generator over an input value, preserving ordering, multiplicity, cartesian behavior, and backtracking.

## Programmatic Acceptance

=== AC generators-conformance ===
Intent: The selected generator corpus slice executes and passes.
Suite: behavioral
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

SELECT = r"(\.|\.\[\]|,|\||empty)"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", SELECT, "--json"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
report = json.loads(result.stdout)
summary = report["summary"]
assert sum(summary.values()) > 0
assert summary["fail"] == 0 and summary["error"] == 0
assert result.returncode == 0
=== END AC generators-conformance ===

=== AC generators-order ===
Intent: A generator preserves supplied input ordering and multiplicity.
Requires: executable=python3; scope=test

import json
import subprocess

result = subprocess.run(["./jq", "-c", "[.[]]"], input="[3,1,3]\n", capture_output=True, text=True)
assert result.returncode == 0
assert json.loads(result.stdout) == [3, 1, 3]
=== END AC generators-order ===

=== AC generators-pipeline ===
Intent: A downstream filter runs once for each upstream generator output.
Requires: executable=python3; scope=test

import json
import subprocess

result = subprocess.run(["./jq", "-c", "[.[] | . * 2]"], input="[1,2,3]\n", capture_output=True, text=True)
assert result.returncode == 0
assert json.loads(result.stdout) == [2, 4, 6]
=== END AC generators-pipeline ===

## User Acceptance

- None.

## Guardrails

- Preserve generator ordering, multiplicity, and partial backtracking.
- Do not collapse streams into single values during evaluation.
