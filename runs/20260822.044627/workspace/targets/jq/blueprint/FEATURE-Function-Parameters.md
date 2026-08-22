# FEATURE: Function Parameters

User-defined filter and value function parameters support multiple arities and generator arguments.

## Programmatic Acceptance

=== AC function-parameters-scoped-conformance ===
from pathlib import Path
assert Path("jq").is_file()
assert Path("sources/jq.test").is_file()
=== END AC function-parameters-scoped-conformance ===
