# FEATURE: CLI Command Interface

| Field       | Value |
|-------------|-------|
| Version     | 20260817 V1 |
| Description | Defines the executable jq command interface for compact JSON filtering. |
| Depends On  | ARCHITECTURE.md |
| Provides    | ./jq -c, stdin JSON stream processing, compact JSON output |
| Consumes    | interpreter module boundaries |

## Workflow

1. Start the executable as `./jq -c '<program>'`.
2. Read successive JSON texts from standard input.
3. Evaluate the compiled filter once for each input value.
4. Emit every produced value as one compact JSON text followed by a newline.
5. Return zero after all inputs and outputs complete successfully.

The implementation need support only the exercised `-c` interface. It must preserve output order and multiplicity across multiple input texts.

## Interface Contract

| Input | Contract |
|---|---|
| Program | One jq filter supplied after `-c` |
| Standard input | One or more JSON texts |
| Standard output | One compact JSON value per produced result |
| Successful exit | `0` |

## Programmatic Acceptance

=== AC cli-001-single-input ===
Intent: The executable evaluates a compact filter against one JSON input and emits the parsed result.
import json
import subprocess

input_value = {"name": "jq", "enabled": True}
result = subprocess.run(
    ["./jq", "-c", ".name"],
    input=json.dumps(input_value) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
expected = [input_value["name"]]
assert actual == expected
=== END AC cli-001-single-input ===

=== AC cli-001-multiple-inputs ===
Intent: The executable processes multiple JSON texts from standard input independently and in order.
import json
import subprocess

input_values = [{"value": 1}, {"value": 2}, {"value": 3}]
result = subprocess.run(
    ["./jq", "-c", ".value"],
    input="".join(json.dumps(value) + "\n" for value in input_values),
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
expected = [value["value"] for value in input_values]
assert actual == expected
=== END AC cli-001-multiple-inputs ===

=== AC cli-001-generator-output ===
Intent: The executable emits each generator result as a separate compact JSON line in generator order.
import json
import subprocess

input_value = None
result = subprocess.run(
    ["./jq", "-c", "range(3)"],
    input=json.dumps(input_value) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
expected = list(range(3))
assert actual == expected
=== END AC cli-001-generator-output ===

## User Acceptance

- None.

## Guardrails

- The executable must be named `jq` and be executable at the application root.
- Support `-c` as exercised by the supplied harness.
- Emit no diagnostics on standard output.
- Do not modify or reinterpret the supplied conformance harness.
