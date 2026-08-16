# FEATURE: Regular-Expression Builtins

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Provide jq-compatible regular-expression matching and substitution builtins. |
| Depends On  | ARCHITECTURE.md, FEATURE-Builtins-Strings.md, FEATURE-Language-Functions.md |
| Provides    | test, match, capture, scan, split, splits, sub, gsub |
| Consumes    | evaluator and jq string values |

## Purpose

Implement the regex builtin family using Python's standard-library `re` module. Support jq regex flags, named and unnamed captures, global matching, UTF-8 codepoint offsets, regex splitting, and substitution interpolation.

## Behavior

- `test` returns Boolean match results.
- `match` emits match objects with `offset`, `length`, `string`, and `captures`.
- `capture` returns named captures as an object.
- `scan` emits matched strings or capture arrays.
- `split` returns an array; `splits` emits a stream.
- `sub` replaces the first matching region; `gsub` replaces all non-overlapping regions.
- Invalid patterns, unsupported inputs, and invalid flags raise jq runtime errors.
- Generator-valued replacement expressions preserve jq output ordering.

## Programmatic Acceptance

=== AC regex-runtime ===
Intent: The implementation supports matching, captures, scanning, splitting, and substitution through the public jq executable.

import json
import subprocess

program = '[test("a+"), match("(?<x>a+)"), capture("(?<x>a+)-(?<y>b+)"), [scan("[ab]+")], split(", "), sub("a"; "X"), gsub("a"; "X")]'
source = '"aa-bb, ab"'
result = subprocess.run(["./jq", "-c", program], input=source, capture_output=True, text=True)
print(result.stdout)
print(result.stderr)
assert result.returncode == 0
actual = json.loads(result.stdout)
assert actual[0] is True
assert actual[1]["string"] == "aa"
assert actual[2]["x"] == "aa"
assert actual[2]["y"] == "bb"
assert actual[3] == ["aa", "bb"]
assert actual[4] == ["aa-bb", "ab"]
assert actual[5] == "Xa-bb, ab"
assert actual[6] == "XX-bb, Xb"
=== END AC regex-runtime ===

=== AC regex-errors ===
Intent: Invalid regular-expression input produces the runtime failure exit code.

import subprocess

result = subprocess.run(
    ["./jq", "-c", 'test("[")'],
    input='"value"',
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr)
assert result.returncode == 5
=== END AC regex-errors ===

## User Acceptance

- None.

## Guardrails

- Use only Python standard-library regex facilities.
- Do not shell out to jq or use third-party regex or jq libraries.
