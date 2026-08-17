# Evidence: Block 2 · Foundational (block-2)

- block type: block
- date: 2026-08-16
- resulting state: closed/verified
- story points (combined assembled cost): 12088
- execution id: 20260817.000917.297Z-aecad35b

## Stories built
- Implement the executable jq entry point and process contract. (cli-foundation) [story]

## Reusable compacts
- full_test_compact.md
- run_conformance_compact.md

## Stacked context
- compass: COMPASS.md (SP 3821)
- implements: FEATURE-CLI-FOUNDATION.md (SP 796)
- context: full_test.sh (SP 189)
- context: run_conformance.py (SP 4354)
- context: ARCHITECTURE_compact.md (SP 147)
- stack: common_compact.md (SP 1179)
- stack: python_compact.md (SP 1534)

## Build directory changes
- README.md
- jq

## Pre-build acceptance observation
- RED: cli-identity (FEATURE-CLI-FOUNDATION.md)
  intent: The executable accepts compact mode, reads JSON stdin, and emits a compact JSON result.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      errno_num = 2
      err_msg = 'No such file or directory'
      err_filename = './jq'
    --- drydock: end values ---
    Traceback (most recent call last):
      File "cli-identity.py", line 7, in <module>
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
- RED: cli-generator-output (FEATURE-CLI-FOUNDATION.md)
  intent: The executable emits one compact line for each generated array element in source order.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      errno_num = 2
      err_msg = 'No such file or directory'
      err_filename = './jq'
    --- drydock: end values ---
    Traceback (most recent call last):
      File "cli-generator-output.py", line 7, in <module>
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
- RED: cli-compile-error (FEATURE-CLI-FOUNDATION.md)
  intent: A syntactically invalid jq program returns the documented compile-error status.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      errno_num = 2
      err_msg = 'No such file or directory'
      err_filename = './jq'
    --- drydock: end values ---
    Traceback (most recent call last):
      File "cli-compile-error.py", line 3, in <module>
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
- RED: cli-runtime-error (FEATURE-CLI-FOUNDATION.md)
  intent: A compiled program that raises at runtime returns the documented runtime-error status.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      errno_num = 2
      err_msg = 'No such file or directory'
      err_filename = './jq'
    --- drydock: end values ---
    Traceback (most recent call last):
      File "cli-runtime-error.py", line 3, in <module>
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
- PASS: cli-identity (FEATURE-CLI-FOUNDATION.md)
  intent: The executable accepts compact mode, reads JSON stdin, and emits a compact JSON result.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
  stdout:
    {"name":"jq","items":[1,2,3]}
- PASS: cli-generator-output (FEATURE-CLI-FOUNDATION.md)
  intent: The executable emits one compact line for each generated array element in source order.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
  stdout:
    3
    1
    4
- PASS: cli-compile-error (FEATURE-CLI-FOUNDATION.md)
  intent: A syntactically invalid jq program returns the documented compile-error status.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
  stdout:
    compile error: 'NoneType' object has no attribute 'startswith'
- PASS: cli-runtime-error (FEATURE-CLI-FOUNDATION.md)
  intent: A compiled program that raises at runtime returns the documented runtime-error status.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
  stdout:
    runtime error: division by zero

## Build summary
<reusable-compact filename="full_test.sh">
Requires executable `./jq`; runs `JQ="$PWD/jq" python3 sources/run_conformance.py` with exit status as verdict. Do not modify scoring behavior.
</reusable-compact>

<reusable-compact filename="run_conformance.py">
Runs each `jq.test` case independently with a 10-second timeout. Requires exit code 3 for compile failures, 0 or 5 for normal/runtime cases, and compares newline-delimited JSON structurally. Harness exits 0 only when all non-skipped cases pass.
</reusable-compact>

RESULT: FAILED

FILES CHANGED:
- jq
- README.md

SUMMARY:
Implemented the executable CLI and documented interface. All 4 declared CLI acceptance checks passed; existing tests passed (3/3). Full conformance did not complete: the interpreter hung on later corpus cases and was stopped.

BLOCKERS:
- Full jq conformance remains incomplete; broader parser/runtime implementation is required.
