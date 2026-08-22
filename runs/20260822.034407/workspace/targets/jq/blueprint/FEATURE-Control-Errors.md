# FEATURE: Control Flow Errors

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Implements jq conditionals, runtime errors, exception handling, labels, and breaks. |
| Depends On  | ARCHITECTURE.md, FEATURE-Paths-Assignment.md |
| Provides    | conditionals, error, halt, halt_error, try/catch, optional suppression, labels, break |
| Consumes    | generator evaluator, assignment operators |

## Behavior

This feature implements `if`, `then`, `elif`, `else`, and `end` with jq truthiness: only `false` and `null` select the false branch. Runtime errors carry values, may be caught by `try ... catch`, and preserve outputs emitted before an uncaught error. The optional operator suppresses errors. Labels establish lexical break targets, and `halt`/`halt_error` terminate evaluation with their specified status behavior. Compile failures remain distinct from runtime failures.

## Programmatic Acceptance

=== AC control-errors-suite ===
Intent: Execute the conformance cases covering conditionals, errors, try/catch, and optional suppression.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys
from pathlib import Path

assert Path("jq").is_file()

select = r"if .*then|try |catch |error|halt|\\?"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", select, "--json"],
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
=== END AC control-errors-suite ===

=== AC control-label-suite ===
Intent: Execute the conformance cases covering lexical labels and break control flow.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys
from pathlib import Path

assert Path("jq").is_file()

select = r"label |break "
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", select, "--json"],
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
=== END AC control-label-suite ===

## User Acceptance

- None.

## Guardrails

- Compile failures must exit 3 and runtime failures must exit 5.
- Diagnostics go to stderr and are not used as behavioral output.
- Runtime errors must not discard values emitted before the error.
