# Evidence: Block 1 · Foundational (block-1)

- block type: block
- date: 2026-08-20
- resulting state: closed/verified
- story points (combined assembled cost): 9533
- execution id: 20260820.230131.595Z-6fdb819d

## Stories built
- Define project identity and executable delivery metadata. (project-identity) [story]

## Stacked context
- compass: COMPASS.md (SP 3420)
- implements: METADATA.md (SP 378)
- stack: common.md (SP 1807)
- stack: python.md (SP 3892)

## Build directory changes
- METADATA.md
- tests/test_metadata.py

## Pre-build acceptance observation
- RED: metadata-contract (METADATA.md)
  intent: Project metadata declares the executable interface and approved runtime stack.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      self = PosixPath('METADATA.md')
      mode = 'r'
      buffering = -1
      encoding = 'utf-8'
      errors = None
      newline = None
    --- drydock: end values ---
    Traceback (most recent call last):
      File "metadata-contract.py", line 3, in <module>
        text = Path("METADATA.md").read_text(encoding="utf-8")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/home/barlo/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/pathlib.py", line 1027, in read_text
        with self.open(mode='r', encoding=encoding, errors=errors) as f:
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/home/barlo/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/pathlib.py", line 1013, in open
        return io.open(self, mode, buffering, encoding, errors, newline)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    FileNotFoundError: [Errno 2] No such file or directory: 'METADATA.md'
- RED: metadata-interface (METADATA.md)
  intent: Project metadata records the required compact-filter command shape.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      self = PosixPath('METADATA.md')
      mode = 'r'
      buffering = -1
      encoding = 'utf-8'
      errors = None
      newline = None
    --- drydock: end values ---
    Traceback (most recent call last):
      File "metadata-interface.py", line 3, in <module>
        text = Path("METADATA.md").read_text(encoding="utf-8")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/home/barlo/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/pathlib.py", line 1027, in read_text
        with self.open(mode='r', encoding=encoding, errors=errors) as f:
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/home/barlo/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/pathlib.py", line 1013, in open
        return io.open(self, mode, buffering, encoding, errors, newline)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    FileNotFoundError: [Errno 2] No such file or directory: 'METADATA.md'

## Post-build programmatic acceptance
- PASS: metadata-contract (METADATA.md)
  intent: Project metadata declares the executable interface and approved runtime stack.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: metadata-interface (METADATA.md)
  intent: Project metadata records the required compact-filter command shape.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0

## Build summary
RESULT: SUCCESS

FILES CHANGED:
- METADATA.md
- tests/test_metadata.py

SUMMARY:
Created jq project metadata and executable contract. Both acceptance checks and 2 unit tests pass.

BLOCKERS:
- None
