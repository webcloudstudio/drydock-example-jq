# MANIFEST: jq
updated:     2026-08-22T05:04:46+00:00
state:       approved
blocks:      38

## story 1: Establish the standalone Python interpreter architecture and executable boundary.
id:           architecture-foundation
summary:      Establish the standalone Python interpreter architecture and executable boundary.
type:         foundational
kind:         capability
phase:        1
block:        1
implements:   ARCHITECTURE.md
scope:        target
instructions: |
  Establish the module boundaries for lexing, parsing, generator evaluation, builtins, runtime errors, and CLI serialization. Keep the implementation standard-library-only and prevent shelling out to any jq implementation.
stack:        common.md, python.md
stack_mode:   builder
size:         9292
provides:     jq interpreter architecture
acceptance:   yes
state:        pending

## story 2: Implement the executable jq entry point.
id: EXEC-001
summary: Implement the executable jq entry point.
type: foundational
kind: capability
phase: 1
block: 1
implements: FEATURE-Executable-Entry-Point.md
covers: EXEC-001
context: ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 10008
provides: ./jq -c program interface
consumes: jq interpreter architecture
instructions: Deliver an executable named jq at the application root. Accept the exercised -c program interface, read JSON from standard input, evaluate the program, and emit compact JSON values one per line.
acceptance: yes
depends: architecture-foundation
state: pending
scope: target

## story 3: Implement jq process exit and diagnostic behavior.
id: EXEC-002
summary: Implement jq process exit and diagnostic behavior.
type: service
kind: capability
phase: 1
block: 2
implements: FEATURE-Process-Contract.md
covers: EXEC-002
context: ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 10029
provides: compile and runtime exit contract
consumes: ./jq -c program interface
instructions: Distinguish compile failures with exit 3, runtime failures with exit 5, and successful completion with exit 0. Send diagnostics only to stderr and preserve output emitted before a runtime failure.
acceptance: yes
depends: EXEC-001
state: pending
scope: target

## story 4: Implement JSON input and compact output handling.
id: EXEC-003
summary: Implement JSON input and compact output handling.
type: service
kind: capability
phase: 1
block: 2
implements: FEATURE-JSON-I-O.md
covers: EXEC-003
context: ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 10627
provides: JSON input stream and compact JSON output
consumes: compile and runtime exit contract
instructions: Parse multiple JSON input values, preserve Unicode and special numeric behavior required by the corpus, and serialize every produced value as one compact JSON value per line.
acceptance: yes
depends: EXEC-002
state: blocked/questions
scope: target

## story 5: Implement jq lexical scanning.
id: PARSE-001
summary: Implement jq lexical scanning.
type: service
kind: capability
phase: 1
block: 2
implements: FEATURE-Lexer.md
covers: PARSE-001
context: lexer.l, parser.y, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 12984
provides: jq tokenization
consumes: JSON input stream and compact JSON output
instructions: Implement identifiers, fields, bindings, keywords, literals, operators, delimiters, comments, formats, and lexical rejection behavior according to the supplied lexer reference.
acceptance: yes
depends: EXEC-003
state: pending
scope: target

## story 6: Implement literals, strings, escapes, and interpolation.
id: PARSE-002
summary: Implement literals, strings, escapes, and interpolation.
type: service
kind: capability
phase: 1
block: 2
implements: FEATURE-Literals-and-Strings.md
covers: PARSE-002
context: lexer.l, parser.y, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 26152
provides: jq string and literal expressions
consumes: jq tokenization
instructions: Parse JSON escapes, Unicode strings, formatted strings, and \(expression) interpolation, including invalid escape rejection.
acceptance: yes
depends: PARSE-001
state: blocked/questions
scope: target

## story 7: Implement the core jq filter expression grammar.
id: PARSE-003
summary: Implement the core jq filter expression grammar.
type: service
kind: capability
phase: 1
block: 2
implements: FEATURE-Filter-Grammar.md
covers: PARSE-003
context: parser.y, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 25031
provides: jq filter AST
consumes: jq string and literal expressions
instructions: Implement precedence and parsing for pipes, commas, indexing, slicing, arrays, objects, unary operators, binary operators, parentheses, and optional expressions.
acceptance: yes
depends: PARSE-002
state: blocked/questions
scope: target

## story 8: Implement declarations, control syntax, and grammar rejection.
id: PARSE-004
summary: Implement declarations, control syntax, and grammar rejection.
type: service
kind: capability
phase: 1
block: 2
implements: FEATURE-Advanced-Grammar.md
covers: PARSE-004
context: parser.y, lexer.l, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 26062
provides: declarations and control-flow AST forms
consumes: jq filter AST
instructions: Parse definitions, imports and modules, conditionals, try/catch, reductions, foreach, labels, bindings, and destructuring. Reject invalid module grammar and other %%FAIL programs with compile exit 3 without loading module fixtures.
acceptance: yes
depends: PARSE-003
state: pending
scope: target

## story 9: Implement stream-valued filter evaluation.
id: CORE-001
summary: Implement stream-valued filter evaluation.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-Generator-Core.md
covers: CORE-001
context: jq-manual.txt, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 52116
budget: over-target
provides: ordered jq generator evaluation
consumes: jq filter AST
instructions: Evaluate filters as ordered streams with zero, one, or many outputs, preserving backtracking, multiplicity, and generator ordering.
acceptance: yes
depends: PARSE-004
state: blocked/questions
scope: target

## story 10: Implement composition and cartesian evaluation.
id: CORE-002
summary: Implement composition and cartesian evaluation.
type: service
kind: capability
phase: 1
block: 4
implements: FEATURE-Composition.md
covers: CORE-002
context: jq-manual.txt, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 52000
budget: over-target
provides: pipe, comma, collection, object, and cartesian semantics
consumes: ordered jq generator evaluation
instructions: Implement composition of streams, cartesian products for filter arguments, array collection, object construction, and multi-output operator behavior.
acceptance: yes
depends: CORE-001
state: pending
scope: target

## story 11: Implement empty, runtime errors, optional evaluation, and partial output.
id: CORE-003
summary: Implement empty, runtime errors, optional evaluation, and partial output.
type: service
kind: capability
phase: 1
block: 5
implements: FEATURE-Errors-and-Optional.md
covers: CORE-003
context: jq-manual.txt, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 52004
budget: over-target
provides: empty, error, try, catch, and optional semantics
consumes: ordered jq generator evaluation
instructions: Implement empty streams, runtime errors, try/catch, the ? operator, and preservation of outputs emitted before a runtime error.
acceptance: yes
depends: CORE-002, EXEC-002
state: pending
scope: target

## story 12: Implement truthiness, equality, and ordering semantics.
id: CORE-004
summary: Implement truthiness, equality, and ordering semantics.
type: service
kind: capability
phase: 1
block: 6
implements: FEATURE-Truthiness-and-Comparison.md
covers: CORE-004
context: jq-manual.txt, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 51992
budget: over-target
provides: jq truthiness and comparison
consumes: ordered jq generator evaluation
instructions: Treat only false and null as falsey and implement structural equality, numeric equivalence, and jq type ordering.
acceptance: yes
depends: CORE-002
state: pending
scope: target

## story 13: Implement the jq value model and numeric edge cases.
id: VALUE-001
summary: Implement the jq value model and numeric edge cases.
type: service
kind: capability
phase: 1
block: 7
implements: FEATURE-Value-Model.md
covers: VALUE-001
context: jq-manual.txt, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 52005
budget: over-target
provides: jq JSON values, NaN, and infinities
consumes: JSON input stream and compact JSON output
instructions: Represent null, booleans, numbers, strings, arrays, objects, NaN, and infinities with the numeric conversion and serialization behavior required by the corpus.
acceptance: yes
depends: EXEC-003, CORE-004
state: pending
scope: target

## story 14: Implement field and index access.
id: VALUE-002
summary: Implement field and index access.
type: service
kind: capability
phase: 1
block: 8
implements: FEATURE-Accessors.md
covers: VALUE-002
context: jq-manual.txt, jq.test, parser.y, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 57713
budget: over-target
provides: field, index, optional, and negative-index access
consumes: jq value model and ordered jq generator evaluation
instructions: Implement object fields, array indices, dynamic keys, optional access, missing values, and negative indices with jq error behavior.
acceptance: yes
depends: VALUE-001, CORE-001
state: blocked/questions
scope: target

## story 15: Implement slices and collection iteration.
id: VALUE-003
summary: Implement slices and collection iteration.
type: service
kind: capability
phase: 1
block: 9
implements: FEATURE-Slices-and-Iteration.md
covers: VALUE-003
context: jq-manual.txt, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 52000
budget: over-target
provides: array/string slices and array/object iteration
consumes: field, index, optional, and negative-index access
instructions: Implement array and string slices, iteration over arrays and objects, optional iteration, fractional bounds, and out-of-range behavior.
acceptance: yes
depends: VALUE-002
state: pending
scope: target

## story 16: Implement type, length, numeric predicates, and math primitives.
id: VALUE-004
summary: Implement type, length, numeric predicates, and math primitives.
type: service
kind: capability
phase: 1
block: 10
implements: FEATURE-Type-and-Numeric-Primitives.md
covers: VALUE-004
context: jq-manual.txt, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 52131
budget: over-target
provides: type and numeric builtin filters
consumes: jq value model
instructions: Implement type, length, utf8bytelength, numeric predicates, conversion functions, arithmetic primitives, and required standard-library math functions.
acceptance: yes
depends: VALUE-001, CORE-004
state: blocked/questions
scope: target

## story 17: Stage and validate immutable conformance assets.
id: CONF-001
summary: Stage and validate immutable conformance assets.
type: foundational
kind: test harness
phase: 1
block: 11
implements: FEATURE-Conformance-Assets.md
covers: CONF-001
context: run_conformance.py, jq.test, exclusions.txt, full_test.sh, jq-manual.txt, parser.y, lexer.l, builtin.jq, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 70116
budget: over-target
provides: staged conformance corpus and harness
consumes: jq interpreter architecture
instructions: Stage all supplied sources unchanged in the required sources directory. Validate corpus parsing, exclusion consistency, and the expected complete asset set by importing the harness parsers directly. Do not launch the candidate or alter any source asset.
acceptance: yes
depends: architecture-foundation
state: pending
scope: both

## story 18: Implement arithmetic and structural operators.
id: FLOW-001
summary: Implement arithmetic and structural operators.
type: service
kind: capability
phase: 2
block: 12
implements: FEATURE-Arithmetic-and-Structural-Operators.md
covers: FLOW-001
context: jq-manual.txt, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 52128
budget: over-target
provides: jq arithmetic and structural operators
consumes: jq value model and comparison semantics
instructions: Implement +, -, *, /, %, unary negation, recursive object merge, string repetition, and string splitting with jq type errors and numeric behavior.
acceptance: yes
depends: VALUE-004, CORE-002
state: blocked/questions
scope: target

## story 19: Implement boolean and alternative operators.
id: FLOW-002
summary: Implement boolean and alternative operators.
type: service
kind: capability
phase: 2
block: 13
implements: FEATURE-Boolean-and-Alternative-Operators.md
covers: FLOW-002
context: jq-manual.txt, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 52120
budget: over-target
provides: and, or, not, //, and //=
consumes: jq truthiness and comparison
instructions: Implement boolean operators, not, defined-or fallback, short-circuiting, and defined-or assignment while preserving generator semantics.
acceptance: yes
depends: CORE-004, CORE-003
state: blocked/questions
scope: target

## story 20: Implement conditionals and exception flow.
id: FLOW-003
summary: Implement conditionals and exception flow.
type: service
kind: capability
phase: 2
block: 14
implements: FEATURE-Conditionals-and-Exception-Flow.md
covers: FLOW-003
context: parser.y, jq-manual.txt, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 57713
budget: over-target
provides: if, elif, else, try, catch, and optional control flow
consumes: empty, error, try, catch, and optional semantics
instructions: Implement branch streams, optional else behavior, try/catch propagation, and optional operators across nested control flow.
acceptance: yes
depends: CORE-003, FLOW-002
state: blocked/questions
scope: target

## story 21: Implement lexical labels and breaks.
id: FLOW-004
summary: Implement lexical labels and breaks.
type: service
kind: capability
phase: 2
block: 15
implements: FEATURE-Labels-and-Breaks.md
covers: FLOW-004
context: parser.y, jq-manual.txt, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 57706
budget: over-target
provides: label and break control
consumes: conditionals and exception flow
instructions: Implement lexically scoped labels and breaks that terminate only the corresponding generator and reject unbound breaks at compile time.
acceptance: yes
depends: FLOW-003
state: blocked/questions
scope: target

## story 22: Implement reductions and iteration-control builtins.
id: FLOW-005
summary: Implement reductions and iteration-control builtins.
type: service
kind: capability
phase: 2
block: 16
implements: FEATURE-Reductions-and-Iteration-Control.md
covers: FLOW-005
context: parser.y, jq-manual.txt, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 57603
budget: over-target
provides: reduce, foreach, range, limit, skip, first, last, and nth
consumes: labels and breaks, ordered jq generators
instructions: Implement stateful reductions, foreach extraction, ranges, limiting, skipping, first/last/nth, cartesian arguments, and backtracking.
acceptance: yes
depends: FLOW-004, CORE-001
state: pending
scope: target

## story 23: Implement recursive generators.
id: FLOW-006
summary: Implement recursive generators.
type: service
kind: capability
phase: 2
block: 17
implements: FEATURE-Recursive-Generators.md
covers: FLOW-006
context: jq-manual.txt, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 52122
budget: over-target
provides: while, until, repeat, recurse, and recursive descent
consumes: ordered jq generator evaluation and conditionals
instructions: Implement while, until, repeat, recurse, recursive descent, and safe termination behavior for recursive generator expressions.
acceptance: yes
depends: FLOW-005, FLOW-003
state: blocked/questions
scope: target

## story 24: Implement lexical variable bindings.
id: FUNC-001
summary: Implement lexical variable bindings.
type: service
kind: capability
phase: 2
block: 18
implements: FEATURE-Variable-Bindings.md
covers: FUNC-001
context: parser.y, jq-manual.txt, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 57712
budget: over-target
provides: as bindings, variables, shadowing, and patterns
consumes: jq filter AST and ordered jq generators
instructions: Implement as bindings, nested lexical scope, shadowing, keyword identifiers, destructuring patterns, and value lifetime.
acceptance: yes
depends: PARSE-004, CORE-001
state: blocked/questions
scope: target

## story 25: Implement filter and value function parameters.
id: FUNC-002
summary: Implement filter and value function parameters.
type: service
kind: capability
phase: 2
block: 19
implements: FEATURE-Function-Parameters.md
covers: FUNC-002
context: parser.y, jq-manual.txt, builtin.jq, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 60016
budget: over-target
provides: filter and value function arguments
consumes: lexical variable bindings and generator evaluation
instructions: Implement user-defined functions with filter parameters, value parameters, multiple arities, closures, and cartesian argument evaluation.
acceptance: yes
depends: FUNC-001, CORE-002
state: pending
scope: target

## story 26: Implement function definitions, scope, redefinition, and recursion.
id: FUNC-003
summary: Implement function definitions, scope, redefinition, and recursion.
type: service
kind: capability
phase: 2
block: 20
implements: FEATURE-Function-Definitions.md
covers: FUNC-003
context: parser.y, jq-manual.txt, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 57717
budget: over-target
provides: lexical function definitions and recursion
consumes: filter and value function arguments
instructions: Implement definitions, forward and self references, lexical function scope, redefinitions by arity, and recursive user functions.
acceptance: yes
depends: FUNC-002
state: blocked/questions
scope: target

## story 27: Implement destructuring alternatives.
id: FUNC-004
summary: Implement destructuring alternatives.
type: service
kind: capability
phase: 2
block: 21
implements: FEATURE-Destructuring-Alternatives.md
covers: FUNC-004
context: parser.y, jq-manual.txt, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 57712
budget: over-target
provides: ?// destructuring alternatives
consumes: lexical variable bindings and exception flow
instructions: Implement array and object destructuring, missing bindings, ?// alternatives, fallback binding behavior, and error-triggered alternative selection.
acceptance: yes
depends: FUNC-001, FLOW-003
state: blocked/questions
scope: target

## story 28: Implement path discovery and projection.
id: PATH-001
summary: Implement path discovery and projection.
type: service
kind: capability
phase: 2
block: 22
implements: FEATURE-Path-Discovery.md
covers: PATH-001
context: jq-manual.txt, jq.test, builtin.jq, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 54518
budget: over-target
provides: path, paths, and pick
consumes: accessors, slices, and recursive generators
instructions: Implement exact and generated paths, path filtering, paths, and projections with valid path arrays and path-expression errors.
acceptance: yes
depends: VALUE-003, FLOW-006
state: blocked/questions
scope: target

## story 29: Implement path access and mutation primitives.
id: PATH-002
summary: Implement path access and mutation primitives.
type: service
kind: capability
phase: 2
block: 23
implements: FEATURE-Path-Primitives.md
covers: PATH-002
context: jq-manual.txt, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 51997
budget: over-target
provides: getpath, setpath, and delpaths
consumes: path discovery and jq value model
instructions: Implement nested path reads, creation and replacement, deletion, array expansion, invalid-path errors, depth limits, and immutable updates.
acceptance: yes
depends: PATH-001, VALUE-002
state: pending
scope: target

## story 30: Implement deletion and assignment operators.
id: PATH-003
summary: Implement deletion and assignment operators.
type: service
kind: capability
phase: 2
block: 24
implements: FEATURE-Assignment-Operators.md
covers: PATH-003
context: jq-manual.txt, jq.test, builtin.jq, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 54404
budget: over-target
provides: del, =, |=, +=, -=, *=, /=, %=, and //=
consumes: getpath, setpath, and delpaths
instructions: Implement deletion, plain assignment, update assignment, arithmetic assignment, defined-or assignment, multiple paths, and immutable output behavior.
acceptance: yes
depends: PATH-002, FLOW-002
state: pending
scope: target

## story 31: Implement complex assignment edge cases.
id: PATH-004
summary: Implement complex assignment edge cases.
type: service
kind: capability
phase: 2
block: 25
implements: FEATURE-Complex-Assignments.md
covers: PATH-004
context: jq.test, jq-manual.txt, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 52111
budget: over-target
provides: complex assignment edge-case behavior
consumes: deletion and assignment operators
instructions: Handle iterated paths, empty updates, array expansion, invalid paths, negative and NaN indices, deep paths, and partial assignment failures.
acceptance: yes
depends: PATH-003, FLOW-005
state: blocked/questions
scope: target

## story 32: Implement collection transformation builtins.
id: DATA-001
summary: Implement collection transformation builtins.
type: service
kind: capability
phase: 2
block: 26
implements: FEATURE-Collection-Transformations.md
covers: DATA-001
context: builtin.jq, jq-manual.txt, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 54408
budget: over-target
provides: map, map_values, select, add, flatten, transpose, combinations, and walk
consumes: generator evaluation and assignment
instructions: Implement collection transformations and recursive walk semantics, including empty streams and bounded flattening.
acceptance: yes
depends: CORE-002, PATH-003, FLOW-006
state: pending
scope: target

## story 33: Implement sorting, grouping, and extrema builtins.
id: DATA-002
summary: Implement sorting, grouping, and extrema builtins.
type: service
kind: capability
phase: 2
block: 27
implements: FEATURE-Sorting-and-Grouping.md
covers: DATA-002
context: jq-manual.txt, builtin.jq, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 54518
budget: over-target
provides: sort, sort_by, group_by, unique, unique_by, min, max, min_by, and max_by
consumes: jq comparison and generator semantics
instructions: Implement jq ordering, keyed sorting, grouping, uniqueness, minima, maxima, and deep comparison limits.
acceptance: yes
depends: CORE-004, DATA-001
state: blocked/questions
scope: target

## story 34: Implement object-entry and containment builtins.
id: DATA-003
summary: Implement object-entry and containment builtins.
type: service
kind: capability
phase: 2
block: 28
implements: FEATURE-Object-Entries-and-Containment.md
covers: DATA-003
context: jq-manual.txt, builtin.jq, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 54405
budget: over-target
provides: keys, keys_unsorted, has, in, inside, contains, to_entries, from_entries, and with_entries
consumes: jq value model and comparison semantics
instructions: Implement object and array key utilities, containment and inverse containment, entry conversion, and entry transformations.
acceptance: yes
depends: VALUE-002, CORE-004, DATA-001
state: pending
scope: target

## story 35: Implement index, membership, search, and SQL-style utilities.
id: DATA-004
summary: Implement index, membership, search, and SQL-style utilities.
type: service
kind: capability
phase: 2
block: 29
implements: FEATURE-Index-and-Membership.md
covers: DATA-004
context: jq-manual.txt, builtin.jq, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 54408
budget: over-target
provides: indices, index, rindex, bsearch, all, any, isempty, INDEX, JOIN, and IN
consumes: collection transformations and comparison semantics
instructions: Implement array and string search, binary search, quantifiers, emptiness checks, and SQL-style index, join, and membership functions.
acceptance: yes
depends: DATA-002, DATA-003, FLOW-005
state: pending
scope: target

## story 36: Implement string manipulation builtins.
id: TEXT-001
summary: Implement string manipulation builtins.
type: service
kind: capability
phase: 2
block: 30
implements: FEATURE-String-Manipulation.md
covers: TEXT-001
context: jq-manual.txt, builtin.jq, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 54538
budget: over-target
provides: trimming, case, codepoint, split, join, prefix, and suffix filters
consumes: jq string and value primitives
instructions: Implement trimming, prefix and suffix operations, ASCII case conversion, explode and implode, split, join, and interpolation-related string behavior.
acceptance: yes
depends: VALUE-004, FLOW-001
state: blocked/questions
scope: target

## story 37: Implement JSON conversion and output formats.
id: TEXT-002
summary: Implement JSON conversion and output formats.
type: service
kind: capability
phase: 2
block: 31
implements: FEATURE-Formats-and-Serialization.md
covers: TEXT-002
context: jq-manual.txt, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 51995
budget: over-target
provides: tostring, tojson, fromjson, @text, @json, @html, @uri, @urid, @csv, @tsv, @sh, @base64, and @base64d
consumes: jq value model and string manipulation
instructions: Implement JSON conversion and all required format filters with escaping, encoding, decoding, interpolation, and compact serialization semantics.
acceptance: yes
depends: TEXT-001, VALUE-001
state: pending
scope: target

## story 38: Implement regular-expression filters.
id: TEXT-003
summary: Implement regular-expression filters.
type: service
kind: capability
phase: 2
block: 32
implements: FEATURE-Regular-Expressions.md
covers: TEXT-003
context: jq-manual.txt, builtin.jq, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 54544
budget: over-target
provides: test, match, capture, scan, split, splits, sub, and gsub
consumes: jq string manipulation and generator evaluation
instructions: Implement regular-expression matching, flags, named captures, offsets, streams, splitting, substitution, and global substitution using the Python standard library.
acceptance: yes
depends: TEXT-001, CORE-001
state: blocked/questions
scope: target

## story 39: Implement date and time filters.
id: TEXT-004
summary: Implement date and time filters.
type: service
kind: capability
phase: 2
block: 33
implements: FEATURE-Date-and-Time.md
covers: TEXT-004
context: jq-manual.txt, builtin.jq, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 54960
budget: over-target
provides: strptime, strftime, strflocaltime, gmtime, localtime, mktime, fromdate, and todate
consumes: jq string and numeric primitives
instructions: Implement UTC ISO dates, low-level broken-down time conversion, formatting, parsing, and the supplied timezone behavior.
acceptance: yes
depends: VALUE-004, TEXT-001
state: blocked/questions
scope: target

## story 40: Implement input stream controls.
id: IO-001
summary: Implement input stream controls.
type: service
kind: capability
phase: 2
block: 34
implements: FEATURE-Input-Controls.md
covers: IO-001
context: jq-manual.txt, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 52539
budget: over-target
provides: input, inputs, input_filename, and input_line_number
consumes: JSON input stream and generator evaluation
instructions: Implement input stream consumption and input metadata within the fixed stdin interface, preserving interaction with ordinary filter input.
acceptance: yes
depends: EXEC-003, CORE-001
state: blocked/questions
scope: target

## story 41: Implement diagnostics and stderr filters.
id: IO-002
summary: Implement diagnostics and stderr filters.
type: service
kind: capability
phase: 2
block: 35
implements: FEATURE-Diagnostics.md
covers: IO-002
context: jq-manual.txt, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 52518
budget: over-target
provides: debug, stderr, and halt_error
consumes: process exit and diagnostic behavior
instructions: Implement debug and stderr side effects, raw stderr output, halt_error exit behavior, and preservation of stdout semantics.
acceptance: yes
depends: EXEC-002, CORE-003
state: blocked/questions
scope: target

## story 42: Implement streaming transformations.
id: IO-003
summary: Implement streaming transformations.
type: service
kind: capability
phase: 2
block: 36
implements: FEATURE-Streaming.md
covers: IO-003
context: jq-manual.txt, builtin.jq, jq.test, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 54398
budget: over-target
provides: tostream, fromstream, and truncate_stream
consumes: input controls and generator evaluation
instructions: Implement jq stream-form conversion, reconstruction, and path truncation for the supplied streaming cases.
acceptance: yes
depends: IO-001, CORE-001
state: pending
scope: target

## story 43: Provide scoped conformance verification for implementation slices.
id: CONF-002
summary: Provide scoped conformance verification for implementation slices.
type: service
kind: test harness
phase: 2
block: 37
implements: FEATURE-Scoped-Conformance.md
covers: CONF-002
context: run_conformance.py, jq.test, exclusions.txt, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 24467
provides: scoped conformance verification
consumes: staged conformance corpus and harness, ./jq -c program interface
instructions: Bind scoped acceptance checks to the supplied conformance runner with JQ supplied through the inherited environment. Each implementing slice must execute matching cases and assert the parsed report has no failures or errors and matched a non-empty case set.
acceptance: yes
depends: CONF-001, EXEC-001
state: blocked/questions
scope: both

## story 44: Verify the completed interpreter against the full conformance corpus.
id: CONF-003
summary: Verify the completed interpreter against the full conformance corpus.
type: feature
kind: test harness
phase: 3
block: 38
implements: FEATURE-Full-Conformance.md
covers: CONF-003
accepts: st-001
context: full_test.sh, run_conformance.py, jq.test, exclusions.txt, ARCHITECTURE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 24937
provides: complete jq conformance verification
consumes: scoped conformance verification
instructions: Assemble the completed interpreter and run the supplied full scoring entry point from the application root. This is the terminal verification story and its full-suite acceptance must require the command to exit successfully.
acceptance: yes
depends: EXEC-001, EXEC-002, EXEC-003, PARSE-001, PARSE-002, PARSE-003, PARSE-004, CORE-001, CORE-002, CORE-003, CORE-004, VALUE-001, VALUE-002, VALUE-003, VALUE-004, FLOW-001, FLOW-002, FLOW-003, FLOW-004, FLOW-005, FLOW-006, FUNC-001, FUNC-002, FUNC-003, FUNC-004, PATH-001, PATH-002, PATH-003, PATH-004, DATA-001, DATA-002, DATA-003, DATA-004, TEXT-001, TEXT-002, TEXT-003, TEXT-004, IO-001, IO-002, IO-003, CONF-001, CONF-002
state: pending
scope: both
