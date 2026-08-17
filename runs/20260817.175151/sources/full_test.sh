#!/bin/sh
# full_test.sh — scoring entry point. Do not filter, skip, or reinterpret.
#
# `drydock uat` runs `sh sources/full_test.sh` from the completed application root and takes its
# exit code and output as the score. The interface check is separate from the conformance run so
# that a missing or non-executable program and a genuine conformance failure are distinguishable
# in the evidence. JQ is the harness's only knowledge of the implementation language; the
# harness itself is language-neutral.
set -eu
if [ ! -x ./jq ]; then
    echo "error: no executable ./jq at the application root." >&2
    echo "The deliverable is an executable named jq that reads JSON on stdin." >&2
    exit 1
fi
JQ="$PWD/jq" exec python3 sources/run_conformance.py
