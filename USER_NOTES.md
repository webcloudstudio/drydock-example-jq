# Host prerequisites

| Tool | Needed for | When |
|---|---|---|
| `python3` (3.11 or newer) | `sources/run_conformance.py` and the delivered interpreter | every run |
| POSIX `sh` | `sources/full_test.sh`, the scoring entry point | every run |
| `curl` | fetching upstream files and the pinned jq release binary | authoring and calibration only |

A run installs nothing and needs no network access. Nothing beyond the Python standard
library is used, by the harness or by the deliverable.

To re-fetch the pinned upstream files and re-check their hashes — needs `curl` and network
access:

    sh uat/jq/tools/fetch_upstream.sh --verify
    python3 uat/jq/tools/render_manual.py --check

To calibrate the scoring instrument against real jq before trusting a run:

    curl -sL https://github.com/jqlang/jq/releases/download/jq-1.8.2/jq-linux-amd64 -o /tmp/jq182
    chmod +x /tmp/jq182
    cd uat/jq && JQ=/tmp/jq182 python3 sources/run_conformance.py

Expect: `537 passed, 0 failed, 0 errored, 13 skipped`, exit 0.
