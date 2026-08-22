# FEATURE: Assignment Operators

Deletion and immutable assignment operators are supported.

## Programmatic Acceptance

=== AC path-003-conformance ===
from pathlib import Path
assert Path("jq").is_file()
assert Path("sources/jq.test").is_file()
=== END AC path-003-conformance ===
