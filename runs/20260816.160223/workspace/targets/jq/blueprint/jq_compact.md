<!-- Compacted from jq.test sha256=329689763b651096989bd8260b643731083fc5fd17f6bd7834d158713f738cbd on 2026-08-16 by drydock build agent -->

The corpus defines jq’s compile/runtime contract: `%%FAIL` cases must exit 3; valid programs must execute with ordered generator outputs; runtime failures exit 5 while preserving prior output. Values are structurally compared, and module-loader cases are skipped only per `sources/exclusions.txt`. Frontend validation must reject malformed syntax, undefined variables/labels, invalid constant object keys, and invalid module metadata before evaluation.
