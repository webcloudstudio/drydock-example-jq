# FEATURE: Slices and Iteration

Array and string slices and array/object iteration preserve jq ordering and multiplicity.

## Programmatic Acceptance

=== AC value-003-conformance ===
from pathlib import Path
assert Path("jq").is_file()
assert Path("sources/jq.test").is_file()
=== END AC value-003-conformance ===
