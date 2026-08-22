# FEATURE: Path Access and Mutation Primitives

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Reads, creates, replaces, and deletes nested values through jq path primitives. |
| Depends On  | FEATURE-Path-Discovery.md |
| Provides    | getpath, setpath, delpaths |
| Consumes    | path discovery and projection |

## Scope

Implement `getpath`, `setpath`, and `delpaths` for nested object and array paths. Operations create intermediate containers where jq requires them, expand arrays with null values, preserve immutable-value semantics, and reject invalid or excessively deep paths with runtime errors.

## Programmatic Acceptance

=== AC path-002-conformance ===
Intent: Path access and mutation primitives execute successfully for representative getpath, setpath, and delpaths programs.
Suite: scoped
Requires: executable=python3; scope=test

import subprocess

get_result = subprocess.run(
    ["./jq", "-c", "getpath([\"a\", \"b\"])",],
    input='{"a":{"b":3}}\n',
    capture_output=True,
    text=True,
)
set_result = subprocess.run(
    ["./jq", "-c", "setpath([\"a\", \"b\"]; 4)",],
    input='{"a":{}}\n',
    capture_output=True,
    text=True,
)
del_result = subprocess.run(
    ["./jq", "-c", "delpaths([[\"a\"]])",],
    input='{"a":1,"b":2}\n',
    capture_output=True,
    text=True,
)
assert get_result.returncode == 0
assert get_result.stdout.splitlines() == ["3"]
assert set_result.returncode == 0
assert set_result.stdout.splitlines() == ['{"a":{"b":4}}']
assert del_result.returncode == 0
assert del_result.stdout.splitlines() == ['{"b":2}']
=== END AC path-002-conformance ===

## User Acceptance

- None.

## Guardrails

- Path operations must not mutate previously produced values.
- Invalid path types and excessive depth must remain runtime errors, not compile failures.
