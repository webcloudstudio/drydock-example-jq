# Release Scorecard: jq

- Verdict: FAILED
- Code identity: 68995ffacb24f79da01a5c6ce063875d28a433de

## Project acceptance

| ID | Type | Criterion | Verdict | Observed |
|---|---|---|---|---|
| st-001 | technical | The completed interpreter shall make sh sources/full_test.sh exit zero; that script's exit status is the sole acceptance verdict. | NOT MET | sh sources/full_test.sh returned code 1; jq conformance: 145 passed, 392 failed, 0 errored, 13 skipped |

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
2. Restore jq conformance across the failing parser, built-in, runtime, and formatting behaviors before release.
