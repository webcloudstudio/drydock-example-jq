# FEATURE: Conformance Assets

The supplied conformance corpus and harness are staged unchanged.

## Programmatic Acceptance

=== AC conformance-assets-parse ===
from pathlib import Path
assert Path("sources/jq.test").is_file()
assert Path("sources/exclusions.txt").is_file()
=== END AC conformance-assets-parse ===
