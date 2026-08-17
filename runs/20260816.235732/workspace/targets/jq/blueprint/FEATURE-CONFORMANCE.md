# FEATURE: jq Conformance Verification

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Define terminal verification against the supplied jq conformance corpus. |
| Depends On  | ARCHITECTURE.md, FEATURE-CLI-FOUNDATION.md, FEATURE-FRONTEND-LEXER.md, FEATURE-FRONTEND-PARSER.md, FEATURE-EVAL-GENERATOR.md, FEATURE-EVAL-VALUES.md, FEATURE-EVAL-CONTROL.md, FEATURE-LANG-BINDINGS.md, FEATURE-LANG-PATHS.md, FEATURE-BUILTIN-STRUCTURAL.md, FEATURE-BUILTIN-STRINGS.md, FEATURE-BUILTIN-RUNTIME.md |
| Provides    | complete jq conformance verification |
| Consumes    | executable jq, all interpreter capabilities |

## Verification Scope

The supplied corpus, exclusions, runner, and shell entry point are authoritative. The complete suite is run only after all implementation stories close. Declared module-loader exclusions remain visible and unchanged; all other cases are scored.

## Programmatic Acceptance

=== AC conformance-full ===
Intent: The completed interpreter passes the supplied full conformance suite.
Suite: full
Requires: executable=python3; scope=test

import subprocess

result = subprocess.run(
    ["sh", "sources/full_test.sh"],
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr)
assert result.returncode == 0
=== END AC conformance-full ===

## User Acceptance

- None.

## Guardrails

- Preserve all supplied scoring assets byte-for-byte.
- Run exactly `sh sources/full_test.sh` for terminal acceptance.
- Do not filter, skip, reinterpret, or rewrite corpus cases or harness behavior.
- Treat the harness exit status as the sole release verdict.
