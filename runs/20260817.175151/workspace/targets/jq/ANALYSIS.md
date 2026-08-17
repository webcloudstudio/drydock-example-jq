# Blueprint Analysis: jq

## Commander Expectations

- assert the interpreter implements the jq language and passes every supplied conformance case through the required executable interface.

## Crew

| Crew | Charge |
|---|---|
| Commander | Defines intent and decides what done means. |
| Team Lead | Confirms epic completeness and stakeholder expectations. |
| Planning Crew | Authors atomic specifications and the ordered Manifest. |
| Shipyard Crew | Builds the tickets without synchronous Commander access. |

## Story List

### Feature: CLI Execution Contract

| ID | Story | High-level AC |
|---|---|---|
| CLI-001 | Provide the executable jq entrypoint | An executable named `jq` accepts `-c`, reads JSON from stdin, and emits compact JSON values one per line. |
| CLI-002 | Implement compile and runtime exit semantics | Compile errors exit 3 and runtime errors exit 5 while preserving outputs emitted before a runtime error. |
| CLI-003 | Document the command-line interface | README documents stdin/stdout behavior, exit codes, and `sh sources/full_test.sh`. |

### Feature: jq Front End

| ID | Story | High-level AC |
|---|---|---|
| FRONT-001 | Tokenize jq source | The lexer recognizes jq literals, identifiers, bindings, operators, delimiters, comments, formats, strings, and interpolation syntax. |
| FRONT-002 | Parse jq expressions into an executable representation | The parser handles jq precedence, associativity, indexing, slicing, construction, conditionals, functions, bindings, modules, and reductions. |
| FRONT-003 | Reject invalid jq programs | Invalid syntax, invalid escapes, undefined bindings, malformed object keys, and invalid module forms are rejected at compile time. |

### Feature: Generator Evaluation Core

| ID | Story | High-level AC |
|---|---|---|
| CORE-001 | Evaluate identity, literals, pipes, and comma generators | Filters preserve jq stream ordering, backtracking, and Cartesian-product behavior. |
| CORE-002 | Implement indexing, iteration, and slicing | Arrays, objects, strings, optional access, negative indices, slices, and iteration follow jq semantics. |
| CORE-003 | Implement jq values and operators | Numbers, strings, arrays, objects, null, booleans, arithmetic, comparison, logical operators, and defined-or behave according to the manual. |
| CORE-004 | Construct arrays and objects from generators | Array and object expressions collect or expand generator outputs with jq-compatible key and value semantics. |

### Feature: Bindings, Functions, and Control Flow

| ID | Story | High-level AC |
|---|---|---|
| FLOW-001 | Implement lexical variables and destructuring | `as` bindings, array/object patterns, lexical scope, and destructuring alternatives bind values correctly. |
| FLOW-002 | Implement user-defined functions and closures | `def` supports recursive functions, filter arguments, value arguments, arity, redefinition, and lexical scoping. |
| FLOW-003 | Implement conditionals, errors, try/catch, and labels | Truthiness, `if`, `try`, `catch`, optional filters, `label`, and `break` match jq behavior. |
| FLOW-004 | Implement reduce and foreach | Reductions and intermediate extraction preserve generator order and accumulator semantics. |
| FLOW-005 | Implement iteration and recursion utilities | `range`, `while`, `until`, `repeat`, `limit`, `skip`, `first`, `last`, `nth`, and `recurse` work with streams. |

### Feature: Paths and Assignment

| ID | Story | High-level AC |
|---|---|---|
| PATH-001 | Implement path discovery and access | `path`, `paths`, `getpath`, and path-based traversal produce and consume jq paths correctly. |
| PATH-002 | Implement path mutation and deletion | `setpath`, `delpaths`, and `del` update nested arrays and objects, including creation, deletion, and invalid-path behavior. |
| PATH-003 | Implement assignment operators | Plain, update, arithmetic, and defined-or assignments support multiple path expressions and jq’s immutable update semantics. |

### Feature: Built-in Data and Text Operations

| ID | Story | High-level AC |
|---|---|---|
| BUILTIN-001 | Implement type, collection, and object builtins | Type predicates, length, keys, entries, containment, sorting, grouping, uniqueness, joins, flattening, and transposition match the corpus. |
| BUILTIN-002 | Implement string and Unicode builtins | String trimming, splitting, joining, case conversion, codepoint conversion, and UTF-8 length follow jq semantics. |
| BUILTIN-003 | Implement regular-expression builtins | `test`, `match`, `capture`, `scan`, `split`, `splits`, `sub`, and `gsub` support the supplied regex behavior and flags. |
| BUILTIN-004 | Implement format and JSON conversion builtins | `tostring`, `tonumber`, `toboolean`, `tojson`, `fromjson`, and `@` formats produce the required values and escaping. |
| BUILTIN-005 | Implement numeric, math, and date builtins | Floating-point behavior, special numbers, math functions, date parsing, formatting, and epoch conversion satisfy the supplied cases. |

### Feature: Streaming and Runtime I/O

| ID | Story | High-level AC |
|---|---|---|
| IO-001 | Implement input and diagnostic builtins | `input`, `inputs`, `debug`, `stderr`, environment access, and location values follow the defined interface. |
| IO-002 | Implement streaming transformations | `tostream`, `fromstream`, and `truncate_stream` transform the supplied streaming representations correctly. |

### Feature: Conformance Delivery

| ID | Story | High-level AC |
|---|---|---|
| CONF-001 | Stage and preserve the supplied conformance assets | The implementation runs against the staged corpus and harness without modifying scoring assets. |
| CONF-002 | Run the complete jq conformance gate | **Suite: full** — the terminal verification invokes `sh sources/full_test.sh` and every non-excluded supplied case passes with no failures or errors. |

## Surfaced Acceptance Criteria

| ID | Story ID | Criterion |
|---|---|---|
| AC-001 | CLI-001 | The executable operates using only the standard-library/runtime facilities available in the supplied environment and requires no installation or network access. |
| AC-002 | FRONT-003 | Module grammar cases are rejected without attempting filesystem module loading. |
| AC-003 | CONF-001 | The read-only scoring files remain unmodified and are available at their documented `sources/` paths during verification. |

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
| `sources/lexer.l` | parser-to-normalizer | `sources/parser.y` | Lexer tokens and parser grammar jointly define the front end. | Front-end stories must sequence lexer support before parser execution. |
| `sources/parser.y` | instruction-to-test | `sources/jq.test` | Grammar constructs and precedence are exercised by corpus programs. | Parser coverage is validated by scoped corpus selections. |
| `sources/jq-manual.txt` | reference-to-replacement | implementation stories | Manual defines language and builtin semantics. | The Python interpreter replaces the upstream executable behavior without using a third-party jq implementation. |
| `sources/builtin.jq` | reference-to-replacement | `BUILTIN-*` stories | jq-defined builtins provide executable semantic references. | Builtins must be implemented in the interpreter’s standard-library code. |
| `sources/jq.test` | test-kit-to-implementation | all implementation stories | Corpus supplies programs, inputs, expected streams, and compile-failure cases. | Each feature owns scoped cases; only `CONF-002` runs the complete suite. |
| `sources/run_conformance.py` | test-kit-to-implementation | `CONF-002` | Harness launches `jq -c`, compares structural JSON, and enforces exit codes. | Stage the harness and use its exit status as the terminal verdict. |
| `sources/full_test.sh` | instruction-to-test | `CONF-002` | Script checks the executable and invokes the unfiltered harness. | Preserve the script and execute it once as the terminal acceptance check. |
| `sources/exclusions.txt` | test-kit-to-implementation | `sources/run_conformance.py` | Exclusions define only unsupported module-loader cases. | Stage the file and preserve its declared skips. |

## Source Roles

| Path | Role | Plan disposition | Build disposition |
|---|---|---|---|
| `sources/INSTRUCTIONS.md` | author intent | prompt-only | prompt-only |
| `sources/builtin.jq` | reference implementation | context | stage |
| `sources/exclusions.txt` | conformance harness | context | stage |
| `sources/full_test.sh` | conformance harness | context | stage |
| `sources/jq-manual.txt` | normative specification | context | prompt-only |
| `sources/jq.test` | normative specification and conformance test suite | context | stage |
| `sources/lexer.l` | normative specification | context | stage |
| `sources/parser.y` | normative specification | context | stage |
| `sources/run_conformance.py` | conformance harness | context | stage |

## Planning Instructions

### Delivery Shape

The product is a standalone command-line jq interpreter. It accepts a jq program and JSON input streams, lexes and parses the program, evaluates it as a generator-based filter, and emits compact JSON values or diagnostics. The execution flow is: executable entrypoint → source front end → generator evaluator → builtins and path operations → stdout/stderr and documented exit status.

### Story Realization Map

| Story ID | Blueprint scope | Evidence | Related files | Delivery kind |
|---|---|---|---|---|
| CLI-001 | Executable and stdin/stdout adapter | `sources/INSTRUCTIONS.md` | `sources/run_conformance.py` | capability |
| CLI-002 | Exit and error mapping | `sources/INSTRUCTIONS.md`, `sources/run_conformance.py` | `sources/jq.test` | capability |
| CLI-003 | README interface documentation | `sources/INSTRUCTIONS.md` | `sources/full_test.sh` | acceptance contract |
| FRONT-001 | Lexer | `sources/lexer.l` | `sources/parser.y` | capability |
| FRONT-002 | Parser and AST | `sources/parser.y` | `sources/lexer.l` | capability |
| FRONT-003 | Static validation | `sources/parser.y`, `sources/jq.test` | `sources/run_conformance.py` | capability |
| CORE-001 | Stream evaluator | `sources/jq-manual.txt` | `sources/jq.test` | capability |
| CORE-002 | Index and iterator evaluator | `sources/parser.y`, `sources/jq.test` | `sources/lexer.l` | capability |
| CORE-003 | Value/operator semantics | `sources/jq-manual.txt`, `sources/jq.test` | — | capability |
| CORE-004 | Collection evaluator | `sources/parser.y`, `sources/jq.test` | — | capability |
| FLOW-001 | Environment and pattern matcher | `sources/parser.y`, `sources/jq-manual.txt` | `sources/jq.test` | capability |
| FLOW-002 | Function registry and closures | `sources/parser.y`, `sources/builtin.jq` | `sources/jq.test` | capability |
| FLOW-003 | Control and error runtime | `sources/parser.y`, `sources/jq-manual.txt` | `sources/jq.test` | capability |
| FLOW-004 | Reduction runtime | `sources/parser.y`, `sources/jq.test` | — | capability |
| FLOW-005 | Recursive generators | `sources/builtin.jq`, `sources/jq.test` | — | capability |
| PATH-001 | Path evaluator | `sources/jq-manual.txt`, `sources/jq.test` | — | capability |
| PATH-002 | Nested mutation helpers | `sources/builtin.jq`, `sources/jq.test` | — | capability |
| PATH-003 | Assignment evaluator | `sources/parser.y`, `sources/jq-manual.txt` | — | capability |
| BUILTIN-001 | Collection/object builtins | `sources/builtin.jq`, `sources/jq-manual.txt` | `sources/jq.test` | capability |
| BUILTIN-002 | String/Unicode builtins | `sources/builtin.jq`, `sources/jq-manual.txt` | `sources/jq.test` | capability |
| BUILTIN-003 | Regex builtins | `sources/builtin.jq`, `sources/jq-manual.txt` | `sources/jq.test` | capability |
| BUILTIN-004 | Formatting/conversion builtins | `sources/builtin.jq`, `sources/jq-manual.txt` | `sources/jq.test` | capability |
| BUILTIN-005 | Math/date builtins | `sources/jq-manual.txt`, `sources/jq.test` | — | capability |
| IO-001 | Runtime input and diagnostics | `sources/jq-manual.txt`, `sources/jq.test` | — | capability |
| IO-002 | Streaming builtins | `sources/jq-manual.txt`, `sources/builtin.jq` | `sources/jq.test` | capability |
| CONF-001 | Asset staging and preservation | `sources/INSTRUCTIONS.md` | all staged `sources/*` assets | acceptance contract |
| CONF-002 | Terminal full-suite verification | `sources/full_test.sh`, `sources/run_conformance.py` | `sources/jq.test`, `sources/exclusions.txt` | acceptance contract |

### Test and Acceptance Strategy

Implementation stories use focused unit and corpus selections for their owned syntax or builtin behavior. The conformance harness is staged as a test helper; scoped runs use `--select` during development. `CONF-002` is the sole terminal story that invokes the complete unfiltered suite and asserts only the harness success verdict.

### Sequencing and Dependencies

The executable adapter precedes runtime verification. Lexer support precedes parser execution; parser and AST support precede evaluator work. Generator evaluation precedes control flow, paths, assignments, and higher-level builtins. Runtime helpers precede builtin integration. All staged corpus and harness assets must be present before `CONF-002`. No external services, persistence, package installation, or network access are required.

### Source Conflicts and Gaps

No conflicting product definitions or blockers were found. The source defines a standalone CLI, Python-compatible runtime constraints, the executable contract, and the complete conformance objective. Project identity remains to be confirmed by the Commander.

## Analysis Notes
generated: 2026-08-17
blueprint: /mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260817.175151/workspace/targets/jq/blueprint

Quality: Questions
  blockers: 0
  questions: 1
  features: 8
  stories: 29
  stack: Python standard library with POSIX sh
  display_name: not proposed
  short_description: A standalone Python interpreter for the jq language that reads JSON from stdin and emits jq filter results.

None.
