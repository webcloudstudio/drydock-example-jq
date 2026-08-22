# FEATURE: Index and Membership

Search, quantifier, emptiness, indexing, joining, and membership utilities are supported.

## Programmatic Acceptance

=== AC data-004-conformance ===
from pathlib import Path
assert Path("jq").is_file()
assert Path("sources/jq.test").is_file()
=== END AC data-004-conformance ===
