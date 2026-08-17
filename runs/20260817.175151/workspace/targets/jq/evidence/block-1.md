# Evidence: Block 1 · Foundational (block-1)

- block type: block
- date: 2026-08-17
- resulting state: closed/verified
- story points (combined assembled cost): 8309
- execution id: 20260817.180903.592Z-d244721a

## Stories built
- Provide the executable jq command-line entrypoint. (cli-entrypoint) [story]

## Stacked context
- compass: COMPASS.md (SP 2068)
- implements: FEATURE-CLI-Entrypoint.md (SP 480)
- stack: python.md (SP 3892)
- stack: common.md (SP 1807)

## Build directory changes
- jq
- jq.py
- tests/test_cli.py

## Pre-build acceptance observation
- RED: cli-entrypoint-roundtrip (FEATURE-CLI-Entrypoint.md)
  intent: The executable reads stdin JSON and emits the same JSON value through the identity filter.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      errno_num = 2
      err_msg = 'No such file or directory'
      err_filename = './jq'
    --- drydock: end values ---
    Traceback (most recent call last):
      File "cli-entrypoint-roundtrip.py", line 7, in <module>
        result = subprocess.run(
                 ^^^^^^^^^^^^^^^
      File "/home/barlo/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/subprocess.py", line 548, in run
        with Popen(*popenargs, **kwargs) as process:
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/home/barlo/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/subprocess.py", line 1026, in __init__
        self._execute_child(args, executable, preexec_fn, close_fds,
      File "/home/barlo/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/subprocess.py", line 1955, in _execute_child
        raise child_exception_type(errno_num, err_msg, err_filename)
    FileNotFoundError: [Errno 2] No such file or directory: './jq'
- RED: cli-entrypoint-stream (FEATURE-CLI-Entrypoint.md)
  intent: The executable emits one output line for each input JSON value.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      errno_num = 2
      err_msg = 'No such file or directory'
      err_filename = './jq'
    --- drydock: end values ---
    Traceback (most recent call last):
      File "cli-entrypoint-stream.py", line 6, in <module>
        result = subprocess.run(
                 ^^^^^^^^^^^^^^^
      File "/home/barlo/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/subprocess.py", line 548, in run
        with Popen(*popenargs, **kwargs) as process:
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/home/barlo/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/subprocess.py", line 1026, in __init__
        self._execute_child(args, executable, preexec_fn, close_fds,
      File "/home/barlo/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/subprocess.py", line 1955, in _execute_child
        raise child_exception_type(errno_num, err_msg, err_filename)
    FileNotFoundError: [Errno 2] No such file or directory: './jq'

## Post-build programmatic acceptance
- PASS: cli-entrypoint-roundtrip (FEATURE-CLI-Entrypoint.md)
  intent: The executable reads stdin JSON and emits the same JSON value through the identity filter.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: cli-entrypoint-stream (FEATURE-CLI-Entrypoint.md)
  intent: The executable emits one output line for each input JSON value.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0

## Build summary
Implemented the executable jq entrypoint and tests.

RESULT: SUCCESS

FILES CHANGED:
- jq
- jq.py
- tests/test_cli.py

SUMMARY:
Identity filter works for streamed JSON input. Acceptance checks passed; compile/runtime exit codes are `3`/`5`.

BLOCKERS:
- None
