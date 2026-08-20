# FEATURE: Control Conditionals

| Field | Value |
|-------|-------|
| Version | 20260820 V1 |
| Description | Implement jq conditionals, boolean filters, lexical labels, and breaks. |
| Depends On | FEATURE-Core-Errors.md, FEATURE-Paths-Assignment.md |
| Provides | if, then, elif, else, end, label, break, and, or, not |
| Consumes | runtime error handling, generator evaluation, assignment, bindings |

## Capability

Conditional expressions use jq truthiness, preserve generator behavior, and implement lexical labels and breaks.

## Programmatic Acceptance

=== AC control-conditionals-suite ===
Intent: The authoritative conditional, label, break, and boolean cases owned by this story execute and pass.
Suite: behavioral
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

SELECT = r"(if|label|break|and|or|not)"
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
=== END AC control-conditionals-suite ===

=== AC control-conditionals-label-error ===
Intent: A break without a visible lexical label is rejected at compile time.
Requires: executable=python3; scope=test

import os
import subprocess

result = subprocess.run(
    ["./jq", "-c", "break $missing"],
    input="null\n",
    capture_output=True,
    text=True,
    env={**os.environ},
)
assert result.returncode == 3
assert result.stderr is not None
=== END AC control-conditionals-label-error ===

## User Acceptance

- None.

## Guardrails

- Do not use Python truthiness in place of jq truthiness.
- A label's scope is lexical, not dynamically discovered.
- Break must stop the labeled generator without leaking later outputs.
- Conditional branches must preserve generator ordering and multiplicity.
