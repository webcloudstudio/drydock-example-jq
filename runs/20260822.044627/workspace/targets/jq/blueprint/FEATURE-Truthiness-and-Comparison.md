# FEATURE: Truthiness and Comparison

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Defines jq truthiness, structural equality, numeric equivalence, and total comparison ordering. |
| Depends On  | ARCHITECTURE.md, FEATURE-Generator-Core.md, FEATURE-Composition-And-Cartesian-Evaluation.md, FEATURE-Value-Model.md |
| Provides    | false/null truthiness, equality, inequality, ordering, numeric equivalence |
| Consumes    | jq value model, generator evaluation |

## Scope and Behavior

Only `false` and `null` are falsey. Every other jq value, including zero, empty strings, arrays, and objects, is truthy.

Equality is structural and independent of object key order. Numbers compare equivalently across integer and floating representations when their numeric values are equal. Ordering follows jq's type order: null, false, true, numbers, strings, arrays, and objects, with recursive ordering within compound values.

Comparison operators preserve generator multiplicity and evaluate both operands according to jq filter semantics.

## Programmatic Acceptance

=== AC core-004-conformance ===
Intent: The conformance corpus cases exercising equality, inequality, truthiness, and ordering execute and pass.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

select = r"==|!=|<=|>=|<|>"
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
=== END AC core-004-conformance ===

=== AC core-004-truthiness ===
Intent: False and null are falsey while zero and empty containers are truthy.
import json
import subprocess

input_value = "null\n"
program = "[if false then 1 else 0 end, if null then 1 else 0 end, if 0 then 1 else 0 end, if [] then 1 else 0 end]"
result = subprocess.run(["./jq", "-c", program], input=input_value, capture_output=True, text=True)
assert result.returncode == 0
assert json.loads(result.stdout) == [0, 0, 1, 1]
=== END AC core-004-truthiness ===

## User Acceptance

- None.

## Guardrails

- Do not use Python truthiness as a substitute for jq truthiness.
- Do not equate booleans with numbers.
- Object key insertion order must not affect equality.
