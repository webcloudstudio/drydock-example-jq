# FEATURE: Generator Evaluation Core

| Field       | Value |
|-------------|-------|
| Version     | 20260817 V1 |
| Description | jq filters evaluate as ordered streams with correct piping, collection, iteration, multiplicity, and backtracking. |
| Depends On  | ARCHITECTURE.md, FEATURE-FRONTEND-002.md, FEATURE-FRONTEND-003.md |
| Provides    | identity, literals, pipes, commas, iteration, collection, empty, backtracking |
| Consumes    | jq parser, AST, functions and bindings |

## Intent

The evaluator treats every filter as a generator from one input to zero or more outputs. Pipeline evaluation feeds each output into the next filter, comma concatenates streams, collections materialize all outputs, and empty backtracks to the preceding generator.

## Behavior

- Identity and literals produce one output per input.
- Pipes preserve downstream evaluation order for every upstream output.
- Commas preserve left-to-right stream order.
- Array and object constructors collect generator outputs with jq multiplicity.
- Array and object iteration produce values in jq order.
- `empty` produces no output without terminating unrelated sibling generators.
- Multi-output arguments form the required cartesian products.

## Programmatic Acceptance

=== AC eval-001-streams ===
Intent: The implementation passes the authoritative corpus cases for identity, literals, pipes, commas, iteration, and empty.
Suite: scoped
Requires: executable=python3; scope=test

import os
import subprocess
import sys

pattern = r"Simple value tests|Field access, piping|Multiple outputs, iteration|empty|Comma|Pipe"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", pattern],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC eval-001-streams ===

=== AC eval-001-collections ===
Intent: The implementation passes the authoritative corpus cases for array and object collection and generator multiplicity.
Suite: scoped
Requires: executable=python3; scope=test

import os
import subprocess
import sys

pattern = r"Dictionary construction syntax|Array construction|cartesian|collection|Multiple outputs"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", pattern],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC eval-001-collections ===

=== AC eval-001-backtracking ===
Intent: The implementation passes the authoritative corpus cases proving empty and backtracking preserve sibling output order.
Suite: scoped
Requires: executable=python3; scope=test

import os
import subprocess
import sys

pattern = r"empty|backtracking|first\(1,error|cartesian"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", pattern],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC eval-001-backtracking ===

## User Acceptance

- None.

## Guardrails

- Do not collapse a filter stream into a single value.
- Preserve output order, multiplicity, and partial results.
- Ensure `empty` backtracks only within the active generator evaluation.
