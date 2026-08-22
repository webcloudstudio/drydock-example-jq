# FEATURE: Lexer

The lexer tokenizes jq literals, identifiers, operators, delimiters, comments, and formats.

## Programmatic Acceptance

=== AC lexer-basic-tokens ===
from pathlib import Path
assert Path("jq").is_file()
assert Path("sources/jq.test").is_file()
=== END AC lexer-basic-tokens ===
