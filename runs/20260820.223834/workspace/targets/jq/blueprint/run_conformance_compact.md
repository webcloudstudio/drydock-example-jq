<!-- Compacted from run_conformance.py sha256=c1b5be717d542f2d2dc4f4a694dd02ae8c8f84b25f15c6224fbb6a784abe7492 on 2026-08-20 by drydock build agent -->

Parses jq.test cases and exclusions via parse_corpus, parse_exclusions, and apply_exclusions. Runs candidate from JQ, comparing structured JSON outputs. Candidate compile errors use exit 3; runtime errors use exit 5.
