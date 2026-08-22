# FEATURE: Input Stream Controls

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provide jq input stream controls over the fixed standard-input interface. |
| Depends On  | ARCHITECTURE.md, FEATURE-TEXT-004.md |
| Provides    | input, inputs, input_filename, input_line_number |
| Consumes    | JSON stdin reader |

## Workflow

Expose the remaining JSON values from the process input stream through `input` and `inputs`, while preserving the already-selected current input and generator ordering. Provide the fixed-interface filename and line-number primitives required by the corpus.

## Programmatic Acceptance

=== AC io-001-input-conformance ===
Intent: The authoritative corpus cases covering input stream controls execute and pass.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

selector = r"input|inputs|input_filename|input_line_number"
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
=== END AC io-001-input-conformance ===

=== AC io-001-streams ===
Intent: The selected corpus includes both single-next-input and remaining-input stream behavior.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

selector = r"\binput\b|\binputs\b"
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
=== END AC io-001-streams ===

## User Acceptance

- None.

## Guardrails

- Read only the fixed standard input stream; do not add command-line input modes.
- Preserve the distinction between the current input and remaining inputs.
