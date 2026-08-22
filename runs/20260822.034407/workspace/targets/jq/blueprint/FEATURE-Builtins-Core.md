# FEATURE: Builtins Core

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provides jq's core type, collection, ordering, containment, string, and Unicode builtins. |
| Depends On  | FEATURE-Functions-Definitions.md, FEATURE-Paths-Access.md, FEATURE-Control-Recursion.md |
| Provides    | type and collection builtins, sorting, grouping, uniqueness, containment, indexing helpers, string operations, Unicode helpers |
| Consumes    | user-defined functions, variables, paths, control flow |

## Intent

Implement the core builtins described by `sources/builtin.jq` and `sources/jq-manual.txt`, including type predicates, collection transforms, sorting and grouping, containment, indexing, string manipulation, Unicode conversion, and related helpers. Preserve generator multiplicity and jq ordering.

## Programmatic Acceptance

=== AC builtins-core-collections ===
Intent: The authoritative corpus slice covering core collection, type, ordering, containment, and indexing builtins passes.
Suite: scoped

import json
import os
import subprocess
import sys
from pathlib import Path

assert Path("jq").is_file()

selector = r"type|keys|sort|group_by|unique|contains|inside|indices|index|rindex|flatten|transpose|to_entries|from_entries|map_values"
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

=== END AC builtins-core-collections ===

=== AC builtins-core-strings ===
Intent: The authoritative corpus slice covering string, trimming, joining, and Unicode builtins passes.
Suite: scoped

import json
import os
import subprocess
import sys
from pathlib import Path

assert Path("jq").is_file()

selector = r"join|split|trim|startswith|endswith|explode|implode|ascii_|reverse"
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

=== END AC builtins-core-strings ===

## User Acceptance

- None.

## Guardrails

- Implement only standard-library functionality; do not add third-party jq bindings.
- Preserve jq generator ordering, multiplicity, structural comparison, and Unicode codepoint semantics.
