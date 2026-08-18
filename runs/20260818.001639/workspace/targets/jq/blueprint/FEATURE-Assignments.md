# FEATURE: Assignments

| Field       | Value |
|-------------|-------|
| Version     | 20260818 V1 |
| Description | Provide jq plain, update, arithmetic, and defined-or assignments. |
| Depends On  | FEATURE-Path-Mutation.md |
| Provides    | =, |=, +=, -=, *=, /=, %=, //=
| Consumes    | setpath, delpaths, del, path discovery |

## Purpose

Implement jq assignment operators over exact, generated, and multi-result paths.

## Behavior

- Plain `=` evaluates the right-hand side against the original input and uses every produced value.
- Update assignment evaluates the right-hand side against each selected path value and uses the first result.
- Empty update results delete the selected path.
- Arithmetic assignments behave as update assignment with the corresponding arithmetic operator.
- Defined-or assignment updates only false or null values according to jq semantics.
- Multiple selected paths, overlapping paths, array growth, and immutable results follow jq ordering and backtracking rules.
- Invalid path expressions and invalid updates retain jq runtime error behavior.

## Programmatic Acceptance

=== AC assignments-suite ===
Intent: The implementation passes the authoritative conformance cases for all assignment operators.
Suite: scoped

import os
import subprocess
import sys

selector = r"(=|\\|=|\\+=|-=|\\*=|/=|%=|//=)"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--list", "--select", selector],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC assignments-suite ===

=== AC assignments-paths ===
Intent: Assignment cases involving generated and multi-result paths execute successfully.
Suite: scoped

import os
import subprocess
import sys

selector = r"(\\.\\[\\]|\\.\\[[^]]*,[^]]*\\]|select\\([^)]*\\).*\\|=|setpath)"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--list", "--select", selector],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC assignments-paths ===

## User Acceptance

- None.

## Guardrails

- Assignment must preserve immutable jq value semantics.
- Plain and update assignment must not be conflated.
- Empty-result and multi-path behavior must preserve selection order and jq deletion rules.
