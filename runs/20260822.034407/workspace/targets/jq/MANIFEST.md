# MANIFEST: jq
updated:     2026-08-22T04:01:46+00:00
state:       approved
blocks:      21

applied: ARCHITECTURE.md=4e38a5887a3da0ff8de24850cfaa822586f3cf28,TECHNOLOGY_STACK.md=4e38a5887a3da0ff8de24850cfaa822586f3cf28,common.md=4e38a5887a3da0ff8de24850cfaa822586f3cf28,python.md=4e38a5887a3da0ff8de24850cfaa822586f3cf28
applied_specs: |
  ARCHITECTURE.md sha256=4f66ab67409074d13b7837b0c8eefec7ec2ab64ffdf9e91b66dc67b5df6d4247 commit=6054df2b2fc1c4fff171dffc133b1e0cbb49f6eb applied_by=block-1 applied_at=2026-08-22T04:10:05+00:00 build_sha256=c50eebb5888f756b0cd70a928ec91e3d5045c637173544477150027d211c4c74

## story 1: Define the standalone jq interpreter architecture and module boundaries.
id: architecture
summary: Define the standalone jq interpreter architecture and module boundaries.
type: foundational
kind: capability
phase: 1
block: 1
implements: ARCHITECTURE.md
context: TECHNOLOGY_STACK.md
stack: common.md, python.md
stack_mode: builder
size: 13762
provides: interpreter architecture, CLI boundary, evaluator boundaries
instructions: |
  Define the Python standard-library interpreter architecture, lexer/parser/evaluator boundaries,
  generator evaluation model, runtime error model, executable boundary, and source asset layout.
  Establish the implementation foundation required by all subsequent stories.
acceptance: yes
state: blocked/questions
evidence: evidence/block-1.md
scope: target
finding: ADVISORY: implemented, not verified — no governed acceptance command covers this story. Declare one in ACCEPTANCE.json to gate it.

## story 2: Implement jq lexical analysis.
id: frontend-001
finding: programmatic acceptance failed: lexer-conformance: json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
evidence: evidence/block-2.md
summary: Implement jq lexical analysis.
type: service
kind: capability
phase: 1
block: 2
implements: FEATURE-Frontend-Lexer.md
covers: FRONTEND-001
context: lexer.l, jq-manual.txt, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 41585
provides: jq lexer
consumes: interpreter architecture
instructions: |
  Implement lexical analysis for jq literals, identifiers, bindings, fields, operators, strings,
  interpolation markers, formats, comments, delimiters, and invalid characters. Preserve source
  locations and reject malformed lexical input with compile exit status 3.
acceptance: yes
depends: architecture
state: closed/failed
scope: target

## story 3: Implement jq parsing and AST construction.
id: frontend-002
summary: Implement jq parsing and AST construction.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-Frontend-Parser.md
covers: FRONTEND-002
context: parser.y, lexer.l, jq-manual.txt, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 47195
provides: jq parser, jq AST
consumes: jq lexer
instructions: |
  Implement the jq grammar, precedence, associativity, syntax validation, and AST construction
  defined by parser.y and the manual. Reject invalid programs with exit status 3.
acceptance: yes
depends: frontend-001
state: pending
scope: target

## story 4: Implement jq string interpolation and format syntax.
id: frontend-003
summary: Implement jq string interpolation and format syntax.
type: service
kind: capability
phase: 1
block: 4
implements: FEATURE-Frontend-Interpolation.md
covers: FRONTEND-003
context: lexer.l, parser.y, jq-manual.txt, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 47204
provides: string interpolation AST, format expressions
consumes: jq parser, jq AST
instructions: |
  Implement interpolated strings, escaped text, embedded filter evaluation, and @format syntax
  in the AST and evaluator-facing representation.
acceptance: yes
depends: frontend-002
state: pending
scope: target

## story 5: Stage and validate the supplied conformance harness assets.
id: cli-002
summary: Stage and validate the supplied conformance harness assets.
type: foundational
kind: test harness
phase: 1
block: 5
implements: FEATURE-CLI-Harness.md
covers: CLI-002
context: run_conformance.py, jq.test, exclusions.txt, full_test.sh, jq-manual.txt, parser.y, lexer.l, builtin.jq, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 66829
budget: over-target
provides: staged conformance corpus, exclusions, runner, scoring entry point
consumes: interpreter architecture
instructions: |
  Stage every supplied source asset byte-for-byte under sources/. Validate the corpus and
  exclusions by importing the runner parsers directly. Do not modify scoring assets and do not
  execute the candidate interpreter in this staging story.
acceptance: yes
depends: architecture
state: pending
scope: both

## story 6: Implement stream-based filter evaluation.
id: core-001
summary: Implement stream-based filter evaluation.
type: service
kind: capability
phase: 2
block: 6
implements: FEATURE-Core-Generator.md
covers: CORE-001
context: jq-manual.txt, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 53512
budget: over-target
provides: generator evaluator, identity, empty, pipeline, comma
consumes: jq AST
instructions: |
  Implement the stream evaluator so filters produce ordered zero-, one-, or many-value streams.
  Preserve pipeline backtracking, comma ordering, multiplicity, cartesian behavior, and partial
  output before runtime errors.
acceptance: yes
depends: frontend-003
state: pending
scope: target

## story 7: Implement jq values, indexing, iteration, slicing, and construction.
id: core-002
summary: Implement jq values, indexing, iteration, slicing, and construction.
type: service
kind: capability
phase: 2
block: 7
implements: FEATURE-Core-Values.md
covers: CORE-002
context: jq-manual.txt, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 53292
budget: over-target
provides: literals, field access, indexing, iteration, slices, arrays, objects
consumes: generator evaluator
instructions: |
  Implement JSON values, identity and literals, object and array construction, field and indexed
  access, optional access, iteration, negative indices, and slices with jq semantics.
acceptance: yes
depends: core-001
state: pending
scope: target

## story 8: Implement jq operators and comparisons.
id: core-003
summary: Implement jq operators and comparisons.
type: service
kind: capability
phase: 2
block: 8
implements: FEATURE-Core-Operators.md
covers: CORE-003
context: jq-manual.txt, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 53322
budget: over-target
provides: arithmetic, concatenation, merge, equality, ordering, boolean, alternative, optional operators
consumes: generator evaluator, jq values
instructions: |
  Implement arithmetic and type-directed operators, recursive and shallow merge, comparisons,
  boolean operators, defined-or, negation, and error behavior.
acceptance: yes
depends: core-002
state: pending
scope: target

## story 9: Implement jq path discovery and path access.
id: paths-001
summary: Implement jq path discovery and path access.
type: service
kind: capability
phase: 3
block: 9
implements: FEATURE-Paths-Access.md
covers: PATHS-001
context: jq-manual.txt, jq.test, builtin.jq, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 55685
budget: over-target
provides: path, paths, getpath
consumes: generator evaluator, jq values, jq operators
instructions: |
  Implement path expressions, exact and pattern path discovery, paths traversal, and getpath
  semantics including missing and nested values.
acceptance: yes
depends: core-003
state: pending
scope: target

## story 10: Implement jq path mutation and deletion.
id: paths-002
summary: Implement jq path mutation and deletion.
type: service
kind: capability
phase: 3
block: 10
implements: FEATURE-Paths-Mutation.md
covers: PATHS-002
context: jq-manual.txt, jq.test, builtin.jq, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 55697
budget: over-target
provides: setpath, delpaths, del
consumes: path, paths, getpath
instructions: |
  Implement immutable nested path updates, creation of missing containers, deletion of object
  fields and array ranges, invalid-path errors, and deep-path limits.
acceptance: yes
depends: paths-001
state: pending
scope: target

## story 11: Implement jq assignment operators.
id: paths-003
summary: Implement jq assignment operators.
type: service
kind: capability
phase: 3
block: 11
implements: FEATURE-Paths-Assignment.md
covers: PATHS-003
context: jq-manual.txt, jq.test, builtin.jq, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 55737
budget: over-target
provides: =, |=, +=, -=, *=, /=, %=, //=
consumes: path mutation and deletion
instructions: |
  Implement plain, update, arithmetic, and defined-or assignments over generator-produced paths,
  preserving immutable values, multiplicity, deletion on empty updates, and RHS semantics.
acceptance: yes
depends: paths-002
state: pending
scope: target

## story 12: Implement jq conditionals, errors, try/catch, labels, and breaks.
id: control-001
summary: Implement jq conditionals, errors, try/catch, labels, and breaks.
type: service
kind: capability
phase: 4
block: 12
implements: FEATURE-Control-Errors.md
covers: CONTROL-001
context: jq-manual.txt, jq.test, parser.y, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 59178
budget: over-target
provides: conditionals, error, halt, try/catch, labels, break
consumes: generator evaluator, assignment operators
instructions: |
  Implement if/then/elif/else, runtime errors, compile and runtime exit distinctions, try/catch,
  optional suppression, lexical labels, and break control flow.
acceptance: yes
depends: paths-003
state: pending
scope: target

## story 13: Implement jq reduction and iteration constructs.
id: control-002
summary: Implement jq reduction and iteration constructs.
type: service
kind: capability
phase: 4
block: 13
implements: FEATURE-Control-Reduce.md
covers: CONTROL-002
context: jq-manual.txt, jq.test, builtin.jq, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 55992
budget: over-target
provides: reduce, foreach, limit, skip, first, last, nth, while, until, repeat
consumes: generator evaluator, errors, labels
instructions: |
  Implement reducers, extractors, bounded and skipped generators, first/last/nth, while, until,
  and repeat with correct stream ordering, state progression, short-circuiting, and breaks.
acceptance: yes
depends: control-001
state: pending
scope: target

## story 14: Implement jq recursion and recursive descent.
id: control-003
summary: Implement jq recursion and recursive descent.
type: service
kind: capability
phase: 4
block: 14
implements: FEATURE-Control-Recursion.md
covers: CONTROL-003
context: jq-manual.txt, jq.test, builtin.jq, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 55935
budget: over-target
provides: recurse, recursive descent
consumes: generator evaluator, control flow
instructions: |
  Implement recurse variants, .., recursive traversal order, recursive conditions, and safe
  recursive generator evaluation.
acceptance: yes
depends: control-002
state: pending
scope: target

## story 15: Implement jq variables and destructuring.
id: functions-001
summary: Implement jq variables and destructuring.
type: service
kind: capability
phase: 5
block: 15
implements: FEATURE-Functions-Bindings.md
covers: FUNCTIONS-001
context: jq-manual.txt, jq.test, parser.y, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 59183
budget: over-target
provides: lexical variables, bindings, array/object patterns, ?// destructuring
consumes: jq AST, generator evaluator, control flow
instructions: |
  Implement lexical bindings, variable scope, array and object destructuring, closures over
  bindings, missing-value null binding, and destructuring alternatives with backtracking.
acceptance: yes
depends: control-003
state: pending
scope: target

## story 16: Implement jq user-defined functions.
id: functions-002
summary: Implement jq user-defined functions.
type: service
kind: capability
phase: 5
block: 16
implements: FEATURE-Functions-Definitions.md
covers: FUNCTIONS-002
context: jq-manual.txt, jq.test, parser.y, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 59176
budget: over-target
provides: def declarations, filter arguments, value arguments, recursion, function scope
consumes: variables and destructuring, jq AST, generator evaluator
instructions: |
  Implement def declarations, arity, filter and value parameters, lexical function scope,
  redefinition, closures, recursive functions, and generator backtracking through calls.
acceptance: yes
depends: functions-001
state: pending
scope: target

## story 17: Implement core jq type, collection, and string builtins.
id: builtins-001
summary: Implement core jq type, collection, and string builtins.
type: service
kind: capability
phase: 6
block: 17
implements: FEATURE-Builtins-Core.md
covers: BUILTINS-001
context: builtin.jq, jq-manual.txt, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 56005
budget: over-target
provides: type and collection builtins, sorting, grouping, containment, string operations, Unicode helpers
consumes: user-defined functions, variables, paths, control flow
instructions: |
  Implement type predicates, collection transforms, sorting/grouping/uniqueness, containment,
  indexing helpers, string trimming/splitting/joining, Unicode conversion, and related builtins.
acceptance: yes
depends: functions-002
state: pending
scope: target

## story 18: Implement jq regular-expression builtins.
id: builtins-002
summary: Implement jq regular-expression builtins.
type: service
kind: capability
phase: 6
block: 18
implements: FEATURE-Builtins-Regex.md
covers: BUILTINS-002
context: jq-manual.txt, jq.test, builtin.jq, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 55931
budget: over-target
provides: test, match, capture, scan, split, splits, sub, gsub
consumes: user-defined functions, strings, generator evaluator
instructions: |
  Implement regex matching and replacement builtins using Python standard-library regular
  expressions, including flags, captures, global streams, splits, substitutions, and errors.
acceptance: yes
depends: builtins-001
state: pending
scope: target

## story 19: Implement jq serialization, formats, dates, math, and streaming builtins.
id: builtins-003
summary: Implement jq serialization, formats, dates, math, and streaming builtins.
type: service
kind: capability
phase: 6
block: 19
implements: FEATURE-Builtins-Extended.md
covers: BUILTINS-003
context: jq-manual.txt, jq.test, builtin.jq, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 56043
budget: over-target
provides: JSON conversion, @ formats, dates, math, SQL-style operators, streaming utilities
consumes: regex builtins, collection builtins, generator evaluator
instructions: |
  Implement tojson/fromjson, format encoders, date/time functions, mathematical functions,
  SQL-style INDEX/JOIN/IN, stream conversion, environment and I/O-compatible builtins supported
  by the fixed CLI contract.
acceptance: yes
depends: builtins-002
state: pending
scope: target

## story 20: Implement the executable jq command-line interface.
id: cli-001
summary: Implement the executable jq command-line interface.
type: service
kind: capability
phase: 7
block: 20
implements: FEATURE-CLI-Executable.md
covers: CLI-001
context: full_test.sh, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 11641
provides: executable jq, -c program interface, JSON stdin/stdout protocol, exit codes 0/3/5
consumes: complete evaluator
instructions: |
  Deliver an executable named jq at the application root. Accept -c and one jq program, read JSON
  inputs from stdin, emit compact JSON values one per line, write diagnostics to stderr, and return
  exit status 0 for completion, 3 for compile failure, and 5 for runtime failure.
acceptance: yes
depends: builtins-003
state: pending
scope: target

## story 21: Prove complete jq conformance.
id: cli-003
summary: Prove complete jq conformance.
type: service
kind: test harness
phase: 8
block: 21
implements: FEATURE-CLI-Conformance.md
covers: CLI-003
accepts: st-001
context: full_test.sh, run_conformance.py, jq.test, exclusions.txt, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 24859
provides: complete conformance proof
consumes: executable jq, staged conformance harness
instructions: |
  Run the supplied complete scoring command from the application root, print captured stdout and
  stderr for diagnosis, and require its exit status to be zero. This is the terminal verification
  story and the only story that runs the entire corpus.
acceptance: yes
depends: architecture, frontend-001, frontend-002, frontend-003, core-001, core-002, core-003, paths-001, paths-002, paths-003, control-001, control-002, control-003, functions-001, functions-002, builtins-001, builtins-002, builtins-003, cli-001, cli-002
state: pending
scope: target
