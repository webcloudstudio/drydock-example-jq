# Evidence: Block 7 · Foundational (block-7)

- block type: block
- date: 2026-08-16
- resulting state: closed/verified
- story points (combined assembled cost): 67299
- execution id: 20260817.035740.885Z-c066740a

## Stories built
- Stage the supplied jq conformance assets unchanged. (verify-001) [story]

## Reusable compacts
- full_test_compact.md
- exclusions_compact.md
- builtin_compact.md

## Stacked context
- compass: COMPASS.md (SP 3799)
- implements: FEATURE-VERIFY-001.md (SP 470)
- context: full_test.sh (SP 189)
- context: run_conformance.py (SP 4354)
- context: exclusions.txt (SP 654)
- context: jq.test (SP 13058)
- context: jq-manual.txt (SP 32696)
- context: parser.y (SP 5596)
- context: lexer.l (SP 1137)
- context: builtin.jq (SP 2408)
- context: ARCHITECTURE_compact.md (SP 162)
- stack: common_compact.md (SP 1179)
- stack: python_compact.md (SP 1534)

## Pre-build acceptance observation
- GREEN (prepassed): verify-001-harness-list (FEATURE-VERIFY-001.md)
  intent: The staged conformance runner can parse the staged corpus and exclusions without a harness error.
  return code: 0
  stdout:
    run  jq.test:48  .
    run  jq.test:58  .
    
    2 cases, 0 excluded
- GREEN (prepassed): verify-001-script-contract (FEATURE-VERIFY-001.md)
  intent: The staged scoring script is executable by POSIX sh and reaches the candidate interface check.
  return code: 0
  stdout:
    FAIL jq.test:39  program did not compile: expected } at position 19
        program:  {x:-1},{x:-.},{x:-.|abs}
        input:    1
        expected: ['{"x":-1}', '{"x":-1}', '{"x":1}']
        actual:   (no output)
        stderr:   expected } at position 19
    FAIL jq.test:48  output mismatch
        program:  .
        input:    ﻿"byte order mark"
        expected: ['"byte order mark"']
        actual:   (no output)
        stderr:   Unexpected UTF-8 BOM (decode using utf-8-sig): line 1 column 1 (char 0)
    FAIL jq.test:72  output mismatch
        program:  @text,@json,([1,.]|@csv,@tsv),@html,(@uri|.,@urid),@sh,(@base64|.,@base64d)
        input:    "!()<>&'\"\t"
        expected: ['"!()<>&\'\\"\\t"', '"\\"!()<>&\'\\\\\\"\\\\t\\""', '"1,\\"!()<>&\'\\"\\"\\t\\""', '"1\\t!()<>&\'\\"\\\\t"', '"!()&lt;&gt;&amp;&apos;&quot;\\t"', '"%21%28%29%3C%3E%26%27%22%09"', '"!()<>&\'\\"\\t"', '"\'!()<>&\'\\\\\'\'\\"\\t\'"', '"ISgpPD4mJyIJ"', '"!()<>&\'\\"\\t"']
        actual:   (no output)
        stderr:   unsupported filter
    FAIL jq.test:86  output mismatch
        program:  @base64
        input:    "foóbar\n"
        expected: ['"Zm/Ds2Jhcgo="']
        actual:   (no output)
        stderr:   unsupported filter
    FAIL jq.test:90  output mismatch
        program:  @base64d
        input:    "Zm/Ds2Jhcgo="
        expected: ['"foóbar\\n"']
        actual:   (no output)
        stderr:   unsupported filter
    FAIL jq.test:94  output mismatch
        program:  @uri
        input:    "\u03bc"
        expected: ['"%CE%BC"']
        actual:   (no output)
        stderr:   unsupported filter
    FAIL jq.test:98  output mismatch
        program:  @urid
        input:    "%CE%BC"
        expected: ['"\\u03bc"']
        actual:   (no output)
        stderr:   unsupported filter
    FAIL jq.test:102  program did not compile: unexpected token at position 6
        program:  @html "<b>\(.)</b>"
        input:    "<script>hax</script>"
        expected: ['"<b>&lt;script&gt;hax&lt;/script&gt;</b>"']
        actual:   (no output)
        stderr:   unexpected token at position 6
    FAIL jq.test:122  output mismatch
        program:  {"a",b,"a$\(1+1)"}
        input:    {"a":1, "b":2, "c":3, "a$2":4}
        expected: ['{"a":1, "b":2, "a$2":4}']
        actual:   ['{"a":1,"b":2,"[(\'text\', \'a$\'), (\'expr\', \'1+1\')]":null}']
    FAIL jq.test:127  program was accepted, but the corpus marks it %%FAIL
        program:  {(0):1}
    FAIL jq.test:139  program was accepted, but the corpus marks it %%FAIL
        program:  {non_const:., (0):1}
    FAIL jq.test:168  program did not compile: unexpected token at position 1
        program:  ."foo"."bar"
        input:    {"foo": {"bar": 20}}
        expected: ['20']
        actual:   (no output)
        stderr:   unexpected token at position 1
    FAIL jq.test:183  output mismatch
        program:  [.[]|.foo?.bar?]
        input:    [1,[2],[],{"foo":3},{"foo":{"bar":4}},{}]
        expected: ['[4,null]']
        actual:   ['[4]']
    FAIL jq.test:187  program did not compile: expected filter at position 1
        program:  [..]
        input:    [1,[[2]],{ "a":[1]}]
        expected: ['[[1,[[2]],{"a":[1]}],1,[[2]],[2],2,{"a":[1]},[1],1]']
        actual:   (no output)
        stderr:   expected filter at position 1
    FAIL jq.test:195  output mismatch
        program:  [.[]|.[1:3]?]
        input:    [1,null,true,false,"abcdef",{},{"a":1,"b":2},[],[1,2,3,4,5],[1,2]]
        expected: ['[null,"bc",[],[2,3],[2]]']
        actual:   (no output)
        stderr:   'int' object is not subscriptable
    FAIL jq.test:200  program did not compile: expected ) at position 28
        program:  map(try .a[] catch ., try .a.[] catch ., .a[]?, .a.[]?)
        input:    [{"a": [1,2]}, {"a": 123}]
        expected: ['[1,2,1,2,1,2,1,2,"Cannot iterate over number (123)","Cannot iterate over number (123)"]']
        actual:   (no output)
        stderr:   expected ) at position 28
    FAIL jq.test:205  output mismatch
        program:  try ["OK", (.[] | error)] catch ["KO", .]
        input:    {"a":["b"],"c":["d"]}
        expected: ['["KO",["b"]]']
        actual:   ['["KO","error"]']
    FAIL jq.test:213  output mismatch
        program:  try (.foo[-1] = 0) catch .
        input:    null
        expected: ['"Out of bounds negative array index"']
        actual:   (no output)
        stderr:   'NoneType' object is not subscriptable
    FAIL jq.test:217  output mismatch
        program:  try (.foo[-2] = 0) catch .
        input:    null
        expected: ['"Out of bounds negative array index"']
        actual:   (no output)
        stderr:   'NoneType' object is not subscriptable
    FAIL jq.test:229  output mismatch
        program:  try (.[999999999] = 0) catch .
        input:    null
        expected: ['"Array index too large"']
        actual:   ['null']
    FAIL jq.test:277  output mismatch
        program:  {x: (1,2)},{x:3} | .x
        input:    null
        expected: ['1', '2', '3']
        actual:   ['2', '3']
    FAIL jq.test:283  output mismatch
        program:  [.[-4,-3,-2,-1,0,1,2,3]]
        input:    [1,2,3]
        expected: ['[null,1,2,3,1,2,3,null]']
        actual:   (no output)
        stderr:   cannot index
    FAIL jq.test:291  output mismatch
        program:  [range(0,1;3,4)]
        input:    null
        expected: ['[0,1,2, 0,1,2,3, 1,2, 1,2,3]']
        actual:   ['[0,1,2]']
    FAIL jq.test:307  output mismatch
        program:  [range(0,1;4,5;1,2)]
        input:    null
        expected: ['[0,1,2,3,0,2, 0,1,2,3,4,0,2,4, 1,2,3,1,3, 1,2,3,4,1,3]']
        actual:   ['[0,1,2,3]']
    FAIL jq.test:311  program did not compile: unknown function while/2
        program:  [while(.<100; .*2)]
        input:    1
        expected: ['[1,2,4,8,16,32,64]']
        actual:   (no output)
        stderr:   unknown function while/2
    FAIL jq.test:329  program did not compile: unknown function until/2
        program:  [.[]|[.,1]|until(.[0] < 1; [.[0] - 1, .[1] * .[0]])|.[1]]
        input:    [1,2,3,4,5]
        expected: ['[1,2,6,24,120]']
        actual:   (no output)
        stderr:   unknown function until/2
    FAIL jq.test:345  output mismatch
        program:  [foreach .[] as {a:$a} (0; . + $a; -.)]
        input:    [{"a":1}, {"b":2}, {"a":3, "b":4}]
        expected: ['[-1, -1, -4]']
        actual:   (no output)
        stderr:   unsupported operand type(s) for +: 'float' and 'NoneType'
    FAIL jq.test:361  program did not compile: unknown function limit/2
        program:  [limit(3; .[])]
        input:    [11,22,33,44,55,66,77,88,99]
        expected: ['[11,22,33]']
        actual:   (no output)
        stderr:   unknown function limit/2
    FAIL jq.test:365  program did not compile: unknown function limit/2
        program:  [limit(0; error)]
        input:    "badness"
        expected: ['[]']
        actual:   (no output)
        stderr:   unknown function limit/2
    FAIL jq.test:369  program did not compile: unknown function limit/2
        program:  [limit(1; 1, error)]
        input:    "badness"
        expected: ['[1]']
        actual:   (no output)
        stderr:   unknown function limit/2
    FAIL jq.test:373  program did not compile: unknown function limit/2
        program:  try limit(-1; error) catch .
        input:    null
        expected: ['"limit doesn\'t support negative count"']
        actual:   (no output)
        stderr:   unknown function limit/2
    FAIL jq.test:377  program did not compile: unknown function skip/2
        program:  [skip(3; .[])]
        input:    [1,2,3,4,5,6,7,8,9]
        expected: ['[4,5,6,7,8,9]']
        actual:   (no output)
        stderr:   unknown function skip/2
    FAIL jq.test:381  program did not compile: unknown function skip/2
        program:  [skip(0,2,3,4; .[])]
        input:    [1,2,3]
        expected: ['[1,2,3,3]']
        actual:   (no output)
        stderr:   unknown function skip/2
    FAIL jq.test:385  program did not compile: unknown function skip/2
        program:  [skip(3; .[])]
        input:    []
        expected: ['[]']
        actual:   (no output)
        stderr:   unknown function skip/2
    FAIL jq.test:389  program did not compile: unknown function skip/2
        program:  try skip(-1; error) catch .
        input:    null
        expected: ['"skip doesn\'t support negative count"']
        actual:   (no output)
        stderr:   unknown function skip/2
    FAIL jq.test:393  program did not compile: unknown function nth/2
        program:  nth(1; 0,1,error("foo"))
        input:    null
        expected: ['1']
        actual:   (no output)
        stderr:   unknown function nth/2
    FAIL jq.test:397  program did not compile: unknown function first/1
        program:  [first(range(.)), last(range(.))]
        input:    10
        expected: ['[0,9]']
        actual:   (no output)
        stderr:   unknown function first/1
    FAIL jq.test:401  program did not compile: unknown function first/1
        program:  [first(range(.)), last(range(.))]
        input:    0
        expected: ['[]']
        actual:   (no output)
        stderr:   unknown function first/1
    FAIL jq.test:405  program did not compile: unknown function nth/2
        program:  [nth(0,5,9,10,15; range(.)), try nth(-1; range(.)) catch .]
        input:    10
        expected: ['[0,5,9,"nth doesn\'t support negative indices"]']
        actual:   (no output)
        stderr:   unknown function nth/2
    FAIL jq.test:410  program did not compile: unknown function first/1
        program:  first(1,error("foo"))
        input:    null
        expected: ['1']
        actual:   (no output)
        stderr:   unknown function first/1
    FAIL jq.test:420  program did not compile: unknown function limit/2
        program:  [limit(5,7; range(9))]
        input:    null
        expected: ['[0,1,2,3,4,0,1,2,3,4,5,6]']
        actual:   (no output)
        stderr:   unknown function limit/2
    FAIL jq.test:425  program did not compile: unknown function nth/2
        program:  [nth(5,7; range(9;0;-1))]
        input:    null
        expected: ['[4,2]']
        actual:   (no output)
        stderr:   unknown function nth/2
    FAIL jq.test:430  output mismatch
        program:  [range(0,1,2;4,3,2;2,3)]
        input:    null
        expected: ['[0,2,0,3,0,2,0,0,0,1,3,1,1,1,1,1,2,2,2,2]']
        actual:   ['[0,2]']
    FAIL jq.test:435  output mismatch
        program:  [range(3,5)]
        input:    null
        expected: ['[0,1,2,0,1,2,3,4]']
        actual:   ['[0,1,2]']
    FAIL jq.test:440  program did not compile: unknown function index/1
        program:  [(index(",","|"), rindex(",","|")), indices(",","|")]
        input:    "a,b|c,d,e||f,g,h,|,|,i,j"
        expected: ['[1,3,22,19,[1,5,7,12,14,16,18,20,22],[3,9,10,17,19]]']
        actual:   (no output)
        stderr:   unknown function index/1
    FAIL jq.test:445  output mismatch
        program:  join(",","/")
        input:    ["a","b","c","d"]
        expected: ['"a,b,c,d"', '"a/b/c/d"']
        actual:   ['"a,b,c,d"']
    FAIL jq.test:455  output mismatch
        program:  flatten(3,2,1)
        input:    [0, [1], [[2]], [[[3]]]]
        expected: ['[0,1,2,3]', '[0,1,2,[3]]', '[0,1,[2],[[3]]]']
        actual:   (no output)
        stderr:   'int' object is not reversible
    FAIL jq.test:466  output mismatch
        program:  [.[3:2], .[-5:4], .[:-2], .[-2:], .[3:3][1:], .[10:]]
        input:    [0,1,2,3,4,5,6]
        expected: ['[[], [2,3], [0,1,2,3,4], [5,6], [], []]']
        actual:   (no output)
        stderr:   slice indices must be integers or None or have an __index__ method
    FAIL jq.test:470  output mismatch
        program:  [.[3:2], .[-5:4], .[:-2], .[-2:], .[3:3][1:], .[10:]]
        input:    "abcdefghi"
        expected: ['["","","abcdefg","hi","",""]']
        actual:   (no output)
        stderr:   slice indices must be integers or None or have an __index__ method
    FAIL jq.test:474  program did not compile: unknown function del/1
        program:  del(.[2:4],.[0],.[-2:])
        input:    [0,1,2,3,4,5,6,7]
        expected: ['[1,4,5]']
        actual:   (no output)
        stderr:   unknown function del/1
    FAIL jq.test:478  output mismatch
        program:  .[2:4] = ([], ["a","b"], ["a","b","c"])
        input:    [0,1,2,3,4,5,6,7]
        expected: ['[0,1,4,5,6,7]', '[0,1,"a","b",4,5,6,7]', '[0,1,"a","b","c",4,5,6,7]']
        actual:   (no output)
        stderr:   invalid update path
    FAIL jq.test:530  program did not compile: expected : at position 29
        program:  . as {as: $kw, "str": $str, ("e"+"x"+"p"): $exp} | [$kw, $str, $exp]
        input:    {"as": 1, "str": 2, "exp": 3}
        expected: ['[1, 2, 3]']
        actual:   (no output)
        stderr:   expected : at position 29
    FAIL jq.test:548  program was accepted, but the corpus marks it %%FAIL
        program:  . as [] | null
    FAIL jq.test:554  program was accepted, but the corpus marks it %%FAIL
        program:  . as {} | null
    FAIL jq.test:601  output mismatch
        program:  .+null
        input:    {"a":42}
        expected: ['{"a":42}']
        actual:   (no output)
        stderr:   unsupported operand type(s) for +: 'dict' and 'NoneType'
    FAIL jq.test:605  output mismatch
        program:  null+.
        input:    null
        expected: ['null']
        actual:   (no output)
        stderr:   unsupported operand type(s) for +: 'NoneType' and 'NoneType'
    FAIL jq.test:609  output mismatch
        program:  .a+.b
        input:    {"a":42}
        expected: ['42']
        actual:   (no output)
        stderr:   unsupported operand type(s) for +: 'int' and 'NoneType'
    FAIL jq.test:661  output mismatch
        program:  9E999999999, 9999999999E999999990, 1E-999999999, 0.000000001E-999999990
        input:    null
        expected: ['9E+999999999', '9.999999999E+999999999', '1E-999999999', '1E-999999999']
        actual:   (no output)
        stderr:   Out of range float values are not JSON compliant: inf
    FAIL jq.test:689  output mismatch
        program:  [(infinite, -infinite) % (1, -1, infinite)]
        input:    null
        expected: ['[0,0,0,0,0,-1]']
        actual:   (no output)
        stderr:   unknown function infinite
    FAIL jq.test:693  program did not compile: unknown filter at position 20
        program:  [nan % 1, 1 % nan | isnan]
        input:    null
        expected: ['[true,true]']
        actual:   (no output)
        stderr:   unknown filter at position 20
    FAIL jq.test:701  output mismatch
        program:  "123\u0000456" | try tonumber catch .
        input:    null
        expected: ['"string (\\"123\\\\u0000456\\") cannot be parsed as a number"']
        actual:   (no output)
        stderr:   invalid literal for int() with base 10: '123\x00456'
    FAIL jq.test:705  program did not compile: unknown filter at position 4
        program:  map(toboolean)
        input:    ["false","true",false,true]
        expected: ['[false,true,false,true]']
        actual:   (no output)
        stderr:   unknown filter at position 4
    FAIL jq.test:709  program did not compile: unknown filter at position 10
        program:  .[] | try toboolean catch .
        input:    [null,0,"tru","truee","fals","falsee",[],{}]
        expected: ['"null (null) cannot be parsed as a boolean"', '"number (0) cannot be parsed as a boolean"', '"string (\\"tru\\") cannot be parsed as a boolean"', '"string (\\"truee\\") cannot be parsed as a boolean"', '"string (\\"fals\\") cannot be parsed as a boolean"', '"string (\\"falsee\\") cannot be parsed as a boolean"', '"array ([]) cannot be parsed as a boolean"', '"object ({}) cannot be parsed as a boolean"']
        actual:   (no output)
        stderr:   unknown filter at position 10
    FAIL jq.test:720  program did not compile: unknown filter at position 35
        program:  "true\u0000x", "false\u0000" | try toboolean catch .
        input:    null
        expected: ['"string (\\"true\\\\u0000x\\") cannot be parsed as a boolean"', '"string (\\"false\\\\u0000\\") cannot be parsed as a boolean"']
        actual:   (no output)
        stderr:   unknown filter at position 35
    FAIL jq.test:741  output mismatch
        program:  utf8bytelength
        input:    "asdf\u03bc"
        expected: ['6']
        actual:   ['5']
    FAIL jq.test:745  output mismatch
        program:  [.[] | try utf8bytelength catch .]
        input:    [[], {}, [1,2], 55, true, false]
        expected: ['["array ([]) only strings have UTF-8 byte length","object ({}) only strings have UTF-8 byte length","array ([1,2]) only strings have UTF-8 byte length","number (55) only strings have UTF-8 byte length","boolean (true) only strings have UTF-8 byte length","boolean (false) only strings have UTF-8 byte length"]']
        actual:   ['[0,0,2,55,1,0]']
    FAIL jq.test:758  output mismatch
        program:  map(add)
        input:    [[], [1,2,3], ["a","b","c"], [[3],[4,5],[6]], [{"a":1}, {"b":2}, {"a":3}]]
        expected: ['[null, 6, "abc", [3,4,5,6], {"a":3, "b": 2}]']
        actual:   (no output)
        stderr:   sequence item 0: expected str instance, list found
    FAIL jq.test:766  output mismatch
        program:  [add(null), add(range(range(10))), add(empty), add(10,range(10))]
        input:    null
        expected: ['[null,120,null,55]']
        actual:   (no output)
        stderr:   can only join an iterable
    FAIL jq.test:771  output mismatch
        program:  .sum = add(.arr[])
        input:    {"arr":[]}
        expected: ['{"arr":[],"sum":null}']
        actual:   (no output)
        stderr:   cannot index
    FAIL jq.test:775  output mismatch
        program:  add({(.[]):1}) | keys
        input:    ["a","a","b","a","d","b","d","a","d"]
        expected: ['["a","b","d"]']
        actual:   (no output)
        stderr:   'str' object has no attribute 'keys'
    FAIL jq.test:847  program did not compile: unknown filter at position 0
        program:  atan * 4 * 1000000|floor / 1000000
        input:    1
        expected: ['3.141592']
        actual:   (no output)
        stderr:   unknown filter at position 0
    FAIL jq.test:851  program did not compile: unknown filter at position 37
        program:  [(3.141592 / 2) * (range(0;20) / 20)|cos * 1000000|floor / 1000000]
        input:    null
        expected: ['[1,0.996917,0.987688,0.972369,0.951056,0.923879,0.891006,0.85264,0.809017,0.760406,0.707106,0.649448,0.587785,0.522498,0.45399,0.382683,0.309017,0.233445,0.156434,0.078459]']
        actual:   (no output)
        stderr:   unknown filter at position 37
    FAIL jq.test:855  program did not compile: unknown filter at position 37
        program:  [(3.141592 / 2) * (range(0;20) / 20)|sin * 1000000|floor / 1000000]
        input:    null
        expected: ['[0,0.078459,0.156434,0.233445,0.309016,0.382683,0.45399,0.522498,0.587785,0.649447,0.707106,0.760405,0.809016,0.85264,0.891006,0.923879,0.951056,0.972369,0.987688,0.996917]']
        actual:   (no output)
        stderr:   unknown filter at position 37
    FAIL jq.test:933  program did not compile: variable is not defined at position 29
        program:  . as {$a, $b:[$c, $d]}| [$a, $b, $c, $d]
        input:    {"a":1, "b":[2,{"d":3}]}
        expected: ['[1,[2,{"d":3}],2,{"d":3}]']
        actual:   (no output)
        stderr:   variable is not defined at position 29
    FAIL jq.test:1062  output mismatch
        program:  any(true, error; .)
        input:    "badness"
        expected: ['true']
        actual:   (no output)
        stderr:   error
    FAIL jq.test:1066  output mismatch
        program:  all(false, error; .)
        input:    "badness"
        expected: ['false']
        actual:   (no output)
        stderr:   error
    FAIL jq.test:1070  output mismatch
        program:  any(not)
        input:    []
        expected: ['false']
        actual:   (no output)
        stderr:   'bool' object is not iterable
    FAIL jq.test:1074  output mismatch
        program:  all(not)
        input:    []
        expected: ['true']
        actual:   (no output)
        stderr:   'bool' object is not iterable
    FAIL jq.test:1078  output mismatch
        program:  any(not)
        input:    [false]
        expected: ['true']
        actual:   (no output)
        stderr:   'bool' object is not iterable
    FAIL jq.test:1082  output mismatch
        program:  all(not)
        input:    [false]
        expected: ['true']
        actual:   (no output)
        stderr:   'bool' object is not iterable
    FAIL jq.test:1110  program did not compile: unknown function path/1
        program:  path(.foo[0,1])
        input:    null
        expected: ['["foo", 0]', '["foo", 1]']
        actual:   (no output)
        stderr:   unknown function path/1
    FAIL jq.test:1115  program did not compile: unknown function path/1
        program:  path(.[] | select(.>3))
        input:    [1,5,3]
        expected: ['[1]']
        actual:   (no output)
        stderr:   unknown function path/1
    FAIL jq.test:1119  program did not compile: unknown function path/1
        program:  path(.)
        input:    42
        expected: ['[]']
        actual:   (no output)
        stderr:   unknown function path/1
    FAIL jq.test:1123  program did not compile: unknown function path/1
        program:  try path(.a | map(select(.b == 0))) catch .
        input:    {"a":[{"b":0}]}
        expected: ['"Invalid path expression with result [{\\"b\\":0}]"']
        actual:   (no output)
        stderr:   unknown function path/1
    FAIL jq.test:1127  program did not compile: unknown function path/1
        program:  try path(.a | map(select(.b == 0)) | .[0]) catch .
        input:    {"a":[{"b":0}]}
        expected: ['"Invalid path expression near attempt to access element 0 of [{\\"b\\":0}]"']
        actual:   (no output)
        stderr:   unknown function path/1
    FAIL jq.test:1131  program did not compile: unknown function path/1
        program:  try path(.a | map(select(.b == 0)) | .c) catch .
        input:    {"a":[{"b":0}]}
        expected: ['"Invalid path expression near attempt to access element \\"c\\" of [{\\"b\\":0}]"']
        actual:   (no output)
        stderr:   unknown function path/1
    FAIL jq.test:1135  program did not compile: unknown function path/1
        program:  try path(.a | map(select(.b == 0)) | .[]) catch .
        input:    {"a":[{"b":0}]}
        expected: ['"Invalid path expression near attempt to iterate through [{\\"b\\":0}]"']
        actual:   (no output)
        stderr:   unknown function path/1
    FAIL jq.test:1139  program did not compile: unknown function path/1
        program:  path(.a[path(.b)[0]])
        input:    {"a":{"b":0}}
        expected: ['["a","b"]']
        actual:   (no output)
        stderr:   unknown function path/1
    FAIL jq.test:1143  program did not compile: unknown filter at position 1
        program:  [paths]
        input:    [1,[[],{"a":2}]]
        expected: ['[[0],[1],[1,0],[1,1],[1,1,"a"]]']
        actual:   (no output)
        stderr:   unknown filter at position 1
    FAIL jq.test:1173  output mismatch
        program:  try delpaths(0) catch .
        input:    {}
        expected: ['"Paths must be specified as an array"']
        actual:   (no output)
        stderr:   'int' object is not iterable
    FAIL jq.test:1177  program did not compile: unknown function del/1
        program:  del(.), del(empty), del((.foo,.bar,.baz) | .[2,3,0]), del(.foo[0], .bar[0], .foo, .baz.bar[0].x)
        input:    {"foo": [0,1,2,3,4], "bar": [0,1]}
        expected: ['null', '{"foo": [0,1,2,3,4], "bar": [0,1]}', '{"foo": [1,4], "bar": [1]}', '{"bar": [1]}']
        actual:   (no output)
        stderr:   unknown function del/1
    FAIL jq.test:1184  program did not compile: unknown function del/1
        program:  del(.[1], .[-6], .[2], .[-3:9])
        input:    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        expected: ['[0, 3, 5, 6, 9]']
        actual:   (no output)
        stderr:   unknown function del/1
    FAIL jq.test:1188  program did not compile: unknown function del/1
        program:  del(.[nan])
        input:    [1,2,3]
        expected: ['[1,2,3]']
        actual:   (no output)
        stderr:   unknown function del/1
    FAIL jq.test:1192  program did not compile: unknown function del/1
        program:  del(.[nan,nan])
        input:    [1,2,3]
        expected: ['[1,2,3]']
        actual:   (no output)
        stderr:   unknown function del/1
    FAIL jq.test:1201  program did not compile: unknown function pick/1
        program:  pick(.a.b.c)
        input:    null
        expected: ['{"a":{"b":{"c":null}}}']
        actual:   (no output)
        stderr:   unknown function pick/1
    FAIL jq.test:1205  program did not compile: unknown filter at position 5
        program:  pick(first)
        input:    [1,2]
        expected: ['[1]']
        actual:   (no output)
        stderr:   unknown filter at position 5
    FAIL jq.test:1209  program did not compile: unknown filter at position 5
        program:  pick(first|first)
        input:    [[10,20],30]
        expected: ['[[10]]']
        actual:   (no output)
        stderr:   unknown filter at position 5
    FAIL jq.test:1214  program did not compile: unknown filter at position 9
        program:  try pick(last) catch .
        input:    [1,2]
        expected: ['"Out of bounds negative array index"']
        actual:   (no output)
        stderr:   unknown filter at position 9
    FAIL jq.test:1225  output mismatch
        program:  .foo = .bar
        input:    {"bar":42}
        expected: ['{"foo":42, "bar":42}']
        actual:   (no output)
        stderr:   cannot index
    FAIL jq.test:1233  output mismatch
        program:  .[] += 2, .[] *= 2, .[] -= 2, .[] /= 2, .[] %=2
        input:    [1,3,5]
        expected: ['[3,5,7]', '[2,6,10]', '[-1,1,3]', '[0.5, 1.5, 2.5]', '[1,1,1]']
        actual:   (no output)
        stderr:   invalid update path
    FAIL jq.test:1245  output mismatch
        program:  .foo += .foo
        input:    {"foo":2}
        expected: ['{"foo":4}']
        actual:   (no output)
        stderr:   cannot index
    FAIL jq.test:1249  output mismatch
        program:  .[0].a |= {"old":., "new":(.+1)}
        input:    [{"a":1,"b":2}]
        expected: ['[{"a":{"old":1, "new":2},"b":2}]']
        actual:   (no output)
        stderr:   invalid update path
    FAIL jq.test:1258  output mismatch
        program:  .[] | try (getpath(["a",0,"b"]) |= 5) catch .
        input:    [null,{"b":0},{"a":0},{"a":null},{"a":[0,1]},{"a":{"b":1}},{"a":[{}]},{"a":[{"c":3}]}]
        expected: ['{"a":[{"b":5}]}', '{"b":0,"a":[{"b":5}]}', '"Cannot index number with number (0)"', '{"a":[{"b":5}]}', '"Cannot index number with string (\\"b\\")"', '"Cannot index object with number (0)"', '{"a":[{"b":5}]}', '{"a":[{"c":3,"b":5}]}']
        actual:   ['"invalid update path"', '"invalid update path"', '"invalid update path"', '"invalid update path"', '"invalid update path"', '"invalid update path"', '"invalid update path"', '"invalid update path"']
    FAIL jq.test:1270  output mismatch
        program:  (.[] | select(. >= 2)) |= empty
        input:    [1,5,3,0,7]
        expected: ['[1,0]']
        actual:   (no output)
        stderr:   invalid update path
    FAIL jq.test:1274  output mismatch
        program:  .[] |= select(. % 2 == 0)
        input:    [0,1,2,3,4,5]
        expected: ['[0,2,4]']
        actual:   (no output)
        stderr:   unknown function select
    FAIL jq.test:1278  output mismatch
        program:  .foo[1,4,2,3] |= empty
        input:    {"foo":[0,1,2,3,4,5]}
        expected: ['{"foo":[0,5]}']
        actual:   ['{"foo":[0,1,2,3,4,5]}']
    FAIL jq.test:1282  output mismatch
        program:  .[2][3] = 1
        input:    [4]
        expected: ['[4, null, [null, null, null, 1]]']
        actual:   (no output)
        stderr:   list index out of range
    FAIL jq.test:1286  output mismatch
        program:  .foo[2].bar = 1
        input:    {"foo":[11], "bar":42}
        expected: ['{"foo":[11,null,{"bar":1}], "bar":42}']
        actual:   (no output)
        stderr:   cannot index
    FAIL jq.test:1290  output mismatch
        program:  try ((map(select(.a == 1))[].b) = 10) catch .
        input:    [{"a":0},{"a":1}]
        expected: ['"Invalid path expression near attempt to iterate through [{\\"a\\":1}]"']
        actual:   ['"unknown function select"']
    FAIL jq.test:1294  output mismatch
        program:  try ((map(select(.a == 1))[].a) |= .+1) catch .
        input:    [{"a":0},{"a":1}]
        expected: ['"Invalid path expression near attempt to iterate through [{\\"a\\":1}]"']
        actual:   ['"unknown function select"']
    FAIL jq.test:1306  output mismatch
        program:  .[] = 1
        input:    [1,null,Infinity,-Infinity,NaN,-NaN]
        expected: ['[1,1,1,1,1,1]']
        actual:   (no output)
        stderr:   Expecting value: line 1 column 32 (char 31)
    FAIL jq.test:1318  program did not compile: expected end at position 40
        program:  [.[] | if .baz then "strange" elif .foo then "yep" else "nope" end]
        input:    [{"foo":0},{"foo":1},{"foo":[]},{"foo":true},{"foo":false},{"foo":null},{"foo":"foo"},{}]
        expected: ['["yep","yep","yep","yep","nope","nope","yep","nope"]']
        actual:   (no output)
        stderr:   expected end at position 40
    FAIL jq.test:1342  output mismatch
        program:  [if false then 3 end]
        input:    7
        expected: ['[7]']
        actual:   ['[null]']
    FAIL jq.test:1350  program did not compile: expected end at position 28
        program:  [if false then 3 elif false then 4 end]
        input:    7
        expected: ['[7]']
        actual:   (no output)
        stderr:   expected end at position 28
    FAIL jq.test:1354  program did not compile: expected end at position 28
        program:  [if false then 3 elif false then 4 else . end]
        input:    7
        expected: ['[7]']
        actual:   (no output)
        stderr:   expected end at position 28
    FAIL jq.test:1370  output mismatch
        program:  [.[] | [.foo[] // .bar]]
        input:    [{"foo":[1,2], "bar": 42}, {"foo":[1], "bar": null}, {"foo":[null,false,3], "bar": 18}, {"foo":[], "bar":42}, {"foo": [null,false,null], "bar": 41}]
        expected: ['[[1,2], [1], [3], [42], [41]]']
        actual:   ['[[1,2],[1],[18,18,3],[],[41,41,41]]']
    FAIL jq.test:1374  output mismatch
        program:  .[] //= .[0]
        input:    ["hello",true,false,[false],null]
        expected: ['["hello",true,"hello",[false],"hello"]']
        actual:   (no output)
        stderr:   cannot index
    FAIL jq.test:1448  program did not compile: expected end at position 44
        program:  [.[]|try if . == 0 then error("foo") elif . == 1 then .a elif . == 2 then empty else . end catch .]
        input:    [0,1,2,3]
        expected: ['["foo","Cannot index number with string (\\"a\\")",3]']
        actual:   (no output)
        stderr:   expected end at position 44
    FAIL jq.test:1452  output mismatch
        program:  [.[]|(.a, .a)?]
        input:    [null,true,{"a":1}]
        expected: ['[null,null,1,1]']
        actual:   ['[1,1]']
    FAIL jq.test:1464  output mismatch
        program:  try error(0) // 1
        input:    null
        expected: ['1']
        actual:   (no output)
    FAIL jq.test:1473  output mismatch
        program:  1 + try 2 catch 3 + 4
        input:    null
        expected: ['7']
        actual:   ['3']
    FAIL jq.test:1481  output mismatch
        program:  try -.? catch .
        input:    "foo"
        expected: ['"string (\\"foo\\") cannot be negated"']
        actual:   ['"number required"']
    FAIL jq.test:1485  program did not compile: unknown filter at position 33
        program:  {x: try 1, y: try error catch 2, z: if true then 3 end}
        input:    null
        expected: ['{"x":1,"y":2,"z":3}']
        actual:   (no output)
        stderr:   unknown filter at position 33
    FAIL jq.test:1493  output mismatch
        program:  .[] | try error catch .
        input:    [1,null,2]
        expected: ['1', 'null', '2']
        actual:   ['"error"', '"error"', '"error"']
    FAIL jq.test:1499  output mismatch
        program:  try error("\($__loc__)") catch .
        input:    null
        expected: ['"{\\"file\\":\\"<top-level>\\",\\"line\\":1}"']
        actual:   (no output)
        stderr:   variable is not defined at position 0
    FAIL jq.test:1512  output mismatch
        program:  [.[] | split(", ")]
        input:    ["a,b, c, d, e,f",", a,b, c, d, e,f, "]
        expected: ['[["a,b","c","d","e,f"],["","a,b","c","d","e,f",""]]']
        actual:   (no output)
        stderr:   list index out of range
    FAIL jq.test:1516  output mismatch
        program:  split("")
        input:    "abc"
        expected: ['["a","b","c"]']
        actual:   (no output)
        stderr:   list index out of range
    FAIL jq.test:1528  output mismatch
        program:  [.[]|trimstr("foo")]
        input:    ["fo", "foo", "barfoo", "foobarfoo", "foob"]
        expected: ['["fo","","bar","bar","b"]']
        actual:   ['["fo","","bar","barfoo","b"]']
    FAIL jq.test:1544  program did not compile: unknown function index/1
        program:  [(index(","), rindex(",")), indices(",")]
        input:    "a,bc,def,ghij,klmno"
        expected: ['[1,13,[1,4,8,13]]']
        actual:   (no output)
        stderr:   unknown function index/1
    FAIL jq.test:1548  program did not compile: unknown function index/1
        program:  [ index("aba"), rindex("aba"), indices("aba") ]
        input:    "xababababax"
        expected: ['[1,7,[1,3,5,7]]']
        actual:   (no output)
        stderr:   unknown function index/1
    FAIL jq.test:1553  program did not compile: unknown function _strindices/1
        program:  try _strindices("abc") catch .
        input:    123
        expected: ['"number (123) cannot be searched, as it is not a string"']
        actual:   (no output)
        stderr:   unknown function _strindices/1
    FAIL jq.test:1557  program did not compile: unknown function _strindices/1
        program:  try _strindices(123) catch .
        input:    "abc"
        expected: ['"number (123) is not a string"']
        actual:   (no output)
        stderr:   unknown function _strindices/1
    FAIL jq.test:1563  program did not compile: unknown filter at position 4
        program:  map(trim), map(ltrim), map(rtrim)
        input:    [" \n\t\r\f\u000b", "","  ", "a", " a ", "abc", "  abc  ", "  abc", "abc  "]
        expected: ['["", "", "", "a", "a", "abc", "abc", "abc", "abc"]', '["", "", "", "a", "a ", "abc", "abc  ", "abc", "abc  "]', '["", "", "", "a", " a", "abc", "  abc", "  abc", "abc"]']
        actual:   (no output)
        stderr:   unknown filter at position 4
    FAIL jq.test:1569  program did not compile: unknown filter at position 0
        program:  trim, ltrim, rtrim
        input:    "\u0009\u000A\u000B\u000C\u000D\u0020\u0085\u00A0\u1680\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200A\u2028\u2029\u202F\u205F\u3000abc\u0009\u000A\u000B\u000C\u000D\u0020\u0085\u00A0\u1680\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200A\u2028\u2029\u202F\u205F\u3000"
        expected: ['"abc"', '"abc\\u0009\\u000A\\u000B\\u000C\\u000D\\u0020\\u0085\\u00A0\\u1680\\u2000\\u2001\\u2002\\u2003\\u2004\\u2005\\u2006\\u2007\\u2008\\u2009\\u200A\\u2028\\u2029\\u202F\\u205F\\u3000"', '"\\u0009\\u000A\\u000B\\u000C\\u000D\\u0020\\u0085\\u00A0\\u1680\\u2000\\u2001\\u2002\\u2003\\u2004\\u2005\\u2006\\u2007\\u2008\\u2009\\u200A\\u2028\\u2029\\u202F\\u205F\\u3000abc"']
        actual:   (no output)
        stderr:   unknown filter at position 0
    FAIL jq.test:1575  program did not compile: unknown filter at position 4
        program:  try trim catch ., try ltrim catch ., try rtrim catch .
        input:    123
        expected: ['"trim input must be a string"', '"trim input must be a string"', '"trim input must be a string"']
        actual:   (no output)
        stderr:   unknown filter at position 4
    FAIL jq.test:1581  program did not compile: unknown function indices/1
        program:  indices(1)
        input:    [0,1,1,2,3,4,1,5]
        expected: ['[1,2,6]']
        actual:   (no output)
        stderr:   unknown function indices/1
    FAIL jq.test:1585  program did not compile: unknown function indices/1
        program:  indices([1,2])
        input:    [0,1,2,3,1,4,2,5,1,2,6,7]
        expected: ['[1,8]']
        actual:   (no output)
        stderr:   unknown function indices/1
    FAIL jq.test:1589  program did not compile: unknown function indices/1
        program:  indices([1,2])
        input:    [1]
        expected: ['[]']
        actual:   (no output)
        stderr:   unknown function indices/1
    FAIL jq.test:1593  program did not compile: unknown function indices/1
        program:  indices(", ")
        input:    "a,b, cd,e, fgh, ijkl"
        expected: ['[3,9,14]']
        actual:   (no output)
        stderr:   unknown function indices/1
    FAIL jq.test:1597  program did not compile: unknown function index/1
        program:  index("!")
        input:    "здравствуй мир!"
        expected: ['14']
        actual:   (no output)
        stderr:   unknown function index/1
    FAIL jq.test:1601  program did not compile: unknown function rindex/1
        program:  .[:rindex("x")]
        input:    "正xyz"
        expected: ['"正"']
        actual:   (no output)
        stderr:   unknown function rindex/1
    FAIL jq.test:1605  program did not compile: unknown function indices/1
        program:  indices("o")
        input:    "🇬🇧oo"
        expected: ['[2,3]']
        actual:   (no output)
        stderr:   unknown function indices/1
    FAIL jq.test:1609  program did not compile: unknown function indices/1
        program:  indices("o")
        input:    "ƒoo"
        expected: ['[1,2]']
        actual:   (no output)
        stderr:   unknown function indices/1
    FAIL jq.test:1613  output mismatch
        program:  [.[]|split(",")]
        input:    ["a, bc, def, ghij, jklmn, a,b, c,d, e,f", "a,b,c,d, e,f,g,h"]
        expected: ['[["a"," bc"," def"," ghij"," jklmn"," a","b"," c","d"," e","f"],["a","b","c","d"," e","f","g","h"]]']
        actual:   (no output)
        stderr:   list index out of range
    FAIL jq.test:1617  output mismatch
        program:  [.[]|split(", ")]
        input:    ["a, bc, def, ghij, jklmn, a,b, c,d, e,f", "a,b,c,d, e,f,g,h"]
        expected: ['[["a","bc","def","ghij","jklmn","a,b","c,d","e,f"],["a,b,c,d","e,f,g,h"]]']
        actual:   (no output)
        stderr:   list index out of range
    FAIL jq.test:1625  output mismatch
        program:  [.[] * "abc"]
        input:    [-1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 3.7, 10.0]
        expected: ['[null,null,"","","abc","abc","abcabcabc","abcabcabcabcabcabcabcabcabcabc"]']
        actual:   (no output)
        stderr:   can't multiply sequence by non-int of type 'float'
    FAIL jq.test:1629  output mismatch
        program:  [. * (nan,-nan)]
        input:    "abc"
        expected: ['[null,null]']
        actual:   (no output)
        stderr:   unknown function nan
    FAIL jq.test:1633  output mismatch
        program:  . * 100000 | [.[:10],.[-10:]]
        input:    "abc"
        expected: ['["abcabcabca","cabcabcabc"]']
        actual:   (no output)
        stderr:   'NoneType' object has no attribute 'kind'
    FAIL jq.test:1641  output mismatch
        program:  try (. * 1000000000) catch .
        input:    "abc"
        expected: ['"Repeat string result too long"']
        actual:   (no output)
        stderr:   runtime evaluation failed
    FAIL jq.test:1677  program did not compile: unknown function sort_by/1
        program:  (sort_by(.b) | sort_by(.a)), sort_by(.a, .b), sort_by(.b, .c), group_by(.b), group_by(.a + .b - .c == 2)
        input:    [{"a": 1, "b": 4, "c": 14}, {"a": 4, "b": 1, "c": 3}, {"a": 1, "b": 4, "c": 3}, {"a": 0, "b": 2, "c": 43}]
        expected: ['[{"a": 0, "b": 2, "c": 43}, {"a": 1, "b": 4, "c": 14}, {"a": 1, "b": 4, "c": 3}, {"a": 4, "b": 1, "c": 3}]', '[{"a": 0, "b": 2, "c": 43}, {"a": 1, "b": 4, "c": 14}, {"a": 1, "b": 4, "c": 3}, {"a": 4, "b": 1, "c": 3}]', '[{"a": 4, "b": 1, "c": 3}, {"a": 0, "b": 2, "c": 43}, {"a": 1, "b": 4, "c": 3}, {"a": 1, "b": 4, "c": 14}]', '[[{"a": 4, "b": 1, "c": 3}], [{"a": 0, "b": 2, "c": 43}], [{"a": 1, "b": 4, "c": 14}, {"a": 1, "b": 4, "c": 3}]]', '[[{"a": 1, "b": 4, "c": 14}, {"a": 0, "b": 2, "c": 43}], [{"a": 4, "b": 1, "c": 3}, {"a": 1, "b": 4, "c": 3}]]']
        actual:   (no output)
        stderr:   unknown function sort_by/1
    FAIL jq.test:1693  program did not compile: unknown function min_by/1
        program:  [min, max, min_by(.[1]), max_by(.[1]), min_by(.[2]), max_by(.[2])]
        input:    [[4,2,"a"],[3,1,"a"],[2,4,"a"],[1,3,"a"]]
        expected: ['[[1,3,"a"],[4,2,"a"],[3,1,"a"],[2,4,"a"],[4,2,"a"],[1,3,"a"]]']
        actual:   (no output)
        stderr:   unknown function min_by/1
    FAIL jq.test:1697  program did not compile: unknown function min_by/1
        program:  [min,max,min_by(.),max_by(.)]
        input:    []
        expected: ['[null,null,null,null]']
        actual:   (no output)
        stderr:   unknown function min_by/1
    FAIL jq.test:1701  output mismatch
        program:  .foo[.baz]
        input:    {"foo":{"bar":4},"baz":"bar"}
        expected: ['4']
        actual:   (no output)
        stderr:   cannot index
    FAIL jq.test:1705  output mismatch
        program:  .[] | .error = "no, it's OK"
        input:    [{"error":true}]
        expected: ['{"error": "no, it\'s OK"}']
        actual:   (no output)
        stderr:   invalid update path
    FAIL jq.test:1709  output mismatch
        program:  [{a:1}] | .[] | .a=999
        input:    null
        expected: ['{"a": 999}']
        actual:   (no output)
        stderr:   invalid update path
    FAIL jq.test:1713  program did not compile: unknown filter at position 0
        program:  to_entries
        input:    {"a": 1, "b": 2}
        expected: ['[{"key":"a", "value":1}, {"key":"b", "value":2}]']
        actual:   (no output)
        stderr:   unknown filter at position 0
    FAIL jq.test:1717  program did not compile: unknown filter at position 0
        program:  from_entries
        input:    [{"key":"a", "value":1}, {"Key":"b", "Value":2}, {"name":"c", "value":3}, {"Name":"d", "Value":4}]
        expected: ['{"a": 1, "b": 2, "c": 3, "d": 4}']
        actual:   (no output)
        stderr:   unknown filter at position 0
    FAIL jq.test:1721  program did not compile: unknown function with_entries/1
        program:  with_entries(.key |= "KEY_" + .)
        input:    {"a": 1, "b": 2}
        expected: ['{"KEY_a": 1, "KEY_b": 2}']
        actual:   (no output)
        stderr:   unknown function with_entries/1
    FAIL jq.test:1725  program did not compile: unknown function has/1
        program:  map(has("foo"))
        input:    [{"foo": 42}, {}]
        expected: ['[true, false]']
        actual:   (no output)
        stderr:   unknown function has/1
    FAIL jq.test:1729  program did not compile: unknown function has/1
        program:  map(has(2))
        input:    [[0,1], ["a","b","c"]]
        expected: ['[false, true]']
        actual:   (no output)
        stderr:   unknown function has/1
    FAIL jq.test:1733  program did not compile: unknown function has/1
        program:  has(nan)
        input:    [0,1,2]
        expected: ['false']
        actual:   (no output)
        stderr:   unknown function has/1
    FAIL jq.test:1741  output mismatch
        program:  [][.]
        input:    1000000000000000000
        expected: ['null']
        actual:   (no output)
        stderr:   cannot index
    FAIL jq.test:1745  output mismatch
        program:  map([1,2][0:.])
        input:    [-1, 1, 2, 3, 1000000000000000000]
        expected: ['[[1], [1], [1,2], [1,2], [1,2]]']
        actual:   (no output)
        stderr:   slice indices must be integers or None or have an __index__ method
    FAIL jq.test:1799  output mismatch
        program:  flatten(0)
        input:    [0, [1], [[2]], [[[3]]]]
        expected: ['[0, [1], [[2]], [[[3]]]]']
        actual:   (no output)
        stderr:   'int' object is not reversible
    FAIL jq.test:1803  output mismatch
        program:  flatten(2)
        input:    [0, [1], [[2]], [[[3]]]]
        expected: ['[0, 1, 2, [3]]']
        actual:   (no output)
        stderr:   'int' object is not reversible
    FAIL jq.test:1807  output mismatch
        program:  flatten(2)
        input:    [0, [1, [2]], [1, [[3], 2]]]
        expected: ['[0, 1, 2, 1, [3], 2]']
        actual:   (no output)
        stderr:   'int' object is not reversible
    FAIL jq.test:1811  output mismatch
        program:  try flatten(-1) catch .
        input:    [0, [1], [[2]], [[[3]]]]
        expected: ['"flatten depth must not be negative"']
        actual:   (no output)
        stderr:   'float' object is not reversible
    FAIL jq.test:1815  program did not compile: unknown filter at position 0
        program:  transpose
        input:    [[1], [2,3]]
        expected: ['[[1,2],[null,3]]']
        actual:   (no output)
        stderr:   unknown filter at position 0
    FAIL jq.test:1819  program did not compile: unknown filter at position 0
        program:  transpose
        input:    []
        expected: ['[]']
        actual:   (no output)
        stderr:   unknown filter at position 0
    FAIL jq.test:1823  program did not compile: unknown filter at position 0
        program:  ascii_upcase
        input:    "useful but not for é"
        expected: ['"USEFUL BUT NOT FOR é"']
        actual:   (no output)
        stderr:   unknown filter at position 0
    FAIL jq.test:1827  program did not compile: unknown function bsearch/1
        program:  bsearch(0,1,2,3,4)
        input:    [1,2,3]
        expected: ['-1', '0', '1', '2', '-4']
        actual:   (no output)
        stderr:   unknown function bsearch/1
    FAIL jq.test:1835  program did not compile: unknown function bsearch/1
        program:  bsearch({x:1})
        input:    [{ "x": 0 },{ "x": 1 },{ "x": 2 }]
        expected: ['1']
        actual:   (no output)
        stderr:   unknown function bsearch/1
    FAIL jq.test:1839  program did not compile: unknown function bsearch/1
        program:  try ["OK", bsearch(0)] catch ["KO",.]
        input:    "aa"
        expected: ['["KO","string (\\"aa\\") cannot be searched from"]']
        actual:   (no output)
        stderr:   unknown function bsearch/1
    FAIL jq.test:1843  program did not compile: unknown function strftime/1
        program:  strftime("%Y-%m-%dT%H:%M:%SZ")
        input:    [2015,2,5,23,51,47,4,63]
        expected: ['"2015-03-05T23:51:47Z"']
        actual:   (no output)
        stderr:   unknown function strftime/1
    FAIL jq.test:1847  program did not compile: unknown function strftime/1
        program:  strftime("%A, %B %d, %Y")
        input:    1435677542.822351
        expected: ['"Tuesday, June 30, 2015"']
        actual:   (no output)
        stderr:   unknown function strftime/1
    FAIL jq.test:1851  program did not compile: unknown function strftime/1
        program:  strftime("%Y-%m-%dT%H:%M:%SZ")
        input:    [2024,2,15]
        expected: ['"2024-03-15T00:00:00Z"']
        actual:   (no output)
        stderr:   unknown function strftime/1
    FAIL jq.test:1855  program did not compile: unknown filter at position 0
        program:  mktime
        input:    [2024,8,21]
        expected: ['1726876800']
        actual:   (no output)
        stderr:   unknown filter at position 0
    FAIL jq.test:1859  program did not compile: unknown filter at position 0
        program:  gmtime
        input:    1425599507
        expected: ['[2015,2,5,23,51,47,4,63]']
        actual:   (no output)
        stderr:   unknown filter at position 0
    FAIL jq.test:1863  program did not compile: unknown filter at position 0
        program:  gmtime[5]
        input:    1425599507.25
        expected: ['47.25']
        actual:   (no output)
        stderr:   unknown filter at position 0
    FAIL jq.test:1868  program did not compile: unknown function strftime/1
        program:  try strftime("%Y-%m-%dT%H:%M:%SZ") catch .
        input:    ["a",1,2,3,4,5,6,7]
        expected: ['"strftime/1 requires parsed datetime inputs"']
        actual:   (no output)
        stderr:   unknown function strftime/1
    FAIL jq.test:1872  program did not compile: unknown function strflocaltime/1
        program:  try strflocaltime("%Y-%m-%dT%H:%M:%SZ") catch .
        input:    ["a",1,2,3,4,5,6,7]
        expected: ['"strflocaltime/1 requires parsed datetime inputs"']
        actual:   (no output)
        stderr:   unknown function strflocaltime/1
    FAIL jq.test:1876  program did not compile: unknown filter at position 4
        program:  try mktime catch .
        input:    ["a",1,2,3,4,5,6,7]
        expected: ['"mktime requires parsed datetime inputs"']
        actual:   (no output)
        stderr:   unknown filter at position 4
    FAIL jq.test:1881  program did not compile: unknown function strftime/1
        program:  try ["OK", strftime([])] catch ["KO", .]
        input:    0
        expected: ['["KO","strftime/1 requires a string format"]']
        actual:   (no output)
        stderr:   unknown function strftime/1
    FAIL jq.test:1885  program did not compile: unknown function strflocaltime/1
        program:  try ["OK", strflocaltime({})] catch ["KO", .]
        input:    0
        expected: ['["KO","strflocaltime/1 requires a string format"]']
        actual:   (no output)
        stderr:   unknown function strflocaltime/1
    FAIL jq.test:1889  program did not compile: unknown function strptime/1
        program:  [strptime("%Y-%m-%dT%H:%M:%SZ")|(.,mktime)]
        input:    "2015-03-05T23:51:47Z"
        expected: ['[[2015,2,5,23,51,47,4,63],1425599507]']
        actual:   (no output)
        stderr:   unknown function strptime/1
    FAIL jq.test:1895  program did not compile: unknown function strptime/1
        program:  last(range(365 * 67)|("1970-03-01T01:02:03Z"|strptime("%Y-%m-%dT%H:%M:%SZ")|mktime) + (86400 * .)|strftime("%Y-%m-%dT%H:%M:%SZ")|strptime("%Y-%m-%dT%H:%M:%SZ"))
        input:    null
        expected: ['[2037,1,11,1,2,3,3,41]']
        actual:   (no output)
        stderr:   unknown function strptime/1
    FAIL jq.test:1997  output mismatch
        program:  try -. catch .
        input:    "very-long-long-long-long-string"
        expected: ['"string (\\"very-long-long-long-long...\\") cannot be negated"']
        actual:   ['"number required"']
    FAIL jq.test:2001  output mismatch
        program:  try (.-.) catch .
        input:    "very-long-long-long-long-string"
        expected: ['"string (\\"very-long-long-long-long...\\") and string (\\"very-long-long-long-long...\\") cannot be subtracted"']
        actual:   ['[]']
    FAIL jq.test:2005  output mismatch
        program:  "x" * range(0; 12; 2) + "☆" * 8 | try -. catch .
        input:    null
        expected: ['"string (\\"☆☆☆☆☆☆☆☆\\") cannot be negated"', '"string (\\"xx☆☆☆☆☆☆☆☆\\") cannot be negated"', '"string (\\"xxxx☆☆☆☆☆☆...\\") cannot be negated"', '"string (\\"xxxxxx☆☆☆☆☆☆...\\") cannot be negated"', '"string (\\"xxxxxxxx☆☆☆☆☆...\\") cannot be negated"', '"string (\\"xxxxxxxxxx☆☆☆☆...\\") cannot be negated"']
        actual:   ['"number required"', '"number required"', '"number required"', '"number required"', '"number required"', '"number required"']
    FAIL jq.test:2014  program did not compile: unknown filter at position 28
        program:  try (. + "x") catch . == if have_decnum then "number (12345678901234567890123456...) and string (\"x\") cannot be added" else "number (12345678901234568000000000...) and string (\"x\") cannot be added" end
        input:    123456789012345678901234567890
        expected: ['true']
        actual:   (no output)
        stderr:   unknown filter at position 28
    FAIL jq.test:2034  output mismatch
        program:  try join(",") catch .
        input:    ["1","2",{"a":{"b":{"c":33}}}]
        expected: ['"string (\\"1,2,\\") and object ({\\"a\\":{\\"b\\":{\\"c\\":33}}}) cannot be added"']
        actual:   ['"1,2,{\'a\': {\'b\': {\'c\': 33}}}"']
    FAIL jq.test:2038  output mismatch
        program:  try join(",") catch .
        input:    ["1","2",[3,4,5]]
        expected: ['"string (\\"1,2,\\") and array ([3,4,5]) cannot be added"']
        actual:   ['"1,2,[3, 4, 5]"']
    FAIL jq.test:2046  output mismatch
        program:  try (1/.) catch .
        input:    0
        expected: ['"number (1) and number (0) cannot be divided because the divisor is zero"']
        actual:   (no output)
        stderr:   float division by zero
    FAIL jq.test:2050  output mismatch
        program:  try (1/0) catch .
        input:    0
        expected: ['"number (1) and number (0) cannot be divided because the divisor is zero"']
        actual:   (no output)
        stderr:   float division by zero
    FAIL jq.test:2054  output mismatch
        program:  try (0/0) catch .
        input:    0
        expected: ['"number (0) and number (0) cannot be divided because the divisor is zero"']
        actual:   (no output)
        stderr:   float division by zero
    FAIL jq.test:2058  output mismatch
        program:  try (1%.) catch .
        input:    0
        expected: ['"number (1) and number (0) cannot be divided (remainder) because the divisor is zero"']
        actual:   (no output)
        stderr:   math domain error
    FAIL jq.test:2062  output mismatch
        program:  try (1%0) catch .
        input:    0
        expected: ['"number (1) and number (0) cannot be divided (remainder) because the divisor is zero"']
        actual:   (no output)
        stderr:   math domain error
    FAIL jq.test:2086  output mismatch
        program:  (.[{}] = 0)?
        input:    null
        expected: (no output)
        actual:   ['null']
    FAIL jq.test:2089  program did not compile: unknown function INDEX/2
        program:  INDEX(range(5)|[., "foo\(.)"]; .[0])
        input:    null
        expected: ['{"0":[0,"foo0"],"1":[1,"foo1"],"2":[2,"foo2"],"3":[3,"foo3"],"4":[4,"foo4"]}']
        actual:   (no output)
        stderr:   unknown function INDEX/2
    FAIL jq.test:2093  program did not compile: unknown function JOIN/2
        program:  JOIN({"0":[0,"abc"],"1":[1,"bcd"],"2":[2,"def"],"3":[3,"efg"],"4":[4,"fgh"]}; .[0]|tostring)
        input:    [[5,"foo"],[3,"bar"],[1,"foobar"]]
        expected: ['[[[5,"foo"],null],[[3,"bar"],[3,"efg"]],[[1,"foobar"],[1,"bcd"]]]']
        actual:   (no output)
        stderr:   unknown function JOIN/2
    FAIL jq.test:2097  program did not compile: unknown function IN/1
        program:  range(5;10)|IN(range(10))
        input:    null
        expected: ['true', 'true', 'true', 'true', 'true']
        actual:   (no output)
        stderr:   unknown function IN/1
    FAIL jq.test:2105  program did not compile: unknown function IN/1
        program:  range(5;13)|IN(range(0;10;3))
        input:    null
        expected: ['false', 'true', 'false', 'false', 'true', 'false', 'false', 'false']
        actual:   (no output)
        stderr:   unknown function IN/1
    FAIL jq.test:2116  program did not compile: unknown function IN/1
        program:  range(10;12)|IN(range(10))
        input:    null
        expected: ['false', 'false']
        actual:   (no output)
        stderr:   unknown function IN/1
    FAIL jq.test:2121  program did not compile: unknown function IN/2
        program:  IN(range(10;20); range(10))
        input:    null
        expected: ['false']
        actual:   (no output)
        stderr:   unknown function IN/2
    FAIL jq.test:2125  program did not compile: unknown function IN/2
        program:  IN(range(5;20); range(10))
        input:    null
        expected: ['true']
        actual:   (no output)
        stderr:   unknown function IN/2
    FAIL jq.test:2135  program did not compile: expected filter at position 1
        program:  (.. | select(type == "object" and has("b") and (.b | type) == "array")|.b) |= .[0]
        input:    {"a": {"b": [1, {"b": 3}]}}
        expected: ['{"a": {"b": 1}}']
        actual:   (no output)
        stderr:   expected filter at position 1
    FAIL jq.test:2139  program did not compile: unknown function isempty/1
        program:  isempty(empty)
        input:    null
        expected: ['true']
        actual:   (no output)
        stderr:   unknown function isempty/1
    FAIL jq.test:2143  program did not compile: unknown function isempty/1
        program:  isempty(range(3))
        input:    null
        expected: ['false']
        actual:   (no output)
        stderr:   unknown function isempty/1
    FAIL jq.test:2147  program did not compile: unknown function isempty/1
        program:  isempty(1,error("foo"))
        input:    null
        expected: ['false']
        actual:   (no output)
        stderr:   unknown function isempty/1
    FAIL jq.test:2152  program did not compile: unknown function index/1
        program:  index("")
        input:    ""
        expected: ['null']
        actual:   (no output)
        stderr:   unknown function index/1
    FAIL jq.test:2157  program did not compile: unknown filter at position 0
        program:  builtins|length > 10
        input:    null
        expected: ['true']
        actual:   (no output)
        stderr:   unknown filter at position 0
    FAIL jq.test:2161  program did not compile: unknown filter at position 8
        program:  "-1"|IN(builtins[] / "/"|.[1])
        input:    null
        expected: ['false']
        actual:   (no output)
        stderr:   unknown filter at position 8
    FAIL jq.test:2165  program did not compile: unknown filter at position 4
        program:  all(builtins[] / "/"; .[1]|tonumber >= 0)
        input:    null
        expected: ['true']
        actual:   (no output)
        stderr:   unknown filter at position 4
    FAIL jq.test:2169  program did not compile: unknown filter at position 0
        program:  builtins|any(.[:1] == "_")
        input:    null
        expected: ['false']
        actual:   (no output)
        stderr:   unknown filter at position 0
    FAIL jq.test:2196  program did not compile: unknown filter at position 26
        program:  .[0] | tostring | . == if have_decnum then "13911860366432393" else "13911860366432392" end
        input:    [13911860366432393]
        expected: ['true']
        actual:   (no output)
        stderr:   unknown filter at position 26
    FAIL jq.test:2200  program did not compile: unknown filter at position 22
        program:  .x | tojson | . == if have_decnum then "13911860366432393" else "13911860366432392" end
        input:    {"x":13911860366432393}
        expected: ['true']
        actual:   (no output)
        stderr:   unknown filter at position 22
    FAIL jq.test:2204  program did not compile: unknown filter at position 51
        program:  (13911860366432393 == 13911860366432392) | . == if have_decnum then false else true end
        input:    null
        expected: ['true']
        actual:   (no output)
        stderr:   unknown filter at position 51
    FAIL jq.test:2224  program did not compile: unknown filter at position 18
        program:  -. | tojson == if have_decnum then "-13911860366432393" else "-13911860366432392" end
        input:    13911860366432393
        expected: ['true']
        actual:   (no output)
        stderr:   unknown filter at position 18
    FAIL jq.test:2228  program did not compile: unknown filter at position 18
        program:  -. | tojson == if have_decnum then "0.12345678901234567890123456789" else "0.12345678901234568" end
        input:    -0.12345678901234567890123456789
        expected: ['true']
        actual:   (no output)
        stderr:   unknown filter at position 18
    FAIL jq.test:2232  program did not compile: unknown filter at position 34
        program:  [1E+1000,-1E+1000 | tojson] == if have_decnum then ["1E+1000","-1E+1000"] else ["1.7976931348623157e+308","-1.7976931348623157e+308"] end
        input:    null
        expected: ['true']
        actual:   (no output)
        stderr:   unknown filter at position 34
    FAIL jq.test:2236  output mismatch
        program:  . |= try . catch .
        input:    1
        expected: ['1']
        actual:   (no output)
        stderr:   unsupported operator
    FAIL jq.test:2250  output mismatch
        program:  abs
        input:    "abc"
        expected: ['"abc"']
        actual:   (no output)
        stderr:   number required
    FAIL jq.test:2258  program did not compile: unknown filter at position 4
        program:  map(fabs)
        input:    [-0, 0, -10, -1.1]
        expected: ['[0,0,10,1.1]']
        actual:   (no output)
        stderr:   unknown filter at position 4
    FAIL jq.test:2271  program did not compile: unknown filter at position 49
        program:  [1E+1000,-1E+1000 | abs | tojson] | unique == if have_decnum then ["1E+1000"] else ["1.7976931348623157e+308"] end
        input:    null
        expected: ['true']
        actual:   (no output)
        stderr:   unknown filter at position 49
    FAIL jq.test:2275  program did not compile: unknown filter at position 52
        program:  [1E+1000,-1E+1000 | length | tojson] | unique == if have_decnum then ["1E+1000"] else ["1.7976931348623157e+308"] end
        input:    null
        expected: ['true']
        actual:   (no output)
        stderr:   unknown filter at position 52
    FAIL jq.test:2285  output mismatch
        program:  [ label $if | range(10) | ., (select(. == 5) | break $if) ]
        input:    null
        expected: ['[0,1,2,3,4,5]']
        actual:   (no output)
        stderr:   unknown function select
    FAIL jq.test:2304  output mismatch
        program:  { a, $__loc__, c }
        input:    {"a":[1,2,3],"b":"foo","c":{"hi":"hey"}}
        expected: ['{"a":[1,2,3],"__loc__":{"file":"<top-level>","line":1},"c":{"hi":"hey"}}']
        actual:   (no output)
        stderr:   no such variable: $__loc__
    FAIL jq.test:2315  program did not compile: unknown filter at position 11
        program:  fromjson | isnan
        input:    "nan"
        expected: ['true']
        actual:   (no output)
        stderr:   unknown filter at position 11
    FAIL jq.test:2319  output mismatch
        program:  tojson | fromjson
        input:    {"a":nan}
        expected: ['{"a":null}']
        actual:   (no output)
        stderr:   Expecting value: line 1 column 6 (char 5)
    FAIL jq.test:2324  program did not compile: unknown filter at position 22
        program:  .[] | try (fromjson | isnan) catch .
        input:    ["NaN","-NaN","NaN1","NaN10","NaN100","NaN1000","NaN10000","NaN100000"]
        expected: ['true', 'true', '"Invalid numeric literal at EOF at line 1, column 4 (while parsing \'NaN1\')"', '"Invalid numeric literal at EOF at line 1, column 5 (while parsing \'NaN10\')"', '"Invalid numeric literal at EOF at line 1, column 6 (while parsing \'NaN100\')"', '"Invalid numeric literal at EOF at line 1, column 7 (while parsing \'NaN1000\')"', '"Invalid numeric literal at EOF at line 1, column 8 (while parsing \'NaN10000\')"', '"Invalid numeric literal at EOF at line 1, column 9 (while parsing \'NaN100000\')"']
        actual:   (no output)
        stderr:   unknown filter at position 22
    FAIL jq.test:2337  program did not compile: unknown filter at position 4
        program:  try input catch .
        input:    null
        expected: ['"break"']
        actual:   (no output)
        stderr:   unknown filter at position 4
    FAIL jq.test:2341  program did not compile: unknown filter at position 0
        program:  debug
        input:    1
        expected: ['1']
        actual:   (no output)
        stderr:   unknown filter at position 0
    FAIL jq.test:2354  output mismatch
        program:  try (["hi","ho"]|.[]|(try . catch (if .=="ho" then "BROKEN"|error else empty end)) | if .=="ho" then error else "\(.) there!" end) catch "caught outside \(.)"
        input:    null
        expected: ['"hi there!"', '"caught outside ho"']
        actual:   ['"hi there!"', '"caught outside error"']
    FAIL jq.test:2363  output mismatch
        program:  try (try error catch "inner catch \(.)") catch "outer catch \(.)"
        input:    "foo"
        expected: ['"inner catch foo"']
        actual:   ['"inner catch error"']
    FAIL jq.test:2367  output mismatch
        program:  try ((try error catch "inner catch \(.)")|error) catch "outer catch \(.)"
        input:    "foo"
        expected: ['"outer catch inner catch foo"']
        actual:   ['"outer catch error"']
    FAIL jq.test:2372  program did not compile: unknown function first/1
        program:  first(.?,.?)
        input:    null
        expected: ['null']
        actual:   (no output)
        stderr:   unknown function first/1
    FAIL jq.test:2377  output mismatch
        program:  {foo: "bar"} | .foo |= .?
        input:    null
        expected: ['{"foo": "bar"}']
        actual:   (no output)
        stderr:   invalid update path
    FAIL jq.test:2382  output mismatch
        program:  . |= try 2
        input:    1
        expected: ['2']
        actual:   (no output)
        stderr:   unsupported operator
    FAIL jq.test:2386  output mismatch
        program:  . |= try 2 catch 3
        input:    1
        expected: ['2']
        actual:   (no output)
        stderr:   unsupported operator
    FAIL jq.test:2390  output mismatch
        program:  .[] |= try tonumber
        input:    ["1", "2a", "3", " 4", "5 ", "6.7", ".89", "-876", "+5.43", 21]
        expected: ['[1, 3, 6.7, 0.89, -876, 5.43, 21]']
        actual:   (no output)
        stderr:   invalid literal for int() with base 10: '2a'
    FAIL jq.test:2403  program did not compile: unknown filter at position 0
        program:  implode|explode
        input:    [-1,0,1,2,3,1114111,1114112,55295,55296,57343,57344,1.1,1.9]
        expected: ['[65533,0,1,2,3,1114111,65533,55295,65533,65533,57344,1,1]']
        actual:   (no output)
        stderr:   unknown filter at position 0
    FAIL jq.test:2407  program did not compile: unknown filter at position 8
        program:  map(try implode catch .)
        input:    [123,["a"],[nan]]
        expected: ['["implode input must be an array","string (\\"a\\") can\'t be imploded, unicode codepoint needs to be numeric","number (null) can\'t be imploded, unicode codepoint needs to be numeric"]']
        actual:   (no output)
        stderr:   unknown filter at position 8
    FAIL jq.test:2411  program did not compile: unknown filter at position 6
        program:  try 0[implode] catch .
        input:    []
        expected: ['"Cannot index number with string (\\"\\")"']
        actual:   (no output)
        stderr:   unknown filter at position 6
    FAIL jq.test:2416  program did not compile: unknown function walk/1
        program:  walk(.)
        input:    {"x":0}
        expected: ['{"x":0}']
        actual:   (no output)
        stderr:   unknown function walk/1
    FAIL jq.test:2420  program did not compile: unknown function walk/1
        program:  walk(1)
        input:    {"x":0}
        expected: ['1']
        actual:   (no output)
        stderr:   unknown function walk/1
    FAIL jq.test:2425  program did not compile: unknown function walk/1
        program:  [walk(.,1)]
        input:    {"x":0}
        expected: ['[{"x":0},1]']
        actual:   (no output)
        stderr:   unknown function walk/1
    FAIL jq.test:2430  program did not compile: unknown function IN/1
        program:  walk(select(IN({}, []) | not))
        input:    {"a":1,"b":[]}
        expected: ['{"a":1}']
        actual:   (no output)
        stderr:   unknown function IN/1
    FAIL jq.test:2435  output mismatch
        program:  [range(10)] | .[1.2:3.5]
        input:    null
        expected: ['[1,2,3]']
        actual:   (no output)
        stderr:   slice indices must be integers or None or have an __index__ method
    FAIL jq.test:2439  output mismatch
        program:  [range(10)] | .[1.5:3.5]
        input:    null
        expected: ['[1,2,3]']
        actual:   (no output)
        stderr:   slice indices must be integers or None or have an __index__ method
    FAIL jq.test:2443  output mismatch
        program:  [range(10)] | .[1.7:3.5]
        input:    null
        expected: ['[1,2,3]']
        actual:   (no output)
        stderr:   slice indices must be integers or None or have an __index__ method
    FAIL jq.test:2447  output mismatch
        program:  [range(10)] | .[1.7:4294967295]
        input:    null
        expected: ['[1,2,3,4,5,6,7,8,9]']
        actual:   (no output)
        stderr:   slice indices must be integers or None or have an __index__ method
    FAIL jq.test:2451  output mismatch
        program:  [range(10)] | .[1.7:-4294967296]
        input:    null
        expected: ['[]']
        actual:   (no output)
        stderr:   slice indices must be integers or None or have an __index__ method
    FAIL jq.test:2455  output mismatch
        program:  [[range(10)] | .[1.1,1.5,1.7]]
        input:    null
        expected: ['[1,1,1]']
        actual:   (no output)
        stderr:   cannot index
    FAIL jq.test:2459  output mismatch
        program:  [range(5)] | .[1.1] = 5
        input:    null
        expected: ['[0,5,2,3,4]']
        actual:   (no output)
        stderr:   invalid update path
    FAIL jq.test:2463  output mismatch
        program:  [range(3)] | .[nan:1]
        input:    null
        expected: ['[0]']
        actual:   (no output)
        stderr:   unknown function nan
    FAIL jq.test:2467  output mismatch
        program:  [range(3)] | .[1:nan]
        input:    null
        expected: ['[1,2]']
        actual:   (no output)
        stderr:   unknown function nan
    FAIL jq.test:2471  output mismatch
        program:  [range(3)] | .[nan]
        input:    null
        expected: ['null']
        actual:   (no output)
        stderr:   unknown function nan
    FAIL jq.test:2475  output mismatch
        program:  try ([range(3)] | .[nan] = 9) catch .
        input:    null
        expected: ['"Cannot set array element at NaN index"']
        actual:   ['"invalid update path"']
    FAIL jq.test:2479  output mismatch
        program:  try ("foobar" | .[1.5:3.5] = "xyz") catch .
        input:    null
        expected: ['"Cannot update string slices"']
        actual:   ['"invalid update path"']
    FAIL jq.test:2483  output mismatch
        program:  try ([range(10)] | .[1.5:3.5] = ["xyz"]) catch .
        input:    null
        expected: ['[0,"xyz",4,5,6,7,8,9]']
        actual:   ['"invalid update path"']
    FAIL jq.test:2487  output mismatch
        program:  try ("foobar" | .[1.5]) catch .
        input:    null
        expected: ['"Cannot index string with number (1.5)"']
        actual:   ['"cannot index"']
    FAIL jq.test:2494  output mismatch
        program:  try ["ok", setpath([1]; 1)] catch ["ko", .]
        input:    {"hi":"hello"}
        expected: ['["ko","Cannot index object with number (1)"]']
        actual:   ['["ok",{"hi":"hello","1":1}]']
    FAIL jq.test:2498  output mismatch
        program:  try fromjson catch .
        input:    "{'a': 123}"
        expected: ['"Invalid string literal; expected \\", but got \' at line 1, column 5 (while parsing \'{\'a\': 123}\')"']
        actual:   ['"Expecting property name enclosed in double quotes: line 1 column 2 (char 1)"']
    FAIL jq.test:2504  output mismatch
        program:  try ltrimstr(1) catch "x", try rtrimstr(1) catch "x" | "ok"
        input:    "hi"
        expected: ['"ok"', '"ok"']
        actual:   (no output)
        stderr:   startswith first arg must be str or a tuple of str, not int
    FAIL jq.test:2509  output mismatch
        program:  try ltrimstr("x") catch "x", try rtrimstr("x") catch "x" | "ok"
        input:    {"hey":[]}
        expected: ['"ok"', '"ok"']
        actual:   (no output)
        stderr:   'dict' object has no attribute 'startswith'
    FAIL jq.test:2516  output mismatch
        program:  .[] as [$x, $y] | try ["ok", ($x | ltrimstr($y))] catch ["ko", .]
        input:    [["hi",1],[1,"hi"],["hi","hi"],[1,1]]
        expected: ['["ko","startswith() requires string inputs"]', '["ko","startswith() requires string inputs"]', '["ok",""]', '["ko","startswith() requires string inputs"]']
        actual:   (no output)
        stderr:   startswith first arg must be str or a tuple of str, not int
    FAIL jq.test:2523  output mismatch
        program:  .[] as [$x, $y] | try ["ok", ($x | rtrimstr($y))] catch ["ko", .]
        input:    [["hi",1],[1,"hi"],["hi","hi"],[1,1]]
        expected: ['["ko","endswith() requires string inputs"]', '["ko","endswith() requires string inputs"]', '["ok",""]', '["ko","endswith() requires string inputs"]']
        actual:   (no output)
        stderr:   endswith first arg must be str or a tuple of str, not int
    FAIL jq.test:2533  output mismatch
        program:  try ["OK", setpath([[1]]; 1)] catch ["KO", .]
        input:    []
        expected: ['["KO","Cannot update field at array index of array"]']
        actual:   (no output)
        stderr:   int() argument must be a string, a bytes-like object or a real number, not 'list'
    FAIL jq.test:2548  program did not compile: unknown function strflocaltime/1
        program:  strflocaltime("" | ., @uri)
        input:    0
        expected: ['""', '""']
        actual:   (no output)
        stderr:   unknown function strflocaltime/1
    FAIL jq.test:2573  output mismatch
        program:  setpath([range(10000) | 0]; 0) | flatten
        input:    null
        expected: ['[0]']
        actual:   (no output)
        stderr:   'NoneType' object is not reversible
    FAIL jq.test:2577  output mismatch
        program:  try setpath([range(10001) | 0]; 0) catch .
        input:    null
        expected: ['"Path too deep"']
        actual:   ['null']
    FAIL jq.test:2585  output mismatch
        program:  try getpath([range(10001) | 0]) catch .
        input:    null
        expected: ['"Path too deep"']
        actual:   ['null']
    FAIL jq.test:2593  output mismatch
        program:  try delpaths([[range(10001) | 0]]) catch .
        input:    null
        expected: ['"Path too deep"']
        actual:   ['null']
    jq conformance: 264 passed, 273 failed, 0 errored, 13 skipped (corpus jq.test @ jq-1.8.2)

## Post-build programmatic acceptance
- PASS: verify-001-harness-list (FEATURE-VERIFY-001.md)
  intent: The staged conformance runner can parse the staged corpus and exclusions without a harness error.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
  stdout:
    run  jq.test:48  .
    run  jq.test:58  .
    
    2 cases, 0 excluded
- PASS: verify-001-script-contract (FEATURE-VERIFY-001.md)
  intent: The staged scoring script is executable by POSIX sh and reaches the candidate interface check.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
  stdout:
    FAIL jq.test:39  program did not compile: expected } at position 19
        program:  {x:-1},{x:-.},{x:-.|abs}
        input:    1
        expected: ['{"x":-1}', '{"x":-1}', '{"x":1}']
        actual:   (no output)
        stderr:   expected } at position 19
    FAIL jq.test:48  output mismatch
        program:  .
        input:    ﻿"byte order mark"
        expected: ['"byte order mark"']
        actual:   (no output)
        stderr:   Unexpected UTF-8 BOM (decode using utf-8-sig): line 1 column 1 (char 0)
    FAIL jq.test:72  output mismatch
        program:  @text,@json,([1,.]|@csv,@tsv),@html,(@uri|.,@urid),@sh,(@base64|.,@base64d)
        input:    "!()<>&'\"\t"
        expected: ['"!()<>&\'\\"\\t"', '"\\"!()<>&\'\\\\\\"\\\\t\\""', '"1,\\"!()<>&\'\\"\\"\\t\\""', '"1\\t!()<>&\'\\"\\\\t"', '"!()&lt;&gt;&amp;&apos;&quot;\\t"', '"%21%28%29%3C%3E%26%27%22%09"', '"!()<>&\'\\"\\t"', '"\'!()<>&\'\\\\\'\'\\"\\t\'"', '"ISgpPD4mJyIJ"', '"!()<>&\'\\"\\t"']
        actual:   (no output)
        stderr:   unsupported filter
    FAIL jq.test:86  output mismatch
        program:  @base64
        input:    "foóbar\n"
        expected: ['"Zm/Ds2Jhcgo="']
        actual:   (no output)
        stderr:   unsupported filter
    FAIL jq.test:90  output mismatch
        program:  @base64d
        input:    "Zm/Ds2Jhcgo="
        expected: ['"foóbar\\n"']
        actual:   (no output)
        stderr:   unsupported filter
    FAIL jq.test:94  output mismatch
        program:  @uri
        input:    "\u03bc"
        expected: ['"%CE%BC"']
        actual:   (no output)
        stderr:   unsupported filter
    FAIL jq.test:98  output mismatch
        program:  @urid
        input:    "%CE%BC"
        expected: ['"\\u03bc"']
        actual:   (no output)
        stderr:   unsupported filter
    FAIL jq.test:102  program did not compile: unexpected token at position 6
        program:  @html "<b>\(.)</b>"
        input:    "<script>hax</script>"
        expected: ['"<b>&lt;script&gt;hax&lt;/script&gt;</b>"']
        actual:   (no output)
        stderr:   unexpected token at position 6
    FAIL jq.test:122  output mismatch
        program:  {"a",b,"a$\(1+1)"}
        input:    {"a":1, "b":2, "c":3, "a$2":4}
        expected: ['{"a":1, "b":2, "a$2":4}']
        actual:   ['{"a":1,"b":2,"[(\'text\', \'a$\'), (\'expr\', \'1+1\')]":null}']
    FAIL jq.test:127  program was accepted, but the corpus marks it %%FAIL
        program:  {(0):1}
    FAIL jq.test:139  program was accepted, but the corpus marks it %%FAIL
        program:  {non_const:., (0):1}
    FAIL jq.test:168  program did not compile: unexpected token at position 1
        program:  ."foo"."bar"
        input:    {"foo": {"bar": 20}}
        expected: ['20']
        actual:   (no output)
        stderr:   unexpected token at position 1
    FAIL jq.test:183  output mismatch
        program:  [.[]|.foo?.bar?]
        input:    [1,[2],[],{"foo":3},{"foo":{"bar":4}},{}]
        expected: ['[4,null]']
        actual:   ['[4]']
    FAIL jq.test:187  program did not compile: expected filter at position 1
        program:  [..]
        input:    [1,[[2]],{ "a":[1]}]
        expected: ['[[1,[[2]],{"a":[1]}],1,[[2]],[2],2,{"a":[1]},[1],1]']
        actual:   (no output)
        stderr:   expected filter at position 1
    FAIL jq.test:195  output mismatch
        program:  [.[]|.[1:3]?]
        input:    [1,null,true,false,"abcdef",{},{"a":1,"b":2},[],[1,2,3,4,5],[1,2]]
        expected: ['[null,"bc",[],[2,3],[2]]']
        actual:   (no output)
        stderr:   'int' object is not subscriptable
    FAIL jq.test:200  program did not compile: expected ) at position 28
        program:  map(try .a[] catch ., try .a.[] catch ., .a[]?, .a.[]?)
        input:    [{"a": [1,2]}, {"a": 123}]
        expected: ['[1,2,1,2,1,2,1,2,"Cannot iterate over number (123)","Cannot iterate over number (123)"]']
        actual:   (no output)
        stderr:   expected ) at position 28
    FAIL jq.test:205  output mismatch
        program:  try ["OK", (.[] | error)] catch ["KO", .]
        input:    {"a":["b"],"c":["d"]}
        expected: ['["KO",["b"]]']
        actual:   ['["KO","error"]']
    FAIL jq.test:213  output mismatch
        program:  try (.foo[-1] = 0) catch .
        input:    null
        expected: ['"Out of bounds negative array index"']
        actual:   (no output)
        stderr:   'NoneType' object is not subscriptable
    FAIL jq.test:217  output mismatch
        program:  try (.foo[-2] = 0) catch .
        input:    null
        expected: ['"Out of bounds negative array index"']
        actual:   (no output)
        stderr:   'NoneType' object is not subscriptable
    FAIL jq.test:229  output mismatch
        program:  try (.[999999999] = 0) catch .
        input:    null
        expected: ['"Array index too large"']
        actual:   ['null']
    FAIL jq.test:277  output mismatch
        program:  {x: (1,2)},{x:3} | .x
        input:    null
        expected: ['1', '2', '3']
        actual:   ['2', '3']
    FAIL jq.test:283  output mismatch
        program:  [.[-4,-3,-2,-1,0,1,2,3]]
        input:    [1,2,3]
        expected: ['[null,1,2,3,1,2,3,null]']
        actual:   (no output)
        stderr:   cannot index
    FAIL jq.test:291  output mismatch
        program:  [range(0,1;3,4)]
        input:    null
        expected: ['[0,1,2, 0,1,2,3, 1,2, 1,2,3]']
        actual:   ['[0,1,2]']
    FAIL jq.test:307  output mismatch
        program:  [range(0,1;4,5;1,2)]
        input:    null
        expected: ['[0,1,2,3,0,2, 0,1,2,3,4,0,2,4, 1,2,3,1,3, 1,2,3,4,1,3]']
        actual:   ['[0,1,2,3]']
    FAIL jq.test:311  program did not compile: unknown function while/2
        program:  [while(.<100; .*2)]
        input:    1
        expected: ['[1,2,4,8,16,32,64]']
        actual:   (no output)
        stderr:   unknown function while/2
    FAIL jq.test:329  program did not compile: unknown function until/2
        program:  [.[]|[.,1]|until(.[0] < 1; [.[0] - 1, .[1] * .[0]])|.[1]]
        input:    [1,2,3,4,5]
        expected: ['[1,2,6,24,120]']
        actual:   (no output)
        stderr:   unknown function until/2
    FAIL jq.test:345  output mismatch
        program:  [foreach .[] as {a:$a} (0; . + $a; -.)]
        input:    [{"a":1}, {"b":2}, {"a":3, "b":4}]
        expected: ['[-1, -1, -4]']
        actual:   (no output)
        stderr:   unsupported operand type(s) for +: 'float' and 'NoneType'
    FAIL jq.test:361  program did not compile: unknown function limit/2
        program:  [limit(3; .[])]
        input:    [11,22,33,44,55,66,77,88,99]
        expected: ['[11,22,33]']
        actual:   (no output)
        stderr:   unknown function limit/2
    FAIL jq.test:365  program did not compile: unknown function limit/2
        program:  [limit(0; error)]
        input:    "badness"
        expected: ['[]']
        actual:   (no output)
        stderr:   unknown function limit/2
    FAIL jq.test:369  program did not compile: unknown function limit/2
        program:  [limit(1; 1, error)]
        input:    "badness"
        expected: ['[1]']
        actual:   (no output)
        stderr:   unknown function limit/2
    FAIL jq.test:373  program did not compile: unknown function limit/2
        program:  try limit(-1; error) catch .
        input:    null
        expected: ['"limit doesn\'t support negative count"']
        actual:   (no output)
        stderr:   unknown function limit/2
    FAIL jq.test:377  program did not compile: unknown function skip/2
        program:  [skip(3; .[])]
        input:    [1,2,3,4,5,6,7,8,9]
        expected: ['[4,5,6,7,8,9]']
        actual:   (no output)
        stderr:   unknown function skip/2
    FAIL jq.test:381  program did not compile: unknown function skip/2
        program:  [skip(0,2,3,4; .[])]
        input:    [1,2,3]
        expected: ['[1,2,3,3]']
        actual:   (no output)
        stderr:   unknown function skip/2
    FAIL jq.test:385  program did not compile: unknown function skip/2
        program:  [skip(3; .[])]
        input:    []
        expected: ['[]']
        actual:   (no output)
        stderr:   unknown function skip/2
    FAIL jq.test:389  program did not compile: unknown function skip/2
        program:  try skip(-1; error) catch .
        input:    null
        expected: ['"skip doesn\'t support negative count"']
        actual:   (no output)
        stderr:   unknown function skip/2
    FAIL jq.test:393  program did not compile: unknown function nth/2
        program:  nth(1; 0,1,error("foo"))
        input:    null
        expected: ['1']
        actual:   (no output)
        stderr:   unknown function nth/2
    FAIL jq.test:397  program did not compile: unknown function first/1
        program:  [first(range(.)), last(range(.))]
        input:    10
        expected: ['[0,9]']
        actual:   (no output)
        stderr:   unknown function first/1
    FAIL jq.test:401  program did not compile: unknown function first/1
        program:  [first(range(.)), last(range(.))]
        input:    0
        expected: ['[]']
        actual:   (no output)
        stderr:   unknown function first/1
    FAIL jq.test:405  program did not compile: unknown function nth/2
        program:  [nth(0,5,9,10,15; range(.)), try nth(-1; range(.)) catch .]
        input:    10
        expected: ['[0,5,9,"nth doesn\'t support negative indices"]']
        actual:   (no output)
        stderr:   unknown function nth/2
    FAIL jq.test:410  program did not compile: unknown function first/1
        program:  first(1,error("foo"))
        input:    null
        expected: ['1']
        actual:   (no output)
        stderr:   unknown function first/1
    FAIL jq.test:420  program did not compile: unknown function limit/2
        program:  [limit(5,7; range(9))]
        input:    null
        expected: ['[0,1,2,3,4,0,1,2,3,4,5,6]']
        actual:   (no output)
        stderr:   unknown function limit/2
    FAIL jq.test:425  program did not compile: unknown function nth/2
        program:  [nth(5,7; range(9;0;-1))]
        input:    null
        expected: ['[4,2]']
        actual:   (no output)
        stderr:   unknown function nth/2
    FAIL jq.test:430  output mismatch
        program:  [range(0,1,2;4,3,2;2,3)]
        input:    null
        expected: ['[0,2,0,3,0,2,0,0,0,1,3,1,1,1,1,1,2,2,2,2]']
        actual:   ['[0,2]']
    FAIL jq.test:435  output mismatch
        program:  [range(3,5)]
        input:    null
        expected: ['[0,1,2,0,1,2,3,4]']
        actual:   ['[0,1,2]']
    FAIL jq.test:440  program did not compile: unknown function index/1
        program:  [(index(",","|"), rindex(",","|")), indices(",","|")]
        input:    "a,b|c,d,e||f,g,h,|,|,i,j"
        expected: ['[1,3,22,19,[1,5,7,12,14,16,18,20,22],[3,9,10,17,19]]']
        actual:   (no output)
        stderr:   unknown function index/1
    FAIL jq.test:445  output mismatch
        program:  join(",","/")
        input:    ["a","b","c","d"]
        expected: ['"a,b,c,d"', '"a/b/c/d"']
        actual:   ['"a,b,c,d"']
    FAIL jq.test:455  output mismatch
        program:  flatten(3,2,1)
        input:    [0, [1], [[2]], [[[3]]]]
        expected: ['[0,1,2,3]', '[0,1,2,[3]]', '[0,1,[2],[[3]]]']
        actual:   (no output)
        stderr:   'int' object is not reversible
    FAIL jq.test:466  output mismatch
        program:  [.[3:2], .[-5:4], .[:-2], .[-2:], .[3:3][1:], .[10:]]
        input:    [0,1,2,3,4,5,6]
        expected: ['[[], [2,3], [0,1,2,3,4], [5,6], [], []]']
        actual:   (no output)
        stderr:   slice indices must be integers or None or have an __index__ method
    FAIL jq.test:470  output mismatch
        program:  [.[3:2], .[-5:4], .[:-2], .[-2:], .[3:3][1:], .[10:]]
        input:    "abcdefghi"
        expected: ['["","","abcdefg","hi","",""]']
        actual:   (no output)
        stderr:   slice indices must be integers or None or have an __index__ method
    FAIL jq.test:474  program did not compile: unknown function del/1
        program:  del(.[2:4],.[0],.[-2:])
        input:    [0,1,2,3,4,5,6,7]
        expected: ['[1,4,5]']
        actual:   (no output)
        stderr:   unknown function del/1
    FAIL jq.test:478  output mismatch
        program:  .[2:4] = ([], ["a","b"], ["a","b","c"])
        input:    [0,1,2,3,4,5,6,7]
        expected: ['[0,1,4,5,6,7]', '[0,1,"a","b",4,5,6,7]', '[0,1,"a","b","c",4,5,6,7]']
        actual:   (no output)
        stderr:   invalid update path
    FAIL jq.test:530  program did not compile: expected : at position 29
        program:  . as {as: $kw, "str": $str, ("e"+"x"+"p"): $exp} | [$kw, $str, $exp]
        input:    {"as": 1, "str": 2, "exp": 3}
        expected: ['[1, 2, 3]']
        actual:   (no output)
        stderr:   expected : at position 29
    FAIL jq.test:548  program was accepted, but the corpus marks it %%FAIL
        program:  . as [] | null
    FAIL jq.test:554  program was accepted, but the corpus marks it %%FAIL
        program:  . as {} | null
    FAIL jq.test:601  output mismatch
        program:  .+null
        input:    {"a":42}
        expected: ['{"a":42}']
        actual:   (no output)
        stderr:   unsupported operand type(s) for +: 'dict' and 'NoneType'
    FAIL jq.test:605  output mismatch
        program:  null+.
        input:    null
        expected: ['null']
        actual:   (no output)
        stderr:   unsupported operand type(s) for +: 'NoneType' and 'NoneType'
    FAIL jq.test:609  output mismatch
        program:  .a+.b
        input:    {"a":42}
        expected: ['42']
        actual:   (no output)
        stderr:   unsupported operand type(s) for +: 'int' and 'NoneType'
    FAIL jq.test:661  output mismatch
        program:  9E999999999, 9999999999E999999990, 1E-999999999, 0.000000001E-999999990
        input:    null
        expected: ['9E+999999999', '9.999999999E+999999999', '1E-999999999', '1E-999999999']
        actual:   (no output)
        stderr:   Out of range float values are not JSON compliant: inf
    FAIL jq.test:689  output mismatch
        program:  [(infinite, -infinite) % (1, -1, infinite)]
        input:    null
        expected: ['[0,0,0,0,0,-1]']
        actual:   (no output)
        stderr:   unknown function infinite
    FAIL jq.test:693  program did not compile: unknown filter at position 20
        program:  [nan % 1, 1 % nan | isnan]
        input:    null
        expected: ['[true,true]']
        actual:   (no output)
        stderr:   unknown filter at position 20
    FAIL jq.test:701  output mismatch
        program:  "123\u0000456" | try tonumber catch .
        input:    null
        expected: ['"string (\\"123\\\\u0000456\\") cannot be parsed as a number"']
        actual:   (no output)
        stderr:   invalid literal for int() with base 10: '123\x00456'
    FAIL jq.test:705  program did not compile: unknown filter at position 4
        program:  map(toboolean)
        input:    ["false","true",false,true]
        expected: ['[false,true,false,true]']
        actual:   (no output)
        stderr:   unknown filter at position 4
    FAIL jq.test:709  program did not compile: unknown filter at position 10
        program:  .[] | try toboolean catch .
        input:    [null,0,"tru","truee","fals","falsee",[],{}]
        expected: ['"null (null) cannot be parsed as a boolean"', '"number (0) cannot be parsed as a boolean"', '"string (\\"tru\\") cannot be parsed as a boolean"', '"string (\\"truee\\") cannot be parsed as a boolean"', '"string (\\"fals\\") cannot be parsed as a boolean"', '"string (\\"falsee\\") cannot be parsed as a boolean"', '"array ([]) cannot be parsed as a boolean"', '"object ({}) cannot be parsed as a boolean"']
        actual:   (no output)
        stderr:   unknown filter at position 10
    FAIL jq.test:720  program did not compile: unknown filter at position 35
        program:  "true\u0000x", "false\u0000" | try toboolean catch .
        input:    null
        expected: ['"string (\\"true\\\\u0000x\\") cannot be parsed as a boolean"', '"string (\\"false\\\\u0000\\") cannot be parsed as a boolean"']
        actual:   (no output)
        stderr:   unknown filter at position 35
    FAIL jq.test:741  output mismatch
        program:  utf8bytelength
        input:    "asdf\u03bc"
        expected: ['6']
        actual:   ['5']
    FAIL jq.test:745  output mismatch
        program:  [.[] | try utf8bytelength catch .]
        input:    [[], {}, [1,2], 55, true, false]
        expected: ['["array ([]) only strings have UTF-8 byte length","object ({}) only strings have UTF-8 byte length","array ([1,2]) only strings have UTF-8 byte length","number (55) only strings have UTF-8 byte length","boolean (true) only strings have UTF-8 byte length","boolean (false) only strings have UTF-8 byte length"]']
        actual:   ['[0,0,2,55,1,0]']
    FAIL jq.test:758  output mismatch
        program:  map(add)
        input:    [[], [1,2,3], ["a","b","c"], [[3],[4,5],[6]], [{"a":1}, {"b":2}, {"a":3}]]
        expected: ['[null, 6, "abc", [3,4,5,6], {"a":3, "b": 2}]']
        actual:   (no output)
        stderr:   sequence item 0: expected str instance, list found
    FAIL jq.test:766  output mismatch
        program:  [add(null), add(range(range(10))), add(empty), add(10,range(10))]
        input:    null
        expected: ['[null,120,null,55]']
        actual:   (no output)
        stderr:   can only join an iterable
    FAIL jq.test:771  output mismatch
        program:  .sum = add(.arr[])
        input:    {"arr":[]}
        expected: ['{"arr":[],"sum":null}']
        actual:   (no output)
        stderr:   cannot index
    FAIL jq.test:775  output mismatch
        program:  add({(.[]):1}) | keys
        input:    ["a","a","b","a","d","b","d","a","d"]
        expected: ['["a","b","d"]']
        actual:   (no output)
        stderr:   'str' object has no attribute 'keys'
    FAIL jq.test:847  program did not compile: unknown filter at position 0
        program:  atan * 4 * 1000000|floor / 1000000
        input:    1
        expected: ['3.141592']
        actual:   (no output)
        stderr:   unknown filter at position 0
    FAIL jq.test:851  program did not compile: unknown filter at position 37
        program:  [(3.141592 / 2) * (range(0;20) / 20)|cos * 1000000|floor / 1000000]
        input:    null
        expected: ['[1,0.996917,0.987688,0.972369,0.951056,0.923879,0.891006,0.85264,0.809017,0.760406,0.707106,0.649448,0.587785,0.522498,0.45399,0.382683,0.309017,0.233445,0.156434,0.078459]']
        actual:   (no output)
        stderr:   unknown filter at position 37
    FAIL jq.test:855  program did not compile: unknown filter at position 37
        program:  [(3.141592 / 2) * (range(0;20) / 20)|sin * 1000000|floor / 1000000]
        input:    null
        expected: ['[0,0.078459,0.156434,0.233445,0.309016,0.382683,0.45399,0.522498,0.587785,0.649447,0.707106,0.760405,0.809016,0.85264,0.891006,0.923879,0.951056,0.972369,0.987688,0.996917]']
        actual:   (no output)
        stderr:   unknown filter at position 37
    FAIL jq.test:933  program did not compile: variable is not defined at position 29
        program:  . as {$a, $b:[$c, $d]}| [$a, $b, $c, $d]
        input:    {"a":1, "b":[2,{"d":3}]}
        expected: ['[1,[2,{"d":3}],2,{"d":3}]']
        actual:   (no output)
        stderr:   variable is not defined at position 29
    FAIL jq.test:1062  output mismatch
        program:  any(true, error; .)
        input:    "badness"
        expected: ['true']
        actual:   (no output)
        stderr:   error
    FAIL jq.test:1066  output mismatch
        program:  all(false, error; .)
        input:    "badness"
        expected: ['false']
        actual:   (no output)
        stderr:   error
    FAIL jq.test:1070  output mismatch
        program:  any(not)
        input:    []
        expected: ['false']
        actual:   (no output)
        stderr:   'bool' object is not iterable
    FAIL jq.test:1074  output mismatch
        program:  all(not)
        input:    []
        expected: ['true']
        actual:   (no output)
        stderr:   'bool' object is not iterable
    FAIL jq.test:1078  output mismatch
        program:  any(not)
        input:    [false]
        expected: ['true']
        actual:   (no output)
        stderr:   'bool' object is not iterable
    FAIL jq.test:1082  output mismatch
        program:  all(not)
        input:    [false]
        expected: ['true']
        actual:   (no output)
        stderr:   'bool' object is not iterable
    FAIL jq.test:1110  program did not compile: unknown function path/1
        program:  path(.foo[0,1])
        input:    null
        expected: ['["foo", 0]', '["foo", 1]']
        actual:   (no output)
        stderr:   unknown function path/1
    FAIL jq.test:1115  program did not compile: unknown function path/1
        program:  path(.[] | select(.>3))
        input:    [1,5,3]
        expected: ['[1]']
        actual:   (no output)
        stderr:   unknown function path/1
    FAIL jq.test:1119  program did not compile: unknown function path/1
        program:  path(.)
        input:    42
        expected: ['[]']
        actual:   (no output)
        stderr:   unknown function path/1
    FAIL jq.test:1123  program did not compile: unknown function path/1
        program:  try path(.a | map(select(.b == 0))) catch .
        input:    {"a":[{"b":0}]}
        expected: ['"Invalid path expression with result [{\\"b\\":0}]"']
        actual:   (no output)
        stderr:   unknown function path/1
    FAIL jq.test:1127  program did not compile: unknown function path/1
        program:  try path(.a | map(select(.b == 0)) | .[0]) catch .
        input:    {"a":[{"b":0}]}
        expected: ['"Invalid path expression near attempt to access element 0 of [{\\"b\\":0}]"']
        actual:   (no output)
        stderr:   unknown function path/1
    FAIL jq.test:1131  program did not compile: unknown function path/1
        program:  try path(.a | map(select(.b == 0)) | .c) catch .
        input:    {"a":[{"b":0}]}
        expected: ['"Invalid path expression near attempt to access element \\"c\\" of [{\\"b\\":0}]"']
        actual:   (no output)
        stderr:   unknown function path/1
    FAIL jq.test:1135  program did not compile: unknown function path/1
        program:  try path(.a | map(select(.b == 0)) | .[]) catch .
        input:    {"a":[{"b":0}]}
        expected: ['"Invalid path expression near attempt to iterate through [{\\"b\\":0}]"']
        actual:   (no output)
        stderr:   unknown function path/1
    FAIL jq.test:1139  program did not compile: unknown function path/1
        program:  path(.a[path(.b)[0]])
        input:    {"a":{"b":0}}
        expected: ['["a","b"]']
        actual:   (no output)
        stderr:   unknown function path/1
    FAIL jq.test:1143  program did not compile: unknown filter at position 1
        program:  [paths]
        input:    [1,[[],{"a":2}]]
        expected: ['[[0],[1],[1,0],[1,1],[1,1,"a"]]']
        actual:   (no output)
        stderr:   unknown filter at position 1
    FAIL jq.test:1173  output mismatch
        program:  try delpaths(0) catch .
        input:    {}
        expected: ['"Paths must be specified as an array"']
        actual:   (no output)
        stderr:   'int' object is not iterable
    FAIL jq.test:1177  program did not compile: unknown function del/1
        program:  del(.), del(empty), del((.foo,.bar,.baz) | .[2,3,0]), del(.foo[0], .bar[0], .foo, .baz.bar[0].x)
        input:    {"foo": [0,1,2,3,4], "bar": [0,1]}
        expected: ['null', '{"foo": [0,1,2,3,4], "bar": [0,1]}', '{"foo": [1,4], "bar": [1]}', '{"bar": [1]}']
        actual:   (no output)
        stderr:   unknown function del/1
    FAIL jq.test:1184  program did not compile: unknown function del/1
        program:  del(.[1], .[-6], .[2], .[-3:9])
        input:    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        expected: ['[0, 3, 5, 6, 9]']
        actual:   (no output)
        stderr:   unknown function del/1
    FAIL jq.test:1188  program did not compile: unknown function del/1
        program:  del(.[nan])
        input:    [1,2,3]
        expected: ['[1,2,3]']
        actual:   (no output)
        stderr:   unknown function del/1
    FAIL jq.test:1192  program did not compile: unknown function del/1
        program:  del(.[nan,nan])
        input:    [1,2,3]
        expected: ['[1,2,3]']
        actual:   (no output)
        stderr:   unknown function del/1
    FAIL jq.test:1201  program did not compile: unknown function pick/1
        program:  pick(.a.b.c)
        input:    null
        expected: ['{"a":{"b":{"c":null}}}']
        actual:   (no output)
        stderr:   unknown function pick/1
    FAIL jq.test:1205  program did not compile: unknown filter at position 5
        program:  pick(first)
        input:    [1,2]
        expected: ['[1]']
        actual:   (no output)
        stderr:   unknown filter at position 5
    FAIL jq.test:1209  program did not compile: unknown filter at position 5
        program:  pick(first|first)
        input:    [[10,20],30]
        expected: ['[[10]]']
        actual:   (no output)
        stderr:   unknown filter at position 5
    FAIL jq.test:1214  program did not compile: unknown filter at position 9
        program:  try pick(last) catch .
        input:    [1,2]
        expected: ['"Out of bounds negative array index"']
        actual:   (no output)
        stderr:   unknown filter at position 9
    FAIL jq.test:1225  output mismatch
        program:  .foo = .bar
        input:    {"bar":42}
        expected: ['{"foo":42, "bar":42}']
        actual:   (no output)
        stderr:   cannot index
    FAIL jq.test:1233  output mismatch
        program:  .[] += 2, .[] *= 2, .[] -= 2, .[] /= 2, .[] %=2
        input:    [1,3,5]
        expected: ['[3,5,7]', '[2,6,10]', '[-1,1,3]', '[0.5, 1.5, 2.5]', '[1,1,1]']
        actual:   (no output)
        stderr:   invalid update path
    FAIL jq.test:1245  output mismatch
        program:  .foo += .foo
        input:    {"foo":2}
        expected: ['{"foo":4}']
        actual:   (no output)
        stderr:   cannot index
    FAIL jq.test:1249  output mismatch
        program:  .[0].a |= {"old":., "new":(.+1)}
        input:    [{"a":1,"b":2}]
        expected: ['[{"a":{"old":1, "new":2},"b":2}]']
        actual:   (no output)
        stderr:   invalid update path
    FAIL jq.test:1258  output mismatch
        program:  .[] | try (getpath(["a",0,"b"]) |= 5) catch .
        input:    [null,{"b":0},{"a":0},{"a":null},{"a":[0,1]},{"a":{"b":1}},{"a":[{}]},{"a":[{"c":3}]}]
        expected: ['{"a":[{"b":5}]}', '{"b":0,"a":[{"b":5}]}', '"Cannot index number with number (0)"', '{"a":[{"b":5}]}', '"Cannot index number with string (\\"b\\")"', '"Cannot index object with number (0)"', '{"a":[{"b":5}]}', '{"a":[{"c":3,"b":5}]}']
        actual:   ['"invalid update path"', '"invalid update path"', '"invalid update path"', '"invalid update path"', '"invalid update path"', '"invalid update path"', '"invalid update path"', '"invalid update path"']
    FAIL jq.test:1270  output mismatch
        program:  (.[] | select(. >= 2)) |= empty
        input:    [1,5,3,0,7]
        expected: ['[1,0]']
        actual:   (no output)
        stderr:   invalid update path
    FAIL jq.test:1274  output mismatch
        program:  .[] |= select(. % 2 == 0)
        input:    [0,1,2,3,4,5]
        expected: ['[0,2,4]']
        actual:   (no output)
        stderr:   unknown function select
    FAIL jq.test:1278  output mismatch
        program:  .foo[1,4,2,3] |= empty
        input:    {"foo":[0,1,2,3,4,5]}
        expected: ['{"foo":[0,5]}']
        actual:   ['{"foo":[0,1,2,3,4,5]}']
    FAIL jq.test:1282  output mismatch
        program:  .[2][3] = 1
        input:    [4]
        expected: ['[4, null, [null, null, null, 1]]']
        actual:   (no output)
        stderr:   list index out of range
    FAIL jq.test:1286  output mismatch
        program:  .foo[2].bar = 1
        input:    {"foo":[11], "bar":42}
        expected: ['{"foo":[11,null,{"bar":1}], "bar":42}']
        actual:   (no output)
        stderr:   cannot index
    FAIL jq.test:1290  output mismatch
        program:  try ((map(select(.a == 1))[].b) = 10) catch .
        input:    [{"a":0},{"a":1}]
        expected: ['"Invalid path expression near attempt to iterate through [{\\"a\\":1}]"']
        actual:   ['"unknown function select"']
    FAIL jq.test:1294  output mismatch
        program:  try ((map(select(.a == 1))[].a) |= .+1) catch .
        input:    [{"a":0},{"a":1}]
        expected: ['"Invalid path expression near attempt to iterate through [{\\"a\\":1}]"']
        actual:   ['"unknown function select"']
    FAIL jq.test:1306  output mismatch
        program:  .[] = 1
        input:    [1,null,Infinity,-Infinity,NaN,-NaN]
        expected: ['[1,1,1,1,1,1]']
        actual:   (no output)
        stderr:   Expecting value: line 1 column 32 (char 31)
    FAIL jq.test:1318  program did not compile: expected end at position 40
        program:  [.[] | if .baz then "strange" elif .foo then "yep" else "nope" end]
        input:    [{"foo":0},{"foo":1},{"foo":[]},{"foo":true},{"foo":false},{"foo":null},{"foo":"foo"},{}]
        expected: ['["yep","yep","yep","yep","nope","nope","yep","nope"]']
        actual:   (no output)
        stderr:   expected end at position 40
    FAIL jq.test:1342  output mismatch
        program:  [if false then 3 end]
        input:    7
        expected: ['[7]']
        actual:   ['[null]']
    FAIL jq.test:1350  program did not compile: expected end at position 28
        program:  [if false then 3 elif false then 4 end]
        input:    7
        expected: ['[7]']
        actual:   (no output)
        stderr:   expected end at position 28
    FAIL jq.test:1354  program did not compile: expected end at position 28
        program:  [if false then 3 elif false then 4 else . end]
        input:    7
        expected: ['[7]']
        actual:   (no output)
        stderr:   expected end at position 28
    FAIL jq.test:1370  output mismatch
        program:  [.[] | [.foo[] // .bar]]
        input:    [{"foo":[1,2], "bar": 42}, {"foo":[1], "bar": null}, {"foo":[null,false,3], "bar": 18}, {"foo":[], "bar":42}, {"foo": [null,false,null], "bar": 41}]
        expected: ['[[1,2], [1], [3], [42], [41]]']
        actual:   ['[[1,2],[1],[18,18,3],[],[41,41,41]]']
    FAIL jq.test:1374  output mismatch
        program:  .[] //= .[0]
        input:    ["hello",true,false,[false],null]
        expected: ['["hello",true,"hello",[false],"hello"]']
        actual:   (no output)
        stderr:   cannot index
    FAIL jq.test:1448  program did not compile: expected end at position 44
        program:  [.[]|try if . == 0 then error("foo") elif . == 1 then .a elif . == 2 then empty else . end catch .]
        input:    [0,1,2,3]
        expected: ['["foo","Cannot index number with string (\\"a\\")",3]']
        actual:   (no output)
        stderr:   expected end at position 44
    FAIL jq.test:1452  output mismatch
        program:  [.[]|(.a, .a)?]
        input:    [null,true,{"a":1}]
        expected: ['[null,null,1,1]']
        actual:   ['[1,1]']
    FAIL jq.test:1464  output mismatch
        program:  try error(0) // 1
        input:    null
        expected: ['1']
        actual:   (no output)
    FAIL jq.test:1473  output mismatch
        program:  1 + try 2 catch 3 + 4
        input:    null
        expected: ['7']
        actual:   ['3']
    FAIL jq.test:1481  output mismatch
        program:  try -.? catch .
        input:    "foo"
        expected: ['"string (\\"foo\\") cannot be negated"']
        actual:   ['"number required"']
    FAIL jq.test:1485  program did not compile: unknown filter at position 33
        program:  {x: try 1, y: try error catch 2, z: if true then 3 end}
        input:    null
        expected: ['{"x":1,"y":2,"z":3}']
        actual:   (no output)
        stderr:   unknown filter at position 33
    FAIL jq.test:1493  output mismatch
        program:  .[] | try error catch .
        input:    [1,null,2]
        expected: ['1', 'null', '2']
        actual:   ['"error"', '"error"', '"error"']
    FAIL jq.test:1499  output mismatch
        program:  try error("\($__loc__)") catch .
        input:    null
        expected: ['"{\\"file\\":\\"<top-level>\\",\\"line\\":1}"']
        actual:   (no output)
        stderr:   variable is not defined at position 0
    FAIL jq.test:1512  output mismatch
        program:  [.[] | split(", ")]
        input:    ["a,b, c, d, e,f",", a,b, c, d, e,f, "]
        expected: ['[["a,b","c","d","e,f"],["","a,b","c","d","e,f",""]]']
        actual:   (no output)
        stderr:   list index out of range
    FAIL jq.test:1516  output mismatch
        program:  split("")
        input:    "abc"
        expected: ['["a","b","c"]']
        actual:   (no output)
        stderr:   list index out of range
    FAIL jq.test:1528  output mismatch
        program:  [.[]|trimstr("foo")]
        input:    ["fo", "foo", "barfoo", "foobarfoo", "foob"]
        expected: ['["fo","","bar","bar","b"]']
        actual:   ['["fo","","bar","barfoo","b"]']
    FAIL jq.test:1544  program did not compile: unknown function index/1
        program:  [(index(","), rindex(",")), indices(",")]
        input:    "a,bc,def,ghij,klmno"
        expected: ['[1,13,[1,4,8,13]]']
        actual:   (no output)
        stderr:   unknown function index/1
    FAIL jq.test:1548  program did not compile: unknown function index/1
        program:  [ index("aba"), rindex("aba"), indices("aba") ]
        input:    "xababababax"
        expected: ['[1,7,[1,3,5,7]]']
        actual:   (no output)
        stderr:   unknown function index/1
    FAIL jq.test:1553  program did not compile: unknown function _strindices/1
        program:  try _strindices("abc") catch .
        input:    123
        expected: ['"number (123) cannot be searched, as it is not a string"']
        actual:   (no output)
        stderr:   unknown function _strindices/1
    FAIL jq.test:1557  program did not compile: unknown function _strindices/1
        program:  try _strindices(123) catch .
        input:    "abc"
        expected: ['"number (123) is not a string"']
        actual:   (no output)
        stderr:   unknown function _strindices/1
    FAIL jq.test:1563  program did not compile: unknown filter at position 4
        program:  map(trim), map(ltrim), map(rtrim)
        input:    [" \n\t\r\f\u000b", "","  ", "a", " a ", "abc", "  abc  ", "  abc", "abc  "]
        expected: ['["", "", "", "a", "a", "abc", "abc", "abc", "abc"]', '["", "", "", "a", "a ", "abc", "abc  ", "abc", "abc  "]', '["", "", "", "a", " a", "abc", "  abc", "  abc", "abc"]']
        actual:   (no output)
        stderr:   unknown filter at position 4
    FAIL jq.test:1569  program did not compile: unknown filter at position 0
        program:  trim, ltrim, rtrim
        input:    "\u0009\u000A\u000B\u000C\u000D\u0020\u0085\u00A0\u1680\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200A\u2028\u2029\u202F\u205F\u3000abc\u0009\u000A\u000B\u000C\u000D\u0020\u0085\u00A0\u1680\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200A\u2028\u2029\u202F\u205F\u3000"
        expected: ['"abc"', '"abc\\u0009\\u000A\\u000B\\u000C\\u000D\\u0020\\u0085\\u00A0\\u1680\\u2000\\u2001\\u2002\\u2003\\u2004\\u2005\\u2006\\u2007\\u2008\\u2009\\u200A\\u2028\\u2029\\u202F\\u205F\\u3000"', '"\\u0009\\u000A\\u000B\\u000C\\u000D\\u0020\\u0085\\u00A0\\u1680\\u2000\\u2001\\u2002\\u2003\\u2004\\u2005\\u2006\\u2007\\u2008\\u2009\\u200A\\u2028\\u2029\\u202F\\u205F\\u3000abc"']
        actual:   (no output)
        stderr:   unknown filter at position 0
    FAIL jq.test:1575  program did not compile: unknown filter at position 4
        program:  try trim catch ., try ltrim catch ., try rtrim catch .
        input:    123
        expected: ['"trim input must be a string"', '"trim input must be a string"', '"trim input must be a string"']
        actual:   (no output)
        stderr:   unknown filter at position 4
    FAIL jq.test:1581  program did not compile: unknown function indices/1
        program:  indices(1)
        input:    [0,1,1,2,3,4,1,5]
        expected: ['[1,2,6]']
        actual:   (no output)
        stderr:   unknown function indices/1
    FAIL jq.test:1585  program did not compile: unknown function indices/1
        program:  indices([1,2])
        input:    [0,1,2,3,1,4,2,5,1,2,6,7]
        expected: ['[1,8]']
        actual:   (no output)
        stderr:   unknown function indices/1
    FAIL jq.test:1589  program did not compile: unknown function indices/1
        program:  indices([1,2])
        input:    [1]
        expected: ['[]']
        actual:   (no output)
        stderr:   unknown function indices/1
    FAIL jq.test:1593  program did not compile: unknown function indices/1
        program:  indices(", ")
        input:    "a,b, cd,e, fgh, ijkl"
        expected: ['[3,9,14]']
        actual:   (no output)
        stderr:   unknown function indices/1
    FAIL jq.test:1597  program did not compile: unknown function index/1
        program:  index("!")
        input:    "здравствуй мир!"
        expected: ['14']
        actual:   (no output)
        stderr:   unknown function index/1
    FAIL jq.test:1601  program did not compile: unknown function rindex/1
        program:  .[:rindex("x")]
        input:    "正xyz"
        expected: ['"正"']
        actual:   (no output)
        stderr:   unknown function rindex/1
    FAIL jq.test:1605  program did not compile: unknown function indices/1
        program:  indices("o")
        input:    "🇬🇧oo"
        expected: ['[2,3]']
        actual:   (no output)
        stderr:   unknown function indices/1
    FAIL jq.test:1609  program did not compile: unknown function indices/1
        program:  indices("o")
        input:    "ƒoo"
        expected: ['[1,2]']
        actual:   (no output)
        stderr:   unknown function indices/1
    FAIL jq.test:1613  output mismatch
        program:  [.[]|split(",")]
        input:    ["a, bc, def, ghij, jklmn, a,b, c,d, e,f", "a,b,c,d, e,f,g,h"]
        expected: ['[["a"," bc"," def"," ghij"," jklmn"," a","b"," c","d"," e","f"],["a","b","c","d"," e","f","g","h"]]']
        actual:   (no output)
        stderr:   list index out of range
    FAIL jq.test:1617  output mismatch
        program:  [.[]|split(", ")]
        input:    ["a, bc, def, ghij, jklmn, a,b, c,d, e,f", "a,b,c,d, e,f,g,h"]
        expected: ['[["a","bc","def","ghij","jklmn","a,b","c,d","e,f"],["a,b,c,d","e,f,g,h"]]']
        actual:   (no output)
        stderr:   list index out of range
    FAIL jq.test:1625  output mismatch
        program:  [.[] * "abc"]
        input:    [-1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 3.7, 10.0]
        expected: ['[null,null,"","","abc","abc","abcabcabc","abcabcabcabcabcabcabcabcabcabc"]']
        actual:   (no output)
        stderr:   can't multiply sequence by non-int of type 'float'
    FAIL jq.test:1629  output mismatch
        program:  [. * (nan,-nan)]
        input:    "abc"
        expected: ['[null,null]']
        actual:   (no output)
        stderr:   unknown function nan
    FAIL jq.test:1633  output mismatch
        program:  . * 100000 | [.[:10],.[-10:]]
        input:    "abc"
        expected: ['["abcabcabca","cabcabcabc"]']
        actual:   (no output)
        stderr:   'NoneType' object has no attribute 'kind'
    FAIL jq.test:1641  output mismatch
        program:  try (. * 1000000000) catch .
        input:    "abc"
        expected: ['"Repeat string result too long"']
        actual:   (no output)
        stderr:   runtime evaluation failed
    FAIL jq.test:1677  program did not compile: unknown function sort_by/1
        program:  (sort_by(.b) | sort_by(.a)), sort_by(.a, .b), sort_by(.b, .c), group_by(.b), group_by(.a + .b - .c == 2)
        input:    [{"a": 1, "b": 4, "c": 14}, {"a": 4, "b": 1, "c": 3}, {"a": 1, "b": 4, "c": 3}, {"a": 0, "b": 2, "c": 43}]
        expected: ['[{"a": 0, "b": 2, "c": 43}, {"a": 1, "b": 4, "c": 14}, {"a": 1, "b": 4, "c": 3}, {"a": 4, "b": 1, "c": 3}]', '[{"a": 0, "b": 2, "c": 43}, {"a": 1, "b": 4, "c": 14}, {"a": 1, "b": 4, "c": 3}, {"a": 4, "b": 1, "c": 3}]', '[{"a": 4, "b": 1, "c": 3}, {"a": 0, "b": 2, "c": 43}, {"a": 1, "b": 4, "c": 3}, {"a": 1, "b": 4, "c": 14}]', '[[{"a": 4, "b": 1, "c": 3}], [{"a": 0, "b": 2, "c": 43}], [{"a": 1, "b": 4, "c": 14}, {"a": 1, "b": 4, "c": 3}]]', '[[{"a": 1, "b": 4, "c": 14}, {"a": 0, "b": 2, "c": 43}], [{"a": 4, "b": 1, "c": 3}, {"a": 1, "b": 4, "c": 3}]]']
        actual:   (no output)
        stderr:   unknown function sort_by/1
    FAIL jq.test:1693  program did not compile: unknown function min_by/1
        program:  [min, max, min_by(.[1]), max_by(.[1]), min_by(.[2]), max_by(.[2])]
        input:    [[4,2,"a"],[3,1,"a"],[2,4,"a"],[1,3,"a"]]
        expected: ['[[1,3,"a"],[4,2,"a"],[3,1,"a"],[2,4,"a"],[4,2,"a"],[1,3,"a"]]']
        actual:   (no output)
        stderr:   unknown function min_by/1
    FAIL jq.test:1697  program did not compile: unknown function min_by/1
        program:  [min,max,min_by(.),max_by(.)]
        input:    []
        expected: ['[null,null,null,null]']
        actual:   (no output)
        stderr:   unknown function min_by/1
    FAIL jq.test:1701  output mismatch
        program:  .foo[.baz]
        input:    {"foo":{"bar":4},"baz":"bar"}
        expected: ['4']
        actual:   (no output)
        stderr:   cannot index
    FAIL jq.test:1705  output mismatch
        program:  .[] | .error = "no, it's OK"
        input:    [{"error":true}]
        expected: ['{"error": "no, it\'s OK"}']
        actual:   (no output)
        stderr:   invalid update path
    FAIL jq.test:1709  output mismatch
        program:  [{a:1}] | .[] | .a=999
        input:    null
        expected: ['{"a": 999}']
        actual:   (no output)
        stderr:   invalid update path
    FAIL jq.test:1713  program did not compile: unknown filter at position 0
        program:  to_entries
        input:    {"a": 1, "b": 2}
        expected: ['[{"key":"a", "value":1}, {"key":"b", "value":2}]']
        actual:   (no output)
        stderr:   unknown filter at position 0
    FAIL jq.test:1717  program did not compile: unknown filter at position 0
        program:  from_entries
        input:    [{"key":"a", "value":1}, {"Key":"b", "Value":2}, {"name":"c", "value":3}, {"Name":"d", "Value":4}]
        expected: ['{"a": 1, "b": 2, "c": 3, "d": 4}']
        actual:   (no output)
        stderr:   unknown filter at position 0
    FAIL jq.test:1721  program did not compile: unknown function with_entries/1
        program:  with_entries(.key |= "KEY_" + .)
        input:    {"a": 1, "b": 2}
        expected: ['{"KEY_a": 1, "KEY_b": 2}']
        actual:   (no output)
        stderr:   unknown function with_entries/1
    FAIL jq.test:1725  program did not compile: unknown function has/1
        program:  map(has("foo"))
        input:    [{"foo": 42}, {}]
        expected: ['[true, false]']
        actual:   (no output)
        stderr:   unknown function has/1
    FAIL jq.test:1729  program did not compile: unknown function has/1
        program:  map(has(2))
        input:    [[0,1], ["a","b","c"]]
        expected: ['[false, true]']
        actual:   (no output)
        stderr:   unknown function has/1
    FAIL jq.test:1733  program did not compile: unknown function has/1
        program:  has(nan)
        input:    [0,1,2]
        expected: ['false']
        actual:   (no output)
        stderr:   unknown function has/1
    FAIL jq.test:1741  output mismatch
        program:  [][.]
        input:    1000000000000000000
        expected: ['null']
        actual:   (no output)
        stderr:   cannot index
    FAIL jq.test:1745  output mismatch
        program:  map([1,2][0:.])
        input:    [-1, 1, 2, 3, 1000000000000000000]
        expected: ['[[1], [1], [1,2], [1,2], [1,2]]']
        actual:   (no output)
        stderr:   slice indices must be integers or None or have an __index__ method
    FAIL jq.test:1799  output mismatch
        program:  flatten(0)
        input:    [0, [1], [[2]], [[[3]]]]
        expected: ['[0, [1], [[2]], [[[3]]]]']
        actual:   (no output)
        stderr:   'int' object is not reversible
    FAIL jq.test:1803  output mismatch
        program:  flatten(2)
        input:    [0, [1], [[2]], [[[3]]]]
        expected: ['[0, 1, 2, [3]]']
        actual:   (no output)
        stderr:   'int' object is not reversible
    FAIL jq.test:1807  output mismatch
        program:  flatten(2)
        input:    [0, [1, [2]], [1, [[3], 2]]]
        expected: ['[0, 1, 2, 1, [3], 2]']
        actual:   (no output)
        stderr:   'int' object is not reversible
    FAIL jq.test:1811  output mismatch
        program:  try flatten(-1) catch .
        input:    [0, [1], [[2]], [[[3]]]]
        expected: ['"flatten depth must not be negative"']
        actual:   (no output)
        stderr:   'float' object is not reversible
    FAIL jq.test:1815  program did not compile: unknown filter at position 0
        program:  transpose
        input:    [[1], [2,3]]
        expected: ['[[1,2],[null,3]]']
        actual:   (no output)
        stderr:   unknown filter at position 0
    FAIL jq.test:1819  program did not compile: unknown filter at position 0
        program:  transpose
        input:    []
        expected: ['[]']
        actual:   (no output)
        stderr:   unknown filter at position 0
    FAIL jq.test:1823  program did not compile: unknown filter at position 0
        program:  ascii_upcase
        input:    "useful but not for é"
        expected: ['"USEFUL BUT NOT FOR é"']
        actual:   (no output)
        stderr:   unknown filter at position 0
    FAIL jq.test:1827  program did not compile: unknown function bsearch/1
        program:  bsearch(0,1,2,3,4)
        input:    [1,2,3]
        expected: ['-1', '0', '1', '2', '-4']
        actual:   (no output)
        stderr:   unknown function bsearch/1
    FAIL jq.test:1835  program did not compile: unknown function bsearch/1
        program:  bsearch({x:1})
        input:    [{ "x": 0 },{ "x": 1 },{ "x": 2 }]
        expected: ['1']
        actual:   (no output)
        stderr:   unknown function bsearch/1
    FAIL jq.test:1839  program did not compile: unknown function bsearch/1
        program:  try ["OK", bsearch(0)] catch ["KO",.]
        input:    "aa"
        expected: ['["KO","string (\\"aa\\") cannot be searched from"]']
        actual:   (no output)
        stderr:   unknown function bsearch/1
    FAIL jq.test:1843  program did not compile: unknown function strftime/1
        program:  strftime("%Y-%m-%dT%H:%M:%SZ")
        input:    [2015,2,5,23,51,47,4,63]
        expected: ['"2015-03-05T23:51:47Z"']
        actual:   (no output)
        stderr:   unknown function strftime/1
    FAIL jq.test:1847  program did not compile: unknown function strftime/1
        program:  strftime("%A, %B %d, %Y")
        input:    1435677542.822351
        expected: ['"Tuesday, June 30, 2015"']
        actual:   (no output)
        stderr:   unknown function strftime/1
    FAIL jq.test:1851  program did not compile: unknown function strftime/1
        program:  strftime("%Y-%m-%dT%H:%M:%SZ")
        input:    [2024,2,15]
        expected: ['"2024-03-15T00:00:00Z"']
        actual:   (no output)
        stderr:   unknown function strftime/1
    FAIL jq.test:1855  program did not compile: unknown filter at position 0
        program:  mktime
        input:    [2024,8,21]
        expected: ['1726876800']
        actual:   (no output)
        stderr:   unknown filter at position 0
    FAIL jq.test:1859  program did not compile: unknown filter at position 0
        program:  gmtime
        input:    1425599507
        expected: ['[2015,2,5,23,51,47,4,63]']
        actual:   (no output)
        stderr:   unknown filter at position 0
    FAIL jq.test:1863  program did not compile: unknown filter at position 0
        program:  gmtime[5]
        input:    1425599507.25
        expected: ['47.25']
        actual:   (no output)
        stderr:   unknown filter at position 0
    FAIL jq.test:1868  program did not compile: unknown function strftime/1
        program:  try strftime("%Y-%m-%dT%H:%M:%SZ") catch .
        input:    ["a",1,2,3,4,5,6,7]
        expected: ['"strftime/1 requires parsed datetime inputs"']
        actual:   (no output)
        stderr:   unknown function strftime/1
    FAIL jq.test:1872  program did not compile: unknown function strflocaltime/1
        program:  try strflocaltime("%Y-%m-%dT%H:%M:%SZ") catch .
        input:    ["a",1,2,3,4,5,6,7]
        expected: ['"strflocaltime/1 requires parsed datetime inputs"']
        actual:   (no output)
        stderr:   unknown function strflocaltime/1
    FAIL jq.test:1876  program did not compile: unknown filter at position 4
        program:  try mktime catch .
        input:    ["a",1,2,3,4,5,6,7]
        expected: ['"mktime requires parsed datetime inputs"']
        actual:   (no output)
        stderr:   unknown filter at position 4
    FAIL jq.test:1881  program did not compile: unknown function strftime/1
        program:  try ["OK", strftime([])] catch ["KO", .]
        input:    0
        expected: ['["KO","strftime/1 requires a string format"]']
        actual:   (no output)
        stderr:   unknown function strftime/1
    FAIL jq.test:1885  program did not compile: unknown function strflocaltime/1
        program:  try ["OK", strflocaltime({})] catch ["KO", .]
        input:    0
        expected: ['["KO","strflocaltime/1 requires a string format"]']
        actual:   (no output)
        stderr:   unknown function strflocaltime/1
    FAIL jq.test:1889  program did not compile: unknown function strptime/1
        program:  [strptime("%Y-%m-%dT%H:%M:%SZ")|(.,mktime)]
        input:    "2015-03-05T23:51:47Z"
        expected: ['[[2015,2,5,23,51,47,4,63],1425599507]']
        actual:   (no output)
        stderr:   unknown function strptime/1
    FAIL jq.test:1895  program did not compile: unknown function strptime/1
        program:  last(range(365 * 67)|("1970-03-01T01:02:03Z"|strptime("%Y-%m-%dT%H:%M:%SZ")|mktime) + (86400 * .)|strftime("%Y-%m-%dT%H:%M:%SZ")|strptime("%Y-%m-%dT%H:%M:%SZ"))
        input:    null
        expected: ['[2037,1,11,1,2,3,3,41]']
        actual:   (no output)
        stderr:   unknown function strptime/1
    FAIL jq.test:1997  output mismatch
        program:  try -. catch .
        input:    "very-long-long-long-long-string"
        expected: ['"string (\\"very-long-long-long-long...\\") cannot be negated"']
        actual:   ['"number required"']
    FAIL jq.test:2001  output mismatch
        program:  try (.-.) catch .
        input:    "very-long-long-long-long-string"
        expected: ['"string (\\"very-long-long-long-long...\\") and string (\\"very-long-long-long-long...\\") cannot be subtracted"']
        actual:   ['[]']
    FAIL jq.test:2005  output mismatch
        program:  "x" * range(0; 12; 2) + "☆" * 8 | try -. catch .
        input:    null
        expected: ['"string (\\"☆☆☆☆☆☆☆☆\\") cannot be negated"', '"string (\\"xx☆☆☆☆☆☆☆☆\\") cannot be negated"', '"string (\\"xxxx☆☆☆☆☆☆...\\") cannot be negated"', '"string (\\"xxxxxx☆☆☆☆☆☆...\\") cannot be negated"', '"string (\\"xxxxxxxx☆☆☆☆☆...\\") cannot be negated"', '"string (\\"xxxxxxxxxx☆☆☆☆...\\") cannot be negated"']
        actual:   ['"number required"', '"number required"', '"number required"', '"number required"', '"number required"', '"number required"']
    FAIL jq.test:2014  program did not compile: unknown filter at position 28
        program:  try (. + "x") catch . == if have_decnum then "number (12345678901234567890123456...) and string (\"x\") cannot be added" else "number (12345678901234568000000000...) and string (\"x\") cannot be added" end
        input:    123456789012345678901234567890
        expected: ['true']
        actual:   (no output)
        stderr:   unknown filter at position 28
    FAIL jq.test:2034  output mismatch
        program:  try join(",") catch .
        input:    ["1","2",{"a":{"b":{"c":33}}}]
        expected: ['"string (\\"1,2,\\") and object ({\\"a\\":{\\"b\\":{\\"c\\":33}}}) cannot be added"']
        actual:   ['"1,2,{\'a\': {\'b\': {\'c\': 33}}}"']
    FAIL jq.test:2038  output mismatch
        program:  try join(",") catch .
        input:    ["1","2",[3,4,5]]
        expected: ['"string (\\"1,2,\\") and array ([3,4,5]) cannot be added"']
        actual:   ['"1,2,[3, 4, 5]"']
    FAIL jq.test:2046  output mismatch
        program:  try (1/.) catch .
        input:    0
        expected: ['"number (1) and number (0) cannot be divided because the divisor is zero"']
        actual:   (no output)
        stderr:   float division by zero
    FAIL jq.test:2050  output mismatch
        program:  try (1/0) catch .
        input:    0
        expected: ['"number (1) and number (0) cannot be divided because the divisor is zero"']
        actual:   (no output)
        stderr:   float division by zero
    FAIL jq.test:2054  output mismatch
        program:  try (0/0) catch .
        input:    0
        expected: ['"number (0) and number (0) cannot be divided because the divisor is zero"']
        actual:   (no output)
        stderr:   float division by zero
    FAIL jq.test:2058  output mismatch
        program:  try (1%.) catch .
        input:    0
        expected: ['"number (1) and number (0) cannot be divided (remainder) because the divisor is zero"']
        actual:   (no output)
        stderr:   math domain error
    FAIL jq.test:2062  output mismatch
        program:  try (1%0) catch .
        input:    0
        expected: ['"number (1) and number (0) cannot be divided (remainder) because the divisor is zero"']
        actual:   (no output)
        stderr:   math domain error
    FAIL jq.test:2086  output mismatch
        program:  (.[{}] = 0)?
        input:    null
        expected: (no output)
        actual:   ['null']
    FAIL jq.test:2089  program did not compile: unknown function INDEX/2
        program:  INDEX(range(5)|[., "foo\(.)"]; .[0])
        input:    null
        expected: ['{"0":[0,"foo0"],"1":[1,"foo1"],"2":[2,"foo2"],"3":[3,"foo3"],"4":[4,"foo4"]}']
        actual:   (no output)
        stderr:   unknown function INDEX/2
    FAIL jq.test:2093  program did not compile: unknown function JOIN/2
        program:  JOIN({"0":[0,"abc"],"1":[1,"bcd"],"2":[2,"def"],"3":[3,"efg"],"4":[4,"fgh"]}; .[0]|tostring)
        input:    [[5,"foo"],[3,"bar"],[1,"foobar"]]
        expected: ['[[[5,"foo"],null],[[3,"bar"],[3,"efg"]],[[1,"foobar"],[1,"bcd"]]]']
        actual:   (no output)
        stderr:   unknown function JOIN/2
    FAIL jq.test:2097  program did not compile: unknown function IN/1
        program:  range(5;10)|IN(range(10))
        input:    null
        expected: ['true', 'true', 'true', 'true', 'true']
        actual:   (no output)
        stderr:   unknown function IN/1
    FAIL jq.test:2105  program did not compile: unknown function IN/1
        program:  range(5;13)|IN(range(0;10;3))
        input:    null
        expected: ['false', 'true', 'false', 'false', 'true', 'false', 'false', 'false']
        actual:   (no output)
        stderr:   unknown function IN/1
    FAIL jq.test:2116  program did not compile: unknown function IN/1
        program:  range(10;12)|IN(range(10))
        input:    null
        expected: ['false', 'false']
        actual:   (no output)
        stderr:   unknown function IN/1
    FAIL jq.test:2121  program did not compile: unknown function IN/2
        program:  IN(range(10;20); range(10))
        input:    null
        expected: ['false']
        actual:   (no output)
        stderr:   unknown function IN/2
    FAIL jq.test:2125  program did not compile: unknown function IN/2
        program:  IN(range(5;20); range(10))
        input:    null
        expected: ['true']
        actual:   (no output)
        stderr:   unknown function IN/2
    FAIL jq.test:2135  program did not compile: expected filter at position 1
        program:  (.. | select(type == "object" and has("b") and (.b | type) == "array")|.b) |= .[0]
        input:    {"a": {"b": [1, {"b": 3}]}}
        expected: ['{"a": {"b": 1}}']
        actual:   (no output)
        stderr:   expected filter at position 1
    FAIL jq.test:2139  program did not compile: unknown function isempty/1
        program:  isempty(empty)
        input:    null
        expected: ['true']
        actual:   (no output)
        stderr:   unknown function isempty/1
    FAIL jq.test:2143  program did not compile: unknown function isempty/1
        program:  isempty(range(3))
        input:    null
        expected: ['false']
        actual:   (no output)
        stderr:   unknown function isempty/1
    FAIL jq.test:2147  program did not compile: unknown function isempty/1
        program:  isempty(1,error("foo"))
        input:    null
        expected: ['false']
        actual:   (no output)
        stderr:   unknown function isempty/1
    FAIL jq.test:2152  program did not compile: unknown function index/1
        program:  index("")
        input:    ""
        expected: ['null']
        actual:   (no output)
        stderr:   unknown function index/1
    FAIL jq.test:2157  program did not compile: unknown filter at position 0
        program:  builtins|length > 10
        input:    null
        expected: ['true']
        actual:   (no output)
        stderr:   unknown filter at position 0
    FAIL jq.test:2161  program did not compile: unknown filter at position 8
        program:  "-1"|IN(builtins[] / "/"|.[1])
        input:    null
        expected: ['false']
        actual:   (no output)
        stderr:   unknown filter at position 8
    FAIL jq.test:2165  program did not compile: unknown filter at position 4
        program:  all(builtins[] / "/"; .[1]|tonumber >= 0)
        input:    null
        expected: ['true']
        actual:   (no output)
        stderr:   unknown filter at position 4
    FAIL jq.test:2169  program did not compile: unknown filter at position 0
        program:  builtins|any(.[:1] == "_")
        input:    null
        expected: ['false']
        actual:   (no output)
        stderr:   unknown filter at position 0
    FAIL jq.test:2196  program did not compile: unknown filter at position 26
        program:  .[0] | tostring | . == if have_decnum then "13911860366432393" else "13911860366432392" end
        input:    [13911860366432393]
        expected: ['true']
        actual:   (no output)
        stderr:   unknown filter at position 26
    FAIL jq.test:2200  program did not compile: unknown filter at position 22
        program:  .x | tojson | . == if have_decnum then "13911860366432393" else "13911860366432392" end
        input:    {"x":13911860366432393}
        expected: ['true']
        actual:   (no output)
        stderr:   unknown filter at position 22
    FAIL jq.test:2204  program did not compile: unknown filter at position 51
        program:  (13911860366432393 == 13911860366432392) | . == if have_decnum then false else true end
        input:    null
        expected: ['true']
        actual:   (no output)
        stderr:   unknown filter at position 51
    FAIL jq.test:2224  program did not compile: unknown filter at position 18
        program:  -. | tojson == if have_decnum then "-13911860366432393" else "-13911860366432392" end
        input:    13911860366432393
        expected: ['true']
        actual:   (no output)
        stderr:   unknown filter at position 18
    FAIL jq.test:2228  program did not compile: unknown filter at position 18
        program:  -. | tojson == if have_decnum then "0.12345678901234567890123456789" else "0.12345678901234568" end
        input:    -0.12345678901234567890123456789
        expected: ['true']
        actual:   (no output)
        stderr:   unknown filter at position 18
    FAIL jq.test:2232  program did not compile: unknown filter at position 34
        program:  [1E+1000,-1E+1000 | tojson] == if have_decnum then ["1E+1000","-1E+1000"] else ["1.7976931348623157e+308","-1.7976931348623157e+308"] end
        input:    null
        expected: ['true']
        actual:   (no output)
        stderr:   unknown filter at position 34
    FAIL jq.test:2236  output mismatch
        program:  . |= try . catch .
        input:    1
        expected: ['1']
        actual:   (no output)
        stderr:   unsupported operator
    FAIL jq.test:2250  output mismatch
        program:  abs
        input:    "abc"
        expected: ['"abc"']
        actual:   (no output)
        stderr:   number required
    FAIL jq.test:2258  program did not compile: unknown filter at position 4
        program:  map(fabs)
        input:    [-0, 0, -10, -1.1]
        expected: ['[0,0,10,1.1]']
        actual:   (no output)
        stderr:   unknown filter at position 4
    FAIL jq.test:2271  program did not compile: unknown filter at position 49
        program:  [1E+1000,-1E+1000 | abs | tojson] | unique == if have_decnum then ["1E+1000"] else ["1.7976931348623157e+308"] end
        input:    null
        expected: ['true']
        actual:   (no output)
        stderr:   unknown filter at position 49
    FAIL jq.test:2275  program did not compile: unknown filter at position 52
        program:  [1E+1000,-1E+1000 | length | tojson] | unique == if have_decnum then ["1E+1000"] else ["1.7976931348623157e+308"] end
        input:    null
        expected: ['true']
        actual:   (no output)
        stderr:   unknown filter at position 52
    FAIL jq.test:2285  output mismatch
        program:  [ label $if | range(10) | ., (select(. == 5) | break $if) ]
        input:    null
        expected: ['[0,1,2,3,4,5]']
        actual:   (no output)
        stderr:   unknown function select
    FAIL jq.test:2304  output mismatch
        program:  { a, $__loc__, c }
        input:    {"a":[1,2,3],"b":"foo","c":{"hi":"hey"}}
        expected: ['{"a":[1,2,3],"__loc__":{"file":"<top-level>","line":1},"c":{"hi":"hey"}}']
        actual:   (no output)
        stderr:   no such variable: $__loc__
    FAIL jq.test:2315  program did not compile: unknown filter at position 11
        program:  fromjson | isnan
        input:    "nan"
        expected: ['true']
        actual:   (no output)
        stderr:   unknown filter at position 11
    FAIL jq.test:2319  output mismatch
        program:  tojson | fromjson
        input:    {"a":nan}
        expected: ['{"a":null}']
        actual:   (no output)
        stderr:   Expecting value: line 1 column 6 (char 5)
    FAIL jq.test:2324  program did not compile: unknown filter at position 22
        program:  .[] | try (fromjson | isnan) catch .
        input:    ["NaN","-NaN","NaN1","NaN10","NaN100","NaN1000","NaN10000","NaN100000"]
        expected: ['true', 'true', '"Invalid numeric literal at EOF at line 1, column 4 (while parsing \'NaN1\')"', '"Invalid numeric literal at EOF at line 1, column 5 (while parsing \'NaN10\')"', '"Invalid numeric literal at EOF at line 1, column 6 (while parsing \'NaN100\')"', '"Invalid numeric literal at EOF at line 1, column 7 (while parsing \'NaN1000\')"', '"Invalid numeric literal at EOF at line 1, column 8 (while parsing \'NaN10000\')"', '"Invalid numeric literal at EOF at line 1, column 9 (while parsing \'NaN100000\')"']
        actual:   (no output)
        stderr:   unknown filter at position 22
    FAIL jq.test:2337  program did not compile: unknown filter at position 4
        program:  try input catch .
        input:    null
        expected: ['"break"']
        actual:   (no output)
        stderr:   unknown filter at position 4
    FAIL jq.test:2341  program did not compile: unknown filter at position 0
        program:  debug
        input:    1
        expected: ['1']
        actual:   (no output)
        stderr:   unknown filter at position 0
    FAIL jq.test:2354  output mismatch
        program:  try (["hi","ho"]|.[]|(try . catch (if .=="ho" then "BROKEN"|error else empty end)) | if .=="ho" then error else "\(.) there!" end) catch "caught outside \(.)"
        input:    null
        expected: ['"hi there!"', '"caught outside ho"']
        actual:   ['"hi there!"', '"caught outside error"']
    FAIL jq.test:2363  output mismatch
        program:  try (try error catch "inner catch \(.)") catch "outer catch \(.)"
        input:    "foo"
        expected: ['"inner catch foo"']
        actual:   ['"inner catch error"']
    FAIL jq.test:2367  output mismatch
        program:  try ((try error catch "inner catch \(.)")|error) catch "outer catch \(.)"
        input:    "foo"
        expected: ['"outer catch inner catch foo"']
        actual:   ['"outer catch error"']
    FAIL jq.test:2372  program did not compile: unknown function first/1
        program:  first(.?,.?)
        input:    null
        expected: ['null']
        actual:   (no output)
        stderr:   unknown function first/1
    FAIL jq.test:2377  output mismatch
        program:  {foo: "bar"} | .foo |= .?
        input:    null
        expected: ['{"foo": "bar"}']
        actual:   (no output)
        stderr:   invalid update path
    FAIL jq.test:2382  output mismatch
        program:  . |= try 2
        input:    1
        expected: ['2']
        actual:   (no output)
        stderr:   unsupported operator
    FAIL jq.test:2386  output mismatch
        program:  . |= try 2 catch 3
        input:    1
        expected: ['2']
        actual:   (no output)
        stderr:   unsupported operator
    FAIL jq.test:2390  output mismatch
        program:  .[] |= try tonumber
        input:    ["1", "2a", "3", " 4", "5 ", "6.7", ".89", "-876", "+5.43", 21]
        expected: ['[1, 3, 6.7, 0.89, -876, 5.43, 21]']
        actual:   (no output)
        stderr:   invalid literal for int() with base 10: '2a'
    FAIL jq.test:2403  program did not compile: unknown filter at position 0
        program:  implode|explode
        input:    [-1,0,1,2,3,1114111,1114112,55295,55296,57343,57344,1.1,1.9]
        expected: ['[65533,0,1,2,3,1114111,65533,55295,65533,65533,57344,1,1]']
        actual:   (no output)
        stderr:   unknown filter at position 0
    FAIL jq.test:2407  program did not compile: unknown filter at position 8
        program:  map(try implode catch .)
        input:    [123,["a"],[nan]]
        expected: ['["implode input must be an array","string (\\"a\\") can\'t be imploded, unicode codepoint needs to be numeric","number (null) can\'t be imploded, unicode codepoint needs to be numeric"]']
        actual:   (no output)
        stderr:   unknown filter at position 8
    FAIL jq.test:2411  program did not compile: unknown filter at position 6
        program:  try 0[implode] catch .
        input:    []
        expected: ['"Cannot index number with string (\\"\\")"']
        actual:   (no output)
        stderr:   unknown filter at position 6
    FAIL jq.test:2416  program did not compile: unknown function walk/1
        program:  walk(.)
        input:    {"x":0}
        expected: ['{"x":0}']
        actual:   (no output)
        stderr:   unknown function walk/1
    FAIL jq.test:2420  program did not compile: unknown function walk/1
        program:  walk(1)
        input:    {"x":0}
        expected: ['1']
        actual:   (no output)
        stderr:   unknown function walk/1
    FAIL jq.test:2425  program did not compile: unknown function walk/1
        program:  [walk(.,1)]
        input:    {"x":0}
        expected: ['[{"x":0},1]']
        actual:   (no output)
        stderr:   unknown function walk/1
    FAIL jq.test:2430  program did not compile: unknown function IN/1
        program:  walk(select(IN({}, []) | not))
        input:    {"a":1,"b":[]}
        expected: ['{"a":1}']
        actual:   (no output)
        stderr:   unknown function IN/1
    FAIL jq.test:2435  output mismatch
        program:  [range(10)] | .[1.2:3.5]
        input:    null
        expected: ['[1,2,3]']
        actual:   (no output)
        stderr:   slice indices must be integers or None or have an __index__ method
    FAIL jq.test:2439  output mismatch
        program:  [range(10)] | .[1.5:3.5]
        input:    null
        expected: ['[1,2,3]']
        actual:   (no output)
        stderr:   slice indices must be integers or None or have an __index__ method
    FAIL jq.test:2443  output mismatch
        program:  [range(10)] | .[1.7:3.5]
        input:    null
        expected: ['[1,2,3]']
        actual:   (no output)
        stderr:   slice indices must be integers or None or have an __index__ method
    FAIL jq.test:2447  output mismatch
        program:  [range(10)] | .[1.7:4294967295]
        input:    null
        expected: ['[1,2,3,4,5,6,7,8,9]']
        actual:   (no output)
        stderr:   slice indices must be integers or None or have an __index__ method
    FAIL jq.test:2451  output mismatch
        program:  [range(10)] | .[1.7:-4294967296]
        input:    null
        expected: ['[]']
        actual:   (no output)
        stderr:   slice indices must be integers or None or have an __index__ method
    FAIL jq.test:2455  output mismatch
        program:  [[range(10)] | .[1.1,1.5,1.7]]
        input:    null
        expected: ['[1,1,1]']
        actual:   (no output)
        stderr:   cannot index
    FAIL jq.test:2459  output mismatch
        program:  [range(5)] | .[1.1] = 5
        input:    null
        expected: ['[0,5,2,3,4]']
        actual:   (no output)
        stderr:   invalid update path
    FAIL jq.test:2463  output mismatch
        program:  [range(3)] | .[nan:1]
        input:    null
        expected: ['[0]']
        actual:   (no output)
        stderr:   unknown function nan
    FAIL jq.test:2467  output mismatch
        program:  [range(3)] | .[1:nan]
        input:    null
        expected: ['[1,2]']
        actual:   (no output)
        stderr:   unknown function nan
    FAIL jq.test:2471  output mismatch
        program:  [range(3)] | .[nan]
        input:    null
        expected: ['null']
        actual:   (no output)
        stderr:   unknown function nan
    FAIL jq.test:2475  output mismatch
        program:  try ([range(3)] | .[nan] = 9) catch .
        input:    null
        expected: ['"Cannot set array element at NaN index"']
        actual:   ['"invalid update path"']
    FAIL jq.test:2479  output mismatch
        program:  try ("foobar" | .[1.5:3.5] = "xyz") catch .
        input:    null
        expected: ['"Cannot update string slices"']
        actual:   ['"invalid update path"']
    FAIL jq.test:2483  output mismatch
        program:  try ([range(10)] | .[1.5:3.5] = ["xyz"]) catch .
        input:    null
        expected: ['[0,"xyz",4,5,6,7,8,9]']
        actual:   ['"invalid update path"']
    FAIL jq.test:2487  output mismatch
        program:  try ("foobar" | .[1.5]) catch .
        input:    null
        expected: ['"Cannot index string with number (1.5)"']
        actual:   ['"cannot index"']
    FAIL jq.test:2494  output mismatch
        program:  try ["ok", setpath([1]; 1)] catch ["ko", .]
        input:    {"hi":"hello"}
        expected: ['["ko","Cannot index object with number (1)"]']
        actual:   ['["ok",{"hi":"hello","1":1}]']
    FAIL jq.test:2498  output mismatch
        program:  try fromjson catch .
        input:    "{'a': 123}"
        expected: ['"Invalid string literal; expected \\", but got \' at line 1, column 5 (while parsing \'{\'a\': 123}\')"']
        actual:   ['"Expecting property name enclosed in double quotes: line 1 column 2 (char 1)"']
    FAIL jq.test:2504  output mismatch
        program:  try ltrimstr(1) catch "x", try rtrimstr(1) catch "x" | "ok"
        input:    "hi"
        expected: ['"ok"', '"ok"']
        actual:   (no output)
        stderr:   startswith first arg must be str or a tuple of str, not int
    FAIL jq.test:2509  output mismatch
        program:  try ltrimstr("x") catch "x", try rtrimstr("x") catch "x" | "ok"
        input:    {"hey":[]}
        expected: ['"ok"', '"ok"']
        actual:   (no output)
        stderr:   'dict' object has no attribute 'startswith'
    FAIL jq.test:2516  output mismatch
        program:  .[] as [$x, $y] | try ["ok", ($x | ltrimstr($y))] catch ["ko", .]
        input:    [["hi",1],[1,"hi"],["hi","hi"],[1,1]]
        expected: ['["ko","startswith() requires string inputs"]', '["ko","startswith() requires string inputs"]', '["ok",""]', '["ko","startswith() requires string inputs"]']
        actual:   (no output)
        stderr:   startswith first arg must be str or a tuple of str, not int
    FAIL jq.test:2523  output mismatch
        program:  .[] as [$x, $y] | try ["ok", ($x | rtrimstr($y))] catch ["ko", .]
        input:    [["hi",1],[1,"hi"],["hi","hi"],[1,1]]
        expected: ['["ko","endswith() requires string inputs"]', '["ko","endswith() requires string inputs"]', '["ok",""]', '["ko","endswith() requires string inputs"]']
        actual:   (no output)
        stderr:   endswith first arg must be str or a tuple of str, not int
    FAIL jq.test:2533  output mismatch
        program:  try ["OK", setpath([[1]]; 1)] catch ["KO", .]
        input:    []
        expected: ['["KO","Cannot update field at array index of array"]']
        actual:   (no output)
        stderr:   int() argument must be a string, a bytes-like object or a real number, not 'list'
    FAIL jq.test:2548  program did not compile: unknown function strflocaltime/1
        program:  strflocaltime("" | ., @uri)
        input:    0
        expected: ['""', '""']
        actual:   (no output)
        stderr:   unknown function strflocaltime/1
    FAIL jq.test:2573  output mismatch
        program:  setpath([range(10000) | 0]; 0) | flatten
        input:    null
        expected: ['[0]']
        actual:   (no output)
        stderr:   'NoneType' object is not reversible
    FAIL jq.test:2577  output mismatch
        program:  try setpath([range(10001) | 0]; 0) catch .
        input:    null
        expected: ['"Path too deep"']
        actual:   ['null']
    FAIL jq.test:2585  output mismatch
        program:  try getpath([range(10001) | 0]) catch .
        input:    null
        expected: ['"Path too deep"']
        actual:   ['null']
    FAIL jq.test:2593  output mismatch
        program:  try delpaths([[range(10001) | 0]]) catch .
        input:    null
        expected: ['"Path too deep"']
        actual:   ['null']
    jq conformance: 264 passed, 273 failed, 0 errored, 13 skipped (corpus jq.test @ jq-1.8.2)

## Build summary
<reusable-compact filename="full_test.sh">
Runs the supplied conformance harness from the application root via `python3 sources/run_conformance.py`; requires executable `./jq`.
</reusable-compact>

<reusable-compact filename="exclusions.txt">
Declares only module-loader corpus cases as skipped. Entries must match corpus program lines exactly; stale entries are harness errors.
</reusable-compact>

<reusable-compact filename="builtin.jq">
Reference jq builtin definitions covering generators, transformations, paths, assignments, strings, regexes, dates, streaming, and SQL-style helpers.
</reusable-compact>

RESULT: SUCCESS

FILES CHANGED:
- None; all required assets were already staged and preserved unchanged.

SUMMARY:
Verified all eight required `sources/` assets. The corpus listing acceptance passed, and the scoring script contract acceptance passed.

BLOCKERS:
- None
