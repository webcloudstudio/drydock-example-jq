# FEATURE: Formats and Serialization

JSON conversion and jq output-format filters are supported.

## Programmatic Acceptance

=== AC formats-conformance ===
from pathlib import Path
assert Path("jq").is_file()
assert Path("sources/jq.test").is_file()
=== END AC formats-conformance ===
