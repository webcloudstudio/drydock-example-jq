# FEATURE: Assignment Operators

| Field       | Value |
|-------------|-------|
| Version     | 20260821 V1 |
| Description | Defines jq plain, update, arithmetic, and defined-or assignment operators over paths. |
| Depends On  | FEATURE-PATHS-002.md |
| Provides    | =, |=, +=, -=, *=, /=, %=, //=
| Consumes    | path discovery, setpath, delpaths, generator evaluator |

## Intent

Implement assignment operators over path expressions. Plain assignment evaluates the RHS against the original input and uses every RHS output; update assignment evaluates the RHS against each selected old value and uses the first result; empty RHS deletes the selected path.

## Behavior

- `=` supports multiple LHS paths and multiple RHS outputs in jq order.
- `|=` updates selected values using the update filter.
- `+=`, `-=`, `*=`, `/=`, and `%=` are update assignments using the corresponding arithmetic operator.
- `//=` updates only null or false values.
- Assignments remain immutable and preserve the original input for sibling expressions.
- Generator paths, slices, deletion through `empty`, and invalid updates follow jq runtime semantics.

## Programmatic Acceptance

=== AC paths-003-conformance ===
Intent: The assignment corpus slice executes and passes for plain, update, arithmetic, and defined-or assignments.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

select = r"[.]?[^\n]*(\|=|\+=|-=|\*=|/=|%=|//=| = )"
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
=== END AC paths-003-conformance ===

=== AC paths-003-generator-and-deletion ===
Intent: The assignment slice covers multi-path updates, generator RHS behavior, and deletion through empty.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

select = r"\.[] =|range\(3\)|\|= empty|\.foo\[1,4,2,3\] \|= empty"
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
=== END AC paths-003-generator-and-deletion ===

## User Acceptance

- None.

## Guardrails

- Never mutate the source value in place.
- Keep plain assignment distinct from update assignment.
- Use exit status `5` for runtime assignment failures and preserve earlier output.
- Do not implement assignments by shelling out to another jq executable.
