# FEATURE: Core Expressions

| Field | Value |
|-------|-------|
| Version | 20260820 V1 |
| Description | Implement jq values, indexing, construction, and core operators. |
| Depends On | FEATURE-Core-Generators.md |
| Provides | literals, field and index access, slices, arrays, objects, arithmetic, comparison, boolean operators |
| Consumes | ordered generator evaluation, pipeline composition, backtracking |

## Scope

Implement JSON literals, field and index access, optional indexing, iteration, slices, construction, recursive descent, arithmetic, comparisons, and boolean operators while preserving jq semantics.

## Programmatic Acceptance

=== AC expressions-conformance ===
Intent: The selected core-expression corpus slice executes and passes.
Suite: behavioral
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

SELECT = r"(\+|-|\*|/|%|==|!=|<|>|\[|\{|\.\[)"
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
=== END AC expressions-conformance ===

=== AC expressions-indexing ===
Intent: Field and array indexing return values derived from supplied JSON input.
Requires: executable=python3; scope=test

import json
import subprocess

payload = '{"a":[10,20,30]}\n'
result = subprocess.run(["./jq", "-c", "[.a[1], .a[-1]]"], input=payload, capture_output=True, text=True)
assert result.returncode == 0
assert json.loads(result.stdout) == [10, 30]
=== END AC expressions-indexing ===

=== AC expressions-arithmetic ===
Intent: Numeric arithmetic evaluates using supplied operands.
Requires: executable=python3; scope=test

import json
import subprocess

result = subprocess.run(["./jq", "-c", "2 + 3"], input="null\n", capture_output=True, text=True)
assert result.returncode == 0
assert json.loads(result.stdout) == 5
=== END AC expressions-arithmetic ===

## User Acceptance

- None.

## Guardrails

- Do not implicitly convert strings, booleans, arrays, or objects during arithmetic.
- Preserve jq comparison ordering and boolean truthiness.
- Use only Python standard-library facilities.
