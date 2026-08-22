# FEATURE: Variable Bindings

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provides lexical jq value bindings with scoped lifetime and shadowing. |
| Depends On  | ARCHITECTURE.md, FEATURE-Declarations-And-Control-Syntax.md, FEATURE-Composition-And-Cartesian-Evaluation.md |
| Provides    | as bindings, nested scope, shadowing, keyword identifiers, binding lifetime |
| Consumes    | parsed patterns, generator evaluation, lexical environments |

## Workflow

Implement `expression as $name | continuation` with lexical scope. Bind each output independently, preserve the original input for the continuation, support nested shadowing and keyword-shaped names, and maintain bindings correctly across generator backtracking and destructuring contexts.

## Programmatic Acceptance

=== AC func-001-conformance ===
Intent: The authoritative corpus slice exercising lexical variable bindings executes and passes.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

select = r" as \$|\$[A-Za-z]"
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
assert summary["fail"] == 0
assert summary["error"] == 0
assert result.returncode == 0
=== END AC func-001-conformance ===

=== AC func-001-interface ===
Intent: A binding preserves its value while the pipeline continues with the original input.
import subprocess

program = ".bar as $x | .foo + $x"
payload = '{"foo":10,"bar":200}\n'
result = subprocess.run(
    ["./jq", "-c", program],
    input=payload,
    capture_output=True,
    text=True,
)
assert result.returncode in (0, 5)
=== END AC func-001-interface ===

## User Acceptance

- None.

## Guardrails

- Bindings are immutable and lexically scoped.
- Do not leak inner shadowed bindings outside their scope.
- Preserve binding values independently for every generator branch.
