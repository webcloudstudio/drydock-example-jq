<!-- Compacted from jq.test sha256=329689763b651096989bd8260b643731083fc5fd17f6bd7834d158713f738cbd on 2026-08-16 by drydock build agent -->

The corpus is the authoritative jq 1.8.2 behavior suite. Valid programs must exit 0 with structurally matching ordered outputs; compile failures exit 3 and runtime failures exit 5. Deep-value tests require jq-compatible depth errors rather than host recursion failures.
