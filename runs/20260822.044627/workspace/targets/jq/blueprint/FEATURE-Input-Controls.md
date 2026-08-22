# FEATURE: Input Controls

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Define jq input-stream consumption and input metadata filters. |
| Depends On  | FEATURE-JSON-I-O.md, FEATURE-Generator-Core.md |
| Provides    | input, inputs, input_filename, input_line_number |
| Consumes    | JSON input stream and ordered generator evaluation |

## Scope

Implement `input` and `inputs` over the fixed stdin interface, including interaction with the initially consumed filter input. Provide the input filename and line-number filters required by the corpus within the supported command-line boundary.

## Programmatic Acceptance

=== AC input-controls-conformance ===
Intent: The authoritative corpus cases covering input-stream controls execute successfully.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

select = r"\binputs?\b|input_filename|input_line_number"
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
=== END AC input-stream-behavior ===
Intent: The authoritative corpus verifies consumption of remaining JSON values and the no-input runtime behavior.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

select = r"\binput\b|\binputs\b"
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
assert summary["pass"] > 0
assert summary["fail"] == 0
assert summary["error"] == 0
assert result.returncode == 0
=== END AC input-stream-behavior ===

## User Acceptance

- None.

## Guardrails

- Input controls must preserve the order of JSON values read from stdin.
- `input` and `inputs` must not silently swallow malformed or unavailable input.
- Do not introduce command-line options beyond the fixed `-c` interface.
