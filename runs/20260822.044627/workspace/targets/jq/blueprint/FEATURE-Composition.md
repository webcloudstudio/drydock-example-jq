# FEATURE: Composition

Pipes, commas, collections, objects, and cartesian generator semantics are supported.

## Programmatic Acceptance

=== AC core-002-conformance ===
from pathlib import Path
assert Path("jq").is_file()
assert Path("sources/jq.test").is_file()
=== END AC core-002-conformance ===
