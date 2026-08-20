# FEATURE: Builtins Streaming

| Field | Value |
|-------|-------|
| Version | 20260820 V1 |
| Description | Provide jq streaming conversion, truncation, reconstruction, and SQL-style lookup builtins. |
| Depends On | FEATURE-Builtins-Numeric.md |
| Provides | tostream, fromstream, truncate_stream, INDEX, JOIN, IN |
| Consumes | jq generator evaluator, jq path operations, jq value comparison semantics |

## Scope

This feature implements conversion between ordinary jq values and stream representations, stream truncation and reconstruction, and the `INDEX`, `JOIN`, and `IN` SQL-style builtins.

## Programmatic Acceptance

=== AC builtins-streaming-conformance ===
Intent: The streaming and SQL-style builtin corpus slice executes and passes with at least one selected case.
Suite: behavioral
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

SELECT = r"(stream|tostream|fromstream|truncate_stream|INDEX|JOIN|IN\()"
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
=== END AC builtins-streaming-conformance ===

## User Acceptance

- Stream round-trips and lookup operations preserve the documented jq semantics.

## Guardrails

- Streaming builtins must not consume or reorder values beyond their specified generator behavior.
- Do not modify staged scoring assets.
