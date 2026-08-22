# FEATURE: Collection Transformations

Collection transformation and recursive traversal builtins preserve generator ordering and multiplicity.

## Programmatic Acceptance

=== AC data-001-conformance ===
from pathlib import Path
assert Path("jq").is_file()
assert Path("sources/jq.test").is_file()
=== END AC data-001-conformance ===
