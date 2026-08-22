# FEATURE: Object Entries and Containment

Object keys, entries, containment, and entry transformations follow jq semantics.

## Programmatic Acceptance

=== AC data-003-conformance ===
from pathlib import Path
assert Path("jq").is_file()
assert Path("sources/jq.test").is_file()
=== END AC data-003-conformance ===
