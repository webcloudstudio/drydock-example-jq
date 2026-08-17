# Evidence: Block 14 · Service (block-14)

- block type: block
- date: 2026-08-17
- resulting state: closed/verified
- story points (combined assembled cost): 25728
- execution id: 20260817.184038.829Z-62ba0052

## Stories built
- Implement reduce and foreach accumulation. (flow-reduce) [story]
- Implement range, iteration utilities, and recursive generators. (flow-recursion-utilities) [story]

## Stacked context
- compass: COMPASS.md (SP 2068)
- implements: FEATURE-Flow-Reduce.md (SP 466)
- context: parser.y (SP 5596)
- context: jq.test (SP 13058)
- stack: python_compact.md (SP 1534)
- implements: FEATURE-Flow-Recursion-Utilities.md (SP 527)
- context: builtin.jq (SP 2408)

## Build directory changes
- jq
- tests/test_flow_reduce_recursion.py

## Pre-build acceptance observation
- GREEN (prepassed): flow-reduce-suite (FEATURE-Flow-Reduce.md)
  intent: The implementation passes conformance cases for reduce expressions and accumulator updates.
  return code: 0
  stdout:
    run  jq.test:490  reduce range(65540;65536;-1) as $i ([]; .[$i] = $i)|.[65536:]
    run  jq.test:899  reduce .[] as $x (0; . + $x)
    run  jq.test:903  reduce .[] as [$i, {j:$j}] (0; . + $i - $j)
    run  jq.test:907  reduce [[1,2,10], [3,4,10]][] as [$i,$j] (0; . + $i * $j)
    run  jq.test:911  [-reduce -.[] as $x (0; . + $x)]
    run  jq.test:915  [reduce .[] / .[] as $i (0; . + $i)]
    run  jq.test:919  reduce .[] as $x (0; . + $x) as $x | $x
    run  jq.test:924  reduce . as $n (.; .)
    run  jq.test:2042  {if:0,and:1,or:2,then:3,else:4,elif:5,end:6,as:7,def:8,reduce:9,foreach:10,try:11,catch:12,label:13,import:14,include:15,module:16}
    run  jq.test:2289  reduce .[] as $then (4 as $else | $else; . as $elif | . + $then * $elif)
    run  jq.test:2558  reduce range(9999) as $_ ([];[.]) | tojson | fromjson | flatten
    run  jq.test:2563  reduce range(10000) as $_ ([];[.]) | tojson | try (fromjson) catch . | (contains("<skipped: too deep>") | not) and contains("Exceeds depth limit for parsing")
    run  jq.test:2568  reduce range(10001) as $_ ([];[.]) | tojson | contains("<skipped: too deep>")
    run  jq.test:2598  reduce range(10000) as $_ ([]; [.]) | contains([[]])
    run  jq.test:2602  try (reduce range(10001) as $_ ([]; [.]) as $x | $x | contains($x)) catch .
    run  jq.test:2607  reduce range(10000) as $_ ({}; {a: .}) as $x | $x * $x | length
    run  jq.test:2611  try (reduce range(10001) as $_ ({}; {a: .}) as $x | $x * $x) catch .
    run  jq.test:2616  try ((reduce range(10001) as $_ ([]; [.])) as $x | (reduce range(10001) as $_ ([]; [.])) as $y | $x == $y) catch .
    run  jq.test:2621  try ((reduce range(10001) as $_ ([]; [.])) as $x | [$x, $x] | sort) catch .
    run  jq.test:2625  try ((reduce range(10001) as $_ ([]; [.])) as $x | [$x, $x] | unique) catch .
    run  jq.test:2629  try ((reduce range(10001) as $_ ({}; {a: .})) as $x | [$x, $x] | sort) catch .
    run  jq.test:2633  try ((reduce range(10001) as $_ ({}; {a: .})) as $x | [$x, $x] | unique) catch .
    
    22 cases, 0 excluded
- GREEN (prepassed): flow-foreach-suite (FEATURE-Flow-Reduce.md)
  intent: The implementation passes conformance cases for foreach extraction and stream order.
  return code: 0
  stdout:
    run  jq.test:333  [label $out | foreach .[] as $item ([3, null]; if .[0] < 1 then break $out else [.[0] -1, $item] end; .[1])]
    run  jq.test:337  [foreach range(5) as $item (0; $item)]
    run  jq.test:341  [foreach .[] as [$i, $j] (0; . + $i - $j)]
    run  jq.test:345  [foreach .[] as {a:$a} (0; . + $a; -.)]
    run  jq.test:349  [-foreach -.[] as $x (0; . + $x)]
    run  jq.test:353  [foreach .[] / .[] as $i (0; . + $i)]
    run  jq.test:357  [foreach .[] as $x (0; . + $x) as $x | $x]
    run  jq.test:2042  {if:0,and:1,or:2,then:3,else:4,elif:5,end:6,as:7,def:8,reduce:9,foreach:10,try:11,catch:12,label:13,import:14,include:15,module:16}
    run  jq.test:2293  1 as $foreach | 2 as $and | 3 as $or | { $foreach, $and, $or, a }
    run  jq.test:2297  [ foreach .[] as $try (1 as $catch | $catch - 1; . + $try; .) ]
    run  jq.test:2538  foreach .[] as $x (0, 1; . + $x)
    
    11 cases, 0 excluded
- GREEN (prepassed): flow-range-utilities (FEATURE-Flow-Recursion-Utilities.md)
  intent: The implementation passes conformance cases for range, limit, skip, first, last, and nth.
  return code: 0
  stdout:
    run  jq.test:287  [range(0;10)]
    run  jq.test:291  [range(0,1;3,4)]
    run  jq.test:295  [range(0;10;3)]
    run  jq.test:299  [range(0;10;-1)]
    run  jq.test:303  [range(0;-5;-1)]
    run  jq.test:307  [range(0,1;4,5;1,2)]
    run  jq.test:337  [foreach range(5) as $item (0; $item)]
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
    run  jq.test:490  reduce range(65540;65536;-1) as $i ([]; .[$i] = $i)|.[65536:]
    run  jq.test:766  [add(null), add(range(range(10))), add(empty), add(10,range(10))]
    run  jq.test:851  [(3.141592 / 2) * (range(0;20) / 20)|cos * 1000000|floor / 1000000]
    run  jq.test:855  [(3.141592 / 2) * (range(0;20) / 20)|sin * 1000000|floor / 1000000]
    run  jq.test:1205  pick(first)
    run  jq.test:1209  pick(first|first)
    run  jq.test:1214  try pick(last) catch .
    run  jq.test:1895  last(range(365 * 67)|("1970-03-01T01:02:03Z"|strptime("%Y-%m-%dT%H:%M:%SZ")|mktime) + (86400 * .)|strftime("%Y-%m-%dT%H:%M:%SZ")|strptime("%Y-%m-%dT%H:%M:%SZ"))
    run  jq.test:2005  "x" * range(0; 12; 2) + "☆" * 8 | try -. catch .
    run  jq.test:2067  [range(-52;52;1)] as $powers | [$powers[]|pow(2;.)|log2|round] == $powers
    run  jq.test:2071  [range(-99/2;99/2;1)] as $orig | [$orig[]|pow(2;.)|log2] as $back | ($orig|keys)[]|. as $k | (($orig|.[$k])-($back|.[$k]))|if . < 0 then . * -1 else . end|select(.>.00005)
    run  jq.test:2089  INDEX(range(5)|[., "foo\(.)"]; .[0])
    run  jq.test:2097  range(5;10)|IN(range(10))
    run  jq.test:2105  range(5;13)|IN(range(0;10;3))
    run  jq.test:2116  range(10;12)|IN(range(10))
    run  jq.test:2121  IN(range(10;20); range(10))
    run  jq.test:2125  IN(range(5;20); range(10))
    run  jq.test:2143  isempty(range(3))
    run  jq.test:2285  [ label $if | range(10) | ., (select(. == 5) | break $if) ]
    run  jq.test:2372  first(.?,.?)
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
    run  jq.test:2483  try ([range(10)] | .[1.5:3.5] = ["xyz"]) catch .
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
    
    74 cases, 0 excluded
- GREEN (prepassed): flow-recursion-utilities (FEATURE-Flow-Recursion-Utilities.md)
  intent: The implementation passes conformance cases for while, until, repeat, and recurse generators.
  return code: 0
  stdout:
    run  jq.test:187  [..]
    run  jq.test:311  [while(.<100; .*2)]
    run  jq.test:329  [.[]|[.,1]|until(.[0] < 1; [.[0] - 1, .[1] * .[0]])|.[1]]
    run  jq.test:2014  try (. + "x") catch . == if have_decnum then "number (12345678901234567890123456...) and string (\"x\") cannot be added" else "number (12345678901234568000000000...) and string (\"x\") cannot be added" end
    run  jq.test:2135  (.. | select(type == "object" and has("b") and (.b | type) == "array")|.b) |= .[0]
    
    5 cases, 0 excluded

## Post-build programmatic acceptance
- PASS: flow-reduce-suite (FEATURE-Flow-Reduce.md)
  intent: The implementation passes conformance cases for reduce expressions and accumulator updates.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
  stdout:
    run  jq.test:490  reduce range(65540;65536;-1) as $i ([]; .[$i] = $i)|.[65536:]
    run  jq.test:899  reduce .[] as $x (0; . + $x)
    run  jq.test:903  reduce .[] as [$i, {j:$j}] (0; . + $i - $j)
    run  jq.test:907  reduce [[1,2,10], [3,4,10]][] as [$i,$j] (0; . + $i * $j)
    run  jq.test:911  [-reduce -.[] as $x (0; . + $x)]
    run  jq.test:915  [reduce .[] / .[] as $i (0; . + $i)]
    run  jq.test:919  reduce .[] as $x (0; . + $x) as $x | $x
    run  jq.test:924  reduce . as $n (.; .)
    run  jq.test:2042  {if:0,and:1,or:2,then:3,else:4,elif:5,end:6,as:7,def:8,reduce:9,foreach:10,try:11,catch:12,label:13,import:14,include:15,module:16}
    run  jq.test:2289  reduce .[] as $then (4 as $else | $else; . as $elif | . + $then * $elif)
    run  jq.test:2558  reduce range(9999) as $_ ([];[.]) | tojson | fromjson | flatten
    run  jq.test:2563  reduce range(10000) as $_ ([];[.]) | tojson | try (fromjson) catch . | (contains("<skipped: too deep>") | not) and contains("Exceeds depth limit for parsing")
    run  jq.test:2568  reduce range(10001) as $_ ([];[.]) | tojson | contains("<skipped: too deep>")
    run  jq.test:2598  reduce range(10000) as $_ ([]; [.]) | contains([[]])
    run  jq.test:2602  try (reduce range(10001) as $_ ([]; [.]) as $x | $x | contains($x)) catch .
    run  jq.test:2607  reduce range(10000) as $_ ({}; {a: .}) as $x | $x * $x | length
    run  jq.test:2611  try (reduce range(10001) as $_ ({}; {a: .}) as $x | $x * $x) catch .
    run  jq.test:2616  try ((reduce range(10001) as $_ ([]; [.])) as $x | (reduce range(10001) as $_ ([]; [.])) as $y | $x == $y) catch .
    run  jq.test:2621  try ((reduce range(10001) as $_ ([]; [.])) as $x | [$x, $x] | sort) catch .
    run  jq.test:2625  try ((reduce range(10001) as $_ ([]; [.])) as $x | [$x, $x] | unique) catch .
    run  jq.test:2629  try ((reduce range(10001) as $_ ({}; {a: .})) as $x | [$x, $x] | sort) catch .
    run  jq.test:2633  try ((reduce range(10001) as $_ ({}; {a: .})) as $x | [$x, $x] | unique) catch .
    
    22 cases, 0 excluded
- PASS: flow-foreach-suite (FEATURE-Flow-Reduce.md)
  intent: The implementation passes conformance cases for foreach extraction and stream order.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
  stdout:
    run  jq.test:333  [label $out | foreach .[] as $item ([3, null]; if .[0] < 1 then break $out else [.[0] -1, $item] end; .[1])]
    run  jq.test:337  [foreach range(5) as $item (0; $item)]
    run  jq.test:341  [foreach .[] as [$i, $j] (0; . + $i - $j)]
    run  jq.test:345  [foreach .[] as {a:$a} (0; . + $a; -.)]
    run  jq.test:349  [-foreach -.[] as $x (0; . + $x)]
    run  jq.test:353  [foreach .[] / .[] as $i (0; . + $i)]
    run  jq.test:357  [foreach .[] as $x (0; . + $x) as $x | $x]
    run  jq.test:2042  {if:0,and:1,or:2,then:3,else:4,elif:5,end:6,as:7,def:8,reduce:9,foreach:10,try:11,catch:12,label:13,import:14,include:15,module:16}
    run  jq.test:2293  1 as $foreach | 2 as $and | 3 as $or | { $foreach, $and, $or, a }
    run  jq.test:2297  [ foreach .[] as $try (1 as $catch | $catch - 1; . + $try; .) ]
    run  jq.test:2538  foreach .[] as $x (0, 1; . + $x)
    
    11 cases, 0 excluded
- PASS: flow-range-utilities (FEATURE-Flow-Recursion-Utilities.md)
  intent: The implementation passes conformance cases for range, limit, skip, first, last, and nth.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
  stdout:
    run  jq.test:287  [range(0;10)]
    run  jq.test:291  [range(0,1;3,4)]
    run  jq.test:295  [range(0;10;3)]
    run  jq.test:299  [range(0;10;-1)]
    run  jq.test:303  [range(0;-5;-1)]
    run  jq.test:307  [range(0,1;4,5;1,2)]
    run  jq.test:337  [foreach range(5) as $item (0; $item)]
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
    run  jq.test:490  reduce range(65540;65536;-1) as $i ([]; .[$i] = $i)|.[65536:]
    run  jq.test:766  [add(null), add(range(range(10))), add(empty), add(10,range(10))]
    run  jq.test:851  [(3.141592 / 2) * (range(0;20) / 20)|cos * 1000000|floor / 1000000]
    run  jq.test:855  [(3.141592 / 2) * (range(0;20) / 20)|sin * 1000000|floor / 1000000]
    run  jq.test:1205  pick(first)
    run  jq.test:1209  pick(first|first)
    run  jq.test:1214  try pick(last) catch .
    run  jq.test:1895  last(range(365 * 67)|("1970-03-01T01:02:03Z"|strptime("%Y-%m-%dT%H:%M:%SZ")|mktime) + (86400 * .)|strftime("%Y-%m-%dT%H:%M:%SZ")|strptime("%Y-%m-%dT%H:%M:%SZ"))
    run  jq.test:2005  "x" * range(0; 12; 2) + "☆" * 8 | try -. catch .
    run  jq.test:2067  [range(-52;52;1)] as $powers | [$powers[]|pow(2;.)|log2|round] == $powers
    run  jq.test:2071  [range(-99/2;99/2;1)] as $orig | [$orig[]|pow(2;.)|log2] as $back | ($orig|keys)[]|. as $k | (($orig|.[$k])-($back|.[$k]))|if . < 0 then . * -1 else . end|select(.>.00005)
    run  jq.test:2089  INDEX(range(5)|[., "foo\(.)"]; .[0])
    run  jq.test:2097  range(5;10)|IN(range(10))
    run  jq.test:2105  range(5;13)|IN(range(0;10;3))
    run  jq.test:2116  range(10;12)|IN(range(10))
    run  jq.test:2121  IN(range(10;20); range(10))
    run  jq.test:2125  IN(range(5;20); range(10))
    run  jq.test:2143  isempty(range(3))
    run  jq.test:2285  [ label $if | range(10) | ., (select(. == 5) | break $if) ]
    run  jq.test:2372  first(.?,.?)
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
    run  jq.test:2483  try ([range(10)] | .[1.5:3.5] = ["xyz"]) catch .
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
    
    74 cases, 0 excluded
- PASS: flow-recursion-utilities (FEATURE-Flow-Recursion-Utilities.md)
  intent: The implementation passes conformance cases for while, until, repeat, and recurse generators.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
  stdout:
    run  jq.test:187  [..]
    run  jq.test:311  [while(.<100; .*2)]
    run  jq.test:329  [.[]|[.,1]|until(.[0] < 1; [.[0] - 1, .[1] * .[0]])|.[1]]
    run  jq.test:2014  try (. + "x") catch . == if have_decnum then "number (12345678901234567890123456...) and string (\"x\") cannot be added" else "number (12345678901234568000000000...) and string (\"x\") cannot be added" end
    run  jq.test:2135  (.. | select(type == "object" and has("b") and (.b | type) == "array")|.b) |= .[0]
    
    5 cases, 0 excluded

## Build summary
RESULT: SUCCESS

FILES CHANGED:
- jq
- tests/test_flow_reduce_recursion.py

SUMMARY:
Implemented reduce, foreach, range, iteration utilities, and recursive generators. Added focused regression tests; all 70 tests pass. All four declared list-mode acceptance checks pass.

BLOCKERS:
- None
