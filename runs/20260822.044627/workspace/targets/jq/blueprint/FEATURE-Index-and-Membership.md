# FEATURE: Index and Membership

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provides jq index lookup, binary search, quantifier, emptiness, and SQL-style membership utilities. |
| Depends On  | FEATURE-Object-and-Containment-Builtins.md, FEATURE-Truthiness-and-Comparison.md |
| Provides    | indices, index, rindex, bsearch, all, any, isempty, IN |
| Consumes    | collection and comparison builtins, ordered generators |

## Scope

This feature implements string and array occurrence searches, insertion-point binary search, generator-aware quantifiers, emptiness checks, and SQL-style `IN` functions.

## Behavior

- `indices` returns all matching string or array positions.
- `index` and `rindex` return the first and last matching positions.
- `bsearch` returns an index or jq's negative insertion-point encoding.
- `all` and `any` preserve short-circuit behavior over generated values.
- `isempty` distinguishes empty streams from streams that produce values.
- `IN` supports source and comparison generator forms.

## Programmatic Acceptance

=== AC data-004-conformance ===
Intent: Index lookup and membership behavior is implemented.

import json
import subprocess

result = subprocess.run(
    ["./jq", "-c", "[indices(\"a\"), index(\"a\"), rindex(\"a\")]"],
    input="\"banana\"\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
assert json.loads(result.stdout) == [[1, 3, 5], 1, 5]

=== END AC data-004-conformance ===

## User Acceptance

- None.

## Guardrails

- Preserve match positions in jq codepoint/index semantics.
- Do not evaluate generator operands beyond required short-circuit points.
- Do not modify files under `sources/`.
