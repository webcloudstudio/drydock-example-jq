# FEATURE: String Manipulation Builtins

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provide jq string trimming, conversion, splitting, joining, and prefix operations. |
| Depends On  | ARCHITECTURE.md, FEATURE-DATA-004.md |
| Provides    | trim, ltrim, rtrim, ltrimstr, rtrimstr, trimstr, ascii_downcase, ascii_upcase, explode, implode, split, join, startswith, endswith |
| Consumes    | jq string values, generator evaluator |

## Workflow

Implement Unicode-aware whitespace trimming, prefix and suffix removal, ASCII-only case conversion, Unicode codepoint conversion, string splitting and joining, and prefix/suffix predicates. Validate input types and preserve jq's stream and error behavior.

## Programmatic Acceptance

=== AC text-001-conformance ===
Intent: The string manipulation slice executes matching corpus cases and passes all selected cases.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

select = r"split|join|trim|ascii_|explode|implode|startswith|endswith"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", select, "--json"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
report = json.loads(result.stdout)
summary = report["summary"]
assert sum(summary.values()) > 0
assert summary["fail"] == 0
assert summary["error"] == 0
assert result.returncode == 0
=== END AC text-001-conformance ===

## User Acceptance

- None.

## Guardrails

- String length and codepoint operations must support Unicode values without treating UTF-8 bytes as individual characters.
- `ascii_downcase` and `ascii_upcase` must affect only ASCII letters.
- Invalid argument types must produce jq runtime errors rather than silent coercions.
