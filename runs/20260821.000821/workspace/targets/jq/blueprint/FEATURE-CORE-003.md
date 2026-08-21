# FEATURE: Arithmetic, Comparison, and Boolean Operators

| Field       | Value |
|-------------|-------|
| Version     | 20260821 V1 |
| Description | Defines jq's type-directed arithmetic, comparison, ordering, truthiness, and Boolean operators. |
| Depends On  | FEATURE-CORE-002.md |
| Provides    | arithmetic operators, comparisons, and, or, not, jq ordering and truthiness |
| Consumes    | generator evaluation, basic filters |

## Intent

Implement `+`, `-`, `*`, `/`, `%`, relational and equality comparisons, `and`, `or`, and `not`. Operators evaluate filter operands as generators, preserve jq's cartesian ordering, distinguish Boolean values from numbers, and apply jq's type-specific array, string, and object semantics.

## Behavior

- Arithmetic follows jq's numeric and structural rules, including null identity, array concatenation, string operations, object merging, division errors, and modulo errors.
- Comparisons use jq's total ordering and structural equality.
- Boolean operators use only `false` and `null` as false values and preserve generator multiplicity.
- Runtime failures propagate with exit status `5` after preserving prior output.

## Programmatic Acceptance

=== AC core-003-conformance ===
Intent: The arithmetic and comparison corpus slice executes and passes for the implemented operator surface.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

select = r"[+*/%<>=]| and | or |==|!="
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
=== END AC core-003-conformance ===

=== AC core-003-runtime-errors ===
Intent: The operator slice preserves the harness verdict for valid programs that raise runtime errors.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

select = r"try \(1/\.|try \(1/0|try \(1%\.|try \(1%0"
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
=== END AC core-003-runtime-errors ===

## User Acceptance

- None.

## Guardrails

- Use only Python standard-library facilities.
- Do not coerce strings, arrays, objects, or booleans implicitly into numbers.
- Preserve generator ordering and multiplicity.
