# FEATURE: Executable Entry Point

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provides the executable jq command-line entry point for compact filter execution. |
| Depends On  | ARCHITECTURE.md, FEATURE-Conformance-Asset-Staging.md |
| Provides    | executable jq, -c filter invocation |
| Consumes    | interpreter architecture, JSON input stream |

## Intent

The application root contains an executable named `jq`. It accepts the exercised `-c '<program>'` interface, reads JSON values from standard input, evaluates the filter, and emits every generated result as a compact JSON value on its own output line.

The entry point is self-contained within the modular Python implementation and does not require installation or environment configuration beyond the standard Python runtime.

## Programmatic Acceptance

=== AC executable-basic-filters ===
Intent: The executable accepts the required -c interface and executes the basic corpus slice.

import json
import os
import subprocess
import sys

result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", r"^(true|false|null|1)$", "--json"],
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
=== END AC executable-basic-filters ===

=== AC executable-stdin-output ===
Intent: The executable reads JSON from stdin and emits one result for each generated output.

import json
import subprocess

payload = "[1,2,3]\n"
result = subprocess.run(
    ["./jq", "-c", ".[]"],
    input=payload,
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr, file=__import__("sys").stderr)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
expected = json.loads(payload)
assert actual == expected
=== END AC executable-stdin-output ===

## User Acceptance

- None.

## Guardrails

- The executable must be named exactly `jq` and be executable at the application root.
- Only the exercised `-c` interface is required.
- Output must remain one compact JSON value per line.
