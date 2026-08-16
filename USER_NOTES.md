No setup is required to run this kit. Python 3 is the only prerequisite, and the
kit needs no network access.

To re-fetch the pinned upstream files and re-check their hashes:

    sh uat/jq/tools/fetch_upstream.sh --verify
    python3 uat/jq/tools/render_manual.py --check

To calibrate the scoring instrument against real jq before trusting a run:

    curl -sL https://github.com/jqlang/jq/releases/download/jq-1.8.2/jq-linux-amd64 -o /tmp/jq182
    chmod +x /tmp/jq182
    cd uat/jq && JQ=/tmp/jq182 python3 sources/run_conformance.py

Expect: 537 passed, 0 failed, 0 errored, 13 skipped.
