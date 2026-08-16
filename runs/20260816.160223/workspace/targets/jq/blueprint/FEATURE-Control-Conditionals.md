# FEATURE: Conditionals and Alternative Expressions

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Implement jq conditionals, defined-or fallback, and optional expressions. |
| Depends On  | FEATURE-Values-Comparison.md, FEATURE-Eval-Cartesian.md |
| Provides    | if/then/elif/else/end, //, ? |
| Consumes    | ordered generator evaluator, comparison operators |

## Intent

Conditional constructs operate over streams. Each result of a condition selects a branch according to jq truthiness; absent branches use identity. The defined-or operator suppresses false and null values only when no defined left result exists. The optional operator catches errors from its expression and produces no output.

## Behaviors

- `if`, `then`, `elif`, `else`, and `end` support multiple condition outputs.
- An omitted `else` behaves as identity.
- `a // b` evaluates the fallback only when the left stream has no defined value.
- `EXP?` suppresses errors from `EXP` while retaining successful outputs.
- Empty streams and false/null results backtrack according to jq generator semantics.

## Programmatic Acceptance

=== AC conditionals-branches ===
Intent: The implementation passes the authoritative if/then/elif/else/end corpus slice.
Suite: scoped

import subprocess
import sys

result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select",
     "if .* then|elif|else .* end|Possibly unterminated 'if'"],
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC conditionals-branches ===

=== AC conditionals-defined-or ===
Intent: The implementation passes the authoritative defined-or and fallback corpus slice.
Suite: scoped

import subprocess
import sys

result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select",
     "//|defined.or|default|//="],
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC conditionals-defined-or ===

=== AC conditionals-optional ===
Intent: The implementation passes the authoritative optional-expression and empty-stream corpus slice.
Suite: scoped

import subprocess
import sys

result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select",
     r"\?|optional|empty stream|try \.a"],
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC conditionals-optional ===

## User Acceptance

- None.

## Guardrails

- Preserve all successful outputs produced before a later branch error.
- Do not confuse `//` with boolean `or`.
- Optional expressions suppress runtime errors only for the expression carrying `?`.
