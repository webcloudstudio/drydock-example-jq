# FEATURE: SQL-Style and Metadata Builtins

| Field       | Value |
|-------------|-------|
| Version     | 20260818 V1 |
| Description | Provides jq indexing, joining, membership, builtin enumeration, and numeric capability metadata. |
| Depends On  | FEATURE-Functions.md, FEATURE-Path-Discovery.md, FEATURE-IO-Builtins.md |
| Provides    | INDEX, JOIN, IN, builtins, have_decnum, metadata helpers |
| Consumes    | functions, paths, generator evaluation |

## Purpose

Implement jq's SQL-style operators and metadata filters with generator-aware stream semantics.

## Behavior

- `INDEX` builds objects from streams using computed keys.
- `JOIN` combines stream values with indexed values and applies optional join filters.
- `IN` tests membership across generated streams.
- `builtins` emits the available builtin name/arity strings.
- `have_decnum` reports the selected numeric compatibility behavior.
- Metadata helpers expose the supported builtin capability surface.

## Programmatic Acceptance

=== AC sql-metadata-conformance ===
Intent: The implementation passes the authoritative corpus cases for SQL-style operators and metadata builtins.
Suite: scoped
Requires: executable=python3; scope=test

import os
import subprocess
import sys

result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--list", "--select",
     r"(^|[^A-Za-z])(INDEX|JOIN|IN|builtins|have_decnum|modulemeta)\b"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC sql-metadata-conformance ===

=== AC sql-runtime-status ===
Intent: A valid SQL-style membership program completes with the documented success status.
import subprocess

program = "range(1;2)|IN(range(2))"
result = subprocess.run(["./jq", "-c", program], input="null\n", capture_output=True, text=True)
assert result.returncode == 0
=== END AC sql-runtime-status ===

## User Acceptance

- None.

## Guardrails

- Do not expose filesystem-backed module loading beyond the supplied flat-source constraints.
- Keep metadata derived from the implemented builtin registry.
