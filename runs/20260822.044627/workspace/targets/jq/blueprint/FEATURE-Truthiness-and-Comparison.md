# FEATURE: Truthiness and Comparison

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Defines jq truthiness, equality, inequality, and total value ordering. |
| Depends On  | FEATURE-Error-and-Optional-Evaluation.md |
| Provides    | truthiness, equality, inequality, type ordering, comparisons |
| Consumes    | ordered generator evaluation |

## Semantics

Only `false` and `null` are falsey. Equality is type-aware, with numeric equivalence across integer and floating representations. Ordering follows jq's value ordering across nulls, booleans, numbers, strings, arrays, and objects. Comparison operators preserve generator multiplicity.

## Programmatic Acceptance

=== AC core-004-conformance ===
Intent: The authoritative corpus comparison and truthiness cases execute without failures.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

selector = r"==|!=|<=|>=|<|>"
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
assert summary["fail"] == 0
assert summary["error"] == 0
assert result.returncode == 0
=== END AC core-004-conformance ===

=== AC core-004-json-contract ===
Intent: The runner confirms structural equality and ordering behavior over the supplied corpus.
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

selector = r"==|!=|<=|>=|<|>"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", selector, "--json"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
report = json.loads(result.stdout)
summary = report["summary"]
assert isinstance(summary["pass"], int)
assert summary["pass"] > 0
assert summary["fail"] == 0
assert summary["error"] == 0
assert result.returncode == 0
=== END AC core-004-json-contract ===

## User Acceptance

- None.

## Guardrails

- Python truthiness must not replace jq truthiness.
- Boolean values must not compare equal to numbers.
- Object key insertion order must not affect structural equality.
