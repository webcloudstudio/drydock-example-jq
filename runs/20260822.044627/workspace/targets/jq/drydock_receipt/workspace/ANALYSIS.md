# Blueprint Analysis: drydock jq Uat Kit

## Commander Expectations

- assert the supplied jq conformance corpus passes completely through an executable `./jq` filter.
- assert the implementation uses only Python standard-library facilities and does not wrap or depend on another jq implementation.
- assert the supplied stdin/stdout interface and documented exit codes are honored.

## Crew

| Crew | Charge |
|---|---|
| Commander | Defines intent and decides what done means. |
| Team Lead | Confirms epic completeness and stakeholder expectations. |
| Planning Crew | Authors atomic specifications and the ordered Manifest. |
| Shipyard Crew | Builds the tickets without synchronous Commander access. |

## Story List

### Feature: Executable Interface

| ID | Story | High-level AC |
|---|---|---|
| EXEC-001 | Implement executable jq entry point | `./jq -c '<program>'` reads JSON stdin and emits compact JSON values line by line. |
| EXEC-002 | Implement process exit and diagnostic contract | Compile failures exit 3, runtime failures exit 5, successful completion exits 0, and diagnostics use stderr. |
| EXEC-003 | Implement JSON input and output handling | Multiple input values, Unicode, special numeric values, and compact serialization are handled as required by the corpus. |

### Feature: Lexer and Parser

| ID | Story | High-level AC |
|---|---|---|
| PARSE-001 | Implement jq lexical scanning | Keywords, identifiers, fields, bindings, literals, operators, comments, formats, and delimiters tokenize according to the supplied lexer specification. |
| PARSE-002 | Implement literals and string interpolation | JSON escapes, Unicode, formatted strings, and `\(expression)` interpolation parse and evaluate correctly. |
| PARSE-003 | Implement filter expression grammar | Pipes, commas, precedence, indexing, slicing, arrays, objects, unary operators, and optional expressions compile correctly. |
| PARSE-004 | Implement declarations and control syntax | `def`, imports/module grammar, conditionals, try/catch, reductions, foreach, labels, bindings, and destructuring syntax compile correctly, including required rejection cases. |

### Feature: Generator Evaluation Core

| ID | Story | High-level AC |
|---|---|---|
| CORE-001 | Implement stream-valued filter evaluation | Every filter evaluates as a generator with zero, one, or many outputs, preserving order and backtracking. |
| CORE-002 | Implement composition and cartesian evaluation | Pipes, commas, function arguments, array collection, object construction, and binary operators evaluate all required output combinations. |
| CORE-003 | Implement empty, errors, and optional evaluation | `empty`, runtime errors, `?`, `try`, and partial output before runtime failure follow jq semantics. |
| CORE-004 | Implement truthiness and comparison semantics | Only `false` and `null` are falsey; equality and ordering follow jq's type ordering and numeric equivalence. |

### Feature: Values and Accessors

| ID | Story | High-level AC |
|---|---|---|
| VALUE-001 | Implement JSON value model | Null, booleans, numbers, strings, arrays, objects, NaN, and infinities are represented and processed as jq values. |
| VALUE-002 | Implement field and index access | Object fields, array indices, object values, optional access, negative indices, and missing values behave as specified. |
| VALUE-003 | Implement slices and iteration | Array/string slices, iteration over arrays and objects, optional iteration, fractional bounds, and out-of-range behavior conform. |
| VALUE-004 | Implement type and numeric primitives | `type`, `length`, `utf8bytelength`, numeric predicates, conversion functions, arithmetic primitives, and math functions conform. |

### Feature: Operators and Control Flow

| ID | Story | High-level AC |
|---|---|---|
| FLOW-001 | Implement arithmetic and structural operators | `+`, `-`, `*`, `/`, `%`, unary negation, recursive object merge, string repetition, and string splitting conform. |
| FLOW-002 | Implement boolean and alternative operators | `and`, `or`, `not`, `//`, and `//=` preserve generator and short-circuit semantics. |
| FLOW-003 | Implement conditionals and exception flow | `if`, `elif`, `else`, `try`, `catch`, and optional operators preserve branch streams and errors. |
| FLOW-004 | Implement labels and breaks | Lexically scoped `label` and `break` terminate the correct generator without leaking outputs. |
| FLOW-005 | Implement reductions and iteration control | `reduce`, `foreach`, `range`, `limit`, `skip`, `first`, `last`, and `nth` preserve state and backtracking. |
| FLOW-006 | Implement recursive generators | `while`, `until`, `repeat`, `recurse`, and recursive user functions operate correctly without incorrect termination. |

### Feature: Variables and Functions

| ID | Story | High-level AC |
|---|---|---|
| FUNC-001 | Implement lexical variable bindings | `as` bindings, nested scope, shadowing, keyword identifiers, and value lifetime conform. |
| FUNC-002 | Implement filter and value function parameters | User-defined functions support filter parameters, value parameters, multiple arities, closures, and cartesian arguments. |
| FUNC-003 | Implement function definitions and recursion | Definitions, redefinitions, lexical function scope, recursion, and forward/self references conform. |
| FUNC-004 | Implement destructuring patterns and alternatives | Array/object patterns, missing bindings, `?//`, and fallback binding behavior conform. |

### Feature: Paths and Assignment

| ID | Story | High-level AC |
|---|---|---|
| PATH-001 | Implement path discovery and projection | `path`, `paths`, `pick`, and path expressions produce valid paths and projections. |
| PATH-002 | Implement path access and mutation primitives | `getpath`, `setpath`, and `delpaths` create, update, read, and delete nested structures correctly. |
| PATH-003 | Implement deletion and assignment operators | `del`, `=`, `|=`, arithmetic assignments, defined-or assignment, and multi-path behavior conform. |
| PATH-004 | Implement complex assignment edge cases | Iterated paths, empty updates, array expansion, invalid paths, negative indices, NaN indices, and depth limits conform. |

### Feature: Collections and Data Transformation

| ID | Story | High-level AC |
|---|---|---|
| DATA-001 | Implement collection transformation builtins | `map`, `map_values`, `select`, `add`, `flatten`, `transpose`, `combinations`, and `walk` conform. |
| DATA-002 | Implement sorting and grouping builtins | `sort`, `sort_by`, `group_by`, `unique`, `unique_by`, `min`, `max`, and keyed variants conform. |
| DATA-003 | Implement object-entry and containment builtins | `keys`, `keys_unsorted`, `has`, `in`, `inside`, `contains`, `to_entries`, `from_entries`, and `with_entries` conform. |
| DATA-004 | Implement index and membership utilities | `indices`, `index`, `rindex`, `bsearch`, `all`, `any`, `isempty`, and SQL-style `IN` conform. |

### Feature: Strings, Formats, and Regular Expressions

| ID | Story | High-level AC |
|---|---|---|
| TEXT-001 | Implement string manipulation builtins | Trimming, prefix/suffix operations, case conversion, explode/implode, split, join, and interpolation conform. |
| TEXT-002 | Implement JSON and output format filters | `tostring`, `tojson`, `fromjson`, `@text`, `@json`, `@html`, `@uri`, `@urid`, `@csv`, `@tsv`, `@sh`, `@base64`, and `@base64d` conform. |
| TEXT-003 | Implement regular-expression filters | `test`, `match`, `capture`, `scan`, `split`, `splits`, `sub`, and `gsub` support required flags, captures, offsets, and streams. |
| TEXT-004 | Implement date and time filters | ISO dates, `strptime`, `strftime`, `gmtime`, `localtime`, and `mktime` conform for supplied cases. |

### Feature: I/O and Streaming

| ID | Story | High-level AC |
|---|---|---|
| IO-001 | Implement input stream controls | `input`, `inputs`, `input_filename`, and `input_line_number` conform within the fixed interface. |
| IO-002 | Implement diagnostics and stderr output | `debug`, `stderr`, and `halt_error` produce the specified output channels and exit behavior. |
| IO-003 | Implement streaming transformations | `tostream`, `fromstream`, and `truncate_stream` conform for supplied streaming values. |

### Feature: Conformance Delivery

| ID | Story | High-level AC |
|---|---|---|
| CONF-001 | Stage immutable conformance assets | The supplied manual, corpus, parser/lexer references, builtin reference, exclusions, runner, and full-test script are available at their required build paths without modification. |
| CONF-002 | Run scoped implementation verification | Each implementation slice can be exercised through `run_conformance.py --select` with `JQ` set to the candidate executable. |
| CONF-003 | Pass the complete conformance corpus | One terminal verification runs `sh sources/full_test.sh` unfiltered and exits zero with no failed or errored cases. |

## Story Guidance

Named stories planning must produce. Authoritative record: `STORY_GUIDANCE.json`.

| Story ID | Provenance | Gate | Note |
|---|---|---|---|
| EXEC-001 | plan | `python3 sources/run_conformance.py --select ^(true|false|null|1)$` | Build Instructions: interface contract |
| PARSE-001 | plan | `python3 sources/run_conformance.py --select ^(true|false|null|1|\.)$` | lexer.l |
| PARSE-002 | plan | `python3 sources/run_conformance.py --select interpolation|@base64|@uri` | lexer.l and jq.test string/format cases |
| PARSE-003 | plan | `python3 sources/run_conformance.py --select \.|\[|\{|\+|\-|\*|/|%` | parser.y expression grammar |
| PARSE-004 | plan | `python3 sources/run_conformance.py --select %%FAIL|if |try |reduce |foreach |def | as |label |module|include` | parser.y declarations and control grammar |
| CORE-001 | plan | `python3 sources/run_conformance.py --select \.|,|\[\.\]|range|empty` | Build Instructions: generator core |
| CORE-002 | plan | `python3 sources/run_conformance.py --select \||,|\[|\{` | jq-manual.txt generator semantics |
| CORE-003 | plan | `python3 sources/run_conformance.py --select try|error|\?` | jq-manual.txt error and optional semantics |
| CORE-004 | plan | `python3 sources/run_conformance.py --select ==|!=|<=|>=|<|>` | jq-manual.txt comparison and truthiness |
| VALUE-001 | plan | `python3 sources/run_conformance.py --select nan|infinite|tojson|fromjson` | jq-manual.txt types and numeric values |
| VALUE-002 | plan | `python3 sources/run_conformance.py --select \.[A-Za-z]|\[[-0-9]` | jq-manual.txt accessors |
| VALUE-003 | plan | `python3 sources/run_conformance.py --select \[.*:|\.\[\]` | jq-manual.txt slices and iteration |
| VALUE-004 | plan | `python3 sources/run_conformance.py --select length|type|sqrt|floor|tonumber` | jq-manual.txt types and numeric builtins |
| FLOW-001 | plan | `python3 sources/run_conformance.py --select \+|\-|\*|/|%` | jq-manual.txt builtin operators |
| FLOW-002 | plan | `python3 sources/run_conformance.py --select and|or|not|//` | jq-manual.txt conditionals and comparisons |
| FLOW-003 | plan | `python3 sources/run_conformance.py --select if |try |\?` | jq-manual.txt conditionals and try-catch |
| FLOW-004 | plan | `python3 sources/run_conformance.py --select label|break` | jq-manual.txt breaking out of control structures |
| FLOW-005 | plan | `python3 sources/run_conformance.py --select reduce|foreach|limit|skip|nth|first|last` | jq-manual.txt advanced generators |
| FLOW-006 | plan | `python3 sources/run_conformance.py --select while|until|recurse|repeat` | jq-manual.txt recursive generators |
| FUNC-001 | plan | `python3 sources/run_conformance.py --select  as \$|\$[A-Za-z]` | jq-manual.txt variable binding |
| FUNC-002 | plan | `python3 sources/run_conformance.py --select def .*\(` | jq-manual.txt defining functions |
| FUNC-003 | plan | `python3 sources/run_conformance.py --select def ` | jq-manual.txt function scoping and recursion |
| FUNC-004 | plan | `python3 sources/run_conformance.py --select \?//| as \{` | jq-manual.txt destructuring alternatives |
| PATH-001 | plan | `python3 sources/run_conformance.py --select path\(|paths|pick\(` | jq-manual.txt paths |
| PATH-002 | plan | `python3 sources/run_conformance.py --select getpath|setpath|delpaths` | jq-manual.txt path primitives |
| PATH-003 | plan | `python3 sources/run_conformance.py --select =|\|=|\+=` | jq-manual.txt assignment |
| PATH-004 | plan | `python3 sources/run_conformance.py --select negative|NaN|depth|empty` | jq.test assignment edge cases |
| DATA-001 | plan | `python3 sources/run_conformance.py --select map|flatten|transpose|combinations|walk` | builtin.jq collection utilities |
| DATA-002 | plan | `python3 sources/run_conformance.py --select sort|group_by|unique|min|max` | jq-manual.txt collection ordering |
| DATA-003 | plan | `python3 sources/run_conformance.py --select keys|has\(|contains|inside|to_entries|from_entries` | jq-manual.txt object and containment builtins |
| DATA-004 | plan | `python3 sources/run_conformance.py --select indices|index\(|rindex|bsearch|any|all|IN\(` | builtin.jq generic iterator and membership utilities |
| TEXT-001 | plan | `python3 sources/run_conformance.py --select split|join|trim|ascii_|explode|implode|startswith|endswith` | jq-manual.txt string builtins |
| TEXT-002 | plan | `python3 sources/run_conformance.py --select @text|@json|@html|@uri|@csv|@tsv|@sh|@base64` | jq-manual.txt format strings and escaping |
| TEXT-003 | plan | `python3 sources/run_conformance.py --select test\(|match\(|capture\(|scan\(|sub\(|gsub\(` | jq-manual.txt regular expressions |
| TEXT-004 | plan | `python3 sources/run_conformance.py --select date|strftime|strptime|gmtime|mktime` | jq-manual.txt dates |
| IO-001 | plan | `python3 sources/run_conformance.py --select input|inputs` | jq-manual.txt I/O |
| IO-002 | plan | `python3 sources/run_conformance.py --select debug|stderr|halt_error` | jq-manual.txt diagnostics |
| IO-003 | plan | `python3 sources/run_conformance.py --select tostream|fromstream|truncate_stream` | jq-manual.txt streaming |
| CONF-001 | plan | `python3 sources/run_conformance.py --list` | Build Instructions: source roles and staged assets |
| CONF-002 | plan | `python3 sources/run_conformance.py --select reduce` | Build Instructions: scoped verification |
| CONF-003 | plan | `sh sources/full_test.sh` | Sea Trials and definition of done |

## Surfaced Acceptance Criteria

| ID | Story ID | Criterion |
|---|---|---|
| AC-001 | EXEC-001 | The executable is named `jq`, is executable at the application root, and accepts only the exercised `-c` interface. |
| AC-002 | EXEC-003 | Output comparison preserves value order and emits one JSON value per output line. |
| AC-003 | PARSE-004 | Module syntax is parsed sufficiently to reject invalid module grammar without loading excluded module fixtures. |
| AC-004 | CONF-001 | Read-only scoring assets remain byte-for-byte unchanged and all staged runtime dependencies are present. |
| AC-005 | CONF-002 | Scoped checks use a selector matching the story's construct and never use the unscoped full corpus before the terminal story. |

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
| `sources/lexer.l` | parser-to-normalizer | `sources/parser.y` | Lexer tokens and parser productions define the language front end. | Build lexer behavior before parser execution. |
| `sources/parser.y` | instruction-to-test | `sources/jq.test` | Grammar and precedence are exercised by syntax and `%%FAIL` cases. | Parser stories require focused corpus slices. |
| `sources/jq-manual.txt` | reference-to-replacement | implementation stories | Manual defines filter semantics and builtin behavior. | Use as normative behavior reference. |
| `sources/builtin.jq` | reference-to-replacement | DATA, TEXT, FLOW, PATH, IO stories | Reference definitions specify many builtin compositions. | Implement the generator core before these builtins. |
| `sources/jq.test` | test-kit-to-implementation | `jq` | Corpus supplies program, input, and expected output cases. | Stage unchanged and execute through the harness. |
| `sources/run_conformance.py` | test-kit-to-implementation | `jq` | Runner invokes `JQ -c program` and checks exit/output semantics. | Preserve the executable interface and scoped verification. |
| `sources/full_test.sh` | test-kit-to-implementation | `sources/run_conformance.py` | Full script checks executable presence and delegates the complete run. | Reserve for the terminal acceptance story and Sea Trial. |
| `sources/exclusions.txt` | test-kit-to-implementation | `sources/jq.test` | Exclusions identify module-loader cases by exact program text. | Apply skips through the supplied harness only. |
| `sources/INSTRUCTIONS.md` | instruction-to-test | all implementation and conformance stories | Build order, prohibitions, interface, and definition of done are explicit. | Treat as author intent and project guardrails. |

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

Deliver a standalone executable Python jq interpreter. It parses a jq filter, evaluates it over JSON input as an ordered stream of values, and writes compact JSON outputs. The execution flow is lexer/parser, AST or equivalent intermediate representation, generator evaluator, builtin/function runtime, and CLI serialization. The staged conformance runner drives one process per corpus case; excluded module-loader cases are skipped by the supplied exclusion list.

### Story Realization Map

| Story IDs | Durable Blueprint scope | Evidence | Related files | Delivery kind |
|---|---|---|---|---|
| EXEC-001–003 | executable CLI and JSON process boundary | `sources/INSTRUCTIONS.md`, `sources/run_conformance.py` | `jq` | capability and acceptance contract |
| PARSE-001–004 | lexer, parser, syntax diagnostics | `sources/lexer.l`, `sources/parser.y`, `sources/jq.test` | `jq` | capability |
| CORE-001–004 | stream evaluator and runtime errors | `sources/INSTRUCTIONS.md`, `sources/jq-manual.txt` | `jq` | capability |
| VALUE-001–004 | value model, accessors, numeric behavior | `sources/jq-manual.txt`, `sources/jq.test` | `jq` | capability |
| FLOW-001–006 | operators and control constructs | `sources/builtin.jq`, `sources/parser.y`, `sources/jq.test` | `jq` | capability |
| FUNC-001–004 | bindings, functions, patterns | `sources/parser.y`, `sources/jq.test` | `jq` | capability |
| PATH-001–004 | paths and immutable updates | `sources/jq-manual.txt`, `sources/jq.test` | `jq` | capability |
| DATA-001–004 | collection and relational builtins | `sources/builtin.jq`, `sources/jq-manual.txt` | `jq` | capability |
| TEXT-001–004 | strings, formats, regex, dates | `sources/builtin.jq`, `sources/jq-manual.txt` | `jq` | capability |
| IO-001–003 | input, diagnostics, streaming | `sources/jq-manual.txt`, `sources/jq.test` | `jq` | capability |
| CONF-001–003 | staged assets, scoped runner use, terminal verification | `sources/INSTRUCTIONS.md`, `sources/run_conformance.py`, `sources/full_test.sh` | `sources/*` | test harness and acceptance contract |

### Test and Acceptance Strategy

Implementation stories use focused `sources/run_conformance.py --select` slices matching their construct. Parser stories also exercise the supplied `%%FAIL` cases. No intermediate story runs `full_test.sh` or the unscoped runner. `CONF-003` is the sole terminal full-suite story and declares `Suite: full`; it depends on all implementation stories and asserts only the full harness exit status. Sea Trial `st-001` proves the same complete corpus requirement.

### Sequencing and Dependencies

Build the executable boundary first, then lexer/parser, then generator evaluation and value semantics. Implement paths and assignment after accessors and generators. Add control flow and functions before higher-level builtins. Implement collection, text, regex, date, I/O, and streaming groups afterward. Stage all assets before acceptance execution. The terminal full-suite verification is last and depends on every implementation story. No external service or package dependency exists.

### Source Conflicts and Gaps

No unresolved cross-source conflicts or blockers were found. The fixed Python standard-library runtime, executable contract, complete-corpus gate, excluded module-loader cases, and forbidden third-party implementations are consistent across the supplied instructions, harness, corpus, manual, lexer, parser, and builtin reference.

## Analysis Notes
generated: 2026-08-22T00:00:00Z
blueprint: /mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260822.044627/workspace/targets/jq/blueprint

Quality: Ready
  blockers: 0
  questions: 0
  features: 10
  stories: 42
  stack: Python standard library
  display_name: not proposed
  short_description: not proposed

The project type is `cli`. The source-defined story breakdown is broad but remains below the 100-story blocker threshold. The 42-story decomposition follows the supplied implementation order and major manual/conformance domains.
