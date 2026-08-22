# FEATURE: Errors and Optional Evaluation

Empty streams, runtime errors, exception handling, optional evaluation, and partial output are supported.

## Programmatic Acceptance

=== AC core-003-conformance ===
from pathlib import Path
assert Path("jq").is_file()
assert Path("sources/jq.test").is_file()
=== END AC core-003-conformance ===
