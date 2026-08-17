# Evidence: Block 5 · Service (block-5)

- block type: block
- date: 2026-08-16
- resulting state: closed/failed
- story points (combined assembled cost): 59920
- execution id: 20260817.001857.069Z-aae6aa99

## Stories built
- Implement jq parsing, precedence, and executable AST construction. (frontend-parser) [story]

## Stacked context
- compass: COMPASS.md (SP 3821)
- implements: FEATURE-FRONTEND-PARSER.md (SP 697)
- context: parser.y (SP 5596)
- context: lexer.l (SP 1137)
- context: jq-manual.txt (SP 32696)
- context: jq.test (SP 13058)
- context: ARCHITECTURE_compact.md (SP 147)
- stack: common_compact.md (SP 1179)
- stack: python_compact.md (SP 1534)

## Build directory changes
- jq
- tests/test_parser.py

## Pre-build acceptance observation
- RED: parser-valid-programs (FEATURE-FRONTEND-PARSER.md)
  intent: The parser accepts representative valid jq programs and the conformance runner reports success for the parser-owned corpus slice.
  return code: 1
  stdout:
    FAIL jq.test:48  output mismatch
        program:  .
        input:    ﻿"byte order mark"
        expected: ['"byte order mark"']
        actual:   (no output)
        stderr:   runtime error: Unexpected UTF-8 BOM (decode using utf-8-sig): line 1 column 1 (char 0)
    FAIL jq.test:72  program did not compile: compile error: invalid token
        program:  @text,@json,([1,.]|@csv,@tsv),@html,(@uri|.,@urid),@sh,(@base64|.,@base64d)
        input:    "!()<>&'\"\t"
        expected: ['"!()<>&\'\\"\\t"', '"\\"!()<>&\'\\\\\\"\\\\t\\""', '"1,\\"!()<>&\'\\"\\"\\t\\""', '"1\\t!()<>&\'\\"\\\\t"', '"!()&lt;&gt;&amp;&apos;&quot;\\t"', '"%21%28%29%3C%3E%26%27%22%09"', '"!()<>&\'\\"\\t"', '"\'!()<>&\'\\\\\'\'\\"\\t\'"', '"ISgpPD4mJyIJ"', '"!()<>&\'\\"\\t"']
        actual:   (no output)
        stderr:   compile error: invalid token
    FAIL jq.test:86  program did not compile: compile error: invalid token
        program:  @base64
        input:    "foóbar\n"
        expected: ['"Zm/Ds2Jhcgo="']
        actual:   (no output)
        stderr:   compile error: invalid token
    FAIL jq.test:90  program did not compile: compile error: invalid token
        program:  @base64d
        input:    "Zm/Ds2Jhcgo="
        expected: ['"foóbar\\n"']
        actual:   (no output)
        stderr:   compile error: invalid token
    FAIL jq.test:94  program did not compile: compile error: invalid token
        program:  @uri
        input:    "\u03bc"
        expected: ['"%CE%BC"']
        actual:   (no output)
        stderr:   compile error: invalid token
    FAIL jq.test:98  program did not compile: compile error: invalid token
        program:  @urid
        input:    "%CE%BC"
        expected: ['"\\u03bc"']
        actual:   (no output)
        stderr:   compile error: invalid token
    FAIL jq.test:102  program did not compile: compile error: invalid token
        program:  @html "<b>\(.)</b>"
        input:    "<script>hax</script>"
        expected: ['"<b>&lt;script&gt;hax&lt;/script&gt;</b>"']
        actual:   (no output)
        stderr:   compile error: invalid token
    FAIL jq.test:148  program did not compile: compile error: unexpected foo
        program:  .foo
        input:    {"foo": 42, "bar": 43}
        expected: ['42']
        actual:   (no output)
        stderr:   compile error: unexpected foo
    FAIL jq.test:152  program did not compile: compile error: unexpected foo
        program:  .foo | .bar
        input:    {"foo": {"bar": 42}, "bar": "badvalue"}
        expected: ['42']
        actual:   (no output)
        stderr:   compile error: unexpected foo
    FAIL jq.test:156  program did not compile: compile error: unexpected foo
        program:  .foo.bar
        input:    {"foo": {"bar": 42}, "bar": "badvalue"}
        expected: ['42']
        actual:   (no output)
        stderr:   compile error: unexpected foo
    FAIL jq.test:160  program did not compile: compile error: unexpected foo_bar
        program:  .foo_bar
        input:    {"foo_bar": 2}
        expected: ['2']
        actual:   (no output)
        stderr:   compile error: unexpected foo_bar
    FAIL jq.test:168  program did not compile: compile error: unexpected "foo"
        program:  ."foo"."bar"
        input:    {"foo": {"bar": 20}}
        expected: ['20']
        actual:   (no output)
        stderr:   compile error: unexpected "foo"
    FAIL jq.test:172  program did not compile: compile error: unexpected e0
        program:  .e0, .E1, .E-1, .E+1
        input:    {"e0": 1, "E1": 2, "E": 3}
        expected: ['1', '2', '2', '4']
        actual:   (no output)
        stderr:   compile error: unexpected e0
    FAIL jq.test:179  program did not compile: compile error: expected ]
        program:  [.[]|.foo?]
        input:    [1,[2],{"foo":3,"bar":4},{},{"foo":5}]
        expected: ['[3,null,5]']
        actual:   (no output)
        stderr:   compile error: expected ]
    FAIL jq.test:183  program did not compile: compile error: expected ]
        program:  [.[]|.foo?.bar?]
        input:    [1,[2],[],{"foo":3},{"foo":{"bar":4}},{}]
        expected: ['[4,null]']
        actual:   (no output)
        stderr:   compile error: expected ]
    FAIL jq.test:187  program did not compile: compile error: unexpected ..
        program:  [..]
        input:    [1,[[2]],{ "a":[1]}]
        expected: ['[[1,[[2]],{"a":[1]}],1,[[2]],[2],2,{"a":[1]},[1],1]']
        actual:   (no output)
        stderr:   compile error: unexpected ..
    FAIL jq.test:195  output mismatch
        program:  [.[]|.[1:3]?]
        input:    [1,null,true,false,"abcdef",{},{"a":1,"b":2},[],[1,2,3,4,5],[1,2]]
        expected: ['[null,"bc",[],[2,3],[2]]']
        actual:   (no output)
        stderr:   runtime error: 'int' object is not subscriptable
    FAIL jq.test:205  output mismatch
        program:  try ["OK", (.[] | error)] catch ["KO", .]
        input:    {"a":["b"],"c":["d"]}
        expected: ['["KO",["b"]]']
        actual:   ['["KO","error"]']
    FAIL jq.test:213  program did not compile: compile error: expected )
        program:  try (.foo[-1] = 0) catch .
        input:    null
        expected: ['"Out of bounds negative array index"']
        actual:   (no output)
        stderr:   compile error: expected )
    FAIL jq.test:217  program did not compile: compile error: expected )
        program:  try (.foo[-2] = 0) catch .
        input:    null
        expected: ['"Out of bounds negative array index"']
        actual:   (no output)
        stderr:   compile error: expected )
    FAIL jq.test:221  program did not compile: compile error: unexpected =
        program:  .[-1] = 5
        input:    [0,1,2]
        expected: ['[0,1,5]']
        actual:   (no output)
        stderr:   compile error: unexpected =
    FAIL jq.test:225  program did not compile: compile error: unexpected =
        program:  .[-2] = 5
        input:    [0,1,2]
        expected: ['[0,5,2]']
        actual:   (no output)
        stderr:   compile error: unexpected =
    FAIL jq.test:229  program did not compile: compile error: expected )
        program:  try (.[999999999] = 0) catch .
        input:    null
        expected: ['"Array index too large"']
        actual:   (no output)
        stderr:   compile error: expected )
    FAIL jq.test:329  output mismatch
        program:  [.[]|[.,1]|until(.[0] < 1; [.[0] - 1, .[1] * .[0]])|.[1]]
        input:    [1,2,3,4,5]
        expected: ['[1,2,6,24,120]']
        actual:   (no output)
        stderr:   runtime error: unknown function until
    FAIL jq.test:373  output mismatch
        program:  try limit(-1; error) catch .
        input:    null
        expected: ['"limit doesn\'t support negative count"']
        actual:   ['"unknown function limit"']
    FAIL jq.test:389  output mismatch
        program:  try skip(-1; error) catch .
        input:    null
        expected: ['"skip doesn\'t support negative count"']
        actual:   ['"unknown function skip"']
    FAIL jq.test:466  program did not compile: compile error: unexpected :
        program:  [.[3:2], .[-5:4], .[:-2], .[-2:], .[3:3][1:], .[10:]]
        input:    [0,1,2,3,4,5,6]
        expected: ['[[], [2,3], [0,1,2,3,4], [5,6], [], []]']
        actual:   (no output)
        stderr:   compile error: unexpected :
    FAIL jq.test:470  program did not compile: compile error: unexpected :
        program:  [.[3:2], .[-5:4], .[:-2], .[-2:], .[3:3][1:], .[10:]]
        input:    "abcdefghi"
        expected: ['["","","abcdefg","hi","",""]']
        actual:   (no output)
        stderr:   compile error: unexpected :
    FAIL jq.test:478  program did not compile: compile error: unexpected =
        program:  .[2:4] = ([], ["a","b"], ["a","b","c"])
        input:    [0,1,2,3,4,5,6,7]
        expected: ['[0,1,4,5,6,7]', '[0,1,"a","b",4,5,6,7]', '[0,1,"a","b","c",4,5,6,7]']
        actual:   (no output)
        stderr:   compile error: unexpected =
    FAIL jq.test:490  program did not compile: compile error: unexpected range
        program:  reduce range(65540;65536;-1) as $i ([]; .[$i] = $i)|.[65536:]
        input:    null
        expected: ['[null,65537,65538,65539,65540]']
        actual:   (no output)
        stderr:   compile error: unexpected range
    FAIL jq.test:530  program did not compile: compile error: unexpected as
        program:  . as {as: $kw, "str": $str, ("e"+"x"+"p"): $exp} | [$kw, $str, $exp]
        input:    {"as": 1, "str": 2, "exp": 3}
        expected: ['[1, 2, 3]']
        actual:   (no output)
        stderr:   compile error: unexpected as
    FAIL jq.test:534  program did not compile: compile error: unexpected as
        program:  .[] as [$a, $b] | [$b, $a]
        input:    [[1], [1, 2, 3]]
        expected: ['[null, 1]', '[2, 1]']
        actual:   (no output)
        stderr:   compile error: unexpected as
    FAIL jq.test:539  program did not compile: compile error: unexpected as
        program:  . as $i | . as [$i] | $i
        input:    [0]
        expected: ['0']
        actual:   (no output)
        stderr:   compile error: unexpected as
    FAIL jq.test:543  program did not compile: compile error: unexpected as
        program:  . as [$i] | . as $i | $i
        input:    [0]
        expected: ['[0]']
        actual:   (no output)
        stderr:   compile error: unexpected as
    FAIL jq.test:609  program did not compile: compile error: unexpected a
        program:  .a+.b
        input:    {"a":42}
        expected: ['42']
        actual:   (no output)
        stderr:   compile error: unexpected a
    FAIL jq.test:709  output mismatch
        program:  .[] | try toboolean catch .
        input:    [null,0,"tru","truee","fals","falsee",[],{}]
        expected: ['"null (null) cannot be parsed as a boolean"', '"number (0) cannot be parsed as a boolean"', '"string (\\"tru\\") cannot be parsed as a boolean"', '"string (\\"truee\\") cannot be parsed as a boolean"', '"string (\\"fals\\") cannot be parsed as a boolean"', '"string (\\"falsee\\") cannot be parsed as a boolean"', '"array ([]) cannot be parsed as a boolean"', '"object ({}) cannot be parsed as a boolean"']
        actual:   ['"unknown function toboolean"', '"unknown function toboolean"', '"unknown function toboolean"', '"unknown function toboolean"', '"unknown function toboolean"', '"unknown function toboolean"', '"unknown function toboolean"', '"unknown function toboolean"']
    FAIL jq.test:745  output mismatch
        program:  [.[] | try utf8bytelength catch .]
        input:    [[], {}, [1,2], 55, true, false]
        expected: ['["array ([]) only strings have UTF-8 byte length","object ({}) only strings have UTF-8 byte length","array ([1,2]) only strings have UTF-8 byte length","number (55) only strings have UTF-8 byte length","boolean (true) only strings have UTF-8 byte length","boolean (false) only strings have UTF-8 byte length"]']
        actual:   (no output)
        stderr:   runtime error: 'list' object has no attribute 'encode'
    FAIL jq.test:771  program did not compile: compile error: unexpected sum
        program:  .sum = add(.arr[])
        input:    {"arr":[]}
        expected: ['{"arr":[],"sum":null}']
        actual:   (no output)
        stderr:   compile error: unexpected sum
    FAIL jq.test:784  program did not compile: compile error: unexpected f
        program:  def f: . + 1; def g: def g: . + 100; f | g | f; (f | g), g
        input:    3.0
        expected: ['106.0', '105.0']
        actual:   (no output)
        stderr:   compile error: unexpected f
    FAIL jq.test:789  program did not compile: compile error: unexpected f
        program:  def f: (1000,2000); f
        input:    123412345
        expected: ['1000', '2000']
        actual:   (no output)
        stderr:   compile error: unexpected f
    FAIL jq.test:794  program did not compile: compile error: unexpected f
        program:  def f(a;b;c;d;e;f): [a+1,b,c,d,e,f]; f(.[0];.[1];.[0];.[0];.[0];.[0])
        input:    [1,2]
        expected: ['[2,2,1,1,1,1]']
        actual:   (no output)
        stderr:   compile error: unexpected f
    FAIL jq.test:798  program did not compile: compile error: unexpected f
        program:  def f: 1; def g: f, def f: 2; def g: 3; f, def f: g; f, g; def f: 4; [f, def f: g; def g: 5; f, g]+[f,g]
        input:    null
        expected: ['[4,1,2,3,3,5,4,1,2,3,3]']
        actual:   (no output)
        stderr:   compile error: unexpected f
    FAIL jq.test:803  program did not compile: compile error: unexpected a
        program:  def a: 0; . | a
        input:    null
        expected: ['0']
        actual:   (no output)
        stderr:   compile error: unexpected a
    FAIL jq.test:808  program did not compile: compile error: unexpected f
        program:  def f(a;b;c;d;e;f;g;h;i;j): [j,i,h,g,f,e,d,c,b,a]; f(.[0];.[1];.[2];.[3];.[4];.[5];.[6];.[7];.[8];.[9])
        input:    [0,1,2,3,4,5,6,7,8,9]
        expected: ['[9,8,7,6,5,4,3,2,1,0]']
        actual:   (no output)
        stderr:   compile error: unexpected f
    FAIL jq.test:860  program did not compile: compile error: unexpected f
        program:  def f(x): x | x; f([.], . + [42])
        input:    [1,2,3]
        expected: ['[[[1,2,3]]]', '[[1,2,3],42]', '[[1,2,3,42]]', '[1,2,3,42,42]']
        actual:   (no output)
        stderr:   compile error: unexpected f
    FAIL jq.test:868  program did not compile: compile error: unexpected f
        program:  def f: .+1; def g: f; def f: .+100; def f(a):a+.+11; [(g|f(20)), f]
        input:    1
        expected: ['[33,101]']
        actual:   (no output)
        stderr:   compile error: unexpected f
    FAIL jq.test:873  program did not compile: compile error: unexpected id
        program:  def id(x):x; 2000 as $x | def f(x):1 as $x | id([$x, x, x]); def g(x): 100 as $x | f($x,$x+x); g($x)
        input:    "more testing"
        expected: ['[1,100,2100.0,100,2100.0]']
        actual:   (no output)
        stderr:   compile error: unexpected id
    FAIL jq.test:878  program did not compile: compile error: unexpected x
        program:  def x(a;b): a as $a | b as $b | $a + $b; def y($a;$b): $a + $b; def check(a;b): [x(a;b)] == [y(a;b)]; check(.[];.[]*2)
        input:    [1,2,3]
        expected: ['true']
        actual:   (no output)
        stderr:   compile error: unexpected x
    FAIL jq.test:889  program did not compile: compile error: unexpected fac
        program:  def fac: if . == 1 then 1 else . * (. - 1 | fac) end; [.[] | fac]
        input:    [1,2,3,4]
        expected: ['[1,2,6,24]']
        actual:   (no output)
        stderr:   compile error: unexpected fac
    FAIL jq.test:899  program did not compile: compile error: unexpected .
        program:  reduce .[] as $x (0; . + $x)
        input:    [1,2,4]
        expected: ['7']
        actual:   (no output)
        stderr:   compile error: unexpected .
    FAIL jq.test:903  program did not compile: compile error: unexpected .
        program:  reduce .[] as [$i, {j:$j}] (0; . + $i - $j)
        input:    [[2,{"j":1}], [5,{"j":3}], [6,{"j":4}]]
        expected: ['5']
        actual:   (no output)
        stderr:   compile error: unexpected .
    FAIL jq.test:907  program did not compile: compile error: unexpected as
        program:  reduce [[1,2,10], [3,4,10]][] as [$i,$j] (0; . + $i * $j)
        input:    null
        expected: ['14']
        actual:   (no output)
        stderr:   compile error: unexpected as
    FAIL jq.test:919  program did not compile: compile error: unexpected .
        program:  reduce .[] as $x (0; . + $x) as $x | $x
        input:    [1,2,3]
        expected: ['6']
        actual:   (no output)
        stderr:   compile error: unexpected .
    FAIL jq.test:924  program did not compile: compile error: unexpected $n
        program:  reduce . as $n (.; .)
        input:    null
        expected: ['null']
        actual:   (no output)
        stderr:   compile error: unexpected $n
    FAIL jq.test:929  program did not compile: compile error: unexpected as
        program:  . as {$a, b: [$c, {$d}]} | [$a, $c, $d]
        input:    {"a":1, "b":[2,{"d":3}]}
        expected: ['[1,2,3]']
        actual:   (no output)
        stderr:   compile error: unexpected as
    FAIL jq.test:933  program did not compile: compile error: unexpected as
        program:  . as {$a, $b:[$c, $d]}| [$a, $b, $c, $d]
        input:    {"a":1, "b":[2,{"d":3}]}
        expected: ['[1,[2,{"d":3}],2,{"d":3}]']
        actual:   (no output)
        stderr:   compile error: unexpected as
    FAIL jq.test:938  program did not compile: compile error: unexpected as
        program:  .[] | . as {$a, b: [$c, {$d}]} ?// [$a, {$b}, $e] ?// $f | [$a, $b, $c, $d, $e, $f]
        input:    [{"a":1, "b":[2,{"d":3}]}, [4, {"b":5, "c":6}, 7, 8, 9], "foo"]
        expected: ['[1, null, 2, 3, null, null]', '[4, 5, null, null, 7, null]', '[null, null, null, null, null, "foo"]']
        actual:   (no output)
        stderr:   compile error: unexpected as
    FAIL jq.test:945  program did not compile: compile error: unexpected as
        program:  .[] | . as {a:$a} ?// {a:$a} ?// {a:$a} | $a
        input:    [[3],[4],[5],6]
        expected: (no output)
        actual:   (no output)
        stderr:   compile error: unexpected as
    FAIL jq.test:949  program did not compile: compile error: unexpected as
        program:  .[] as {a:$a} ?// {a:$a} ?// {a:$a} | $a
        input:    [[3],[4],[5],6]
        expected: (no output)
        actual:   (no output)
        stderr:   compile error: unexpected as
    FAIL jq.test:961  program did not compile: compile error: unexpected as
        program:  .[] | . as {a:$a} ?// {a:$a} ?// $a | $a
        input:    [[3],[4],[5],6]
        expected: ['[3]', '[4]', '[5]', '6']
        actual:   (no output)
        stderr:   compile error: unexpected as
    FAIL jq.test:968  program did not compile: compile error: unexpected as
        program:  .[] as {a:$a} ?// {a:$a} ?// $a | $a
        input:    [[3],[4],[5],6]
        expected: ['[3]', '[4]', '[5]', '6']
        actual:   (no output)
        stderr:   compile error: unexpected as
    FAIL jq.test:989  program did not compile: compile error: unexpected as
        program:  .[] | . as {a:$a} ?// $a ?// {a:$a} | $a
        input:    [[3],[4],[5],6]
        expected: ['[3]', '[4]', '[5]', '6']
        actual:   (no output)
        stderr:   compile error: unexpected as
    FAIL jq.test:996  program did not compile: compile error: unexpected as
        program:  .[] as {a:$a} ?// $a ?// {a:$a} | $a
        input:    [[3],[4],[5],6]
        expected: ['[3]', '[4]', '[5]', '6']
        actual:   (no output)
        stderr:   compile error: unexpected as
    FAIL jq.test:1017  program did not compile: compile error: unexpected as
        program:  .[] | . as $a ?// {a:$a} ?// {a:$a} | $a
        input:    [[3],[4],[5],6]
        expected: ['[3]', '[4]', '[5]', '6']
        actual:   (no output)
        stderr:   compile error: unexpected as
    FAIL jq.test:1024  program did not compile: compile error: unexpected as
        program:  .[] as $a ?// {a:$a} ?// {a:$a} | $a
        input:    [[3],[4],[5],6]
        expected: ['[3]', '[4]', '[5]', '6']
        actual:   (no output)
        stderr:   compile error: unexpected as
    FAIL jq.test:1045  program did not compile: compile error: unexpected as
        program:  . as $dot|any($dot[];not)
        input:    [1,2,3,4,true,false,1,2,3,4,5]
        expected: ['true']
        actual:   (no output)
        stderr:   compile error: unexpected as
    FAIL jq.test:1049  program did not compile: compile error: unexpected as
        program:  . as $dot|any($dot[];not)
        input:    [1,2,3,4,true]
        expected: ['false']
        actual:   (no output)
        stderr:   compile error: unexpected as
    FAIL jq.test:1053  program did not compile: compile error: unexpected as
        program:  . as $dot|all($dot[];.)
        input:    [1,2,3,4,true,false,1,2,3,4,5]
        expected: ['false']
        actual:   (no output)
        stderr:   compile error: unexpected as
    FAIL jq.test:1057  program did not compile: compile error: unexpected as
        program:  . as $dot|all($dot[];.)
        input:    [1,2,3,4,true]
        expected: ['true']
        actual:   (no output)
        stderr:   compile error: unexpected as
    FAIL jq.test:1123  program did not compile: compile error: expected )
        program:  try path(.a | map(select(.b == 0))) catch .
        input:    {"a":[{"b":0}]}
        expected: ['"Invalid path expression with result [{\\"b\\":0}]"']
        actual:   (no output)
        stderr:   compile error: expected )
    FAIL jq.test:1127  program did not compile: compile error: expected )
        program:  try path(.a | map(select(.b == 0)) | .[0]) catch .
        input:    {"a":[{"b":0}]}
        expected: ['"Invalid path expression near attempt to access element 0 of [{\\"b\\":0}]"']
        actual:   (no output)
        stderr:   compile error: expected )
    FAIL jq.test:1131  program did not compile: compile error: expected )
        program:  try path(.a | map(select(.b == 0)) | .c) catch .
        input:    {"a":[{"b":0}]}
        expected: ['"Invalid path expression near attempt to access element \\"c\\" of [{\\"b\\":0}]"']
        actual:   (no output)
        stderr:   compile error: expected )
    FAIL jq.test:1135  program did not compile: compile error: expected )
        program:  try path(.a | map(select(.b == 0)) | .[]) catch .
        input:    {"a":[{"b":0}]}
        expected: ['"Invalid path expression near attempt to iterate through [{\\"b\\":0}]"']
        actual:   (no output)
        stderr:   compile error: expected )
    FAIL jq.test:1173  output mismatch
        program:  try delpaths(0) catch .
        input:    {}
        expected: ['"Paths must be specified as an array"']
        actual:   ['"unknown function delpaths"']
    FAIL jq.test:1214  output mismatch
        program:  try pick(last) catch .
        input:    [1,2]
        expected: ['"Out of bounds negative array index"']
        actual:   ['"unknown function pick"']
    FAIL jq.test:1221  program did not compile: compile error: unexpected message
        program:  .message = "goodbye"
        input:    {"message": "hello"}
        expected: ['{"message": "goodbye"}']
        actual:   (no output)
        stderr:   compile error: unexpected message
    FAIL jq.test:1225  program did not compile: compile error: unexpected foo
        program:  .foo = .bar
        input:    {"bar":42}
        expected: ['{"foo":42, "bar":42}']
        actual:   (no output)
        stderr:   compile error: unexpected foo
    FAIL jq.test:1229  program did not compile: compile error: unexpected foo
        program:  .foo |= .+1
        input:    {"foo": 42}
        expected: ['{"foo": 43}']
        actual:   (no output)
        stderr:   compile error: unexpected foo
    FAIL jq.test:1233  program did not compile: compile error: unexpected =
        program:  .[] += 2, .[] *= 2, .[] -= 2, .[] /= 2, .[] %=2
        input:    [1,3,5]
        expected: ['[3,5,7]', '[2,6,10]', '[-1,1,3]', '[0.5, 1.5, 2.5]', '[1,1,1]']
        actual:   (no output)
        stderr:   compile error: unexpected =
    FAIL jq.test:1241  output mismatch
        program:  [.[] % 7]
        input:    [-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7]
        expected: ['[0,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,0]']
        actual:   ['[0,1,2,3,4,5,6,0,1,2,3,4,5,6,0]']
    FAIL jq.test:1245  program did not compile: compile error: unexpected foo
        program:  .foo += .foo
        input:    {"foo":2}
        expected: ['{"foo":4}']
        actual:   (no output)
        stderr:   compile error: unexpected foo
    FAIL jq.test:1249  program did not compile: compile error: unexpected |=
        program:  .[0].a |= {"old":., "new":(.+1)}
        input:    [{"a":1,"b":2}]
        expected: ['[{"a":{"old":1, "new":2},"b":2}]']
        actual:   (no output)
        stderr:   compile error: unexpected |=
    FAIL jq.test:1253  program did not compile: compile error: unexpected inc
        program:  def inc(x): x |= .+1; inc(.[].a)
        input:    [{"a":1,"b":2},{"a":2,"b":4},{"a":7,"b":8}]
        expected: ['[{"a":2,"b":2},{"a":3,"b":4},{"a":8,"b":8}]']
        actual:   (no output)
        stderr:   compile error: unexpected inc
    FAIL jq.test:1258  program did not compile: compile error: expected )
        program:  .[] | try (getpath(["a",0,"b"]) |= 5) catch .
        input:    [null,{"b":0},{"a":0},{"a":null},{"a":[0,1]},{"a":{"b":1}},{"a":[{}]},{"a":[{"c":3}]}]
        expected: ['{"a":[{"b":5}]}', '{"b":0,"a":[{"b":5}]}', '"Cannot index number with number (0)"', '{"a":[{"b":5}]}', '"Cannot index number with string (\\"b\\")"', '"Cannot index object with number (0)"', '{"a":[{"b":5}]}', '{"a":[{"c":3,"b":5}]}']
        actual:   (no output)
        stderr:   compile error: expected )
    FAIL jq.test:1274  program did not compile: compile error: unexpected |=
        program:  .[] |= select(. % 2 == 0)
        input:    [0,1,2,3,4,5]
        expected: ['[0,2,4]']
        actual:   (no output)
        stderr:   compile error: unexpected |=
    FAIL jq.test:1278  program did not compile: compile error: unexpected foo
        program:  .foo[1,4,2,3] |= empty
        input:    {"foo":[0,1,2,3,4,5]}
        expected: ['{"foo":[0,5]}']
        actual:   (no output)
        stderr:   compile error: unexpected foo
    FAIL jq.test:1282  program did not compile: compile error: unexpected =
        program:  .[2][3] = 1
        input:    [4]
        expected: ['[4, null, [null, null, null, 1]]']
        actual:   (no output)
        stderr:   compile error: unexpected =
    FAIL jq.test:1286  program did not compile: compile error: unexpected foo
        program:  .foo[2].bar = 1
        input:    {"foo":[11], "bar":42}
        expected: ['{"foo":[11,null,{"bar":1}], "bar":42}']
        actual:   (no output)
        stderr:   compile error: unexpected foo
    FAIL jq.test:1290  program did not compile: compile error: expected )
        program:  try ((map(select(.a == 1))[].b) = 10) catch .
        input:    [{"a":0},{"a":1}]
        expected: ['"Invalid path expression near attempt to iterate through [{\\"a\\":1}]"']
        actual:   (no output)
        stderr:   compile error: expected )
    FAIL jq.test:1294  program did not compile: compile error: expected )
        program:  try ((map(select(.a == 1))[].a) |= .+1) catch .
        input:    [{"a":0},{"a":1}]
        expected: ['"Invalid path expression near attempt to iterate through [{\\"a\\":1}]"']
        actual:   (no output)
        stderr:   compile error: expected )
    FAIL jq.test:1298  program did not compile: compile error: unexpected x
        program:  def x: .[1,2]; x=10
        input:    [0,1,2]
        expected: ['[0,10,10]']
        actual:   (no output)
        stderr:   compile error: unexpected x
    FAIL jq.test:1302  program did not compile: compile error: expected )
        program:  try (def x: reverse; x=10) catch .
        input:    [0,1,2]
        expected: ['"Invalid path expression with result [2,1,0]"']
        actual:   (no output)
        stderr:   compile error: expected )
    FAIL jq.test:1306  program did not compile: compile error: unexpected =
        program:  .[] = 1
        input:    [1,null,Infinity,-Infinity,NaN,-NaN]
        expected: ['[1,1,1,1,1,1]']
        actual:   (no output)
        stderr:   compile error: unexpected =
    FAIL jq.test:1314  program did not compile: compile error: expected then
        program:  [.[] | if .foo then "yep" else "nope" end]
        input:    [{"foo":0},{"foo":1},{"foo":[]},{"foo":true},{"foo":false},{"foo":null},{"foo":"foo"},{}]
        expected: ['["yep","yep","yep","yep","nope","nope","yep","nope"]']
        actual:   (no output)
        stderr:   compile error: expected then
    FAIL jq.test:1318  program did not compile: compile error: expected then
        program:  [.[] | if .baz then "strange" elif .foo then "yep" else "nope" end]
        input:    [{"foo":0},{"foo":1},{"foo":[]},{"foo":true},{"foo":false},{"foo":null},{"foo":"foo"},{}]
        expected: ['["yep","yep","yep","yep","nope","nope","yep","nope"]']
        actual:   (no output)
        stderr:   compile error: expected then
    FAIL jq.test:1370  program did not compile: compile error: expected ]
        program:  [.[] | [.foo[] // .bar]]
        input:    [{"foo":[1,2], "bar": 42}, {"foo":[1], "bar": null}, {"foo":[null,false,3], "bar": 18}, {"foo":[], "bar":42}, {"foo": [null,false,null], "bar": 41}]
        expected: ['[[1,2], [1], [3], [42], [41]]']
        actual:   (no output)
        stderr:   compile error: expected ]
    FAIL jq.test:1374  program did not compile: compile error: unexpected =
        program:  .[] //= .[0]
        input:    ["hello",true,false,[false],null]
        expected: ['["hello",true,"hello",[false],"hello"]']
        actual:   (no output)
        stderr:   compile error: unexpected =
    FAIL jq.test:1448  program did not compile: compile error: expected end
        program:  [.[]|try if . == 0 then error("foo") elif . == 1 then .a elif . == 2 then empty else . end catch .]
        input:    [0,1,2,3]
        expected: ['["foo","Cannot index number with string (\\"a\\")",3]']
        actual:   (no output)
        stderr:   compile error: expected end
    FAIL jq.test:1452  program did not compile: compile error: expected )
        program:  [.[]|(.a, .a)?]
        input:    [null,true,{"a":1}]
        expected: ['[null,null,1,1]']
        actual:   (no output)
        stderr:   compile error: expected )
    FAIL jq.test:1464  output mismatch
        program:  try error(0) // 1
        input:    null
        expected: ['1']
        actual:   (no output)
    FAIL jq.test:1481  output mismatch
        program:  try -.? catch .
        input:    "foo"
        expected: ['"string (\\"foo\\") cannot be negated"']
        actual:   (no output)
        stderr:   runtime error: bad operand type for unary -: 'str'
    FAIL jq.test:1493  output mismatch
        program:  .[] | try error catch .
        input:    [1,null,2]
        expected: ['1', 'null', '2']
        actual:   ['"error"', '"error"', '"error"']
    FAIL jq.test:1499  output mismatch
        program:  try error("\($__loc__)") catch .
        input:    null
        expected: ['"{\\"file\\":\\"<top-level>\\",\\"line\\":1}"']
        actual:   ['"None"']
    FAIL jq.test:1520  output mismatch
        program:  [.[]|ltrimstr("foo")]
        input:    ["fo", "foo", "barfoo", "foobar", "afoo"]
        expected: ['["fo","","barfoo","bar","afoo"]']
        actual:   (no output)
        stderr:   runtime error: unknown function ltrimstr
    FAIL jq.test:1524  output mismatch
        program:  [.[]|rtrimstr("foo")]
        input:    ["fo", "foo", "barfoo", "foobar", "foob"]
        expected: ['["fo","","bar","foobar","foob"]']
        actual:   (no output)
        stderr:   runtime error: unknown function rtrimstr
    FAIL jq.test:1528  output mismatch
        program:  [.[]|trimstr("foo")]
        input:    ["fo", "foo", "barfoo", "foobarfoo", "foob"]
        expected: ['["fo","","bar","bar","b"]']
        actual:   (no output)
        stderr:   runtime error: unknown function trimstr
    FAIL jq.test:1532  output mismatch
        program:  [.[]|ltrimstr("")]
        input:    ["a", "xx", ""]
        expected: ['["a", "xx", ""]']
        actual:   (no output)
        stderr:   runtime error: unknown function ltrimstr
    FAIL jq.test:1536  output mismatch
        program:  [.[]|rtrimstr("")]
        input:    ["a", "xx", ""]
        expected: ['["a", "xx", ""]']
        actual:   (no output)
        stderr:   runtime error: unknown function rtrimstr
    FAIL jq.test:1540  output mismatch
        program:  [.[]|trimstr("")]
        input:    ["a", "xx", ""]
        expected: ['["a", "xx", ""]']
        actual:   (no output)
        stderr:   runtime error: unknown function trimstr
    FAIL jq.test:1553  output mismatch
        program:  try _strindices("abc") catch .
        input:    123
        expected: ['"number (123) cannot be searched, as it is not a string"']
        actual:   ['"unknown function _strindices"']
    FAIL jq.test:1557  output mismatch
        program:  try _strindices(123) catch .
        input:    "abc"
        expected: ['"number (123) is not a string"']
        actual:   ['"unknown function _strindices"']
    FAIL jq.test:1575  output mismatch
        program:  try trim catch ., try ltrim catch ., try rtrim catch .
        input:    123
        expected: ['"trim input must be a string"', '"trim input must be a string"', '"trim input must be a string"']
        actual:   (no output)
        stderr:   runtime error: 'int' object has no attribute 'strip'
    FAIL jq.test:1601  program did not compile: compile error: unexpected :
        program:  .[:rindex("x")]
        input:    "正xyz"
        expected: ['"正"']
        actual:   (no output)
        stderr:   compile error: unexpected :
    FAIL jq.test:1625  output mismatch
        program:  [.[] * "abc"]
        input:    [-1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 3.7, 10.0]
        expected: ['[null,null,"","","abc","abc","abcabcabc","abcabcabcabcabcabcabcabcabcabc"]']
        actual:   (no output)
        stderr:   runtime error: can't multiply sequence by non-int of type 'float'
    FAIL jq.test:1629  output mismatch
        program:  [. * (nan,-nan)]
        input:    "abc"
        expected: ['[null,null]']
        actual:   (no output)
        stderr:   runtime error: unknown function nan
    FAIL jq.test:1633  program did not compile: compile error: unexpected :
        program:  . * 100000 | [.[:10],.[-10:]]
        input:    "abc"
        expected: ['["abcabcabca","cabcabcabc"]']
        actual:   (no output)
        stderr:   compile error: unexpected :
    FAIL jq.test:1641  output mismatch
        program:  try (. * 1000000000) catch .
        input:    "abc"
        expected: ['"Repeat string result too long"']
        actual:   (no output)
        stderr:   runtime error:
    FAIL jq.test:1645  output mismatch
        program:  [.[] / ","]
        input:    ["a, bc, def, ghij, jklmn, a,b, c,d, e,f", "a,b,c,d, e,f,g,h"]
        expected: ['[["a"," bc"," def"," ghij"," jklmn"," a","b"," c","d"," e","f"],["a","b","c","d"," e","f","g","h"]]']
        actual:   (no output)
        stderr:   runtime error: unsupported operand type(s) for /: 'str' and 'str'
    FAIL jq.test:1649  output mismatch
        program:  [.[] / ", "]
        input:    ["a, bc, def, ghij, jklmn, a,b, c,d, e,f", "a,b,c,d, e,f,g,h"]
        expected: ['[["a","bc","def","ghij","jklmn","a,b","c,d","e,f"],["a,b,c,d","e,f,g,h"]]']
        actual:   (no output)
        stderr:   runtime error: unsupported operand type(s) for /: 'str' and 'str'
    FAIL jq.test:1701  program did not compile: compile error: unexpected foo
        program:  .foo[.baz]
        input:    {"foo":{"bar":4},"baz":"bar"}
        expected: ['4']
        actual:   (no output)
        stderr:   compile error: unexpected foo
    FAIL jq.test:1705  program did not compile: compile error: unexpected error
        program:  .[] | .error = "no, it's OK"
        input:    [{"error":true}]
        expected: ['{"error": "no, it\'s OK"}']
        actual:   (no output)
        stderr:   compile error: unexpected error
    FAIL jq.test:1767  output mismatch
        program:  [.[]|arrays]
        input:    [1,2,"foo",[],[3,[]],{},true,false,null]
        expected: ['[[],[3,[]]]']
        actual:   (no output)
        stderr:   runtime error: unknown function arrays
    FAIL jq.test:1771  output mismatch
        program:  [.[]|objects]
        input:    [1,2,"foo",[],[3,[]],{},true,false,null]
        expected: ['[{}]']
        actual:   (no output)
        stderr:   runtime error: unknown function objects
    FAIL jq.test:1775  output mismatch
        program:  [.[]|iterables]
        input:    [1,2,"foo",[],[3,[]],{},true,false,null]
        expected: ['[[],[3,[]],{}]']
        actual:   (no output)
        stderr:   runtime error: unknown function iterables
    FAIL jq.test:1779  output mismatch
        program:  [.[]|scalars]
        input:    [1,2,"foo",[],[3,[]],{},true,false,null]
        expected: ['[1,2,"foo",true,false,null]']
        actual:   (no output)
        stderr:   runtime error: unknown function scalars
    FAIL jq.test:1783  output mismatch
        program:  [.[]|values]
        input:    [1,2,"foo",[],[3,[]],{},true,false,null]
        expected: ['[1,2,"foo",[],[3,[]],{},true,false]']
        actual:   (no output)
        stderr:   runtime error: unknown function values
    FAIL jq.test:1787  output mismatch
        program:  [.[]|booleans]
        input:    [1,2,"foo",[],[3,[]],{},true,false,null]
        expected: ['[true,false]']
        actual:   (no output)
        stderr:   runtime error: unknown function booleans
    FAIL jq.test:1791  output mismatch
        program:  [.[]|nulls]
        input:    [1,2,"foo",[],[3,[]],{},true,false,null]
        expected: ['[null]']
        actual:   (no output)
        stderr:   runtime error: unknown function nulls
    FAIL jq.test:1811  output mismatch
        program:  try flatten(-1) catch .
        input:    [0, [1], [[2]], [[[3]]]]
        expected: ['"flatten depth must not be negative"']
        actual:   ['"unknown function flatten"']
    FAIL jq.test:1839  output mismatch
        program:  try ["OK", bsearch(0)] catch ["KO",.]
        input:    "aa"
        expected: ['["KO","string (\\"aa\\") cannot be searched from"]']
        actual:   ['["KO","unknown function bsearch"]']
    FAIL jq.test:1868  output mismatch
        program:  try strftime("%Y-%m-%dT%H:%M:%SZ") catch .
        input:    ["a",1,2,3,4,5,6,7]
        expected: ['"strftime/1 requires parsed datetime inputs"']
        actual:   ['"unknown function strftime"']
    FAIL jq.test:1872  output mismatch
        program:  try strflocaltime("%Y-%m-%dT%H:%M:%SZ") catch .
        input:    ["a",1,2,3,4,5,6,7]
        expected: ['"strflocaltime/1 requires parsed datetime inputs"']
        actual:   ['"unknown function strflocaltime"']
    FAIL jq.test:1876  output mismatch
        program:  try mktime catch .
        input:    ["a",1,2,3,4,5,6,7]
        expected: ['"mktime requires parsed datetime inputs"']
        actual:   ['"unknown function mktime"']
    FAIL jq.test:1881  output mismatch
        program:  try ["OK", strftime([])] catch ["KO", .]
        input:    0
        expected: ['["KO","strftime/1 requires a string format"]']
        actual:   ['["KO","unknown function strftime"]']
    FAIL jq.test:1885  output mismatch
        program:  try ["OK", strflocaltime({})] catch ["KO", .]
        input:    0
        expected: ['["KO","strflocaltime/1 requires a string format"]']
        actual:   ['["KO","unknown function strflocaltime"]']
    FAIL jq.test:1997  output mismatch
        program:  try -. catch .
        input:    "very-long-long-long-long-string"
        expected: ['"string (\\"very-long-long-long-long...\\") cannot be negated"']
        actual:   (no output)
        stderr:   runtime error: bad operand type for unary -: 'str'
    FAIL jq.test:2001  output mismatch
        program:  try (.-.) catch .
        input:    "very-long-long-long-long-string"
        expected: ['"string (\\"very-long-long-long-long...\\") and string (\\"very-long-long-long-long...\\") cannot be subtracted"']
        actual:   (no output)
        stderr:   runtime error: unsupported operand type(s) for -: 'str' and 'str'
    FAIL jq.test:2014  output mismatch
        program:  try (. + "x") catch . == if have_decnum then "number (12345678901234567890123456...) and string (\"x\") cannot be added" else "number (12345678901234568000000000...) and string (\"x\") cannot be added" end
        input:    123456789012345678901234567890
        expected: ['true']
        actual:   (no output)
        stderr:   runtime error: unsupported operand type(s) for +: 'int' and 'str'
    FAIL jq.test:2022  output mismatch
        program:  .[] | join(",")
        input:    [[], [null], [null,null], [null,null,null]]
        expected: ['""', '""', '","', '",,"']
        actual:   ['""', '"None"', '"None,None"', '"None,None,None"']
    FAIL jq.test:2029  output mismatch
        program:  .[] | join(",")
        input:    [["a",null], [null,"a"]]
        expected: ['"a,"', '",a"']
        actual:   ['"a,None"', '"None,a"']
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
        actual:   ['"division by zero"']
    FAIL jq.test:2050  output mismatch
        program:  try (1/0) catch .
        input:    0
        expected: ['"number (1) and number (0) cannot be divided because the divisor is zero"']
        actual:   ['"division by zero"']
    FAIL jq.test:2054  output mismatch
        program:  try (0/0) catch .
        input:    0
        expected: ['"number (0) and number (0) cannot be divided because the divisor is zero"']
        actual:   ['"division by zero"']
    FAIL jq.test:2058  output mismatch
        program:  try (1%.) catch .
        input:    0
        expected: ['"number (1) and number (0) cannot be divided (remainder) because the divisor is zero"']
        actual:   (no output)
        stderr:   runtime error: integer modulo by zero
    FAIL jq.test:2062  output mismatch
        program:  try (1%0) catch .
        input:    0
        expected: ['"number (1) and number (0) cannot be divided (remainder) because the divisor is zero"']
        actual:   (no output)
        stderr:   runtime error: integer modulo by zero
    FAIL jq.test:2196  output mismatch
        program:  .[0] | tostring | . == if have_decnum then "13911860366432393" else "13911860366432392" end
        input:    [13911860366432393]
        expected: ['true']
        actual:   (no output)
        stderr:   runtime error: unknown function have_decnum
    FAIL jq.test:2200  program did not compile: compile error: unexpected x
        program:  .x | tojson | . == if have_decnum then "13911860366432393" else "13911860366432392" end
        input:    {"x":13911860366432393}
        expected: ['true']
        actual:   (no output)
        stderr:   compile error: unexpected x
    FAIL jq.test:2211  output mismatch
        program:  . - 10
        input:    13911860366432393
        expected: ['13911860366432382']
        actual:   ['13911860366432383']
    FAIL jq.test:2215  output mismatch
        program:  .[0] - 10
        input:    [13911860366432393]
        expected: ['13911860366432382']
        actual:   ['13911860366432383']
    FAIL jq.test:2219  program did not compile: compile error: unexpected x
        program:  .x - 10
        input:    {"x":13911860366432393}
        expected: ['13911860366432382']
        actual:   (no output)
        stderr:   compile error: unexpected x
    FAIL jq.test:2236  program did not compile: compile error: unexpected |=
        program:  . |= try . catch .
        input:    1
        expected: ['1']
        actual:   (no output)
        stderr:   compile error: unexpected |=
    FAIL jq.test:2241  program did not compile: compile error: unexpected as
        program:  .[] as $n | $n+0 | [., tostring, . == $n]
        input:    [-9007199254740993, -9007199254740992, 9007199254740992, 9007199254740993, 13911860366432393]
        expected: ['[-9007199254740992,"-9007199254740992",true]', '[-9007199254740992,"-9007199254740992",true]', '[9007199254740992,"9007199254740992",true]', '[9007199254740992,"9007199254740992",true]', '[13911860366432392,"13911860366432392",true]']
        actual:   (no output)
        stderr:   compile error: unexpected as
    FAIL jq.test:2289  program did not compile: compile error: unexpected .
        program:  reduce .[] as $then (4 as $else | $else; . as $elif | . + $then * $elif)
        input:    [1,2,3]
        expected: ['96']
        actual:   (no output)
        stderr:   compile error: unexpected .
    FAIL jq.test:2324  output mismatch
        program:  .[] | try (fromjson | isnan) catch .
        input:    ["NaN","-NaN","NaN1","NaN10","NaN100","NaN1000","NaN10000","NaN100000"]
        expected: ['true', 'true', '"Invalid numeric literal at EOF at line 1, column 4 (while parsing \'NaN1\')"', '"Invalid numeric literal at EOF at line 1, column 5 (while parsing \'NaN10\')"', '"Invalid numeric literal at EOF at line 1, column 6 (while parsing \'NaN100\')"', '"Invalid numeric literal at EOF at line 1, column 7 (while parsing \'NaN1000\')"', '"Invalid numeric literal at EOF at line 1, column 8 (while parsing \'NaN10000\')"', '"Invalid numeric literal at EOF at line 1, column 9 (while parsing \'NaN100000\')"']
        actual:   ['"unknown function isnan"']
        stderr:   runtime error: Expecting value: line 1 column 1 (char 0)
    FAIL jq.test:2337  output mismatch
        program:  try input catch .
        input:    null
        expected: ['"break"']
        actual:   ['"unknown function input"']
    FAIL jq.test:2350  output mismatch
        program:  .[]|(try (if .=="hi" then . else error end) catch empty) | "\(.) there!"
        input:    ["hi","ho"]
        expected: ['"hi there!"']
        actual:   ['"hihi"']
    FAIL jq.test:2354  output mismatch
        program:  try (["hi","ho"]|.[]|(try . catch (if .=="ho" then "BROKEN"|error else empty end)) | if .=="ho" then error else "\(.) there!" end) catch "caught outside \(.)"
        input:    null
        expected: ['"hi there!"', '"caught outside ho"']
        actual:   ['"hihi"', '"caught outside error"']
    FAIL jq.test:2359  output mismatch
        program:  .[]|(try . catch (if .=="ho" then "BROKEN"|error else empty end)) | if .=="ho" then error else "\(.) there!" end
        input:    ["hi","ho"]
        expected: ['"hi there!"']
        actual:   ['"hihi"']
        stderr:   runtime error: error
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
    FAIL jq.test:2382  program did not compile: compile error: unexpected |=
        program:  . |= try 2
        input:    1
        expected: ['2']
        actual:   (no output)
        stderr:   compile error: unexpected |=
    FAIL jq.test:2386  program did not compile: compile error: unexpected |=
        program:  . |= try 2 catch 3
        input:    1
        expected: ['2']
        actual:   (no output)
        stderr:   compile error: unexpected |=
    FAIL jq.test:2390  program did not compile: compile error: unexpected |=
        program:  .[] |= try tonumber
        input:    ["1", "2a", "3", " 4", "5 ", "6.7", ".89", "-876", "+5.43", 21]
        expected: ['[1, 3, 6.7, 0.89, -876, 5.43, 21]']
        actual:   (no output)
        stderr:   compile error: unexpected |=
    FAIL jq.test:2411  output mismatch
        program:  try 0[implode] catch .
        input:    []
        expected: ['"Cannot index number with string (\\"\\")"']
        actual:   ['"unknown function implode"']
    FAIL jq.test:2475  program did not compile: compile error: expected )
        program:  try ([range(3)] | .[nan] = 9) catch .
        input:    null
        expected: ['"Cannot set array element at NaN index"']
        actual:   (no output)
        stderr:   compile error: expected )
    FAIL jq.test:2479  program did not compile: compile error: expected )
        program:  try ("foobar" | .[1.5:3.5] = "xyz") catch .
        input:    null
        expected: ['"Cannot update string slices"']
        actual:   (no output)
        stderr:   compile error: expected )
    FAIL jq.test:2483  program did not compile: compile error: expected )
        program:  try ([range(10)] | .[1.5:3.5] = ["xyz"]) catch .
        input:    null
        expected: ['[0,"xyz",4,5,6,7,8,9]']
        actual:   (no output)
        stderr:   compile error: expected )
    FAIL jq.test:2487  output mismatch
        program:  try ("foobar" | .[1.5]) catch .
        input:    null
        expected: ['"Cannot index string with number (1.5)"']
        actual:   ['"o"']
    FAIL jq.test:2494  output mismatch
        program:  try ["ok", setpath([1]; 1)] catch ["ko", .]
        input:    {"hi":"hello"}
        expected: ['["ko","Cannot index object with number (1)"]']
        actual:   ['["ko","unknown function setpath"]']
    FAIL jq.test:2498  output mismatch
        program:  try fromjson catch .
        input:    "{'a': 123}"
        expected: ['"Invalid string literal; expected \\", but got \' at line 1, column 5 (while parsing \'{\'a\': 123}\')"']
        actual:   (no output)
        stderr:   runtime error: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
    FAIL jq.test:2504  output mismatch
        program:  try ltrimstr(1) catch "x", try rtrimstr(1) catch "x" | "ok"
        input:    "hi"
        expected: ['"ok"', '"ok"']
        actual:   ['"x"', '"ok"']
    FAIL jq.test:2509  output mismatch
        program:  try ltrimstr("x") catch "x", try rtrimstr("x") catch "x" | "ok"
        input:    {"hey":[]}
        expected: ['"ok"', '"ok"']
        actual:   ['"x"', '"ok"']
    FAIL jq.test:2516  program did not compile: compile error: unexpected as
        program:  .[] as [$x, $y] | try ["ok", ($x | ltrimstr($y))] catch ["ko", .]
        input:    [["hi",1],[1,"hi"],["hi","hi"],[1,1]]
        expected: ['["ko","startswith() requires string inputs"]', '["ko","startswith() requires string inputs"]', '["ok",""]', '["ko","startswith() requires string inputs"]']
        actual:   (no output)
        stderr:   compile error: unexpected as
    FAIL jq.test:2523  program did not compile: compile error: unexpected as
        program:  .[] as [$x, $y] | try ["ok", ($x | rtrimstr($y))] catch ["ko", .]
        input:    [["hi",1],[1,"hi"],["hi","hi"],[1,1]]
        expected: ['["ko","endswith() requires string inputs"]', '["ko","endswith() requires string inputs"]', '["ok",""]', '["ko","endswith() requires string inputs"]']
        actual:   (no output)
        stderr:   compile error: unexpected as
    FAIL jq.test:2533  output mismatch
        program:  try ["OK", setpath([[1]]; 1)] catch ["KO", .]
        input:    []
        expected: ['["KO","Cannot update field at array index of array"]']
        actual:   ['["KO","unknown function setpath"]']
    FAIL jq.test:2538  program did not compile: compile error: unexpected .
        program:  foreach .[] as $x (0, 1; . + $x)
        input:    [1, 2]
        expected: ['1', '3', '2', '4']
        actual:   (no output)
        stderr:   compile error: unexpected .
    FAIL jq.test:2558  program did not compile: compile error: unexpected range
        program:  reduce range(9999) as $_ ([];[.]) | tojson | fromjson | flatten
        input:    null
        expected: ['[]']
        actual:   (no output)
        stderr:   compile error: unexpected range
    FAIL jq.test:2563  program did not compile: compile error: unexpected range
        program:  reduce range(10000) as $_ ([];[.]) | tojson | try (fromjson) catch . | (contains("<skipped: too deep>") | not) and contains("Exceeds depth limit for parsing")
        input:    null
        expected: ['true']
        actual:   (no output)
        stderr:   compile error: unexpected range
    FAIL jq.test:2568  program did not compile: compile error: unexpected range
        program:  reduce range(10001) as $_ ([];[.]) | tojson | contains("<skipped: too deep>")
        input:    null
        expected: ['true']
        actual:   (no output)
        stderr:   compile error: unexpected range
    FAIL jq.test:2577  output mismatch
        program:  try setpath([range(10001) | 0]; 0) catch .
        input:    null
        expected: ['"Path too deep"']
        actual:   ['"unknown function setpath"']
    FAIL jq.test:2585  output mismatch
        program:  try getpath([range(10001) | 0]) catch .
        input:    null
        expected: ['"Path too deep"']
        actual:   ['"unknown function getpath"']
    FAIL jq.test:2593  output mismatch
        program:  try delpaths([[range(10001) | 0]]) catch .
        input:    null
        expected: ['"Path too deep"']
        actual:   ['"unknown function delpaths"']
    FAIL jq.test:2598  program did not compile: compile error: unexpected range
        program:  reduce range(10000) as $_ ([]; [.]) | contains([[]])
        input:    null
        expected: ['true']
        actual:   (no output)
        stderr:   compile error: unexpected range
    FAIL jq.test:2602  program did not compile: compile error: expected )
        program:  try (reduce range(10001) as $_ ([]; [.]) as $x | $x | contains($x)) catch .
        input:    null
        expected: ['"Containment check too deep"']
        actual:   (no output)
        stderr:   compile error: expected )
    FAIL jq.test:2607  program did not compile: compile error: unexpected range
        program:  reduce range(10000) as $_ ({}; {a: .}) as $x | $x * $x | length
        input:    null
        expected: ['1']
        actual:   (no output)
        stderr:   compile error: unexpected range
    FAIL jq.test:2611  program did not compile: compile error: expected )
        program:  try (reduce range(10001) as $_ ({}; {a: .}) as $x | $x * $x) catch .
        input:    null
        expected: ['"Object merge too deep"']
        actual:   (no output)
        stderr:   compile error: expected )
    FAIL jq.test:2616  program did not compile: compile error: expected )
        program:  try ((reduce range(10001) as $_ ([]; [.])) as $x | (reduce range(10001) as $_ ([]; [.])) as $y | $x == $y) catch .
        input:    null
        expected: ['"Equality check too deep"']
        actual:   (no output)
        stderr:   compile error: expected )
    FAIL jq.test:2621  program did not compile: compile error: expected )
        program:  try ((reduce range(10001) as $_ ([]; [.])) as $x | [$x, $x] | sort) catch .
        input:    null
        expected: ['"Comparison too deep"']
        actual:   (no output)
        stderr:   compile error: expected )
    FAIL jq.test:2625  program did not compile: compile error: expected )
        program:  try ((reduce range(10001) as $_ ([]; [.])) as $x | [$x, $x] | unique) catch .
        input:    null
        expected: ['"Comparison too deep"']
        actual:   (no output)
        stderr:   compile error: expected )
    FAIL jq.test:2629  program did not compile: compile error: expected )
        program:  try ((reduce range(10001) as $_ ({}; {a: .})) as $x | [$x, $x] | sort) catch .
        input:    null
        expected: ['"Comparison too deep"']
        actual:   (no output)
        stderr:   compile error: expected )
    FAIL jq.test:2633  program did not compile: compile error: expected )
        program:  try ((reduce range(10001) as $_ ({}; {a: .})) as $x | [$x, $x] | unique) catch .
        input:    null
        expected: ['"Comparison too deep"']
        actual:   (no output)
        stderr:   compile error: expected )
    jq conformance: 29 passed, 193 failed, 0 errored, 0 skipped (corpus jq.test @ jq-1.8.2)
  stderr:
    --- drydock: values at failure ---
      result = CompletedProcess(args=['/mnt/c/Users/barlo/projects/drydock/.venv/bin/python3', 'sources/run_conformance.py', '--select', '^(\\.foo|\\.|\\[\\.|def |if |reduce |foreach |try |@)'], returncode=1, stdout='FAIL jq.test:48  output mismatch\n    program:  .\n    input:    \ufeff"byte order mark"\n    expected: [\'"byte order mark"\']\n    actual:   (no output)\n    stderr:   runtime error: Unexpected UT… (+53582 chars)
    --- drydock: end values ---
    Traceback (most recent call last):
      File "parser-valid-programs.py", line 14, in <module>
        assert result.returncode == 0
               ^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- GREEN (prepassed): parser-invalid-programs (FEATURE-FRONTEND-PARSER.md)
  intent: Invalid jq syntax is rejected with the documented compile-error status.
  return code: 0
- RED: parser-precedence (FEATURE-FRONTEND-PARSER.md)
  intent: Parsed arithmetic precedence and grouping are accepted by the authoritative corpus.
  return code: 1
  stdout:
    FAIL jq.test:122  output mismatch
        program:  {"a",b,"a$\(1+1)"}
        input:    {"a":1, "b":2, "c":3, "a$2":4}
        expected: ['{"a":1, "b":2, "a$2":4}']
        actual:   ['{"a":1,"b":2,"a$\\\\(1+1)":null}']
    jq conformance: 4 passed, 1 failed, 0 errored, 0 skipped (corpus jq.test @ jq-1.8.2)
  stderr:
    --- drydock: values at failure ---
      result = CompletedProcess(args=['/mnt/c/Users/barlo/projects/drydock/.venv/bin/python3', 'sources/run_conformance.py', '--select', '1\\+1|1 \\+ 2 \\* 2|16 / 4'], returncode=1, stdout='FAIL jq.test:122  output mismatch\n    program:  {"a",b,"a$\\(1+1)"}\n    input:    {"a":1, "b":2, "c":3, "a$2":4}\n    expected: [\'{"a":1, "b":2, "a$2":4}\']\n    actual:   [\'{"a":1,"b":2,"a$\\\\\\\\(1+1)":null}\']\njq con… (+93 chars)
    --- drydock: end values ---
    Traceback (most recent call last):
      File "parser-precedence.py", line 14, in <module>
        assert result.returncode == 0
               ^^^^^^^^^^^^^^^^^^^^^^
    AssertionError

## Failure
- summary: target verification interrupted by build agent
- detail:
    A target verification command was interrupted inside the build-agent session. Drydock did not configure an LLM execution timeout for this build. The evaluator hangs while running the supplied corpus; further runtime debugging is required before rerunning the build.

## Build summary
RESULT: FAILED

FILES CHANGED:
- jq
- tests/test_parser.py

SUMMARY:
Implemented parser support for definitions, bindings, reductions, precedence, interpolation, and compile/runtime status handling. Focused tests passed; precedence acceptance passed 5/5.

BLOCKERS:
- Full conformance hung in an unsupported evaluator case and was interrupted.
- Broad parser-valid acceptance did not terminate.

FAILURE_SUMMARY: Full conformance did not complete.
FAILURE_DETAIL: The evaluator hangs while running the supplied corpus; further runtime debugging is required before rerunning the build.

## Diagnosis

CAUSE: The jq implementation still misparses or lacks core constructs and builtins, causing the conformance evaluator to hang on unsupported programs.
DO: Edit `jq` to correctly implement the failing parser constructs, interpolation, `range`, `getpath`, `setpath`, and `delpaths`.
DO: Run `drydock build jq --step block-5`.
