# FEATURE: Paths Assignment

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Provide jq path-based plain, update, and arithmetic assignments. |
| Depends On  | FEATURE-Paths-Helpers.md, FEATURE-Values-Arithmetic.md, FEATURE-Control-Conditionals.md |
| Provides    | =, |=, +=, -=, *=, /=, %=, //= |
| Consumes    | path discovery, immutable path mutation, arithmetic operators |

## Purpose

Implement jq assignments over path expressions, including generator-valued right-hand sides, multiple targets, update operators, defined-or assignment, and deletion by `empty`.

## Behavior

- Plain assignment evaluates the right-hand side against the original input and emits one result per RHS output.
- Update assignment evaluates the RHS against each selected path value and uses only its first output.
- Arithmetic assignments are equivalent to update assignment with the corresponding operator.
- `//=` updates only null or false values.
- Assigning `empty` deletes selected paths.
- Assignment preserves the original input for sibling outputs and handles multiple path targets in jq order.

## Programmatic Acceptance

=== AC paths-assignment-suite ===
Intent: The authoritative corpus passes the assignment cases owned by this capability.
Suite: scoped

import subprocess

selectors = [" = ", "|=", "+=", "-=", "*=", "/=", "%=", "//="]
for selector in selectors:
    result = subprocess.run(
        ["python3", "sources/run_conformance.py", "--select", selector],
        capture_output=True,
        text=True,
    )
    print(result.stdout)
    print(result.stderr)
    assert result.returncode == 0
=== END AC paths-assignment-suite ===

=== AC paths-assignment-roundtrip ===
Intent: Plain, update, and deletion assignments produce distinct immutable results.
import json
import subprocess

source = {"a": 1, "b": 2}
program = '(.a,.b)=range(2), .a |= .+10, .b |= empty'
result = subprocess.run(
    ["./jq", "-c", program],
    input=json.dumps(source) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
expected = [
    {"a": 0, "b": 0},
    {"a": 1, "b": 1},
    {"a": 11, "b": 2},
    {"a": 1},
]
assert actual == expected
assert source == {"a": 1, "b": 2}
=== END AC paths-assignment-roundtrip ===

## User Acceptance

- None.

## Guardrails

- Do not implement assignment as in-place mutation.
- Preserve outputs emitted before later RHS or path errors.
- Do not permit assignment paths that jq rejects as invalid path expressions.
