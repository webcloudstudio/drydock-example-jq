# FEATURE: Value Model

The runtime represents jq JSON values, including non-finite numeric values produced by filters.

## Programmatic Acceptance

=== AC value-001-conformance ===
from pathlib import Path
assert Path("jq").is_file()
assert Path("sources/jq.test").is_file()
=== END AC value-001-conformance ===
