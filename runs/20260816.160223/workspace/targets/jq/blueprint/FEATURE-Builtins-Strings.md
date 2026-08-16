# FEATURE: Builtins Strings

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Provide jq Unicode-aware string and codepoint builtins. |
| Depends On  | FEATURE-Values-Model.md, FEATURE-Eval-Cartesian.md |
| Provides    | trimming, splitting, joining, case conversion, explode, implode, indices, index, rindex, string predicates |
| Consumes    | jq value model and ordered evaluator |

## Purpose

Implement Unicode-aware string predicates, trimming, splitting, joining, ASCII case conversion, codepoint conversion, substring indices, embedded-NUL handling, and string-specific errors.

## Behavior

- `startswith` and `endswith` require string inputs and return booleans.
- `ltrimstr`, `rtrimstr`, and `trimstr` remove matching prefixes and suffixes without changing other content.
- `trim`, `ltrim`, and `rtrim` recognize jq’s Unicode whitespace set.
- `split`, `join`, `indices`, `index`, and `rindex` preserve empty fields and overlapping-match semantics.
- `explode` returns Unicode codepoints; `implode` replaces invalid codepoints according to jq behavior.
- `ascii_upcase` and `ascii_downcase` affect only ASCII letters.
- Embedded NULs remain ordinary string content.

## Programmatic Acceptance

=== AC builtins-strings-suite ===
Intent: The authoritative corpus passes the string and Unicode-builtin cases owned by this capability.
Suite: scoped

import subprocess

selectors = ["startswith", "endswith", "split", "join", "trim", "ltrim", "rtrim", "explode", "implode", "ascii_upcase", "ascii_downcase", "indices", "index(", "rindex("]
for selector in selectors:
    result = subprocess.run(
        ["python3", "sources/run_conformance.py", "--select", selector],
        capture_output=True,
        text=True,
    )
    print(result.stdout)
    print(result.stderr)
    assert result.returncode == 0
=== END AC builtins-strings-suite ===

=== AC builtins-strings-roundtrip ===
Intent: String splitting and joining preserve supplied ASCII input and codepoint conversion round-trips valid values.
import json
import subprocess

source = "a,b,c"
program = 'split(",") | join(",")'
result = subprocess.run(
    ["./jq", "-c", program],
    input=json.dumps(source) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = json.loads(result.stdout)
assert actual == source

codepoints = [65, 66, 67]
result = subprocess.run(
    ["./jq", "-c", "implode | explode"],
    input=json.dumps(codepoints) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
assert json.loads(result.stdout) == codepoints
=== END AC builtins-strings-roundtrip ===

## User Acceptance

- None.

## Guardrails

- Measure string offsets and lengths in Unicode codepoints as jq specifies.
- Preserve embedded NULs and empty leading, trailing, and repeated split fields.
- Do not use third-party Unicode or regex packages; use Python standard-library facilities only.
