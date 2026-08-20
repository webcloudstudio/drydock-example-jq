# FEATURE: Paths Assignment

| Field | Value |
|-------|-------|
| Version | 20260820 V1 |
| Description | Apply jq plain, update, arithmetic, and defined-or assignments over paths. |
| Depends On | FEATURE-Paths-Mutation.md |
| Provides | =, |=, +=, -=, *=, /=, %=, //= |
| Consumes | path mutation, generator evaluation, runtime errors, bindings |

## Capability

Assignment evaluates left-hand sides as path expressions over the original input and produces immutable replacement values while preserving jq ordering, multiplicity, and runtime behavior.

## Programmatic Acceptance

=== AC paths-assignment-suite ===
Intent: The authoritative corpus executes the plain, update, arithmetic, and defined-or assignment cases owned by this story.
Suite: behavioral
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

SELECT = r"(=|\|=|\+=|-=|\*=|/=|%=|//=)"
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
=== END AC paths-assignment-suite ===

=== AC paths-assignment-compile-status ===
Intent: Assignment syntax is accepted as a compiled jq program.
Requires: executable=python3; scope=test

import os
import subprocess

result = subprocess.run(
    ["./jq", "-c", ".foo |= . + 1"],
    input='{"foo": 1}\n',
    capture_output=True,
    text=True,
    env={**os.environ},
)
assert result.returncode != 3
assert result.stderr is not None
=== END AC paths-assignment-compile-status ===

## User Acceptance

- None.

## Guardrails

- Assignment must not mutate values previously emitted by the same program.
- Plain assignment and update assignment must retain their distinct right-hand-side input semantics.
- Multi-path assignments must preserve jq's specified output order and multiplicity.
- An uncaught assignment runtime error must use exit status 5.
