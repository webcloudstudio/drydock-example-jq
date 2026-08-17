# FEATURE: Generator Evaluation

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Evaluates jq filters as ordered generators with backtracking, multiplicity, and stream composition. |
| Depends On  | ARCHITECTURE.md, FEATURE-FRONTEND-PARSER.md |
| Provides    | generator evaluator, pipes, commas, iteration, collection |
| Consumes    | executable AST |

## Purpose

The evaluator executes every filter against an input value and produces an ordered stream of zero or more values. It must preserve jq's backtracking model rather than collapsing filters into single-return functions.

## Scope

Implement identity and literal filters, pipes, comma generators, array and object iteration, collection, `empty`, cartesian evaluation of generator-valued arguments, and compact one-value-per-line output. Preserve output order and multiplicity across nested generators.

## Programmatic Acceptance

=== AC generator-streams ===
Intent: The authoritative corpus passes representative generator, pipe, comma, iteration, and collection cases.
Suite: scoped

import os
import subprocess
import sys

result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select",
     r"^\.\[\]|^1,1$|^\[\.|^range\(|^while\("],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC generator-streams ===

=== AC generator-output-contract ===
Intent: A generator emits each produced value as compact JSON on its own output line.

import json
import subprocess

source = "[1,2,3]\n"
result = subprocess.run(
    ["./jq", "-c", ".[]"],
    input=source,
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
expected = json.loads(source)
assert actual == expected
=== END AC generator-output-contract ===

=== AC generator-empty ===
Intent: The empty filter produces no output while a surrounding generator continues in order.

import os
import subprocess
import sys

result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select",
     r"^1, empty, 2$|^\[1,2,empty,3"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC generator-empty ===

## User Acceptance

- None.

## Guardrails

- Preserve generator order, backtracking, and multiplicity.
- Do not treat a filter as a scalar function.
- Emit JSON results only to stdout and diagnostics only to stderr.
