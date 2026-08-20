# Blueprint Analysis: drydock jq Uat Case

## Commander Expectations

- assert a standards-compliant jq interpreter is delivered as an executable named `jq`.
- assert the supplied jq 1.8.2 conformance corpus passes completely, with declared exclusions remaining auditable.
- assert the implementation uses Python standard-library capabilities without third-party jq implementations or a system jq dependency.

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
| FRONTEND-001 | Implement jq lexer | jq source tokens, strings, interpolation, comments, escapes, identifiers, and formats are recognized according to the supplied lexer specification. |
| FRONTEND-002 | Build jq parser and AST | jq programs are parsed with the supplied precedence, associativity, expressions, patterns, definitions, modules, and control syntax. |
| FRONTEND-003 | Provide compile-time diagnostics | Invalid programs, including all supplied `%%FAIL` cases, exit with compile status 3. |

### Feature: Generator Evaluation Core

| ID | Story | High-level AC |
|---|---|---|
| CORE-001 | Implement stream-valued filter evaluation | Every filter evaluates as an ordered stream supporting zero, one, or multiple outputs. |
| CORE-002 | Implement composition and cartesian evaluation | Pipes, commas, literals, field access, iteration, operators, and function arguments preserve jq backtracking and cartesian semantics. |
| CORE-003 | Implement collection and construction filters | Array and object construction collect and combine generator outputs in jq order. |

### Feature: Paths and Assignment

| ID | Story | High-level AC |
|---|---|---|
| PATHS-001 | Implement path navigation and mutation primitives | `path`, `getpath`, `setpath`, `delpaths`, indexing, slicing, and deletion follow jq path semantics. |
| PATHS-002 | Implement assignment operators | Plain, update, arithmetic, and defined-or assignments modify selected paths with jq’s output and deletion behavior. |

### Feature: Control Flow

| ID | Story | High-level AC |
|---|---|---|
| CONTROL-001 | Implement conditionals and boolean operators | `if`, `elif`, `else`, `and`, `or`, `not`, and `//` implement jq truthiness and generator behavior. |
| CONTROL-002 | Implement errors, try, catch, and optional filters | Runtime errors, catches, `?`, `error`, `halt`, and `halt_error` produce the required outputs and statuses. |
| CONTROL-003 | Implement reductions and iteration controls | `reduce`, `foreach`, `range`, `limit`, `skip`, `first`, `last`, `nth`, `while`, `until`, and `repeat` preserve stream semantics. |
| CONTROL-004 | Implement labels, breaks, and recursion | `label`, `break`, `recurse`, and recursive user filters terminate and backtrack as specified. |

### Feature: Functions and Bindings

| ID | Story | High-level AC |
|---|---|---|
| FUNCTIONS-001 | Implement lexical variable bindings | `as` bindings, scopes, closures, and destructuring patterns bind values with jq’s lexical rules. |
| FUNCTIONS-002 | Implement user-defined functions | `def` supports recursive definitions, filter arguments, value arguments, arity, redefinition, and lexical scoping. |
| FUNCTIONS-003 | Implement destructuring alternatives | `?//` alternatives select matching patterns and expose the required null bindings and fallback behavior. |

### Feature: Built-in Library

| ID | Story | High-level AC |
|---|---|---|
| BUILTINS-001 | Implement type, conversion, and predicate builtins | Type inspection, JSON conversion, numeric/string/boolean conversion, predicates, containment, and environment primitives conform to the manual. |
| BUILTINS-002 | Implement collection and object builtins | Sorting, grouping, uniqueness, mapping, entries, joins, flattening, combinations, transpose, paths, and containment match the corpus. |
| BUILTINS-003 | Implement string, format, and regex builtins | String operations, interpolation, regex matching, substitution, splitting, and `@` formats produce the specified streams and values. |
| BUILTINS-004 | Implement date and time builtins | Date parsing, formatting, epoch conversion, and broken-down time operations satisfy supplied cases. |
| BUILTINS-005 | Implement streaming, I/O, debugging, and SQL-style builtins | `input`, `inputs`, debug/stderr behavior, stream conversion, `walk`, `INDEX`, `JOIN`, and `IN` conform to the supplied definitions. |

### Feature: Numbers and Edge Cases

| ID | Story | High-level AC |
|---|---|---|
| NUMBERS-001 | Implement jq numeric arithmetic and ordering | Arithmetic, modulo, numeric comparison, IEEE-compatible special values, math functions, and numeric formatting behave as required. |
| NUMBERS-002 | Handle numeric, Unicode, depth, and boundary cases | Large literals, NaN/infinity, Unicode codepoints, deep structures, invalid indices, and boundary errors match the corpus. |

### Feature: Executable Delivery and Verification

| ID | Story | High-level AC |
|---|---|---|
| DELIVERY-001 | Deliver the executable jq interface | An executable root-level `jq` accepts `-c`, reads JSON values from stdin, emits compact JSON values one per line, and returns the documented statuses. |
| DELIVERY-002 | Stage the supplied verification assets and document operation | The supplied sources remain available under `sources/`, remain unmodified, and `README.md` documents the interface, exit codes, and full verification command. |
| DELIVERY-003 | Run the complete conformance gate | The terminal verification runs `sh sources/full_test.sh` unfiltered and succeeds for every non-excluded corpus case. |

## Story Guidance

Named stories planning must produce. Authoritative record: `STORY_GUIDANCE.json`.

| Story ID | Provenance | Gate | Note |
|---|---|---|---|
| FRONTEND-001 | plan | — | Suggested implementation order: lexer and parser; sources/lexer.l. |
| FRONTEND-002 | plan | — | Suggested implementation order: lexer and parser; sources/parser.y. |
| FRONTEND-003 | plan | `python3 sources/run_conformance.py --select %%FAIL|module|import|include|break|syntax` | Corpus compile-failure cases and module grammar cases. |
| CORE-001 | plan | `python3 sources/run_conformance.py --select \.|empty|,|\[\.\]|\.\[\]` | Generator core and stream semantics. |
| CORE-002 | plan | `python3 sources/run_conformance.py --select \||,|range|cartesian` | Generator composition and backtracking cases. |
| CORE-003 | plan | `python3 sources/run_conformance.py --select ^\[|\{|\[\.\[]` | Array and object collection cases. |
| PATHS-001 | plan | `python3 sources/run_conformance.py --select path|getpath|setpath|delpaths|del\(|\[[^]]*:` | Paths and assignment primitives. |
| PATHS-002 | plan | `python3 sources/run_conformance.py --select \|=|\+=|-=|\*=|/=|%=|//=` | Assignment operator cases. |
| CONTROL-001 | plan | `python3 sources/run_conformance.py --select if |and|or|//|not` | Conditionals and comparisons. |
| CONTROL-002 | plan | `python3 sources/run_conformance.py --select try|catch|error|\?` | Error and optional-filter cases. |
| CONTROL-003 | plan | `python3 sources/run_conformance.py --select reduce|foreach|range|limit|skip|first|last|nth|while|until|repeat` | Control-flow generator cases. |
| CONTROL-004 | plan | `python3 sources/run_conformance.py --select label|break|recurse` | Labels, breaks, and recursion. |
| FUNCTIONS-001 | plan | `python3 sources/run_conformance.py --select  as \$|destructur` | Variables and destructuring. |
| FUNCTIONS-002 | plan | `python3 sources/run_conformance.py --select ^def |def ` | User-defined functions and closures. |
| FUNCTIONS-003 | plan | `python3 sources/run_conformance.py --select \?//` | Destructuring alternatives. |
| BUILTINS-001 | plan | `python3 sources/run_conformance.py --select type|tonumber|tostring|tojson|fromjson|contains|inside|has|keys` | Core type and conversion builtins. |
| BUILTINS-002 | plan | `python3 sources/run_conformance.py --select sort|group_by|unique|map|flatten|transpose|combinations|entries` | Collection and object builtins. |
| BUILTINS-003 | plan | `python3 sources/run_conformance.py --select @|split|join|match|test|capture|scan|sub|gsub|trim` | String, format, and regex builtins. |
| BUILTINS-004 | plan | `python3 sources/run_conformance.py --select date|strftime|strptime|mktime|gmtime|localtime` | Date and time builtins. |
| BUILTINS-005 | plan | `python3 sources/run_conformance.py --select input|inputs|debug|tostream|fromstream|walk|INDEX|JOIN|IN` | I/O, streaming, debugging, and SQL-style builtins. |
| NUMBERS-001 | plan | `python3 sources/run_conformance.py --select pow|log|sin|cos|sqrt|floor|%|infinite|nan|isnan` | Math and special-number cases. |
| NUMBERS-002 | plan | `python3 sources/run_conformance.py --select decnum|literal|deep|depth|NaN|Unicode|65536` | Numeric, Unicode, depth, and boundary cases. |
| DELIVERY-001 | plan | — | Interface contract in sources/INSTRUCTIONS.md. |
| DELIVERY-002 | plan | — | Read-only scoring assets and README requirements in sources/INSTRUCTIONS.md. |
| DELIVERY-003 | plan | `sh sources/full_test.sh` | Terminal complete-suite acceptance gate. |

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
| `sources/lexer.l` | parser-to-normalizer | `sources/parser.y` | Lexer token definitions and parser productions jointly define the front end. | Build lexer behavior before AST parsing and evaluation. |
| `sources/parser.y` | instruction-to-test | `sources/jq.test` | Grammar, precedence, patterns, and syntax failures are exercised by corpus programs. | Front-end stories use scoped corpus slices before downstream features. |
| `sources/jq-manual.txt` | reference-to-replacement | `sources/builtin.jq` | Manual defines behavior; builtin source supplies jq-level reference definitions. | Builtins must be implemented from both normative sources. |
| `sources/jq.test` | test-kit-to-implementation | `jq` | Corpus executes the candidate through the harness. | Every implementation story receives a scoped runner slice. |
| `sources/run_conformance.py` | test-kit-to-implementation | `sources/full_test.sh` | Full test delegates to the conformance runner after checking `./jq`. | Only the terminal delivery story runs the complete corpus. |
| `sources/exclusions.txt` | dependency | `sources/run_conformance.py` | Runner validates exclusion programs and reports skips. | Preserve exclusions and stage them with the harness. |
| `sources/INSTRUCTIONS.md` | instruction-to-test | all implementation stories | Build order, constraints, interface, and acceptance rules are stated there. | Treat as author intent and planning context, not a staged runtime asset. |

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

Deliver a standalone Python implementation exposed through an executable root-level `jq`. It reads JSON from stdin, evaluates a jq filter into an ordered stream, and writes compact JSON values to stdout. The staged corpus and harness provide scoped development verification and one final complete-suite gate.

### Story Realization Map

Each Story ID maps to the corresponding durable scope named by its title. Front-end stories use `sources/lexer.l` and `sources/parser.y`; evaluator, path, control, function, builtin, and numeric stories use `sources/jq-manual.txt`, `sources/builtin.jq`, and scoped cases from `sources/jq.test`. Delivery stories use `sources/full_test.sh`, `sources/run_conformance.py`, `sources/exclusions.txt`, and the root executable contract. The work is primarily capability implementation, with staged test-harness and final acceptance-contract scopes.

### Test and Acceptance Strategy

Stories run only their own `--select` corpus slices through `sources/run_conformance.py` and assert a zero runner status. The terminal `DELIVERY-003` story alone runs `sh sources/full_test.sh` with `Suite: full`; it depends on every implementation story and uses the harness exit status as the verdict.

### Sequencing and Dependencies

Stage all runtime verification assets before acceptance. Build lexer and parser before evaluation; build generator evaluation before paths and assignment; build those foundations before control flow, functions, and builtins; complete numeric and boundary behavior before the final executable and full-suite gate. No external service or package dependency exists.

### Source Conflicts and Gaps

No unresolved cross-source conflicts or blockers were found. The supplied instructions explicitly settle the implementation language, interface, exclusions, acceptance command, and prohibited dependencies.

## Analysis Notes
generated: 2026-08-20
blueprint: /mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260820.235126/workspace/targets/jq/blueprint

Quality: Ready
  blockers: 0
  questions: 0
  features: 8
  stories: 25
  stack: Python with standard library and POSIX sh
  display_name: not proposed
  short_description: not proposed

None.
