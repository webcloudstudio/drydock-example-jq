# FEATURE: Generator Evaluation Core

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Ordered stream evaluation for jq filters. |
| Depends On  | FEATURE-Frontend-Interpolation.md, ARCHITECTURE.md |
| Provides    | generator evaluator, identity, empty, pipeline, comma |
| Consumes    | jq AST |

## Capability

The evaluator represents each filter as an ordered generator. Identity emits its input, `empty` emits no values, comma concatenates left and right streams, and pipelines evaluate the right filter once for every left-hand output. The implementation preserves ordering, multiplicity, cartesian behavior, backtracking, and outputs emitted before a runtime error.

## Programmatic Acceptance

=== AC generator-identity ===
Intent: Identity evaluates successfully over JSON input.

import os
import subprocess

source = "."
result = subprocess.run(
    ["./jq", "-c", source],
    input='{"value": 1}\n',
    capture_output=True,
    text=True,
    env={**os.environ},
)
assert result.returncode == 0
=== END AC generator-identity ===

=== AC generator-empty-and-comma ===
Intent: Empty and comma generator syntax execute successfully.

import os
import subprocess

source = "1, empty, 2"
result = subprocess.run(
    ["./jq", "-c", source],
    input="null\n",
    capture_output=True,
    text=True,
    env={**os.environ},
)
assert result.returncode == 0
=== END AC generator-empty-and-comma ===

=== AC generator-conformance ===
Intent: Executed conformance cases exercising generator ordering and pipelines pass without failures or errors.

import json
import os
import subprocess
import sys
from pathlib import Path

assert Path("jq").is_file()

selector = r"(^\.($|[^a-zA-Z])|empty|,|\|)"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", selector, "--json"],
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
=== END AC generator-conformance ===

## User Acceptance

- None.

## Guardrails

- Preserve exact generator ordering and multiplicity.
- Do not collapse streams into single values.
- Preserve partial stdout output when a later computation raises a runtime error.
