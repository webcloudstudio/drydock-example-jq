# Evidence: Block 2 · Service (block-2)

- block type: block
- date: 2026-08-17
- resulting state: closed/verified
- story points (combined assembled cost): 4550
- execution id: 20260817.181016.110Z-bfc4d565

## Stories built
- Map compilation and runtime failures to the required exit codes. (cli-exit-semantics) [story]
- Document the jq command-line contract. (cli-documentation) [story]

## Stacked context
- compass: COMPASS.md (SP 2068)
- implements: FEATURE-CLI-Exit-Semantics.md (SP 505)
- stack: python_compact.md (SP 1534)
- implements: FEATURE-CLI-Documentation.md (SP 369)

## Build directory changes
- README.md
- jq
- tests/test_cli.py

## Pre-build acceptance observation
- GREEN (prepassed): cli-exit-compile (FEATURE-CLI-Exit-Semantics.md)
  intent: A syntactically invalid jq program returns the documented compile-failure status.
  return code: 0
- RED: cli-exit-runtime (FEATURE-CLI-Exit-Semantics.md)
  intent: A compiled program that raises at runtime returns the documented runtime-failure status.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      result = CompletedProcess(args=['./jq', '-c', 'error'], returncode=3, stdout='', stderr='jq: unsupported jq program\n')
    --- drydock: end values ---
    Traceback (most recent call last):
      File "cli-exit-runtime.py", line 11, in <module>
        assert result.returncode == 5
               ^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: cli-exit-partial-output (FEATURE-CLI-Exit-Semantics.md)
  intent: Values produced before a runtime error remain available to the caller.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      result = CompletedProcess(args=['./jq', '-c', '1, error'], returncode=3, stdout='', stderr='jq: unsupported jq program\n')
    --- drydock: end values ---
    Traceback (most recent call last):
      File "cli-exit-partial-output.py", line 13, in <module>
        assert result.returncode == 5
               ^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: cli-documentation-content (FEATURE-CLI-Documentation.md)
  intent: README documents the required command-line contract and verification command.
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
      File "cli-documentation-content.py", line 3, in <module>
        readme = Path("README.md").read_text(encoding="utf-8")
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/home/barlo/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/pathlib.py", line 1027, in read_text
        with self.open(mode='r', encoding=encoding, errors=errors) as f:
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/home/barlo/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/pathlib.py", line 1013, in open
        return io.open(self, mode, buffering, encoding, errors, newline)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    FileNotFoundError: [Errno 2] No such file or directory: 'README.md'
- RED: cli-documentation-statuses (FEATURE-CLI-Documentation.md)
  intent: README documents all three required exit statuses.
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
      File "cli-documentation-statuses.py", line 3, in <module>
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
- PASS: cli-exit-compile (FEATURE-CLI-Exit-Semantics.md)
  intent: A syntactically invalid jq program returns the documented compile-failure status.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: cli-exit-runtime (FEATURE-CLI-Exit-Semantics.md)
  intent: A compiled program that raises at runtime returns the documented runtime-failure status.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: cli-exit-partial-output (FEATURE-CLI-Exit-Semantics.md)
  intent: Values produced before a runtime error remain available to the caller.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: cli-documentation-content (FEATURE-CLI-Documentation.md)
  intent: README documents the required command-line contract and verification command.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: cli-documentation-statuses (FEATURE-CLI-Documentation.md)
  intent: README documents all three required exit statuses.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0

## Build summary
RESULT: SUCCESS

FILES CHANGED:
- README.md
- jq
- tests/test_cli.py

SUMMARY:
Implemented compile status `3`, runtime status `5`, partial output preservation, and documented the CLI contract. All declared acceptance checks and 6 unit tests pass.

BLOCKERS:
- None
