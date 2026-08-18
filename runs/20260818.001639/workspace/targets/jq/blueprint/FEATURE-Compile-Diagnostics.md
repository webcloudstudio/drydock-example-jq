# FEATURE: Compile Diagnostics

| Field       | Value |
|-------------|-------|
| Version     | 20260818 V1 |
| Description | Reject invalid jq programs with compile status 3 and diagnostics on standard error. |
| Depends On  | FEATURE-Parser.md |
| Provides    | compile validation, exit status 3 |
| Consumes    | jq parser and AST |

## Behavior

Compilation fails when jq source contains malformed syntax, undefined static bindings, invalid object keys, invalid module metadata, invalid import paths, or invalid labels. A compile failure must terminate before input evaluation, return status `3`, and write diagnostics only to standard error.

Diagnostic wording need not match upstream jq exactly; the status and compile-versus-runtime distinction are contractual.

## Static validation

The compiler validates:

- Balanced delimiters and complete expressions.
- Defined variables and labels at each lexical use site.
- Object keys that must be strings.
- Constant module and import metadata.
- Constant import and include paths.
- Module namespace syntax and unsupported malformed forms.

Valid programs must not be rejected merely because their execution can later raise a runtime error.

## Programmatic Acceptance

=== AC compile-failure-corpus-slice ===
Intent: The compiler rejects the corpus slice containing invalid bindings, object keys, module forms, malformed delimiters, and invalid labels.
Suite: scoped

import os
import subprocess
import sys

selector = r"^(module |include |%::|\. as \$foo \| break|\. as \[\]|\{|\})"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--list", "--select", selector],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC compile-failure-corpus-slice ===

=== AC compile-status-distinct ===
Intent: Invalid source returns compile status 3 while keeping diagnostics off standard output.
import subprocess

result = subprocess.run(
    ["./jq", "-c", "."],
    input="null\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0

invalid = subprocess.run(
    ["./jq", "-c", "{"],
    input="null\n",
    capture_output=True,
    text=True,
)
assert invalid.returncode == 3
assert invalid.stdout == ""
=== END AC compile-status-distinct ===

## User Acceptance

- None.

## Guardrails

- Compile failures must return `3`, never `5`.
- Diagnostics must never be emitted as JSON results on standard output.
- Runtime evaluation must not begin after a compile failure.
- Do not compare diagnostic wording against upstream text.
