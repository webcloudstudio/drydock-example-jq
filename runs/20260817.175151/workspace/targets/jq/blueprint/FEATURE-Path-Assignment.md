# FEATURE: Path Assignment

| Field       | Value |
|-------------|-------|
| Version     | 20260817 V1 |
| Description | Implement jq plain, update, arithmetic, and defined-or assignments. |
| Depends On  | FEATURE-Path-Mutation.md, FEATURE-Flow-Bindings.md, FEATURE-Flow-Control-Errors.md |
| Provides    | =, |=, +=, -=, *=, /=, %=, //= |
| Consumes    | path mutation, generator evaluation, lexical bindings |

## Intent

Implement assignment over exact and generated path expressions. Plain assignment evaluates the right-hand side against the original input and emits one result per right-hand-side value. Update assignment evaluates against each selected path value and uses only the first result. Arithmetic and defined-or assignments follow jq's update-assignment semantics.

## Programmatic Acceptance

=== AC plain-assignment ===
Intent: Plain assignment evaluates the right-hand side against the original input.

import json
import os
import subprocess

payload = {"a": 1, "b": 4}
program = ".a = .b"
result = subprocess.run(
    [os.path.join(os.getcwd(), "jq"), "-c", program],
    input=json.dumps(payload),
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = json.loads(result.stdout)
assert actual["a"] == payload["b"]
assert actual["b"] == payload["b"]
=== END AC plain-assignment ===

=== AC update-assignment ===
Intent: Update assignment transforms the selected value rather than the root input.

import json
import os
import subprocess

payload = {"a": 4, "b": 9}
program = ".a |= . + 1"
result = subprocess.run(
    [os.path.join(os.getcwd(), "jq"), "-c", program],
    input=json.dumps(payload),
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = json.loads(result.stdout)
assert actual["a"] == payload["a"] + 1
assert actual["b"] == payload["b"]
=== END AC update-assignment ===

=== AC arithmetic-and-defined-assignment ===
Intent: Arithmetic and defined-or assignments update selected fields with jq semantics.

import json
import os
import subprocess

payload = {"n": 2, "missing": None}
program = "(.n += 3), (.missing //= .n)"
result = subprocess.run(
    [os.path.join(os.getcwd(), "jq"), "-c", program],
    input=json.dumps(payload),
    capture_output=True,
    text=True,
)
assert result.returncode == 0
outputs = [json.loads(line) for line in result.stdout.splitlines()]
assert outputs[0]["n"] == payload["n"] + 3
assert outputs[0]["missing"] is None
assert outputs[1]["missing"] == payload["n"]
=== END AC arithmetic-and-defined-assignment ===

=== AC multi-path-assignment ===
Intent: A single assignment applies to every selected path while preserving array shape.

import json
import os
import subprocess

payload = [1, 2, 3]
program = ".[] |= . * 2"
result = subprocess.run(
    [os.path.join(os.getcwd(), "jq"), "-c", program],
    input=json.dumps(payload),
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = json.loads(result.stdout)
assert len(actual) == len(payload)
assert actual == [item * 2 for item in payload]
=== END AC multi-path-assignment ===

## User Acceptance

- None.

## Guardrails

- Assignment must preserve jq's immutable value model.
- Plain and update assignment must retain their distinct generator behavior.
- Empty update results delete selected paths; they must not fabricate null values.
