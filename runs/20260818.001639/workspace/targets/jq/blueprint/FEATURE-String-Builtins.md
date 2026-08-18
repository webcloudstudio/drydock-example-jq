# FEATURE: String Builtins

| Field       | Value |
|-------------|-------|
| Version     | 20260818 V1 |
| Description | Provide jq string, Unicode, conversion, interpolation, and indexing builtins. |
| Depends On  | FEATURE-Structural-Builtins.md |
| Provides    | string trimming, splitting, joining, case conversion, indexing, codepoint conversion, interpolation, JSON conversion |
| Consumes    | functions, generator evaluator, JSON serialization |

## Purpose

Implement jq string and Unicode operations with codepoint-correct behavior.

## Behavior

Support `tostring`, `tonumber`, `toboolean`, `tojson`, `fromjson`, `explode`, `implode`, `split`, `join`, `indices`, `index`, `rindex`, `startswith`, `endswith`, `ltrimstr`, `rtrimstr`, `trimstr`, `trim`, `ltrim`, `rtrim`, `ascii_upcase`, `ascii_downcase`, `length`, `utf8bytelength`, and string indexing and interpolation.

Operations must preserve Unicode codepoints, embedded nulls, jq numeric conversion rules, JSON escaping, empty separators, regex-independent string splitting, and specified errors for non-string or invalid inputs.

## Programmatic Acceptance

=== AC string-builtins-suite ===
Intent: The implementation passes the authoritative conformance cases for string and Unicode builtins.
Suite: scoped

import os
import subprocess
import sys

selector = r"(tostring|tonumber|toboolean|tojson|fromjson|explode|implode|split\\(|join\\(|indices\\(|index\\(|rindex\\(|startswith\\(|endswith\\(|ltrimstr|rtrimstr|trim\\b|ascii_upcase|ascii_downcase|utf8bytelength)"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--list", "--select", selector],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC string-builtins-suite ===

=== AC string-unicode ===
Intent: The implementation passes authoritative cases for Unicode codepoints, embedded nulls, trimming, and conversion errors.
Suite: scoped

import os
import subprocess
import sys

selector = r"(explode|implode|trim|ltrim|rtrim|utf8bytelength|\\u0000|fromjson|tonumber|toboolean)"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--list", "--select", selector],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC string-unicode ===

## User Acceptance

- None.

## Guardrails

- Use Unicode codepoint semantics rather than byte or UTF-16 indexing.
- Preserve embedded nulls and valid JSON escape behavior.
- Do not coerce unsupported values where jq specifies a runtime error.
- Preserve numeric literal and arithmetic conversion behavior established by the architecture.
