# FEATURE: Focused Verification

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Provide bounded diagnostic verification across the completed jq implementation areas. |
| Depends On  | FEATURE-Executable.md |
| Provides    | bounded implementation verification |
| Consumes    | ./jq executable, supplied conformance runner |

## Purpose

Add focused, bounded verification for representative implementation areas using the supplied conformance harness selectors. This story is diagnostic only and must not replace or duplicate the terminal full-conformance gate.

## Verification Scope

The focused checks cover representative lexer/parser, generator, core-value, operator, control-flow, function, builtin, and executable behavior. Each invocation must use a bounded selector and must not modify the imported corpus, exclusions, or runner.

## Programmatic Acceptance

=== AC focused-lexer-parser ===
Intent: The executable passes bounded lexer and parser conformance selections.

import os
import subprocess

result = subprocess.run(
    ["python3", "sources/run_conformance.py", "--select", r"interpolation|object|field"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": "./jq"},
)
print(result.stdout)
print(result.stderr)
assert result.returncode == 0
=== END AC focused-lexer-parser ===

=== AC focused-runtime-builtins ===
Intent: The executable passes bounded runtime and builtin conformance selections.

import os
import subprocess

result = subprocess.run(
    ["python3", "sources/run_conformance.py", "--select", r"reduce|range|sort|match|tojson"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": "./jq"},
)
print(result.stdout)
print(result.stderr)
assert result.returncode == 0
=== END AC focused-runtime-builtins ===

=== AC focused-assets-unchanged ===
Intent: The focused verification command completes using the supplied harness and candidate executable.

import os
import subprocess

result = subprocess.run(
    ["python3", "sources/run_conformance.py", "--select", r"^\\.$"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": "./jq"},
)
print(result.stdout)
print(result.stderr)
assert result.returncode == 0
=== END AC focused-assets-unchanged ===

## User Acceptance

- None.

## Guardrails

- Never invoke the full corpus from this story.
- Never edit, filter, skip, or reinterpret supplied scoring assets.
- The terminal full-conformance story remains the sole release gate.
