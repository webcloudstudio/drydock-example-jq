# FEATURE: Arithmetic Comparison

| Field       | Value |
|-------------|-------|
| Version     | 20260818 V1 |
| Description | Implement jq type-directed arithmetic, equality, ordering, and numeric runtime behavior. |
| Depends On  | FEATURE-Primitive-Filters.md |
| Provides    | arithmetic operators, comparison operators, numeric predicates |
| Consumes    | ordered filter generators |

## Operators

Implement `+`, `-`, `*`, `/`, `%`, unary negation, `==`, `!=`, `<`, `>`, `<=`, and `>=` with jq's generator argument semantics.

Arithmetic is type-directed:

- Numbers use jq-compatible numeric conversion and edge behavior.
- Strings concatenate, split, or repeat where specified.
- Arrays concatenate or subtract elements where specified.
- Objects merge shallowly with `+` and recursively with `*`.
- `null` acts as the additive identity where jq specifies it.
- Invalid combinations and division or remainder by zero raise runtime errors.

Comparison must distinguish JSON types and use jq ordering, while equality treats numerically equal integer and floating representations as equal but never equates booleans with numbers.

## Numeric representation

Use the architecture decision's decimal-backed literal representation with explicit conversion for arithmetic. Preserve literal values when no arithmetic mutation occurs and expose the corpus-compatible `have_decnum` behavior.

## Programmatic Acceptance

=== AC arithmetic-corpus-slice ===
Intent: The arithmetic evaluator passes the corpus slice covering arithmetic, comparisons, equality, ordering, numeric predicates, string operations, array operations, object merge, and numeric errors.
Suite: scoped

import os
import subprocess
import sys

selector = r"(==|!=|<=|>=|[0-9][^ ]*[+*/% -][^ ]*|infinite|nan|isnan|isfinite|sort|cannot be divided)"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--list", "--select", selector],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC arithmetic-corpus-slice ===

=== AC arithmetic-runtime-error ===
Intent: Division by zero is reported as a runtime failure and does not become a compile failure.
import subprocess

result = subprocess.run(
    ["./jq", "-c", "1 / 0"],
    input="null\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 5
=== END AC arithmetic-runtime-error ===

=== AC arithmetic-json-values ===
Intent: A valid arithmetic expression emits a valid JSON result on standard output.
import json
import subprocess

left = 2
right = 3
result = subprocess.run(
    ["./jq", "-c", "(. + right)"],
    input=json.dumps(left) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 3
=== END AC arithmetic-json-values ===

## User Acceptance

- None.

## Guardrails

- Do not equate booleans with numbers.
- Preserve generator cartesian products for operator operands.
- Division and remainder by zero must be runtime errors.
- Do not use third-party numeric or jq libraries.
- Do not shell out to a system jq executable.
