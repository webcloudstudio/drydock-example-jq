# FEATURE: String and Unicode Builtins

| Field       | Value |
|-------------|-------|
| Version     | 20260821 V1 |
| Description | Provides jq string, Unicode, codepoint, substring, and prefix/suffix builtins. |
| Depends On  | FEATURE-BUILTINS-001.md |
| Provides    | trim, ltrim, rtrim, trimstr, ltrimstr, rtrimstr, split, splits, join, explode, implode, indices, index, rindex, ascii_downcase, ascii_upcase, startswith, endswith |
| Consumes    | core filters, generator utilities |

## Purpose

Implement jq's string and Unicode builtin behavior using standard-library string and Unicode facilities.

## Behavior

- Trimming follows jq's Unicode whitespace semantics.
- Prefix and suffix helpers validate string inputs and remove matching text.
- Splitting and joining preserve empty fields and scalar conversion rules.
- `explode` and `implode` convert between strings and Unicode codepoints, replacing invalid codepoints as jq specifies.
- `indices`, `index`, and `rindex` support strings and arrays, including overlapping string matches.
- ASCII case functions change only ASCII letters.
- String length and offsets are measured in Unicode codepoints.

## Programmatic Acceptance

=== AC builtins-002-strings ===
Intent: The authoritative corpus slice exercising trimming, splitting, joining, and prefix/suffix helpers executes and passes.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

selector = r"split|trim|join|startswith|endswith"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", selector, "--json"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
report = json.loads(result.stdout)
summary = report["summary"]
assert sum(summary.values()) > 0
assert summary["fail"] == 0 and summary["error"] == 0
assert result.returncode == 0
=== END AC builtins-002-strings ===

=== AC builtins-002-unicode ===
Intent: The authoritative corpus slice exercising Unicode codepoints, indices, and ASCII case conversion executes and passes.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

selector = r"explode|implode|indices|index|rindex|ascii_"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", selector, "--json"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
report = json.loads(result.stdout)
summary = report["summary"]
assert sum(summary.values()) > 0
assert summary["fail"] == 0 and summary["error"] == 0
assert result.returncode == 0
=== END AC builtins-002-unicode ===

## User Acceptance

- None.

## Guardrails

- Preserve Unicode codepoint semantics and embedded null characters.
- Do not apply non-ASCII case folding to ASCII-only case functions.
- Preserve empty leading, trailing, and adjacent split fields.
