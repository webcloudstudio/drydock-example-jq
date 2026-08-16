# Release Scorecard: jq

- Verdict: FAILED
- Code identity: 680a1ccc09650aec97f6a11f3b5a51ed1f211971

## Project acceptance

| ID | Type | Criterion | Verdict | Observed |
|---|---|---|---|---|
| st-001 | technical | The completed interpreter shall make sh sources/full_test.sh exit zero; that script's exit status is the sole acceptance verdict. | NOT MET | sh sources/full_test.sh returned code 1; sources/full_test.sh: jq conformance reported 456 failed tests |

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
2. Make the interpreter pass the full jq conformance suite, addressing the reported missing AST nodes, builtins, parsing, and evaluation mismatches.
