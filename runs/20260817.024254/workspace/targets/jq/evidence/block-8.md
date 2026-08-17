# Evidence: Block 8 · Service (block-8)

- block type: block
- date: 2026-08-16
- resulting state: closed/verified
- story points (combined assembled cost): 52172
- execution id: 20260817.041240.888Z-83d84521

## Stories built
- Implement the stream-based generator evaluation core. (eval-001) [story]

## Acceptance tooling authorization
- FEATURE-EVAL-001.md#eval-001-streams: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-EVAL-001.md#eval-001-collections: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-EVAL-001.md#eval-001-backtracking: executable=python3; scope=test; authorization=existing Target environment

## Stacked context
- compass: COMPASS.md (SP 3799)
- implements: FEATURE-EVAL-001.md (SP 863)
- context: jq-manual.txt (SP 32696)
- context: jq.test (SP 13058)
- context: ARCHITECTURE_compact.md (SP 162)
- stack: python_compact.md (SP 1534)

## Build directory changes
- jq_interpreter/evaluator.py
- jq_interpreter/parser.py

## Pre-build acceptance observation
- RED: eval-001-streams (FEATURE-EVAL-001.md)
  intent: The implementation passes the authoritative corpus cases for identity, literals, pipes, commas, iteration, and empty.
  return code: 1
  stdout:
    FAIL jq.test:766  output mismatch
        program:  [add(null), add(range(range(10))), add(empty), add(10,range(10))]
        input:    null
        expected: ['[null,120,null,55]']
        actual:   (no output)
        stderr:   can only join an iterable
    FAIL jq.test:1177  program did not compile: unknown function del/1
        program:  del(.), del(empty), del((.foo,.bar,.baz) | .[2,3,0]), del(.foo[0], .bar[0], .foo, .baz.bar[0].x)
        input:    {"foo": [0,1,2,3,4], "bar": [0,1]}
        expected: ['null', '{"foo": [0,1,2,3,4], "bar": [0,1]}', '{"foo": [1,4], "bar": [1]}', '{"bar": [1]}']
        actual:   (no output)
        stderr:   unknown function del/1
    FAIL jq.test:1270  output mismatch
        program:  (.[] | select(. >= 2)) |= empty
        input:    [1,5,3,0,7]
        expected: ['[1,0]']
        actual:   (no output)
        stderr:   invalid update path
    FAIL jq.test:1278  output mismatch
        program:  .foo[1,4,2,3] |= empty
        input:    {"foo":[0,1,2,3,4,5]}
        expected: ['{"foo":[0,5]}']
        actual:   ['{"foo":[0,1,2,3,4,5]}']
    FAIL jq.test:1448  program did not compile: expected end at position 44
        program:  [.[]|try if . == 0 then error("foo") elif . == 1 then .a elif . == 2 then empty else . end catch .]
        input:    [0,1,2,3]
        expected: ['["foo","Cannot index number with string (\\"a\\")",3]']
        actual:   (no output)
        stderr:   expected end at position 44
    FAIL jq.test:2139  program did not compile: unknown function isempty/1
        program:  isempty(empty)
        input:    null
        expected: ['true']
        actual:   (no output)
        stderr:   unknown function isempty/1
    FAIL jq.test:2143  program did not compile: unknown function isempty/1
        program:  isempty(range(3))
        input:    null
        expected: ['false']
        actual:   (no output)
        stderr:   unknown function isempty/1
    FAIL jq.test:2147  program did not compile: unknown function isempty/1
        program:  isempty(1,error("foo"))
        input:    null
        expected: ['false']
        actual:   (no output)
        stderr:   unknown function isempty/1
    FAIL jq.test:2354  output mismatch
        program:  try (["hi","ho"]|.[]|(try . catch (if .=="ho" then "BROKEN"|error else empty end)) | if .=="ho" then error else "\(.) there!" end) catch "caught outside \(.)"
        input:    null
        expected: ['"hi there!"', '"caught outside ho"']
        actual:   ['"hi there!"', '"caught outside error"']
    jq conformance: 4 passed, 9 failed, 0 errored, 0 skipped (corpus jq.test @ jq-1.8.2)
  stderr:
    --- drydock: values at failure ---
      result = CompletedProcess(args=['/mnt/c/Users/barlo/projects/drydock/.venv/bin/python3', 'sources/run_conformance.py', '--select', 'Simple value tests|Field access, piping|Multiple outputs, iteration|empty|Comma|Pipe'], returncode=1, stdout='FAIL jq.test:766  output mismatch\n    program:  [add(null), add(range(range(10))), add(empty), add(10,range(10))]\n    input:    null\n    expected: [\'[null,120,null… (+2353 chars)
    --- drydock: end values ---
    Traceback (most recent call last):
      File "eval-001-streams.py", line 14, in <module>
        assert result.returncode == 0
               ^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- GREEN (prepassed): eval-001-collections (FEATURE-EVAL-001.md)
  intent: The implementation passes the authoritative corpus cases for array and object collection and generator multiplicity.
  return code: 0
  stdout:
    jq conformance: 0 passed, 0 failed, 0 errored, 0 skipped (corpus jq.test @ jq-1.8.2)
- RED: eval-001-backtracking (FEATURE-EVAL-001.md)
  intent: The implementation passes the authoritative corpus cases proving empty and backtracking preserve sibling output order.
  return code: 1
  stdout:
    FAIL jq.test:410  program did not compile: unknown function first/1
        program:  first(1,error("foo"))
        input:    null
        expected: ['1']
        actual:   (no output)
        stderr:   unknown function first/1
    FAIL jq.test:766  output mismatch
        program:  [add(null), add(range(range(10))), add(empty), add(10,range(10))]
        input:    null
        expected: ['[null,120,null,55]']
        actual:   (no output)
        stderr:   can only join an iterable
    FAIL jq.test:1177  program did not compile: unknown function del/1
        program:  del(.), del(empty), del((.foo,.bar,.baz) | .[2,3,0]), del(.foo[0], .bar[0], .foo, .baz.bar[0].x)
        input:    {"foo": [0,1,2,3,4], "bar": [0,1]}
        expected: ['null', '{"foo": [0,1,2,3,4], "bar": [0,1]}', '{"foo": [1,4], "bar": [1]}', '{"bar": [1]}']
        actual:   (no output)
        stderr:   unknown function del/1
    FAIL jq.test:1270  output mismatch
        program:  (.[] | select(. >= 2)) |= empty
        input:    [1,5,3,0,7]
        expected: ['[1,0]']
        actual:   (no output)
        stderr:   invalid update path
    FAIL jq.test:1278  output mismatch
        program:  .foo[1,4,2,3] |= empty
        input:    {"foo":[0,1,2,3,4,5]}
        expected: ['{"foo":[0,5]}']
        actual:   ['{"foo":[0,1,2,3,4,5]}']
    FAIL jq.test:1448  program did not compile: expected end at position 44
        program:  [.[]|try if . == 0 then error("foo") elif . == 1 then .a elif . == 2 then empty else . end catch .]
        input:    [0,1,2,3]
        expected: ['["foo","Cannot index number with string (\\"a\\")",3]']
        actual:   (no output)
        stderr:   expected end at position 44
    FAIL jq.test:2139  program did not compile: unknown function isempty/1
        program:  isempty(empty)
        input:    null
        expected: ['true']
        actual:   (no output)
        stderr:   unknown function isempty/1
    FAIL jq.test:2143  program did not compile: unknown function isempty/1
        program:  isempty(range(3))
        input:    null
        expected: ['false']
        actual:   (no output)
        stderr:   unknown function isempty/1
    FAIL jq.test:2147  program did not compile: unknown function isempty/1
        program:  isempty(1,error("foo"))
        input:    null
        expected: ['false']
        actual:   (no output)
        stderr:   unknown function isempty/1
    FAIL jq.test:2354  output mismatch
        program:  try (["hi","ho"]|.[]|(try . catch (if .=="ho" then "BROKEN"|error else empty end)) | if .=="ho" then error else "\(.) there!" end) catch "caught outside \(.)"
        input:    null
        expected: ['"hi there!"', '"caught outside ho"']
        actual:   ['"hi there!"', '"caught outside error"']
    jq conformance: 4 passed, 10 failed, 0 errored, 0 skipped (corpus jq.test @ jq-1.8.2)
  stderr:
    --- drydock: values at failure ---
      result = CompletedProcess(args=['/mnt/c/Users/barlo/projects/drydock/.venv/bin/python3', 'sources/run_conformance.py', '--select', 'empty|backtracking|first\\(1,error|cartesian'], returncode=1, stdout='FAIL jq.test:410  program did not compile: unknown function first/1\n    program:  first(1,error("foo"))\n    input:    null\n    expected: [\'1\']\n    actual:   (no output)\n    stderr:   unknown function … (+2530 chars)
    --- drydock: end values ---
    Traceback (most recent call last):
      File "eval-001-backtracking.py", line 14, in <module>
        assert result.returncode == 0
               ^^^^^^^^^^^^^^^^^^^^^^
    AssertionError

## Post-build programmatic acceptance
- PASS: eval-001-streams (FEATURE-EVAL-001.md)
  intent: The implementation passes the authoritative corpus cases for identity, literals, pipes, commas, iteration, and empty.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
  stdout:
    jq conformance: 13 passed, 0 failed, 0 errored, 0 skipped (corpus jq.test @ jq-1.8.2)
- PASS: eval-001-collections (FEATURE-EVAL-001.md)
  intent: The implementation passes the authoritative corpus cases for array and object collection and generator multiplicity.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
  stdout:
    jq conformance: 0 passed, 0 failed, 0 errored, 0 skipped (corpus jq.test @ jq-1.8.2)
- PASS: eval-001-backtracking (FEATURE-EVAL-001.md)
  intent: The implementation passes the authoritative corpus cases proving empty and backtracking preserve sibling output order.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
  stdout:
    jq conformance: 14 passed, 0 failed, 0 errored, 0 skipped (corpus jq.test @ jq-1.8.2)

## Repair attempts
- attempt 0 (initial build): failed; 1/3 checks; 23/27 cases model=gpt-5.6-luna; execution 20260817.040106.376Z-fe978ce7
- attempt 1 (repair 1): failed; 3/3 checks; 27/27 cases model=gpt-5.6-luna; execution 20260817.040726.124Z-4690c0af
- attempt 2 (repair 2): built; 3/3 checks; 27/27 cases model=gpt-5.6-luna; execution 20260817.041240.888Z-83d84521

## Build summary
RESULT: SUCCESS

FILES CHANGED:
- jq_interpreter/evaluator.py

SUMMARY:
Fixed generator-core path evaluation, null-root `setpath`, invalid path validation, and deep-path guards. Declared acceptance selectors pass; local tests: 25 passed.

BLOCKERS:
- Full corpus still has pre-existing failures outside this block: 287 passed, 250 failed, 0 errored, 13 skipped.
