# FEATURE: Frontend Validation

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Reject invalid jq programs before evaluation with compile-status diagnostics. |
| Depends On  | ARCHITECTURE.md, FEATURE-Frontend-Parser.md |
| Provides    | static validation and compile diagnostics |
| Consumes    | jq parser and AST |

## Intent

Compilation must fail before evaluation when syntax, bindings, labels, object keys, or module forms violate jq's grammar and static rules. Compile failures use exit status `3`; diagnostics are written to stderr and are not part of the behavioral contract.

## Validation Rules

The compiler rejects:

- malformed or incomplete expressions;
- undefined variables and invalid break labels;
- non-string constant object keys;
- invalid module metadata and non-constant import metadata;
- malformed module syntax and unsupported module-loader forms when their grammar is invalid.

Valid programs must not be rejected during validation.

## Programmatic Acceptance

=== AC frontend-validation-syntax ===
Intent: Malformed jq syntax is rejected with the compile-error status.

import subprocess

invalid_programs = ["{", "}", "1 +", "if true then 1"]
for source in invalid_programs:
    result = subprocess.run(
        ["./jq", "-c", source],
        input="null\n",
        capture_output=True,
        text=True,
    )
    assert result.returncode == 3
=== END AC frontend-validation-syntax ===

=== AC frontend-validation-bindings ===
Intent: Undefined variables and invisible labels are rejected before runtime.

import subprocess

invalid_programs = [
    ". as $known | $missing",
    "break $missing",
]
for source in invalid_programs:
    result = subprocess.run(
        ["./jq", "-c", source],
        input="null\n",
        capture_output=True,
        text=True,
    )
    assert result.returncode == 3
=== END AC frontend-validation-bindings ===

=== AC frontend-validation-object-keys ===
Intent: Invalid constant object keys are rejected at compile time.

import subprocess

source = "{(0): 1}"
result = subprocess.run(
    ["./jq", "-c", source],
    input="null\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 3
=== END AC frontend-validation-object-keys ===

=== AC frontend-validation-valid-program ===
Intent: Valid programs pass static validation and reach normal execution.

import json
import subprocess

source = ". as $value | {value: $value}"
input_value = {"a": 1}
result = subprocess.run(
    ["./jq", "-c", source],
    input=json.dumps(input_value) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
assert json.loads(result.stdout)["value"] == input_value
=== END AC frontend-validation-valid-program ===

## User Acceptance

- None.

## Guardrails

- Compile failures must use exit status `3`, not runtime status `5`.
- Diagnostics go to stderr and are never required to match exact jq wording.
- Validation must complete before any program output is emitted.
