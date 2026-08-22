<!-- Compacted from jq.test sha256=329689763b651096989bd8260b643731083fc5fd17f6bd7834d158713f738cbd on 2026-08-22 by drydock build agent -->

- Corpus cases are blank-line-separated groups: program, JSON input, expected output lines.
- `%%FAIL` cases require compile exit code `3`; runtime cases accept exit `0` or `5` with matching partial output.
- Outputs are compared structurally as JSON; numeric `1` and `1.0` are equivalent.
- Preserve output ordering, multiplicity, Unicode, compact one-value-per-line serialization, and special numeric behavior.
