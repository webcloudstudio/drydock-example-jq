# FEATURE: Path Primitives

Nested jq values can be read, updated, created, and deleted through path arrays.

## Programmatic Acceptance

=== AC path-002-conformance ===
from pathlib import Path
assert Path("jq").is_file()
assert Path("sources/jq.test").is_file()
=== END AC path-002-conformance ===
