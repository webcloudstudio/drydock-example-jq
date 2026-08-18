# MANIFEST: jq
updated:     2026-08-18T00:32:13+00:00
state:       approved
blocks:      26
planning_feedback: |
  analyze-display_name applied ARCHITECTURE.md
  analyze-short_description applied ARCHITECTURE.md

## story 1: Define the interpreter architecture and module boundaries.
id: architecture
summary: Define the interpreter architecture and module boundaries.
type: foundational
kind: capability
phase: 1
block: 1
implements: ARCHITECTURE.md
covers: —
context: TECHNOLOGY_STACK.md
stack: common.md, python.md
stack_mode: builder
size: 14345
provides: interpreter architecture, evaluator interfaces, source asset layout
consumes: —
instructions: |
  Define the Python standard-library architecture, executable boundary, lexer/parser/evaluator
  modules, generator model, error model, and staged source-asset layout.
acceptance: yes
state: blocked/questions
scope: both

## story 2: Stage the supplied conformance assets and prove the harness is runnable.
id: conformance-staging
summary: Stage the supplied conformance assets and prove the harness is runnable.
type: foundational
kind: test harness
phase: 1
block: 2
implements: FEATURE-Conformance-Staging.md
context: run_conformance.py, full_test.sh, exclusions.txt, jq.test, jq-manual.txt, parser.y, lexer.l, builtin.jq, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 65405
budget: over-target
provides: sources/jq.test, sources/run_conformance.py, sources/full_test.sh, sources/exclusions.txt
consumes: —
instructions: |
  Copy the supplied source assets into the application root without modification. Verify the
  corpus and exclusion list are complete and that the harness list mode runs with JQ supplied.
acceptance: yes
depends: architecture
state: pending

## story 3: Implement the executable jq command process contract.
id: executable-contract
summary: Implement the executable jq command process contract.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-Executable-Contract.md
covers: EXEC-001
context: run_conformance.py, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 15054
provides: ./jq -c, stdin JSON stream processing, compact JSON line output, exit codes 0/3/5
consumes: interpreter architecture
instructions: |
  Implement an executable named jq at the application root. Accept only the exercised -c
  invocation, read JSON values from stdin, emit compact JSON values one per line, route
  diagnostics to stderr, and preserve compile versus runtime exit status.
acceptance: yes
depends: architecture
state: pending

## story 4: Document jq invocation, streams, exit codes, and scoring.
id: usage-documentation
summary: Document jq invocation, streams, exit codes, and scoring.
type: service
kind: capability
phase: 1
block: 3
implements: README.md
covers: EXEC-002
stack: common.md
stack_mode: consumer
size: 6847
provides: project usage documentation
consumes: ./jq -c
instructions: |
  Write a concise README documenting the stdin/stdout interface, exit codes, standard-library-only
  constraint, and sh sources/full_test.sh verification command.
acceptance: yes
depends: executable-contract
state: pending

## story 5: Implement jq lexical analysis and interpolation tokens.
id: lexer
summary: Implement jq lexical analysis and interpolation tokens.
type: service
kind: capability
phase: 2
block: 4
implements: FEATURE-Lexer.md
covers: FRONT-001
context: lexer.l, jq-manual.txt, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 52300
budget: over-target
provides: jq lexer
consumes: interpreter architecture
instructions: |
  Implement lexical analysis for jq literals, identifiers, bindings, operators, delimiters,
  comments, strings, escapes, interpolation, formats, and module tokens according to the supplied
  lexer and corpus.
acceptance: yes
depends: architecture, executable-contract
state: pending

## story 6: Parse jq programs into executable AST structures.
id: parser
summary: Parse jq programs into executable AST structures.
type: service
kind: capability
phase: 2
block: 5
implements: FEATURE-Parser.md
covers: FRONT-002
context: parser.y, lexer.l, jq-manual.txt, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 57954
budget: over-target
provides: jq parser and AST
consumes: jq lexer
instructions: |
  Implement precedence, associativity, expressions, constructors, functions, bindings, control
  forms, assignments, reducers, modules, and interpolation parsing into an executable AST.
acceptance: yes
depends: lexer
state: pending

## story 7: Distinguish and report jq compile-time failures.
id: compile-diagnostics
summary: Distinguish and report jq compile-time failures.
type: service
kind: capability
phase: 2
block: 6
implements: FEATURE-Compile-Diagnostics.md
covers: FRONT-003
context: parser.y, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 24147
provides: compile validation, exit status 3
consumes: jq parser and AST
instructions: |
  Reject malformed syntax, invalid static bindings, invalid object keys, invalid module forms,
  and other static errors with exit status 3 and diagnostics on stderr.
acceptance: yes
depends: parser
state: pending

## story 8: Implement ordered stream evaluation and pipeline composition.
id: generator-core
summary: Implement ordered stream evaluation and pipeline composition.
type: service
kind: capability
phase: 3
block: 7
implements: FEATURE-Generator-Core.md
covers: CORE-001
context: jq-manual.txt, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 51188
budget: over-target
provides: ordered filter generators, pipeline backtracking, stream errors
consumes: jq parser and AST
instructions: |
  Evaluate every filter as an ordered generator, preserving zero/many outputs, cartesian
  composition, downstream backtracking, partial output, and runtime failure propagation.
acceptance: yes
depends: parser, compile-diagnostics
state: pending

## story 9: Implement jq primitives, constructors, indexing, and generators.
id: primitive-filters
summary: Implement jq primitives, constructors, indexing, and generators.
type: service
kind: capability
phase: 3
block: 8
implements: FEATURE-Primitive-Filters.md
covers: CORE-002
context: jq-manual.txt, jq.test, builtin.jq, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 53581
budget: over-target
provides: identity, literals, arrays, objects, fields, indexes, iteration, slices, comma, pipe, empty
consumes: ordered filter generators
instructions: |
  Implement primitive filters and constructors, including field access, array/object indexing,
  iteration, slices, comma, pipe, recursive descent, optional access, and empty.
acceptance: yes
depends: generator-core
state: pending

## story 10: Implement jq arithmetic, equality, ordering, and numeric behavior.
id: arithmetic-comparison
summary: Implement jq arithmetic, equality, ordering, and numeric behavior.
type: service
kind: capability
phase: 3
block: 9
implements: FEATURE-Arithmetic-Comparison.md
covers: CORE-003
context: jq-manual.txt, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 51377
budget: over-target
provides: arithmetic operators, comparison operators, numeric predicates
consumes: ordered filter generators
instructions: |
  Implement type-directed arithmetic, string and array operations, object merge, equality,
  ordering, cartesian filter arguments, floating-point edge cases, and numeric runtime errors.
acceptance: yes
depends: primitive-filters
state: pending

## story 11: Implement jq conditional and boolean control operators.
id: conditionals
summary: Implement jq conditional and boolean control operators.
type: service
kind: capability
phase: 3
block: 10
implements: FEATURE-Conditionals.md
covers: CORE-004
context: jq-manual.txt, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 51076
budget: over-target
provides: if/then/elif/else/end, and, or, not, //, optional execution
consumes: ordered filter generators
instructions: |
  Implement jq truthiness, conditional branching over generator outputs, boolean operators,
  defined-or defaults, and optional error suppression.
acceptance: yes
depends: arithmetic-comparison
state: pending

## story 12: Implement runtime errors, catches, halts, labels, and breaks.
id: runtime-errors
summary: Implement runtime errors, catches, halts, labels, and breaks.
type: service
kind: capability
phase: 3
block: 11
implements: FEATURE-Runtime-Errors.md
covers: CORE-005
context: jq-manual.txt, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 51088
budget: over-target
provides: error, try/catch, halt, halt_error, label, break, runtime exit status 5
consumes: ordered filter generators
instructions: |
  Implement runtime error values and propagation, try/catch behavior, halt semantics, labels,
  breaks, stderr behavior, and the required runtime exit distinction.
acceptance: yes
depends: conditionals
state: pending

## story 13: Implement user-defined jq functions, parameters, recursion, and closures.
id: functions
summary: Implement user-defined jq functions, parameters, recursion, and closures.
type: service
kind: capability
phase: 4
block: 12
implements: FEATURE-Functions.md
covers: FLOW-001
context: jq-manual.txt, builtin.jq, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 53508
budget: over-target
provides: def functions, filter parameters, value parameters, recursion, lexical closures
consumes: jq parser and generator evaluator
instructions: |
  Implement lexical function definitions, arities, filter and value parameters, redefinition,
  recursion, closures, generator backtracking, and function-local scope.
acceptance: yes
depends: runtime-errors
state: pending

## story 14: Implement jq variable bindings and destructuring alternatives.
id: bindings
summary: Implement jq variable bindings and destructuring alternatives.
type: service
kind: capability
phase: 4
block: 13
implements: FEATURE-Bindings.md
covers: FLOW-002
context: jq-manual.txt, parser.y, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 56699
budget: over-target
provides: as bindings, array/object patterns, ?// alternatives
consumes: jq parser and generator evaluator
instructions: |
  Implement lexical value bindings, array and object destructuring, nested patterns, missing-value
  binding, and ?// alternative matching with correct scope and error fallback.
acceptance: yes
depends: functions
state: pending

## story 15: Implement reducers, iterators, ranges, and generator control flow.
id: reducers
summary: Implement reducers, iterators, ranges, and generator control flow.
type: service
kind: capability
phase: 4
block: 14
implements: FEATURE-Reducers.md
covers: FLOW-003
context: jq-manual.txt, builtin.jq, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 53529
budget: over-target
provides: reduce, foreach, range, limit, skip, first, last, nth, while, until, repeat, recurse, any, all
consumes: user-defined functions and bindings
instructions: |
  Implement reducer state transitions, extraction streams, ranges, short-circuiting generators,
  recursive traversal, iteration helpers, and any/all semantics.
acceptance: yes
depends: bindings
state: pending

## story 16: Implement jq path discovery and path reads.
id: path-discovery
summary: Implement jq path discovery and path reads.
type: service
kind: capability
phase: 5
block: 15
implements: FEATURE-Path-Discovery.md
covers: PATH-001
context: jq-manual.txt, builtin.jq, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 53538
budget: over-target
provides: path, paths, getpath, pick
consumes: generator evaluator, indexing, reducers
instructions: |
  Implement path capture and traversal for objects, arrays, slices, generated paths, missing values,
  getpath reads, and pick projections.
acceptance: yes
depends: reducers
state: pending

## story 17: Implement nested path mutation and deletion.
id: path-mutation
summary: Implement nested path mutation and deletion.
type: service
kind: capability
phase: 5
block: 16
implements: FEATURE-Path-Mutation.md
covers: PATH-002
context: jq-manual.txt, builtin.jq, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 53614
budget: over-target
provides: setpath, delpaths, del
consumes: path discovery
instructions: |
  Implement immutable nested updates, array growth and deletion, object deletion, multi-path
  deletion, missing containers, and specified path mutation errors.
acceptance: yes
depends: path-discovery
state: pending

## story 18: Implement jq assignment and update-assignment operators.
id: assignments
summary: Implement jq assignment and update-assignment operators.
type: service
kind: capability
phase: 5
block: 17
implements: FEATURE-Assignments.md
covers: PATH-003
context: jq-manual.txt, builtin.jq, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 53618
budget: over-target
provides: =, |=, +=, -=, *=, /=, %=, //=
consumes: path mutation and path discovery
instructions: |
  Implement plain and update assignments over exact and multi-result paths, immutable updates,
  empty-result deletion, cartesian RHS behavior, and all arithmetic assignment variants.
acceptance: yes
depends: path-mutation
state: pending

## story 19: Implement type, collection, and structural jq builtins.
id: structural-builtins
summary: Implement type, collection, and structural jq builtins.
type: service
kind: capability
phase: 6
block: 18
implements: FEATURE-Structural-Builtins.md
covers: BUILTIN-001
context: builtin.jq, jq-manual.txt, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 53691
budget: over-target
provides: structural collection, containment, sorting, grouping, uniqueness, flattening, transpose, walking builtins
consumes: assignments, paths, reducers, functions
instructions: |
  Implement structural and collection builtins, including type selectors, length, keys, entries,
  containment, sorting, grouping, uniqueness, flattening, combinations, transpose, walk, and
  related helpers.
acceptance: yes
depends: assignments
state: pending

## story 20: Implement jq string and Unicode builtins.
id: string-builtins
summary: Implement jq string and Unicode builtins.
type: service
kind: capability
phase: 6
block: 19
implements: FEATURE-String-Builtins.md
covers: BUILTIN-002
context: builtin.jq, jq-manual.txt, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 53701
budget: over-target
provides: string trimming, splitting, joining, case, indexing, codepoint, interpolation, JSON conversion
consumes: functions and generator evaluator
instructions: |
  Implement Unicode-aware string operations, codepoint conversion, interpolation, tostring,
  tonumber, tojson/fromjson, trimming, splitting, joining, and string indexing behavior.
acceptance: yes
depends: structural-builtins
state: pending

## story 21: Implement jq regular-expression filters and replacements.
id: regex-builtins
summary: Implement jq regular-expression filters and replacements.
type: service
kind: capability
phase: 6
block: 20
implements: FEATURE-Regex-Builtins.md
covers: BUILTIN-003
context: builtin.jq, jq-manual.txt, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 53579
budget: over-target
provides: test, match, capture, scan, split, splits, sub, gsub
consumes: string builtins and generator evaluator
instructions: |
  Implement regex matching, flags, named and unnamed captures, offsets, scanning, splitting,
  substitution, global replacement, and generator-valued replacement behavior using the standard
  library.
acceptance: yes
depends: string-builtins
state: pending

## story 22: Implement jq output formats and encodings.
id: format-builtins
summary: Implement jq output formats and encodings.
type: service
kind: capability
phase: 6
block: 21
implements: FEATURE-Format-Builtins.md
covers: BUILTIN-004
context: builtin.jq, jq-manual.txt, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 53513
budget: over-target
provides: @text, @json, @html, @uri, @urid, @csv, @tsv, @sh, @base64, @base64d
consumes: string builtins and JSON serialization
instructions: |
  Implement all specified format filters, escaping rules, interpolation behavior, CSV/TSV
  serialization, shell quoting, URI encoding, and base64 conversion.
acceptance: yes
depends: regex-builtins
state: pending

## story 23: Implement jq date, time, math, and numeric helper builtins.
id: date-math-builtins
summary: Implement jq date, time, math, and numeric helper builtins.
type: service
kind: capability
phase: 6
block: 22
implements: FEATURE-Date-Math-Builtins.md
covers: BUILTIN-005
context: builtin.jq, jq-manual.txt, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 53580
budget: over-target
provides: date conversion, time structures, math functions, numeric predicates
consumes: arithmetic-comparison and string builtins
instructions: |
  Implement UTC date conversion, strptime/strftime/mktime/gmtime/localtime, now, standard math
  functions, infinities, NaN, finiteness, normality, and numeric edge cases.
acceptance: yes
depends: format-builtins
state: pending

## story 24: Implement jq streaming, environment, input, and diagnostic builtins.
id: io-builtins
summary: Implement jq streaming, environment, input, and diagnostic builtins.
type: service
kind: capability
phase: 6
block: 23
implements: FEATURE-IO-Builtins.md
covers: BUILTIN-006
context: builtin.jq, jq-manual.txt, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 53551
budget: over-target
provides: tostream, fromstream, truncate_stream, input, inputs, debug, stderr, env, $ENV
consumes: generator evaluator and executable stdin/stderr
instructions: |
  Implement streaming transformations, additional input consumption, environment access, debug
  output, stderr output, and the specified interaction with the executable process.
acceptance: yes
depends: date-math-builtins
state: pending

## story 25: Implement jq SQL-style and metadata builtins.
id: sql-metadata-builtins
summary: Implement jq SQL-style and metadata builtins.
type: service
kind: capability
phase: 6
block: 24
implements: FEATURE-SQL-Metadata-Builtins.md
covers: BUILTIN-007
context: builtin.jq, jq-manual.txt, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 53525
budget: over-target
provides: INDEX, JOIN, IN, builtins, have_decnum, metadata helpers
consumes: functions, paths, and generator evaluator
instructions: |
  Implement INDEX, JOIN, IN, builtins enumeration, have_decnum, and related metadata behavior
  without external dependencies.
acceptance: yes
depends: io-builtins
state: pending

## story 26: Validate jq module, import, and include grammar boundaries.
id: module-grammar
summary: Validate jq module, import, and include grammar boundaries.
type: service
kind: capability
phase: 7
block: 25
implements: FEATURE-Module-Grammar.md
covers: MODULE-001
context: parser.y, lexer.l, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 25215
provides: module/import/include syntax validation
consumes: jq lexer and parser
instructions: |
  Parse module, import, and include forms sufficiently to reject invalid metadata, paths, and
  namespace syntax with compile status 3, without requiring filesystem module loading.
acceptance: yes
depends: sql-metadata-builtins
state: pending

## story 27: Prove the completed interpreter against the full supplied corpus.
id: conformance-verification
summary: Prove the completed interpreter against the full supplied corpus.
type: service
kind: test harness
phase: 8
block: 26
implements: FEATURE-Conformance-Verification.md
covers: VERIFY-001
accepts: st-001
context: full_test.sh, run_conformance.py, exclusions.txt, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 23652
provides: complete jq conformance proof
consumes: executable jq, all implemented language and builtin capabilities
instructions: |
  Run sh sources/full_test.sh from the completed application root. Capture and print stdout and
  stderr for diagnosis, and require the supplied command to exit zero. This is the terminal
  whole-corpus verification story.
acceptance: yes
depends: architecture, conformance-staging, executable-contract, usage-documentation, lexer, parser, compile-diagnostics, generator-core, primitive-filters, arithmetic-comparison, conditionals, runtime-errors, functions, bindings, reducers, path-discovery, path-mutation, assignments, structural-builtins, string-builtins, regex-builtins, format-builtins, date-math-builtins, io-builtins, sql-metadata-builtins, module-grammar
state: pending
