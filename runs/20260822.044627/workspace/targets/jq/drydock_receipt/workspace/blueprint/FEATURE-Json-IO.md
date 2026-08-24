# FEATURE: JSON Input and Output

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provides ordered JSON input processing, Unicode handling, numeric values, and compact output serialization. |
| Depends On  | FEATURE-Process-Contract.md |
| Provides    | JSON stdin parsing, compact JSON serialization, ordered output stream |
| Consumes    | ./jq -c program execution |

## Input Processing

Read the JSON values supplied by standard input in corpus order. Evaluate the filter independently against each input while preserving the global output order. Support Unicode escapes and characters, embedded control characters, large numeric literals, NaN, and infinities where required by jq semantics.

## Output Processing

Serialize every generated jq value as one compact JSON value per line. Structural comparison, not object key spelling or whitespace, defines conformance, but serialization must remain valid JSON-compatible output for the harness. Preserve generator multiplicity and ordering.

## Programmatic Acceptance

=== AC exec-003-conformance ===
Intent: JSON numeric values compile and execute successfully with compact output.

import subprocess

result = subprocess.run(
    ["./jq", "-c", "nan, infinite"],
    input="null\n",
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr, file=__import__("sys").stderr)
assert result.returncode == 0
assert len(result.stdout.splitlines()) == 2
=== END AC exec-003-conformance ===

=== AC exec-003-multiple-inputs ===
Intent: Multiple newline-delimited JSON inputs produce outputs in input and generator order.

import subprocess

inputs = "1\n2\n3\n"
result = subprocess.run(
    ["./jq", "-c", "."],
    input=inputs,
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr, file=__import__("sys").stderr)
assert result.returncode == 0
assert result.stdout.splitlines() == inputs.splitlines()
=== END AC exec-003-multiple-inputs ===

=== AC exec-003-unicode-and-compact ===
Intent: Unicode input is decoded and emitted as one compact JSON value per line.

import subprocess

value = '"\\u03bc"'
result = subprocess.run(
    ["./jq", "-c", "."],
    input=value + "\n",
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr, file=__import__("sys").stderr)
assert result.returncode == 0
lines = result.stdout.splitlines()
assert len(lines) == 1
assert __import__("json").loads(lines[0]) == __import__("json").loads(value)
=== END AC exec-003-unicode-and-compact ===

## User Acceptance

- None.

## Guardrails

- Preserve input and output ordering.
- Emit one output value per line.
- Do not pretty-print output.
- Preserve generator multiplicity.
- Do not silently discard Unicode or special numeric values required by the corpus.
