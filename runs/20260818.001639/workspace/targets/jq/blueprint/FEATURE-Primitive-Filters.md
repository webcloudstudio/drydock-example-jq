# FEATURE: Primitive Filters

| Field       | Value |
|-------------|-------|
| Version     | 20260818 V1 |
| Description | Implement jq primitive filters, constructors, indexing, iteration, and empty-stream behavior. |
| Depends On  | FEATURE-Generator-Core.md |
| Provides    | identity, literals, arrays, objects, fields, indexes, iteration, slices, comma, pipe, empty |
| Consumes    | ordered filter generators |

## Primitive semantics

Implement identity and literal filters, arrays and objects, shorthand and computed object keys, field access, numeric and string indexing, object and array iteration, slices, optional access, recursive descent, comma, pipe, and `empty`.

Indexing must follow jq's type rules, including null results for missing fields and out-of-range reads, errors for invalid non-optional accesses, negative indices, and slice normalization. Array and object constructors collect all values produced by their child filters in order.

## Programmatic Acceptance

=== AC primitive-corpus-slice ===
Intent: The primitive evaluator passes the corpus slice covering fields, indexing, iteration, slices, constructors, recursive descent, optional access, and empty.
Suite: scoped

import os
import subprocess
import sys

selector = r"(\.[A-Za-z_][A-Za-z_0-9]*|\.\[|\.{2}|\[\.\[\]|\[1|\{[A-Za-z_]|empty|recursive)"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--list", "--select", selector],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC primitive-corpus-slice ===

=== AC primitive-compact-output ===
Intent: Primitive filters emit one valid compact JSON value per output line.
import json
import subprocess

source = "[1, 2, null]"
result = subprocess.run(
    ["./jq", "-c", "."],
    input=source + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
values = [json.loads(line) for line in result.stdout.splitlines()]
assert values == [source]
=== END AC primitive-compact-output ===

## User Acceptance

- None.

## Guardrails

- Preserve constructor output ordering.
- Optional access suppresses only the relevant runtime error.
- Do not pretty-print or combine separate output values.
- Object keys must remain JSON strings.
