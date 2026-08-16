# FEATURE: Language Alternation

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Provides jq destructuring alternatives with null bindings and error fallback. |
| Depends On  | ARCHITECTURE.md, FEATURE-Language-Bindings.md, FEATURE-Control-Errors.md |
| Provides    | ?// destructuring alternative |
| Consumes    | lexical bindings, runtime error handling |

## Purpose

Implement the `?//` destructuring alternative operator, including pattern selection, shared variable visibility, null exposure for variables absent from the selected pattern, and fallback after downstream errors.

## Behavior

- Alternatives are attempted in order.
- The first pattern that successfully destructures the input supplies the downstream bindings.
- Variables declared only by another alternative are visible as null.
- Errors during downstream evaluation cause the next alternative to be attempted when defined by jq semantics.
- The final alternative propagates its runtime error.

## Programmatic Acceptance

=== AC alternation-shapes ===
Intent: Destructuring alternatives select the matching object or array shape and expose shared bindings.

import json
import subprocess

source = [{"a": 1, "b": 2, "c": {"d": 3}}, [4, {"b": 5, "c": 6}, 7]]
program = ".[] as {$a, b: [$c, {$d}]} ?// [$a, {$b}, $e] | [$a, $b, $c, $d, $e]"
result = subprocess.run(["./jq", "-c", program], input=json.dumps(source) + "\n", capture_output=True, text=True)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
assert actual == [[1, None, 2, 3, None], [4, 5, None, None, 7]]
=== END AC alternation-shapes ===

=== AC alternation-null-bindings ===
Intent: Variables declared only by the unsuccessful alternative are available as null.

import json
import subprocess

source = [[3]]
program = ".[] as [$a] ?// [$b] | {$a, $b}"
result = subprocess.run(["./jq", "-c", program], input=json.dumps(source) + "\n", capture_output=True, text=True)
assert result.returncode == 0
assert [json.loads(line) for line in result.stdout.splitlines()] == [{"a": None, "b": 3}]
=== END AC alternation-null-bindings ===

=== AC alternation-runtime-fallback ===
Intent: A downstream error in an earlier pattern can select a later successful pattern.

import json
import subprocess

source = [[3]]
program = ".[] as [$a] ?// [$b] | if $a != null then error(\"err\") else {$a, $b} end"
result = subprocess.run(["./jq", "-c", program], input=json.dumps(source) + "\n", capture_output=True, text=True)
assert result.returncode == 0
assert [json.loads(line) for line in result.stdout.splitlines()] == [{"a": None, "b": 3}]
=== END AC alternation-runtime-fallback ===

## User Acceptance

- None.

## Guardrails

- Do not treat a merely absent optional field as a failed alternative when jq binds it as null.
- Preserve the final alternative's runtime errors.
- Keep alternative bindings lexically scoped to the downstream expression.
