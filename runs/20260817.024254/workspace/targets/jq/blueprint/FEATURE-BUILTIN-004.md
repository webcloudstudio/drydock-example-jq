# FEATURE: Formatting, Date, Math, and Environment Builtins

| Field       | Value |
|-------------|-------|
| Version     | 20260817 V1 |
| Description | Provide jq formatting, date, mathematical, numeric, and environment builtins. |
| Depends On  | ARCHITECTURE.md, FEATURE-BUILTIN-002.md, FEATURE-DATA-001.md |
| Provides    | jq format filters, date functions, math functions, numeric predicates, environment access |
| Consumes    | string builtins, JSON values, generator evaluator |

## Purpose

Implement the standard-library builtin families exercised by the corpus: `@text`, `@json`, `@html`, `@uri`, `@urid`, `@csv`, `@tsv`, `@sh`, `@base64`, `@base64d`, date conversion and formatting, math functions, numeric predicates, `now`, `env`, `$ENV`, and number-literal compatibility helpers.

Formatting must preserve jq escaping rules. Date operations use UTC where specified. Mathematical operations must expose jq-compatible numeric behavior, including infinities, NaN, and literal-preserving numbers where supported.

## Programmatic Acceptance

=== AC builtin-004-formats ===
Intent: The implementation passes the authoritative corpus cases for jq formatting filters.
Suite: scoped

import os
import subprocess
import sys

result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", r"^(@text|@json|@csv|@tsv|@html|@uri|@urid|@sh|@base64|@base64d)"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC builtin-004-formats ===

=== AC builtin-004-dates-math ===
Intent: The implementation passes the authoritative corpus cases for date and mathematical builtins.
Suite: scoped

import os
import subprocess
import sys

result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", r"^(fromdate|todate|strptime|strftime|mktime|gmtime|atan|sqrt|pow|floor|infinite|nan|have_decnum)"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC builtin-004-dates-math ===

## User Acceptance

- None.

## Guardrails

- Use only Python standard-library facilities.
- Do not introduce network, package-installation, or third-party runtime dependencies.
- Do not shell out to a system jq executable.
