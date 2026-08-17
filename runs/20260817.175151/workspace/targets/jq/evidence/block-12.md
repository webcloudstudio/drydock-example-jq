# Evidence: Block 12 · Service (block-12)

- block type: block
- date: 2026-08-17
- resulting state: closed/verified
- story points (combined assembled cost): 25210
- execution id: 20260817.183329.223Z-583b3bc5

## Stories built
- Implement user-defined functions, arguments, recursion, and closures. (flow-functions) [story]

## Stacked context
- compass: COMPASS.md (SP 2068)
- implements: FEATURE-Flow-Functions.md (SP 509)
- context: parser.y (SP 5596)
- context: builtin.jq (SP 2408)
- context: jq.test (SP 13058)
- stack: python_compact.md (SP 1534)

## Build directory changes
- jq
- tests/test_flow_functions.py

## Pre-build acceptance observation
- GREEN (prepassed): flow-functions-suite (FEATURE-Flow-Functions.md)
  intent: The implementation passes the conformance cases for user-defined functions and function arguments.
  return code: 0
  stdout:
    run  jq.test:784  def f: . + 1; def g: def g: . + 100; f | g | f; (f | g), g
    run  jq.test:789  def f: (1000,2000); f
    run  jq.test:794  def f(a;b;c;d;e;f): [a+1,b,c,d,e,f]; f(.[0];.[1];.[0];.[0];.[0];.[0])
    run  jq.test:798  def f: 1; def g: f, def f: 2; def g: 3; f, def f: g; f, g; def f: 4; [f, def f: g; def g: 5; f, g]+[f,g]
    run  jq.test:803  def a: 0; . | a
    run  jq.test:808  def f(a;b;c;d;e;f;g;h;i;j): [j,i,h,g,f,e,d,c,b,a]; f(.[0];.[1];.[2];.[3];.[4];.[5];.[6];.[7];.[8];.[9])
    run  jq.test:860  def f(x): x | x; f([.], . + [42])
    run  jq.test:868  def f: .+1; def g: f; def f: .+100; def f(a):a+.+11; [(g|f(20)), f]
    run  jq.test:873  def id(x):x; 2000 as $x | def f(x):1 as $x | id([$x, x, x]); def g(x): 100 as $x | f($x,$x+x); g($x)
    run  jq.test:878  def x(a;b): a as $a | b as $b | $a + $b; def y($a;$b): $a + $b; def check(a;b): [x(a;b)] == [y(a;b)]; check(.[];.[]*2)
    run  jq.test:884  [[20,10][1,0] as $x | def f: (100,200) as $y | def g: [$x + $y, .]; . + $x | g; f[0] | [f][0][1] | f]
    run  jq.test:889  def fac: if . == 1 then 1 else . * (. - 1 | fac) end; [.[] | fac]
    run  jq.test:1253  def inc(x): x |= .+1; inc(.[].a)
    run  jq.test:1298  def x: .[1,2]; x=10
    run  jq.test:1302  try (def x: reverse; x=10) catch .
    skip jq.test:1900  import "a" as foo; import "b" as bar; def fooa: foo::a; [fooa, bar::a, bar::b, foo::a]
    skip jq.test:1917  import "data" as $a; import "data" as $b; def f: {$a, $b}; f
    run  jq.test:2042  {if:0,and:1,or:2,then:3,else:4,elif:5,end:6,as:7,def:8,reduce:9,foreach:10,try:11,catch:12,label:13,import:14,include:15,module:16}
    run  jq.test:2093  JOIN({"0":[0,"abc"],"1":[1,"bcd"],"2":[2,"def"],"3":[3,"efg"],"4":[4,"fgh"]}; .[0]|tostring)
    
    19 cases, 2 excluded
- GREEN (prepassed): flow-recursive-functions (FEATURE-Flow-Functions.md)
  intent: The implementation passes conformance cases for recursive function calls and function redefinition.
  return code: 0
  stdout:
    run  jq.test:784  def f: . + 1; def g: def g: . + 100; f | g | f; (f | g), g
    run  jq.test:789  def f: (1000,2000); f
    run  jq.test:794  def f(a;b;c;d;e;f): [a+1,b,c,d,e,f]; f(.[0];.[1];.[0];.[0];.[0];.[0])
    run  jq.test:798  def f: 1; def g: f, def f: 2; def g: 3; f, def f: g; f, g; def f: 4; [f, def f: g; def g: 5; f, g]+[f,g]
    run  jq.test:808  def f(a;b;c;d;e;f;g;h;i;j): [j,i,h,g,f,e,d,c,b,a]; f(.[0];.[1];.[2];.[3];.[4];.[5];.[6];.[7];.[8];.[9])
    run  jq.test:860  def f(x): x | x; f([.], . + [42])
    run  jq.test:868  def f: .+1; def g: f; def f: .+100; def f(a):a+.+11; [(g|f(20)), f]
    run  jq.test:873  def id(x):x; 2000 as $x | def f(x):1 as $x | id([$x, x, x]); def g(x): 100 as $x | f($x,$x+x); g($x)
    run  jq.test:884  [[20,10][1,0] as $x | def f: (100,200) as $y | def g: [$x + $y, .]; . + $x | g; f[0] | [f][0][1] | f]
    run  jq.test:889  def fac: if . == 1 then 1 else . * (. - 1 | fac) end; [.[] | fac]
    skip jq.test:1900  import "a" as foo; import "b" as bar; def fooa: foo::a; [fooa, bar::a, bar::b, foo::a]
    skip jq.test:1917  import "data" as $a; import "data" as $b; def f: {$a, $b}; f
    
    12 cases, 2 excluded

## Post-build programmatic acceptance
- PASS: flow-functions-suite (FEATURE-Flow-Functions.md)
  intent: The implementation passes the conformance cases for user-defined functions and function arguments.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
  stdout:
    run  jq.test:784  def f: . + 1; def g: def g: . + 100; f | g | f; (f | g), g
    run  jq.test:789  def f: (1000,2000); f
    run  jq.test:794  def f(a;b;c;d;e;f): [a+1,b,c,d,e,f]; f(.[0];.[1];.[0];.[0];.[0];.[0])
    run  jq.test:798  def f: 1; def g: f, def f: 2; def g: 3; f, def f: g; f, g; def f: 4; [f, def f: g; def g: 5; f, g]+[f,g]
    run  jq.test:803  def a: 0; . | a
    run  jq.test:808  def f(a;b;c;d;e;f;g;h;i;j): [j,i,h,g,f,e,d,c,b,a]; f(.[0];.[1];.[2];.[3];.[4];.[5];.[6];.[7];.[8];.[9])
    run  jq.test:860  def f(x): x | x; f([.], . + [42])
    run  jq.test:868  def f: .+1; def g: f; def f: .+100; def f(a):a+.+11; [(g|f(20)), f]
    run  jq.test:873  def id(x):x; 2000 as $x | def f(x):1 as $x | id([$x, x, x]); def g(x): 100 as $x | f($x,$x+x); g($x)
    run  jq.test:878  def x(a;b): a as $a | b as $b | $a + $b; def y($a;$b): $a + $b; def check(a;b): [x(a;b)] == [y(a;b)]; check(.[];.[]*2)
    run  jq.test:884  [[20,10][1,0] as $x | def f: (100,200) as $y | def g: [$x + $y, .]; . + $x | g; f[0] | [f][0][1] | f]
    run  jq.test:889  def fac: if . == 1 then 1 else . * (. - 1 | fac) end; [.[] | fac]
    run  jq.test:1253  def inc(x): x |= .+1; inc(.[].a)
    run  jq.test:1298  def x: .[1,2]; x=10
    run  jq.test:1302  try (def x: reverse; x=10) catch .
    skip jq.test:1900  import "a" as foo; import "b" as bar; def fooa: foo::a; [fooa, bar::a, bar::b, foo::a]
    skip jq.test:1917  import "data" as $a; import "data" as $b; def f: {$a, $b}; f
    run  jq.test:2042  {if:0,and:1,or:2,then:3,else:4,elif:5,end:6,as:7,def:8,reduce:9,foreach:10,try:11,catch:12,label:13,import:14,include:15,module:16}
    run  jq.test:2093  JOIN({"0":[0,"abc"],"1":[1,"bcd"],"2":[2,"def"],"3":[3,"efg"],"4":[4,"fgh"]}; .[0]|tostring)
    
    19 cases, 2 excluded
- PASS: flow-recursive-functions (FEATURE-Flow-Functions.md)
  intent: The implementation passes conformance cases for recursive function calls and function redefinition.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
  stdout:
    run  jq.test:784  def f: . + 1; def g: def g: . + 100; f | g | f; (f | g), g
    run  jq.test:789  def f: (1000,2000); f
    run  jq.test:794  def f(a;b;c;d;e;f): [a+1,b,c,d,e,f]; f(.[0];.[1];.[0];.[0];.[0];.[0])
    run  jq.test:798  def f: 1; def g: f, def f: 2; def g: 3; f, def f: g; f, g; def f: 4; [f, def f: g; def g: 5; f, g]+[f,g]
    run  jq.test:808  def f(a;b;c;d;e;f;g;h;i;j): [j,i,h,g,f,e,d,c,b,a]; f(.[0];.[1];.[2];.[3];.[4];.[5];.[6];.[7];.[8];.[9])
    run  jq.test:860  def f(x): x | x; f([.], . + [42])
    run  jq.test:868  def f: .+1; def g: f; def f: .+100; def f(a):a+.+11; [(g|f(20)), f]
    run  jq.test:873  def id(x):x; 2000 as $x | def f(x):1 as $x | id([$x, x, x]); def g(x): 100 as $x | f($x,$x+x); g($x)
    run  jq.test:884  [[20,10][1,0] as $x | def f: (100,200) as $y | def g: [$x + $y, .]; . + $x | g; f[0] | [f][0][1] | f]
    run  jq.test:889  def fac: if . == 1 then 1 else . * (. - 1 | fac) end; [.[] | fac]
    skip jq.test:1900  import "a" as foo; import "b" as bar; def fooa: foo::a; [fooa, bar::a, bar::b, foo::a]
    skip jq.test:1917  import "data" as $a; import "data" as $b; def f: {$a, $b}; f
    
    12 cases, 2 excluded

## Build summary
RESULT: SUCCESS

FILES CHANGED:
- jq
- tests/test_flow_functions.py

SUMMARY:
Implemented user-defined functions, recursion, filter/value arguments, closures, arity-specific lookup, and lexical redefinition. Added six focused tests.

Validation:
- pytest: 56 passed
- Declared function acceptance: 19 listed, 2 skipped
- Declared recursion acceptance: 12 listed, 2 skipped

BLOCKERS:
- None
