# Blueprint Analysis: jq

## Commander Expectations

- assert the interpreter accepts jq programs through `./jq -c`, reads JSON from stdin, emits compact JSON values on stdout, and passes every supplied non-excluded conformance case.

## Crew

| Crew | Charge |
|---|---|
| Commander | Defines intent and decides what done means. |
| Team Lead | Confirms epic completeness and stakeholder expectations. |
| Planning Crew | Authors atomic specifications and the ordered Manifest. |
| Shipyard Crew | Builds the tickets without synchronous Commander access. |

## Story List

### Feature: CLI Foundation

| ID | Story | High-level AC |
|---|---|---|
| CLI-001 | Implement the executable jq entry point | An executable `jq` accepts `-c`, reads stdin, emits one compact JSON value per line, and returns the documented exit codes. |
| CLI-002 | Document the interpreter interface | `README.md` documents stdin/stdout behavior, exit codes, and `sh sources/full_test.sh`. |

### Feature: Front End

| ID | Story | High-level AC |
|---|---|---|
| FRONTEND-001 | Implement jq lexical analysis | jq literals, identifiers, bindings, strings, interpolation, operators, comments, formats, and delimiters are tokenized according to the supplied lexer specification. |
| FRONTEND-002 | Implement jq parsing and AST construction | Valid jq syntax produces an executable AST and invalid syntax returns compile exit code 3. |

### Feature: Generator Evaluation

| ID | Story | High-level AC |
|---|---|---|
| EVAL-001 | Implement the generator execution model | Identity, literals, pipes, commas, iteration, collection, empty, and cartesian evaluation preserve jq stream order and multiplicity. |
| EVAL-002 | Implement operators and value semantics | Arithmetic, comparison, boolean operators, indexing, slicing, strings, arrays, objects, nulls, and jq ordering follow the supplied specification. |
| EVAL-003 | Implement control flow and errors | Conditionals, alternatives, try/catch, optional expressions, labels, breaks, reduce, foreach, limit, skip, first, last, nth, while, until, and recurse behave as generators. |

### Feature: Language Binding and Mutation

| ID | Story | High-level AC |
|---|---|---|
| LANG-001 | Implement variables, patterns, and user functions | `as`, destructuring, `?//`, function definitions, function parameters, closures, recursion, and lexical scoping work with generator-valued arguments. |
| LANG-002 | Implement paths and assignment | `path`, `getpath`, `setpath`, `delpaths`, `del`, plain assignment, update assignment, and arithmetic assignment update the intended paths with jq semantics. |

### Feature: Standard Library

| ID | Story | High-level AC |
|---|---|---|
| BUILTIN-001 | Implement collection and structural builtins | Array/object selectors, map operations, add, flatten, sorting, grouping, uniqueness, entries, containment, combinations, transpose, walk, and related builtins conform to the corpus. |
| BUILTIN-002 | Implement string, regex, format, and date builtins | String transforms, regex matching and replacement, format filters, JSON conversion, base64, URI, CSV, TSV, shell escaping, and date functions produce specified results. |
| BUILTIN-003 | Implement numeric, environment, and I/O builtins | Numeric edge cases, math functions, environment access, input/inputs, debug, stderr, and streaming helpers follow the supplied behavior. |

### Feature: Conformance Delivery

| ID | Story | High-level AC |
|---|---|---|
| CONF-001 | Run the complete supplied conformance suite | `sh sources/full_test.sh` runs the unfiltered corpus, honors only declared exclusions, and exits zero when every executed case passes with no failures or errors. `Suite: full` |

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
| `sources/lexer.l` | parser-to-normalizer | `sources/parser.y` | Lexer tokens and parser productions define the front end jointly. | Lexer implementation precedes parser validation. |
| `sources/parser.y` | implementation-to-helper | `FRONTEND-001`, `EVAL-001` | Grammar constructs AST operations consumed by evaluation. | AST contracts must be settled before evaluator work. |
| `sources/jq-manual.txt` | reference-to-replacement | all implementation stories | Manual is the normative language specification. | Stories must implement documented semantics rather than shell out to jq. |
| `sources/builtin.jq` | reference-to-replacement | `BUILTIN-*`, `LANG-*` | jq-defined builtins express generator, path, assignment, and control-flow behavior. | Builtins depend on the evaluator and binding model. |
| `sources/jq.test` | test-kit-to-implementation | all implementation stories | Corpus supplies executable behavior checks. | Tests are staged context and sliced by story during development. |
| `sources/run_conformance.py` | test-kit-to-implementation | `CONF-001` | Harness invokes `./jq -c` and compares structural outputs and exit codes. | Final verification depends on every implementation story. |
| `sources/full_test.sh` | instruction-to-test | `CONF-001` | The shell script is the sole acceptance entry point. | The terminal verification must execute this exact command. |
| `sources/exclusions.txt` | dependency | `sources/run_conformance.py` | Exclusions define the only skipped module-loader cases. | Harness and implementation must preserve declared skip behavior. |

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

Deliver a standalone Python executable named `jq`. It accepts a jq filter through `-c`, reads JSON values from stdin, evaluates each filter as a generator, and writes compact JSON outputs line-by-line. The implementation is organized around lexer/parser, AST evaluation, generator semantics, language bindings, paths and assignments, and standard-library behavior. The staged corpus and harness provide final verification.

### Story Realization Map

- `CLI-001`: executable entry point and process contract; evidence `sources/INSTRUCTIONS.md`, `sources/full_test.sh`; capability and acceptance contract.
- `CLI-002`: project README; evidence `sources/INSTRUCTIONS.md`; documentation scope.
- `FRONTEND-001`: lexer implementation; evidence `sources/lexer.l`; capability.
- `FRONTEND-002`: parser and AST; evidence `sources/parser.y`; capability.
- `EVAL-001`: generator runtime; evidence `sources/INSTRUCTIONS.md`, `sources/jq-manual.txt`; capability.
- `EVAL-002`: operators and values; evidence `sources/jq-manual.txt`, `sources/jq.test`; capability.
- `EVAL-003`: control flow and errors; evidence `sources/builtin.jq`, `sources/jq.test`; capability.
- `LANG-001`: bindings, patterns, and functions; evidence `sources/parser.y`, `sources/jq-manual.txt`; capability.
- `LANG-002`: paths and assignments; evidence `sources/builtin.jq`, `sources/jq-manual.txt`; capability.
- `BUILTIN-001`: structural builtins; evidence `sources/builtin.jq`, `sources/jq-manual.txt`; capability.
- `BUILTIN-002`: strings, regex, formats, and dates; evidence `sources/builtin.jq`, `sources/jq-manual.txt`; capability.
- `BUILTIN-003`: numeric, environment, I/O, and streaming builtins; evidence `sources/jq-manual.txt`, `sources/jq.test`; capability.
- `CONF-001`: complete suite execution; evidence `sources/full_test.sh`, `sources/run_conformance.py`, `sources/jq.test`, `sources/exclusions.txt`; conformance harness and acceptance contract.

### Test and Acceptance Strategy

Each implementation story uses focused corpus selections or targeted unit tests and must not run the complete acceptance suite. `CONF-001` is the sole terminal story with `Suite: full`; it runs `sh sources/full_test.sh` and gates delivery on its exit status.

### Sequencing and Dependencies

Build the CLI foundation first, then lexer and parser, followed by generator evaluation. Implement bindings and paths after the evaluator contracts exist. Implement standard-library groups after their runtime primitives. Stage the corpus, manual, reference builtins, lexer, parser, exclusions, and harness before verification. `CONF-001` depends on every implementation story.

### Source Conflicts and Gaps

No conflicting product definitions were found. The sources define a CLI interpreter and its acceptance workflow. Project identity is not supplied and is carried as a Commander confirmation questionnaire. Authentication, persistence, deployment, and interactive UI are not implied by this CLI project.

## Analysis Notes
generated: 2026-08-16
blueprint: /mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260816.235732/workspace/targets/jq/blueprint

Quality: Questions
  blockers: 0
  questions: 1
  features: 6
  stories: 14
  stack: Python with standard library and POSIX sh
  display_name: jq Interpreter
  short_description: A standalone Python interpreter for the jq language that reads JSON from stdin and emits filtered JSON values.

None.
