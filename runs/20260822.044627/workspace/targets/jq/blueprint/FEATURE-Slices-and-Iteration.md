# FEATURE: Slices and Iteration

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Defines array and string slicing plus array and object iteration semantics. |
| Depends On  | FEATURE-Accessors.md |
| Provides    | array/string slices, array/object iteration, fractional bounds |
| Consumes    | field and index access |

## Semantics

Array and string slices use inclusive-start and exclusive-end bounds, support omitted and negative bounds, and clamp out-of-range values. Fractional bounds are handled according to jq's numeric rules. Iteration over arrays and objects yields values in the required order, while optional iteration suppresses invalid-container errors.

## Programmatic Acceptance

=== AC value-003-conformance ===
Intent: The authoritative corpus slice cases execute without failures.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

selector = r"\[.*:|\.\[\]"
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
=== END AC value-003-conformance ===

=== AC value-003-iteration-contract ===
Intent: Array iteration and slicing preserve output order and bounds.
Requires: executable=python3; scope=test

import json
import subprocess

payload = '["a","b","c","d"]\n'
result = subprocess.run(
    ["./jq", "-c", ".[], .[1:3]"],
    input=payload,
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
expected = ["a", "b", "c", "d", ["b", "c"]]
assert actual == expected
=== END AC value-003-iteration-contract ===

## User Acceptance

- None.

## Guardrails

- Iteration preserves generator order and multiplicity.
- Slices must not mutate the source value.
- Out-of-range slices return the jq-compatible empty or clamped result rather than failing unexpectedly.
