# Technology Stack

**Approved:** 2026-08-14

Technology decisions of record for this Target. One row per technology, naming the
Rigging best-practice file that governs building it.

A `—` in the Rigging column means no Rigging guidance exists for that technology; the
builder applies general best practice instead. Adding a row never requires a matching
Rigging file.

This file is owned by the UAT kit. It is seeded into the Target before `analyze`, which
never overwrites it, and `drydock plan` reads it to assign per-story `stack:` guidance.

| Technology | Rigging | Notes |
|---|---|---|
| Python | python.md | Python 3.11 or newer. Standard library only; the deliverable declares no third-party runtime dependency. |
| Shell | common.md | POSIX sh for the supplied scoring entry point. |
