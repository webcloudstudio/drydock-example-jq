# FEATURE: Core Values

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Implements jq values, indexing, iteration, slicing, and construction. |
| Depends On  | ARCHITECTURE.md, FEATURE-Core-Generator.md |
| Provides    | literals, field access, indexing, iteration, slices, arrays, objects |
| Consumes    | generator evaluator, jq AST |

## Intent

This feature evaluates JSON literals and constructs, identity, field access, array and object indexing, optional access, iteration, negative indices, slices, and generator-preserving array and object construction.

## Programmatic Acceptance

=== AC core-values-conformance ===
Intent: The interpreter passes the authoritative corpus cases covering values, indexing, iteration, slicing, and construction.
Suite: scoped

import json
import os
import subprocess
import sys
from pathlib import Path

assert Path("jq").is_file()

selector = r"\.foo|\.|\.\[|\.\[\]|\[[^]]*\]|^\{"
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
=== END AC core-values-conformance ===

## User Acceptance

- None.

## Guardrails

- Preserve generator ordering and multiplicity.
- Preserve immutable JSON values and compact JSON-compatible semantics.
