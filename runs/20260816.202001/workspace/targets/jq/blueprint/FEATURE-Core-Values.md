# FEATURE: Core jq Values

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Implements jq core values, indexing, iteration, slicing, and construction. |
| Depends On  | FEATURE-Generator-Runtime.md |
| Provides    | identity, literals, indexing, slicing, iteration, arrays, objects, recursive descent, empty |
| Consumes    | generator evaluator |

## Intent

Implement JSON value operations and core jq filter constructs, including field access, array and object construction, iteration, optional access, slices, and recursive descent.

## Scope

- Identity and JSON literals.
- Object fields, array indexes, dynamic indexes, and optional access.
- Array and string slices.
- Array/object iterators.
- Array and object constructors.
- Recursive descent and core path traversal.

## Programmatic Acceptance

=== AC core-values-suite ===
Intent: Core value behavior passes its authoritative conformance slice.
Suite: scoped

import subprocess

result = subprocess.run(
    ["python3", "sources/run_conformance.py", "--select", r"(\.foo|\.\[|^\[\.)"],
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr)
assert result.returncode == 0
=== END AC core-values-suite ===

=== AC core-values-indexing ===
Intent: Field access and iteration return the corresponding supplied values.

import json
import subprocess

value = {"items": [{"name": "a"}, {"name": "b"}]}
program = ".items[] | .name"
result = subprocess.run(
    ["./jq", "-c", program],
    input=json.dumps(value) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
expected = [item["name"] for item in value["items"]]
assert actual == expected
=== END AC core-values-indexing ===

=== AC core-values-construction ===
Intent: Array construction collects all outputs from its generator expression.

import json
import subprocess

program = "[range(0; 3)]"
result = subprocess.run(
    ["./jq", "-c", program],
    input="null\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = json.loads(result.stdout)
assert actual == list(range(0, 3))
=== END AC core-values-construction ===

## User Acceptance

- None.

## Guardrails

- Do not coerce invalid indexes silently except where jq specifies null or optional suppression.
- Preserve object key order for output construction where observable.
- Keep path-aware operations compatible with later assignment and structural builtins.
