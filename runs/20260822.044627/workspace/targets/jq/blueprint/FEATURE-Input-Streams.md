# FEATURE: Input Streams

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Implement jq filters for consuming additional JSON inputs and input metadata. |
| Depends On  | FEATURE-JSON-IO-Boundary.md, FEATURE-Generator-Core.md |
| Provides    | input, inputs, input_filename, input_line_number |
| Consumes    | JSON process boundary, generator evaluator |

## Intent

Implement `input` and `inputs` over the fixed stdin stream, coordinating consumption with the initial input value. Provide the input filename and line-number filters supported by the fixed executable interface.

## Programmatic Acceptance

=== AC io-001-conformance ===
Intent: The implementation passes the authoritative input-stream corpus slice.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

SELECT = r"input|inputs"
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
assert summary["fail"] == 0
assert summary["error"] == 0
assert result.returncode == 0
=== END AC io-001-conformance ===

## User Acceptance

- None.

## Guardrails

- Read inputs only from the process input stream.
- Preserve input order and generator semantics.
- Do not add unsupported command-line options or external input sources.
