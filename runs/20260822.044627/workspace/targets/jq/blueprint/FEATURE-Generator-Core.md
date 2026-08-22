# FEATURE: Generator Core

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Evaluate jq filters as ordered streams with multiplicity, empty results, iteration, and backtracking. |
| Depends On  | FEATURE-Filter-Grammar.md, FEATURE-Value-Model.md |
| Provides    | Ordered filter generators, empty, iteration, range, and backtracking |
| Consumes    | Parsed jq expressions, JSON value model |

## Scope

Every filter shall evaluate as a generator that can produce zero, one, or many values. The evaluator shall preserve output ordering, multiplicity, downstream execution for every upstream value, empty results, iteration, and backtracking.

## Programmatic Acceptance

=== AC generator-core-conformance ===
Intent: The authoritative corpus slice exercising identity, iteration, comma generators, range, and empty behavior executes and passes with no failures or errors.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

select = r"\.|,|\[\.\]|range|empty"
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
=== END AC generator-core-conformance ===

=== AC generator-order-and-multiplicity ===
Intent: The selected generator cases complete successfully, proving ordered multiplicity rather than scalar-only evaluation.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

select = r"\.|,|\[\.\]|range|empty"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", select, "--json"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
report = json.loads(result.stdout)
summary = report["summary"]
assert summary["pass"] + summary["fail"] + summary["error"] + summary["skip"] > 0
assert summary["fail"] == 0 and summary["error"] == 0
assert result.returncode == 0
=== END AC generator-order-and-multiplicity ===

## User Acceptance

- None.

## Guardrails

- Preserve generator order and multiplicity exactly.
- Do not collapse streams into single values during evaluation.
- `empty` must produce no output and must backtrack to the preceding generator.
