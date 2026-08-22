# FEATURE: Streaming Transformations

Streaming representations can be emitted, reconstructed, and truncated.

## Programmatic Acceptance

=== AC streaming-conformance ===
from pathlib import Path
assert Path("jq").is_file()
assert Path("sources/jq.test").is_file()
=== END AC streaming-conformance ===
