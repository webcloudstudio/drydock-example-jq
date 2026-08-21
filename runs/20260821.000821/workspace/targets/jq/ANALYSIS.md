# Blueprint Analysis: Drydock jq Uat Case

## Commander Expectations

- assert the project delivers a real jq 1.8.2 language interpreter exposed as an executable named `jq`.
- assert the interpreter passes every non-excluded case in the supplied upstream conformance corpus.
- assert the implementation remains self-contained, auditable, and free of third-party jq implementations or system-jq delegation.

## Crew

| Crew | Charge |
|---|---|
| Commander | Defines intent and decides what done means. |
| Team Lead | Confirms epic completeness and stakeholder expectations. |
| Planning Crew | Authors atomic specifications and the ordered Manifest. |
| Shipyard Crew | Builds the tickets without synchronous Commander access. |

## Story List

### Feature: Project Foundation and Executable Contract

| ID | Story | High-level AC |
|---|---|---|
| FOUNDATION-001 | Stage the pinned jq source and scoring assets | All required source, corpus, harness, exclusion, grammar, lexer, and reference files are available under `sources/` without modification. |
| FOUNDATION-002 | Implement the executable jq entry point | An executable named `jq` accepts `-c`, reads JSON values from stdin, writes compact JSON values one per line, and returns the documented exit codes. |
| FOUNDATION-003 | Document the project interface | `README.md` documents stdin/stdout behavior, exit codes, and `sh sources/full_test.sh`. |

### Feature: Lexer, Parser, and Program Definitions

| ID | Story | High-level AC |
|---|---|---|
| FRONTEND-001 | Implement jq lexical scanning | Identifiers, bindings, literals, strings, interpolation, formats, comments, operators, delimiters, and invalid characters are tokenized according to `sources/lexer.l`. |
| FRONTEND-002 | Implement jq expression parsing | The parser produces an AST with the precedence, associativity, suffix, collection, object, conditional, error, and assignment forms defined by `sources/parser.y`. |
| FRONTEND-003 | Implement compile-time rejection | Invalid programs, including module grammar errors and undefined bindings or labels, exit with code `3`. |
| FRONTEND-004 | Implement user-defined functions and lexical scope | `def`, filter arguments, value arguments, closures, recursion, redefinition, and lexical binding scope behave according to the manual and corpus. |
| FRONTEND-005 | Implement destructuring and `?//` alternatives | Array/object patterns, missing-value bindings, alternative patterns, and fallback behavior work for both successful and failing alternatives. |

### Feature: Generator Evaluation Core

| ID | Story | High-level AC |
|---|---|---|
| CORE-001 | Implement stream-based filter evaluation | Every filter evaluates as a stream of zero or more values, with correct backtracking and downstream execution for generators. |
| CORE-002 | Implement basic filters and constructors | Identity, literals, comma, pipe, arrays, objects, field access, indexing, iteration, slices, recursive descent, and `empty` produce the required streams. |
| CORE-003 | Implement arithmetic, comparison, and boolean operators | Operators implement jq type semantics, cartesian argument evaluation, ordering, truthiness, short-circuiting, and runtime errors. |
| CORE-004 | Implement error handling and control flow | `if`, `elif`, `else`, `try`, `catch`, `?`, `//`, labels, breaks, and runtime exit behavior preserve outputs produced before an error. |

### Feature: Paths and Immutable Updates

| ID | Story | High-level AC |
|---|---|---|
| PATHS-001 | Implement path discovery and access | `path`, `paths`, `getpath`, and path expressions return or access the correct array/object paths, including missing values and invalid-path errors. |
| PATHS-002 | Implement path mutation and deletion | `setpath`, `delpaths`, `del`, indexing updates, slice updates, and nested creation/deletion follow jq's immutable value semantics. |
| PATHS-003 | Implement assignment operators | `=`, `|=`, `+=`, `-=`, `*=`, `/=`, `%=`, and `//=` support multi-path updates, generator RHS behavior, and deletion through `empty`. |

### Feature: Reduction and Recursive Control

| ID | Story | High-level AC |
|---|---|---|
| CONTROL-001 | Implement reductions and iteration | `reduce`, `foreach`, `limit`, `skip`, `first`, `last`, and `nth` preserve generator order and accumulator semantics. |
| CONTROL-002 | Implement recursive generators | `while`, `until`, `repeat`, `recurse`, and combinations support recursive streams without losing required outputs or termination behavior. |
| CONTROL-003 | Implement generator predicates and collection utilities | `any`, `all`, `isempty`, combinations, ranges, transpose, and related generator utilities evaluate the required streams and short-circuit cases. |

### Feature: Builtin Language Library

| ID | Story | High-level AC |
|---|---|---|
| BUILTINS-001 | Implement type, structural, and collection builtins | Type selectors, length, keys, containment, entries, mapping, flattening, sorting, grouping, uniqueness, joins, and related builtins match jq semantics. |
| BUILTINS-002 | Implement string and Unicode builtins | String trimming, splitting, joining, case conversion, explode/implode, indices, substring operations, and Unicode behavior conform to the corpus. |
| BUILTINS-003 | Implement regular-expression builtins | `test`, `match`, `capture`, `scan`, `split`, `splits`, `sub`, and `gsub` support the corpus's regex modes, captures, offsets, and replacement streams. |
| BUILTINS-004 | Implement format and JSON conversion builtins | `tostring`, `tonumber`, `toboolean`, `tojson`, `fromjson`, `@text`, `@json`, `@html`, `@uri`, `@urid`, `@csv`, `@tsv`, `@sh`, `@base64`, and `@base64d` conform. |
| BUILTINS-005 | Implement date and math builtins | Date conversion, broken-down time functions, standard math functions, numeric predicates, and floating-point edge cases conform to the supplied behavior. |
| BUILTINS-006 | Implement environment, diagnostics, and I/O builtins | `input`, `inputs`, `debug`, `stderr`, `env`, `$ENV`, location metadata, build flags, and builtin introspection behave as specified. |
| BUILTINS-007 | Implement streaming builtins | `tostream`, `fromstream`, `truncate_stream`, and stream reconstruction support the supplied streaming cases. |
| BUILTINS-008 | Implement remaining structural helpers | `walk`, `pick`, `INDEX`, `JOIN`, `IN`, `bsearch`, and related helpers conform to their manual definitions. |

### Feature: Corpus Verification

| ID | Story | High-level AC |
|---|---|---|
| VERIFICATION-001 | Run scoped conformance slices for implemented features | Each implementation feature can be verified through a non-empty `--select` slice of `sources/run_conformance.py`, with no unscoped suite execution before the terminal gate. |
| VERIFICATION-002 | Pass the complete supplied conformance corpus | `sh sources/full_test.sh` exits zero, every runnable supplied case passes, excluded module-loader cases are reported as skips, and no case fails or errors. |

## Story Guidance

Named stories planning must produce. Authoritative record: `STORY_GUIDANCE.json`.

| Story ID | Provenance | Gate | Note |
|---|---|---|---|
| FOUNDATION-001 | plan | — | Build Instructions: source roles and read-only scoring assets |
| FOUNDATION-002 | plan | — | Build Instructions: interface contract |
| FOUNDATION-003 | plan | — | Definition of Done: README requirement |
| FRONTEND-001 | plan | `python3 sources/run_conformance.py --select ^(\.|\[|\{|def|if|try|reduce|foreach|module|include|%::|"|@)` | Suggested implementation order: lexer |
| FRONTEND-002 | plan | `python3 sources/run_conformance.py --select ^(\.|\[|\{|def|if|try|reduce|foreach|module|include|%::|"|@)` | Suggested implementation order: parser and AST |
| FRONTEND-003 | plan | `python3 sources/run_conformance.py --select %%UNMATCHABLE_COMPILE_CASE_SELECTOR%%` | Compile-error corpus cases are selected by their program text in the implementation plan. |
| FRONTEND-004 | plan | `python3 sources/run_conformance.py --select ^def ` | Suggested implementation order: functions, variables, and destructuring |
| FRONTEND-005 | plan | `python3 sources/run_conformance.py --select \?//| as \$| as \[` | Suggested implementation order: destructuring and ?// |
| CORE-001 | plan | `python3 sources/run_conformance.py --select \.|\[|,|empty|range|while|recurse` | Suggested implementation order: generator core |
| CORE-002 | plan | `python3 sources/run_conformance.py --select \.|\[|\{|\.\[|\.\w` | Suggested implementation order: basic filters and constructors |
| CORE-003 | plan | `python3 sources/run_conformance.py --select [+*/%<>=]| and | or |==|!=` | Suggested implementation order: arithmetic and comparison |
| CORE-004 | plan | `python3 sources/run_conformance.py --select if |try |\?| //|label |break ` | Suggested implementation order: control flow and errors |
| PATHS-001 | plan | `python3 sources/run_conformance.py --select path|paths|getpath` | Suggested implementation order: paths |
| PATHS-002 | plan | `python3 sources/run_conformance.py --select setpath|delpaths|del\(` | Suggested implementation order: path mutation and deletion |
| PATHS-003 | plan | `python3 sources/run_conformance.py --select [.]?[^\n]*(\|=|\+=|-=|\*=|/=|%=|//=| = )` | Suggested implementation order: assignment |
| CONTROL-001 | plan | `python3 sources/run_conformance.py --select reduce|foreach|limit|skip|first\(|last\(|nth\(` | Suggested implementation order: reductions and iteration |
| CONTROL-002 | plan | `python3 sources/run_conformance.py --select while|until|repeat|recurse` | Suggested implementation order: recursive control |
| CONTROL-003 | plan | `python3 sources/run_conformance.py --select any|all|isempty|combinations|range|transpose` | Suggested implementation order: generator utilities |
| BUILTINS-001 | plan | `python3 sources/run_conformance.py --select map|select|sort|group_by|unique|contains|keys|entries|flatten|join` | Builtin definitions and manual: structural and collection builtins |
| BUILTINS-002 | plan | `python3 sources/run_conformance.py --select split|trim|explode|implode|indices|ascii_|startswith|endswith` | Manual: string and Unicode builtins |
| BUILTINS-003 | plan | `python3 sources/run_conformance.py --select test\(|match\(|capture\(|scan\(|sub\(|gsub\(` | Manual: regular expressions |
| BUILTINS-004 | plan | `python3 sources/run_conformance.py --select @|tojson|fromjson|tostring|tonumber|toboolean` | Manual: format strings and JSON conversion |
| BUILTINS-005 | plan | `python3 sources/run_conformance.py --select date|strftime|strptime|mktime|gmtime|pow\(|sin|cos|sqrt|floor` | Manual: dates and math |
| BUILTINS-006 | plan | `python3 sources/run_conformance.py --select input|inputs|debug|stderr|env|\$ENV|\$__loc__|builtins` | Manual: I/O and diagnostics |
| BUILTINS-007 | plan | `python3 sources/run_conformance.py --select tostream|fromstream|truncate_stream` | Manual: streaming |
| BUILTINS-008 | plan | `python3 sources/run_conformance.py --select walk|pick|INDEX|JOIN|IN\(|bsearch` | Builtin definitions and manual: remaining helpers |
| VERIFICATION-001 | plan | `python3 sources/run_conformance.py --select reduce|foreach|recurse|path|def|map|split|test|@` | Instructions: every non-terminal story uses a scoped, executing corpus slice |
| VERIFICATION-002 | plan | `sh sources/full_test.sh` | Sea Trial st-001 and Definition of Done: complete supplied corpus |

## Surfaced Acceptance Criteria

| ID | Story ID | Criterion |
|---|---|---|
| AC-001 | FOUNDATION-002 | The executable shall distinguish compile failures with exit `3` from runtime failures with exit `5`, while preserving values emitted before a runtime failure. |
| AC-002 | FOUNDATION-001 | The scoring assets shall remain byte-for-byte supplied inputs; exclusions shall be auditable and hash-verifiable. |
| AC-003 | VERIFICATION-001 | Every non-terminal conformance invocation shall use a non-empty `--select` expression that executes cases rather than merely listing them. |
| AC-004 | VERIFICATION-002 | The terminal verification shall be the only unscoped corpus execution and shall assert the harness exit status rather than a hard-coded case count. |
| AC-005 | FOUNDATION-002 | The command-line interface shall require only the exercised `-c` option and shall communicate through stdin, stdout, and stderr as specified. |

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
| `sources/lexer.l` | parser-to-normalizer | `sources/parser.y` | Lexer tokens and parser token declarations define the frontend contract. | Build lexer and parser together before evaluation. |
| `sources/parser.y` | implementation-to-helper | `sources/jq-manual.txt` | Grammar defines syntax while the manual defines observable semantics. | AST and evaluator specifications must be reconciled against both sources. |
| `sources/builtin.jq` | reference implementation | `sources/jq-manual.txt` | Builtin definitions provide executable jq-level semantics for many functions. | Implement core generator behavior before loading or reproducing builtin semantics. |
| `sources/jq.test` | test-kit-to-implementation | `jq` executable | The corpus supplies program, input, and expected output cases. | Each feature owns scoped corpus slices; the final story runs the complete corpus. |
| `sources/run_conformance.py` | instruction-to-test | `sources/jq.test` | The runner parses cases, applies exclusions, invokes `jq`, and compares structural JSON values. | Stage the runner and corpus unchanged and use its exit code as the verdict. |
| `sources/full_test.sh` | instruction-to-test | `sources/run_conformance.py` | The shell script performs the executable check and invokes the unfiltered runner. | Preserve the script except for any necessary staged-path correction. |
| `sources/exclusions.txt` | dependency | `sources/jq.test` | Exclusions identify module-loader cases that cannot be carried by the flat kit. | Verify every exclusion matches a corpus case and report skips transparently. |
| `sources/INSTRUCTIONS.md` | author intent | all implementation stories | Instructions define implementation order, prohibitions, interface, and delivery constraints. | Treat as project orientation; do not stage it as a runtime asset. |

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

The product is a standalone CLI filter executable. It reads one or more JSON values from stdin, evaluates a jq program supplied with `-c`, and emits a stream of compact JSON values on stdout. The implementation consists of a lexer, parser/AST, stream evaluator, immutable path/update engine, builtin library, CLI wrapper, and staged conformance harness. The required flow is parse and compile the program, evaluate it against stdin as a generator, serialize each output, and return the documented status.

### Story Realization Map

| Story ID | Blueprint scope | Evidence | Related files | Delivery kind |
|---|---|---|---|---|
| FOUNDATION-001 | Source staging and provenance | `sources/INSTRUCTIONS.md` source-role table | all staged `sources/*` files | acceptance contract |
| FOUNDATION-002 | CLI process and JSON stream boundary | `sources/INSTRUCTIONS.md` interface contract | `jq` and evaluator package | capability |
| FOUNDATION-003 | Project handoff documentation | `sources/INSTRUCTIONS.md` Definition of Done | `README.md` | acceptance contract |
| FRONTEND-001 | Lexer | `sources/lexer.l` | lexer implementation | capability |
| FRONTEND-002 | Parser and AST | `sources/parser.y` | parser, AST types | capability |
| FRONTEND-003 | Compile errors and static validation | `sources/parser.y`, `sources/jq.test` | compiler diagnostics | capability |
| FRONTEND-004 | Definitions and scope | `sources/parser.y`, `sources/jq-manual.txt`, `sources/builtin.jq` | function environment | capability |
| FRONTEND-005 | Patterns and alternation | `sources/parser.y`, `sources/jq-manual.txt`, `sources/jq.test` | pattern matcher and bindings | capability |
| CORE-001 | Stream evaluator | `sources/INSTRUCTIONS.md`, `sources/jq-manual.txt` | evaluator runtime | capability |
| CORE-002 | Core expressions and constructors | `sources/parser.y`, `sources/jq.test` | evaluator and value model | capability |
| CORE-003 | Operators and comparisons | `sources/jq-manual.txt`, `sources/jq.test` | operator library | capability |
| CORE-004 | Control and errors | `sources/jq-manual.txt`, `sources/builtin.jq`, `sources/jq.test` | runtime error and control machinery | capability |
| PATHS-001 | Path reads and discovery | `sources/jq-manual.txt`, `sources/jq.test` | path engine | capability |
| PATHS-002 | Immutable path mutation | `sources/jq-manual.txt`, `sources/jq.test` | update engine | capability |
| PATHS-003 | Assignment forms | `sources/parser.y`, `sources/jq-manual.txt` | assignment evaluator | capability |
| CONTROL-001 | Reductions and bounded streams | `sources/builtin.jq`, `sources/jq.test` | reducer runtime | capability |
| CONTROL-002 | Recursive controls | `sources/builtin.jq`, `sources/jq.test` | recursive evaluator | capability |
| CONTROL-003 | Generator utilities | `sources/builtin.jq`, `sources/jq.test` | builtin library | capability |
| BUILTINS-001 | Structural builtins | `sources/builtin.jq`, `sources/jq-manual.txt` | builtin library | capability |
| BUILTINS-002 | String and Unicode builtins | `sources/jq-manual.txt`, `sources/jq.test` | builtin library | capability |
| BUILTINS-003 | Regex builtins | `sources/jq-manual.txt`, `sources/jq.test` | regex builtin module | capability |
| BUILTINS-004 | Formatting and JSON builtins | `sources/jq-manual.txt`, `sources/jq.test` | serialization and format module | capability |
| BUILTINS-005 | Date and math builtins | `sources/jq-manual.txt`, `sources/jq.test` | standard-library builtin module | capability |
| BUILTINS-006 | Environment and I/O builtins | `sources/jq-manual.txt`, `sources/jq.test` | process/runtime integration | integration |
| BUILTINS-007 | Streaming builtins | `sources/jq-manual.txt`, `sources/jq.test` | stream conversion module | capability |
| BUILTINS-008 | Remaining helpers | `sources/builtin.jq`, `sources/jq.test` | builtin library | capability |
| VERIFICATION-001 | Scoped corpus verification | `sources/run_conformance.py`, `sources/jq.test` | story acceptance commands | test harness |
| VERIFICATION-002 | Full corpus gate | `sources/full_test.sh`, `sources/run_conformance.py`, `sources/exclusions.txt` | terminal acceptance | acceptance contract |

### Test and Acceptance Strategy

Implementation stories use focused unit and integration tests plus a non-empty `--select` expression against the relevant corpus cases. The runner's `--list` mode is reserved for planning and corpus-shape inspection, not behavioral acceptance. The terminal verification story is the only story that runs the complete corpus and declares `Suite: full`; it depends on every implementation story and proves the existing Sea Trial through the harness exit status.

### Sequencing and Dependencies

Stage all read-only scoring assets first. Build the lexer before the parser, the parser before AST evaluation, and the stream evaluator before paths, assignment, control flow, or builtins. Implement the core value and generator model before jq-defined builtins. Build path operations before assignment and reductions. Run scoped corpus slices after each feature area. Run the unfiltered `sources/full_test.sh` only in `VERIFICATION-002`. The runtime uses Python standard-library facilities and does not require network access, package installation, or external services.

### Source Conflicts and Gaps

No unresolved cross-source conflicts or blockers were identified. The sources consistently define a Python, standard-library implementation exposed through an executable `jq`, with the supplied harness as the acceptance authority. Authentication, persistence, web UI, external services, and deployment infrastructure are not part of this CLI product.

## Analysis Notes
generated: 2026-08-20
blueprint: /mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260821.000821/workspace/targets/jq/blueprint

Quality: Ready
  blockers: 0
  questions: 0
  features: 7
  stories: 28
  stack: Python with no third-party runtime dependency; POSIX sh harness
  display_name: not proposed
  short_description: not proposed

Project type: cli. No non-conformant headers or ambiguous signals.
