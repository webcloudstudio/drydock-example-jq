# FEATURE: Front Validation

| Field       | Value |
|-------------|-------|
| Version     | 20260817 V1 |
| Description | Reject malformed jq programs during compilation with diagnostics and exit status 3. |
| Depends On  | FEATURE-Front-Parser.md |
| Provides    | static validation and compile diagnostics |
| Consumes    | jq parser and AST |

## Intent

Validate parsed jq programs before evaluation. Reject malformed syntax, invalid escapes, undefined variables, invalid object keys, invalid module metadata, and unresolved labels. Diagnostics are written to standard error, while the executable returns status 3.

## Validation Rules

- Undefined variable and label references are compile errors.
- Invalid escapes and malformed delimiters are compile errors.
- Constant object keys must be strings.
- Module metadata must be constant objects.
- Runtime evaluation must not begin after a compile error.

## Programmatic Acceptance

=== AC validation-rejects-invalid-programs ===
Intent: Invalid jq programs are rejected with the declared compile exit status.

import json
import os
import subprocess

program = "{"
payload = "null\n"
result = subprocess.run(
    ["./jq", "-c", program],
    input=payload,
    capture_output=True,
    text=True,
    env={**os.environ},
)
assert result.returncode == 3
assert result.stdout == ""
=== END AC validation-rejects-invalid-programs ===

=== AC validation-rejects-undefined-bindings ===
Intent: Undefined variable references fail during compilation rather than runtime evaluation.

program = ". as $known | $unknown"
payload = "null\n"
import os
import subprocess

result = subprocess.run(
    ["./jq", "-c", program],
    input=payload,
    capture_output=True,
    text=True,
    env={**os.environ},
)
assert result.returncode == 3
assert result.stdout == ""
=== END AC validation-rejects-undefined-bindings ===

=== AC validation-rejects-invalid-object-keys ===
Intent: A constant non-string object key is rejected during compilation.

program = "{(0):1}"
payload = "null\n"
import os
import subprocess

result = subprocess.run(
    ["./jq", "-c", program],
    input=payload,
    capture_output=True,
    text=True,
    env={**os.environ},
)
assert result.returncode == 3
assert result.stdout == ""
=== END AC validation-rejects-invalid-object-keys ===

=== AC validation-accepts-valid-program ===
Intent: A valid program reaches evaluation and returns its supplied input.

import json
import os
import subprocess

program = "."
payload_value = {"valid": [1, 2]}
payload = json.dumps(payload_value) + "\n"
result = subprocess.run(
    ["./jq", "-c", program],
    input=payload,
    capture_output=True,
    text=True,
    env={**os.environ},
)
assert result.returncode == 0
assert json.loads(result.stdout) == payload_value
=== END AC validation-accepts-valid-program ===

## User Acceptance

- None.

## Guardrails

- Do not execute or modify files under `sources/`.
- Do not shell out to a system jq executable or use a third-party jq implementation.
- Preserve the distinction between compile status 3 and runtime status 5.
