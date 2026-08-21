# FEATURE: Scoped Conformance Verification

| Field       | Value |
|-------------|-------|
| Version     | 20260821 V1 |
| Description | Provides executing, scoped conformance verification for implemented jq capabilities. |
| Depends On  | FEATURE-BUILTINS-008.md |
| Provides    | scoped conformance verification |
| Consumes    | executable jq, staged conformance harness, implemented capability slices |

## Purpose

Bind each implementation area to an executing, non-empty slice of the supplied authoritative conformance corpus.

## Behavior

- Every scoped invocation supplies the candidate through the inherited `JQ` environment.
- Selectors match program syntax owned by implemented capabilities.
- The machine-readable report is parsed as JSON.
- A scoped verification passes only when it matched cases, reported no failures or errors, and exited successfully.
- This story does not run the unfiltered corpus.

## Programmatic Acceptance

=== AC verification-001-scoped ===
Intent: The authoritative scoped conformance slice executes non-empty cases for representative implemented capabilities and passes completely.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

selector = r"reduce|foreach|recurse|path|def|map|split|test|@"
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
assert summary["fail"] == 0
assert summary["error"] == 0
assert result.returncode == 0
=== END AC verification-001-scoped ===

=== AC verification-001-environment ===
Intent: The scoped verification command receives the candidate through JQ and returns a machine-readable successful report.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

selector = r"walk|pick|INDEX|JOIN|IN\(|bsearch"
candidate = f"{os.getcwd()}/jq"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", selector, "--json"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": candidate},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
report = json.loads(result.stdout)
assert report["candidate"] == [candidate]
assert sum(report["summary"].values()) > 0
assert result.returncode == 0
=== END AC verification-001-environment ===

## User Acceptance

- None.

## Guardrails

- Never invoke the harness in non-executing enumeration or dry-run mode.
- Never invoke the unfiltered corpus from this story.
- Preserve the supplied harness and corpus unchanged.
