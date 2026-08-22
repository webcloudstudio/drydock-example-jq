# FEATURE: Control Flow Recursion

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Implements recursive filters, recursive descent, and ordered structural traversal. |
| Depends On  | ARCHITECTURE.md, FEATURE-Control-Reduce.md |
| Provides    | recurse, recursive descent |
| Consumes    | generator evaluator, control flow |

## Behavior

`recurse` emits the current value followed by recursively generated descendants. Its filter and condition variants preserve depth-first jq ordering. `..` is equivalent to the zero-argument recursive traversal and handles arrays and objects through optional iteration. Recursive generator evaluation must preserve multiplicity and avoid changing the observable order of outputs.

## Programmatic Acceptance

=== AC control-recursion-suite ===
Intent: Execute the conformance cases covering recurse variants and recursive descent.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys
from pathlib import Path

assert Path("jq").is_file()

select = r"recurse|\\.\\."
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
=== END AC control-recursion-suite ===

=== AC control-recursion-order-suite ===
Intent: Execute recursive traversal cases that assert ordered descendant generation.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys
from pathlib import Path

assert Path("jq").is_file()

select = r"\\[\\.\\.|\\.\\. \\|"
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
=== END AC control-recursion-order-suite ===

## User Acceptance

- None.

## Guardrails

- Recursive traversal must emit the root before descendants.
- Preserve depth-first ordering and generator multiplicity.
- Do not follow non-iterable scalar values as children.
