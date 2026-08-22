# FEATURE: Arithmetic and Structural Operators

| Field       | Value |
|-------------|-------|
| Version     | 20220822 V1 |
| Description | Provide jq arithmetic, structural merge, repetition, splitting, and negation operators. |
| Depends On  | ARCHITECTURE.md, FEATURE-VALUE-004.md |
| Provides    | plus, minus, multiply, divide, modulo, negation, recursive merge, repetition, splitting |
| Consumes    | jq value model, ordered generator evaluator |

## Intent

Implement jq's typed `+`, `-`, `*`, `/`, and `%` operators, unary negation, recursive object merge, array subtraction, string repetition, string splitting, and associated runtime errors. Operators must preserve generator Cartesian-product semantics and jq numeric behavior.

## Programmatic Acceptance

=== AC flow-001-conformance ===
Intent: The implementation passes the authoritative corpus slice covering arithmetic and structural operators.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

select = r"\+|\-|\*|/|%"
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
=== END AC flow-001-conformance ===

## User Acceptance

- None.

## Guardrails

- Do not perform implicit type conversions.
- Preserve partial output before runtime failures.
- Do not shell out to a system jq implementation.
