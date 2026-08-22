# FEATURE: String Manipulation

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provide jq string trimming, case, codepoint, splitting, joining, and interpolation behavior. |
| Depends On  | FEATURE-Type-And-Numeric-Primitives.md, FEATURE-Literals-And-Interpolation.md, FEATURE-Composition-And-Cartesian-Evaluation.md |
| Provides    | trim, ltrim, rtrim, ltrimstr, rtrimstr, trimstr, startswith, endswith, ascii_downcase, ascii_upcase, explode, implode, split, join, string interpolation |
| Consumes    | string values, generator evaluator |

## Workflow

Implement Unicode-aware whitespace trimming, prefix and suffix removal, ASCII-only case conversion, codepoint conversion, string splitting and joining, and interpolation over generator-valued expressions. Follow jq's distinctions between codepoints and UTF-8 byte lengths and its handling of null, booleans, and numbers in joins.

## Programmatic Acceptance

=== AC text-001-conformance ===
Intent: The authoritative corpus slice covering string manipulation and interpolation executes and passes.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

selector = r"split|join|trim|ascii_|explode|implode|startswith|endswith"
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
assert summary["fail"] == 0
assert summary["error"] == 0
assert result.returncode == 0
=== END AC text-001-conformance ===

## User Acceptance

- None.

## Guardrails

- Preserve Unicode codepoints and embedded control characters.
- `ascii_downcase` and `ascii_upcase` affect only ASCII letters.
- String operations must reject invalid input with runtime errors rather than silently coercing it.
