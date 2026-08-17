# FEATURE: jq Regular-Expression Builtins

| Field       | Value |
|-------------|-------|
| Version     | 20260817 V1 |
| Description | Provide jq regular-expression matching, scanning, splitting, and substitution builtins. |
| Depends On  | FEATURE-BUILTIN-002.md, FEATURE-EVAL-001.md |
| Provides    | test, match, capture, scan, split, splits, sub, gsub |
| Consumes    | string builtins, generator evaluator |

## Purpose

Implement the corpus-required regular-expression builtins with Python standard-library facilities.
Support flags, global and non-global matching, UTF-8/codepoint offsets, unnamed and named captures,
regex splitting, substitutions, interpolation, and generator multiplicity.

## Programmatic Acceptance

=== AC builtin-003-test ===
Intent: Regex test supports matching and case-insensitive flags.
import json
import subprocess

source = '["abc","ABC","xyz"]'
program = 'map(test("abc"; "i"))'
result = subprocess.run(["./jq", "-c", program], input=source, text=True, capture_output=True)
assert result.returncode == 0
actual = json.loads(result.stdout)
assert actual == [True, True, False]
=== END AC builtin-003-test ===

=== AC builtin-003-match ===
Intent: Global matching returns match objects with offsets and lengths.
import json
import subprocess

source = '"ab ab"'
program = '[match("ab"; "g") | {offset, length, string}]'
result = subprocess.run(["./jq", "-c", program], input=source, text=True, capture_output=True)
assert result.returncode == 0
actual = json.loads(result.stdout)
assert actual == [
    {"offset": 0, "length": 2, "string": "ab"},
    {"offset": 3, "length": 2, "string": "ab"},
]
=== END AC builtin-003-match ===

=== AC builtin-003-capture ===
Intent: Named captures are returned by capture and scan.
import json
import subprocess

source = '"abc-42"'
program = 'capture("(?<word>[a-z]+)-(?<number>[0-9]+)")'
result = subprocess.run(["./jq", "-c", program], input=source, text=True, capture_output=True)
assert result.returncode == 0
actual = json.loads(result.stdout)
assert actual == {"word": "abc", "number": "42"}
=== END AC builtin-003-capture ===

=== AC builtin-003-substitution ===
Intent: Global substitution replaces every non-overlapping match.
import json
import subprocess

source = '"abcabc"'
program = 'gsub("a"; "X")'
result = subprocess.run(["./jq", "-c", program], input=source, text=True, capture_output=True)
assert result.returncode == 0
actual = json.loads(result.stdout)
assert actual == "XbcXbc"
=== END AC builtin-003-substitution ===

## User Acceptance

- None.

## Guardrails

- Use only Python standard-library regular-expression facilities.
- Preserve stream multiplicity for global match and substitution operations.
- Preserve named and unnamed capture behavior, codepoint offsets, and supported jq flags.
- Do not introduce a third-party regex dependency or shell out to another jq implementation.
