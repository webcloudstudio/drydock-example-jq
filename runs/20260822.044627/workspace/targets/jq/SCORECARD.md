# Scorecard: jq

## Specification

> **NOT YET RUN**
> drydock score spec jq

## Acceptance

> **FAILED**
> drydock score ac jq · 2026-08-23T12:29:16.640+00:00

PASS 18   FAIL 3   UNVERIFIED 0   PREPASSED 36   (57 AC total)

Failed:
- text-003-regex-conformance — FEATURE-TEXT-003.md
- text-003-captures — FEATURE-TEXT-003.md
- io-003-conformance — FEATURE-IO-003.md

## Build

> **FAILED**
> drydock score build jq · 2026-08-23T12:29:18.889+00:00

Blocks: 43   Repaired: 2   Failed: 1
Tokens: 103,535,036 (cached 97,192,704, output 364,320)   Cache hit rate: 94.2%

## Release

> **RELEASED**
> drydock score release jq · 2026-08-23T12:33:02.229+00:00

- Verdict: PASSED

jq: PASSED — 1 of 1

  st-001  MET       ["sh", "sources/full_test.sh"] exited 0; sh sources/full_test.sh exited 0; jq conformance: 537 passed, 0 failed, 0 errored, 13 skipped
  reported: Build directory has uncommitted changes

## Project acceptance

| ID | Type | Criterion | Verdict | Observed |
|---|---|---|---|---|
| st-001 | technical | The completed interpreter shall make sh sources/full_test.sh exit zero; that script's exit status is the sole acceptance verdict. | MET | ["sh", "sources/full_test.sh"] exited 0; sh sources/full_test.sh exited 0; jq conformance: 537 passed, 0 failed, 0 errored, 13 skipped |

**Advisory warnings:**
- Build directory has uncommitted changes
