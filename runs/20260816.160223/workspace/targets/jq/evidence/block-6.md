# Evidence: Block 6 · Service (block-6)

- block type: block
- date: 2026-08-16
- resulting state: closed/verified
- story points (combined assembled cost): 54414
- execution id: 20260816.163902.220Z-a3b80435

## Stories built
- Implement ordered stream-valued filter evaluation. (eval-stream) [story]

## Reusable compacts
- builtin_compact.md

## Stacked context
- compass: COMPASS.md (SP 3787)
- implements: FEATURE-Eval-Stream.md (SP 762)
- context: jq-manual.txt (SP 32696)
- context: jq.test (SP 13058)
- context: builtin.jq (SP 2408)
- context: ARCHITECTURE_compact.md (SP 126)
- stack: python_compact.md (SP 1534)

## Build directory changes
- jq_evaluator.py
- tests/test_eval_stream.py

## Pre-build acceptance observation
- GREEN (prepassed): eval-stream-fanout (FEATURE-Eval-Stream.md)
  intent: A generator pipeline preserves every upstream value and its order.
  return code: 0
- GREEN (prepassed): eval-stream-pipeline (FEATURE-Eval-Stream.md)
  intent: Downstream filters execute once for each upstream generator output.
  return code: 0
- GREEN (prepassed): eval-stream-empty (FEATURE-Eval-Stream.md)
  intent: The empty filter produces no output while completing successfully.
  return code: 0
- GREEN (prepassed): eval-stream-order (FEATURE-Eval-Stream.md)
  intent: Comma composition preserves left-to-right stream order.
  return code: 0

## Post-build programmatic acceptance
- PASS: eval-stream-fanout (FEATURE-Eval-Stream.md)
  intent: A generator pipeline preserves every upstream value and its order.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: eval-stream-pipeline (FEATURE-Eval-Stream.md)
  intent: Downstream filters execute once for each upstream generator output.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: eval-stream-empty (FEATURE-Eval-Stream.md)
  intent: The empty filter produces no output while completing successfully.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: eval-stream-order (FEATURE-Eval-Stream.md)
  intent: Comma composition preserves left-to-right stream order.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0

## Build summary
<reusable-compact filename="builtin.jq">
Built-in contract surface: generator-aware filters include `map/1`, `select/1`, `sort_by/1`, `group_by/1`, `unique_by/1`, `max_by/1`, `min_by/1`, `add/0|1`, `recurse/0|1|2`, `while/2`, `until/2`, `limit/2`, `skip/2`, `first/0|1`, `last/0`, `nth/1|2`, `all/0|1|2`, `any/0|1|2`, `range/1|2|3`, `reduce`, and `foreach`. These consume and produce ordered jq streams, preserving backtracking and cartesian argument evaluation.

Collection/path interfaces include `map_values/1`, `del/1`, `getpath/1`, `setpath/2`, `delpaths/1`, `path/1`, `paths/0|1`, `pick/1`, `tostream`, `fromstream/1`, and `truncate_stream/1`. `empty` produces no values; `select` retains its input only for truthy results; assignment updates paths immutably.

Type/string/format interfaces include `type`, `length`, `keys`, `has`, `in`, `inside`, `join`, `split`, `splits`, `sub`, `gsub`, `match`, `test`, `capture`, `scan`, trimming/case functions, `tojson`, `fromjson`, `tostring`, and `@text|json|html|uri|urid|csv|tsv|sh|base64|base64d`.

Error/control interfaces include `error`, `try/catch`, `halt`, `halt_error`, labels/breaks, and optional `?`; runtime errors must preserve values emitted before failure. SQL-style interfaces include `INDEX`, `JOIN`, and `IN`.
</reusable-compact>

RESULT: SUCCESS

FILES CHANGED:
- jq_evaluator.py
- tests/test_eval_stream.py

SUMMARY:
Implemented lazy ordered index-key evaluation so earlier stream outputs survive later runtime errors. Added acceptance-aligned stream tests. All 25 project tests pass.

BLOCKERS:
- None
