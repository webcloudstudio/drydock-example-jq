# FEATURE: Process Contract

Compilation, runtime failure, success, diagnostics, and partial output follow the required exit contract.

## Programmatic Acceptance

=== AC process-compile-exit ===
import subprocess
result = subprocess.run(["./jq", "-c", "{"], input="null\n", capture_output=True, text=True)
print(result.stdout, result.stderr)
assert result.returncode == 3
assert result.stderr
=== END AC process-compile-exit ===
