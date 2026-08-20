# Blueprint Analysis: drydock jq Uat Case

## Commander Expectations

- assert the completed jq interpreter passes the supplied jq 1.8.2 conformance corpus through the provided scoring entry point.
- assert the deliverable is a standalone executable named `jq` with no third-party runtime dependency or network access.

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
| FRONTEND-001 | Implement jq lexer | jq source is tokenized according to the supplied lexer specification, including comments, literals, strings, interpolation, formats, identifiers, bindings, and operators. |
| FRONTEND-002 | Implement jq parser and AST | Valid jq programs produce an AST with the specified precedence, associativity, bindings, definitions, patterns, modules, and control forms. |
| FRONTEND-003 | Implement compile diagnostics | Invalid jq programs exit `3`; valid module grammar errors are rejected without filesystem access. |

### Feature: Generator Evaluation Core

| ID | Story | High-level AC |
|---|---|---|
| CORE-001 | Implement stream-valued filter evaluation | Filters produce ordered zero-, one-, or many-value streams, and pipelines execute downstream filters once per upstream output. |
| CORE-002 | Implement literals, indexing, iteration, construction, and operators | Identity, literals, field/index access, slices, iteration, arrays, objects, arithmetic, comparison, and boolean operators follow jq semantics. |
| CORE-003 | Implement errors, optional evaluation, and alternatives | `empty`, `try`, `catch`, `?`, `//`, runtime errors, and partial output behavior follow the interface contract. |
| CORE-004 | Implement generator utilities | `range`, `while`, `until`, `repeat`, `first`, `last`, `nth`, `limit`, `skip`, `any`, `all`, `combinations`, and `transpose` preserve generator backtracking and short-circuiting. |

### Feature: Paths and Assignment

| ID | Story | High-level AC |
|---|---|---|
| PATHS-001 | Implement path discovery and traversal | `path`, `paths`, `getpath`, and path expressions produce and consume the specified array/string paths. |
| PATHS-002 | Implement path mutation | `setpath`, `delpaths`, `del`, and nested path creation/deletion handle arrays, objects, slices, invalid paths, and depth limits. |
| PATHS-003 | Implement assignment operators | `=`, `|=`, `+=`, `-=`, `*=`, `/=`, `%=`, and `//=` apply jq's immutable assignment semantics, including multi-path and generator behavior. |

### Feature: Control Flow and Bindings

| ID | Story | High-level AC |
|---|---|---|
| CONTROL-001 | Implement conditionals and labels | `if`, `then`, `elif`, `else`, `end`, `label`, and `break` implement jq truthiness, branching, and lexical break behavior. |
| CONTROL-002 | Implement reductions and foreach | `reduce` and `foreach` bind patterns, process generator outputs in order, and expose the correct accumulator and extracted streams. |
| CONTROL-003 | Implement variables and destructuring | `as`, lexical variable scope, array/object patterns, closures, and destructuring alternatives bind values as specified. |
| CONTROL-004 | Implement user-defined functions | `def` supports arities, filter and value parameters, recursive calls, lexical definitions, redefinition, and generator-valued arguments. |

### Feature: Standard Library and Runtime Services

| ID | Story | High-level AC |
|---|---|---|
| BUILTINS-001 | Implement type, collection, and structural builtins | Type predicates, `length`, `keys`, `has`, `contains`, `inside`, `map`, `map_values`, `add`, flattening, sorting, grouping, uniqueness, entries, walking, and related builtins pass their specified behavior. |
| BUILTINS-002 | Implement string and encoding builtins | String trimming, splitting, joining, case conversion, explode/implode, JSON conversion, URI/HTML/CSV/TSV/shell/base64 formats, and interpolation behave as specified. |
| BUILTINS-003 | Implement regular-expression builtins | `test`, `match`, `capture`, `scan`, `split`, `splits`, `sub`, and `gsub` support the corpus's regex modes, captures, offsets, and generator behavior using the standard library. |
| BUILTINS-004 | Implement date, math, numeric, and special-value builtins | Date/time functions, math functions, numeric conversion, infinities, NaN, numeric comparison, and `have_decnum` behavior satisfy the supplied specification and corpus. |
| BUILTINS-005 | Implement streaming and SQL-style builtins | `tostream`, `fromstream`, `truncate_stream`, `INDEX`, `JOIN`, and `IN` implement the documented stream and lookup semantics. |
| BUILTINS-006 | Implement environment and I/O builtins | `input`, `inputs`, `debug`, `stderr`, `env`, `$ENV`, `$__loc__`, and related runtime values follow the documented interface. |

### Feature: Executable and Conformance Delivery

| ID | Story | High-level AC |
|---|---|---|
| DELIVERY-001 | Provide the jq executable interface | An executable root-level `jq` accepts `-c PROGRAM`, reads JSON values from stdin, emits compact JSON values one per line, and uses the specified exit codes. |
| DELIVERY-002 | Stage and preserve conformance assets | The supplied sources, corpus, exclusions, and harness are staged at the required paths without modification, and declared exclusions remain auditable. |
| DELIVERY-003 | Document operation and verification | `README.md` documents stdin/stdout behavior, exit codes, and `sh sources/full_test.sh`. |
| DELIVERY-004 | Pass the complete conformance suite | The terminal verification runs the unfiltered supplied corpus and every non-excluded case passes with no failures or errors. |

## Story Guidance

Named stories planning must produce. Authoritative record: `STORY_GUIDANCE.json`.

| Story ID | Provenance | Gate | Note |
|---|---|---|---|
| FRONTEND-001 | plan | `python3 sources/run_conformance.py --jq ./jq --select ^(true|false|null|[-0-9]|\.|@|def|module|include|%::)` | Lexer specification in sources/lexer.l and parser corpus cases in sources/jq.test. |
| FRONTEND-002 | plan | `python3 sources/run_conformance.py --jq ./jq --select (\.|\[|\{|\(|if|try|reduce|foreach|def| as |module|include)` | Grammar and precedence in sources/parser.y. |
| CORE-001 | plan | `python3 sources/run_conformance.py --jq ./jq --select (\.|\.\[\]|,|\||empty)` | Generator model required by sources/INSTRUCTIONS.md and sources/jq-manual.txt. |
| CORE-002 | plan | `python3 sources/run_conformance.py --jq ./jq --select (\+|-|\*|/|%|==|!=|<|>|\[|\{|\.[])` | Basic filters, values, construction, indexing, and operators. |
| CORE-003 | plan | `python3 sources/run_conformance.py --jq ./jq --select (try|catch|\?|//|error|empty)` | Error suppression and alternative semantics. |
| CORE-004 | plan | `python3 sources/run_conformance.py --jq ./jq --select (range|while|until|repeat|first|last|nth|limit|skip|any|all|combinations|transpose)` | Generator utilities defined in sources/builtin.jq and the manual. |
| PATHS-001 | plan | `python3 sources/run_conformance.py --jq ./jq --select (path|paths|getpath)` | Path evaluation sections in sources/jq-manual.txt and path corpus cases. |
| PATHS-002 | plan | `python3 sources/run_conformance.py --jq ./jq --select (setpath|delpaths|del\()` | Path mutation definitions and regression cases. |
| PATHS-003 | plan | `python3 sources/run_conformance.py --jq ./jq --select (=|\|=|\+=|-=|\*=|/=|%=|//=)` | Assignment sections in sources/parser.y and sources/jq-manual.txt. |
| CONTROL-001 | plan | `python3 sources/run_conformance.py --jq ./jq --select (if|label|break|and|or|not)` | Conditionals and lexical labels. |
| CONTROL-002 | plan | `python3 sources/run_conformance.py --jq ./jq --select (reduce|foreach)` | Reduction and foreach grammar and examples. |
| CONTROL-003 | plan | `python3 sources/run_conformance.py --jq ./jq --select ( as \$|\?//|\[\$|\{\$)` | Variables, patterns, and destructuring alternatives. |
| CONTROL-004 | plan | `python3 sources/run_conformance.py --jq ./jq --select ^def ` | Function definitions, arities, closures, and recursion. |
| BUILTINS-001 | plan | `python3 sources/run_conformance.py --jq ./jq --select (map|sort|group_by|unique|entries|flatten|contains|inside|walk|keys|length)` | Collection and structural builtins from sources/builtin.jq and the manual. |
| BUILTINS-002 | plan | `python3 sources/run_conformance.py --jq ./jq --select (@|split|join|trim|explode|implode|tostring|tojson|fromjson|ascii_)` | String and format builtin sections. |
| BUILTINS-003 | plan | `python3 sources/run_conformance.py --jq ./jq --select (test|match|capture|scan|sub|gsub|splits)` | Regular-expression builtin sections. |
| BUILTINS-004 | plan | `python3 sources/run_conformance.py --jq ./jq --select (date|time|strftime|strptime|mktime|sin|cos|sqrt|pow|nan|infinite|decnum|tonumber)` | Dates, math, numeric edge cases, and special values. |
| BUILTINS-005 | plan | `python3 sources/run_conformance.py --jq ./jq --select (stream|tostream|fromstream|truncate_stream|INDEX|JOIN|IN\()` | Streaming and SQL-style builtin sections. |
| BUILTINS-006 | plan | `python3 sources/run_conformance.py --jq ./jq --select (input|inputs|debug|stderr|env|ENV|__loc__)` | I/O and environment builtin sections. |
| DELIVERY-001 | plan | `python3 sources/run_conformance.py --jq ./jq --select ^\.$` | Executable protocol defined by sources/INSTRUCTIONS.md and sources/full_test.sh. |
| DELIVERY-004 | plan | — | Terminal acceptance uses the complete supplied suite through sources/full_test.sh. |

## Surfaced Acceptance Criteria

| ID | Story ID | Criterion |
|---|---|---|
| AC-001 | DELIVERY-001 | The executable returns exit `3` for compilation errors, exit `5` for runtime errors, and preserves outputs emitted before a runtime error. |
| AC-002 | FRONTEND-001 | Lexer behavior preserves embedded Unicode whitespace and newline handling required by the corpus. |
| AC-003 | BUILTINS-004 | Numeric handling preserves unmodified literals where required while arithmetic uses native floating-point behavior and `have_decnum` selects the supported branch. |
| AC-004 | DELIVERY-002 | Imported scoring assets are not modified, filtered, skipped, or reinterpreted by the implementation. |
| AC-005 | DELIVERY-001 | The executable does not require command-line options beyond `-c` for the scored interface. |

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
| `sources/lexer.l` | parser-to-normalizer | `sources/parser.y` | Lexer tokens are consumed by the grammar. | Lexer precedes parser implementation. |
| `sources/parser.y` | instruction-to-test | `sources/jq.test` | Grammar and precedence cases exercise front-end behavior. | Parser stories require scoped corpus slices. |
| `sources/jq-manual.txt` | reference-to-replacement | `FRONTEND`, `CORE`, `PATHS`, `CONTROL`, `BUILTINS` | Manual defines language and builtin semantics. | Each implementation story uses the manual as normative context. |
| `sources/builtin.jq` | reference-to-replacement | `BUILTINS`, `PATHS`, `CONTROL` | Upstream jq definitions specify higher-level builtin behavior. | Builtins depend on the generator and assignment core. |
| `sources/jq.test` | test-kit-to-implementation | All implementation stories | Corpus contains syntax, semantics, error, and regression cases. | Slices provide story-scoped acceptance; full suite is terminal. |
| `sources/run_conformance.py` | instruction-to-test | `sources/full_test.sh` | Runner executes one subprocess per corpus case and applies exclusions. | Harness must be staged and invoked unchanged. |
| `sources/full_test.sh` | dependency | `DELIVERY-004` | Shell entry point verifies executable presence and launches the runner. | Final acceptance runs this command exactly. |
| `sources/exclusions.txt` | test-kit-to-implementation | `sources/jq.test` | Exclusions identify module-loader cases by exact program text. | Only declared loader cases are skipped. |

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

The system is a standalone command-line jq interpreter. It consumes jq filter programs and newline-delimited JSON input on stdin, evaluates filters as ordered value streams, and emits compact JSON values on stdout. The build flow is lexer/parser, generator runtime, paths and assignment, control/bindings, builtins, executable wrapper, then scoped corpus verification followed by one complete-suite gate.

### Story Realization Map

| Story ID | Durable scope | Evidence | Related files | Delivery kind |
|---|---|---|---|---|
| FRONTEND-001 | Lexer/tokenizer | `sources/lexer.l` | `sources/jq.test` | capability |
| FRONTEND-002 | Parser and AST | `sources/parser.y` | `sources/lexer.l`, `sources/jq.test` | capability |
| FRONTEND-003 | Compile errors | `sources/parser.y`, `sources/jq.test` | `sources/run_conformance.py` | capability, acceptance contract |
| CORE-001 | Stream evaluator | `sources/INSTRUCTIONS.md`, `sources/jq-manual.txt` | `sources/jq.test` | capability |
| CORE-002 | Core expressions | `sources/jq-manual.txt`, `sources/parser.y` | `sources/jq.test` | capability |
| CORE-003 | Errors and alternatives | `sources/jq-manual.txt` | `sources/jq.test` | capability |
| CORE-004 | Generator controls | `sources/builtin.jq`, `sources/jq-manual.txt` | `sources/jq.test` | capability |
| PATHS-001 | Path evaluation | `sources/jq-manual.txt`, `sources/parser.y` | `sources/jq.test` | capability |
| PATHS-002 | Path mutation | `sources/jq-manual.txt`, `sources/builtin.jq` | `sources/jq.test` | capability |
| PATHS-003 | Assignment | `sources/parser.y`, `sources/jq-manual.txt` | `sources/jq.test` | capability |
| CONTROL-001 | Conditionals and labels | `sources/parser.y`, `sources/jq-manual.txt` | `sources/jq.test` | capability |
| CONTROL-002 | Reduce/foreach | `sources/parser.y`, `sources/jq-manual.txt` | `sources/jq.test` | capability |
| CONTROL-003 | Bindings/patterns | `sources/parser.y`, `sources/jq-manual.txt` | `sources/jq.test` | capability |
| CONTROL-004 | Functions | `sources/parser.y`, `sources/jq-manual.txt` | `sources/builtin.jq`, `sources/jq.test` | capability |
| BUILTINS-001 | Structural builtins | `sources/builtin.jq`, `sources/jq-manual.txt` | `sources/jq.test` | capability |
| BUILTINS-002 | Strings/formats | `sources/builtin.jq`, `sources/jq-manual.txt` | `sources/jq.test` | capability |
| BUILTINS-003 | Regex | `sources/builtin.jq`, `sources/jq-manual.txt` | `sources/jq.test` | capability |
| BUILTINS-004 | Dates/math/numbers | `sources/jq-manual.txt`, `sources/builtin.jq` | `sources/jq.test` | capability |
| BUILTINS-005 | Streaming/SQL builtins | `sources/builtin.jq`, `sources/jq-manual.txt` | `sources/jq.test` | capability |
| BUILTINS-006 | I/O/environment | `sources/jq-manual.txt` | `sources/jq.test` | capability |
| DELIVERY-001 | Root executable and protocol | `sources/INSTRUCTIONS.md`, `sources/full_test.sh` | `README.md` | capability, acceptance contract |
| DELIVERY-002 | Asset staging | `sources/INSTRUCTIONS.md`, `sources/run_conformance.py` | all staged sources | integration |
| DELIVERY-003 | README | `sources/INSTRUCTIONS.md` | `README.md` | acceptance contract |
| DELIVERY-004 | Full verification | `sources/full_test.sh`, `sources/run_conformance.py` | all implementation stories | test harness, acceptance contract |

### Test and Acceptance Strategy

Every implementation story uses `sources/run_conformance.py` with `--jq ./jq` and a selector matching its construct. No intermediate story invokes the unscoped suite. `DELIVERY-004` is the sole terminal full-suite story and uses `Suite: full` with `sh sources/full_test.sh`; it depends on all implementation stories. The complete-suite requirement is proven by the harness exit status, not by asserting a hard-coded case count.

### Sequencing and Dependencies

Stage all runtime assets before acceptance. Build the lexer before the parser, the parser before evaluation, the generator core before paths and control flow, and paths before assignment. Implement functions and builtins after the evaluator supports filters as generators. Provide the executable before invoking any runner. Run scoped corpus slices after each relevant story, then run the full suite exactly once at the terminal gate.

### Source Conflicts and Gaps

No unresolved cross-source conflict prevents a coherent plan. The manual's descriptive numeric wording is reconciled by the explicit implementation instructions requiring native floats and the non-decnum branch. Module-loader cases are explicitly excluded; module grammar cases remain in scope.

## Analysis Notes
generated: 2026-08-20
blueprint: /mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260820.223834/workspace/targets/jq/blueprint

Quality: Ready
  blockers: 0
  questions: 0
  features: 6
  stories: 24
  stack: Python with standard library only; executable interface named jq
  display_name: not proposed
  short_description: not proposed

No blockers or open human-owned questions. The project type is `cli`. All imported source assets have explicit roles and staging dispositions.
