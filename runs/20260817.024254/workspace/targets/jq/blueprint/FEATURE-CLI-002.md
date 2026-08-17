# FEATURE: CLI Diagnostics

| Field       | Value |
|-------------|-------|
| Version     | 20260817 V1 |
| Description | Defines jq compilation and runtime diagnostics and their exit-status distinction. |
| Depends On  | ARCHITECTURE.md, FEATURE-CLI-001.md |
| Provides    | compile exit 3, runtime exit 5, stderr diagnostics |
| Consumes    | ./jq -c, lexer/parser, evaluator |

## Error Contract

| Condition | Exit | Output behavior |
|---|---:|---|
| Syntax or static compilation failure | 3 | Diagnostic on stderr; no normal result output |
| Runtime failure after compilation | 5 | Diagnostic on stderr; values emitted before failure remain available |
| Successful completion | 0 | Results on stdout; diagnostics, if any, remain on stderr |

The exact diagnostic wording is not part of the contract. The status code and stream placement are normative.

## Programmatic Acceptance

=== AC cli-002-compile-error ===
Intent: Invalid jq syntax is rejected with compile exit status 3 and a stderr diagnostic.
import subprocess

result = subprocess.run(
    ["./jq", "-c", "{"],
    input="null\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 3
assert result.stderr != ""
assert result.stdout == ""
=== END AC cli-002-compile-error ===

=== AC cli-002-runtime-error ===
Intent: A compiled filter that raises at runtime returns exit status 5 and keeps diagnostics off stdout.
import subprocess

result = subprocess.run(
    ["./jq", "-c", "error"],
    input="null\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 5
assert result.stderr != ""
assert result.stdout == ""
=== END AC cli-002-runtime-error ===

=== AC cli-002-partial-output ===
Intent: Results emitted before a runtime error remain on stdout while the process returns runtime exit status 5.
import json
import subprocess

result = subprocess.run(
    ["./jq", "-c", "1, error"],
    input="null\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 5
actual = [json.loads(line) for line in result.stdout.splitlines()]
expected = [1]
assert actual == expected
=== END AC cli-002-partial-output ===

## User Acceptance

- None.

## Guardrails

- Exit `3` is reserved for compilation failures.
- Exit `5` is used for runtime failures.
- Diagnostics must be written to standard error.
- Preserve values produced before a runtime failure.
