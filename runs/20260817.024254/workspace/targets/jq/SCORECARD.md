# Release Scorecard: jq

- Verdict: FAILED
- Code identity: 74de3d9912b2581d80993dbd9baf7a175d3810d0

## Project acceptance

| ID | Type | Criterion | Verdict | Observed |
|---|---|---|---|---|
| st-001 | technical | The completed interpreter shall make sh sources/full_test.sh exit zero; that script's exit status is the sole acceptance verdict. | NOT MET | governed gate sh sources/full_test.sh: return code 1; jq conformance: 320 passed, 217 failed, 13 skipped |

## Failures

- st-001: The completed interpreter shall make sh sources/full_test.sh exit zero; that script's exit status is the sole acceptance verdict.
- Governed acceptance gate failed: full: FAIL (exit 1) · sh sources/full_test.sh

## Manual verification required

- None.

## Could not judge

- None.

## Advisory warnings

- Build directory has uncommitted changes

## Ranked improvements

1. Resolve st-001 (NOT MET): The completed interpreter shall make sh sources/full_test.sh exit zero; that script's exit status is the sole acceptance verdict.
2. Make sh sources/full_test.sh pass all required conformance cases.
