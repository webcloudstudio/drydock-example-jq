<!-- Compacted from run_conformance.py sha256=c1b5be717d542f2d2dc4f4a694dd02ae8c8f84b25f15c6224fbb6a784abe7492 on 2026-08-16 by drydock build agent -->

Runs each `jq.test` case independently with a 10-second timeout. Requires exit code 3 for compile failures, 0 or 5 for normal/runtime cases, and compares newline-delimited JSON structurally. Harness exits 0 only when all non-skipped cases pass.
