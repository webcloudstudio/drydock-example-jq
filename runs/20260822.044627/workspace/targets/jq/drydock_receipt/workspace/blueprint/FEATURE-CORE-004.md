# FEATURE: Truthiness and Comparison Semantics

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Define jq truthiness, equality, inequality, and total value ordering. |
| Depends On  | ARCHITECTURE.md, FEATURE-CORE-003.md |
| Provides    | truthiness, equality, inequality, comparison ordering |
| Consumes    | ordered generator evaluator |

## Programmatic Acceptance

=== AC core-004-conformance ===
Intent: The executable evaluates jq truthiness, equality, inequality, and ordering semantics.
Suite: scoped

import subprocess

def run(program, input_text="null\n"):
    return subprocess.run(
        ["./jq", "-c", program],
        input=input_text,
        capture_output=True,
        text=True,
    )

assert run("false, null, 0, 1 | if . then 1 else 0 end").stdout == "0\n0\n1\n1\n"
assert run("1 == 1.0").stdout == "true\n"
assert run("true == 1").stdout == "false\n"
assert run("[1,2] < [1,3]").stdout == "true\n"
=== END AC core-004-conformance ===

## User Acceptance

- None.

## Guardrails

- Only `false` and `null` are falsey.
- Structural comparisons must be independent of object key insertion order.
