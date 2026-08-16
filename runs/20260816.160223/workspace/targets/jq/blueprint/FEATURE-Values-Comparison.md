# FEATURE: Comparison and Boolean Operators

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Implement jq equality, ordering, boolean logic, and truthiness semantics. |
| Depends On  | FEATURE-Values-Model.md, FEATURE-Eval-Cartesian.md |
| Provides    | equality, ordering, and boolean operators |
| Consumes    | JSON value model, ordered generator evaluator |

## Intent

Comparison operates on jq values without coercion. Equality is structural and type-aware; ordering follows jq's total type ordering and recursively compares arrays and objects. Boolean operators evaluate generator outputs independently, while only `false` and `null` are false in conditional contexts.

## Behaviors

- `==` and `!=` distinguish booleans, numbers, strings, arrays, objects, and null.
- Relational operators use jq's ordering rules.
- `and`, `or`, and `not` return booleans and preserve generator multiplicity.
- False/null truthiness is distinct from Python truthiness.
- NaN and infinities participate in the corpus-defined comparison behavior.

## Programmatic Acceptance

=== AC comparison-equality ===
Intent: The implementation passes the authoritative structural equality and inequality corpus slice.
Suite: scoped

import subprocess
import sys

result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select",
     "==|!=|equality|structural equality"],
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC comparison-equality ===

=== AC comparison-ordering ===
Intent: The implementation passes the authoritative jq ordering and relational comparison corpus slice.
Suite: scoped

import subprocess
import sys

result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select",
     "comparison|ordering| > | < | >= | <= |sort"],
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC comparison-ordering ===

=== AC comparison-boolean ===
Intent: The implementation passes the authoritative boolean, not, and truthiness corpus slice.
Suite: scoped

import subprocess
import sys

result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select",
     " and | or |not|truth|false/null"],
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC comparison-boolean ===

## User Acceptance

- None.

## Guardrails

- Never equate booleans with numeric values.
- Do not use Python truthiness as a substitute for jq truthiness.
- Preserve cartesian ordering when comparison operands generate multiple values.
