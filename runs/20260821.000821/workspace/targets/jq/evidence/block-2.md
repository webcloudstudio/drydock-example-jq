# Evidence: Block 2 · Foundational (block-2)

- block type: block
- date: 2026-08-20
- resulting state: closed/verified
- story points (combined assembled cost): 11905
- execution id: 20260821.002612.570Z-33b38a10

## Stories built
- Implement the executable jq command-line contract. (FOUNDATION-002) [story]
- Document the jq project interface and verification command. (FOUNDATION-003) [story]

## Reusable compacts
- run_conformance_compact.md
- full_test_compact.md

## Stacked context
- compass: COMPASS.md (SP 3420)
- implements: FEATURE-FOUNDATION-002.md (SP 672)
- context: run_conformance.py (SP 4354)
- context: full_test.sh (SP 189)
- stack: common_compact.md (SP 1179)
- stack: python_compact.md (SP 1534)
- implements: FEATURE-FOUNDATION-003.md (SP 445)

## Build directory changes
- README.md
- jq
- tests/test_cli_contract.py

## Pre-build acceptance observation
- RED: cli-round-trip (FEATURE-FOUNDATION-002.md)
  intent: The executable accepts the exercised -c form and emits each supplied JSON value as compact JSON.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      errno_num = 2
      err_msg = 'No such file or directory'
      err_filename = './jq'
    --- drydock: end values ---
    Traceback (most recent call last):
      File "cli-round-trip.py", line 8, in <module>
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
- RED: cli-compile-status (FEATURE-FOUNDATION-002.md)
  intent: A syntactically invalid jq program returns the documented compile-failure status.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      errno_num = 2
      err_msg = 'No such file or directory'
      err_filename = './jq'
    --- drydock: end values ---
    Traceback (most recent call last):
      File "cli-compile-status.py", line 4, in <module>
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
- RED: cli-runtime-status (FEATURE-FOUNDATION-002.md)
  intent: A runtime error returns status 5 after preserving values emitted before the error.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      errno_num = 2
      err_msg = 'No such file or directory'
      err_filename = './jq'
    --- drydock: end values ---
    Traceback (most recent call last):
      File "cli-runtime-status.py", line 6, in <module>
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
- RED: readme-interface (FEATURE-FOUNDATION-003.md)
  intent: README.md records the complete executable interface contract.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      self = PosixPath('README.md')
      mode = 'r'
      buffering = -1
      encoding = 'utf-8'
      errors = None
      newline = None
    --- drydock: end values ---
    Traceback (most recent call last):
      File "readme-interface.py", line 3, in <module>
        readme = Path("README.md").read_text(encoding="utf-8")
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/home/barlo/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/pathlib.py", line 1027, in read_text
        with self.open(mode='r', encoding=encoding, errors=errors) as f:
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/home/barlo/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/pathlib.py", line 1013, in open
        return io.open(self, mode, buffering, encoding, errors, newline)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    FileNotFoundError: [Errno 2] No such file or directory: 'README.md'
- RED: readme-verification-command (FEATURE-FOUNDATION-003.md)
  intent: README.md identifies the supplied conformance command as the project verification entry point.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      self = PosixPath('README.md')
      mode = 'r'
      buffering = -1
      encoding = 'utf-8'
      errors = None
      newline = None
    --- drydock: end values ---
    Traceback (most recent call last):
      File "readme-verification-command.py", line 3, in <module>
        readme = Path("README.md").read_text(encoding="utf-8")
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/home/barlo/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/pathlib.py", line 1027, in read_text
        with self.open(mode='r', encoding=encoding, errors=errors) as f:
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/home/barlo/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/pathlib.py", line 1013, in open
        return io.open(self, mode, buffering, encoding, errors, newline)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    FileNotFoundError: [Errno 2] No such file or directory: 'README.md'

## Post-build programmatic acceptance
- PASS: cli-round-trip (FEATURE-FOUNDATION-002.md)
  intent: The executable accepts the exercised -c form and emits each supplied JSON value as compact JSON.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: cli-compile-status (FEATURE-FOUNDATION-002.md)
  intent: A syntactically invalid jq program returns the documented compile-failure status.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: cli-runtime-status (FEATURE-FOUNDATION-002.md)
  intent: A runtime error returns status 5 after preserving values emitted before the error.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: readme-interface (FEATURE-FOUNDATION-003.md)
  intent: README.md records the complete executable interface contract.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: readme-verification-command (FEATURE-FOUNDATION-003.md)
  intent: README.md identifies the supplied conformance command as the project verification entry point.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0

## Agent self-report (advisory)
The build agent declared a failure. This is advisory only; the programmatic acceptance above is the authority for this block's outcome.
- summary: Full jq conformance suite has 216 failures.
- detail:
    The CLI boundary and documentation checks pass, but broader jq parsing and evaluation features remain unsupported. Extend the parser/evaluator and rerun `sh sources/full_test.sh`.

## Build summary
<reusable-compact filename="run_conformance.py">
Requires `JQ` candidate command. Parses 550 corpus cases and 13 exclusions, runs each with `-c`, accepts compile exit `3` and runtime exit `5`, compares JSON structurally, and returns `0` only with zero failures/errors.
</reusable-compact>

<reusable-compact filename="full_test.sh">
Requires executable `./jq`, sets `JQ="$PWD/jq"`, and runs the complete conformance corpus via `python3 sources/run_conformance.py`.
</reusable-compact>

RESULT: FAILED

FILES CHANGED:
- jq
- README.md
- tests/test_cli_contract.py

SUMMARY:
Implemented the executable CLI, exit-status contract, README, and contract tests. CLI tests pass; full conformance result: 439 passed, 216 failed, 0 errored, 0 skipped.

BLOCKERS:
- jq language implementation remains incomplete for the full corpus.

FAILURE_SUMMARY: Full jq conformance suite has 216 failures.
FAILURE_DETAIL: The CLI boundary and documentation checks pass, but broader jq parsing and evaluation features remain unsupported. Extend the parser/evaluator and rerun `sh sources/full_test.sh`.
