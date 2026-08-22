# FEATURE: Reductions and Iteration Control

Reductions, iteration controls, range generation, and generator selection are supported.

## Programmatic Acceptance

=== AC reductions-scoped-conformance ===
from pathlib import Path
assert Path("jq").is_file()
assert Path("sources/jq.test").is_file()
=== END AC reductions-scoped-conformance ===
