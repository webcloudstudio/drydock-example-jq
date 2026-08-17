# Evidence: Block 13 · Service (block-13)

- block type: block
- date: 2026-08-17
- resulting state: closed/verified
- story points (combined assembled cost): 55490
- execution id: 20260817.183714.121Z-40eb2ca7

## Stories built
- Implement conditionals, errors, try/catch, labels, and breaks. (flow-control-errors) [story]

## Stacked context
- compass: COMPASS.md (SP 2068)
- implements: FEATURE-Flow-Control-Errors.md (SP 498)
- context: parser.y (SP 5596)
- context: jq-manual.txt (SP 32696)
- context: jq.test (SP 13058)
- stack: python_compact.md (SP 1534)

## Build directory changes
- jq
- tests/test_flow_control_errors.py

## Pre-build acceptance observation
- GREEN (prepassed): flow-conditionals-suite (FEATURE-Flow-Control-Errors.md)
  intent: The implementation passes conformance cases for conditionals, truthiness, and logical control flow.
  return code: 0
  stdout:
    run  jq.test:315  [(label $here | .[] | if .>1 then break $here else . end), "hi!"]
    run  jq.test:319  [(label $here | .[] | if .>1 then break $here else . end), "hi!"]
    run  jq.test:333  [label $out | foreach .[] as $item ([3, null]; if .[0] < 1 then break $out else [.[0] -1, $item] end; .[1])]
    run  jq.test:889  def fac: if . == 1 then 1 else . * (. - 1 | fac) end; [.[] | fac]
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
    run  jq.test:1448  [.[]|try if . == 0 then error("foo") elif . == 1 then .a elif . == 2 then empty else . end catch .]
    run  jq.test:1460  [if error then 1 else 2 end?]
    run  jq.test:1485  {x: try 1, y: try error catch 2, z: if true then 3 end}
    run  jq.test:2014  try (. + "x") catch . == if have_decnum then "number (12345678901234567890123456...) and string (\"x\") cannot be added" else "number (12345678901234568000000000...) and string (\"x\") cannot be added" end
    run  jq.test:2042  {if:0,and:1,or:2,then:3,else:4,elif:5,end:6,as:7,def:8,reduce:9,foreach:10,try:11,catch:12,label:13,import:14,include:15,module:16}
    run  jq.test:2071  [range(-99/2;99/2;1)] as $orig | [$orig[]|pow(2;.)|log2] as $back | ($orig|keys)[]|. as $k | (($orig|.[$k])-($back|.[$k]))|if . < 0 then . * -1 else . end|select(.>.00005)
    run  jq.test:2196  .[0] | tostring | . == if have_decnum then "13911860366432393" else "13911860366432392" end
    run  jq.test:2200  .x | tojson | . == if have_decnum then "13911860366432393" else "13911860366432392" end
    run  jq.test:2204  (13911860366432393 == 13911860366432392) | . == if have_decnum then false else true end
    run  jq.test:2224  -. | tojson == if have_decnum then "-13911860366432393" else "-13911860366432392" end
    run  jq.test:2228  -. | tojson == if have_decnum then "0.12345678901234567890123456789" else "0.12345678901234568" end
    run  jq.test:2232  [1E+1000,-1E+1000 | tojson] == if have_decnum then ["1E+1000","-1E+1000"] else ["1.7976931348623157e+308","-1.7976931348623157e+308"] end
    run  jq.test:2271  [1E+1000,-1E+1000 | abs | tojson] | unique == if have_decnum then ["1E+1000"] else ["1.7976931348623157e+308"] end
    run  jq.test:2275  [1E+1000,-1E+1000 | length | tojson] | unique == if have_decnum then ["1E+1000"] else ["1.7976931348623157e+308"] end
    run  jq.test:2285  [ label $if | range(10) | ., (select(. == 5) | break $if) ]
    run  jq.test:2289  reduce .[] as $then (4 as $else | $else; . as $elif | . + $then * $elif)
    run  jq.test:2308  1 as $x | "2" as $y | "3" as $z | { $x, as, $y: 4, ($z): 5, if: 6, foo: 7 }
    run  jq.test:2350  .[]|(try (if .=="hi" then . else error end) catch empty) | "\(.) there!"
    run  jq.test:2354  try (["hi","ho"]|.[]|(try . catch (if .=="ho" then "BROKEN"|error else empty end)) | if .=="ho" then error else "\(.) there!" end) catch "caught outside \(.)"
    run  jq.test:2359  .[]|(try . catch (if .=="ho" then "BROKEN"|error else empty end)) | if .=="ho" then error else "\(.) there!" end
    
    38 cases, 0 excluded
- GREEN (prepassed): flow-errors-suite (FEATURE-Flow-Control-Errors.md)
  intent: The implementation passes conformance cases for errors, try/catch, optional filters, labels, and breaks.
  return code: 0
  stdout:
    run  jq.test:179  [.[]|.foo?]
    run  jq.test:183  [.[]|.foo?.bar?]
    run  jq.test:191  [.[]|.[]?]
    run  jq.test:195  [.[]|.[1:3]?]
    run  jq.test:200  map(try .a[] catch ., try .a.[] catch ., .a[]?, .a.[]?)
    run  jq.test:205  try ["OK", (.[] | error)] catch ["KO", .]
    run  jq.test:213  try (.foo[-1] = 0) catch .
    run  jq.test:217  try (.foo[-2] = 0) catch .
    run  jq.test:229  try (.[999999999] = 0) catch .
    run  jq.test:315  [(label $here | .[] | if .>1 then break $here else . end), "hi!"]
    run  jq.test:319  [(label $here | .[] | if .>1 then break $here else . end), "hi!"]
    run  jq.test:324  . as $foo | break $foo
    run  jq.test:333  [label $out | foreach .[] as $item ([3, null]; if .[0] < 1 then break $out else [.[0] -1, $item] end; .[1])]
    run  jq.test:365  [limit(0; error)]
    run  jq.test:369  [limit(1; 1, error)]
    run  jq.test:373  try limit(-1; error) catch .
    run  jq.test:389  try skip(-1; error) catch .
    run  jq.test:393  nth(1; 0,1,error("foo"))
    run  jq.test:405  [nth(0,5,9,10,15; range(.)), try nth(-1; range(.)) catch .]
    run  jq.test:410  first(1,error("foo"))
    run  jq.test:701  "123\u0000456" | try tonumber catch .
    run  jq.test:709  .[] | try toboolean catch .
    run  jq.test:720  "true\u0000x", "false\u0000" | try toboolean catch .
    run  jq.test:745  [.[] | try utf8bytelength catch .]
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
    run  jq.test:1062  any(true, error; .)
    run  jq.test:1066  all(false, error; .)
    run  jq.test:1123  try path(.a | map(select(.b == 0))) catch .
    run  jq.test:1127  try path(.a | map(select(.b == 0)) | .[0]) catch .
    run  jq.test:1131  try path(.a | map(select(.b == 0)) | .c) catch .
    run  jq.test:1135  try path(.a | map(select(.b == 0)) | .[]) catch .
    run  jq.test:1173  try delpaths(0) catch .
    run  jq.test:1214  try pick(last) catch .
    run  jq.test:1258  .[] | try (getpath(["a",0,"b"]) |= 5) catch .
    run  jq.test:1290  try ((map(select(.a == 1))[].b) = 10) catch .
    run  jq.test:1294  try ((map(select(.a == 1))[].a) |= .+1) catch .
    run  jq.test:1302  try (def x: reverse; x=10) catch .
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
    run  jq.test:1493  .[] | try error catch .
    run  jq.test:1499  try error("\($__loc__)") catch .
    run  jq.test:1553  try _strindices("abc") catch .
    run  jq.test:1557  try _strindices(123) catch .
    run  jq.test:1575  try trim catch ., try ltrim catch ., try rtrim catch .
    run  jq.test:1641  try (. * 1000000000) catch .
    run  jq.test:1705  .[] | .error = "no, it's OK"
    run  jq.test:1811  try flatten(-1) catch .
    run  jq.test:1839  try ["OK", bsearch(0)] catch ["KO",.]
    run  jq.test:1868  try strftime("%Y-%m-%dT%H:%M:%SZ") catch .
    run  jq.test:1872  try strflocaltime("%Y-%m-%dT%H:%M:%SZ") catch .
    run  jq.test:1876  try mktime catch .
    run  jq.test:1881  try ["OK", strftime([])] catch ["KO", .]
    run  jq.test:1885  try ["OK", strflocaltime({})] catch ["KO", .]
    skip jq.test:1982  import "syntaxerror" as e; .
    run  jq.test:1997  try -. catch .
    run  jq.test:2001  try (.-.) catch .
    run  jq.test:2005  "x" * range(0; 12; 2) + "☆" * 8 | try -. catch .
    run  jq.test:2014  try (. + "x") catch . == if have_decnum then "number (12345678901234567890123456...) and string (\"x\") cannot be added" else "number (12345678901234568000000000...) and string (\"x\") cannot be added" end
    run  jq.test:2034  try join(",") catch .
    run  jq.test:2038  try join(",") catch .
    run  jq.test:2042  {if:0,and:1,or:2,then:3,else:4,elif:5,end:6,as:7,def:8,reduce:9,foreach:10,try:11,catch:12,label:13,import:14,include:15,module:16}
    run  jq.test:2046  try (1/.) catch .
    run  jq.test:2050  try (1/0) catch .
    run  jq.test:2054  try (0/0) catch .
    run  jq.test:2058  try (1%.) catch .
    run  jq.test:2062  try (1%0) catch .
    run  jq.test:2086  (.[{}] = 0)?
    run  jq.test:2147  isempty(1,error("foo"))
    run  jq.test:2236  . |= try . catch .
    run  jq.test:2281  123 as $label | $label
    run  jq.test:2285  [ label $if | range(10) | ., (select(. == 5) | break $if) ]
    run  jq.test:2297  [ foreach .[] as $try (1 as $catch | $catch - 1; . + $try; .) ]
    run  jq.test:2324  .[] | try (fromjson | isnan) catch .
    run  jq.test:2337  try input catch .
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
    run  jq.test:2407  map(try implode catch .)
    run  jq.test:2411  try 0[implode] catch .
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
    run  jq.test:2563  reduce range(10000) as $_ ([];[.]) | tojson | try (fromjson) catch . | (contains("<skipped: too deep>") | not) and contains("Exceeds depth limit for parsing")
    run  jq.test:2577  try setpath([range(10001) | 0]; 0) catch .
    run  jq.test:2585  try getpath([range(10001) | 0]) catch .
    run  jq.test:2593  try delpaths([[range(10001) | 0]]) catch .
    run  jq.test:2602  try (reduce range(10001) as $_ ([]; [.]) as $x | $x | contains($x)) catch .
    run  jq.test:2611  try (reduce range(10001) as $_ ({}; {a: .}) as $x | $x * $x) catch .
    run  jq.test:2616  try ((reduce range(10001) as $_ ([]; [.])) as $x | (reduce range(10001) as $_ ([]; [.])) as $y | $x == $y) catch .
    run  jq.test:2621  try ((reduce range(10001) as $_ ([]; [.])) as $x | [$x, $x] | sort) catch .
    run  jq.test:2625  try ((reduce range(10001) as $_ ([]; [.])) as $x | [$x, $x] | unique) catch .
    run  jq.test:2629  try ((reduce range(10001) as $_ ({}; {a: .})) as $x | [$x, $x] | sort) catch .
    run  jq.test:2633  try ((reduce range(10001) as $_ ({}; {a: .})) as $x | [$x, $x] | unique) catch .
    
    134 cases, 1 excluded

## Post-build programmatic acceptance
- PASS: flow-conditionals-suite (FEATURE-Flow-Control-Errors.md)
  intent: The implementation passes conformance cases for conditionals, truthiness, and logical control flow.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
  stdout:
    run  jq.test:315  [(label $here | .[] | if .>1 then break $here else . end), "hi!"]
    run  jq.test:319  [(label $here | .[] | if .>1 then break $here else . end), "hi!"]
    run  jq.test:333  [label $out | foreach .[] as $item ([3, null]; if .[0] < 1 then break $out else [.[0] -1, $item] end; .[1])]
    run  jq.test:889  def fac: if . == 1 then 1 else . * (. - 1 | fac) end; [.[] | fac]
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
    run  jq.test:1448  [.[]|try if . == 0 then error("foo") elif . == 1 then .a elif . == 2 then empty else . end catch .]
    run  jq.test:1460  [if error then 1 else 2 end?]
    run  jq.test:1485  {x: try 1, y: try error catch 2, z: if true then 3 end}
    run  jq.test:2014  try (. + "x") catch . == if have_decnum then "number (12345678901234567890123456...) and string (\"x\") cannot be added" else "number (12345678901234568000000000...) and string (\"x\") cannot be added" end
    run  jq.test:2042  {if:0,and:1,or:2,then:3,else:4,elif:5,end:6,as:7,def:8,reduce:9,foreach:10,try:11,catch:12,label:13,import:14,include:15,module:16}
    run  jq.test:2071  [range(-99/2;99/2;1)] as $orig | [$orig[]|pow(2;.)|log2] as $back | ($orig|keys)[]|. as $k | (($orig|.[$k])-($back|.[$k]))|if . < 0 then . * -1 else . end|select(.>.00005)
    run  jq.test:2196  .[0] | tostring | . == if have_decnum then "13911860366432393" else "13911860366432392" end
    run  jq.test:2200  .x | tojson | . == if have_decnum then "13911860366432393" else "13911860366432392" end
    run  jq.test:2204  (13911860366432393 == 13911860366432392) | . == if have_decnum then false else true end
    run  jq.test:2224  -. | tojson == if have_decnum then "-13911860366432393" else "-13911860366432392" end
    run  jq.test:2228  -. | tojson == if have_decnum then "0.12345678901234567890123456789" else "0.12345678901234568" end
    run  jq.test:2232  [1E+1000,-1E+1000 | tojson] == if have_decnum then ["1E+1000","-1E+1000"] else ["1.7976931348623157e+308","-1.7976931348623157e+308"] end
    run  jq.test:2271  [1E+1000,-1E+1000 | abs | tojson] | unique == if have_decnum then ["1E+1000"] else ["1.7976931348623157e+308"] end
    run  jq.test:2275  [1E+1000,-1E+1000 | length | tojson] | unique == if have_decnum then ["1E+1000"] else ["1.7976931348623157e+308"] end
    run  jq.test:2285  [ label $if | range(10) | ., (select(. == 5) | break $if) ]
    run  jq.test:2289  reduce .[] as $then (4 as $else | $else; . as $elif | . + $then * $elif)
    run  jq.test:2308  1 as $x | "2" as $y | "3" as $z | { $x, as, $y: 4, ($z): 5, if: 6, foo: 7 }
    run  jq.test:2350  .[]|(try (if .=="hi" then . else error end) catch empty) | "\(.) there!"
    run  jq.test:2354  try (["hi","ho"]|.[]|(try . catch (if .=="ho" then "BROKEN"|error else empty end)) | if .=="ho" then error else "\(.) there!" end) catch "caught outside \(.)"
    run  jq.test:2359  .[]|(try . catch (if .=="ho" then "BROKEN"|error else empty end)) | if .=="ho" then error else "\(.) there!" end
    
    38 cases, 0 excluded
- PASS: flow-errors-suite (FEATURE-Flow-Control-Errors.md)
  intent: The implementation passes conformance cases for errors, try/catch, optional filters, labels, and breaks.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
  stdout:
    run  jq.test:179  [.[]|.foo?]
    run  jq.test:183  [.[]|.foo?.bar?]
    run  jq.test:191  [.[]|.[]?]
    run  jq.test:195  [.[]|.[1:3]?]
    run  jq.test:200  map(try .a[] catch ., try .a.[] catch ., .a[]?, .a.[]?)
    run  jq.test:205  try ["OK", (.[] | error)] catch ["KO", .]
    run  jq.test:213  try (.foo[-1] = 0) catch .
    run  jq.test:217  try (.foo[-2] = 0) catch .
    run  jq.test:229  try (.[999999999] = 0) catch .
    run  jq.test:315  [(label $here | .[] | if .>1 then break $here else . end), "hi!"]
    run  jq.test:319  [(label $here | .[] | if .>1 then break $here else . end), "hi!"]
    run  jq.test:324  . as $foo | break $foo
    run  jq.test:333  [label $out | foreach .[] as $item ([3, null]; if .[0] < 1 then break $out else [.[0] -1, $item] end; .[1])]
    run  jq.test:365  [limit(0; error)]
    run  jq.test:369  [limit(1; 1, error)]
    run  jq.test:373  try limit(-1; error) catch .
    run  jq.test:389  try skip(-1; error) catch .
    run  jq.test:393  nth(1; 0,1,error("foo"))
    run  jq.test:405  [nth(0,5,9,10,15; range(.)), try nth(-1; range(.)) catch .]
    run  jq.test:410  first(1,error("foo"))
    run  jq.test:701  "123\u0000456" | try tonumber catch .
    run  jq.test:709  .[] | try toboolean catch .
    run  jq.test:720  "true\u0000x", "false\u0000" | try toboolean catch .
    run  jq.test:745  [.[] | try utf8bytelength catch .]
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
    run  jq.test:1062  any(true, error; .)
    run  jq.test:1066  all(false, error; .)
    run  jq.test:1123  try path(.a | map(select(.b == 0))) catch .
    run  jq.test:1127  try path(.a | map(select(.b == 0)) | .[0]) catch .
    run  jq.test:1131  try path(.a | map(select(.b == 0)) | .c) catch .
    run  jq.test:1135  try path(.a | map(select(.b == 0)) | .[]) catch .
    run  jq.test:1173  try delpaths(0) catch .
    run  jq.test:1214  try pick(last) catch .
    run  jq.test:1258  .[] | try (getpath(["a",0,"b"]) |= 5) catch .
    run  jq.test:1290  try ((map(select(.a == 1))[].b) = 10) catch .
    run  jq.test:1294  try ((map(select(.a == 1))[].a) |= .+1) catch .
    run  jq.test:1302  try (def x: reverse; x=10) catch .
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
    run  jq.test:1493  .[] | try error catch .
    run  jq.test:1499  try error("\($__loc__)") catch .
    run  jq.test:1553  try _strindices("abc") catch .
    run  jq.test:1557  try _strindices(123) catch .
    run  jq.test:1575  try trim catch ., try ltrim catch ., try rtrim catch .
    run  jq.test:1641  try (. * 1000000000) catch .
    run  jq.test:1705  .[] | .error = "no, it's OK"
    run  jq.test:1811  try flatten(-1) catch .
    run  jq.test:1839  try ["OK", bsearch(0)] catch ["KO",.]
    run  jq.test:1868  try strftime("%Y-%m-%dT%H:%M:%SZ") catch .
    run  jq.test:1872  try strflocaltime("%Y-%m-%dT%H:%M:%SZ") catch .
    run  jq.test:1876  try mktime catch .
    run  jq.test:1881  try ["OK", strftime([])] catch ["KO", .]
    run  jq.test:1885  try ["OK", strflocaltime({})] catch ["KO", .]
    skip jq.test:1982  import "syntaxerror" as e; .
    run  jq.test:1997  try -. catch .
    run  jq.test:2001  try (.-.) catch .
    run  jq.test:2005  "x" * range(0; 12; 2) + "☆" * 8 | try -. catch .
    run  jq.test:2014  try (. + "x") catch . == if have_decnum then "number (12345678901234567890123456...) and string (\"x\") cannot be added" else "number (12345678901234568000000000...) and string (\"x\") cannot be added" end
    run  jq.test:2034  try join(",") catch .
    run  jq.test:2038  try join(",") catch .
    run  jq.test:2042  {if:0,and:1,or:2,then:3,else:4,elif:5,end:6,as:7,def:8,reduce:9,foreach:10,try:11,catch:12,label:13,import:14,include:15,module:16}
    run  jq.test:2046  try (1/.) catch .
    run  jq.test:2050  try (1/0) catch .
    run  jq.test:2054  try (0/0) catch .
    run  jq.test:2058  try (1%.) catch .
    run  jq.test:2062  try (1%0) catch .
    run  jq.test:2086  (.[{}] = 0)?
    run  jq.test:2147  isempty(1,error("foo"))
    run  jq.test:2236  . |= try . catch .
    run  jq.test:2281  123 as $label | $label
    run  jq.test:2285  [ label $if | range(10) | ., (select(. == 5) | break $if) ]
    run  jq.test:2297  [ foreach .[] as $try (1 as $catch | $catch - 1; . + $try; .) ]
    run  jq.test:2324  .[] | try (fromjson | isnan) catch .
    run  jq.test:2337  try input catch .
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
    run  jq.test:2407  map(try implode catch .)
    run  jq.test:2411  try 0[implode] catch .
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
    run  jq.test:2563  reduce range(10000) as $_ ([];[.]) | tojson | try (fromjson) catch . | (contains("<skipped: too deep>") | not) and contains("Exceeds depth limit for parsing")
    run  jq.test:2577  try setpath([range(10001) | 0]; 0) catch .
    run  jq.test:2585  try getpath([range(10001) | 0]) catch .
    run  jq.test:2593  try delpaths([[range(10001) | 0]]) catch .
    run  jq.test:2602  try (reduce range(10001) as $_ ([]; [.]) as $x | $x | contains($x)) catch .
    run  jq.test:2611  try (reduce range(10001) as $_ ({}; {a: .}) as $x | $x * $x) catch .
    run  jq.test:2616  try ((reduce range(10001) as $_ ([]; [.])) as $x | (reduce range(10001) as $_ ([]; [.])) as $y | $x == $y) catch .
    run  jq.test:2621  try ((reduce range(10001) as $_ ([]; [.])) as $x | [$x, $x] | sort) catch .
    run  jq.test:2625  try ((reduce range(10001) as $_ ([]; [.])) as $x | [$x, $x] | unique) catch .
    run  jq.test:2629  try ((reduce range(10001) as $_ ({}; {a: .})) as $x | [$x, $x] | sort) catch .
    run  jq.test:2633  try ((reduce range(10001) as $_ ({}; {a: .})) as $x | [$x, $x] | unique) catch .
    
    134 cases, 1 excluded

## Build summary
RESULT: SUCCESS

FILES CHANGED:
- jq
- tests/test_flow_control_errors.py

SUMMARY:
Implemented conditionals, `elif`, `try/catch`, errors, optional filters, labels, breaks, `halt`, and `halt_error`. Added regression tests.

Verification: 63 pytest tests passed; both declared acceptance checks passed.

BLOCKERS:
- None
