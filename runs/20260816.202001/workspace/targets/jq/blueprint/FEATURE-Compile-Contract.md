# FEATURE: Compile Contract

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Defines the compile-time diagnostic boundary and jq exit status contract. |
| Depends On  | ARCHITECTURE.md, FEATURE-Parser.md |
| Provides    | compile error boundary, exit status 3 |
| Consumes    | jq parser and AST |

## Contract

A syntactically invalid or statically invalid jq program is a compile failure. The executable must return status `3`, write diagnostics to stderr, and produce no result values for that program.

A valid program must cross the compile boundary and reach runtime evaluation. Runtime failures are distinct and use status `5`; they must not be misreported as compile failures.

Diagnostic wording is not part of the contract. Diagnostics must not be written to stdout.

## Programmatic Acceptance

=== AC compile-api-separates-errors ===
Intent: The compiler exposes a compile boundary that distinguishes invalid source.
import jq_parser

try:
    jq_parser.parse(". as [] | null")
except Exception:
    rejected = True
else:
    rejected = False

assert rejected is True
=== END AC compile-api-separates-errors ===

=== AC compile-valid-source-reaches-ast ===
Intent: Valid source crosses compilation and produces an AST.
import jq_parser

compiled = jq_parser.parse(".")
assert compiled is not None
=== END AC compile-valid-source-reaches-ast ===

=== AC compile-cli-status-contract ===
Intent: The executable reports a malformed program with the declared compile status.
import subprocess

result = subprocess.run(
    ["./jq", "-c", "{"],
    input="null\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 3
assert result.stdout == ""
=== END AC compile-cli-status-contract ===

=== AC compile-diagnostics-use-stderr ===
Intent: Compile diagnostics are separated from result output.
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
=== END AC compile-diagnostics-use-stderr ===

## User Acceptance

- None.

## Guardrails

- Preserve exit status `3` for compile and static failures.
- Preserve exit status `5` for runtime failures.
- Keep diagnostics on stderr and result values on stdout.
