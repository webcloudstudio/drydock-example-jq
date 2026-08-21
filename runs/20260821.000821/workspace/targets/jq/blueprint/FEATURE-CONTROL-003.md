# FEATURE: Generator Predicates and Collection Utilities

| Field       | Value |
|-------------|-------|
| Version     | 20260821 V1 |
| Description | Provides jq generator predicates, ranges, combinations, and transpose utilities. |
| Depends On  | FEATURE-CONTROL-002.md, FEATURE-CONTROL-001.md |
| Provides    | any, all, isempty, combinations, range, transpose |
| Consumes    | recursive generators, reductions, generator evaluation |

## Purpose

Implement generator-oriented predicates and collection utilities with correct empty-stream behavior, short-circuiting, cartesian combinations, and rectangular transposition.

## Behavior

- `any` and `all` evaluate generator predicates with jq truthiness and short-circuiting.
- `isempty` distinguishes an empty stream from a stream that emits false or null.
- `range` supports one-, two-, and three-argument forms and positive or negative steps.
- `combinations` emits ordered cartesian combinations.
- `transpose` pads jagged rows with null values.

## Programmatic Acceptance

=== AC control-003-predicates ===
Intent: The authoritative corpus slice exercising any, all, and isempty executes and passes.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

selector = r"any|all|isempty"
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
=== END AC control-003-predicates ===

=== AC control-003-collections ===
Intent: The authoritative corpus slice exercising ranges, combinations, and transpose executes and passes.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

selector = r"range|combinations|transpose"
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
=== END AC control-003-collections ===

## User Acceptance

- None.

## Guardrails

- Preserve short-circuit behavior for predicate generators.
- Preserve ordering and multiplicity of cartesian combinations.
- Pad jagged transposed rows with null rather than dropping positions.
