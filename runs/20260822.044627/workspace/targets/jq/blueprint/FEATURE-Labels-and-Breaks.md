# FEATURE: Labels and Breaks

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Define lexically scoped jq labels and break expressions for terminating generators. |
| Depends On  | FEATURE-Conditionals-and-Exceptions.md |
| Provides    | label and break |
| Consumes    | conditionals and exception flow, ordered generator evaluation |

## Intent

This capability implements lexical control transfer from `break $label` to its matching visible `label $label`.

## Behavior

- `label $name | EXP` establishes a lexical break target.
- `break $name` terminates the nearest matching labeled generator and produces no further values from it.
- Breaks do not escape their lexical label or affect unrelated generators.
- A break without a visible matching label is rejected at compile time with exit status 3.
- Labels preserve output ordering for values produced before the break.

## Programmatic Acceptance

=== AC flow-004-conformance ===
Intent: Labels terminate generators at their matching break and invalid labels fail at compile time.

import subprocess

result = subprocess.run(
    ["./jq", "-c", "label $out | (1, 2, break $out, 3)"],
    input="null\n",
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr, file=__import__("sys").stderr)
assert result.returncode == 0
assert result.stdout.splitlines() == ["1", "2"]

invalid = subprocess.run(
    ["./jq", "-c", "break $missing"],
    input="null\n",
    capture_output=True,
    text=True,
)
assert invalid.returncode == 3
=== END AC flow-004-conformance ===

## User Acceptance

- None.

## Guardrails

- Break targets are lexical, not dynamically searched.
- A break must not leak values after its matching label terminates.
- Invalid labels must be compile failures, never runtime failures.
