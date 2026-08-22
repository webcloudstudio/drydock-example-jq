# FEATURE: Scoped Conformance Verification

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provide executing, machine-readable conformance gates for implementation slices. |
| Depends On  | ARCHITECTURE.md, FEATURE-Conformance-Assets.md, FEATURE-Streaming.md |
| Provides    | executing scoped conformance gates |
| Consumes    | ./jq -c program execution, staged conformance runner |

## Workflow

Each implementation story uses the supplied runner with a selector matching its owned syntax.
The candidate command is supplied through the inherited `JQ` environment variable. The gate
executes selected cases, parses the JSON report, requires a non-empty selection, requires zero
failures and errors, and checks the runner exit status.

## Programmatic Acceptance

=== AC scoped-conformance ===
Intent: The scoped runner executes a non-empty reduce slice and reports no failures or errors.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

selector = r"reduce"
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
=== END AC scoped-conformance ===

=== AC scoped-environment ===
Intent: The scoped runner receives the candidate through JQ while retaining the inherited execution environment.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

selector = r"true"
environment = {**os.environ, "JQ": f"{os.getcwd()}/jq"}
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", selector, "--json"],
    capture_output=True,
    text=True,
    env=environment,
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
report = json.loads(result.stdout)
assert report["summary"]["pass"] > 0
assert report["summary"]["fail"] == 0
assert report["summary"]["error"] == 0
assert result.returncode == 0
=== END AC scoped-environment ===

## User Acceptance

- None.

## Guardrails

- Scoped gates must execute cases; enumeration-only or dry-run modes are not acceptance.
- Every runner invocation must extend the inherited environment and set `JQ`.
- Scoped checks must use machine-readable state and must not assert on summary text.
