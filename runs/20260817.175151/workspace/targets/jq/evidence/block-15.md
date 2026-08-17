# Evidence: Block 15 · Service (block-15)

- block type: block
- date: 2026-08-17
- resulting state: closed/failed
- story points (combined assembled cost): 50049
- execution id: 20260817.184955.880Z-e006efbf

## Stories built
- Discover, access, and materialize jq paths. (path-discovery) [story]

## Stacked context
- compass: COMPASS.md (SP 2068)
- implements: FEATURE-Path-Discovery.md (SP 655)
- context: jq-manual.txt (SP 32696)
- context: jq.test (SP 13058)
- stack: python_compact.md (SP 1534)

## Build directory changes
- jq
- tests/test_path_discovery.py

## Pre-build acceptance observation
- RED: path-exact-and-read (FEATURE-Path-Discovery.md)
  intent: Exact paths can be materialized and read through the executable.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      result = CompletedProcess(args=['/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260817.175151/build/jq/jq', '-c', '[path(.a[0].b), getpath(["a", 0, "b"])]'], returncode=3, stdout='', stderr='jq: unknown function path/1\n')
    --- drydock: end values ---
    Traceback (most recent call last):
      File "path-exact-and-read.py", line 14, in <module>
        assert result.returncode == 0
               ^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: paths-recursive (FEATURE-Path-Discovery.md)
  intent: Recursive path discovery reports non-root paths in traversal order.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      result = CompletedProcess(args=['/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260817.175151/build/jq/jq', '-c', '[paths]'], returncode=3, stdout='', stderr='jq: unknown function paths\n')
    --- drydock: end values ---
    Traceback (most recent call last):
      File "paths-recursive.py", line 12, in <module>
        assert result.returncode == 0
               ^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- UNVERIFIED: path-filter (FEATURE-Path-Discovery.md)
  intent: Filtered paths select only locations whose values satisfy the filter.
  return code: 1
  error: malformed check: the assertion itself raised NameError (name 'os' is not defined. Did you forget to import 'os') in its own frame, before reaching the code under test. No implementation can satisfy it. Each check runs as its own script in its own process, so a name bound by another check is not in scope. Repair the assertion in the Blueprint specification.
  stderr:
    --- drydock: values at failure ---
      program = '[paths(type == "number")]'
      payload = {'a': [1, 'x', 3]}
    --- drydock: end values ---
    Traceback (most recent call last):
      File "path-filter.py", line 6, in <module>
        [os.path.join(os.getcwd(), "jq"), "-c", program],
         ^^
    NameError: name 'os' is not defined. Did you forget to import 'os'

## Post-build programmatic acceptance
- FAIL: path-exact-and-read (FEATURE-Path-Discovery.md)
  intent: Exact paths can be materialized and read through the executable.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 1
  stderr:
    --- drydock: values at failure ---
      actual = [['a', 0, 'b'], 7]
      payload = {'a': [{'b': 7}]}
    --- drydock: end values ---
    Traceback (most recent call last):
      File "path-exact-and-read.py", line 16, in <module>
        assert actual[0][-1] == payload["a"][0]["b"]
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- PASS: paths-recursive (FEATURE-Path-Discovery.md)
  intent: Recursive path discovery reports non-root paths in traversal order.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- UNVERIFIED: path-filter (FEATURE-Path-Discovery.md)
  intent: Filtered paths select only locations whose values satisfy the filter.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 1
  error: malformed check: the assertion itself raised NameError (name 'os' is not defined. Did you forget to import 'os') in its own frame, before reaching the code under test. No implementation can satisfy it. Each check runs as its own script in its own process, so a name bound by another check is not in scope. Repair the assertion in the Blueprint specification.
  stderr:
    --- drydock: values at failure ---
      program = '[paths(type == "number")]'
      payload = {'a': [1, 'x', 3]}
    --- drydock: end values ---
    Traceback (most recent call last):
      File "path-filter.py", line 6, in <module>
        [os.path.join(os.getcwd(), "jq"), "-c", program],
         ^^
    NameError: name 'os' is not defined. Did you forget to import 'os'

## Repair attempts
- attempt 0 (initial build): failed; 1/3 checks model=gpt-5.6-luna; execution 20260817.184458.672Z-d70acbe1
- attempt 1 (repair 1): failed; 1/3 checks model=gpt-5.6-luna; execution 20260817.184851.802Z-cd68626e
- attempt 2 (repair 2): failed; 1/3 checks model=gpt-5.6-luna; execution 20260817.184955.880Z-e006efbf; stopped: deterministic acceptance score did not improve on 2 consecutive calls

## Failure
- summary: programmatic acceptance failed: path-exact-and-read
- detail:
    Block "Block 15 · Service" [block-15] failed its acceptance criteria.
      Story "Discover, access, and materialize jq paths." [path-discovery] does not meet its own acceptance criteria:
        - AC path-exact-and-read — Exact paths can be materialized and read through the executable.
            assertion: assert actual[0][-1] == payload["a"][0]["b"] → AssertionError
            raised at: path-exact-and-read.py:16
            process exit code: 1
            values at failure:
              actual = [['a', 0, 'b'], 7]
              payload = {'a': [{'b': 7}]}
            check stderr:
              Traceback (most recent call last):
                File "path-exact-and-read.py", line 16, in <module>
                  assert actual[0][-1] == payload["a"][0]["b"]
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
              AssertionError

## Build summary
AC_BROKEN: path-exact-and-read, path-filter

RESULT: FAILED

FILES CHANGED:
- None

SUMMARY:
Existing path implementation passes all 76 project tests. The exact-path AC contradicts jq semantics: output is `[["a",0,"b"],7]`, so `actual[0][-1]` is `"b"`. The path-filter AC fails before execution because it omits `import os`; corrected behavior passes.

BLOCKERS:
- Acceptance criteria require Blueprint repair; no code change is appropriate.
