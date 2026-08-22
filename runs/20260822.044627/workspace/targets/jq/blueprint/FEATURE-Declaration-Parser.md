# FEATURE: Declaration Parser

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Parse jq declarations, control syntax, bindings, modules, and destructuring. |
| Depends On  | FEATURE-Filter-Parser.md |
| Provides    | declarations, modules grammar, conditionals, exceptions, reductions, labels, bindings |
| Consumes    | AST for filter expressions |

## Programmatic Acceptance

=== AC parse-004-declarations ===
Intent: Declarations and bindings parse and execute successfully.
import json
import os
import subprocess

env = {**os.environ, "PATH": os.environ.get("PATH", "")}

result = subprocess.run(
    ["./jq", "-c", "def inc: . + 1; inc"],
    input="2\n",
    capture_output=True,
    text=True,
    env=env,
)
assert result.returncode == 0, result.returncode
assert json.loads(result.stdout) == 3

result = subprocess.run(
    ["./jq", "-c", ". as {$x} | $x"],
    input='{"x":4}\n',
    capture_output=True,
    text=True,
    env=env,
)
assert result.returncode == 0, result.returncode
assert json.loads(result.stdout) == 4
=== END AC parse-004-declarations ===

=== AC parse-004-module-rejections ===
Intent: Invalid declaration syntax is rejected as a compile error.
import os
import subprocess

env = {**os.environ, "PATH": os.environ.get("PATH", "")}

result = subprocess.run(
    ["./jq", "-c", "def ;"],
    input="null\n",
    capture_output=True,
    text=True,
    env=env,
)
assert result.returncode == 3, result.returncode
assert result.stdout == ""

result = subprocess.run(
    ["./jq", "-c", "if true then"],
    input="null\n",
    capture_output=True,
    text=True,
    env=env,
)
assert result.returncode == 3, result.returncode
assert result.stdout == ""
=== END AC parse-004-module-rejections ===

## User Acceptance

- None.

## Guardrails

- Do not resolve or load excluded module fixtures.
- Preserve lexical scope for bindings, labels, and function declarations.
- Do not modify files under `sources/`.
