# Blueprint Analysis: drydock jq Uat Kit

## Commander Expectations

- assert the executable jq interpreter passes every supplied jq 1.8.2 conformance case not declared excluded.
- assert the implementation uses only the Python standard library and the supplied execution environment.
- assert the supplied scoring command remains the sole complete-suite acceptance verdict.

## Crew

| Crew | Charge |
|---|---|
| Commander | Defines intent and decides what done means. |
| Team Lead | Confirms epic completeness and stakeholder expectations. |
| Planning Crew | Authors atomic specifications and the ordered Manifest. |
| Shipyard Crew | Builds the tickets without synchronous Commander access. |

## Story List

### Feature: Front End

| ID | Story | High-level AC |
|---|---|---|
| FRONTEND-001 | Implement jq lexer | The lexer recognizes jq literals, identifiers, bindings, operators, strings, interpolation, comments, formats, and invalid characters. |
| FRONTEND-002 | Implement jq parser and AST | The parser applies the supplied grammar and precedence rules and rejects invalid programs with exit code 3. |
| FRONTEND-003 | Implement string interpolation and formatting syntax | Interpolated strings and `@format` expressions evaluate according to the supplied lexer, parser, and corpus semantics. |

### Feature: Generator Evaluation Core

| ID | Story | High-level AC |
|---|---|---|
| CORE-001 | Implement stream-based filter evaluation | Filters produce zero, one, or many outputs and pipelines and commas preserve jq generator ordering and cartesian behavior. |
| CORE-002 | Implement values, indexing, iteration, slices, and construction | Literals, identity, field access, array/object indexing, iteration, slices, arrays, and objects match corpus behavior. |
| CORE-003 | Implement operators and comparisons | Arithmetic, concatenation, merge, equality, ordering, boolean operators, alternative, and optional evaluation match jq semantics. |

### Feature: Paths and Updates

| ID | Story | High-level AC |
|---|---|---|
| PATHS-001 | Implement path discovery and path access | `path`, `paths`, `getpath`, and path expressions produce and consume jq paths correctly. |
| PATHS-002 | Implement path mutation and deletion | `setpath`, `delpaths`, `del`, and indexed/sliced deletion handle missing, nested, and invalid paths correctly. |
| PATHS-003 | Implement assignment operators | Plain, update, arithmetic, and defined-or assignments apply jq immutable update semantics and generator rules. |

### Feature: Control Flow and Generators

| ID | Story | High-level AC |
|---|---|---|
| CONTROL-001 | Implement conditionals, errors, try/catch, and labels | Conditionals, runtime errors, suppression, catches, labels, and breaks preserve output and control-flow behavior. |
| CONTROL-002 | Implement reduction and iteration constructs | `reduce`, `foreach`, `limit`, `skip`, `first`, `last`, `nth`, `while`, `until`, and `repeat` evaluate streams correctly. |
| CONTROL-003 | Implement recursion and recursive descent | `recurse`, `..`, and recursive user-defined filters traverse structures and retain required generator ordering. |

### Feature: Functions and Bindings

| ID | Story | High-level AC |
|---|---|---|
| FUNCTIONS-001 | Implement variables and destructuring | Lexical bindings, array/object patterns, closures, and destructuring alternatives bind values as specified. |
| FUNCTIONS-002 | Implement user-defined functions | `def` declarations, filter arguments, value arguments, arity, recursion, redefinition, and lexical scope work correctly. |

### Feature: Builtins and Data Operations

| ID | Story | High-level AC |
|---|---|---|
| BUILTINS-001 | Implement core type, collection, and string builtins | Type predicates, collection transforms, sorting/grouping/uniqueness, containment, string operations, and Unicode helpers match the corpus. |
| BUILTINS-002 | Implement regular-expression builtins | `test`, `match`, `capture`, `scan`, `split`, `splits`, `sub`, and `gsub` provide the specified matching and replacement behavior. |
| BUILTINS-003 | Implement serialization, formats, dates, math, and streaming builtins | JSON conversion, format filters, date/time, mathematical, SQL-style, and streaming utilities satisfy supplied cases. |

### Feature: CLI and Verification

| ID | Story | High-level AC |
|---|---|---|
| CLI-001 | Implement the jq executable interface | An executable named `jq` accepts `-c '<program>'`, reads JSON values from stdin, emits compact JSON values one per line, and uses the specified exit codes. |
| CLI-002 | Stage and run the supplied conformance harness | The supplied assets are available under `sources/`, scoped conformance runs execute selected cases, and exclusions are applied without modifying scoring assets. |
| CLI-003 | Prove complete conformance | The terminal verification runs `sh sources/full_test.sh` and succeeds with every non-excluded supplied case passing and no failures or errors. |

## Story Guidance

Named stories planning must produce. Authoritative record: `STORY_GUIDANCE.json`.

| Story ID | Provenance | Gate | Note |
|---|---|---|---|
| FRONTEND-001 | plan | — | Suggested implementation order: lexer and parser; lexer.l is the lexical authority. |
| FRONTEND-002 | plan | — | Suggested implementation order: lexer and parser; parser.y is the grammar authority. |
| CORE-001 | plan | — | Suggested implementation order: generator core and stream evaluation. |
| PATHS-001 | plan | — | Suggested implementation order: paths and assignment. |
| CONTROL-001 | plan | — | Suggested implementation order: control flow and backtracking. |
| FUNCTIONS-001 | plan | — | Suggested implementation order: functions, variables, and destructuring. |
| BUILTINS-001 | plan | — | Suggested implementation order: builtins from builtin.jq and the manual. |
| CLI-003 | plan | `sh sources/full_test.sh` | Definition of Done and Sea Trial: complete supplied corpus verification. |

## Surfaced Acceptance Criteria

None.

## Source Inventory

| Path | Content kind | Disposition | Reason |
|---|---|---|---|
| `sources/INSTRUCTIONS.md` | markdown | analyzed | readable UTF-8 |
| `sources/builtin.jq` | text | analyzed | readable UTF-8 |
| `sources/exclusions.txt` | text | analyzed | readable UTF-8 |
| `sources/full_test.sh` | code | analyzed | readable UTF-8 |
| `sources/jq-manual.txt` | text | chunked | split into 11 bounded chunks |
| `sources/jq.test` | text | chunked | split into 5 bounded chunks |
| `sources/lexer.l` | text | analyzed | readable UTF-8 |
| `sources/parser.y` | text | analyzed | readable UTF-8 |
| `sources/run_conformance.py` | code | analyzed | readable UTF-8 |

## Relationship Model

| Source or group | Relationship type | Related source or group | Evidence | Delivery implication |
|---|---|---|---|---|
| `sources/lexer.l` | parser-to-normalizer | `sources/parser.y` | Lexer tokens and parser productions define the front-end contract. | Implement lexer behavior before parser integration. |
| `sources/parser.y` | normative specification | `sources/jq-manual.txt` | Grammar and precedence complement the manual's language semantics. | Resolve syntax and evaluation structure from both sources. |
| `sources/builtin.jq` | reference implementation | `sources/jq-manual.txt` | Builtin definitions provide executable semantic guidance for the manual. | Implement the evaluator primitives required by builtin definitions first. |
| `sources/jq.test` | test-kit-to-implementation | `sources/run_conformance.py` | The corpus supplies programs, inputs, and expected streams; the runner executes each case. | Every implementation story uses scoped corpus cases. |
| `sources/run_conformance.py` | test-kit-to-implementation | `sources/jq` | The harness invokes the candidate through `JQ` and validates output and exit codes. | Preserve the executable contract and stage the harness. |
| `sources/full_test.sh` | instruction-to-test | `CLI-003` | The supplied shell script is the sole unfiltered acceptance entry point. | Run it only in the terminal verification story. |
| `sources/exclusions.txt` | test-kit-to-implementation | `sources/jq.test` | Exclusions identify module-loader cases that are skipped by the harness. | Stage both files unchanged and preserve exclusion validation. |

## Source Roles

| Path | Role | Plan disposition | Build disposition |
|---|---|---|---|
| `sources/INSTRUCTIONS.md` | author intent | compass | prompt-only |
| `sources/builtin.jq` | reference implementation | context | stage |
| `sources/exclusions.txt` | conformance harness | context | stage |
| `sources/full_test.sh` | conformance harness | context | stage |
| `sources/jq-manual.txt` | normative specification | context | stage |
| `sources/jq.test` | normative specification and conformance test suite | context | stage |
| `sources/lexer.l` | normative specification | context | stage |
| `sources/parser.y` | normative specification | context | stage |
| `sources/run_conformance.py` | conformance harness | context | stage |

## Planning Instructions

### Delivery Shape

Deliver a standalone executable jq-compatible filter interpreter. It receives jq source through `-c`, reads JSON values from stdin, evaluates generator-based filters, and writes compact JSON outputs to stdout. The implementation is Python standard-library code with supplied conformance assets staged under `sources/`. Development uses scoped corpus slices; the final delivery uses the supplied full-test shell entry point.

### Story Realization Map

- `FRONTEND-001`–`FRONTEND-003`: lexer, parser, interpolation, and format syntax from `sources/lexer.l`, `sources/parser.y`, and `sources/jq-manual.txt`; capability stories.
- `CORE-001`–`CORE-003`: generator semantics, values, indexing, construction, operators, and comparisons from `sources/jq-manual.txt` and `sources/jq.test`; capability stories.
- `PATHS-001`–`PATHS-003`: path and assignment semantics from `sources/jq-manual.txt`, `sources/builtin.jq`, and `sources/jq.test`; capability stories.
- `CONTROL-001`–`CONTROL-003`: control-flow and recursive generator semantics from `sources/builtin.jq`, `sources/parser.y`, and `sources/jq.test`; capability stories.
- `FUNCTIONS-001`–`FUNCTIONS-002`: bindings, destructuring, definitions, closures, and scope from `sources/parser.y`, `sources/jq-manual.txt`, and `sources/jq.test`; capability stories.
- `BUILTINS-001`–`BUILTINS-003`: builtin semantics from `sources/builtin.jq`, `sources/jq-manual.txt`, and `sources/jq.test`; capability stories.
- `CLI-001`: executable interface and exit codes from `sources/INSTRUCTIONS.md` and `sources/full_test.sh`; capability and acceptance-contract story.
- `CLI-002`: staged runner and exclusion behavior from `sources/run_conformance.py`, `sources/jq.test`, and `sources/exclusions.txt`; test-harness story.
- `CLI-003`: complete-suite proof from `sources/full_test.sh`; terminal acceptance-contract story.

### Test and Acceptance Strategy

Each implementation story runs only a non-empty `--select` slice matching its construct. Harness and exclusion behavior is tested through bounded runner invocations. The terminal `CLI-003` story is the only story that runs the complete suite and declares `Suite: full`; it executes `sh sources/full_test.sh` and asserts only successful completion. Sea Trials provide the project-level complete-conformance and operating guardrails.

### Sequencing and Dependencies

Build the lexer before the parser, and the parser before evaluator and builtin stories. Establish the generator core before paths, control flow, functions, and builtins. Implement the executable interface before harness execution. Stage all source assets before scoped verification. The final full-suite story depends on every implementation and harness story.

### Source Conflicts and Gaps

No unresolved cross-source conflicts or blockers were found. The sources consistently define a standalone CLI interpreter, Python standard-library implementation, staged conformance corpus, declared module-loader exclusions, and one complete acceptance command.

## Analysis Notes
generated: 2026-08-21
blueprint: /mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260822.034407/workspace/targets/jq/blueprint

Quality: Ready
  blockers: 0
  questions: 0
  features: 7
  stories: 20
  stack: Python standard library with POSIX sh and JSON
  display_name: not proposed
  short_description: not proposed

Project type: cli. No UI, persistence, authentication, external service, or deployment-target gaps apply. The supplied source breakdown is reflected in the feature and story order.
