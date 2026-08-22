# FEATURE: Builtins Regex

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provides jq regular-expression matching, capture, splitting, and substitution builtins. |
| Depends On  | FEATURE-Builtins-Core.md, FEATURE-Functions-Definitions.md |
| Provides    | test, match, capture, scan, split, splits, sub, gsub |
| Consumes    | user-defined functions, strings, generator evaluator |

## Intent

Implement jq regular-expression builtins using Python's standard-library `re` module and a compatibility translation layer. Support jq flags, named captures, global match streams, regex splitting, substitutions, interpolation-driven replacement filters, and specified runtime errors.

## Programmatic Acceptance

=== AC builtins-regex-matching ===
Intent: The authoritative corpus slice covering test, match, capture, and scan passes.
Suite: scoped

import json
import os
import subprocess
import sys
from pathlib import Path

assert Path("jq").is_file()

selector = r"test\(|match\(|capture\(|scan\("
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

=== END AC builtins-regex-matching ===

=== AC builtins-regex-replacement ===
Intent: The authoritative corpus slice covering regex splitting and substitution passes.
Suite: scoped

import json
import os
import subprocess
import sys
from pathlib import Path

assert Path("jq").is_file()

selector = r"split\(|splits\(|sub\(|gsub\("
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

=== END AC builtins-regex-replacement ===

## User Acceptance

- None.

## Guardrails

- Use only standard-library regular expressions and compatibility translation.
- Preserve UTF-8 codepoint offsets, named-capture behavior, global stream ordering, and runtime error propagation.
