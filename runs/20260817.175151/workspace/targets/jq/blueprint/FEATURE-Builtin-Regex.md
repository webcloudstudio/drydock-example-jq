# FEATURE: Builtin Regex

| Field       | Value |
|-------------|-------|
| Version     | 20260817 V1 |
| Description | Provides jq regular-expression matching, capture, scanning, splitting, and replacement builtins. |
| Depends On  | FEATURE-Builtin-Strings.md |
| Provides    | test, match, capture, scan, split, splits, sub, gsub |
| Consumes    | jq string builtins |

## Behavior

The interpreter implements jq regex builtins using Python standard-library facilities. It supports jq flags, named and unnamed captures, Unicode offsets, stream-producing matches and splits, and substitution interpolation. Invalid input types and invalid patterns raise jq runtime errors.

## Programmatic Acceptance

=== AC regex-test ===
Intent: The test builtin returns the supplied match predicate.
import json
import subprocess
import os

source = "abracadabra"
pattern = "bra"
expected = True
result = subprocess.run(
    ["./jq", "-c", 'test("bra")'],
    input=json.dumps(source) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
assert json.loads(result.stdout) == expected
=== END AC regex-test ===

=== AC regex-match-stream ===
Intent: The match builtin emits all requested global matches.
import json
import subprocess

source = "abcabc"
expected = ["abc", "abc"]
result = subprocess.run(
    ["./jq", "-c", '[match("abc"; "g") | .string]'],
    input=json.dumps(source) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
assert json.loads(result.stdout) == expected
=== END AC regex-match-stream ===

=== AC regex-capture ===
Intent: Named captures are exposed by capture.
import json
import subprocess

source = "item-42"
expected = {"name": "item", "number": "42"}
result = subprocess.run(
    ["./jq", "-c", 'capture("(?<name>[a-z]+)-(?<number>[0-9]+)")'],
    input=json.dumps(source) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
assert json.loads(result.stdout) == expected
=== END AC regex-capture ===

=== AC regex-substitution ===
Intent: Global substitution replaces every matching occurrence.
import json
import subprocess

source = "a-b-c"
expected = "a_b_c"
result = subprocess.run(
    ["./jq", "-c", 'gsub("-"; "_")'],
    input=json.dumps(source) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
assert json.loads(result.stdout) == expected
=== END AC regex-substitution ===

## User Acceptance

- None.

## Guardrails

- Regex support uses only Python standard-library facilities and does not add a runtime dependency.
