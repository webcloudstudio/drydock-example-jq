# FEATURE: Slices and Iteration

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Defines jq array, string, and object iteration plus slicing and bounds behavior. |
| Depends On  | ARCHITECTURE.md, FEATURE-Field-And-Index-Access.md, FEATURE-Generator-Core.md |
| Provides    | array and string slices, array/object iteration, fractional bounds, negative bounds, out-of-range behavior |
| Consumes    | field and index access, ordered generators, jq values |

## Scope and Behavior

`.[start:end]` returns a slice of an array or string. Bounds may be omitted, negative, fractional, out of range, or represented by expressions. jq's documented truncation and clamping rules determine the resulting slice.

`.[]` emits each array element or object value as an ordered generator. Optional iteration suppresses invalid-type errors. Empty arrays and objects produce no values. Iteration and slices preserve Unicode codepoint behavior for strings and do not alter the original value.

## Programmatic Acceptance

=== AC value-003-conformance ===
Intent: The conformance corpus cases exercising slices and iteration execute and pass.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

select = r"\[.*:|\.\[\]"
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
=== END AC value-003-conformance ===

=== AC value-003-iteration ===
Intent: Iteration emits ordered array and object values, while optional iteration handles invalid input.
import json
import subprocess

source = '{"a":[1,2],"obj":{"x":3,"y":4},"bad":5}\n'
program = "[.a[], .obj[], (.bad[]?)]"
result = subprocess.run(["./jq", "-c", program], input=source, capture_output=True, text=True)
assert result.returncode == 0
assert json.loads(result.stdout) == [1, 2, 3, 4]
=== END AC value-003-iteration ===

=== AC value-003-slices ===
Intent: Array and string slices honor the supplied bounds and return values derived from those inputs.
import json
import subprocess

array_value = [0, 1, 2, 3, 4]
string_value = "abcdef"
source = json.dumps([array_value, string_value], separators=(",", ":")) + "\n"
program = "[.[0][1:-1], .[1][1:4]]"
result = subprocess.run(["./jq", "-c", program], input=source, capture_output=True, text=True)
assert result.returncode == 0
assert json.loads(result.stdout) == [[1, 2, 3], "bcd"]
=== END AC value-003-slices ===

## User Acceptance

- None.

## Guardrails

- Preserve generator order and multiplicity during iteration.
- Slice operations must not mutate the source array or string.
- Out-of-range slicing is bounded behavior; it must not become an indexing error.
