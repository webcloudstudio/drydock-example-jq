# FEATURE: Truthiness and Comparison

Jq truthiness, equality, inequality, and structural ordering are supported.

## Programmatic Acceptance

=== AC core-004-conformance ===
from pathlib import Path
assert Path("jq").is_file()
assert Path("sources/jq.test").is_file()
=== END AC core-004-conformance ===
