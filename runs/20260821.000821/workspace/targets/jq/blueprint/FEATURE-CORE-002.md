# FEATURE: Basic Filters and Constructors

| Field       | Value |
|-------------|-------|
| Version     | 20260821 V1 |
| Description | Implement jq identity, literals, accessors, constructors, iteration, slices, recursion, and empty. |
| Depends On  | FEATURE-CORE-001.md |
| Provides    | identity, literals, fields, indexing, iteration, slices, arrays, objects, recurse, empty |
| Consumes    | generator evaluation |

## Scope

Implement identity and literal filters; object field access; string, numeric, and computed indexing; optional access; array and object iteration; slices; recursive descent; array and object constructors; and `empty`.

## Programmatic Acceptance

=== AC core-002-access-and-constructors ===
Intent: The implementation passes the executing conformance cases for accessors, indexing, slices, arrays, and objects.
Suite: scoped

import json
import os
import subprocess
import sys

selector = r"^\." + r"|\[" + r"|\{" + r"|\.\[" + r"|\.\w"
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
=== END AC core-002-access-and-constructors ===

=== AC core-002-generators ===
Intent: The implementation passes the executing conformance cases for iteration, recursive descent, optional access, and empty.
Suite: scoped

import json
import os
import subprocess
import sys

selector = r"\.\.|\.\\[\\]|empty|recurse|\?"
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
=== END AC core-002-generators ===

## User Acceptance

- None.

## Guardrails

- Accessors must preserve jq's null and optional-error semantics.
- Constructors must collect all generated values in order.
- Recursive descent must preserve depth-first generator ordering.
