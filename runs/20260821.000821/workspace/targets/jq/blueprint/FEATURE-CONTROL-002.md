# FEATURE: Recursive Generators and Control

| Field       | Value |
|-------------|-------|
| Version     | 20260821 V1 |
| Description | Provides jq recursive generator and loop primitives. |
| Depends On  | FEATURE-CONTROL-001.md, FEATURE-CORE-004.md, FEATURE-FRONTEND-004.md |
| Provides    | while, until, repeat, recurse |
| Consumes    | generator evaluation, conditionals, definitions |

## Purpose

Implement recursive jq generators with correct emission order, termination, branching, and interaction with user-defined filters.

## Behavior

- `while` emits each state while its condition is true and recursively updates the state.
- `until` repeatedly applies its update until its condition becomes true.
- `repeat` continues until its expression raises an error that terminates the repetition.
- `recurse` emits the current value before recursively evaluating descendants.
- Recursive filters preserve multiplicity and support bounded or conditional recursion.

## Programmatic Acceptance

=== AC control-002-recursive ===
Intent: The authoritative corpus slice exercising while, until, repeat, and recurse executes and passes.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

selector = r"while|until|repeat|recurse"
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
=== END AC control-002-recursive ===

=== AC control-002-order ===
Intent: Recursive corpus programs involving generator ordering execute without failures or timeouts.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

selector = r"recurse|while|until"
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
=== END AC control-002-order ===

## User Acceptance

- None.

## Guardrails

- Preserve the current value before recursive descendants.
- Ensure recursive generators terminate when their conditions require termination.
- Preserve partial output before a runtime error.
