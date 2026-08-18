# FEATURE: Generator Core

| Field       | Value |
|-------------|-------|
| Version     | 20260818 V1 |
| Description | Evaluate jq filters as ordered generators with pipeline backtracking and partial runtime output. |
| Depends On  | FEATURE-Parser.md, FEATURE-Compile-Diagnostics.md |
| Provides    | ordered filter generators, pipeline backtracking, stream errors |
| Consumes    | jq parser and AST |

## Evaluation model

Every filter receives one input and produces an ordered stream of zero or more outputs. Pipeline evaluation feeds each output from the left filter into the right filter in order. Comma evaluation emits all left outputs before all right outputs.

The evaluator must preserve:

- Zero-output filters such as `empty`.
- Multiplicity and cartesian products.
- Generator ordering and downstream backtracking.
- Laziness where required by short-circuiting constructs.
- Values emitted before a later runtime error.

Runtime failures propagate with status `5` unless caught by jq control flow.

## Programmatic Acceptance

=== AC generator-corpus-slice ===
Intent: The evaluator passes the corpus slice covering comma, pipe, iteration, ranges, empty, generator multiplicity, and partial output.
Suite: scoped

import os
import subprocess
import sys

selector = r"(,|\||empty|\.\[\]|range\(|while\(|limit\(|skip\(|first\(|last\(|nth\(|error\()"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--list", "--select", selector],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC generator-corpus-slice ===

=== AC generator-preserves-prefix ===
Intent: A runtime failure after a generated value preserves the emitted prefix and returns runtime status 5.
import json
import subprocess

result = subprocess.run(
    ["./jq", "-c", "1, error(\"stop\")"],
    input="null\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 5
lines = result.stdout.splitlines()
assert lines
assert json.loads(lines[0]) == 1
=== END AC generator-preserves-prefix ===

## User Acceptance

- None.

## Guardrails

- Never collapse a generator to a single return value.
- Preserve output order and multiplicity.
- Do not discard output emitted before a runtime error.
- Keep compile status `3` distinct from runtime status `5`.
