# FEATURE: Composition and Cartesian Evaluation

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Implement jq composition, Cartesian argument evaluation, collection, object construction, and binary filter composition. |
| Depends On  | FEATURE-Generator-Core.md, FEATURE-Filter-Grammar.md |
| Provides    | Pipes, commas, Cartesian arguments, arrays, objects, and binary filter composition |
| Consumes    | Generator core, parsed expressions, JSON value model |

## Scope

Composition shall feed every output of a left-hand filter into the right-hand filter, concatenate comma streams in order, evaluate multi-output arguments as Cartesian products, and collect all generated values for arrays and objects. Binary operators shall receive independently evaluated filter results according to jq semantics.

## Programmatic Acceptance

=== AC composition-conformance ===
Intent: The composition implementation passes representative declared pipe, comma, array, and object behaviors.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess

jq = os.path.join(os.getcwd(), "jq")

piped = subprocess.run(
    [jq, "-c", ".[] | . * 2"],
    input="[1,2]",
    capture_output=True,
    text=True,
)
assert piped.returncode == 0
assert [json.loads(line) for line in piped.stdout.splitlines()] == [2, 4]

constructed = subprocess.run(
    [jq, "-c", "[1,2]"],
    capture_output=True,
    text=True,
)
assert constructed.returncode == 0
assert json.loads(constructed.stdout) == [1, 2]

=== END AC composition-conformance ===

=== AC composition-cartesian-streams ===
Intent: The composition implementation preserves comma stream ordering and Cartesian products.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess

jq = os.path.join(os.getcwd(), "jq")

streams = subprocess.run(
    [jq, "-c", "1,2,3"],
    capture_output=True,
    text=True,
)
assert streams.returncode == 0
assert [json.loads(line) for line in streams.stdout.splitlines()] == [1, 2, 3]

cartesian = subprocess.run(
    [jq, "-c", "[1,2] as $a | [3,4] as $b | [$a,$b]"],
    capture_output=True,
    text=True,
)
assert cartesian.returncode == 0
assert json.loads(cartesian.stdout) == [[1, 3], [1, 4], [2, 3], [2, 4]]

=== END AC composition-cartesian-streams ===

## User Acceptance

- None.

## Guardrails

- Preserve left-to-right generator ordering.
- Evaluate every multi-output argument combination required by jq.
- Array and object construction must collect generated values without dropping or duplicating outputs.
