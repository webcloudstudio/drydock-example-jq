# FEATURE: Destructuring Patterns and Alternatives

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Supports array and object destructuring bindings and the ?// alternative operator. |
| Depends On  | FEATURE-Function-Definitions.md, FEATURE-Variable-Bindings.md |
| Provides    | array/object patterns, missing bindings, ?// alternatives |
| Consumes    | function definitions and lexical bindings |

## Scope

Destructuring binds values from arrays and objects to lexical variables, supplying null for missing positions or fields. The `?//` operator selects fallback patterns when a prior pattern cannot match or its downstream evaluation raises an eligible error. Patterns support nested arrays, objects, shorthand bindings, explicit keys, and multiple alternatives.

## Programmatic Acceptance

=== AC func-004-conformance ===
Intent: Destructuring bindings and alternatives execute successfully.
Requires: executable=python3; scope=test

import subprocess

result = subprocess.run(
    ["./jq", "-c", ". as {$x} | $x"],
    input='{"x":1}\n',
    capture_output=True,
    text=True,
)
assert result.returncode == 0
assert result.stdout.splitlines() == ["1"]

alternative = subprocess.run(
    ["./jq", "-c", ".a? // .b"],
    input='{"b":2}\n',
    capture_output=True,
    text=True,
)
assert alternative.returncode == 0
assert alternative.stdout.splitlines() == ["2"]
=== END AC func-004-conformance ===

## User Acceptance

- None.

## Guardrails

- Pattern alternatives must preserve generator ordering and lexical variable scope.
- Module loading is not required for this capability.
