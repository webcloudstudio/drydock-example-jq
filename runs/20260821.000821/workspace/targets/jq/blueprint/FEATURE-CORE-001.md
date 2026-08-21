# FEATURE: Stream-Based Filter Evaluation

| Field       | Value |
|-------------|-------|
| Version     | 20260821 V1 |
| Description | Evaluate every jq filter as an ordered stream of zero or more values. |
| Depends On  | FEATURE-FRONTEND-003.md |
| Provides    | generator evaluation, backtracking, downstream stream execution |
| Consumes    | jq parser and AST |

## Scope

Build the evaluator around ordered generators. Comma concatenates streams, pipes run downstream filters once per upstream value, and multi-output expressions preserve cartesian products, backtracking, multiplicity, and partial output before runtime errors.

## Programmatic Acceptance

=== AC core-001-generators ===
Intent: The implementation passes the executing conformance cases for generator ordering, pipes, commas, and iteration.
Suite: scoped

import json
import os
import subprocess
import sys

selector = r"\.|\[|,|empty|range|while|recurse"
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
assert summary["fail"] == 0
assert summary["error"] == 0
assert result.returncode == 0
=== END AC core-001-generators ===

=== AC core-001-backtracking ===
Intent: The implementation passes the executing cases that require multiplicity and downstream backtracking.
Suite: scoped

import json
import os
import subprocess
import sys

selector = r"foreach|limit|skip|first\(|last\(|nth\(|try |empty"
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
assert summary["fail"] == 0
assert summary["error"] == 0
assert result.returncode == 0
=== END AC core-001-backtracking ===

## User Acceptance

- None.

## Guardrails

- Never collapse a generator into a single value.
- Preserve output order, multiplicity, and downstream cartesian evaluation.
- Preserve values emitted before a runtime failure.
