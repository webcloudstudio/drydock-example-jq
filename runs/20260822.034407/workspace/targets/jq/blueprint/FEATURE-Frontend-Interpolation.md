# FEATURE: jq String Interpolation

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Interpolated strings and jq format expressions. |
| Depends On  | FEATURE-Frontend-Parser.md, ARCHITECTURE.md |
| Provides    | string interpolation AST, format expressions |
| Consumes    | jq parser, jq AST |

## Capability

Interpolated strings combine literal text with embedded jq filters using `\(expression)`. Escapes are decoded according to jq string rules, and embedded expressions may produce generator values. Format expressions support the `@text`, `@json`, `@html`, `@uri`, `@urid`, `@csv`, `@tsv`, `@sh`, `@base64`, and `@base64d` forms, including format-prefixed interpolated strings.

## Programmatic Acceptance

=== AC interpolation-basic ===
Intent: The executable accepts interpolation syntax and completes successfully.

import os
import subprocess

source = '"The input was \\(.), which is one less than \\(.+1)"'
result = subprocess.run(
    ["./jq", "-c", source],
    input="42\n",
    capture_output=True,
    text=True,
    env={**os.environ},
)
assert result.returncode == 0
=== END AC interpolation-basic ===

=== AC interpolation-formats ===
Intent: The executable accepts format expressions and completes successfully.

import os
import subprocess

source = "@base64"
result = subprocess.run(
    ["./jq", "-c", source],
    input='"This is a message"\n',
    capture_output=True,
    text=True,
    env={**os.environ},
)
assert result.returncode == 0
=== END AC interpolation-formats ===

=== AC interpolation-conformance ===
Intent: Executed conformance cases exercising interpolation and format syntax pass without failures or errors.

import json
import os
import subprocess
import sys
from pathlib import Path

assert Path("jq").is_file()

selector = r"\\\(|@(?:text|json|html|uri|urid|csv|tsv|sh|base64|base64d)"
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
=== END AC interpolation-conformance ===

## User Acceptance

- None.

## Guardrails

- Preserve escaped text exactly as specified by jq.
- Evaluate interpolation expressions in the current filter context.
- Keep format escaping separate from literal text following a format token.
