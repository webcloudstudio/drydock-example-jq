# FEATURE: Advanced Grammar

The parser supports declarations, control constructs, bindings, modules, and destructuring syntax.

## Programmatic Acceptance

=== AC parse-004-conformance ===
from pathlib import Path
assert Path("jq").is_file()
assert Path("sources/jq.test").is_file()
=== END AC parse-004-conformance ===
