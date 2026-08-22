# FEATURE: Control Flow Reduction

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Implements jq reducers, stream extractors, bounded generators, and iterative control constructs. |
| Depends On  | ARCHITECTURE.md, FEATURE-Control-Errors.md |
| Provides    | reduce, foreach, limit, skip, first, last, nth, while, until, repeat |
| Consumes    | generator evaluator, runtime errors, labels |

## Behavior

Reducers consume generator outputs in order and update an accumulator. `foreach` exposes intermediate extraction results. `limit`, `skip`, `first`, `last`, and `nth` preserve generator ordering and short-circuit where specified. `while`, `until`, and `repeat` repeatedly evaluate filters without losing stream multiplicity, and propagate or suppress termination errors according to jq semantics.

## Programmatic Acceptance

=== AC control-reduce-suite ===
Intent: Execute the conformance cases covering reduce and foreach accumulation and extraction.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys
from pathlib import Path

assert Path("jq").is_file()

select = r"reduce |foreach "
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
=== END AC control-reduce-suite ===

=== AC control-iteration-suite ===
Intent: Execute the conformance cases covering bounded extraction and iterative generators.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys
from pathlib import Path

assert Path("jq").is_file()

select = r"limit\\(|skip\\(|first\\(|last\\(|nth\\(|while\\(|until\\(|repeat\\("
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
=== END AC control-iteration-suite ===

## User Acceptance

- None.

## Guardrails

- Preserve accumulator and extraction ordering.
- Negative limits, skips, and nth indices must raise jq runtime errors where specified.
- Short-circuiting constructs must not evaluate unnecessary generator outputs.
