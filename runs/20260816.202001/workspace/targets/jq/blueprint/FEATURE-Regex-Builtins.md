# FEATURE: String and Regular-Expression Builtins

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Defines jq string utilities and regular-expression matching and substitution builtins. |
| Depends On  | FEATURE-Formats.md, FEATURE-Functions-Bindings.md, FEATURE-Core-Values.md |
| Provides    | string trimming, splitting, joining, case conversion, indices, match, test, scan, capture, sub, gsub |
| Consumes    | string values and interpolation |

## Intent

This feature implements jq's string and regular-expression library using Python standard-library
facilities. It preserves Unicode codepoint offsets, named captures, generator behavior, supported
flags, and jq's distinction between string and non-string inputs.

## Behavior

- `startswith`, `endswith`, `ltrimstr`, `rtrimstr`, `trimstr`, `trim`, `ltrim`, and `rtrim`
  validate string inputs and preserve Unicode behavior.
- `split`, `splits`, and `join` preserve empty fields and jq conversions for numbers, booleans,
  and nulls.
- `indices`, `index`, and `rindex` operate on strings and arrays.
- `match`, `test`, `capture`, and `scan` support supported flags, global matching, named captures,
  offsets, and lengths.
- `sub` replaces the first matching occurrence; `gsub` replaces all non-overlapping occurrences.
- `ascii_downcase`, `ascii_upcase`, `explode`, and `implode` follow jq codepoint rules.
- Invalid input types and invalid regular expressions raise runtime errors.

## Programmatic Acceptance

=== AC regex-builtins-suite ===
Intent: The supplied conformance corpus passes the string and regular-expression cases owned by this feature.
Suite: scoped

import subprocess
import os

pattern = r"startswith|endswith|ltrimstr|rtrimstr|trimstr|trim,|split|splits|join|indices|index\\(|rindex|match|test|capture|scan|sub\\(|gsub|ascii_|explode|implode"
result = subprocess.run(
    ["python3", "sources/run_conformance.py", "--select", pattern],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": "./jq"},
)
print(result.stdout)
print(result.stderr, file=__import__("sys").stderr)
assert result.returncode == 0
=== END AC regex-builtins-suite ===

=== AC string-transformations ===
Intent: String splitting, joining, trimming, and case conversion preserve supplied input semantics.
import subprocess
import json

program = "[split(\",\"), join(\"-\"), trim, ascii_upcase]"
input_value = "[\"a,b\",\"c\"]\n"
result = subprocess.run(["./jq", "-c", program], input=input_value, capture_output=True, text=True)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
expected = [["a", "b"], "a-b", "[\"a,b\",\"c\"]", "[\"A\",\"B\"]"]
assert actual == expected
=== END AC string-transformations ===

=== AC regex-match-capture ===
Intent: Matching and named capture extraction produce structured match data.
import subprocess
import json

program = "[match(\"(?<word>[a-z]+)-(?<n>[0-9]+)\"), capture(\"(?<word>[a-z]+)-(?<n>[0-9]+)\")]"
input_value = "\"abc-12\"\n"
result = subprocess.run(["./jq", "-c", program], input=input_value, capture_output=True, text=True)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
assert len(actual) == 1
assert actual[0][0]["string"] == "abc-12"
assert actual[0][1] == {"word": "abc", "n": "12"}
=== END AC regex-match-capture ===

=== AC regex-invalid-input ===
Intent: Applying a string builtin to a non-string input produces the documented runtime exit status.
import subprocess

result = subprocess.run(
    ["./jq", "-c", "startswith(\"x\")"],
    input="1\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 5
=== END AC regex-invalid-input ===

## User Acceptance

- None.

## Guardrails

- Keep offsets and lengths in Unicode codepoints as jq specifies.
- Do not use a third-party regular-expression package.
- Do not turn a regex error or invalid input into a successful empty stream.
