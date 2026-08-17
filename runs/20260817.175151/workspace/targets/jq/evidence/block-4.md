# Evidence: Block 4 · Foundational (block-4)

- block type: block
- date: 2026-08-17
- resulting state: closed/verified
- story points (combined assembled cost): 65384
- execution id: 20260817.181403.647Z-116220d6

## Stories built
- Stage and validate the supplied conformance assets. (conformance-staging) [story]

## Reusable compacts
- exclusions_compact.md
- full_test_compact.md
- run_conformance_compact.md
- parser_compact.md
- builtin_compact.md

## Missing context
- context: INSTRUCTIONS.md

## Stacked context
- compass: COMPASS.md (SP 2068)
- implements: FEATURE-Conformance-Staging.md (SP 462)
- context: jq.test (SP 13058)
- context: exclusions.txt (SP 654)
- context: full_test.sh (SP 189)
- context: run_conformance.py (SP 4354)
- context: jq-manual.txt (SP 32696)
- context: parser.y (SP 5596)
- context: lexer.l (SP 1137)
- context: builtin.jq (SP 2408)
- stack: python_compact.md (SP 1534)
- stack: common_compact.md (SP 1179)

## Build directory changes
- tests/test_conformance_staging.py

## Pre-build acceptance observation
- GREEN (prepassed): conformance-staging-list (FEATURE-Conformance-Staging.md)
  intent: The staged conformance harness parses and enumerates its corpus successfully without executing cases.
  return code: 0
  stdout:
    run  jq.test:8  true
    run  jq.test:12  false
    run  jq.test:16  null
    run  jq.test:20  1
    run  jq.test:25  -1
    run  jq.test:31  {}
    run  jq.test:35  []
    run  jq.test:39  {x:-1},{x:-.},{x:-.|abs}
    run  jq.test:48  .
    run  jq.test:54  "Aa\r\n\t\b\f\u03bc"
    run  jq.test:58  .
    run  jq.test:63  "u\vw"
    run  jq.test:68  "inter\("pol" + "ation")"
    run  jq.test:72  @text,@json,([1,.]|@csv,@tsv),@html,(@uri|.,@urid),@sh,(@base64|.,@base64d)
    run  jq.test:86  @base64
    run  jq.test:90  @base64d
    run  jq.test:94  @uri
    run  jq.test:98  @urid
    run  jq.test:102  @html "<b>\(.)</b>"
    run  jq.test:106  [.[]|tojson|fromjson]
    run  jq.test:114  {a: 1}
    run  jq.test:118  {a,b,(.d):.a,e:.b}
    run  jq.test:122  {"a",b,"a$\(1+1)"}
    run  jq.test:127  {(0):1}
    run  jq.test:133  {1+2:3}
    run  jq.test:139  {non_const:., (0):1}
    run  jq.test:148  .foo
    run  jq.test:152  .foo | .bar
    run  jq.test:156  .foo.bar
    run  jq.test:160  .foo_bar
    run  jq.test:164  .["foo"].bar
    run  jq.test:168  ."foo"."bar"
    run  jq.test:172  .e0, .E1, .E-1, .E+1
    run  jq.test:179  [.[]|.foo?]
    run  jq.test:183  [.[]|.foo?.bar?]
    run  jq.test:187  [..]
    run  jq.test:191  [.[]|.[]?]
    run  jq.test:195  [.[]|.[1:3]?]
    run  jq.test:200  map(try .a[] catch ., try .a.[] catch ., .a[]?, .a.[]?)
    run  jq.test:205  try ["OK", (.[] | error)] catch ["KO", .]
    run  jq.test:213  try (.foo[-1] = 0) catch .
    run  jq.test:217  try (.foo[-2] = 0) catch .
    run  jq.test:221  .[-1] = 5
    run  jq.test:225  .[-2] = 5
    run  jq.test:229  try (.[999999999] = 0) catch .
    run  jq.test:237  .[]
    run  jq.test:243  1,1
    run  jq.test:248  1,.
    run  jq.test:253  [.]
    run  jq.test:257  [[2]]
    run  jq.test:261  [{}]
    run  jq.test:265  [.[]]
    run  jq.test:269  [(.,1),((.,.[]),(2,3))]
    run  jq.test:273  [([5,5][]),.,.[]]
    run  jq.test:277  {x: (1,2)},{x:3} | .x
    run  jq.test:283  [.[-4,-3,-2,-1,0,1,2,3]]
    run  jq.test:287  [range(0;10)]
    run  jq.test:291  [range(0,1;3,4)]
    run  jq.test:295  [range(0;10;3)]
    run  jq.test:299  [range(0;10;-1)]
    run  jq.test:303  [range(0;-5;-1)]
    run  jq.test:307  [range(0,1;4,5;1,2)]
    run  jq.test:311  [while(.<100; .*2)]
    run  jq.test:315  [(label $here | .[] | if .>1 then break $here else . end), "hi!"]
    run  jq.test:319  [(label $here | .[] | if .>1 then break $here else . end), "hi!"]
    run  jq.test:324  . as $foo | break $foo
    run  jq.test:329  [.[]|[.,1]|until(.[0] < 1; [.[0] - 1, .[1] * .[0]])|.[1]]
    run  jq.test:333  [label $out | foreach .[] as $item ([3, null]; if .[0] < 1 then break $out else [.[0] -1, $item] end; .[1])]
    run  jq.test:337  [foreach range(5) as $item (0; $item)]
    run  jq.test:341  [foreach .[] as [$i, $j] (0; . + $i - $j)]
    run  jq.test:345  [foreach .[] as {a:$a} (0; . + $a; -.)]
    run  jq.test:349  [-foreach -.[] as $x (0; . + $x)]
    run  jq.test:353  [foreach .[] / .[] as $i (0; . + $i)]
    run  jq.test:357  [foreach .[] as $x (0; . + $x) as $x | $x]
    run  jq.test:361  [limit(3; .[])]
    run  jq.test:365  [limit(0; error)]
    run  jq.test:369  [limit(1; 1, error)]
    run  jq.test:373  try limit(-1; error) catch .
    run  jq.test:377  [skip(3; .[])]
    run  jq.test:381  [skip(0,2,3,4; .[])]
    run  jq.test:385  [skip(3; .[])]
    run  jq.test:389  try skip(-1; error) catch .
    run  jq.test:393  nth(1; 0,1,error("foo"))
    run  jq.test:397  [first(range(.)), last(range(.))]
    run  jq.test:401  [first(range(.)), last(range(.))]
    run  jq.test:405  [nth(0,5,9,10,15; range(.)), try nth(-1; range(.)) catch .]
    run  jq.test:410  first(1,error("foo"))
    run  jq.test:420  [limit(5,7; range(9))]
    run  jq.test:425  [nth(5,7; range(9;0;-1))]
    run  jq.test:430  [range(0,1,2;4,3,2;2,3)]
    run  jq.test:435  [range(3,5)]
    run  jq.test:440  [(index(",","|"), rindex(",","|")), indices(",","|")]
    run  jq.test:445  join(",","/")
    run  jq.test:450  [.[]|join("a")]
    run  jq.test:455  flatten(3,2,1)
    run  jq.test:466  [.[3:2], .[-5:4], .[:-2], .[-2:], .[3:3][1:], .[10:]]
    run  jq.test:470  [.[3:2], .[-5:4], .[:-2], .[-2:], .[3:3][1:], .[10:]]
    run  jq.test:474  del(.[2:4],.[0],.[-2:])
    run  jq.test:478  .[2:4] = ([], ["a","b"], ["a","b","c"])
    run  jq.test:490  reduce range(65540;65536;-1) as $i ([]; .[$i] = $i)|.[65536:]
    run  jq.test:498  1 as $x | 2 as $y | [$x,$y,$x]
    run  jq.test:502  [1,2,3][] as $x | [[4,5,6,7][$x]]
    run  jq.test:508  42 as $x | . | . | . + 432 | $x + 1
    run  jq.test:512  1 + 2 as $x | -$x
    run  jq.test:516  "x" as $x | "a"+"y" as $y | $x+","+$y
    run  jq.test:520  1 as $x | [$x,$x,$x as $x | $x]
    run  jq.test:524  [1, {c:3, d:4}] as [$a, {c:$b, b:$c}] | $a, $b, $c
    run  jq.test:530  . as {as: $kw, "str": $str, ("e"+"x"+"p"): $exp} | [$kw, $str, $exp]
    run  jq.test:534  .[] as [$a, $b] | [$b, $a]
    run  jq.test:539  . as $i | . as [$i] | $i
    run  jq.test:543  . as [$i] | . as $i | $i
    run  jq.test:548  . as [] | null
    run  jq.test:554  . as {} | null
    run  jq.test:560  . as $foo | [$foo, $bar]
    run  jq.test:566  . as {(true):$foo} | $foo
    run  jq.test:577  1+1
    run  jq.test:581  1+1
    run  jq.test:585  2-1
    run  jq.test:589  2-(-1)
    run  jq.test:593  1e+0+0.001e3
    run  jq.test:597  .+4
    run  jq.test:601  .+null
    run  jq.test:605  null+.
    run  jq.test:609  .a+.b
    run  jq.test:613  [1,2,3] + [.]
    run  jq.test:617  {"a":1} + {"b":2} + {"c":3}
    run  jq.test:621  "asdf" + "jkl;" + . + . + .
    run  jq.test:625  "\u0000\u0020\u0000" + .
    run  jq.test:629  42 - .
    run  jq.test:633  [1,2,3,4,1] - [.,3]
    run  jq.test:637  [-1 as $x | 1,$x]
    run  jq.test:641  [10 * 20, 20 / .]
    run  jq.test:645  1 + 2 * 2 + 10 / 2
    run  jq.test:649  [16 / 4 / 2, 16 / 4 * 2, 16 - 4 - 2, 16 - 4 + 2]
    run  jq.test:653  1e-19 + 1e-20 - 5e-21
    run  jq.test:657  1 / 1e-17
    run  jq.test:661  9E999999999, 9999999999E999999990, 1E-999999999, 0.000000001E-999999990
    run  jq.test:668  5E500000000 > 5E-5000000000, 10000E500000000 > 10000E-5000000000
    run  jq.test:674  (1e999999999, 10e999999999) > (1e-1147483646, 0.1e-1147483646)
    run  jq.test:681  25 % 7
    run  jq.test:685  49732 % 472
    run  jq.test:689  [(infinite, -infinite) % (1, -1, infinite)]
    run  jq.test:693  [nan % 1, 1 % nan | isnan]
    run  jq.test:697  1 + tonumber + ("10" | tonumber)
    run  jq.test:701  "123\u0000456" | try tonumber catch .
    run  jq.test:705  map(toboolean)
    run  jq.test:709  .[] | try toboolean catch .
    run  jq.test:720  "true\u0000x", "false\u0000" | try toboolean catch .
    run  jq.test:725  [{"a":42},.object,10,.num,false,true,null,"b",[1,4]] | .[] as $x | [$x == .[]]
    run  jq.test:737  [.[] | length]
    run  jq.test:741  utf8bytelength
    run  jq.test:745  [.[] | try utf8bytelength catch .]
    run  jq.test:750  map(keys)
    run  jq.test:754  [1,2,empty,3,empty,4]
    run  jq.test:758  map(add)
    run  jq.test:762  map_values(.+1)
    run  jq.test:766  [add(null), add(range(range(10))), add(empty), add(10,range(10))]
    run  jq.test:771  .sum = add(.arr[])
    run  jq.test:775  add({(.[]):1}) | keys
    run  jq.test:784  def f: . + 1; def g: def g: . + 100; f | g | f; (f | g), g
    run  jq.test:789  def f: (1000,2000); f
    run  jq.test:794  def f(a;b;c;d;e;f): [a+1,b,c,d,e,f]; f(.[0];.[1];.[0];.[0];.[0];.[0])
    run  jq.test:798  def f: 1; def g: f, def f: 2; def g: 3; f, def f: g; f, g; def f: 4; [f, def f: g; def g: 5; f, g]+[f,g]
    run  jq.test:803  def a: 0; . | a
    run  jq.test:808  def f(a;b;c;d;e;f;g;h;i;j): [j,i,h,g,f,e,d,c,b,a]; f(.[0];.[1];.[2];.[3];.[4];.[5];.[6];.[7];.[8];.[9])
    run  jq.test:812  ([1,2] + [4,5])
    run  jq.test:816  true
    run  jq.test:820  null,1,null
    run  jq.test:826  [1,2,3]
    run  jq.test:830  [.[]|floor]
    run  jq.test:834  [.[]|sqrt]
    run  jq.test:838  (add / length) as $m | map((. - $m) as $d | $d * $d) | add / length | sqrt
    run  jq.test:847  atan * 4 * 1000000|floor / 1000000
    run  jq.test:851  [(3.141592 / 2) * (range(0;20) / 20)|cos * 1000000|floor / 1000000]
    run  jq.test:855  [(3.141592 / 2) * (range(0;20) / 20)|sin * 1000000|floor / 1000000]
    run  jq.test:860  def f(x): x | x; f([.], . + [42])
    run  jq.test:868  def f: .+1; def g: f; def f: .+100; def f(a):a+.+11; [(g|f(20)), f]
    run  jq.test:873  def id(x):x; 2000 as $x | def f(x):1 as $x | id([$x, x, x]); def g(x): 100 as $x | f($x,$x+x); g($x)
    run  jq.test:878  def x(a;b): a as $a | b as $b | $a + $b; def y($a;$b): $a + $b; def check(a;b): [x(a;b)] == [y(a;b)]; check(.[];.[]*2)
    run  jq.test:884  [[20,10][1,0] as $x | def f: (100,200) as $y | def g: [$x + $y, .]; . + $x | g; f[0] | [f][0][1] | f]
    run  jq.test:889  def fac: if . == 1 then 1 else . * (. - 1 | fac) end; [.[] | fac]
    run  jq.test:899  reduce .[] as $x (0; . + $x)
    run  jq.test:903  reduce .[] as [$i, {j:$j}] (0; . + $i - $j)
    run  jq.test:907  reduce [[1,2,10], [3,4,10]][] as [$i,$j] (0; . + $i * $j)
    run  jq.test:911  [-reduce -.[] as $x (0; . + $x)]
    run  jq.test:915  [reduce .[] / .[] as $i (0; . + $i)]
    run  jq.test:919  reduce .[] as $x (0; . + $x) as $x | $x
    run  jq.test:924  reduce . as $n (.; .)
    run  jq.test:929  . as {$a, b: [$c, {$d}]} | [$a, $c, $d]
    run  jq.test:933  . as {$a, $b:[$c, $d]}| [$a, $b, $c, $d]
    run  jq.test:938  .[] | . as {$a, b: [$c, {$d}]} ?// [$a, {$b}, $e] ?// $f | [$a, $b, $c, $d, $e, $f]
    run  jq.test:945  .[] | . as {a:$a} ?// {a:$a} ?// {a:$a} | $a
    run  jq.test:949  .[] as {a:$a} ?// {a:$a} ?// {a:$a} | $a
    run  jq.test:953  [[3],[4],[5],6][] | . as {a:$a} ?// {a:$a} ?// {a:$a} | $a
    run  jq.test:957  [[3],[4],[5],6] | .[] as {a:$a} ?// {a:$a} ?// {a:$a} | $a
    run  jq.test:961  .[] | . as {a:$a} ?// {a:$a} ?// $a | $a
    run  jq.test:968  .[] as {a:$a} ?// {a:$a} ?// $a | $a
    run  jq.test:975  [[3],[4],[5],6][] | . as {a:$a} ?// {a:$a} ?// $a | $a
    run  jq.test:982  [[3],[4],[5],6] | .[] as {a:$a} ?// {a:$a} ?// $a | $a
    run  jq.test:989  .[] | . as {a:$a} ?// $a ?// {a:$a} | $a
    run  jq.test:996  .[] as {a:$a} ?// $a ?// {a:$a} | $a
    run  jq.test:1003  [[3],[4],[5],6][] | . as {a:$a} ?// $a ?// {a:$a} | $a
    run  jq.test:1010  [[3],[4],[5],6] | .[] as {a:$a} ?// $a ?// {a:$a} | $a
    run  jq.test:1017  .[] | . as $a ?// {a:$a} ?// {a:$a} | $a
    run  jq.test:1024  .[] as $a ?// {a:$a} ?// {a:$a} | $a
    run  jq.test:1031  [[3],[4],[5],6][] | . as $a ?// {a:$a} ?// {a:$a} | $a
    run  jq.test:1038  [[3],[4],[5],6] | .[] as $a ?// {a:$a} ?// {a:$a} | $a
    run  jq.test:1045  . as $dot|any($dot[];not)
    run  jq.test:1049  . as $dot|any($dot[];not)
    run  jq.test:1053  . as $dot|all($dot[];.)
    run  jq.test:1057  . as $dot|all($dot[];.)
    run  jq.test:1062  any(true, error; .)
    run  jq.test:1066  all(false, error; .)
    run  jq.test:1070  any(not)
    run  jq.test:1074  all(not)
    run  jq.test:1078  any(not)
    run  jq.test:1082  all(not)
    run  jq.test:1086  [any,all]
    run  jq.test:1090  [any,all]
    run  jq.test:1094  [any,all]
    run  jq.test:1098  [any,all]
    run  jq.test:1102  [any,all]
    run  jq.test:1110  path(.foo[0,1])
    run  jq.test:1115  path(.[] | select(.>3))
    run  jq.test:1119  path(.)
    run  jq.test:1123  try path(.a | map(select(.b == 0))) catch .
    run  jq.test:1127  try path(.a | map(select(.b == 0)) | .[0]) catch .
    run  jq.test:1131  try path(.a | map(select(.b == 0)) | .c) catch .
    run  jq.test:1135  try path(.a | map(select(.b == 0)) | .[]) catch .
    run  jq.test:1139  path(.a[path(.b)[0]])
    run  jq.test:1143  [paths]
    run  jq.test:1147  ["foo",1] as $p | getpath($p), setpath($p; 20), delpaths([$p])
    run  jq.test:1153  map(getpath([2])), map(setpath([2]; 42)), map(delpaths([[2]]))
    run  jq.test:1159  map(delpaths([[0,"foo"]]))
    run  jq.test:1163  ["foo",1] as $p | getpath($p), setpath($p; 20), delpaths([$p])
    run  jq.test:1169  delpaths([[-200]])
    run  jq.test:1173  try delpaths(0) catch .
    run  jq.test:1177  del(.), del(empty), del((.foo,.bar,.baz) | .[2,3,0]), del(.foo[0], .bar[0], .foo, .baz.bar[0].x)
    run  jq.test:1184  del(.[1], .[-6], .[2], .[-3:9])
    run  jq.test:1188  del(.[nan])
    run  jq.test:1192  del(.[nan,nan])
    run  jq.test:1197  setpath([-1]; 1)
    run  jq.test:1201  pick(.a.b.c)
    run  jq.test:1205  pick(first)
    run  jq.test:1209  pick(first|first)
    run  jq.test:1214  try pick(last) catch .
    run  jq.test:1221  .message = "goodbye"
    run  jq.test:1225  .foo = .bar
    run  jq.test:1229  .foo |= .+1
    run  jq.test:1233  .[] += 2, .[] *= 2, .[] -= 2, .[] /= 2, .[] %=2
    run  jq.test:1241  [.[] % 7]
    run  jq.test:1245  .foo += .foo
    run  jq.test:1249  .[0].a |= {"old":., "new":(.+1)}
    run  jq.test:1253  def inc(x): x |= .+1; inc(.[].a)
    run  jq.test:1258  .[] | try (getpath(["a",0,"b"]) |= 5) catch .
    run  jq.test:1270  (.[] | select(. >= 2)) |= empty
    run  jq.test:1274  .[] |= select(. % 2 == 0)
    run  jq.test:1278  .foo[1,4,2,3] |= empty
    run  jq.test:1282  .[2][3] = 1
    run  jq.test:1286  .foo[2].bar = 1
    run  jq.test:1290  try ((map(select(.a == 1))[].b) = 10) catch .
    run  jq.test:1294  try ((map(select(.a == 1))[].a) |= .+1) catch .
    run  jq.test:1298  def x: .[1,2]; x=10
    run  jq.test:1302  try (def x: reverse; x=10) catch .
    run  jq.test:1306  .[] = 1
    run  jq.test:1314  [.[] | if .foo then "yep" else "nope" end]
    run  jq.test:1318  [.[] | if .baz then "strange" elif .foo then "yep" else "nope" end]
    run  jq.test:1322  [if 1,null,2 then 3 else 4 end]
    run  jq.test:1326  [if empty then 3 else 4 end]
    run  jq.test:1330  [if 1 then 3,4 else 5 end]
    run  jq.test:1334  [if null then 3 else 5,6 end]
    run  jq.test:1338  [if true then 3 end]
    run  jq.test:1342  [if false then 3 end]
    run  jq.test:1346  [if false then 3 else . end]
    run  jq.test:1350  [if false then 3 elif false then 4 end]
    run  jq.test:1354  [if false then 3 elif false then 4 else . end]
    run  jq.test:1358  [-if true then 1 else 2 end]
    run  jq.test:1362  {x: if true then 1 else 2 end}
    run  jq.test:1366  if true then [.] else . end []
    run  jq.test:1370  [.[] | [.foo[] // .bar]]
    run  jq.test:1374  .[] //= .[0]
    run  jq.test:1378  .[] | [.[0] and .[1], .[0] or .[1]]
    run  jq.test:1385  [.[] | not]
    run  jq.test:1390  [10 > 0, 10 > 10, 10 > 20, 10 < 0, 10 < 10, 10 < 20]
    run  jq.test:1394  [10 >= 0, 10 >= 10, 10 >= 20, 10 <= 0, 10 <= 10, 10 <= 20]
    run  jq.test:1399  [ 10 == 10, 10 != 10, 10 != 11, 10 == 11]
    run  jq.test:1403  ["hello" == "hello", "hello" != "hello", "hello" == "world", "hello" != "world" ]
    run  jq.test:1407  [[1,2,3] == [1,2,3], [1,2,3] != [1,2,3], [1,2,3] == [4,5,6], [1,2,3] != [4,5,6]]
    run  jq.test:1411  [{"foo":42} == {"foo":42},{"foo":42} != {"foo":42}, {"foo":42} != {"bar":42}, {"foo":42} == {"bar":42}]
    run  jq.test:1416  [{"foo":[1,2,{"bar":18},"world"]} == {"foo":[1,2,{"bar":18},"world"]},{"foo":[1,2,{"bar":18},"world"]} == {"foo":[1,2,{"bar":19},"world"]}]
    run  jq.test:1421  [("foo" | contains("foo")), ("foobar" | contains("foo")), ("foo" | contains("foobar"))]
    run  jq.test:1426  [contains(""), contains("\u0000")]
    run  jq.test:1430  [contains(""), contains("a"), contains("ab"), contains("c"), contains("d")]
    run  jq.test:1434  [contains("cd"), contains("b\u0000"), contains("ab\u0000")]
    run  jq.test:1438  [contains("b\u0000c"), contains("b\u0000cd"), contains("b\u0000cd")]
    run  jq.test:1442  [contains("@"), contains("\u0000@"), contains("\u0000what")]
    run  jq.test:1448  [.[]|try if . == 0 then error("foo") elif . == 1 then .a elif . == 2 then empty else . end catch .]
    run  jq.test:1452  [.[]|(.a, .a)?]
    run  jq.test:1456  [[.[]|[.a,.a]]?]
    run  jq.test:1460  [if error then 1 else 2 end?]
    run  jq.test:1464  try error(0) // 1
    run  jq.test:1468  1, try error(2), 3
    run  jq.test:1473  1 + try 2 catch 3 + 4
    run  jq.test:1477  [-try .]
    run  jq.test:1481  try -.? catch .
    run  jq.test:1485  {x: try 1, y: try error catch 2, z: if true then 3 end}
    run  jq.test:1489  {x: 1 + 2, y: false or true, z: null // 3}
    run  jq.test:1493  .[] | try error catch .
    run  jq.test:1499  try error("\($__loc__)") catch .
    run  jq.test:1504  [.[]|startswith("foo")]
    run  jq.test:1508  [.[]|endswith("foo")]
    run  jq.test:1512  [.[] | split(", ")]
    run  jq.test:1516  split("")
    run  jq.test:1520  [.[]|ltrimstr("foo")]
    run  jq.test:1524  [.[]|rtrimstr("foo")]
    run  jq.test:1528  [.[]|trimstr("foo")]
    run  jq.test:1532  [.[]|ltrimstr("")]
    run  jq.test:1536  [.[]|rtrimstr("")]
    run  jq.test:1540  [.[]|trimstr("")]
    run  jq.test:1544  [(index(","), rindex(",")), indices(",")]
    run  jq.test:1548  [ index("aba"), rindex("aba"), indices("aba") ]
    run  jq.test:1553  try _strindices("abc") catch .
    run  jq.test:1557  try _strindices(123) catch .
    run  jq.test:1563  map(trim), map(ltrim), map(rtrim)
    run  jq.test:1569  trim, ltrim, rtrim
    run  jq.test:1575  try trim catch ., try ltrim catch ., try rtrim catch .
    run  jq.test:1581  indices(1)
    run  jq.test:1585  indices([1,2])
    run  jq.test:1589  indices([1,2])
    run  jq.test:1593  indices(", ")
    run  jq.test:1597  index("!")
    run  jq.test:1601  .[:rindex("x")]
    run  jq.test:1605  indices("o")
    run  jq.test:1609  indices("o")
    run  jq.test:1613  [.[]|split(",")]
    run  jq.test:1617  [.[]|split(", ")]
    run  jq.test:1621  [.[] * 3]
    run  jq.test:1625  [.[] * "abc"]
    run  jq.test:1629  [. * (nan,-nan)]
    run  jq.test:1633  . * 100000 | [.[:10],.[-10:]]
    run  jq.test:1637  . * 1000000000
    run  jq.test:1641  try (. * 1000000000) catch .
    run  jq.test:1645  [.[] / ","]
    run  jq.test:1649  [.[] / ", "]
    run  jq.test:1653  map(.[1] as $needle | .[0] | contains($needle))
    run  jq.test:1657  map(.[1] as $needle | .[0] | contains($needle))
    run  jq.test:1661  [({foo: 12, bar:13} | contains({foo: 12})), ({foo: 12} | contains({})), ({foo: 12, bar:13} | contains({baz:14}))]
    run  jq.test:1665  {foo: {baz: 12, blap: {bar: 13}}, bar: 14} | contains({bar: 14, foo: {blap: {}}})
    run  jq.test:1669  {foo: {baz: 12, blap: {bar: 13}}, bar: 14} | contains({bar: 14, foo: {blap: {bar: 14}}})
    run  jq.test:1673  sort
    run  jq.test:1677  (sort_by(.b) | sort_by(.a)), sort_by(.a, .b), sort_by(.b, .c), group_by(.b), group_by(.a + .b - .c == 2)
    run  jq.test:1685  unique
    run  jq.test:1689  unique
    run  jq.test:1693  [min, max, min_by(.[1]), max_by(.[1]), min_by(.[2]), max_by(.[2])]
    run  jq.test:1697  [min,max,min_by(.),max_by(.)]
    run  jq.test:1701  .foo[.baz]
    run  jq.test:1705  .[] | .error = "no, it's OK"
    run  jq.test:1709  [{a:1}] | .[] | .a=999
    run  jq.test:1713  to_entries
    run  jq.test:1717  from_entries
    run  jq.test:1721  with_entries(.key |= "KEY_" + .)
    run  jq.test:1725  map(has("foo"))
    run  jq.test:1729  map(has(2))
    run  jq.test:1733  has(nan)
    run  jq.test:1737  keys
    run  jq.test:1741  [][.]
    run  jq.test:1745  map([1,2][0:.])
    run  jq.test:1751  {"k": {"a": 1, "b": 2}} * .
    run  jq.test:1755  {"k": {"a": 1, "b": 2}, "hello": {"x": 1}} * .
    run  jq.test:1759  {"k": {"a": 1, "b": 2}, "hello": 1} * .
    run  jq.test:1763  {"a": {"b": 1}, "c": {"d": 2}, "e": 5} * .
    run  jq.test:1767  [.[]|arrays]
    run  jq.test:1771  [.[]|objects]
    run  jq.test:1775  [.[]|iterables]
    run  jq.test:1779  [.[]|scalars]
    run  jq.test:1783  [.[]|values]
    run  jq.test:1787  [.[]|booleans]
    run  jq.test:1791  [.[]|nulls]
    run  jq.test:1795  flatten
    run  jq.test:1799  flatten(0)
    run  jq.test:1803  flatten(2)
    run  jq.test:1807  flatten(2)
    run  jq.test:1811  try flatten(-1) catch .
    run  jq.test:1815  transpose
    run  jq.test:1819  transpose
    run  jq.test:1823  ascii_upcase
    run  jq.test:1827  bsearch(0,1,2,3,4)
    run  jq.test:1835  bsearch({x:1})
    run  jq.test:1839  try ["OK", bsearch(0)] catch ["KO",.]
    run  jq.test:1843  strftime("%Y-%m-%dT%H:%M:%SZ")
    run  jq.test:1847  strftime("%A, %B %d, %Y")
    run  jq.test:1851  strftime("%Y-%m-%dT%H:%M:%SZ")
    run  jq.test:1855  mktime
    run  jq.test:1859  gmtime
    run  jq.test:1863  gmtime[5]
    run  jq.test:1868  try strftime("%Y-%m-%dT%H:%M:%SZ") catch .
    run  jq.test:1872  try strflocaltime("%Y-%m-%dT%H:%M:%SZ") catch .
    run  jq.test:1876  try mktime catch .
    run  jq.test:1881  try ["OK", strftime([])] catch ["KO", .]
    run  jq.test:1885  try ["OK", strflocaltime({})] catch ["KO", .]
    run  jq.test:1889  [strptime("%Y-%m-%dT%H:%M:%SZ")|(.,mktime)]
    run  jq.test:1895  last(range(365 * 67)|("1970-03-01T01:02:03Z"|strptime("%Y-%m-%dT%H:%M:%SZ")|mktime) + (86400 * .)|strftime("%Y-%m-%dT%H:%M:%SZ")|strptime("%Y-%m-%dT%H:%M:%SZ"))
    skip jq.test:1900  import "a" as foo; import "b" as bar; def fooa: foo::a; [fooa, bar::a, bar::b, foo::a]
    skip jq.test:1904  import "c" as foo; [foo::a, foo::c]
    skip jq.test:1908  include "c"; [a, c]
    skip jq.test:1912  import "data" as $e; import "data" as $d; [$d[].this,$e[].that,$d::d[].this,$e::e[].that]|join(";")
    skip jq.test:1917  import "data" as $a; import "data" as $b; def f: {$a, $b}; f
    skip jq.test:1921  include "shadow1"; e
    skip jq.test:1925  include "shadow1"; include "shadow2"; e
    skip jq.test:1929  import "shadow1" as f; import "shadow2" as f; import "shadow1" as e; [e::e, f::e]
    run  jq.test:1934  module (.+1); 0
    run  jq.test:1940  module []; 0
    run  jq.test:1946  include "a" (.+1); 0
    run  jq.test:1952  include "a" []; 0
    run  jq.test:1958  include "\ "; 0
    run  jq.test:1964  include "\(a)"; 0
    skip jq.test:1969  modulemeta
    skip jq.test:1973  modulemeta | .deps | length
    skip jq.test:1977  modulemeta | .defs | length
    skip jq.test:1982  import "syntaxerror" as e; .
    run  jq.test:1988  %::wat
    skip jq.test:1993  import "test_bind_order" as check; check::check
    run  jq.test:1997  try -. catch .
    run  jq.test:2001  try (.-.) catch .
    run  jq.test:2005  "x" * range(0; 12; 2) + "☆" * 8 | try -. catch .
    run  jq.test:2014  try (. + "x") catch . == if have_decnum then "number (12345678901234567890123456...) and string (\"x\") cannot be added" else "number (12345678901234568000000000...) and string (\"x\") cannot be added" end
    run  jq.test:2018  join(",")
    run  jq.test:2022  .[] | join(",")
    run  jq.test:2029  .[] | join(",")
    run  jq.test:2034  try join(",") catch .
    run  jq.test:2038  try join(",") catch .
    run  jq.test:2042  {if:0,and:1,or:2,then:3,else:4,elif:5,end:6,as:7,def:8,reduce:9,foreach:10,try:11,catch:12,label:13,import:14,include:15,module:16}
    run  jq.test:2046  try (1/.) catch .
    run  jq.test:2050  try (1/0) catch .
    run  jq.test:2054  try (0/0) catch .
    run  jq.test:2058  try (1%.) catch .
    run  jq.test:2062  try (1%0) catch .
    run  jq.test:2067  [range(-52;52;1)] as $powers | [$powers[]|pow(2;.)|log2|round] == $powers
    run  jq.test:2071  [range(-99/2;99/2;1)] as $orig | [$orig[]|pow(2;.)|log2] as $back | ($orig|keys)[]|. as $k | (($orig|.[$k])-($back|.[$k]))|if . < 0 then . * -1 else . end|select(.>.00005)
    run  jq.test:2075  {
    run  jq.test:2081  }
    run  jq.test:2086  (.[{}] = 0)?
    run  jq.test:2089  INDEX(range(5)|[., "foo\(.)"]; .[0])
    run  jq.test:2093  JOIN({"0":[0,"abc"],"1":[1,"bcd"],"2":[2,"def"],"3":[3,"efg"],"4":[4,"fgh"]}; .[0]|tostring)
    run  jq.test:2097  range(5;10)|IN(range(10))
    run  jq.test:2105  range(5;13)|IN(range(0;10;3))
    run  jq.test:2116  range(10;12)|IN(range(10))
    run  jq.test:2121  IN(range(10;20); range(10))
    run  jq.test:2125  IN(range(5;20); range(10))
    run  jq.test:2130  (.a as $x | .b) = "b"
    run  jq.test:2135  (.. | select(type == "object" and has("b") and (.b | type) == "array")|.b) |= .[0]
    run  jq.test:2139  isempty(empty)
    run  jq.test:2143  isempty(range(3))
    run  jq.test:2147  isempty(1,error("foo"))
    run  jq.test:2152  index("")
    run  jq.test:2157  builtins|length > 10
    run  jq.test:2161  "-1"|IN(builtins[] / "/"|.[1])
    run  jq.test:2165  all(builtins[] / "/"; .[1]|tonumber >= 0)
    run  jq.test:2169  builtins|any(.[:1] == "_")
    run  jq.test:2190  map(. == 1)
    run  jq.test:2196  .[0] | tostring | . == if have_decnum then "13911860366432393" else "13911860366432392" end
    run  jq.test:2200  .x | tojson | . == if have_decnum then "13911860366432393" else "13911860366432392" end
    run  jq.test:2204  (13911860366432393 == 13911860366432392) | . == if have_decnum then false else true end
    run  jq.test:2211  . - 10
    run  jq.test:2215  .[0] - 10
    run  jq.test:2219  .x - 10
    run  jq.test:2224  -. | tojson == if have_decnum then "-13911860366432393" else "-13911860366432392" end
    run  jq.test:2228  -. | tojson == if have_decnum then "0.12345678901234567890123456789" else "0.12345678901234568" end
    run  jq.test:2232  [1E+1000,-1E+1000 | tojson] == if have_decnum then ["1E+1000","-1E+1000"] else ["1.7976931348623157e+308","-1.7976931348623157e+308"] end
    run  jq.test:2236  . |= try . catch .
    run  jq.test:2241  .[] as $n | $n+0 | [., tostring, . == $n]
    run  jq.test:2250  abs
    run  jq.test:2254  map(abs)
    run  jq.test:2258  map(fabs)
    run  jq.test:2262  map(abs == length) | unique
    run  jq.test:2267  map(abs)
    run  jq.test:2271  [1E+1000,-1E+1000 | abs | tojson] | unique == if have_decnum then ["1E+1000"] else ["1.7976931348623157e+308"] end
    run  jq.test:2275  [1E+1000,-1E+1000 | length | tojson] | unique == if have_decnum then ["1E+1000"] else ["1.7976931348623157e+308"] end
    run  jq.test:2281  123 as $label | $label
    run  jq.test:2285  [ label $if | range(10) | ., (select(. == 5) | break $if) ]
    run  jq.test:2289  reduce .[] as $then (4 as $else | $else; . as $elif | . + $then * $elif)
    run  jq.test:2293  1 as $foreach | 2 as $and | 3 as $or | { $foreach, $and, $or, a }
    run  jq.test:2297  [ foreach .[] as $try (1 as $catch | $catch - 1; . + $try; .) ]
    run  jq.test:2304  { a, $__loc__, c }
    run  jq.test:2308  1 as $x | "2" as $y | "3" as $z | { $x, as, $y: 4, ($z): 5, if: 6, foo: 7 }
    run  jq.test:2315  fromjson | isnan
    run  jq.test:2319  tojson | fromjson
    run  jq.test:2324  .[] | try (fromjson | isnan) catch .
    run  jq.test:2337  try input catch .
    run  jq.test:2341  debug
    run  jq.test:2346  "foo" | try ((try . catch "caught too much") | error) catch "caught just right"
    run  jq.test:2350  .[]|(try (if .=="hi" then . else error end) catch empty) | "\(.) there!"
    run  jq.test:2354  try (["hi","ho"]|.[]|(try . catch (if .=="ho" then "BROKEN"|error else empty end)) | if .=="ho" then error else "\(.) there!" end) catch "caught outside \(.)"
    run  jq.test:2359  .[]|(try . catch (if .=="ho" then "BROKEN"|error else empty end)) | if .=="ho" then error else "\(.) there!" end
    run  jq.test:2363  try (try error catch "inner catch \(.)") catch "outer catch \(.)"
    run  jq.test:2367  try ((try error catch "inner catch \(.)")|error) catch "outer catch \(.)"
    run  jq.test:2372  first(.?,.?)
    run  jq.test:2377  {foo: "bar"} | .foo |= .?
    run  jq.test:2382  . |= try 2
    run  jq.test:2386  . |= try 2 catch 3
    run  jq.test:2390  .[] |= try tonumber
    run  jq.test:2395  any(keys[]|tostring?;true)
    run  jq.test:2403  implode|explode
    run  jq.test:2407  map(try implode catch .)
    run  jq.test:2411  try 0[implode] catch .
    run  jq.test:2416  walk(.)
    run  jq.test:2420  walk(1)
    run  jq.test:2425  [walk(.,1)]
    run  jq.test:2430  walk(select(IN({}, []) | not))
    run  jq.test:2435  [range(10)] | .[1.2:3.5]
    run  jq.test:2439  [range(10)] | .[1.5:3.5]
    run  jq.test:2443  [range(10)] | .[1.7:3.5]
    run  jq.test:2447  [range(10)] | .[1.7:4294967295]
    run  jq.test:2451  [range(10)] | .[1.7:-4294967296]
    run  jq.test:2455  [[range(10)] | .[1.1,1.5,1.7]]
    run  jq.test:2459  [range(5)] | .[1.1] = 5
    run  jq.test:2463  [range(3)] | .[nan:1]
    run  jq.test:2467  [range(3)] | .[1:nan]
    run  jq.test:2471  [range(3)] | .[nan]
    run  jq.test:2475  try ([range(3)] | .[nan] = 9) catch .
    run  jq.test:2479  try ("foobar" | .[1.5:3.5] = "xyz") catch .
    run  jq.test:2483  try ([range(10)] | .[1.5:3.5] = ["xyz"]) catch .
    run  jq.test:2487  try ("foobar" | .[1.5]) catch .
    run  jq.test:2494  try ["ok", setpath([1]; 1)] catch ["ko", .]
    run  jq.test:2498  try fromjson catch .
    run  jq.test:2504  try ltrimstr(1) catch "x", try rtrimstr(1) catch "x" | "ok"
    run  jq.test:2509  try ltrimstr("x") catch "x", try rtrimstr("x") catch "x" | "ok"
    run  jq.test:2516  .[] as [$x, $y] | try ["ok", ($x | ltrimstr($y))] catch ["ko", .]
    run  jq.test:2523  .[] as [$x, $y] | try ["ok", ($x | rtrimstr($y))] catch ["ko", .]
    run  jq.test:2533  try ["OK", setpath([[1]]; 1)] catch ["KO", .]
    run  jq.test:2538  foreach .[] as $x (0, 1; . + $x)
    run  jq.test:2548  strflocaltime("" | ., @uri)
    run  jq.test:2558  reduce range(9999) as $_ ([];[.]) | tojson | fromjson | flatten
    run  jq.test:2563  reduce range(10000) as $_ ([];[.]) | tojson | try (fromjson) catch . | (contains("<skipped: too deep>") | not) and contains("Exceeds depth limit for parsing")
    run  jq.test:2568  reduce range(10001) as $_ ([];[.]) | tojson | contains("<skipped: too deep>")
    run  jq.test:2573  setpath([range(10000) | 0]; 0) | flatten
    run  jq.test:2577  try setpath([range(10001) | 0]; 0) catch .
    run  jq.test:2581  getpath([range(10000) | 0])
    run  jq.test:2585  try getpath([range(10001) | 0]) catch .
    run  jq.test:2589  delpaths([[range(10000) | 0]])
    run  jq.test:2593  try delpaths([[range(10001) | 0]]) catch .
    run  jq.test:2598  reduce range(10000) as $_ ([]; [.]) | contains([[]])
    run  jq.test:2602  try (reduce range(10001) as $_ ([]; [.]) as $x | $x | contains($x)) catch .
    run  jq.test:2607  reduce range(10000) as $_ ({}; {a: .}) as $x | $x * $x | length
    run  jq.test:2611  try (reduce range(10001) as $_ ({}; {a: .}) as $x | $x * $x) catch .
    run  jq.test:2616  try ((reduce range(10001) as $_ ([]; [.])) as $x | (reduce range(10001) as $_ ([]; [.])) as $y | $x == $y) catch .
    run  jq.test:2621  try ((reduce range(10001) as $_ ([]; [.])) as $x | [$x, $x] | sort) catch .
    run  jq.test:2625  try ((reduce range(10001) as $_ ([]; [.])) as $x | [$x, $x] | unique) catch .
    run  jq.test:2629  try ((reduce range(10001) as $_ ({}; {a: .})) as $x | [$x, $x] | sort) catch .
    run  jq.test:2633  try ((reduce range(10001) as $_ ({}; {a: .})) as $x | [$x, $x] | unique) catch .
    
    550 cases, 13 excluded

## Post-build programmatic acceptance
- PASS: conformance-staging-list (FEATURE-Conformance-Staging.md)
  intent: The staged conformance harness parses and enumerates its corpus successfully without executing cases.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
  stdout:
    run  jq.test:8  true
    run  jq.test:12  false
    run  jq.test:16  null
    run  jq.test:20  1
    run  jq.test:25  -1
    run  jq.test:31  {}
    run  jq.test:35  []
    run  jq.test:39  {x:-1},{x:-.},{x:-.|abs}
    run  jq.test:48  .
    run  jq.test:54  "Aa\r\n\t\b\f\u03bc"
    run  jq.test:58  .
    run  jq.test:63  "u\vw"
    run  jq.test:68  "inter\("pol" + "ation")"
    run  jq.test:72  @text,@json,([1,.]|@csv,@tsv),@html,(@uri|.,@urid),@sh,(@base64|.,@base64d)
    run  jq.test:86  @base64
    run  jq.test:90  @base64d
    run  jq.test:94  @uri
    run  jq.test:98  @urid
    run  jq.test:102  @html "<b>\(.)</b>"
    run  jq.test:106  [.[]|tojson|fromjson]
    run  jq.test:114  {a: 1}
    run  jq.test:118  {a,b,(.d):.a,e:.b}
    run  jq.test:122  {"a",b,"a$\(1+1)"}
    run  jq.test:127  {(0):1}
    run  jq.test:133  {1+2:3}
    run  jq.test:139  {non_const:., (0):1}
    run  jq.test:148  .foo
    run  jq.test:152  .foo | .bar
    run  jq.test:156  .foo.bar
    run  jq.test:160  .foo_bar
    run  jq.test:164  .["foo"].bar
    run  jq.test:168  ."foo"."bar"
    run  jq.test:172  .e0, .E1, .E-1, .E+1
    run  jq.test:179  [.[]|.foo?]
    run  jq.test:183  [.[]|.foo?.bar?]
    run  jq.test:187  [..]
    run  jq.test:191  [.[]|.[]?]
    run  jq.test:195  [.[]|.[1:3]?]
    run  jq.test:200  map(try .a[] catch ., try .a.[] catch ., .a[]?, .a.[]?)
    run  jq.test:205  try ["OK", (.[] | error)] catch ["KO", .]
    run  jq.test:213  try (.foo[-1] = 0) catch .
    run  jq.test:217  try (.foo[-2] = 0) catch .
    run  jq.test:221  .[-1] = 5
    run  jq.test:225  .[-2] = 5
    run  jq.test:229  try (.[999999999] = 0) catch .
    run  jq.test:237  .[]
    run  jq.test:243  1,1
    run  jq.test:248  1,.
    run  jq.test:253  [.]
    run  jq.test:257  [[2]]
    run  jq.test:261  [{}]
    run  jq.test:265  [.[]]
    run  jq.test:269  [(.,1),((.,.[]),(2,3))]
    run  jq.test:273  [([5,5][]),.,.[]]
    run  jq.test:277  {x: (1,2)},{x:3} | .x
    run  jq.test:283  [.[-4,-3,-2,-1,0,1,2,3]]
    run  jq.test:287  [range(0;10)]
    run  jq.test:291  [range(0,1;3,4)]
    run  jq.test:295  [range(0;10;3)]
    run  jq.test:299  [range(0;10;-1)]
    run  jq.test:303  [range(0;-5;-1)]
    run  jq.test:307  [range(0,1;4,5;1,2)]
    run  jq.test:311  [while(.<100; .*2)]
    run  jq.test:315  [(label $here | .[] | if .>1 then break $here else . end), "hi!"]
    run  jq.test:319  [(label $here | .[] | if .>1 then break $here else . end), "hi!"]
    run  jq.test:324  . as $foo | break $foo
    run  jq.test:329  [.[]|[.,1]|until(.[0] < 1; [.[0] - 1, .[1] * .[0]])|.[1]]
    run  jq.test:333  [label $out | foreach .[] as $item ([3, null]; if .[0] < 1 then break $out else [.[0] -1, $item] end; .[1])]
    run  jq.test:337  [foreach range(5) as $item (0; $item)]
    run  jq.test:341  [foreach .[] as [$i, $j] (0; . + $i - $j)]
    run  jq.test:345  [foreach .[] as {a:$a} (0; . + $a; -.)]
    run  jq.test:349  [-foreach -.[] as $x (0; . + $x)]
    run  jq.test:353  [foreach .[] / .[] as $i (0; . + $i)]
    run  jq.test:357  [foreach .[] as $x (0; . + $x) as $x | $x]
    run  jq.test:361  [limit(3; .[])]
    run  jq.test:365  [limit(0; error)]
    run  jq.test:369  [limit(1; 1, error)]
    run  jq.test:373  try limit(-1; error) catch .
    run  jq.test:377  [skip(3; .[])]
    run  jq.test:381  [skip(0,2,3,4; .[])]
    run  jq.test:385  [skip(3; .[])]
    run  jq.test:389  try skip(-1; error) catch .
    run  jq.test:393  nth(1; 0,1,error("foo"))
    run  jq.test:397  [first(range(.)), last(range(.))]
    run  jq.test:401  [first(range(.)), last(range(.))]
    run  jq.test:405  [nth(0,5,9,10,15; range(.)), try nth(-1; range(.)) catch .]
    run  jq.test:410  first(1,error("foo"))
    run  jq.test:420  [limit(5,7; range(9))]
    run  jq.test:425  [nth(5,7; range(9;0;-1))]
    run  jq.test:430  [range(0,1,2;4,3,2;2,3)]
    run  jq.test:435  [range(3,5)]
    run  jq.test:440  [(index(",","|"), rindex(",","|")), indices(",","|")]
    run  jq.test:445  join(",","/")
    run  jq.test:450  [.[]|join("a")]
    run  jq.test:455  flatten(3,2,1)
    run  jq.test:466  [.[3:2], .[-5:4], .[:-2], .[-2:], .[3:3][1:], .[10:]]
    run  jq.test:470  [.[3:2], .[-5:4], .[:-2], .[-2:], .[3:3][1:], .[10:]]
    run  jq.test:474  del(.[2:4],.[0],.[-2:])
    run  jq.test:478  .[2:4] = ([], ["a","b"], ["a","b","c"])
    run  jq.test:490  reduce range(65540;65536;-1) as $i ([]; .[$i] = $i)|.[65536:]
    run  jq.test:498  1 as $x | 2 as $y | [$x,$y,$x]
    run  jq.test:502  [1,2,3][] as $x | [[4,5,6,7][$x]]
    run  jq.test:508  42 as $x | . | . | . + 432 | $x + 1
    run  jq.test:512  1 + 2 as $x | -$x
    run  jq.test:516  "x" as $x | "a"+"y" as $y | $x+","+$y
    run  jq.test:520  1 as $x | [$x,$x,$x as $x | $x]
    run  jq.test:524  [1, {c:3, d:4}] as [$a, {c:$b, b:$c}] | $a, $b, $c
    run  jq.test:530  . as {as: $kw, "str": $str, ("e"+"x"+"p"): $exp} | [$kw, $str, $exp]
    run  jq.test:534  .[] as [$a, $b] | [$b, $a]
    run  jq.test:539  . as $i | . as [$i] | $i
    run  jq.test:543  . as [$i] | . as $i | $i
    run  jq.test:548  . as [] | null
    run  jq.test:554  . as {} | null
    run  jq.test:560  . as $foo | [$foo, $bar]
    run  jq.test:566  . as {(true):$foo} | $foo
    run  jq.test:577  1+1
    run  jq.test:581  1+1
    run  jq.test:585  2-1
    run  jq.test:589  2-(-1)
    run  jq.test:593  1e+0+0.001e3
    run  jq.test:597  .+4
    run  jq.test:601  .+null
    run  jq.test:605  null+.
    run  jq.test:609  .a+.b
    run  jq.test:613  [1,2,3] + [.]
    run  jq.test:617  {"a":1} + {"b":2} + {"c":3}
    run  jq.test:621  "asdf" + "jkl;" + . + . + .
    run  jq.test:625  "\u0000\u0020\u0000" + .
    run  jq.test:629  42 - .
    run  jq.test:633  [1,2,3,4,1] - [.,3]
    run  jq.test:637  [-1 as $x | 1,$x]
    run  jq.test:641  [10 * 20, 20 / .]
    run  jq.test:645  1 + 2 * 2 + 10 / 2
    run  jq.test:649  [16 / 4 / 2, 16 / 4 * 2, 16 - 4 - 2, 16 - 4 + 2]
    run  jq.test:653  1e-19 + 1e-20 - 5e-21
    run  jq.test:657  1 / 1e-17
    run  jq.test:661  9E999999999, 9999999999E999999990, 1E-999999999, 0.000000001E-999999990
    run  jq.test:668  5E500000000 > 5E-5000000000, 10000E500000000 > 10000E-5000000000
    run  jq.test:674  (1e999999999, 10e999999999) > (1e-1147483646, 0.1e-1147483646)
    run  jq.test:681  25 % 7
    run  jq.test:685  49732 % 472
    run  jq.test:689  [(infinite, -infinite) % (1, -1, infinite)]
    run  jq.test:693  [nan % 1, 1 % nan | isnan]
    run  jq.test:697  1 + tonumber + ("10" | tonumber)
    run  jq.test:701  "123\u0000456" | try tonumber catch .
    run  jq.test:705  map(toboolean)
    run  jq.test:709  .[] | try toboolean catch .
    run  jq.test:720  "true\u0000x", "false\u0000" | try toboolean catch .
    run  jq.test:725  [{"a":42},.object,10,.num,false,true,null,"b",[1,4]] | .[] as $x | [$x == .[]]
    run  jq.test:737  [.[] | length]
    run  jq.test:741  utf8bytelength
    run  jq.test:745  [.[] | try utf8bytelength catch .]
    run  jq.test:750  map(keys)
    run  jq.test:754  [1,2,empty,3,empty,4]
    run  jq.test:758  map(add)
    run  jq.test:762  map_values(.+1)
    run  jq.test:766  [add(null), add(range(range(10))), add(empty), add(10,range(10))]
    run  jq.test:771  .sum = add(.arr[])
    run  jq.test:775  add({(.[]):1}) | keys
    run  jq.test:784  def f: . + 1; def g: def g: . + 100; f | g | f; (f | g), g
    run  jq.test:789  def f: (1000,2000); f
    run  jq.test:794  def f(a;b;c;d;e;f): [a+1,b,c,d,e,f]; f(.[0];.[1];.[0];.[0];.[0];.[0])
    run  jq.test:798  def f: 1; def g: f, def f: 2; def g: 3; f, def f: g; f, g; def f: 4; [f, def f: g; def g: 5; f, g]+[f,g]
    run  jq.test:803  def a: 0; . | a
    run  jq.test:808  def f(a;b;c;d;e;f;g;h;i;j): [j,i,h,g,f,e,d,c,b,a]; f(.[0];.[1];.[2];.[3];.[4];.[5];.[6];.[7];.[8];.[9])
    run  jq.test:812  ([1,2] + [4,5])
    run  jq.test:816  true
    run  jq.test:820  null,1,null
    run  jq.test:826  [1,2,3]
    run  jq.test:830  [.[]|floor]
    run  jq.test:834  [.[]|sqrt]
    run  jq.test:838  (add / length) as $m | map((. - $m) as $d | $d * $d) | add / length | sqrt
    run  jq.test:847  atan * 4 * 1000000|floor / 1000000
    run  jq.test:851  [(3.141592 / 2) * (range(0;20) / 20)|cos * 1000000|floor / 1000000]
    run  jq.test:855  [(3.141592 / 2) * (range(0;20) / 20)|sin * 1000000|floor / 1000000]
    run  jq.test:860  def f(x): x | x; f([.], . + [42])
    run  jq.test:868  def f: .+1; def g: f; def f: .+100; def f(a):a+.+11; [(g|f(20)), f]
    run  jq.test:873  def id(x):x; 2000 as $x | def f(x):1 as $x | id([$x, x, x]); def g(x): 100 as $x | f($x,$x+x); g($x)
    run  jq.test:878  def x(a;b): a as $a | b as $b | $a + $b; def y($a;$b): $a + $b; def check(a;b): [x(a;b)] == [y(a;b)]; check(.[];.[]*2)
    run  jq.test:884  [[20,10][1,0] as $x | def f: (100,200) as $y | def g: [$x + $y, .]; . + $x | g; f[0] | [f][0][1] | f]
    run  jq.test:889  def fac: if . == 1 then 1 else . * (. - 1 | fac) end; [.[] | fac]
    run  jq.test:899  reduce .[] as $x (0; . + $x)
    run  jq.test:903  reduce .[] as [$i, {j:$j}] (0; . + $i - $j)
    run  jq.test:907  reduce [[1,2,10], [3,4,10]][] as [$i,$j] (0; . + $i * $j)
    run  jq.test:911  [-reduce -.[] as $x (0; . + $x)]
    run  jq.test:915  [reduce .[] / .[] as $i (0; . + $i)]
    run  jq.test:919  reduce .[] as $x (0; . + $x) as $x | $x
    run  jq.test:924  reduce . as $n (.; .)
    run  jq.test:929  . as {$a, b: [$c, {$d}]} | [$a, $c, $d]
    run  jq.test:933  . as {$a, $b:[$c, $d]}| [$a, $b, $c, $d]
    run  jq.test:938  .[] | . as {$a, b: [$c, {$d}]} ?// [$a, {$b}, $e] ?// $f | [$a, $b, $c, $d, $e, $f]
    run  jq.test:945  .[] | . as {a:$a} ?// {a:$a} ?// {a:$a} | $a
    run  jq.test:949  .[] as {a:$a} ?// {a:$a} ?// {a:$a} | $a
    run  jq.test:953  [[3],[4],[5],6][] | . as {a:$a} ?// {a:$a} ?// {a:$a} | $a
    run  jq.test:957  [[3],[4],[5],6] | .[] as {a:$a} ?// {a:$a} ?// {a:$a} | $a
    run  jq.test:961  .[] | . as {a:$a} ?// {a:$a} ?// $a | $a
    run  jq.test:968  .[] as {a:$a} ?// {a:$a} ?// $a | $a
    run  jq.test:975  [[3],[4],[5],6][] | . as {a:$a} ?// {a:$a} ?// $a | $a
    run  jq.test:982  [[3],[4],[5],6] | .[] as {a:$a} ?// {a:$a} ?// $a | $a
    run  jq.test:989  .[] | . as {a:$a} ?// $a ?// {a:$a} | $a
    run  jq.test:996  .[] as {a:$a} ?// $a ?// {a:$a} | $a
    run  jq.test:1003  [[3],[4],[5],6][] | . as {a:$a} ?// $a ?// {a:$a} | $a
    run  jq.test:1010  [[3],[4],[5],6] | .[] as {a:$a} ?// $a ?// {a:$a} | $a
    run  jq.test:1017  .[] | . as $a ?// {a:$a} ?// {a:$a} | $a
    run  jq.test:1024  .[] as $a ?// {a:$a} ?// {a:$a} | $a
    run  jq.test:1031  [[3],[4],[5],6][] | . as $a ?// {a:$a} ?// {a:$a} | $a
    run  jq.test:1038  [[3],[4],[5],6] | .[] as $a ?// {a:$a} ?// {a:$a} | $a
    run  jq.test:1045  . as $dot|any($dot[];not)
    run  jq.test:1049  . as $dot|any($dot[];not)
    run  jq.test:1053  . as $dot|all($dot[];.)
    run  jq.test:1057  . as $dot|all($dot[];.)
    run  jq.test:1062  any(true, error; .)
    run  jq.test:1066  all(false, error; .)
    run  jq.test:1070  any(not)
    run  jq.test:1074  all(not)
    run  jq.test:1078  any(not)
    run  jq.test:1082  all(not)
    run  jq.test:1086  [any,all]
    run  jq.test:1090  [any,all]
    run  jq.test:1094  [any,all]
    run  jq.test:1098  [any,all]
    run  jq.test:1102  [any,all]
    run  jq.test:1110  path(.foo[0,1])
    run  jq.test:1115  path(.[] | select(.>3))
    run  jq.test:1119  path(.)
    run  jq.test:1123  try path(.a | map(select(.b == 0))) catch .
    run  jq.test:1127  try path(.a | map(select(.b == 0)) | .[0]) catch .
    run  jq.test:1131  try path(.a | map(select(.b == 0)) | .c) catch .
    run  jq.test:1135  try path(.a | map(select(.b == 0)) | .[]) catch .
    run  jq.test:1139  path(.a[path(.b)[0]])
    run  jq.test:1143  [paths]
    run  jq.test:1147  ["foo",1] as $p | getpath($p), setpath($p; 20), delpaths([$p])
    run  jq.test:1153  map(getpath([2])), map(setpath([2]; 42)), map(delpaths([[2]]))
    run  jq.test:1159  map(delpaths([[0,"foo"]]))
    run  jq.test:1163  ["foo",1] as $p | getpath($p), setpath($p; 20), delpaths([$p])
    run  jq.test:1169  delpaths([[-200]])
    run  jq.test:1173  try delpaths(0) catch .
    run  jq.test:1177  del(.), del(empty), del((.foo,.bar,.baz) | .[2,3,0]), del(.foo[0], .bar[0], .foo, .baz.bar[0].x)
    run  jq.test:1184  del(.[1], .[-6], .[2], .[-3:9])
    run  jq.test:1188  del(.[nan])
    run  jq.test:1192  del(.[nan,nan])
    run  jq.test:1197  setpath([-1]; 1)
    run  jq.test:1201  pick(.a.b.c)
    run  jq.test:1205  pick(first)
    run  jq.test:1209  pick(first|first)
    run  jq.test:1214  try pick(last) catch .
    run  jq.test:1221  .message = "goodbye"
    run  jq.test:1225  .foo = .bar
    run  jq.test:1229  .foo |= .+1
    run  jq.test:1233  .[] += 2, .[] *= 2, .[] -= 2, .[] /= 2, .[] %=2
    run  jq.test:1241  [.[] % 7]
    run  jq.test:1245  .foo += .foo
    run  jq.test:1249  .[0].a |= {"old":., "new":(.+1)}
    run  jq.test:1253  def inc(x): x |= .+1; inc(.[].a)
    run  jq.test:1258  .[] | try (getpath(["a",0,"b"]) |= 5) catch .
    run  jq.test:1270  (.[] | select(. >= 2)) |= empty
    run  jq.test:1274  .[] |= select(. % 2 == 0)
    run  jq.test:1278  .foo[1,4,2,3] |= empty
    run  jq.test:1282  .[2][3] = 1
    run  jq.test:1286  .foo[2].bar = 1
    run  jq.test:1290  try ((map(select(.a == 1))[].b) = 10) catch .
    run  jq.test:1294  try ((map(select(.a == 1))[].a) |= .+1) catch .
    run  jq.test:1298  def x: .[1,2]; x=10
    run  jq.test:1302  try (def x: reverse; x=10) catch .
    run  jq.test:1306  .[] = 1
    run  jq.test:1314  [.[] | if .foo then "yep" else "nope" end]
    run  jq.test:1318  [.[] | if .baz then "strange" elif .foo then "yep" else "nope" end]
    run  jq.test:1322  [if 1,null,2 then 3 else 4 end]
    run  jq.test:1326  [if empty then 3 else 4 end]
    run  jq.test:1330  [if 1 then 3,4 else 5 end]
    run  jq.test:1334  [if null then 3 else 5,6 end]
    run  jq.test:1338  [if true then 3 end]
    run  jq.test:1342  [if false then 3 end]
    run  jq.test:1346  [if false then 3 else . end]
    run  jq.test:1350  [if false then 3 elif false then 4 end]
    run  jq.test:1354  [if false then 3 elif false then 4 else . end]
    run  jq.test:1358  [-if true then 1 else 2 end]
    run  jq.test:1362  {x: if true then 1 else 2 end}
    run  jq.test:1366  if true then [.] else . end []
    run  jq.test:1370  [.[] | [.foo[] // .bar]]
    run  jq.test:1374  .[] //= .[0]
    run  jq.test:1378  .[] | [.[0] and .[1], .[0] or .[1]]
    run  jq.test:1385  [.[] | not]
    run  jq.test:1390  [10 > 0, 10 > 10, 10 > 20, 10 < 0, 10 < 10, 10 < 20]
    run  jq.test:1394  [10 >= 0, 10 >= 10, 10 >= 20, 10 <= 0, 10 <= 10, 10 <= 20]
    run  jq.test:1399  [ 10 == 10, 10 != 10, 10 != 11, 10 == 11]
    run  jq.test:1403  ["hello" == "hello", "hello" != "hello", "hello" == "world", "hello" != "world" ]
    run  jq.test:1407  [[1,2,3] == [1,2,3], [1,2,3] != [1,2,3], [1,2,3] == [4,5,6], [1,2,3] != [4,5,6]]
    run  jq.test:1411  [{"foo":42} == {"foo":42},{"foo":42} != {"foo":42}, {"foo":42} != {"bar":42}, {"foo":42} == {"bar":42}]
    run  jq.test:1416  [{"foo":[1,2,{"bar":18},"world"]} == {"foo":[1,2,{"bar":18},"world"]},{"foo":[1,2,{"bar":18},"world"]} == {"foo":[1,2,{"bar":19},"world"]}]
    run  jq.test:1421  [("foo" | contains("foo")), ("foobar" | contains("foo")), ("foo" | contains("foobar"))]
    run  jq.test:1426  [contains(""), contains("\u0000")]
    run  jq.test:1430  [contains(""), contains("a"), contains("ab"), contains("c"), contains("d")]
    run  jq.test:1434  [contains("cd"), contains("b\u0000"), contains("ab\u0000")]
    run  jq.test:1438  [contains("b\u0000c"), contains("b\u0000cd"), contains("b\u0000cd")]
    run  jq.test:1442  [contains("@"), contains("\u0000@"), contains("\u0000what")]
    run  jq.test:1448  [.[]|try if . == 0 then error("foo") elif . == 1 then .a elif . == 2 then empty else . end catch .]
    run  jq.test:1452  [.[]|(.a, .a)?]
    run  jq.test:1456  [[.[]|[.a,.a]]?]
    run  jq.test:1460  [if error then 1 else 2 end?]
    run  jq.test:1464  try error(0) // 1
    run  jq.test:1468  1, try error(2), 3
    run  jq.test:1473  1 + try 2 catch 3 + 4
    run  jq.test:1477  [-try .]
    run  jq.test:1481  try -.? catch .
    run  jq.test:1485  {x: try 1, y: try error catch 2, z: if true then 3 end}
    run  jq.test:1489  {x: 1 + 2, y: false or true, z: null // 3}
    run  jq.test:1493  .[] | try error catch .
    run  jq.test:1499  try error("\($__loc__)") catch .
    run  jq.test:1504  [.[]|startswith("foo")]
    run  jq.test:1508  [.[]|endswith("foo")]
    run  jq.test:1512  [.[] | split(", ")]
    run  jq.test:1516  split("")
    run  jq.test:1520  [.[]|ltrimstr("foo")]
    run  jq.test:1524  [.[]|rtrimstr("foo")]
    run  jq.test:1528  [.[]|trimstr("foo")]
    run  jq.test:1532  [.[]|ltrimstr("")]
    run  jq.test:1536  [.[]|rtrimstr("")]
    run  jq.test:1540  [.[]|trimstr("")]
    run  jq.test:1544  [(index(","), rindex(",")), indices(",")]
    run  jq.test:1548  [ index("aba"), rindex("aba"), indices("aba") ]
    run  jq.test:1553  try _strindices("abc") catch .
    run  jq.test:1557  try _strindices(123) catch .
    run  jq.test:1563  map(trim), map(ltrim), map(rtrim)
    run  jq.test:1569  trim, ltrim, rtrim
    run  jq.test:1575  try trim catch ., try ltrim catch ., try rtrim catch .
    run  jq.test:1581  indices(1)
    run  jq.test:1585  indices([1,2])
    run  jq.test:1589  indices([1,2])
    run  jq.test:1593  indices(", ")
    run  jq.test:1597  index("!")
    run  jq.test:1601  .[:rindex("x")]
    run  jq.test:1605  indices("o")
    run  jq.test:1609  indices("o")
    run  jq.test:1613  [.[]|split(",")]
    run  jq.test:1617  [.[]|split(", ")]
    run  jq.test:1621  [.[] * 3]
    run  jq.test:1625  [.[] * "abc"]
    run  jq.test:1629  [. * (nan,-nan)]
    run  jq.test:1633  . * 100000 | [.[:10],.[-10:]]
    run  jq.test:1637  . * 1000000000
    run  jq.test:1641  try (. * 1000000000) catch .
    run  jq.test:1645  [.[] / ","]
    run  jq.test:1649  [.[] / ", "]
    run  jq.test:1653  map(.[1] as $needle | .[0] | contains($needle))
    run  jq.test:1657  map(.[1] as $needle | .[0] | contains($needle))
    run  jq.test:1661  [({foo: 12, bar:13} | contains({foo: 12})), ({foo: 12} | contains({})), ({foo: 12, bar:13} | contains({baz:14}))]
    run  jq.test:1665  {foo: {baz: 12, blap: {bar: 13}}, bar: 14} | contains({bar: 14, foo: {blap: {}}})
    run  jq.test:1669  {foo: {baz: 12, blap: {bar: 13}}, bar: 14} | contains({bar: 14, foo: {blap: {bar: 14}}})
    run  jq.test:1673  sort
    run  jq.test:1677  (sort_by(.b) | sort_by(.a)), sort_by(.a, .b), sort_by(.b, .c), group_by(.b), group_by(.a + .b - .c == 2)
    run  jq.test:1685  unique
    run  jq.test:1689  unique
    run  jq.test:1693  [min, max, min_by(.[1]), max_by(.[1]), min_by(.[2]), max_by(.[2])]
    run  jq.test:1697  [min,max,min_by(.),max_by(.)]
    run  jq.test:1701  .foo[.baz]
    run  jq.test:1705  .[] | .error = "no, it's OK"
    run  jq.test:1709  [{a:1}] | .[] | .a=999
    run  jq.test:1713  to_entries
    run  jq.test:1717  from_entries
    run  jq.test:1721  with_entries(.key |= "KEY_" + .)
    run  jq.test:1725  map(has("foo"))
    run  jq.test:1729  map(has(2))
    run  jq.test:1733  has(nan)
    run  jq.test:1737  keys
    run  jq.test:1741  [][.]
    run  jq.test:1745  map([1,2][0:.])
    run  jq.test:1751  {"k": {"a": 1, "b": 2}} * .
    run  jq.test:1755  {"k": {"a": 1, "b": 2}, "hello": {"x": 1}} * .
    run  jq.test:1759  {"k": {"a": 1, "b": 2}, "hello": 1} * .
    run  jq.test:1763  {"a": {"b": 1}, "c": {"d": 2}, "e": 5} * .
    run  jq.test:1767  [.[]|arrays]
    run  jq.test:1771  [.[]|objects]
    run  jq.test:1775  [.[]|iterables]
    run  jq.test:1779  [.[]|scalars]
    run  jq.test:1783  [.[]|values]
    run  jq.test:1787  [.[]|booleans]
    run  jq.test:1791  [.[]|nulls]
    run  jq.test:1795  flatten
    run  jq.test:1799  flatten(0)
    run  jq.test:1803  flatten(2)
    run  jq.test:1807  flatten(2)
    run  jq.test:1811  try flatten(-1) catch .
    run  jq.test:1815  transpose
    run  jq.test:1819  transpose
    run  jq.test:1823  ascii_upcase
    run  jq.test:1827  bsearch(0,1,2,3,4)
    run  jq.test:1835  bsearch({x:1})
    run  jq.test:1839  try ["OK", bsearch(0)] catch ["KO",.]
    run  jq.test:1843  strftime("%Y-%m-%dT%H:%M:%SZ")
    run  jq.test:1847  strftime("%A, %B %d, %Y")
    run  jq.test:1851  strftime("%Y-%m-%dT%H:%M:%SZ")
    run  jq.test:1855  mktime
    run  jq.test:1859  gmtime
    run  jq.test:1863  gmtime[5]
    run  jq.test:1868  try strftime("%Y-%m-%dT%H:%M:%SZ") catch .
    run  jq.test:1872  try strflocaltime("%Y-%m-%dT%H:%M:%SZ") catch .
    run  jq.test:1876  try mktime catch .
    run  jq.test:1881  try ["OK", strftime([])] catch ["KO", .]
    run  jq.test:1885  try ["OK", strflocaltime({})] catch ["KO", .]
    run  jq.test:1889  [strptime("%Y-%m-%dT%H:%M:%SZ")|(.,mktime)]
    run  jq.test:1895  last(range(365 * 67)|("1970-03-01T01:02:03Z"|strptime("%Y-%m-%dT%H:%M:%SZ")|mktime) + (86400 * .)|strftime("%Y-%m-%dT%H:%M:%SZ")|strptime("%Y-%m-%dT%H:%M:%SZ"))
    skip jq.test:1900  import "a" as foo; import "b" as bar; def fooa: foo::a; [fooa, bar::a, bar::b, foo::a]
    skip jq.test:1904  import "c" as foo; [foo::a, foo::c]
    skip jq.test:1908  include "c"; [a, c]
    skip jq.test:1912  import "data" as $e; import "data" as $d; [$d[].this,$e[].that,$d::d[].this,$e::e[].that]|join(";")
    skip jq.test:1917  import "data" as $a; import "data" as $b; def f: {$a, $b}; f
    skip jq.test:1921  include "shadow1"; e
    skip jq.test:1925  include "shadow1"; include "shadow2"; e
    skip jq.test:1929  import "shadow1" as f; import "shadow2" as f; import "shadow1" as e; [e::e, f::e]
    run  jq.test:1934  module (.+1); 0
    run  jq.test:1940  module []; 0
    run  jq.test:1946  include "a" (.+1); 0
    run  jq.test:1952  include "a" []; 0
    run  jq.test:1958  include "\ "; 0
    run  jq.test:1964  include "\(a)"; 0
    skip jq.test:1969  modulemeta
    skip jq.test:1973  modulemeta | .deps | length
    skip jq.test:1977  modulemeta | .defs | length
    skip jq.test:1982  import "syntaxerror" as e; .
    run  jq.test:1988  %::wat
    skip jq.test:1993  import "test_bind_order" as check; check::check
    run  jq.test:1997  try -. catch .
    run  jq.test:2001  try (.-.) catch .
    run  jq.test:2005  "x" * range(0; 12; 2) + "☆" * 8 | try -. catch .
    run  jq.test:2014  try (. + "x") catch . == if have_decnum then "number (12345678901234567890123456...) and string (\"x\") cannot be added" else "number (12345678901234568000000000...) and string (\"x\") cannot be added" end
    run  jq.test:2018  join(",")
    run  jq.test:2022  .[] | join(",")
    run  jq.test:2029  .[] | join(",")
    run  jq.test:2034  try join(",") catch .
    run  jq.test:2038  try join(",") catch .
    run  jq.test:2042  {if:0,and:1,or:2,then:3,else:4,elif:5,end:6,as:7,def:8,reduce:9,foreach:10,try:11,catch:12,label:13,import:14,include:15,module:16}
    run  jq.test:2046  try (1/.) catch .
    run  jq.test:2050  try (1/0) catch .
    run  jq.test:2054  try (0/0) catch .
    run  jq.test:2058  try (1%.) catch .
    run  jq.test:2062  try (1%0) catch .
    run  jq.test:2067  [range(-52;52;1)] as $powers | [$powers[]|pow(2;.)|log2|round] == $powers
    run  jq.test:2071  [range(-99/2;99/2;1)] as $orig | [$orig[]|pow(2;.)|log2] as $back | ($orig|keys)[]|. as $k | (($orig|.[$k])-($back|.[$k]))|if . < 0 then . * -1 else . end|select(.>.00005)
    run  jq.test:2075  {
    run  jq.test:2081  }
    run  jq.test:2086  (.[{}] = 0)?
    run  jq.test:2089  INDEX(range(5)|[., "foo\(.)"]; .[0])
    run  jq.test:2093  JOIN({"0":[0,"abc"],"1":[1,"bcd"],"2":[2,"def"],"3":[3,"efg"],"4":[4,"fgh"]}; .[0]|tostring)
    run  jq.test:2097  range(5;10)|IN(range(10))
    run  jq.test:2105  range(5;13)|IN(range(0;10;3))
    run  jq.test:2116  range(10;12)|IN(range(10))
    run  jq.test:2121  IN(range(10;20); range(10))
    run  jq.test:2125  IN(range(5;20); range(10))
    run  jq.test:2130  (.a as $x | .b) = "b"
    run  jq.test:2135  (.. | select(type == "object" and has("b") and (.b | type) == "array")|.b) |= .[0]
    run  jq.test:2139  isempty(empty)
    run  jq.test:2143  isempty(range(3))
    run  jq.test:2147  isempty(1,error("foo"))
    run  jq.test:2152  index("")
    run  jq.test:2157  builtins|length > 10
    run  jq.test:2161  "-1"|IN(builtins[] / "/"|.[1])
    run  jq.test:2165  all(builtins[] / "/"; .[1]|tonumber >= 0)
    run  jq.test:2169  builtins|any(.[:1] == "_")
    run  jq.test:2190  map(. == 1)
    run  jq.test:2196  .[0] | tostring | . == if have_decnum then "13911860366432393" else "13911860366432392" end
    run  jq.test:2200  .x | tojson | . == if have_decnum then "13911860366432393" else "13911860366432392" end
    run  jq.test:2204  (13911860366432393 == 13911860366432392) | . == if have_decnum then false else true end
    run  jq.test:2211  . - 10
    run  jq.test:2215  .[0] - 10
    run  jq.test:2219  .x - 10
    run  jq.test:2224  -. | tojson == if have_decnum then "-13911860366432393" else "-13911860366432392" end
    run  jq.test:2228  -. | tojson == if have_decnum then "0.12345678901234567890123456789" else "0.12345678901234568" end
    run  jq.test:2232  [1E+1000,-1E+1000 | tojson] == if have_decnum then ["1E+1000","-1E+1000"] else ["1.7976931348623157e+308","-1.7976931348623157e+308"] end
    run  jq.test:2236  . |= try . catch .
    run  jq.test:2241  .[] as $n | $n+0 | [., tostring, . == $n]
    run  jq.test:2250  abs
    run  jq.test:2254  map(abs)
    run  jq.test:2258  map(fabs)
    run  jq.test:2262  map(abs == length) | unique
    run  jq.test:2267  map(abs)
    run  jq.test:2271  [1E+1000,-1E+1000 | abs | tojson] | unique == if have_decnum then ["1E+1000"] else ["1.7976931348623157e+308"] end
    run  jq.test:2275  [1E+1000,-1E+1000 | length | tojson] | unique == if have_decnum then ["1E+1000"] else ["1.7976931348623157e+308"] end
    run  jq.test:2281  123 as $label | $label
    run  jq.test:2285  [ label $if | range(10) | ., (select(. == 5) | break $if) ]
    run  jq.test:2289  reduce .[] as $then (4 as $else | $else; . as $elif | . + $then * $elif)
    run  jq.test:2293  1 as $foreach | 2 as $and | 3 as $or | { $foreach, $and, $or, a }
    run  jq.test:2297  [ foreach .[] as $try (1 as $catch | $catch - 1; . + $try; .) ]
    run  jq.test:2304  { a, $__loc__, c }
    run  jq.test:2308  1 as $x | "2" as $y | "3" as $z | { $x, as, $y: 4, ($z): 5, if: 6, foo: 7 }
    run  jq.test:2315  fromjson | isnan
    run  jq.test:2319  tojson | fromjson
    run  jq.test:2324  .[] | try (fromjson | isnan) catch .
    run  jq.test:2337  try input catch .
    run  jq.test:2341  debug
    run  jq.test:2346  "foo" | try ((try . catch "caught too much") | error) catch "caught just right"
    run  jq.test:2350  .[]|(try (if .=="hi" then . else error end) catch empty) | "\(.) there!"
    run  jq.test:2354  try (["hi","ho"]|.[]|(try . catch (if .=="ho" then "BROKEN"|error else empty end)) | if .=="ho" then error else "\(.) there!" end) catch "caught outside \(.)"
    run  jq.test:2359  .[]|(try . catch (if .=="ho" then "BROKEN"|error else empty end)) | if .=="ho" then error else "\(.) there!" end
    run  jq.test:2363  try (try error catch "inner catch \(.)") catch "outer catch \(.)"
    run  jq.test:2367  try ((try error catch "inner catch \(.)")|error) catch "outer catch \(.)"
    run  jq.test:2372  first(.?,.?)
    run  jq.test:2377  {foo: "bar"} | .foo |= .?
    run  jq.test:2382  . |= try 2
    run  jq.test:2386  . |= try 2 catch 3
    run  jq.test:2390  .[] |= try tonumber
    run  jq.test:2395  any(keys[]|tostring?;true)
    run  jq.test:2403  implode|explode
    run  jq.test:2407  map(try implode catch .)
    run  jq.test:2411  try 0[implode] catch .
    run  jq.test:2416  walk(.)
    run  jq.test:2420  walk(1)
    run  jq.test:2425  [walk(.,1)]
    run  jq.test:2430  walk(select(IN({}, []) | not))
    run  jq.test:2435  [range(10)] | .[1.2:3.5]
    run  jq.test:2439  [range(10)] | .[1.5:3.5]
    run  jq.test:2443  [range(10)] | .[1.7:3.5]
    run  jq.test:2447  [range(10)] | .[1.7:4294967295]
    run  jq.test:2451  [range(10)] | .[1.7:-4294967296]
    run  jq.test:2455  [[range(10)] | .[1.1,1.5,1.7]]
    run  jq.test:2459  [range(5)] | .[1.1] = 5
    run  jq.test:2463  [range(3)] | .[nan:1]
    run  jq.test:2467  [range(3)] | .[1:nan]
    run  jq.test:2471  [range(3)] | .[nan]
    run  jq.test:2475  try ([range(3)] | .[nan] = 9) catch .
    run  jq.test:2479  try ("foobar" | .[1.5:3.5] = "xyz") catch .
    run  jq.test:2483  try ([range(10)] | .[1.5:3.5] = ["xyz"]) catch .
    run  jq.test:2487  try ("foobar" | .[1.5]) catch .
    run  jq.test:2494  try ["ok", setpath([1]; 1)] catch ["ko", .]
    run  jq.test:2498  try fromjson catch .
    run  jq.test:2504  try ltrimstr(1) catch "x", try rtrimstr(1) catch "x" | "ok"
    run  jq.test:2509  try ltrimstr("x") catch "x", try rtrimstr("x") catch "x" | "ok"
    run  jq.test:2516  .[] as [$x, $y] | try ["ok", ($x | ltrimstr($y))] catch ["ko", .]
    run  jq.test:2523  .[] as [$x, $y] | try ["ok", ($x | rtrimstr($y))] catch ["ko", .]
    run  jq.test:2533  try ["OK", setpath([[1]]; 1)] catch ["KO", .]
    run  jq.test:2538  foreach .[] as $x (0, 1; . + $x)
    run  jq.test:2548  strflocaltime("" | ., @uri)
    run  jq.test:2558  reduce range(9999) as $_ ([];[.]) | tojson | fromjson | flatten
    run  jq.test:2563  reduce range(10000) as $_ ([];[.]) | tojson | try (fromjson) catch . | (contains("<skipped: too deep>") | not) and contains("Exceeds depth limit for parsing")
    run  jq.test:2568  reduce range(10001) as $_ ([];[.]) | tojson | contains("<skipped: too deep>")
    run  jq.test:2573  setpath([range(10000) | 0]; 0) | flatten
    run  jq.test:2577  try setpath([range(10001) | 0]; 0) catch .
    run  jq.test:2581  getpath([range(10000) | 0])
    run  jq.test:2585  try getpath([range(10001) | 0]) catch .
    run  jq.test:2589  delpaths([[range(10000) | 0]])
    run  jq.test:2593  try delpaths([[range(10001) | 0]]) catch .
    run  jq.test:2598  reduce range(10000) as $_ ([]; [.]) | contains([[]])
    run  jq.test:2602  try (reduce range(10001) as $_ ([]; [.]) as $x | $x | contains($x)) catch .
    run  jq.test:2607  reduce range(10000) as $_ ({}; {a: .}) as $x | $x * $x | length
    run  jq.test:2611  try (reduce range(10001) as $_ ({}; {a: .}) as $x | $x * $x) catch .
    run  jq.test:2616  try ((reduce range(10001) as $_ ([]; [.])) as $x | (reduce range(10001) as $_ ([]; [.])) as $y | $x == $y) catch .
    run  jq.test:2621  try ((reduce range(10001) as $_ ([]; [.])) as $x | [$x, $x] | sort) catch .
    run  jq.test:2625  try ((reduce range(10001) as $_ ([]; [.])) as $x | [$x, $x] | unique) catch .
    run  jq.test:2629  try ((reduce range(10001) as $_ ({}; {a: .})) as $x | [$x, $x] | sort) catch .
    run  jq.test:2633  try ((reduce range(10001) as $_ ({}; {a: .})) as $x | [$x, $x] | unique) catch .
    
    550 cases, 13 excluded

## Build summary
<reusable-compact filename="exclusions.txt">
Lists verbatim corpus program lines excluded from scoring. Exclusions must match corpus cases; stale entries are harness errors. Only module-loader cases are excluded.
</reusable-compact>

<reusable-compact filename="full_test.sh">
Executable scoring entry point. Requires `./jq` executable, sets `JQ="$PWD/jq"`, then runs `python3 sources/run_conformance.py` unfiltered. Propagates the harness verdict.
</reusable-compact>

<reusable-compact filename="run_conformance.py">
Language-neutral jq corpus runner. Requires `JQ`; supports `--list`, `--select`, `--json`, and verbose mode. List mode parses and enumerates cases without execution. Exit 0 means all run cases pass, 1 means failures/errors, and 2 means harness fault. Candidate compile errors must exit 3; runtime errors must exit 5.
</reusable-compact>

<reusable-compact filename="parser.y">
Authoritative jq grammar covering filters, operators, literals, strings/interpolation, functions, imports, variables, destructuring, reductions, conditionals, assignments, and module syntax. Parser failures are distinct from runtime failures.
</reusable-compact>

<reusable-compact filename="builtin.jq">
Defines jq standard-library filters for mapping, reduction, recursion, paths, strings, regex, sorting, dates, streaming, assignments, SQL-style operators, and type predicates. Builtins preserve jq generator semantics and error behavior.
</reusable-compact>

RESULT: SUCCESS

FILES CHANGED:
- tests/test_conformance_staging.py

SUMMARY:
Staged assets remained byte-for-byte unchanged. List-mode acceptance passed: 550 cases, 13 excluded. Unit tests passed: 9 tests.

BLOCKERS:
- None
