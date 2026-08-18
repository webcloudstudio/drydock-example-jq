# FEATURE: Module Grammar

| Field       | Value |
|-------------|-------|
| Version     | 20260818 V1 |
| Description | Validates jq module, import, and include syntax boundaries without loading modules. |
| Depends On  | FEATURE-Parser.md, FEATURE-Lexer.md |
| Provides    | module/import/include syntax validation |
| Consumes    | jq lexer, jq parser and AST |

## Purpose

The interpreter parses module directives sufficiently to validate constant metadata, constant import paths, and namespace syntax. This capability does not load module files because the fixed executable contract does not expose a module search-path option.

## Behavior

- Accept valid module grammar supported by the parser.
- Reject non-constant module metadata.
- Reject non-object module metadata.
- Reject non-constant include metadata and paths.
- Reject invalid escape sequences in module paths.
- Reject invalid namespace syntax.
- Return compile status `3` for these failures and write diagnostics to standard error.

## Programmatic Acceptance

=== AC module-grammar-conformance ===
Intent: The interpreter executes the conformance cases owned by module grammar validation.
Suite: scoped

import os
import subprocess
import sys

selector = r"^(module|include|%::)"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--list", "--select", selector],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC module-grammar-conformance ===

=== AC module-compile-status ===
Intent: Invalid module forms use the interpreter's compile-failure exit status.
import subprocess

programs = [
    "module (.+1); 0",
    "module []; 0",
    'include "a" (.+1); 0',
    'include "a" []; 0',
    'include "\\ "; 0',
    'include "\\(a)"; 0',
    "%::wat",
]
for program in programs:
    result = subprocess.run(
        ["./jq", "-c", program],
        input="null\n",
        capture_output=True,
        text=True,
    )
    assert result.returncode == 3
=== END AC module-compile-status ===

## User Acceptance

- None.

## Guardrails

- Module grammar validation must not require filesystem module loading.
- The supplied source assets remain unmodified.
- Diagnostics are written to standard error and are not compared by acceptance.
