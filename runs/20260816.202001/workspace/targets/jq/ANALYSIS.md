# Blueprint Analysis: jq

## Commander Expectations

- assert the jq interpreter passes every supplied jq conformance case through the supplied scoring script.

## Crew

| Crew | Charge |
|---|---|
| Commander | Defines intent and decides what done means. |
| Team Lead | Confirms epic completeness and stakeholder expectations. |
| Planning Crew | Authors atomic specifications and the ordered Manifest. |
| Shipyard Crew | Builds the tickets without synchronous Commander access. |

## Story List

### Feature: Interpreter Front End

| ID | Story | High-level AC |
|---|---|---|
| FRONTEND-001 | Implement jq lexer | jq source text is tokenized according to the supplied lexer specification, including strings, interpolation, comments, identifiers, literals, operators, and formats. |
| FRONTEND-002 | Implement jq parser and AST | Valid jq programs parse into an executable AST with the required precedence, associativity, constructs, and compile-error behavior. |
| FRONTEND-003 | Implement compile diagnostics and exit contract | Invalid programs exit 3; diagnostics go to stderr; valid programs reach runtime evaluation. |
| FRONTEND-004 | Implement string interpolation and format syntax | Interpolated strings and `@text`, `@json`, `@html`, `@uri`, `@urid`, `@csv`, `@tsv`, `@sh`, `@base64`, and `@base64d` behave as specified. |

### Feature: Generator Runtime

| ID | Story | High-level AC |
|---|---|---|
| RUNTIME-001 | Implement stream-valued filter evaluation | Filters produce ordered zero-, one-, or many-value streams, and pipelines and comma expressions preserve jq backtracking semantics. |
| RUNTIME-002 | Implement core values, indexing, iteration, and construction | Identity, literals, field/index access, slices, iteration, arrays, objects, recursive descent, and empty behave according to the manual. |
| RUNTIME-003 | Implement operators and comparisons | Arithmetic, string/array/object operations, Boolean operators, defined-or, equality, ordering, and type behavior match jq semantics. |
| RUNTIME-004 | Implement errors, try/catch, optional access, and labels | Runtime errors use exit 5, partial output is preserved, `try`, `catch`, `?`, `label`, and `break` work correctly. |
| RUNTIME-005 | Implement functions, variables, closures, and destructuring | User-defined functions, filter/value parameters, lexical bindings, patterns, and `?//` alternatives work correctly. |
| RUNTIME-006 | Implement reduce, foreach, and recursive control flow | `reduce`, `foreach`, `range`, `limit`, `skip`, `first`, `last`, `nth`, `while`, `until`, `repeat`, and `recurse` preserve generator semantics. |

### Feature: jq Builtin Library

| ID | Story | High-level AC |
|---|---|---|
| BUILTINS-001 | Implement collection and structural builtins | Collection, sorting, grouping, uniqueness, containment, entry conversion, walking, flattening, transposition, and path utilities match the supplied behavior. |
| BUILTINS-002 | Implement string and regular-expression builtins | String trimming, splitting, joining, case conversion, indexing, matching, scanning, capture, substitution, and regex flags work as specified. |
| BUILTINS-003 | Implement numeric, math, and special-number builtins | Numeric conversion, math functions, infinities, NaN, numeric comparison, literal preservation behavior, and `have_decnum` behavior match the corpus requirements. |
| BUILTINS-004 | Implement date, JSON, encoding, and environment builtins | Date/time functions, JSON conversion, environment access, and encoding/escaping builtins produce the specified values and errors. |
| BUILTINS-005 | Implement streaming and I/O builtins | `input`, `inputs`, `debug`, `stderr`, `tostream`, `fromstream`, and `truncate_stream` behave according to the supported interface. |
| BUILTINS-006 | Implement SQL-style and introspection builtins | `INDEX`, `JOIN`, `IN`, `builtins`, and supported module grammar/introspection behavior are implemented without loading excluded fixture modules. |

### Feature: Executable Delivery and Verification

| ID | Story | High-level AC |
|---|---|---|
| DELIVERY-001 | Deliver the executable jq entry point | An executable named `./jq` accepts `-c '<program>'`, reads JSON values from stdin, writes compact JSON values one per line, and uses the documented exit codes. |
| DELIVERY-002 | Stage supplied source and scoring assets | Required sources are available under `sources/` without modifying read-only scoring assets. |
| DELIVERY-003 | Run bounded implementation verification | Focused tests exercise each implementation area without invoking the complete acceptance suite. |
| DELIVERY-004 | Gate delivery on the complete conformance suite | The terminal verification runs the supplied full suite unfiltered and succeeds only when every non-excluded case passes with no failures or errors. |

## Surfaced Acceptance Criteria

| ID | Story ID | Criterion |
|---|---|---|
| AC-001 | DELIVERY-001 | The executable emits each produced value as one compact JSON value per stdout line and sends diagnostics to stderr. |
| AC-002 | DELIVERY-001 | The executable supports the exercised `-c` interface and does not require network access, package installation, or third-party runtime dependencies. |
| AC-003 | FRONTEND-003 | A syntactically invalid jq program exits with status 3, while a runtime failure exits with status 5. |
| AC-004 | DELIVERY-002 | The supplied harness, corpus, exclusions, and normative source files remain unmodified and are staged at their documented paths. |

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
| `sources/lexer.l` | parser-to-normalizer | `sources/parser.y` | Lexer tokens are consumed by the yacc grammar. | Implement lexer behavior before parser execution. |
| `sources/parser.y` | implementation-to-helper | `sources/builtin.jq` | Parser emits calls to builtin and runtime operations. | Runtime callable resolution must support parsed builtin calls. |
| `sources/jq-manual.txt` | reference-to-replacement | `FRONTEND-*`, `RUNTIME-*`, `BUILTINS-*` | Manual defines language and builtin semantics. | Use as the primary behavioral specification. |
| `sources/jq.test` | test-kit-to-implementation | all implementation stories | Corpus exercises parser, generators, builtins, assignments, errors, and edge cases. | Keep focused verification bounded; reserve the complete corpus for the terminal gate. |
| `sources/run_conformance.py` | instruction-to-test | `DELIVERY-004` | Harness invokes `./jq -c`, compares streams structurally, and recognizes exit codes. | Preserve the exact executable contract and harness invocation. |
| `sources/full_test.sh` | instruction-to-test | `DELIVERY-004` | Shell script is the sole supplied scoring entry point. | Run it once as the terminal acceptance verification. |
| `sources/exclusions.txt` | dependency | `sources/jq.test` | Declares module-loader cases that are skipped. | Preserve exclusions and support the remaining module grammar cases. |

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

Deliver a standalone Python executable named `jq` implementing a jq-language interpreter. It reads JSON from stdin, evaluates a filter supplied with `-c`, and emits an ordered stream of compact JSON values. The implementation consists of a lexer/parser front end, generator-based evaluator, builtin library, and command-line entry point. The supplied conformance harness drives one process per corpus case.

### Story Realization Map

| Story ID | Blueprint scope | Evidence | Related files | Delivery kind |
|---|---|---|---|---|
| FRONTEND-001 | Lexer/token model | `sources/lexer.l` | `sources/lexer.l` | capability |
| FRONTEND-002 | Parser and AST | `sources/parser.y` | `sources/parser.y` | capability |
| FRONTEND-003 | Compile/runtime error boundary | `sources/INSTRUCTIONS.md`, `sources/run_conformance.py` | `sources/run_conformance.py` | acceptance contract |
| FRONTEND-004 | Strings and formats | `sources/lexer.l`, `sources/parser.y`, `sources/jq-manual.txt` | `sources/jq.test` | capability |
| RUNTIME-001 | Stream evaluator | `sources/INSTRUCTIONS.md`, `sources/jq-manual.txt` | `sources/jq.test` | capability |
| RUNTIME-002 | Core filters and values | `sources/parser.y`, `sources/jq-manual.txt` | `sources/jq.test` | capability |
| RUNTIME-003 | Operators | `sources/parser.y`, `sources/jq-manual.txt` | `sources/jq.test` | capability |
| RUNTIME-004 | Errors and control labels | `sources/parser.y`, `sources/jq-manual.txt` | `sources/jq.test` | capability |
| RUNTIME-005 | Functions and bindings | `sources/parser.y`, `sources/jq-manual.txt` | `sources/jq.test` | capability |
| RUNTIME-006 | Generator control flow | `sources/builtin.jq`, `sources/jq-manual.txt` | `sources/jq.test` | capability |
| BUILTINS-001 | Structural builtins | `sources/builtin.jq`, `sources/jq-manual.txt` | `sources/jq.test` | capability |
| BUILTINS-002 | String and regex builtins | `sources/builtin.jq`, `sources/jq-manual.txt` | `sources/jq.test` | capability |
| BUILTINS-003 | Numeric and math builtins | `sources/jq-manual.txt` | `sources/jq.test` | capability |
| BUILTINS-004 | Date, JSON, encoding, environment | `sources/builtin.jq`, `sources/jq-manual.txt` | `sources/jq.test` | capability |
| BUILTINS-005 | I/O and streaming | `sources/builtin.jq`, `sources/jq-manual.txt` | `sources/jq.test` | capability |
| BUILTINS-006 | SQL-style and introspection | `sources/builtin.jq`, `sources/jq-manual.txt` | `sources/jq.test` | capability |
| DELIVERY-001 | Executable interface | `sources/INSTRUCTIONS.md`, `sources/full_test.sh` | `jq` | acceptance contract |
| DELIVERY-002 | Source staging | `sources/INSTRUCTIONS.md` | all `sources/*` | asset |
| DELIVERY-003 | Focused verification | `sources/run_conformance.py` | `sources/run_conformance.py` | test harness |
| DELIVERY-004 | Complete conformance gate | `sources/full_test.sh`, `sources/run_conformance.py` | `sources/jq.test` | acceptance contract |

### Test and Acceptance Strategy

Each implementation story uses focused corpus selections or direct examples for its owned behavior. No intermediate story runs the complete suite. `DELIVERY-003` validates bounded slices using the harness selector. `DELIVERY-004` is the sole terminal full-suite verification story and declares `Suite: full`; it depends on all implementation stories and proves the project-level Sea Trial through the harness exit status.

### Sequencing and Dependencies

Stage all supplied assets first. Build the lexer before the parser, the parser before the evaluator, and the generator core before control flow and builtins. Implement paths and assignment before dependent structural builtins. Complete the executable entry point before focused harness runs. Run the full suite only after all implementation and focused verification stories are complete.

### Source Conflicts and Gaps

No conflicting product definitions were found. The product type is `cli`. Authentication, persistence, deployment services, and external service behavior are not applicable to the described local interpreter. The project stack is named in the instructions as Python with standard-library-only runtime support; POSIX `sh` is required by the supplied harness.

## Analysis Notes
generated: 2026-08-16
blueprint: /mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260816.202001/workspace/targets/jq/blueprint

Quality: Questions
  blockers: 0
  questions: 1
  features: 4
  stories: 19
  stack: Python standard library; POSIX sh
  display_name: jq Interpreter
  short_description: A standalone Python interpreter for the jq language that reads JSON filters from stdin and emits compact JSON result streams.

None.
