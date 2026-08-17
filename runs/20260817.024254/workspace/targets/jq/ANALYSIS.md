# Blueprint Analysis: jq

## Commander Expectations

- assert the interpreter passes every supplied jq conformance case that is not explicitly excluded.
- assert the deliverable is an executable `jq` CLI that reads JSON from stdin and emits compact JSON values on stdout.

## Crew

| Crew | Charge |
|---|---|
| Commander | Defines intent and decides what done means. |
| Team Lead | Confirms epic completeness and stakeholder expectations. |
| Planning Crew | Authors atomic specifications and the ordered Manifest. |
| Shipyard Crew | Builds the tickets without synchronous Commander access. |

## Story List

### Feature: CLI Contract

| ID | Story | High-level AC |
|---|---|---|
| CLI-001 | Implement the executable jq command interface | `./jq -c '<program>'` reads JSON stdin, emits one compact JSON value per line, and returns the documented exit codes. |
| CLI-002 | Implement compile and runtime diagnostics | Invalid programs return exit 3; runtime failures return exit 5; diagnostics are written to stderr. |

### Feature: Language Front End

| ID | Story | High-level AC |
|---|---|---|
| FRONTEND-001 | Implement jq lexical analysis | jq literals, identifiers, bindings, strings, interpolation, comments, operators, formats, and delimiters are tokenized according to the supplied lexer specification. |
| FRONTEND-002 | Implement jq parsing and AST construction | Valid jq programs compile into an executable AST with the supplied precedence, associativity, function, binding, destructuring, module-grammar, and control-flow forms. |
| FRONTEND-003 | Implement user-defined functions and lexical bindings | `def`, filter arguments, value arguments, closures, recursion, lexical scope, and destructuring bindings behave according to the corpus and manual. |

### Feature: Generator Evaluation Core

| ID | Story | High-level AC |
|---|---|---|
| EVAL-001 | Implement stream-based filter evaluation | Identity, literals, pipes, commas, iteration, collection, `empty`, and cartesian filter evaluation preserve jq output order and multiplicity. |
| EVAL-002 | Implement operators and conditional control flow | Arithmetic, comparison, Boolean operators, alternative selection, conditionals, optional filters, and error propagation follow jq semantics. |
| EVAL-003 | Implement generator control constructs | `reduce`, `foreach`, `limit`, `skip`, `first`, `last`, `nth`, `while`, `until`, `repeat`, labels, breaks, and recursion support backtracking correctly. |

### Feature: Data, Paths, and Assignment

| ID | Story | High-level AC |
|---|---|---|
| DATA-001 | Implement JSON values and structural operations | Arrays, objects, strings, numbers, nulls, type checks, equality, ordering, containment, indexing, iteration, and slicing behave as specified. |
| DATA-002 | Implement path discovery and path mutation | `path`, `paths`, `getpath`, `setpath`, `delpaths`, and `del` produce and consume valid paths, including nested and missing structures. |
| DATA-003 | Implement assignment operators | Plain, update, arithmetic, defined-or, and complex path assignments produce the correct immutable replacement values and deletion behavior. |

### Feature: Built-in Filter Library

| ID | Story | High-level AC |
|---|---|---|
| BUILTIN-001 | Implement collection and object builtins | Mapping, filtering, reduction, sorting, grouping, uniqueness, entries, joins, flattening, transposition, combinations, and object helpers match jq behavior. |
| BUILTIN-002 | Implement string and Unicode builtins | String trimming, splitting, joining, case conversion, indexing, escaping, exploding, imploding, JSON conversion, and interpolation handle Unicode and embedded characters correctly. |
| BUILTIN-003 | Implement regular-expression builtins | `test`, `match`, `capture`, `scan`, `split`, `splits`, `sub`, and `gsub` support the corpus-required regex behavior and flags. |
| BUILTIN-004 | Implement formatting, date, math, and environment builtins | Formats, date conversion, math functions, numeric predicates, environment access, and related builtins return jq-compatible values or errors. |
| BUILTIN-005 | Implement streaming, I/O, and SQL-style builtins | `input`, `inputs`, `debug`, `stderr`, `tostream`, `fromstream`, `truncate_stream`, `INDEX`, `JOIN`, and `IN` behave as specified for the exercised interface. |

### Feature: Verification and Delivery

| ID | Story | High-level AC |
|---|---|---|
| VERIFY-001 | Stage the supplied conformance assets | The required manual, grammar, lexer, reference builtin source, corpus, exclusions, and harness files are available under `sources/` without modification. |
| VERIFY-002 | Add bounded implementation verification | Focused tests exercise parser, evaluator, builtins, assignments, errors, and CLI behavior without invoking the complete acceptance suite. |
| VERIFY-003 | Run the complete jq conformance gate | The terminal verification runs `sh sources/full_test.sh` as the sole complete-suite acceptance check and succeeds with no failed or errored cases. |

## Surfaced Acceptance Criteria

| ID | Story ID | Criterion |
|---|---|---|
| AC-001 | CLI-001 | When stdin contains multiple JSON texts, the CLI shall process the input stream and emit each produced value as a separate compact JSON line. |
| AC-002 | CLI-002 | If compilation or execution fails, the CLI shall preserve the documented distinction between compile exit 3 and runtime exit 5 and shall keep diagnostics off stdout. |
| AC-003 | VERIFY-001 | The implementation shall not depend on network access, package installation, third-party jq implementations, or a system jq executable. |

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
| `sources/lexer.l` | parser-to-normalizer | `sources/parser.y` | Lexer tokens and parser productions define the language front end. | Build lexer behavior before parser integration. |
| `sources/parser.y` | instruction-to-test | `sources/jq.test` | Grammar, precedence, bindings, assignments, and module syntax are exercised by corpus cases. | Parser stories require focused syntax and compile-error tests. |
| `sources/jq-manual.txt` | reference-to-replacement | `sources/builtin.jq` | Manual semantics and jq-defined builtin implementations specify the runtime library. | Implement generator core before builtin expansion. |
| `sources/builtin.jq` | implementation-to-helper | `sources/parser.y` | Builtins rely on parser-supported functions, generators, paths, assignments, and private helpers. | Builtin delivery depends on evaluator and mutation primitives. |
| `sources/run_conformance.py` | test-kit-to-implementation | `jq` | Harness invokes the executable with `-c`, stdin, and one process per case. | Preserve exact CLI and exit-code contract. |
| `sources/full_test.sh` | instruction-to-test | `sources/run_conformance.py` | The shell script is the single scoring entry point. | Only the terminal verification story runs the unfiltered suite. |
| `sources/exclusions.txt` | dependency | `sources/jq.test` | Exclusions identify loader cases that must be skipped and validate against corpus programs. | Stage both files unchanged and preserve exclusion handling. |

## Source Roles

| Path | Role | Plan disposition | Build disposition |
|---|---|---|---|
| `sources/INSTRUCTIONS.md` | author intent | compass | prompt-only |
| `sources/jq-manual.txt` | normative specification | context | stage |
| `sources/jq.test` | normative specification and conformance test suite | context | stage |
| `sources/parser.y` | normative specification | context | stage |
| `sources/lexer.l` | normative specification | context | stage |
| `sources/builtin.jq` | reference implementation | context | stage |
| `sources/run_conformance.py` | conformance harness | context | stage |
| `sources/full_test.sh` | conformance harness | context | stage |
| `sources/exclusions.txt` | conformance harness | context | stage |

## Planning Instructions

### Delivery Shape

Deliver a standalone Python interpreter exposed as an executable named `jq`. It accepts a jq filter through the command line, reads JSON values from stdin, evaluates filters as ordered generators, and writes compact JSON outputs to stdout. The runtime is layered as lexer/parser, AST and generator evaluator, data/path mutation primitives, builtin library, and CLI/verification harness.

### Story Realization Map

| Story ID | Durable Blueprint scope | Evidence | Related files | Delivery kind |
|---|---|---|---|---|
| CLI-001 | Executable entry point and stdin/stdout protocol | `sources/INSTRUCTIONS.md`, `sources/full_test.sh` | `jq` | capability, acceptance contract |
| CLI-002 | Exit status and diagnostics | `sources/INSTRUCTIONS.md`, `sources/run_conformance.py` | `jq` | capability |
| FRONTEND-001 | Lexer implementation | `sources/lexer.l` | `sources/lexer.l` | capability |
| FRONTEND-002 | Parser and AST | `sources/parser.y` | `sources/parser.y` | capability |
| FRONTEND-003 | Functions, variables, patterns | `sources/parser.y`, `sources/jq-manual.txt` | `sources/jq.test` | capability |
| EVAL-001 | Generator execution engine | `sources/INSTRUCTIONS.md`, `sources/jq-manual.txt` | `sources/jq.test` | capability |
| EVAL-002 | Operators and conditionals | `sources/jq-manual.txt`, `sources/parser.y` | `sources/jq.test` | capability |
| EVAL-003 | Backtracking control flow | `sources/builtin.jq`, `sources/jq-manual.txt` | `sources/jq.test` | capability |
| DATA-001 | JSON and structural semantics | `sources/jq-manual.txt` | `sources/jq.test` | capability |
| DATA-002 | Paths and mutation primitives | `sources/jq-manual.txt`, `sources/builtin.jq` | `sources/jq.test` | capability |
| DATA-003 | Assignment semantics | `sources/parser.y`, `sources/jq-manual.txt` | `sources/jq.test` | capability |
| BUILTIN-001 | Collection and object filters | `sources/builtin.jq`, `sources/jq-manual.txt` | `sources/jq.test` | capability |
| BUILTIN-002 | String and Unicode filters | `sources/jq-manual.txt` | `sources/jq.test` | capability |
| BUILTIN-003 | Regex filters | `sources/jq-manual.txt`, `sources/builtin.jq` | `sources/jq.test` | capability |
| BUILTIN-004 | Formatting, dates, math, environment | `sources/jq-manual.txt`, `sources/builtin.jq` | `sources/jq.test` | capability |
| BUILTIN-005 | Streaming, I/O, SQL-style filters | `sources/jq-manual.txt`, `sources/builtin.jq` | `sources/jq.test` | capability |
| VERIFY-001 | Build-time source staging | `sources/INSTRUCTIONS.md` | all staged `sources/*` assets | acceptance contract |
| VERIFY-002 | Focused verification | `sources/INSTRUCTIONS.md` | implementation tests | test harness |
| VERIFY-003 | Full corpus gate | `sources/full_test.sh`, `sources/run_conformance.py` | `sources/jq.test`, `sources/exclusions.txt` | acceptance contract |

### Test and Acceptance Strategy

Each implementation story uses focused corpus selections or targeted tests for its owned behavior and declares `Suite: scoped`. `VERIFY-002` validates bounded slices and CLI/error behavior. `VERIFY-003` is the only terminal story with `Suite: full`; it runs the complete supplied harness and gates the release through its exit status.

### Sequencing and Dependencies

Stage all required source assets before implementation. Build the lexer before parser integration, parser and AST before evaluation, generator semantics before builtins, and path primitives before assignment and mutation-heavy builtins. Build the executable before CLI verification. Run focused verification after each capability area; run the complete suite only in `VERIFY-003`.

### Source Conflicts and Gaps

No unresolved behavioral conflict was found. The project is a CLI interpreter; no persistence, authentication, external service, or deployment platform is required by the sources. The display name and short description are proposed for Commander confirmation.

## Analysis Notes
generated: 2026-08-16
blueprint: /mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260817.024254/workspace/targets/jq/blueprint

Quality: Questions
  blockers: 0
  questions: 1
  features: 6
  stories: 18
  stack: Python standard library
  display_name: jq Interpreter
  short_description: A standalone Python interpreter for the jq language that reads JSON from stdin and emits filtered JSON values.

No blockers. One identity questionnaire remains open.
