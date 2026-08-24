<!-- Compacted from run_conformance.py sha256=c1b5be717d542f2d2dc4f4a694dd02ae8c8f84b25f15c6224fbb6a784abe7492 on 2026-08-22 by drydock build agent -->

Run `JQ=./jq python3 sources/run_conformance.py`; candidate must emit JSON lines and use exit 3 for compile errors, 5 for runtime errors. Harness reports structural output matches and supports scoped execution via `--select REGEX --json`; exit 2 indicates harness faults.
