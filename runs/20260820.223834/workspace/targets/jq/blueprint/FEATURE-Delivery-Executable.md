# FEATURE: Delivery Executable

| Field | Value |
|-------|-------|
| Version | 20260820 V1 |
| Description | Provide the root-level jq executable and its command-line and exit-status protocol. |
| Depends On | FEATURE-Builtins-IO.md |
| Provides | ./jq -c PROGRAM, newline-delimited JSON stdin/stdout, exit codes 0, 3, 5 |
| Consumes | jq compiler, evaluator, builtin runtime |

## Scope

The deliverable is an executable named `jq` at the application root. It accepts `-c PROGRAM`, reads newline-delimited JSON values, emits compact JSON values per line, and returns exit `0` on completion, `3` for compile failures, and `5` for runtime failures.

## Programmatic Acceptance

=== AC executable-conformance ===
Intent: The executable protocol is exercised by the identity corpus slice and passes with at least one selected case.
Suite: behavioral
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

SELECT = r"^\.$"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", SELECT, "--json"],
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
=== END AC executable-conformance ===

=== AC executable-exit-contract ===
Intent: The executable distinguishes compilation and runtime failures.
Requires: executable=python3; scope=test

import subprocess

compile_failure = subprocess.run(["./jq", "-c", "{"], input="null\n", capture_output=True, text=True)
runtime_failure = subprocess.run(["./jq", "-c", "error"], input="null\n", capture_output=True, text=True)
assert compile_failure.returncode == 3
assert runtime_failure.returncode == 5
=== END AC executable-exit-contract ===

## User Acceptance

- The executable can be invoked from the application root using `./jq -c PROGRAM`.

## Guardrails

- Do not shell out to a system jq executable.
- Do not require third-party runtime packages, network access, or options beyond `-c`.
- Preserve partial stdout output before runtime failure.
