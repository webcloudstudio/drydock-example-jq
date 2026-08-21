# FEATURE: Reductions and Bounded Iteration

| Field       | Value |
|-------------|-------|
| Version     | 20260821 V1 |
| Description | Provides jq reductions and bounded generator iteration. |
| Depends On  | FEATURE-CORE-001.md, FEATURE-CORE-004.md, FEATURE-PATHS-003.md |
| Provides    | reduce, foreach, limit, skip, first, last, nth |
| Consumes    | generator evaluation, lexical bindings, control flow, path assignment |

## Purpose

Implement accumulator-based reduction and iteration primitives while preserving generator ordering, destructured bindings, multiplicity, and lexical break behavior.

## Behavior

- `reduce` consumes every value from its generator in order and emits the final accumulator.
- `foreach` emits extracted intermediate accumulator values.
- `limit`, `skip`, `first`, `last`, and `nth` operate on ordered streams.
- Destructuring patterns bind reducer values, including absent members as `null`.
- Generator arguments retain jq cartesian evaluation semantics.
- Invalid negative limits or indices raise runtime errors.

## Programmatic Acceptance

=== AC control-001-reduce ===
Intent: The authoritative corpus slice exercising reduce and foreach executes and passes.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

selector = r"reduce|foreach"
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
=== END AC control-001-reduce ===

=== AC control-001-bounds ===
Intent: The authoritative corpus slice exercising bounded stream operators executes and passes.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

selector = r"limit|skip|first\(|last\(|nth\("
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
=== END AC control-001-bounds ===

## User Acceptance

- None.

## Guardrails

- Preserve generator order and multiplicity.
- Do not consume more values than the bounded operation requires.
- Keep runtime failures distinct from compile failures.
