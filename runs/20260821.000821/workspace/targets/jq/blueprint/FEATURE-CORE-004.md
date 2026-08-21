# FEATURE: Error Handling and Control Flow

| Field       | Value |
|-------------|-------|
| Version     | 20260821 V1 |
| Description | Defines jq conditionals, exception handling, alternatives, labels, breaks, and runtime failure behavior. |
| Depends On  | FEATURE-CORE-003.md |
| Provides    | if, elif, else, try, catch, ?, //, labels, breaks, runtime errors |
| Consumes    | generator evaluation, arithmetic and comparison operators |

## Intent

Implement conditional branches, `try` and `catch`, optional suppression, defined-or, lexical labels, `break`, `halt`, and runtime error propagation. Control constructs must operate independently for every generator output and preserve values emitted before an uncaught runtime error.

## Behavior

- Conditions treat only `false` and `null` as false.
- `try EXP catch HANDLER` evaluates the handler with the error value.
- `EXP?` suppresses errors and produces no value.
- `a // b` evaluates the fallback only when all left outputs are false, null, or empty.
- Labels and breaks are lexically scoped.
- Valid runtime failures exit `5`; compile failures remain distinct.

## Programmatic Acceptance

=== AC core-004-conformance ===
Intent: The conditional, exception, optional, alternative, label, and break corpus slice executes and passes.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

select = r"if |try |\?| //|label |break "
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", select, "--json"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
report = json.loads(result.stdout)
summary = report["summary"]
assert sum(summary.values()) > 0
assert summary["fail"] == 0 and summary["error"] == 0
assert result.returncode == 0
=== END AC core-004-conformance ===

=== AC core-004-partial-runtime-output ===
Intent: The control-flow slice passes cases exercising output before an error and error recovery.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

select = r"first\(1,error|1, try error|try error|catch"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", select, "--json"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
report = json.loads(result.stdout)
summary = report["summary"]
assert sum(summary.values()) > 0
assert summary["fail"] == 0 and summary["error"] == 0
assert result.returncode == 0
=== END AC core-004-partial-runtime-output ===

## User Acceptance

- None.

## Guardrails

- Do not treat ordinary runtime errors as compile failures.
- Do not emit diagnostic text on standard output.
- Preserve outputs produced before an uncaught runtime error.
