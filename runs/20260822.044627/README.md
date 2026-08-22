# jq: FAILED

1 of 6 receipt claims proven. Open `index.html` for the linked proof kit; verify it with `sha256sum -c SHA256SUMS`.

## Receipt

| Claim | Verdict | Recorded outcome | Proof |
|---|---|---|---|
| Lifecycle completed | FAIL | 10 lifecycle commands executed; the run ended at 10-after-plan-workspace-status. | [result.json](result.json) |
| External conformance suite passed | UNPROVEN | No external test command is defined for this project. | — |
| Target completion check passed | UNPROVEN | No completion check was recorded for this run. | — |
| Acceptance score passed | UNPROVEN | No acceptance score was recorded for this run. | — |
| Release score passed | UNPROVEN | No release score was recorded for this run. | — |
| Integrity verification passed | PASS | 461 files digested; verify with sha256sum -c SHA256SUMS. | [SHA256SUMS](SHA256SUMS) |

## Run facts

- Drydock: `0.2.0` (commit `4e0368d03ff9c237a39c51b815227b9714776ffe`)
- Provider and model: `codex` / `gpt-5.6-luna`
- Platform: `Linux-6.6.87.2-microsoft-standard-WSL2-x86_64-with-glibc2.35` on Python `3.12.13`
- Target: `jq`
- Run: `20260822.044627`
- Ran: 2026-08-22 00:46:27 EDT — 2026-08-22 01:16:38 EDT
- Elapsed: 1811.2s
- LLM calls: 44
- Tokens: cached 457,472; uncached 1,597,114; output 87,375
- LLM elapsed: 1742.2s
- Build passes: 0; repairs: not recorded
- Conformance: no external suite defined
- Verdict: expected PASSED, observed ERROR
- Advisory scores: none recorded

## RUN SUMMARY

- Input specification: [`sources/INSTRUCTIONS.md`](sources/INSTRUCTIONS.md)
- Delivered Code: [`build/jq/`](build/jq)
- Test Results: not recorded for this run.

## RUN NOTES:

- One run is evidence of one run. It is not a benchmark.
- It is not a security certification of the delivered code.

## Shortfall

- Failure: jq: stopped at plan-repair: acceptance criteria still cannot run after one repair pass

## Commands

| # | Command | Exit | Elapsed | Output |
|---|---|---|---|---|
| 01-init | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python3 -m drydock init jq` | 0 | 2.3s | [stdout](evidence/commands/01-init.stdout.log) · [stderr](evidence/commands/01-init.stderr.log) |
| 02-import-sources | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python3 -m drydock import jq sources --format markdown` | 0 | 3.8s | [stdout](evidence/commands/02-import-sources.stdout.log) · [stderr](evidence/commands/02-import-sources.stderr.log) |
| 03-analyze | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python3 -m drydock analyze jq` | 0 | 129.6s | [stdout](evidence/commands/03-analyze.stdout.log) · [stderr](evidence/commands/03-analyze.stderr.log) · [llm](evidence/commands/03-analyze.llm.log) |
| 04-plan | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python3 -m drydock plan jq --override` | 0 | 1357.1s | [stdout](evidence/commands/04-plan.stdout.log) · [stderr](evidence/commands/04-plan.stderr.log) · [llm](evidence/commands/04-plan.llm.log) |
| 05-plan-verify | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python3 -m drydock plan verify jq` | 1 | 2.0s | [stdout](evidence/commands/05-plan-verify.stdout.log) · [stderr](evidence/commands/05-plan-verify.stderr.log) |
| 06-plan-repair | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python3 -m drydock plan repair jq` | 1 | 303.3s | [stdout](evidence/commands/06-plan-repair.stdout.log) · [stderr](evidence/commands/06-plan-repair.stderr.log) · [llm](evidence/commands/06-plan-repair.llm.log) |
| 07-plan-verify-after-repair | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python3 -m drydock plan verify jq` | 1 | 2.9s | [stdout](evidence/commands/07-plan-verify-after-repair.stdout.log) · [stderr](evidence/commands/07-plan-verify-after-repair.stderr.log) |
| 08-after-plan-build-status | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python3 -m drydock build status jq` | 0 | 1.3s | [stdout](evidence/commands/08-after-plan-build-status.stdout.log) · [stderr](evidence/commands/08-after-plan-build-status.stderr.log) |
| 09-after-plan-target-status | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python3 -m drydock status jq` | 0 | 1.2s | [stdout](evidence/commands/09-after-plan-target-status.stdout.log) · [stderr](evidence/commands/09-after-plan-target-status.stderr.log) |
| 10-after-plan-workspace-status | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python3 -m drydock status` | 0 | 0.4s | [stdout](evidence/commands/10-after-plan-workspace-status.stdout.log) · [stderr](evidence/commands/10-after-plan-workspace-status.stderr.log) |

## Evidence

- [`evidence/commands/`](evidence/commands) — stdout and stderr of every command
- [`evidence/prompts/`](evidence/prompts) — the assembled prompt for every LLM call
- [`evidence/provider_raw/`](evidence/provider_raw) — unmodified provider transcripts
- [`evidence/llm_logs/`](evidence/llm_logs) — call banners and token accounting
- [`result.json`](result.json) — the machine-readable record of this run
