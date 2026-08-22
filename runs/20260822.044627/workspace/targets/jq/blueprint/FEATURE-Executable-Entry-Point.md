# FEATURE: Executable Entry Point

The application provides the executable `./jq -c '<program>'` interface.

## Programmatic Acceptance

=== AC executable-permission ===
from pathlib import Path
entry = Path("jq")
assert entry.is_file()
assert entry.stat().st_mode & 0o111
=== END AC executable-permission ===
