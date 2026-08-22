# FEATURE: Diagnostics and Standard Error Output

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provide jq diagnostic filters and controlled standard-error behavior. |
| Depends On  | ARCHITECTURE.md, FEATURE-IO-001.md, FEATURE-EXEC-002.md |
| Provides    | debug, stderr, halt_error |
| Consumes     | process exit and diagnostic contract |

## Workflow

Implement `debug` and `stderr` as side-effecting filters that preserve the required value stream, and implement `halt_error` with its documented stderr emission and exit behavior. Keep diagnostic output separate from JSON values written to stdout.

## Programmatic Acceptance

=== AC io-002-diagnostics-conformance ===
Intent: The authoritative corpus cases covering debug, stderr, and halt_error execute and pass.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

selector = r"debug|stderr|halt_error"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", selector, "--json"],
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
=== END AC io-002-diagnostics-conformance ===

=== AC io-002-channels ===
Intent: The selected corpus exercises diagnostic filters while the conformance runner observes the declared process contract.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

selector = r"debug|stderr|halt_error"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", selector, "--json"],
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
=== END AC io-002-channels ===

## User Acceptance

- None.

## Guardrails

- Diagnostics must never be emitted as JSON values on stdout.
- Do not assert diagnostic message wording; preserve only the documented channels and exit semantics.
