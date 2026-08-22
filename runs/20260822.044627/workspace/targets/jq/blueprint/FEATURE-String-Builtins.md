# FEATURE: String Builtins

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provides jq string trimming, conversion, case, splitting, joining, and codepoint builtins. |
| Depends On  | FEATURE-Index-and-Membership.md, FEATURE-Value-Model.md |
| Provides    | trim, ltrim, rtrim, ltrimstr, rtrimstr, trimstr, startswith, endswith, ascii_downcase, ascii_upcase, explode, implode, split, splits, join |
| Consumes    | jq value model, generator evaluation, string interpolation |

## Scope

This feature implements jq's standard string manipulation filters using Unicode-aware codepoint handling where specified and ASCII-only case conversion for `ascii_downcase` and `ascii_upcase`.

## Behavior

- `trim`, `ltrim`, and `rtrim` use jq's defined Unicode whitespace set.
- Prefix and suffix filters remove text only when the corresponding string is present.
- ASCII case filters alter only ASCII letters.
- `explode` converts strings to codepoint arrays and `implode` applies jq replacement behavior for invalid codepoints.
- `split` returns an array; `splits` returns a stream.
- `join` converts supported scalar values according to jq rules and treats `null` as an empty field.

## Programmatic Acceptance

=== AC text-001-conformance ===
Intent: The authoritative corpus slice containing string manipulation and codepoint syntax executes and passes without failures or errors.

import json
import os
import subprocess
import sys

selector = r"split|join|trim|ascii_|explode|implode|startswith|endswith"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", selector, "--json"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
report = json.loads(result.stdout)
summary = report["summary"]
assert sum(summary.values()) > 0
assert summary["fail"] == 0 and summary["error"] == 0
assert result.returncode == 0
=== END AC text-001-conformance ===

## User Acceptance

- None.

## Guardrails

- Preserve Unicode codepoints and embedded null characters.
- Keep ASCII case conversion distinct from general Unicode case folding.
- Reject unsupported scalar conversions and malformed codepoints according to jq semantics.
