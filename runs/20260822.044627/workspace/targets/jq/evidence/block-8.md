# Evidence: Block 8 · Service (block-8)

- block type: block
- date: 2026-08-22
- resulting state: closed/failed
- story points (combined assembled cost): 25931
- execution id: 20260822.231236.324Z-ca97b585

## Stories built
- Implement jq filter expression grammar. (PARSE-003) [story]
- Implement declarations and control syntax parsing. (PARSE-004) [story]

## Acceptance tooling authorization
- FEATURE-PARSE-003.md#parse-003-conformance: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-PARSE-004.md#parse-004-conformance: executable=python3; scope=test; authorization=existing Target environment

## Stacked context
- compass: COMPASS.md (SP 3420)
- implements: FEATURE-PARSE-003.md (SP 449)
- context: parser.y (SP 5596)
- context: lexer.l (SP 1137)
- context: jq.test (SP 13058)
- context: ARCHITECTURE_compact.md (SP 154)
- stack: python_compact.md (SP 1534)
- implements: FEATURE-PARSE-004.md (SP 484)

## Build directory changes
- jq_interpreter/cli.py
- jq_interpreter/evaluator.py
- jq_interpreter/parser.py

## Pre-build acceptance observation
- RED: parse-003-conformance (FEATURE-PARSE-003.md)
  intent: The executable passes every selected corpus case exercising expression punctuation, accessors, collections, and operators.
  return code: 1
  stdout:
    {
      "candidate": [
        "/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260822.044627/build/jq/jq"
      ],
      "corpus": "jq.test",
      "summary": {
        "pass": 210,
        "fail": 245,
        "error": 0,
        "skip": 9
      },
      "cases": [
        {
          "line": 72,
          "program": "@text,@json,([1,.]|@csv,@tsv),@html,(@uri|.,@urid),@sh,(@base64|.,@base64d)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"!()<>&'\\\"\\t\"",
            "\"\\\"!()<>&'\\\\\\\"\\\\t\\\"\"",
            "\"1,\\\"!()<>&'\\\"\\\"\\t\\\"\"",
            "\"1\\t!()<>&'\\\"\\\\t\"",
            "\"!()&lt;&gt;&amp;&apos;&quot;\\t\"",
            "\"%21%28%29%3C%3E%26%27%22%09\"",
            "\"!()<>&'\\\"\\t\"",
            "\"'!()<>&'\\\\''\\\"\\t'\"",
            "\"ISgpPD4mJyIJ\"",
            "\"!()<>&'\\\"\\t\""
          ],
          "actual": [
            "\"!()<>&'\\\"\\t\"",
            "\"\\\"!()<>&'\\\\\\\"\\\\t\\\"\"",
            "\"1,\\\"!()<>&'\\\"\\\"\\t\\\"\"",
            "\"!\\t(\\t)\\t<\\t>\\t&\\t'\\t\\\"\\t\\\\t\"",
            "\"!()&lt;&gt;&amp;&apos;&quot;\\t\"",
            "\"%21%28%29%3C%3E%26%27%22%09\"",
            "\"!()<>&'\\\"\\t\"",
            "\"'!()<>&'\\\\''\\\"\\t'\"",
            "\"ISgpPD4mJyIJ\"",
            "\"\""
          ]
        },
        {
          "line": 122,
          "program": "{\"a\",b,\"a$\\(1+1)\"}",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "{\"a\":1, \"b\":2, \"a$2\":4}"
          ],
          "actual": [
            "{\"a\":null,\"b\":2,\"a$2\":null}"
          ]
        },
        {
          "line": 183,
          "program": "[.[]|.foo?.bar?]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[4,null]"
          ],
          "actual": [
            "[4]"
          ]
        },
        {
          "line": 187,
          "program": "[..]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[[1,[[2]],{\"a\":[1]}],1,[[2]],[2],2,{\"a\":[1]},[1],1]"
          ],
          "actual": []
        },
        {
          "line": 195,
          "program": "[.[]|.[1:3]?]",
          "status": "fail",
          "detail": "exited 1: Traceback (most recent call last):",
          "expect_failure": false,
          "expected": [
            "[null,\"bc\",[],[2,3],[2]]"
          ],
          "actual": []
        },
        {
          "line": 200,
          "program": "map(try .a[] catch ., try .a.[] catch ., .a[]?, .a.[]?)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1,2,1,2,1,2,1,2,\"Cannot iterate over number (123)\",\"Cannot iterate over number (123)\"]"
          ],
          "actual": [
            "[1,2,1,2,1,2,1,2,\"cannot iterate over value\",\"cannot iterate over value\"]"
          ]
        },
        {
          "line": 205,
          "program": "try [\"OK\", (.[] | error)] catch [\"KO\", .]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[\"KO\",[\"b\"]]"
          ],
          "actual": [
            "[\"KO\",\"error\"]"
          ]
        },
        {
          "line": 213,
          "program": "try (.foo[-1] = 0) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Out of bounds negative array index\""
          ],
          "actual": [
            "{\"foo\":{\"-1\":0}}"
          ]
        },
        {
          "line": 217,
          "program": "try (.foo[-2] = 0) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Out of bounds negative array index\""
          ],
          "actual": [
            "{\"foo\":{\"-2\":0}}"
          ]
        },
        {
          "line": 229,
          "program": "try (.[999999999] = 0) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Array index too large\""
          ],
          "actual": [
            "{\"999999999\":0}"
          ]
        },
        {
          "line": 277,
          "program": "{x: (1,2)},{x:3} | .x",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "1",
            "2",
            "3"
          ],
          "actual": [
            "{\"x\":1}",
            "{\"x\":2}",
            "3"
          ]
        },
        {
          "line": 283,
          "program": "[.[-4,-3,-2,-1,0,1,2,3]]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[null,1,2,3,1,2,3,null]"
          ],
          "actual": [
            "[null]"
          ]
        },
        {
          "line": 291,
          "program": "[range(0,1;3,4)]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[0,1,2, 0,1,2,3, 1,2, 1,2,3]"
          ],
          "actual": [
            "[0,1,2]"
          ]
        },
        {
          "line": 307,
          "program": "[range(0,1;4,5;1,2)]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[0,1,2,3,0,2, 0,1,2,3,4,0,2,4, 1,2,3,1,3, 1,2,3,4,1,3]"
          ],
          "actual": [
            "[0,1,2,3]"
          ]
        },
        {
          "line": 311,
          "program": "[while(.<100; .*2)]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1,2,4,8,16,32,64]"
          ],
          "actual": []
        },
        {
          "line": 324,
          "program": ". as $foo | break $foo",
          "status": "fail",
          "detail": "program was accepted, but the corpus marks it %%FAIL",
          "expect_failure": true,
          "expected": [],
          "actual": []
        },
        {
          "line": 329,
          "program": "[.[]|[.,1]|until(.[0] < 1; [.[0] - 1, .[1] * .[0]])|.[1]]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1,2,6,24,120]"
          ],
          "actual": []
        },
        {
          "line": 349,
          "program": "[-foreach -.[] as $x (0; . + $x)]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1,3,6]"
          ],
          "actual": [
            "[1]"
          ]
        },
        {
          "line": 353,
          "program": "[foreach .[] / .[] as $i (0; . + $i)]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1,3,3.5,4.5]"
          ],
          "actual": [
            "[1.0,1.5,3.5,4.5]"
          ]
        },
        {
          "line": 365,
          "program": "[limit(0; error)]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[]"
          ],
          "actual": []
        },
        {
          "line": 369,
          "program": "[limit(1; 1, error)]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1]"
          ],
          "actual": []
        },
        {
          "line": 381,
          "program": "[skip(0,2,3,4; .[])]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1,2,3,3]"
          ],
          "actual": [
            "[1,2,3]"
          ]
        },
        {
          "line": 405,
          "program": "[nth(0,5,9,10,15; range(.)), try nth(-1; range(.)) catch .]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[0,5,9,\"nth doesn't support negative indices\"]"
          ],
          "actual": []
        },
        {
          "line": 420,
          "program": "[limit(5,7; range(9))]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[0,1,2,3,4,0,1,2,3,4,5,6]"
          ],
          "actual": [
            "[0,1,2,3,4]"
          ]
        },
        {
          "line": 425,
          "program": "[nth(5,7; range(9;0;-1))]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[4,2]"
          ],
          "actual": []
        },
        {
          "line": 430,
          "program": "[range(0,1,2;4,3,2;2,3)]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[0,2,0,3,0,2,0,0,0,1,3,1,1,1,1,1,2,2,2,2]"
          ],
          "actual": [
            "[0,2]"
          ]
        },
        {
          "line": 435,
          "program": "[range(3,5)]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[0,1,2,0,1,2,3,4]"
          ],
          "actual": [
            "[0,1,2]"
          ]
        },
        {
          "line": 440,
          "program": "[(index(\",\",\"|\"), rindex(\",\",\"|\")), indices(\",\",\"|\")]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1,3,22,19,[1,5,7,12,14,16,18,20,22],[3,9,10,17,19]]"
          ],
          "actual": []
        },
        {
          "line": 466,
          "program": "[.[3:2], .[-5:4], .[:-2], .[-2:], .[3:3][1:], .[10:]]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[[], [2,3], [0,1,2,3,4], [5,6], [], []]"
          ],
          "actual": []
        },
        {
          "line": 470,
          "program": "[.[3:2], .[-5:4], .[:-2], .[-2:], .[3:3][1:], .[10:]]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[\"\",\"\",\"abcdefg\",\"hi\",\"\",\"\"]"
          ],
          "actual": []
        },
        {
          "line": 474,
          "program": "del(.[2:4],.[0],.[-2:])",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1,4,5]"
          ],
          "actual": []
        },
        {
          "line": 478,
          "program": ".[2:4] = ([], [\"a\",\"b\"], [\"a\",\"b\",\"c\"])",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[0,1,4,5,6,7]",
            "[0,1,\"a\",\"b\",4,5,6,7]",
            "[0,1,\"a\",\"b\",\"c\",4,5,6,7]"
          ],
          "actual": []
        },
        {
          "line": 530,
          "program": ". as {as: $kw, \"str\": $str, (\"e\"+\"x\"+\"p\"): $exp} | [$kw, $str, $exp]",
          "status": "fail",
          "detail": "program did not compile: jq: compile error: expected ,",
          "expect_failure": false,
          "expected": [
            "[1, 2, 3]"
          ],
          "actual": []
        },
        {
          "line": 560,
          "program": ". as $foo | [$foo, $bar]",
          "status": "fail",
          "detail": "program was accepted, but the corpus marks it %%FAIL",
          "expect_failure": true,
          "expected": [],
          "actual": []
        },
        {
          "line": 617,
          "program": "{\"a\":1} + {\"b\":2} + {\"c\":3}",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "{\"a\":1, \"b\":2, \"c\":3}"
          ],
          "actual": []
        },
        {
          "line": 633,
          "program": "[1,2,3,4,1] - [.,3]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[2,4]"
          ],
          "actual": []
        },
        {
          "line": 661,
          "program": "9E999999999, 9999999999E999999990, 1E-999999999, 0.000000001E-999999990",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "9E+999999999",
            "9.999999999E+999999999",
            "1E-999999999",
            "1E-999999999"
          ],
          "actual": [
            "null",
            "null",
            "0.0",
            "0.0"
          ]
        },
        {
          "line": 689,
          "program": "[(infinite, -infinite) % (1, -1, infinite)]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[0,0,0,0,0,-1]"
          ],
          "actual": []
        },
        {
          "line": 693,
          "program": "[nan % 1, 1 % nan | isnan]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[true,true]"
          ],
          "actual": []
        },
        {
          "line": 709,
          "program": ".[] | try toboolean catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"null (null) cannot be parsed as a boolean\"",
            "\"number (0) cannot be parsed as a boolean\"",
            "\"string (\\\"tru\\\") cannot be parsed as a boolean\"",
            "\"string (\\\"truee\\\") cannot be parsed as a boolean\"",
            "\"string (\\\"fals\\\") cannot be parsed as a boolean\"",
            "\"string (\\\"falsee\\\") cannot be parsed as a boolean\"",
            "\"array ([]) cannot be parsed as a boolean\"",
            "\"object ({}) cannot be parsed as a boolean\""
          ],
          "actual": [
            "\"unknown function toboolean\"",
            "\"unknown function toboolean\"",
            "\"unknown function toboolean\"",
            "\"unknown function toboolean\"",
            "\"unknown function toboolean\"",
            "\"unknown function toboolean\"",
            "\"unknown function toboolean\"",
            "\"unknown function toboolean\""
          ]
        },
        {
          "line": 720,
          "program": "\"true\\u0000x\", \"false\\u0000\" | try toboolean catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"string (\\\"true\\\\u0000x\\\") cannot be parsed as a boolean\"",
            "\"string (\\\"false\\\\u0000\\\") cannot be parsed as a boolean\""
          ],
          "actual": [
            "\"true\\u0000x\"",
            "\"unknown function toboolean\""
          ]
        },
        {
          "line": 725,
          "program": "[{\"a\":42},.object,10,.num,false,true,null,\"b\",[1,4]] | .[] as $x | [$x == .[]]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[true,  true,  false, false, false, false, false, false, false]",
            "[true,  true,  false, false, false, false, false, false, false]",
            "[false, false, true,  true,  false, false, false, false, false]",
            "[false, false, true,  true,  false, false, false, false, false]",
            "[false, false, false, false, true,  false, false, false, false]",
            "[false, false, false, false, false, true,  false, false, false]",
            "[false, false, false, false, false, false, true,  false, false]",
            "[false, false, false, false, false, false, false, true,  false]",
            "[false, false, false, false, false, false, false, false, true ]"
          ],
          "actual": []
        },
        {
          "line": 745,
          "program": "[.[] | try utf8bytelength catch .]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[\"array ([]) only strings have UTF-8 byte length\",\"object ({}) only strings have UTF-8 byte length\",\"array ([1,2]) only strings have UTF-8 byte length\",\"number (55) only strings have UTF-8 byte length\",\"boolean (true) only strings have UTF-8 byte length\",\"boolean (false) only strings have UTF-8 byte length\"]"
          ],
          "actual": [
            "[\"unknown function utf8bytelength\",\"unknown function utf8bytelength\",\"unknown function utf8bytelength\",\"unknown function utf8bytelength\",\"unknown function utf8bytelength\",\"unknown function utf8bytelength\"]"
          ]
        },
        {
          "line": 762,
          "program": "map_values(.+1)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1,2,3]"
          ],
          "actual": []
        },
        {
          "line": 766,
          "program": "[add(null), add(range(range(10))), add(empty), add(10,range(10))]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[null,120,null,55]"
          ],
          "actual": []
        },
        {
          "line": 771,
          "program": ".sum = add(.arr[])",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "{\"arr\":[],\"sum\":null}"
          ],
          "actual": [
            "{\"arr\":[],\"sum\":\"arr\"}"
          ]
        },
        {
          "line": 775,
          "program": "add({(.[]):1}) | keys",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[\"a\",\"b\",\"d\"]"
          ],
          "actual": []
        },
        {
          "line": 798,
          "program": "def f: 1; def g: f, def f: 2; def g: 3; f, def f: g; f, g; def f: 4; [f, def f: g; def g: 5; f, g]+[f,g]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[4,1,2,3,3,5,4,1,2,3,3]"
          ],
          "actual": [
            "[4,5,5,4,4,2,3,3]"
          ]
        },
        {
          "line": 868,
          "program": "def f: .+1; def g: f; def f: .+100; def f(a):a+.+11; [(g|f(20)), f]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[33,101]"
          ],
          "actual": []
        },
        {
          "line": 873,
          "program": "def id(x):x; 2000 as $x | def f(x):1 as $x | id([$x, x, x]); def g(x): 100 as $x | f($x,$x+x); g($x)",
          "status": "fail",
          "detail": "exited 1: Traceback (most recent call last):",
          "expect_failure": false,
          "expected": [
            "[1,100,2100.0,100,2100.0]"
          ],
          "actual": []
        },
        {
          "line": 878,
          "program": "def x(a;b): a as $a | b as $b | $a + $b; def y($a;$b): $a + $b; def check(a;b): [x(a;b)] == [y(a;b)]; check(.[];.[]*2)",
          "status": "fail",
          "detail": "exited 1: Traceback (most recent call last):",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": []
        },
        {
          "line": 884,
          "program": "[[20,10][1,0] as $x | def f: (100,200) as $y | def g: [$x + $y, .]; . + $x | g; f[0] | [f][0][1] | f]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[[110.0, 130.0], [210.0, 130.0], [110.0, 230.0], [210.0, 230.0], [120.0, 160.0], [220.0, 160.0], [120.0, 260.0], [220.0, 260.0]]"
          ],
          "actual": [
            "[[110,130],[210,130],[110,230],[210,230]]"
          ]
        },
        {
          "line": 911,
          "program": "[-reduce -.[] as $x (0; . + $x)]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[6]"
          ],
          "actual": [
            "[1]"
          ]
        },
        {
          "line": 933,
          "program": ". as {$a, $b:[$c, $d]}| [$a, $b, $c, $d]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1,[2,{\"d\":3}],2,{\"d\":3}]"
          ],
          "actual": []
        },
        {
          "line": 938,
          "program": ".[] | . as {$a, b: [$c, {$d}]} ?// [$a, {$b}, $e] ?// $f | [$a, $b, $c, $d, $e, $f]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1, null, 2, 3, null, null]",
            "[4, 5, null, null, 7, null]",
            "[null, null, null, null, null, \"foo\"]"
          ],
          "actual": []
        },
        {
          "line": 1045,
          "program": ". as $dot|any($dot[];not)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": []
        },
        {
          "line": 1049,
          "program": ". as $dot|any($dot[];not)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "false"
          ],
          "actual": []
        },
        {
          "line": 1053,
          "program": ". as $dot|all($dot[];.)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "false"
          ],
          "actual": []
        },
        {
          "line": 1057,
          "program": ". as $dot|all($dot[];.)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": []
        },
        {
          "line": 1062,
          "program": "any(true, error; .)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": []
        },
        {
          "line": 1066,
          "program": "all(false, error; .)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "false"
          ],
          "actual": []
        },
        {
          "line": 1086,
          "program": "[any,all]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[false,true]"
          ],
          "actual": []
        },
        {
          "line": 1090,
          "program": "[any,all]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[true,true]"
          ],
          "actual": []
        },
        {
          "line": 1094,
          "program": "[any,all]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[false,false]"
          ],
          "actual": []
        },
        {
          "line": 1098,
          "program": "[any,all]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[true,false]"
          ],
          "actual": []
        },
        {
          "line": 1102,
          "program": "[any,all]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[true,false]"
          ],
          "actual": []
        },
        {
          "line": 1110,
          "program": "path(.foo[0,1])",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[\"foo\", 0]",
            "[\"foo\", 1]"
          ],
          "actual": []
        },
        {
          "line": 1115,
          "program": "path(.[] | select(.>3))",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1]"
          ],
          "actual": []
        },
        {
          "line": 1119,
          "program": "path(.)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[]"
          ],
          "actual": []
        },
        {
          "line": 1123,
          "program": "try path(.a | map(select(.b == 0))) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Invalid path expression with result [{\\\"b\\\":0}]\""
          ],
          "actual": [
            "\"unknown function path\""
          ]
        },
        {
          "line": 1127,
          "program": "try path(.a | map(select(.b == 0)) | .[0]) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Invalid path expression near attempt to access element 0 of [{\\\"b\\\":0}]\""
          ],
          "actual": [
            "\"unknown function path\""
          ]
        },
        {
          "line": 1131,
          "program": "try path(.a | map(select(.b == 0)) | .c) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Invalid path expression near attempt to access element \\\"c\\\" of [{\\\"b\\\":0}]\""
          ],
          "actual": [
            "\"unknown function path\""
          ]
        },
        {
          "line": 1135,
          "program": "try path(.a | map(select(.b == 0)) | .[]) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Invalid path expression near attempt to iterate through [{\\\"b\\\":0}]\""
          ],
          "actual": [
            "\"unknown function path\""
          ]
        },
        {
          "line": 1139,
          "program": "path(.a[path(.b)[0]])",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[\"a\",\"b\"]"
          ],
          "actual": []
        },
        {
          "line": 1143,
          "program": "[paths]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[[0],[1],[1,0],[1,1],[1,1,\"a\"]]"
          ],
          "actual": []
        },
        {
          "line": 1147,
          "program": "[\"foo\",1] as $p | getpath($p), setpath($p; 20), delpaths([$p])",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"b\"",
            "{\"bar\": 42, \"foo\": [\"a\", 20, \"c\", \"d\"]}",
            "{\"bar\": 42, \"foo\": [\"a\", \"c\", \"d\"]}"
          ],
          "actual": []
        },
        {
          "line": 1153,
          "program": "map(getpath([2])), map(setpath([2]; 42)), map(delpaths([[2]]))",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[null, null, 2]",
            "[[0,null,42], [0,1,42], [0,1,42]]",
            "[[0], [0,1], [0,1]]"
          ],
          "actual": []
        },
        {
          "line": 1159,
          "program": "map(delpaths([[0,\"foo\"]]))",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[[{\"x\":1}], [{\"bar\":2}]]"
          ],
          "actual": []
        },
        {
          "line": 1163,
          "program": "[\"foo\",1] as $p | getpath($p), setpath($p; 20), delpaths([$p])",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "null",
            "{\"bar\":false, \"foo\": [null, 20]}",
            "{\"bar\":false}"
          ],
          "actual": []
        },
        {
          "line": 1169,
          "program": "delpaths([[-200]])",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1,2,3]"
          ],
          "actual": []
        },
        {
          "line": 1173,
          "program": "try delpaths(0) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Paths must be specified as an array\""
          ],
          "actual": [
            "\"unknown function delpaths\""
          ]
        },
        {
          "line": 1177,
          "program": "del(.), del(empty), del((.foo,.bar,.baz) | .[2,3,0]), del(.foo[0], .bar[0], .foo, .baz.bar[0].x)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "null",
            "{\"foo\": [0,1,2,3,4], \"bar\": [0,1]}",
            "{\"foo\": [1,4], \"bar\": [1]}",
            "{\"bar\": [1]}"
          ],
          "actual": []
        },
        {
          "line": 1184,
          "program": "del(.[1], .[-6], .[2], .[-3:9])",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[0, 3, 5, 6, 9]"
          ],
          "actual": []
        },
        {
          "line": 1188,
          "program": "del(.[nan])",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1,2,3]"
          ],
          "actual": []
        },
        {
          "line": 1192,
          "program": "del(.[nan,nan])",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1,2,3]"
          ],
          "actual": []
        },
        {
          "line": 1197,
          "program": "setpath([-1]; 1)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1]"
          ],
          "actual": []
        },
        {
          "line": 1201,
          "program": "pick(.a.b.c)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "{\"a\":{\"b\":{\"c\":null}}}"
          ],
          "actual": []
        },
        {
          "line": 1214,
          "program": "try pick(last) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Out of bounds negative array index\""
          ],
          "actual": [
            "\"unknown function pick\""
          ]
        },
        {
          "line": 1245,
          "program": ".foo += .foo",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "{\"foo\":4}"
          ],
          "actual": []
        },
        {
          "line": 1253,
          "program": "def inc(x): x |= .+1; inc(.[].a)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[{\"a\":2,\"b\":2},{\"a\":3,\"b\":4},{\"a\":8,\"b\":8}]"
          ],
          "actual": []
        },
        {
          "line": 1258,
          "program": ".[] | try (getpath([\"a\",0,\"b\"]) |= 5) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "{\"a\":[{\"b\":5}]}",
            "{\"b\":0,\"a\":[{\"b\":5}]}",
            "\"Cannot index number with number (0)\"",
            "{\"a\":[{\"b\":5}]}",
            "\"Cannot index number with string (\\\"b\\\")\"",
            "\"Cannot index object with number (0)\"",
            "{\"a\":[{\"b\":5}]}",
            "{\"a\":[{\"c\":3,\"b\":5}]}"
          ],
          "actual": []
        },
        {
          "line": 1270,
          "program": "(.[] | select(. >= 2)) |= empty",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1,0]"
          ],
          "actual": []
        },
        {
          "line": 1274,
          "program": ".[] |= select(. % 2 == 0)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[0,2,4]"
          ],
          "actual": [
            "[0,null,2,null,4,null]"
          ]
        },
        {
          "line": 1278,
          "program": ".foo[1,4,2,3] |= empty",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "{\"foo\":[0,5]}"
          ],
          "actual": [
            "{\"foo\":[0,null,null,null,null,5]}"
          ]
        },
        {
          "line": 1282,
          "program": ".[2][3] = 1",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[4, null, [null, null, null, 1]]"
          ],
          "actual": [
            "[4,null,{\"3\":1}]"
          ]
        },
        {
          "line": 1290,
          "program": "try ((map(select(.a == 1))[].b) = 10) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Invalid path expression near attempt to iterate through [{\\\"a\\\":1}]\""
          ],
          "actual": []
        },
        {
          "line": 1294,
          "program": "try ((map(select(.a == 1))[].a) |= .+1) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Invalid path expression near attempt to iterate through [{\\\"a\\\":1}]\""
          ],
          "actual": []
        },
        {
          "line": 1302,
          "program": "try (def x: reverse; x=10) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Invalid path expression with result [2,1,0]\""
          ],
          "actual": []
        },
        {
          "line": 1306,
          "program": ".[] = 1",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1,1,1,1,1,1]"
          ],
          "actual": []
        },
        {
          "line": 1322,
          "program": "[if 1,null,2 then 3 else 4 end]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[3,4,3]"
          ],
          "actual": [
            "[3]"
          ]
        },
        {
          "line": 1326,
          "program": "[if empty then 3 else 4 end]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[]"
          ],
          "actual": [
            "[4]"
          ]
        },
        {
          "line": 1342,
          "program": "[if false then 3 end]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[7]"
          ],
          "actual": [
            "[null]"
          ]
        },
        {
          "line": 1350,
          "program": "[if false then 3 elif false then 4 end]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[7]"
          ],
          "actual": [
            "[null]"
          ]
        },
        {
          "line": 1366,
          "program": "if true then [.] else . end []",
          "status": "fail",
          "detail": "program did not compile: jq: compile error: unexpected token",
          "expect_failure": false,
          "expected": [
            "null"
          ],
          "actual": []
        },
        {
          "line": 1370,
          "program": "[.[] | [.foo[] // .bar]]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[[1,2], [1], [3], [42], [41]]"
          ],
          "actual": [
            "[[1,2],[1],[18,18,3],[],[41,41,41]]"
          ]
        },
        {
          "line": 1374,
          "program": ".[] //= .[0]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[\"hello\",true,\"hello\",[false],\"hello\"]"
          ],
          "actual": []
        },
        {
          "line": 1411,
          "program": "[{\"foo\":42} == {\"foo\":42},{\"foo\":42} != {\"foo\":42}, {\"foo\":42} != {\"bar\":42}, {\"foo\":42} == {\"bar\":42}]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[true,false,true,false]"
          ],
          "actual": []
        },
        {
          "line": 1416,
          "program": "[{\"foo\":[1,2,{\"bar\":18},\"world\"]} == {\"foo\":[1,2,{\"bar\":18},\"world\"]},{\"foo\":[1,2,{\"bar\":18},\"world\"]} == {\"foo\":[1,2,{\"bar\":19},\"world\"]}]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[true,false]"
          ],
          "actual": []
        },
        {
          "line": 1421,
          "program": "[(\"foo\" | contains(\"foo\")), (\"foobar\" | contains(\"foo\")), (\"foo\" | contains(\"foobar\"))]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[true, true, false]"
          ],
          "actual": []
        },
        {
          "line": 1426,
          "program": "[contains(\"\"), contains(\"\\u0000\")]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[true, true]"
          ],
          "actual": []
        },
        {
          "line": 1430,
          "program": "[contains(\"\"), contains(\"a\"), contains(\"ab\"), contains(\"c\"), contains(\"d\")]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[true, true, true, true, true]"
          ],
          "actual": []
        },
        {
          "line": 1434,
          "program": "[contains(\"cd\"), contains(\"b\\u0000\"), contains(\"ab\\u0000\")]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[true, true, true]"
          ],
          "actual": []
        },
        {
          "line": 1438,
          "program": "[contains(\"b\\u0000c\"), contains(\"b\\u0000cd\"), contains(\"b\\u0000cd\")]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[true, true, true]"
          ],
          "actual": []
        },
        {
          "line": 1442,
          "program": "[contains(\"@\"), contains(\"\\u0000@\"), contains(\"\\u0000what\")]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[false, false, false]"
          ],
          "actual": []
        },
        {
          "line": 1448,
          "program": "[.[]|try if . == 0 then error(\"foo\") elif . == 1 then .a elif . == 2 then empty else . end catch .]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[\"foo\",\"Cannot index number with string (\\\"a\\\")\",3]"
          ],
          "actual": [
            "[\"foo\",\"cannot index value\",3]"
          ]
        },
        {
          "line": 1452,
          "program": "[.[]|(.a, .a)?]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[null,null,1,1]"
          ],
          "actual": [
            "[1,1]"
          ]
        },
        {
          "line": 1460,
          "program": "[if error then 1 else 2 end?]",
          "status": "fail",
          "detail": "program did not compile: jq: compile error: expected ]",
          "expect_failure": false,
          "expected": [
            "[]"
          ],
          "actual": []
        },
        {
          "line": 1464,
          "program": "try error(0) // 1",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "1"
          ],
          "actual": []
        },
        {
          "line": 1473,
          "program": "1 + try 2 catch 3 + 4",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "7"
          ],
          "actual": [
            "3"
          ]
        },
        {
          "line": 1481,
          "program": "try -.? catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"string (\\\"foo\\\") cannot be negated\""
          ],
          "actual": []
        },
        {
          "line": 1493,
          "program": ".[] | try error catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "1",
            "null",
            "2"
          ],
          "actual": [
            "\"error\"",
            "\"error\"",
            "\"error\""
          ]
        },
        {
          "line": 1499,
          "program": "try error(\"\\($__loc__)\") catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"{\\\"file\\\":\\\"<top-level>\\\",\\\"line\\\":1}\""
          ],
          "actual": [
            "\"variable $__loc__ is not defined\""
          ]
        },
        {
          "line": 1520,
          "program": "[.[]|ltrimstr(\"foo\")]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[\"fo\",\"\",\"barfoo\",\"bar\",\"afoo\"]"
          ],
          "actual": []
        },
        {
          "line": 1524,
          "program": "[.[]|rtrimstr(\"foo\")]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[\"fo\",\"\",\"bar\",\"foobar\",\"foob\"]"
          ],
          "actual": []
        },
        {
          "line": 1528,
          "program": "[.[]|trimstr(\"foo\")]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[\"fo\",\"\",\"bar\",\"bar\",\"b\"]"
          ],
          "actual": []
        },
        {
          "line": 1532,
          "program": "[.[]|ltrimstr(\"\")]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[\"a\", \"xx\", \"\"]"
          ],
          "actual": []
        },
        {
          "line": 1536,
          "program": "[.[]|rtrimstr(\"\")]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[\"a\", \"xx\", \"\"]"
          ],
          "actual": []
        },
        {
          "line": 1540,
          "program": "[.[]|trimstr(\"\")]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[\"a\", \"xx\", \"\"]"
          ],
          "actual": []
        },
        {
          "line": 1544,
          "program": "[(index(\",\"), rindex(\",\")), indices(\",\")]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1,13,[1,4,8,13]]"
          ],
          "actual": []
        },
        {
          "line": 1548,
          "program": "[ index(\"aba\"), rindex(\"aba\"), indices(\"aba\") ]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1,7,[1,3,5,7]]"
          ],
          "actual": []
        },
        {
          "line": 1553,
          "program": "try _strindices(\"abc\") catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"number (123) cannot be searched, as it is not a string\""
          ],
          "actual": [
            "\"unknown function _strindices\""
          ]
        },
        {
          "line": 1557,
          "program": "try _strindices(123) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"number (123) is not a string\""
          ],
          "actual": [
            "\"unknown function _strindices\""
          ]
        },
        {
          "line": 1575,
          "program": "try trim catch ., try ltrim catch ., try rtrim catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"trim input must be a string\"",
            "\"trim input must be a string\"",
            "\"trim input must be a string\""
          ],
          "actual": [
            "\"unknown function trim\"",
            "\"unknown function ltrim\"",
            "\"unknown function rtrim\""
          ]
        },
        {
          "line": 1585,
          "program": "indices([1,2])",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1,8]"
          ],
          "actual": []
        },
        {
          "line": 1589,
          "program": "indices([1,2])",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[]"
          ],
          "actual": []
        },
        {
          "line": 1601,
          "program": ".[:rindex(\"x\")]",
          "status": "fail",
          "detail": "program did not compile: jq: compile error: expected ]",
          "expect_failure": false,
          "expected": [
            "\"\u6b63\""
          ],
          "actual": []
        },
        {
          "line": 1625,
          "program": "[.[] * \"abc\"]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[null,null,\"\",\"\",\"abc\",\"abc\",\"abcabcabc\",\"abcabcabcabcabcabcabcabcabcabc\"]"
          ],
          "actual": [
            "[\"\",\"\",\"\",\"\",\"abc\",\"abc\",\"abcabcabc\",\"abcabcabcabcabcabcabcabcabcabc\"]"
          ]
        },
        {
          "line": 1629,
          "program": "[. * (nan,-nan)]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[null,null]"
          ],
          "actual": []
        },
        {
          "line": 1633,
          "program": ". * 100000 | [.[:10],.[-10:]]",
          "status": "fail",
          "detail": "program did not compile: jq: compile error: expected ]",
          "expect_failure": false,
          "expected": [
            "[\"abcabcabca\",\"cabcabcabc\"]"
          ],
          "actual": []
        },
        {
          "line": 1653,
          "program": "map(.[1] as $needle | .[0] | contains($needle))",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[true, true, true, false, false]"
          ],
          "actual": []
        },
        {
          "line": 1657,
          "program": "map(.[1] as $needle | .[0] | contains($needle))",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[true, true, false]"
          ],
          "actual": []
        },
        {
          "line": 1661,
          "program": "[({foo: 12, bar:13} | contains({foo: 12})), ({foo: 12} | contains({})), ({foo: 12, bar:13} | contains({baz:14}))]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[true, true, false]"
          ],
          "actual": []
        },
        {
          "line": 1665,
          "program": "{foo: {baz: 12, blap: {bar: 13}}, bar: 14} | contains({bar: 14, foo: {blap: {}}})",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": []
        },
        {
          "line": 1669,
          "program": "{foo: {baz: 12, blap: {bar: 13}}, bar: 14} | contains({bar: 14, foo: {blap: {bar: 14}}})",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "false"
          ],
          "actual": []
        },
        {
          "line": 1677,
          "program": "(sort_by(.b) | sort_by(.a)), sort_by(.a, .b), sort_by(.b, .c), group_by(.b), group_by(.a + .b - .c == 2)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[{\"a\": 0, \"b\": 2, \"c\": 43}, {\"a\": 1, \"b\": 4, \"c\": 14}, {\"a\": 1, \"b\": 4, \"c\": 3}, {\"a\": 4, \"b\": 1, \"c\": 3}]",
            "[{\"a\": 0, \"b\": 2, \"c\": 43}, {\"a\": 1, \"b\": 4, \"c\": 14}, {\"a\": 1, \"b\": 4, \"c\": 3}, {\"a\": 4, \"b\": 1, \"c\": 3}]",
            "[{\"a\": 4, \"b\": 1, \"c\": 3}, {\"a\": 0, \"b\": 2, \"c\": 43}, {\"a\": 1, \"b\": 4, \"c\": 3}, {\"a\": 1, \"b\": 4, \"c\": 14}]",
            "[[{\"a\": 4, \"b\": 1, \"c\": 3}], [{\"a\": 0, \"b\": 2, \"c\": 43}], [{\"a\": 1, \"b\": 4, \"c\": 14}, {\"a\": 1, \"b\": 4, \"c\": 3}]]",
            "[[{\"a\": 1, \"b\": 4, \"c\": 14}, {\"a\": 0, \"b\": 2, \"c\": 43}], [{\"a\": 4, \"b\": 1, \"c\": 3}, {\"a\": 1, \"b\": 4, \"c\": 3}]]"
          ],
          "actual": []
        },
        {
          "line": 1693,
          "program": "[min, max, min_by(.[1]), max_by(.[1]), min_by(.[2]), max_by(.[2])]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[[1,3,\"a\"],[4,2,\"a\"],[3,1,\"a\"],[2,4,\"a\"],[4,2,\"a\"],[1,3,\"a\"]]"
          ],
          "actual": []
        },
        {
          "line": 1697,
          "program": "[min,max,min_by(.),max_by(.)]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[null,null,null,null]"
          ],
          "actual": []
        },
        {
          "line": 1701,
          "program": ".foo[.baz]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "4"
          ],
          "actual": [
            "null"
          ]
        },
        {
          "line": 1721,
          "program": "with_entries(.key |= \"KEY_\" + .)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "{\"KEY_a\": 1, \"KEY_b\": 2}"
          ],
          "actual": []
        },
        {
          "line": 1741,
          "program": "[][.]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "null"
          ],
          "actual": []
        },
        {
          "line": 1745,
          "program": "map([1,2][0:.])",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[[1], [1], [1,2], [1,2], [1,2]]"
          ],
          "actual": []
        },
        {
          "line": 1811,
          "program": "try flatten(-1) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"flatten depth must not be negative\""
          ],
          "actual": [
            "\"unknown function flatten\""
          ]
        },
        {
          "line": 1835,
          "program": "bsearch({x:1})",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "1"
          ],
          "actual": []
        },
        {
          "line": 1839,
          "program": "try [\"OK\", bsearch(0)] catch [\"KO\",.]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[\"KO\",\"string (\\\"aa\\\") cannot be searched from\"]"
          ],
          "actual": [
            "[\"KO\",\"unknown function bsearch\"]"
          ]
        },
        {
          "line": 1843,
          "program": "strftime(\"%Y-%m-%dT%H:%M:%SZ\")",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"2015-03-05T23:51:47Z\""
          ],
          "actual": []
        },
        {
          "line": 1847,
          "program": "strftime(\"%A, %B %d, %Y\")",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Tuesday, June 30, 2015\""
          ],
          "actual": []
        },
        {
          "line": 1851,
          "program": "strftime(\"%Y-%m-%dT%H:%M:%SZ\")",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"2024-03-15T00:00:00Z\""
          ],
          "actual": []
        },
        {
          "line": 1863,
          "program": "gmtime[5]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "47.25"
          ],
          "actual": []
        },
        {
          "line": 1868,
          "program": "try strftime(\"%Y-%m-%dT%H:%M:%SZ\") catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"strftime/1 requires parsed datetime inputs\""
          ],
          "actual": [
            "\"unknown function strftime\""
          ]
        },
        {
          "line": 1872,
          "program": "try strflocaltime(\"%Y-%m-%dT%H:%M:%SZ\") catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"strflocaltime/1 requires parsed datetime inputs\""
          ],
          "actual": [
            "\"unknown function strflocaltime\""
          ]
        },
        {
          "line": 1876,
          "program": "try mktime catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"mktime requires parsed datetime inputs\""
          ],
          "actual": [
            "\"unknown function mktime\""
          ]
        },
        {
          "line": 1881,
          "program": "try [\"OK\", strftime([])] catch [\"KO\", .]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[\"KO\",\"strftime/1 requires a string format\"]"
          ],
          "actual": [
            "[\"KO\",\"unknown function strftime\"]"
          ]
        },
        {
          "line": 1885,
          "program": "try [\"OK\", strflocaltime({})] catch [\"KO\", .]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[\"KO\",\"strflocaltime/1 requires a string format\"]"
          ],
          "actual": [
            "[\"KO\",\"unknown function strflocaltime\"]"
          ]
        },
        {
          "line": 1889,
          "program": "[strptime(\"%Y-%m-%dT%H:%M:%SZ\")|(.,mktime)]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[[2015,2,5,23,51,47,4,63],1425599507]"
          ],
          "actual": []
        },
        {
          "line": 1895,
          "program": "last(range(365 * 67)|(\"1970-03-01T01:02:03Z\"|strptime(\"%Y-%m-%dT%H:%M:%SZ\")|mktime) + (86400 * .)|strftime(\"%Y-%m-%dT%H:%M:%SZ\")|strptime(\"%Y-%m-%dT%H:%M:%SZ\"))",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[2037,1,11,1,2,3,3,41]"
          ],
          "actual": []
        },
        {
          "line": 1900,
          "program": "import \"a\" as foo; import \"b\" as bar; def fooa: foo::a; [fooa, bar::a, bar::b, foo::a]",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": false,
          "expected": [
            "[\"a\",\"b\",\"c\",\"a\"]"
          ],
          "actual": []
        },
        {
          "line": 1904,
          "program": "import \"c\" as foo; [foo::a, foo::c]",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": false,
          "expected": [
            "[0,\"acmehbah\"]"
          ],
          "actual": []
        },
        {
          "line": 1908,
          "program": "include \"c\"; [a, c]",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": false,
          "expected": [
            "[0,\"acmehbah\"]"
          ],
          "actual": []
        },
        {
          "line": 1912,
          "program": "import \"data\" as $e; import \"data\" as $d; [$d[].this,$e[].that,$d::d[].this,$e::e[].that]|join(\";\")",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": false,
          "expected": [
            "\"is a test;is too;is a test;is too\""
          ],
          "actual": []
        },
        {
          "line": 1917,
          "program": "import \"data\" as $a; import \"data\" as $b; def f: {$a, $b}; f",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": false,
          "expected": [
            "{\"a\":[{\"this\":\"is a test\",\"that\":\"is too\"}],\"b\":[{\"this\":\"is a test\",\"that\":\"is too\"}]}"
          ],
          "actual": []
        },
        {
          "line": 1929,
          "program": "import \"shadow1\" as f; import \"shadow2\" as f; import \"shadow1\" as e; [e::e, f::e]",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": false,
          "expected": [
            "[2,3]"
          ],
          "actual": []
        },
        {
          "line": 1973,
          "program": "modulemeta | .deps | length",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": false,
          "expected": [
            "6"
          ],
          "actual": []
        },
        {
          "line": 1977,
          "program": "modulemeta | .defs | length",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": false,
          "expected": [
            "2"
          ],
          "actual": []
        },
        {
          "line": 1982,
          "program": "import \"syntaxerror\" as e; .",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": true,
          "expected": [],
          "actual": []
        },
        {
          "line": 1997,
          "program": "try -. catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"string (\\\"very-long-long-long-long...\\\") cannot be negated\""
          ],
          "actual": []
        },
        {
          "line": 2001,
          "program": "try (.-.) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"string (\\\"very-long-long-long-long...\\\") and string (\\\"very-long-long-long-long...\\\") cannot be subtracted\""
          ],
          "actual": []
        },
        {
          "line": 2005,
          "program": "\"x\" * range(0; 12; 2) + \"\u2606\" * 8 | try -. catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"string (\\\"\u2606\u2606\u2606\u2606\u2606\u2606\u2606\u2606\\\") cannot be negated\"",
            "\"string (\\\"xx\u2606\u2606\u2606\u2606\u2606\u2606\u2606\u2606\\\") cannot be negated\"",
            "\"string (\\\"xxxx\u2606\u2606\u2606\u2606\u2606\u2606...\\\") cannot be negated\"",
            "\"string (\\\"xxxxxx\u2606\u2606\u2606\u2606\u2606\u2606...\\\") cannot be negated\"",
            "\"string (\\\"xxxxxxxx\u2606\u2606\u2606\u2606\u2606...\\\") cannot be negated\"",
            "\"string (\\\"xxxxxxxxxx\u2606\u2606\u2606\u2606...\\\") cannot be negated\""
          ],
          "actual": []
        },
        {
          "line": 2014,
          "program": "try (. + \"x\") catch . == if have_decnum then \"number (12345678901234567890123456...) and string (\\\"x\\\") cannot be added\" else \"number (12345678901234568000000000...) and string (\\\"x\\\") cannot be added\" end",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": []
        },
        {
          "line": 2034,
          "program": "try join(\",\") catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"string (\\\"1,2,\\\") and object ({\\\"a\\\":{\\\"b\\\":{\\\"c\\\":33}}}) cannot be added\""
          ],
          "actual": [
            "\"1,2,{\\\"a\\\":{\\\"b\\\":{\\\"c\\\":33}}}\""
          ]
        },
        {
          "line": 2038,
          "program": "try join(\",\") catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"string (\\\"1,2,\\\") and array ([3,4,5]) cannot be added\""
          ],
          "actual": [
            "\"1,2,[3,4,5]\""
          ]
        },
        {
          "line": 2067,
          "program": "[range(-52;52;1)] as $powers | [$powers[]|pow(2;.)|log2|round] == $powers",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": []
        },
        {
          "line": 2075,
          "program": "{",
          "status": "fail",
          "detail": "exited 1; a rejected program must exit 3",
          "expect_failure": true,
          "expected": [],
          "actual": []
        },
        {
          "line": 2086,
          "program": "(.[{}] = 0)?",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [],
          "actual": [
            "{\"{}\":0}"
          ]
        },
        {
          "line": 2089,
          "program": "INDEX(range(5)|[., \"foo\\(.)\"]; .[0])",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "{\"0\":[0,\"foo0\"],\"1\":[1,\"foo1\"],\"2\":[2,\"foo2\"],\"3\":[3,\"foo3\"],\"4\":[4,\"foo4\"]}"
          ],
          "actual": []
        },
        {
          "line": 2093,
          "program": "JOIN({\"0\":[0,\"abc\"],\"1\":[1,\"bcd\"],\"2\":[2,\"def\"],\"3\":[3,\"efg\"],\"4\":[4,\"fgh\"]}; .[0]|tostring)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[[[5,\"foo\"],null],[[3,\"bar\"],[3,\"efg\"]],[[1,\"foobar\"],[1,\"bcd\"]]]"
          ],
          "actual": []
        },
        {
          "line": 2130,
          "program": "(.a as $x | .b) = \"b\"",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "{\"a\":null,\"b\":\"b\"}"
          ],
          "actual": []
        },
        {
          "line": 2135,
          "program": "(.. | select(type == \"object\" and has(\"b\") and (.b | type) == \"array\")|.b) |= .[0]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "{\"a\": {\"b\": 1}}"
          ],
          "actual": []
        },
        {
          "line": 2161,
          "program": "\"-1\"|IN(builtins[] / \"/\"|.[1])",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "false"
          ],
          "actual": []
        },
        {
          "line": 2165,
          "program": "all(builtins[] / \"/\"; .[1]|tonumber >= 0)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": []
        },
        {
          "line": 2169,
          "program": "builtins|any(.[:1] == \"_\")",
          "status": "fail",
          "detail": "program did not compile: jq: compile error: expected ]",
          "expect_failure": false,
          "expected": [
            "false"
          ],
          "actual": []
        },
        {
          "line": 2196,
          "program": ".[0] | tostring | . == if have_decnum then \"13911860366432393\" else \"13911860366432392\" end",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": []
        },
        {
          "line": 2200,
          "program": ".x | tojson | . == if have_decnum then \"13911860366432393\" else \"13911860366432392\" end",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": []
        },
        {
          "line": 2204,
          "program": "(13911860366432393 == 13911860366432392) | . == if have_decnum then false else true end",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": []
        },
        {
          "line": 2211,
          "program": ". - 10",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "13911860366432382"
          ],
          "actual": [
            "13911860366432383"
          ]
        },
        {
          "line": 2215,
          "program": ".[0] - 10",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "13911860366432382"
          ],
          "actual": [
            "13911860366432383"
          ]
        },
        {
          "line": 2219,
          "program": ".x - 10",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "13911860366432382"
          ],
          "actual": [
            "13911860366432383"
          ]
        },
        {
          "line": 2224,
          "program": "-. | tojson == if have_decnum then \"-13911860366432393\" else \"-13911860366432392\" end",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": []
        },
        {
          "line": 2228,
          "program": "-. | tojson == if have_decnum then \"0.12345678901234567890123456789\" else \"0.12345678901234568\" end",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": []
        },
        {
          "line": 2232,
          "program": "[1E+1000,-1E+1000 | tojson] == if have_decnum then [\"1E+1000\",\"-1E+1000\"] else [\"1.7976931348623157e+308\",\"-1.7976931348623157e+308\"] end",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": []
        },
        {
          "line": 2241,
          "program": ".[] as $n | $n+0 | [., tostring, . == $n]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[-9007199254740992,\"-9007199254740992\",true]",
            "[-9007199254740992,\"-9007199254740992\",true]",
            "[9007199254740992,\"9007199254740992\",true]",
            "[9007199254740992,\"9007199254740992\",true]",
            "[13911860366432392,\"13911860366432392\",true]"
          ],
          "actual": [
            "[-9007199254740993,\"-9007199254740993\",true]",
            "[-9007199254740992,\"-9007199254740992\",true]",
            "[9007199254740992,\"9007199254740992\",true]",
            "[9007199254740993,\"9007199254740993\",true]",
            "[13911860366432393,\"13911860366432393\",true]"
          ]
        },
        {
          "line": 2271,
          "program": "[1E+1000,-1E+1000 | abs | tojson] | unique == if have_decnum then [\"1E+1000\"] else [\"1.7976931348623157e+308\"] end",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": []
        },
        {
          "line": 2275,
          "program": "[1E+1000,-1E+1000 | length | tojson] | unique == if have_decnum then [\"1E+1000\"] else [\"1.7976931348623157e+308\"] end",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": []
        },
        {
          "line": 2285,
          "program": "[ label $if | range(10) | ., (select(. == 5) | break $if) ]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[0,1,2,3,4,5]"
          ],
          "actual": []
        },
        {
          "line": 2293,
          "program": "1 as $foreach | 2 as $and | 3 as $or | { $foreach, $and, $or, a }",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "{\"foreach\":1,\"and\":2,\"or\":3,\"a\":4}"
          ],
          "actual": [
            "{\"1\":1,\"2\":2,\"3\":3,\"a\":4}"
          ]
        },
        {
          "line": 2304,
          "program": "{ a, $__loc__, c }",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "{\"a\":[1,2,3],\"__loc__\":{\"file\":\"<top-level>\",\"line\":1},\"c\":{\"hi\":\"hey\"}}"
          ],
          "actual": []
        },
        {
          "line": 2308,
          "program": "1 as $x | \"2\" as $y | \"3\" as $z | { $x, as, $y: 4, ($z): 5, if: 6, foo: 7 }",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "{\"x\":1,\"as\":8,\"2\":4,\"3\":5,\"if\":6,\"foo\":7}"
          ],
          "actual": [
            "{\"1\":1,\"as\":8,\"2\":4,\"3\":5,\"if\":6,\"foo\":7}"
          ]
        },
        {
          "line": 2324,
          "program": ".[] | try (fromjson | isnan) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "true",
            "true",
            "\"Invalid numeric literal at EOF at line 1, column 4 (while parsing 'NaN1')\"",
            "\"Invalid numeric literal at EOF at line 1, column 5 (while parsing 'NaN10')\"",
            "\"Invalid numeric literal at EOF at line 1, column 6 (while parsing 'NaN100')\"",
            "\"Invalid numeric literal at EOF at line 1, column 7 (while parsing 'NaN1000')\"",
            "\"Invalid numeric literal at EOF at line 1, column 8 (while parsing 'NaN10000')\"",
            "\"Invalid numeric literal at EOF at line 1, column 9 (while parsing 'NaN100000')\""
          ],
          "actual": [
            "\"unknown function isnan\"",
            "\"invalid JSON\"",
            "\"invalid JSON\"",
            "\"invalid JSON\"",
            "\"invalid JSON\"",
            "\"invalid JSON\"",
            "\"invalid JSON\"",
            "\"invalid JSON\""
          ]
        },
        {
          "line": 2337,
          "program": "try input catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"break\""
          ],
          "actual": [
            "\"unknown function input\""
          ]
        },
        {
          "line": 2354,
          "program": "try ([\"hi\",\"ho\"]|.[]|(try . catch (if .==\"ho\" then \"BROKEN\"|error else empty end)) | if .==\"ho\" then error else \"\\(.) there!\" end) catch \"caught outside \\(.)\"",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"hi there!\"",
            "\"caught outside ho\""
          ],
          "actual": [
            "\"hi there!\"",
            "\"caught outside error\""
          ]
        },
        {
          "line": 2363,
          "program": "try (try error catch \"inner catch \\(.)\") catch \"outer catch \\(.)\"",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"inner catch foo\""
          ],
          "actual": [
            "\"inner catch error\""
          ]
        },
        {
          "line": 2367,
          "program": "try ((try error catch \"inner catch \\(.)\")|error) catch \"outer catch \\(.)\"",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"outer catch inner catch foo\""
          ],
          "actual": [
            "\"outer catch error\""
          ]
        },
        {
          "line": 2390,
          "program": ".[] |= try tonumber",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1, 3, 6.7, 0.89, -876, 5.43, 21]"
          ],
          "actual": [
            "[1,null,3,4,5,6.7,null,-876,null,21]"
          ]
        },
        {
          "line": 2395,
          "program": "any(keys[]|tostring?;true)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": []
        },
        {
          "line": 2407,
          "program": "map(try implode catch .)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[\"implode input must be an array\",\"string (\\\"a\\\") can't be imploded, unicode codepoint needs to be numeric\",\"number (null) can't be imploded, unicode codepoint needs to be numeric\"]"
          ],
          "actual": []
        },
        {
          "line": 2411,
          "program": "try 0[implode] catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Cannot index number with string (\\\"\\\")\""
          ],
          "actual": [
            "\"unknown function implode\""
          ]
        },
        {
          "line": 2416,
          "program": "walk(.)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "{\"x\":0}"
          ],
          "actual": []
        },
        {
          "line": 2425,
          "program": "[walk(.,1)]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[{\"x\":0},1]"
          ],
          "actual": []
        },
        {
          "line": 2430,
          "program": "walk(select(IN({}, []) | not))",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "{\"a\":1}"
          ],
          "actual": []
        },
        {
          "line": 2435,
          "program": "[range(10)] | .[1.2:3.5]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1,2,3]"
          ],
          "actual": [
            "[1,2]"
          ]
        },
        {
          "line": 2439,
          "program": "[range(10)] | .[1.5:3.5]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1,2,3]"
          ],
          "actual": [
            "[1,2]"
          ]
        },
        {
          "line": 2443,
          "program": "[range(10)] | .[1.7:3.5]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1,2,3]"
          ],
          "actual": [
            "[1,2]"
          ]
        },
        {
          "line": 2455,
          "program": "[[range(10)] | .[1.1,1.5,1.7]]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1,1,1]"
          ],
          "actual": []
        },
        {
          "line": 2463,
          "program": "[range(3)] | .[nan:1]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[0]"
          ],
          "actual": []
        },
        {
          "line": 2467,
          "program": "[range(3)] | .[1:nan]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1,2]"
          ],
          "actual": []
        },
        {
          "line": 2471,
          "program": "[range(3)] | .[nan]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "null"
          ],
          "actual": []
        },
        {
          "line": 2475,
          "program": "try ([range(3)] | .[nan] = 9) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Cannot set array element at NaN index\""
          ],
          "actual": []
        },
        {
          "line": 2479,
          "program": "try (\"foobar\" | .[1.5:3.5] = \"xyz\") catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Cannot update string slices\""
          ],
          "actual": []
        },
        {
          "line": 2483,
          "program": "try ([range(10)] | .[1.5:3.5] = [\"xyz\"]) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[0,\"xyz\",4,5,6,7,8,9]"
          ],
          "actual": []
        },
        {
          "line": 2487,
          "program": "try (\"foobar\" | .[1.5]) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Cannot index string with number (1.5)\""
          ],
          "actual": [
            "\"cannot index string with number\""
          ]
        },
        {
          "line": 2494,
          "program": "try [\"ok\", setpath([1]; 1)] catch [\"ko\", .]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[\"ko\",\"Cannot index object with number (1)\"]"
          ],
          "actual": [
            "[\"ko\",\"unknown function setpath\"]"
          ]
        },
        {
          "line": 2498,
          "program": "try fromjson catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Invalid string literal; expected \\\", but got ' at line 1, column 5 (while parsing '{'a': 123}')\""
          ],
          "actual": [
            "\"invalid JSON\""
          ]
        },
        {
          "line": 2516,
          "program": ".[] as [$x, $y] | try [\"ok\", ($x | ltrimstr($y))] catch [\"ko\", .]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[\"ko\",\"startswith() requires string inputs\"]",
            "[\"ko\",\"startswith() requires string inputs\"]",
            "[\"ok\",\"\"]",
            "[\"ko\",\"startswith() requires string inputs\"]"
          ],
          "actual": [
            "[\"ko\",\"unknown function ltrimstr\"]",
            "[\"ko\",\"unknown function ltrimstr\"]",
            "[\"ko\",\"unknown function ltrimstr\"]",
            "[\"ko\",\"unknown function ltrimstr\"]"
          ]
        },
        {
          "line": 2523,
          "program": ".[] as [$x, $y] | try [\"ok\", ($x | rtrimstr($y))] catch [\"ko\", .]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[\"ko\",\"endswith() requires string inputs\"]",
            "[\"ko\",\"endswith() requires string inputs\"]",
            "[\"ok\",\"\"]",
            "[\"ko\",\"endswith() requires string inputs\"]"
          ],
          "actual": [
            "[\"ko\",\"unknown function rtrimstr\"]",
            "[\"ko\",\"unknown function rtrimstr\"]",
            "[\"ko\",\"unknown function rtrimstr\"]",
            "[\"ko\",\"unknown function rtrimstr\"]"
          ]
        },
        {
          "line": 2533,
          "program": "try [\"OK\", setpath([[1]]; 1)] catch [\"KO\", .]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[\"KO\",\"Cannot update field at array index of array\"]"
          ],
          "actual": [
            "[\"KO\",\"unknown function setpath\"]"
          ]
        },
        {
          "line": 2538,
          "program": "foreach .[] as $x (0, 1; . + $x)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "1",
            "3",
            "2",
            "4"
          ],
          "actual": [
            "1",
            "2",
            "3",
            "4"
          ]
        },
        {
          "line": 2548,
          "program": "strflocaltime(\"\" | ., @uri)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"\"",
            "\"\""
          ],
          "actual": []
        },
        {
          "line": 2558,
          "program": "reduce range(9999) as $_ ([];[.]) | tojson | fromjson | flatten",
          "status": "fail",
          "detail": "exited 1: Traceback (most recent call last):",
          "expect_failure": false,
          "expected": [
            "[]"
          ],
          "actual": []
        },
        {
          "line": 2563,
          "program": "reduce range(10000) as $_ ([];[.]) | tojson | try (fromjson) catch . | (contains(\"<skipped: too deep>\") | not) and contains(\"Exceeds depth limit for parsing\")",
          "status": "fail",
          "detail": "exited 1: Traceback (most recent call last):",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": []
        },
        {
          "line": 2568,
          "program": "reduce range(10001) as $_ ([];[.]) | tojson | contains(\"<skipped: too deep>\")",
          "status": "fail",
          "detail": "exited 1: Traceback (most recent call last):",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": []
        },
        {
          "line": 2573,
          "program": "setpath([range(10000) | 0]; 0) | flatten",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[0]"
          ],
          "actual": []
        },
        {
          "line": 2577,
          "program": "try setpath([range(10001) | 0]; 0) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Path too deep\""
          ],
          "actual": [
            "\"unknown function setpath\""
          ]
        },
        {
          "line": 2581,
          "program": "getpath([range(10000) | 0])",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "null"
          ],
          "actual": []
        },
        {
          "line": 2585,
          "program": "try getpath([range(10001) | 0]) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Path too deep\""
          ],
          "actual": [
            "\"unknown function getpath\""
          ]
        },
        {
          "line": 2589,
          "program": "delpaths([[range(10000) | 0]])",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "null"
          ],
          "actual": []
        },
        {
          "line": 2593,
          "program": "try delpaths([[range(10001) | 0]]) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Path too deep\""
          ],
          "actual": [
            "\"unknown function delpaths\""
          ]
        },
        {
          "line": 2598,
          "program": "reduce range(10000) as $_ ([]; [.]) | contains([[]])",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": []
        },
        {
          "line": 2602,
          "program": "try (reduce range(10001) as $_ ([]; [.]) as $x | $x | contains($x)) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Containment check too deep\""
          ],
          "actual": [
            "\"unknown function contains\""
          ]
        },
        {
          "line": 2607,
          "program": "reduce range(10000) as $_ ({}; {a: .}) as $x | $x * $x | length",
          "status": "fail",
          "detail": "exited 1: Traceback (most recent call last):",
          "expect_failure": false,
          "expected": [
            "1"
          ],
          "actual": []
        },
        {
          "line": 2611,
          "program": "try (reduce range(10001) as $_ ({}; {a: .}) as $x | $x * $x) catch .",
          "status": "fail",
          "detail": "exited 1: Traceback (most recent call last):",
          "expect_failure": false,
          "expected": [
            "\"Object merge too deep\""
          ],
          "actual": []
        },
        {
          "line": 2616,
          "program": "try ((reduce range(10001) as $_ ([]; [.])) as $x | (reduce range(10001) as $_ ([]; [.])) as $y | $x == $y) catch .",
          "status": "fail",
          "detail": "exited 1: Traceback (most recent call last):",
          "expect_failure": false,
          "expected": [
            "\"Equality check too deep\""
          ],
          "actual": []
        },
        {
          "line": 2621,
          "program": "try ((reduce range(10001) as $_ ([]; [.])) as $x | [$x, $x] | sort) catch .",
          "status": "fail",
          "detail": "exited 1: Traceback (most recent call last):",
          "expect_failure": false,
          "expected": [
            "\"Comparison too deep\""
          ],
          "actual": []
        },
        {
          "line": 2625,
          "program": "try ((reduce range(10001) as $_ ([]; [.])) as $x | [$x, $x] | unique) catch .",
          "status": "fail",
          "detail": "exited 1: Traceback (most recent call last):",
          "expect_failure": false,
          "expected": [
            "\"Comparison too deep\""
          ],
          "actual": []
        },
        {
          "line": 2629,
          "program": "try ((reduce range(10001) as $_ ({}; {a: .})) as $x | [$x, $x] | sort) catch .",
          "status": "fail",
          "detail": "exited 1: Traceback (most recent call last):",
          "expect_failure": false,
          "expected": [
            "\"Comparison too deep\""
          ],
          "actual": []
        },
        {
          "line": 2633,
          "program": "try ((reduce range(10001) as $_ ({}; {a: .})) as $x | [$x, $x] | unique) catch .",
          "status": "fail",
          "detail": "exited 1: Traceback (most recent call last):",
          "expect_failure": false,
          "expected": [
            "\"Comparison too deep\""
          ],
          "actual": []
        }
      ]
    }
  stderr:
    --- drydock: progress ---
    cases: pass=210 fail=245 error=0 skip=9 total=464 from=summary
    --- drydock: end progress ---
    --- drydock: values at failure ---
      summary = {'pass': 210, 'fail': 245, 'error': 0, 'skip': 9}
    --- drydock: end values ---
    Traceback (most recent call last):
      File "parse-003-conformance.py", line 18, in <module>
        assert summary["fail"] == 0 and summary["error"] == 0
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: parse-004-conformance (FEATURE-PARSE-004.md)
  intent: The executable passes every selected corpus case covering declarations, control syntax, bindings, reductions, labels, and required compile failures.
  return code: 1
  stdout:
    {
      "candidate": [
        "/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260822.044627/build/jq/jq"
      ],
      "corpus": "jq.test",
      "summary": {
        "pass": 92,
        "fail": 119,
        "error": 0,
        "skip": 13
      },
      "cases": [
        {
          "line": 200,
          "program": "map(try .a[] catch ., try .a.[] catch ., .a[]?, .a.[]?)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1,2,1,2,1,2,1,2,\"Cannot iterate over number (123)\",\"Cannot iterate over number (123)\"]"
          ],
          "actual": [
            "[1,2,1,2,1,2,1,2,\"cannot iterate over value\",\"cannot iterate over value\"]"
          ]
        },
        {
          "line": 205,
          "program": "try [\"OK\", (.[] | error)] catch [\"KO\", .]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[\"KO\",[\"b\"]]"
          ],
          "actual": [
            "[\"KO\",\"error\"]"
          ]
        },
        {
          "line": 213,
          "program": "try (.foo[-1] = 0) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Out of bounds negative array index\""
          ],
          "actual": [
            "{\"foo\":{\"-1\":0}}"
          ]
        },
        {
          "line": 217,
          "program": "try (.foo[-2] = 0) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Out of bounds negative array index\""
          ],
          "actual": [
            "{\"foo\":{\"-2\":0}}"
          ]
        },
        {
          "line": 229,
          "program": "try (.[999999999] = 0) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Array index too large\""
          ],
          "actual": [
            "{\"999999999\":0}"
          ]
        },
        {
          "line": 324,
          "program": ". as $foo | break $foo",
          "status": "fail",
          "detail": "program was accepted, but the corpus marks it %%FAIL",
          "expect_failure": true,
          "expected": [],
          "actual": []
        },
        {
          "line": 349,
          "program": "[-foreach -.[] as $x (0; . + $x)]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1,3,6]"
          ],
          "actual": [
            "[1]"
          ]
        },
        {
          "line": 353,
          "program": "[foreach .[] / .[] as $i (0; . + $i)]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1,3,3.5,4.5]"
          ],
          "actual": [
            "[1.0,1.5,3.5,4.5]"
          ]
        },
        {
          "line": 405,
          "program": "[nth(0,5,9,10,15; range(.)), try nth(-1; range(.)) catch .]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[0,5,9,\"nth doesn't support negative indices\"]"
          ],
          "actual": []
        },
        {
          "line": 530,
          "program": ". as {as: $kw, \"str\": $str, (\"e\"+\"x\"+\"p\"): $exp} | [$kw, $str, $exp]",
          "status": "fail",
          "detail": "program did not compile: jq: compile error: expected ,",
          "expect_failure": false,
          "expected": [
            "[1, 2, 3]"
          ],
          "actual": []
        },
        {
          "line": 560,
          "program": ". as $foo | [$foo, $bar]",
          "status": "fail",
          "detail": "program was accepted, but the corpus marks it %%FAIL",
          "expect_failure": true,
          "expected": [],
          "actual": []
        },
        {
          "line": 709,
          "program": ".[] | try toboolean catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"null (null) cannot be parsed as a boolean\"",
            "\"number (0) cannot be parsed as a boolean\"",
            "\"string (\\\"tru\\\") cannot be parsed as a boolean\"",
            "\"string (\\\"truee\\\") cannot be parsed as a boolean\"",
            "\"string (\\\"fals\\\") cannot be parsed as a boolean\"",
            "\"string (\\\"falsee\\\") cannot be parsed as a boolean\"",
            "\"array ([]) cannot be parsed as a boolean\"",
            "\"object ({}) cannot be parsed as a boolean\""
          ],
          "actual": [
            "\"unknown function toboolean\"",
            "\"unknown function toboolean\"",
            "\"unknown function toboolean\"",
            "\"unknown function toboolean\"",
            "\"unknown function toboolean\"",
            "\"unknown function toboolean\"",
            "\"unknown function toboolean\"",
            "\"unknown function toboolean\""
          ]
        },
        {
          "line": 720,
          "program": "\"true\\u0000x\", \"false\\u0000\" | try toboolean catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"string (\\\"true\\\\u0000x\\\") cannot be parsed as a boolean\"",
            "\"string (\\\"false\\\\u0000\\\") cannot be parsed as a boolean\""
          ],
          "actual": [
            "\"true\\u0000x\"",
            "\"unknown function toboolean\""
          ]
        },
        {
          "line": 725,
          "program": "[{\"a\":42},.object,10,.num,false,true,null,\"b\",[1,4]] | .[] as $x | [$x == .[]]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[true,  true,  false, false, false, false, false, false, false]",
            "[true,  true,  false, false, false, false, false, false, false]",
            "[false, false, true,  true,  false, false, false, false, false]",
            "[false, false, true,  true,  false, false, false, false, false]",
            "[false, false, false, false, true,  false, false, false, false]",
            "[false, false, false, false, false, true,  false, false, false]",
            "[false, false, false, false, false, false, true,  false, false]",
            "[false, false, false, false, false, false, false, true,  false]",
            "[false, false, false, false, false, false, false, false, true ]"
          ],
          "actual": []
        },
        {
          "line": 745,
          "program": "[.[] | try utf8bytelength catch .]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[\"array ([]) only strings have UTF-8 byte length\",\"object ({}) only strings have UTF-8 byte length\",\"array ([1,2]) only strings have UTF-8 byte length\",\"number (55) only strings have UTF-8 byte length\",\"boolean (true) only strings have UTF-8 byte length\",\"boolean (false) only strings have UTF-8 byte length\"]"
          ],
          "actual": [
            "[\"unknown function utf8bytelength\",\"unknown function utf8bytelength\",\"unknown function utf8bytelength\",\"unknown function utf8bytelength\",\"unknown function utf8bytelength\",\"unknown function utf8bytelength\"]"
          ]
        },
        {
          "line": 798,
          "program": "def f: 1; def g: f, def f: 2; def g: 3; f, def f: g; f, g; def f: 4; [f, def f: g; def g: 5; f, g]+[f,g]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[4,1,2,3,3,5,4,1,2,3,3]"
          ],
          "actual": [
            "[4,5,5,4,4,2,3,3]"
          ]
        },
        {
          "line": 868,
          "program": "def f: .+1; def g: f; def f: .+100; def f(a):a+.+11; [(g|f(20)), f]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[33,101]"
          ],
          "actual": []
        },
        {
          "line": 873,
          "program": "def id(x):x; 2000 as $x | def f(x):1 as $x | id([$x, x, x]); def g(x): 100 as $x | f($x,$x+x); g($x)",
          "status": "fail",
          "detail": "exited 1: Traceback (most recent call last):",
          "expect_failure": false,
          "expected": [
            "[1,100,2100.0,100,2100.0]"
          ],
          "actual": []
        },
        {
          "line": 878,
          "program": "def x(a;b): a as $a | b as $b | $a + $b; def y($a;$b): $a + $b; def check(a;b): [x(a;b)] == [y(a;b)]; check(.[];.[]*2)",
          "status": "fail",
          "detail": "exited 1: Traceback (most recent call last):",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": []
        },
        {
          "line": 884,
          "program": "[[20,10][1,0] as $x | def f: (100,200) as $y | def g: [$x + $y, .]; . + $x | g; f[0] | [f][0][1] | f]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[[110.0, 130.0], [210.0, 130.0], [110.0, 230.0], [210.0, 230.0], [120.0, 160.0], [220.0, 160.0], [120.0, 260.0], [220.0, 260.0]]"
          ],
          "actual": [
            "[[110,130],[210,130],[110,230],[210,230]]"
          ]
        },
        {
          "line": 911,
          "program": "[-reduce -.[] as $x (0; . + $x)]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[6]"
          ],
          "actual": [
            "[1]"
          ]
        },
        {
          "line": 933,
          "program": ". as {$a, $b:[$c, $d]}| [$a, $b, $c, $d]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1,[2,{\"d\":3}],2,{\"d\":3}]"
          ],
          "actual": []
        },
        {
          "line": 938,
          "program": ".[] | . as {$a, b: [$c, {$d}]} ?// [$a, {$b}, $e] ?// $f | [$a, $b, $c, $d, $e, $f]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1, null, 2, 3, null, null]",
            "[4, 5, null, null, 7, null]",
            "[null, null, null, null, null, \"foo\"]"
          ],
          "actual": []
        },
        {
          "line": 1045,
          "program": ". as $dot|any($dot[];not)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": []
        },
        {
          "line": 1049,
          "program": ". as $dot|any($dot[];not)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "false"
          ],
          "actual": []
        },
        {
          "line": 1053,
          "program": ". as $dot|all($dot[];.)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "false"
          ],
          "actual": []
        },
        {
          "line": 1057,
          "program": ". as $dot|all($dot[];.)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": []
        },
        {
          "line": 1123,
          "program": "try path(.a | map(select(.b == 0))) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Invalid path expression with result [{\\\"b\\\":0}]\""
          ],
          "actual": [
            "\"unknown function path\""
          ]
        },
        {
          "line": 1127,
          "program": "try path(.a | map(select(.b == 0)) | .[0]) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Invalid path expression near attempt to access element 0 of [{\\\"b\\\":0}]\""
          ],
          "actual": [
            "\"unknown function path\""
          ]
        },
        {
          "line": 1131,
          "program": "try path(.a | map(select(.b == 0)) | .c) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Invalid path expression near attempt to access element \\\"c\\\" of [{\\\"b\\\":0}]\""
          ],
          "actual": [
            "\"unknown function path\""
          ]
        },
        {
          "line": 1135,
          "program": "try path(.a | map(select(.b == 0)) | .[]) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Invalid path expression near attempt to iterate through [{\\\"b\\\":0}]\""
          ],
          "actual": [
            "\"unknown function path\""
          ]
        },
        {
          "line": 1147,
          "program": "[\"foo\",1] as $p | getpath($p), setpath($p; 20), delpaths([$p])",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"b\"",
            "{\"bar\": 42, \"foo\": [\"a\", 20, \"c\", \"d\"]}",
            "{\"bar\": 42, \"foo\": [\"a\", \"c\", \"d\"]}"
          ],
          "actual": []
        },
        {
          "line": 1163,
          "program": "[\"foo\",1] as $p | getpath($p), setpath($p; 20), delpaths([$p])",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "null",
            "{\"bar\":false, \"foo\": [null, 20]}",
            "{\"bar\":false}"
          ],
          "actual": []
        },
        {
          "line": 1173,
          "program": "try delpaths(0) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Paths must be specified as an array\""
          ],
          "actual": [
            "\"unknown function delpaths\""
          ]
        },
        {
          "line": 1214,
          "program": "try pick(last) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Out of bounds negative array index\""
          ],
          "actual": [
            "\"unknown function pick\""
          ]
        },
        {
          "line": 1253,
          "program": "def inc(x): x |= .+1; inc(.[].a)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[{\"a\":2,\"b\":2},{\"a\":3,\"b\":4},{\"a\":8,\"b\":8}]"
          ],
          "actual": []
        },
        {
          "line": 1258,
          "program": ".[] | try (getpath([\"a\",0,\"b\"]) |= 5) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "{\"a\":[{\"b\":5}]}",
            "{\"b\":0,\"a\":[{\"b\":5}]}",
            "\"Cannot index number with number (0)\"",
            "{\"a\":[{\"b\":5}]}",
            "\"Cannot index number with string (\\\"b\\\")\"",
            "\"Cannot index object with number (0)\"",
            "{\"a\":[{\"b\":5}]}",
            "{\"a\":[{\"c\":3,\"b\":5}]}"
          ],
          "actual": []
        },
        {
          "line": 1290,
          "program": "try ((map(select(.a == 1))[].b) = 10) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Invalid path expression near attempt to iterate through [{\\\"a\\\":1}]\""
          ],
          "actual": []
        },
        {
          "line": 1294,
          "program": "try ((map(select(.a == 1))[].a) |= .+1) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Invalid path expression near attempt to iterate through [{\\\"a\\\":1}]\""
          ],
          "actual": []
        },
        {
          "line": 1302,
          "program": "try (def x: reverse; x=10) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Invalid path expression with result [2,1,0]\""
          ],
          "actual": []
        },
        {
          "line": 1322,
          "program": "[if 1,null,2 then 3 else 4 end]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[3,4,3]"
          ],
          "actual": [
            "[3]"
          ]
        },
        {
          "line": 1326,
          "program": "[if empty then 3 else 4 end]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[]"
          ],
          "actual": [
            "[4]"
          ]
        },
        {
          "line": 1342,
          "program": "[if false then 3 end]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[7]"
          ],
          "actual": [
            "[null]"
          ]
        },
        {
          "line": 1350,
          "program": "[if false then 3 elif false then 4 end]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[7]"
          ],
          "actual": [
            "[null]"
          ]
        },
        {
          "line": 1366,
          "program": "if true then [.] else . end []",
          "status": "fail",
          "detail": "program did not compile: jq: compile error: unexpected token",
          "expect_failure": false,
          "expected": [
            "null"
          ],
          "actual": []
        },
        {
          "line": 1448,
          "program": "[.[]|try if . == 0 then error(\"foo\") elif . == 1 then .a elif . == 2 then empty else . end catch .]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[\"foo\",\"Cannot index number with string (\\\"a\\\")\",3]"
          ],
          "actual": [
            "[\"foo\",\"cannot index value\",3]"
          ]
        },
        {
          "line": 1460,
          "program": "[if error then 1 else 2 end?]",
          "status": "fail",
          "detail": "program did not compile: jq: compile error: expected ]",
          "expect_failure": false,
          "expected": [
            "[]"
          ],
          "actual": []
        },
        {
          "line": 1464,
          "program": "try error(0) // 1",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "1"
          ],
          "actual": []
        },
        {
          "line": 1473,
          "program": "1 + try 2 catch 3 + 4",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "7"
          ],
          "actual": [
            "3"
          ]
        },
        {
          "line": 1481,
          "program": "try -.? catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"string (\\\"foo\\\") cannot be negated\""
          ],
          "actual": []
        },
        {
          "line": 1493,
          "program": ".[] | try error catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "1",
            "null",
            "2"
          ],
          "actual": [
            "\"error\"",
            "\"error\"",
            "\"error\""
          ]
        },
        {
          "line": 1499,
          "program": "try error(\"\\($__loc__)\") catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"{\\\"file\\\":\\\"<top-level>\\\",\\\"line\\\":1}\""
          ],
          "actual": [
            "\"variable $__loc__ is not defined\""
          ]
        },
        {
          "line": 1553,
          "program": "try _strindices(\"abc\") catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"number (123) cannot be searched, as it is not a string\""
          ],
          "actual": [
            "\"unknown function _strindices\""
          ]
        },
        {
          "line": 1557,
          "program": "try _strindices(123) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"number (123) is not a string\""
          ],
          "actual": [
            "\"unknown function _strindices\""
          ]
        },
        {
          "line": 1575,
          "program": "try trim catch ., try ltrim catch ., try rtrim catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"trim input must be a string\"",
            "\"trim input must be a string\"",
            "\"trim input must be a string\""
          ],
          "actual": [
            "\"unknown function trim\"",
            "\"unknown function ltrim\"",
            "\"unknown function rtrim\""
          ]
        },
        {
          "line": 1653,
          "program": "map(.[1] as $needle | .[0] | contains($needle))",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[true, true, true, false, false]"
          ],
          "actual": []
        },
        {
          "line": 1657,
          "program": "map(.[1] as $needle | .[0] | contains($needle))",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[true, true, false]"
          ],
          "actual": []
        },
        {
          "line": 1811,
          "program": "try flatten(-1) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"flatten depth must not be negative\""
          ],
          "actual": [
            "\"unknown function flatten\""
          ]
        },
        {
          "line": 1839,
          "program": "try [\"OK\", bsearch(0)] catch [\"KO\",.]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[\"KO\",\"string (\\\"aa\\\") cannot be searched from\"]"
          ],
          "actual": [
            "[\"KO\",\"unknown function bsearch\"]"
          ]
        },
        {
          "line": 1868,
          "program": "try strftime(\"%Y-%m-%dT%H:%M:%SZ\") catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"strftime/1 requires parsed datetime inputs\""
          ],
          "actual": [
            "\"unknown function strftime\""
          ]
        },
        {
          "line": 1872,
          "program": "try strflocaltime(\"%Y-%m-%dT%H:%M:%SZ\") catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"strflocaltime/1 requires parsed datetime inputs\""
          ],
          "actual": [
            "\"unknown function strflocaltime\""
          ]
        },
        {
          "line": 1876,
          "program": "try mktime catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"mktime requires parsed datetime inputs\""
          ],
          "actual": [
            "\"unknown function mktime\""
          ]
        },
        {
          "line": 1881,
          "program": "try [\"OK\", strftime([])] catch [\"KO\", .]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[\"KO\",\"strftime/1 requires a string format\"]"
          ],
          "actual": [
            "[\"KO\",\"unknown function strftime\"]"
          ]
        },
        {
          "line": 1885,
          "program": "try [\"OK\", strflocaltime({})] catch [\"KO\", .]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[\"KO\",\"strflocaltime/1 requires a string format\"]"
          ],
          "actual": [
            "[\"KO\",\"unknown function strflocaltime\"]"
          ]
        },
        {
          "line": 1900,
          "program": "import \"a\" as foo; import \"b\" as bar; def fooa: foo::a; [fooa, bar::a, bar::b, foo::a]",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": false,
          "expected": [
            "[\"a\",\"b\",\"c\",\"a\"]"
          ],
          "actual": []
        },
        {
          "line": 1904,
          "program": "import \"c\" as foo; [foo::a, foo::c]",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": false,
          "expected": [
            "[0,\"acmehbah\"]"
          ],
          "actual": []
        },
        {
          "line": 1908,
          "program": "include \"c\"; [a, c]",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": false,
          "expected": [
            "[0,\"acmehbah\"]"
          ],
          "actual": []
        },
        {
          "line": 1912,
          "program": "import \"data\" as $e; import \"data\" as $d; [$d[].this,$e[].that,$d::d[].this,$e::e[].that]|join(\";\")",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": false,
          "expected": [
            "\"is a test;is too;is a test;is too\""
          ],
          "actual": []
        },
        {
          "line": 1917,
          "program": "import \"data\" as $a; import \"data\" as $b; def f: {$a, $b}; f",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": false,
          "expected": [
            "{\"a\":[{\"this\":\"is a test\",\"that\":\"is too\"}],\"b\":[{\"this\":\"is a test\",\"that\":\"is too\"}]}"
          ],
          "actual": []
        },
        {
          "line": 1921,
          "program": "include \"shadow1\"; e",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": false,
          "expected": [
            "2"
          ],
          "actual": []
        },
        {
          "line": 1925,
          "program": "include \"shadow1\"; include \"shadow2\"; e",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": false,
          "expected": [
            "3"
          ],
          "actual": []
        },
        {
          "line": 1929,
          "program": "import \"shadow1\" as f; import \"shadow2\" as f; import \"shadow1\" as e; [e::e, f::e]",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": false,
          "expected": [
            "[2,3]"
          ],
          "actual": []
        },
        {
          "line": 1969,
          "program": "modulemeta",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": false,
          "expected": [
            "{\"whatever\":null,\"deps\":[{\"as\":\"foo\",\"is_data\":false,\"relpath\":\"a\"},{\"search\":\"./\",\"as\":\"d\",\"is_data\":false,\"relpath\":\"d\"},{\"search\":\"./\",\"as\":\"d2\",\"is_data\":false,\"relpath\":\"d\"},{\"search\":\"./../lib/jq\",\"as\":\"e\",\"is_data\":false,\"relpath\":\"e\"},{\"search\":\"./../lib/jq\",\"as\":\"f\",\"is_data\":false,\"relpath\":\"f\"},{\"as\":\"d\",\"is_data\":true,\"relpath\":\"data\"}],\"defs\":[\"a/0\",\"c/0\"]}"
          ],
          "actual": []
        },
        {
          "line": 1973,
          "program": "modulemeta | .deps | length",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": false,
          "expected": [
            "6"
          ],
          "actual": []
        },
        {
          "line": 1977,
          "program": "modulemeta | .defs | length",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": false,
          "expected": [
            "2"
          ],
          "actual": []
        },
        {
          "line": 1982,
          "program": "import \"syntaxerror\" as e; .",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": true,
          "expected": [],
          "actual": []
        },
        {
          "line": 1993,
          "program": "import \"test_bind_order\" as check; check::check",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": []
        },
        {
          "line": 1997,
          "program": "try -. catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"string (\\\"very-long-long-long-long...\\\") cannot be negated\""
          ],
          "actual": []
        },
        {
          "line": 2001,
          "program": "try (.-.) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"string (\\\"very-long-long-long-long...\\\") and string (\\\"very-long-long-long-long...\\\") cannot be subtracted\""
          ],
          "actual": []
        },
        {
          "line": 2005,
          "program": "\"x\" * range(0; 12; 2) + \"\u2606\" * 8 | try -. catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"string (\\\"\u2606\u2606\u2606\u2606\u2606\u2606\u2606\u2606\\\") cannot be negated\"",
            "\"string (\\\"xx\u2606\u2606\u2606\u2606\u2606\u2606\u2606\u2606\\\") cannot be negated\"",
            "\"string (\\\"xxxx\u2606\u2606\u2606\u2606\u2606\u2606...\\\") cannot be negated\"",
            "\"string (\\\"xxxxxx\u2606\u2606\u2606\u2606\u2606\u2606...\\\") cannot be negated\"",
            "\"string (\\\"xxxxxxxx\u2606\u2606\u2606\u2606\u2606...\\\") cannot be negated\"",
            "\"string (\\\"xxxxxxxxxx\u2606\u2606\u2606\u2606...\\\") cannot be negated\""
          ],
          "actual": []
        },
        {
          "line": 2014,
          "program": "try (. + \"x\") catch . == if have_decnum then \"number (12345678901234567890123456...) and string (\\\"x\\\") cannot be added\" else \"number (12345678901234568000000000...) and string (\\\"x\\\") cannot be added\" end",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": []
        },
        {
          "line": 2034,
          "program": "try join(\",\") catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"string (\\\"1,2,\\\") and object ({\\\"a\\\":{\\\"b\\\":{\\\"c\\\":33}}}) cannot be added\""
          ],
          "actual": [
            "\"1,2,{\\\"a\\\":{\\\"b\\\":{\\\"c\\\":33}}}\""
          ]
        },
        {
          "line": 2038,
          "program": "try join(\",\") catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"string (\\\"1,2,\\\") and array ([3,4,5]) cannot be added\""
          ],
          "actual": [
            "\"1,2,[3,4,5]\""
          ]
        },
        {
          "line": 2067,
          "program": "[range(-52;52;1)] as $powers | [$powers[]|pow(2;.)|log2|round] == $powers",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": []
        },
        {
          "line": 2130,
          "program": "(.a as $x | .b) = \"b\"",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "{\"a\":null,\"b\":\"b\"}"
          ],
          "actual": []
        },
        {
          "line": 2196,
          "program": ".[0] | tostring | . == if have_decnum then \"13911860366432393\" else \"13911860366432392\" end",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": []
        },
        {
          "line": 2200,
          "program": ".x | tojson | . == if have_decnum then \"13911860366432393\" else \"13911860366432392\" end",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": []
        },
        {
          "line": 2204,
          "program": "(13911860366432393 == 13911860366432392) | . == if have_decnum then false else true end",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": []
        },
        {
          "line": 2224,
          "program": "-. | tojson == if have_decnum then \"-13911860366432393\" else \"-13911860366432392\" end",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": []
        },
        {
          "line": 2228,
          "program": "-. | tojson == if have_decnum then \"0.12345678901234567890123456789\" else \"0.12345678901234568\" end",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": []
        },
        {
          "line": 2232,
          "program": "[1E+1000,-1E+1000 | tojson] == if have_decnum then [\"1E+1000\",\"-1E+1000\"] else [\"1.7976931348623157e+308\",\"-1.7976931348623157e+308\"] end",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": []
        },
        {
          "line": 2241,
          "program": ".[] as $n | $n+0 | [., tostring, . == $n]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[-9007199254740992,\"-9007199254740992\",true]",
            "[-9007199254740992,\"-9007199254740992\",true]",
            "[9007199254740992,\"9007199254740992\",true]",
            "[9007199254740992,\"9007199254740992\",true]",
            "[13911860366432392,\"13911860366432392\",true]"
          ],
          "actual": [
            "[-9007199254740993,\"-9007199254740993\",true]",
            "[-9007199254740992,\"-9007199254740992\",true]",
            "[9007199254740992,\"9007199254740992\",true]",
            "[9007199254740993,\"9007199254740993\",true]",
            "[13911860366432393,\"13911860366432393\",true]"
          ]
        },
        {
          "line": 2271,
          "program": "[1E+1000,-1E+1000 | abs | tojson] | unique == if have_decnum then [\"1E+1000\"] else [\"1.7976931348623157e+308\"] end",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": []
        },
        {
          "line": 2275,
          "program": "[1E+1000,-1E+1000 | length | tojson] | unique == if have_decnum then [\"1E+1000\"] else [\"1.7976931348623157e+308\"] end",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": []
        },
        {
          "line": 2285,
          "program": "[ label $if | range(10) | ., (select(. == 5) | break $if) ]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[0,1,2,3,4,5]"
          ],
          "actual": []
        },
        {
          "line": 2293,
          "program": "1 as $foreach | 2 as $and | 3 as $or | { $foreach, $and, $or, a }",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "{\"foreach\":1,\"and\":2,\"or\":3,\"a\":4}"
          ],
          "actual": [
            "{\"1\":1,\"2\":2,\"3\":3,\"a\":4}"
          ]
        },
        {
          "line": 2308,
          "program": "1 as $x | \"2\" as $y | \"3\" as $z | { $x, as, $y: 4, ($z): 5, if: 6, foo: 7 }",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "{\"x\":1,\"as\":8,\"2\":4,\"3\":5,\"if\":6,\"foo\":7}"
          ],
          "actual": [
            "{\"1\":1,\"as\":8,\"2\":4,\"3\":5,\"if\":6,\"foo\":7}"
          ]
        },
        {
          "line": 2324,
          "program": ".[] | try (fromjson | isnan) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "true",
            "true",
            "\"Invalid numeric literal at EOF at line 1, column 4 (while parsing 'NaN1')\"",
            "\"Invalid numeric literal at EOF at line 1, column 5 (while parsing 'NaN10')\"",
            "\"Invalid numeric literal at EOF at line 1, column 6 (while parsing 'NaN100')\"",
            "\"Invalid numeric literal at EOF at line 1, column 7 (while parsing 'NaN1000')\"",
            "\"Invalid numeric literal at EOF at line 1, column 8 (while parsing 'NaN10000')\"",
            "\"Invalid numeric literal at EOF at line 1, column 9 (while parsing 'NaN100000')\""
          ],
          "actual": [
            "\"unknown function isnan\"",
            "\"invalid JSON\"",
            "\"invalid JSON\"",
            "\"invalid JSON\"",
            "\"invalid JSON\"",
            "\"invalid JSON\"",
            "\"invalid JSON\"",
            "\"invalid JSON\""
          ]
        },
        {
          "line": 2337,
          "program": "try input catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"break\""
          ],
          "actual": [
            "\"unknown function input\""
          ]
        },
        {
          "line": 2354,
          "program": "try ([\"hi\",\"ho\"]|.[]|(try . catch (if .==\"ho\" then \"BROKEN\"|error else empty end)) | if .==\"ho\" then error else \"\\(.) there!\" end) catch \"caught outside \\(.)\"",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"hi there!\"",
            "\"caught outside ho\""
          ],
          "actual": [
            "\"hi there!\"",
            "\"caught outside error\""
          ]
        },
        {
          "line": 2363,
          "program": "try (try error catch \"inner catch \\(.)\") catch \"outer catch \\(.)\"",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"inner catch foo\""
          ],
          "actual": [
            "\"inner catch error\""
          ]
        },
        {
          "line": 2367,
          "program": "try ((try error catch \"inner catch \\(.)\")|error) catch \"outer catch \\(.)\"",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"outer catch inner catch foo\""
          ],
          "actual": [
            "\"outer catch error\""
          ]
        },
        {
          "line": 2390,
          "program": ".[] |= try tonumber",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1, 3, 6.7, 0.89, -876, 5.43, 21]"
          ],
          "actual": [
            "[1,null,3,4,5,6.7,null,-876,null,21]"
          ]
        },
        {
          "line": 2407,
          "program": "map(try implode catch .)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[\"implode input must be an array\",\"string (\\\"a\\\") can't be imploded, unicode codepoint needs to be numeric\",\"number (null) can't be imploded, unicode codepoint needs to be numeric\"]"
          ],
          "actual": []
        },
        {
          "line": 2411,
          "program": "try 0[implode] catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Cannot index number with string (\\\"\\\")\""
          ],
          "actual": [
            "\"unknown function implode\""
          ]
        },
        {
          "line": 2475,
          "program": "try ([range(3)] | .[nan] = 9) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Cannot set array element at NaN index\""
          ],
          "actual": []
        },
        {
          "line": 2479,
          "program": "try (\"foobar\" | .[1.5:3.5] = \"xyz\") catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Cannot update string slices\""
          ],
          "actual": []
        },
        {
          "line": 2483,
          "program": "try ([range(10)] | .[1.5:3.5] = [\"xyz\"]) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[0,\"xyz\",4,5,6,7,8,9]"
          ],
          "actual": []
        },
        {
          "line": 2487,
          "program": "try (\"foobar\" | .[1.5]) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Cannot index string with number (1.5)\""
          ],
          "actual": [
            "\"cannot index string with number\""
          ]
        },
        {
          "line": 2494,
          "program": "try [\"ok\", setpath([1]; 1)] catch [\"ko\", .]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[\"ko\",\"Cannot index object with number (1)\"]"
          ],
          "actual": [
            "[\"ko\",\"unknown function setpath\"]"
          ]
        },
        {
          "line": 2498,
          "program": "try fromjson catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Invalid string literal; expected \\\", but got ' at line 1, column 5 (while parsing '{'a': 123}')\""
          ],
          "actual": [
            "\"invalid JSON\""
          ]
        },
        {
          "line": 2504,
          "program": "try ltrimstr(1) catch \"x\", try rtrimstr(1) catch \"x\" | \"ok\"",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"ok\"",
            "\"ok\""
          ],
          "actual": [
            "\"x\"",
            "\"ok\""
          ]
        },
        {
          "line": 2509,
          "program": "try ltrimstr(\"x\") catch \"x\", try rtrimstr(\"x\") catch \"x\" | \"ok\"",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"ok\"",
            "\"ok\""
          ],
          "actual": [
            "\"x\"",
            "\"ok\""
          ]
        },
        {
          "line": 2516,
          "program": ".[] as [$x, $y] | try [\"ok\", ($x | ltrimstr($y))] catch [\"ko\", .]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[\"ko\",\"startswith() requires string inputs\"]",
            "[\"ko\",\"startswith() requires string inputs\"]",
            "[\"ok\",\"\"]",
            "[\"ko\",\"startswith() requires string inputs\"]"
          ],
          "actual": [
            "[\"ko\",\"unknown function ltrimstr\"]",
            "[\"ko\",\"unknown function ltrimstr\"]",
            "[\"ko\",\"unknown function ltrimstr\"]",
            "[\"ko\",\"unknown function ltrimstr\"]"
          ]
        },
        {
          "line": 2523,
          "program": ".[] as [$x, $y] | try [\"ok\", ($x | rtrimstr($y))] catch [\"ko\", .]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[\"ko\",\"endswith() requires string inputs\"]",
            "[\"ko\",\"endswith() requires string inputs\"]",
            "[\"ok\",\"\"]",
            "[\"ko\",\"endswith() requires string inputs\"]"
          ],
          "actual": [
            "[\"ko\",\"unknown function rtrimstr\"]",
            "[\"ko\",\"unknown function rtrimstr\"]",
            "[\"ko\",\"unknown function rtrimstr\"]",
            "[\"ko\",\"unknown function rtrimstr\"]"
          ]
        },
        {
          "line": 2533,
          "program": "try [\"OK\", setpath([[1]]; 1)] catch [\"KO\", .]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[\"KO\",\"Cannot update field at array index of array\"]"
          ],
          "actual": [
            "[\"KO\",\"unknown function setpath\"]"
          ]
        },
        {
          "line": 2538,
          "program": "foreach .[] as $x (0, 1; . + $x)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "1",
            "3",
            "2",
            "4"
          ],
          "actual": [
            "1",
            "2",
            "3",
            "4"
          ]
        },
        {
          "line": 2558,
          "program": "reduce range(9999) as $_ ([];[.]) | tojson | fromjson | flatten",
          "status": "fail",
          "detail": "exited 1: Traceback (most recent call last):",
          "expect_failure": false,
          "expected": [
            "[]"
          ],
          "actual": []
        },
        {
          "line": 2563,
          "program": "reduce range(10000) as $_ ([];[.]) | tojson | try (fromjson) catch . | (contains(\"<skipped: too deep>\") | not) and contains(\"Exceeds depth limit for parsing\")",
          "status": "fail",
          "detail": "exited 1: Traceback (most recent call last):",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": []
        },
        {
          "line": 2568,
          "program": "reduce range(10001) as $_ ([];[.]) | tojson | contains(\"<skipped: too deep>\")",
          "status": "fail",
          "detail": "exited 1: Traceback (most recent call last):",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": []
        },
        {
          "line": 2577,
          "program": "try setpath([range(10001) | 0]; 0) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Path too deep\""
          ],
          "actual": [
            "\"unknown function setpath\""
          ]
        },
        {
          "line": 2585,
          "program": "try getpath([range(10001) | 0]) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Path too deep\""
          ],
          "actual": [
            "\"unknown function getpath\""
          ]
        },
        {
          "line": 2593,
          "program": "try delpaths([[range(10001) | 0]]) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Path too deep\""
          ],
          "actual": [
            "\"unknown function delpaths\""
          ]
        },
        {
          "line": 2598,
          "program": "reduce range(10000) as $_ ([]; [.]) | contains([[]])",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": []
        },
        {
          "line": 2602,
          "program": "try (reduce range(10001) as $_ ([]; [.]) as $x | $x | contains($x)) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Containment check too deep\""
          ],
          "actual": [
            "\"unknown function contains\""
          ]
        },
        {
          "line": 2607,
          "program": "reduce range(10000) as $_ ({}; {a: .}) as $x | $x * $x | length",
          "status": "fail",
          "detail": "exited 1: Traceback (most recent call last):",
          "expect_failure": false,
          "expected": [
            "1"
          ],
          "actual": []
        },
        {
          "line": 2611,
          "program": "try (reduce range(10001) as $_ ({}; {a: .}) as $x | $x * $x) catch .",
          "status": "fail",
          "detail": "exited 1: Traceback (most recent call last):",
          "expect_failure": false,
          "expected": [
            "\"Object merge too deep\""
          ],
          "actual": []
        },
        {
          "line": 2616,
          "program": "try ((reduce range(10001) as $_ ([]; [.])) as $x | (reduce range(10001) as $_ ([]; [.])) as $y | $x == $y) catch .",
          "status": "fail",
          "detail": "exited 1: Traceback (most recent call last):",
          "expect_failure": false,
          "expected": [
            "\"Equality check too deep\""
          ],
          "actual": []
        },
        {
          "line": 2621,
          "program": "try ((reduce range(10001) as $_ ([]; [.])) as $x | [$x, $x] | sort) catch .",
          "status": "fail",
          "detail": "exited 1: Traceback (most recent call last):",
          "expect_failure": false,
          "expected": [
            "\"Comparison too deep\""
          ],
          "actual": []
        },
        {
          "line": 2625,
          "program": "try ((reduce range(10001) as $_ ([]; [.])) as $x | [$x, $x] | unique) catch .",
          "status": "fail",
          "detail": "exited 1: Traceback (most recent call last):",
          "expect_failure": false,
          "expected": [
            "\"Comparison too deep\""
          ],
          "actual": []
        },
        {
          "line": 2629,
          "program": "try ((reduce range(10001) as $_ ({}; {a: .})) as $x | [$x, $x] | sort) catch .",
          "status": "fail",
          "detail": "exited 1: Traceback (most recent call last):",
          "expect_failure": false,
          "expected": [
            "\"Comparison too deep\""
          ],
          "actual": []
        },
        {
          "line": 2633,
          "program": "try ((reduce range(10001) as $_ ({}; {a: .})) as $x | [$x, $x] | unique) catch .",
          "status": "fail",
          "detail": "exited 1: Traceback (most recent call last):",
          "expect_failure": false,
          "expected": [
            "\"Comparison too deep\""
          ],
          "actual": []
        }
      ]
    }
  stderr:
    --- drydock: progress ---
    cases: pass=92 fail=119 error=0 skip=13 total=224 from=summary
    --- drydock: end progress ---
    --- drydock: values at failure ---
      summary = {'pass': 92, 'fail': 119, 'error': 0, 'skip': 13}
    --- drydock: end values ---
    Traceback (most recent call last):
      File "parse-004-conformance.py", line 18, in <module>
        assert summary["fail"] == 0 and summary["error"] == 0
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError

## Post-build programmatic acceptance
- FAIL: parse-003-conformance (FEATURE-PARSE-003.md)
  intent: The executable passes every selected corpus case exercising expression punctuation, accessors, collections, and operators.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 1
  stdout:
    {
      "candidate": [
        "/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260822.044627/build/jq/jq"
      ],
      "corpus": "jq.test",
      "summary": {
        "pass": 331,
        "fail": 124,
        "error": 0,
        "skip": 9
      },
      "cases": [
        {
          "line": 195,
          "program": "[.[]|.[1:3]?]",
          "status": "fail",
          "detail": "exited 1: Traceback (most recent call last):",
          "expect_failure": false,
          "expected": [
            "[null,\"bc\",[],[2,3],[2]]"
          ],
          "actual": []
        },
        {
          "line": 229,
          "program": "try (.[999999999] = 0) catch .",
          "status": "fail",
          "detail": "exited 1: Traceback (most recent call last):",
          "expect_failure": false,
          "expected": [
            "\"Array index too large\""
          ],
          "actual": []
        },
        {
          "line": 311,
          "program": "[while(.<100; .*2)]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1,2,4,8,16,32,64]"
          ],
          "actual": []
        },
        {
          "line": 329,
          "program": "[.[]|[.,1]|until(.[0] < 1; [.[0] - 1, .[1] * .[0]])|.[1]]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1,2,6,24,120]"
          ],
          "actual": []
        },
        {
          "line": 353,
          "program": "[foreach .[] / .[] as $i (0; . + $i)]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1,3,3.5,4.5]"
          ],
          "actual": [
            "[1.0,1.5,3.5,4.5]"
          ]
        },
        {
          "line": 365,
          "program": "[limit(0; error)]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[]"
          ],
          "actual": []
        },
        {
          "line": 369,
          "program": "[limit(1; 1, error)]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1]"
          ],
          "actual": []
        },
        {
          "line": 381,
          "program": "[skip(0,2,3,4; .[])]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1,2,3,3]"
          ],
          "actual": [
            "[1,2,3]"
          ]
        },
        {
          "line": 405,
          "program": "[nth(0,5,9,10,15; range(.)), try nth(-1; range(.)) catch .]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[0,5,9,\"nth doesn't support negative indices\"]"
          ],
          "actual": []
        },
        {
          "line": 420,
          "program": "[limit(5,7; range(9))]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[0,1,2,3,4,0,1,2,3,4,5,6]"
          ],
          "actual": [
            "[0,1,2,3,4]"
          ]
        },
        {
          "line": 425,
          "program": "[nth(5,7; range(9;0;-1))]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[4,2]"
          ],
          "actual": []
        },
        {
          "line": 440,
          "program": "[(index(\",\",\"|\"), rindex(\",\",\"|\")), indices(\",\",\"|\")]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1,3,22,19,[1,5,7,12,14,16,18,20,22],[3,9,10,17,19]]"
          ],
          "actual": []
        },
        {
          "line": 474,
          "program": "del(.[2:4],.[0],.[-2:])",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1,4,5]"
          ],
          "actual": []
        },
        {
          "line": 478,
          "program": ".[2:4] = ([], [\"a\",\"b\"], [\"a\",\"b\",\"c\"])",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[0,1,4,5,6,7]",
            "[0,1,\"a\",\"b\",4,5,6,7]",
            "[0,1,\"a\",\"b\",\"c\",4,5,6,7]"
          ],
          "actual": []
        },
        {
          "line": 617,
          "program": "{\"a\":1} + {\"b\":2} + {\"c\":3}",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "{\"a\":1, \"b\":2, \"c\":3}"
          ],
          "actual": []
        },
        {
          "line": 633,
          "program": "[1,2,3,4,1] - [.,3]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[2,4]"
          ],
          "actual": []
        },
        {
          "line": 661,
          "program": "9E999999999, 9999999999E999999990, 1E-999999999, 0.000000001E-999999990",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "9E+999999999",
            "9.999999999E+999999999",
            "1E-999999999",
            "1E-999999999"
          ],
          "actual": [
            "null",
            "null",
            "0.0",
            "0.0"
          ]
        },
        {
          "line": 689,
          "program": "[(infinite, -infinite) % (1, -1, infinite)]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[0,0,0,0,0,-1]"
          ],
          "actual": []
        },
        {
          "line": 693,
          "program": "[nan % 1, 1 % nan | isnan]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[true,true]"
          ],
          "actual": [
            "[null,true]"
          ]
        },
        {
          "line": 798,
          "program": "def f: 1; def g: f, def f: 2; def g: 3; f, def f: g; f, g; def f: 4; [f, def f: g; def g: 5; f, g]+[f,g]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[4,1,2,3,3,5,4,1,2,3,3]"
          ],
          "actual": [
            "[4,5,5,4,4,2,3,3]"
          ]
        },
        {
          "line": 868,
          "program": "def f: .+1; def g: f; def f: .+100; def f(a):a+.+11; [(g|f(20)), f]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[33,101]"
          ],
          "actual": [
            "[132,101]"
          ]
        },
        {
          "line": 873,
          "program": "def id(x):x; 2000 as $x | def f(x):1 as $x | id([$x, x, x]); def g(x): 100 as $x | f($x,$x+x); g($x)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1,100,2100.0,100,2100.0]"
          ],
          "actual": [
            "[1,1,1]"
          ]
        },
        {
          "line": 938,
          "program": ".[] | . as {$a, b: [$c, {$d}]} ?// [$a, {$b}, $e] ?// $f | [$a, $b, $c, $d, $e, $f]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1, null, 2, 3, null, null]",
            "[4, 5, null, null, 7, null]",
            "[null, null, null, null, null, \"foo\"]"
          ],
          "actual": []
        },
        {
          "line": 1062,
          "program": "any(true, error; .)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": []
        },
        {
          "line": 1066,
          "program": "all(false, error; .)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "false"
          ],
          "actual": []
        },
        {
          "line": 1115,
          "program": "path(.[] | select(.>3))",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1]"
          ],
          "actual": []
        },
        {
          "line": 1123,
          "program": "try path(.a | map(select(.b == 0))) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Invalid path expression with result [{\\\"b\\\":0}]\""
          ],
          "actual": [
            "\"Invalid path expression\""
          ]
        },
        {
          "line": 1127,
          "program": "try path(.a | map(select(.b == 0)) | .[0]) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Invalid path expression near attempt to access element 0 of [{\\\"b\\\":0}]\""
          ],
          "actual": [
            "\"Invalid path expression\""
          ]
        },
        {
          "line": 1131,
          "program": "try path(.a | map(select(.b == 0)) | .c) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Invalid path expression near attempt to access element \\\"c\\\" of [{\\\"b\\\":0}]\""
          ],
          "actual": [
            "\"Invalid path expression\""
          ]
        },
        {
          "line": 1135,
          "program": "try path(.a | map(select(.b == 0)) | .[]) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Invalid path expression near attempt to iterate through [{\\\"b\\\":0}]\""
          ],
          "actual": [
            "\"Invalid path expression\""
          ]
        },
        {
          "line": 1177,
          "program": "del(.), del(empty), del((.foo,.bar,.baz) | .[2,3,0]), del(.foo[0], .bar[0], .foo, .baz.bar[0].x)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "null",
            "{\"foo\": [0,1,2,3,4], \"bar\": [0,1]}",
            "{\"foo\": [1,4], \"bar\": [1]}",
            "{\"bar\": [1]}"
          ],
          "actual": []
        },
        {
          "line": 1184,
          "program": "del(.[1], .[-6], .[2], .[-3:9])",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[0, 3, 5, 6, 9]"
          ],
          "actual": []
        },
        {
          "line": 1188,
          "program": "del(.[nan])",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1,2,3]"
          ],
          "actual": []
        },
        {
          "line": 1192,
          "program": "del(.[nan,nan])",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1,2,3]"
          ],
          "actual": []
        },
        {
          "line": 1201,
          "program": "pick(.a.b.c)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "{\"a\":{\"b\":{\"c\":null}}}"
          ],
          "actual": []
        },
        {
          "line": 1214,
          "program": "try pick(last) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Out of bounds negative array index\""
          ],
          "actual": [
            "\"unknown function pick\""
          ]
        },
        {
          "line": 1253,
          "program": "def inc(x): x |= .+1; inc(.[].a)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[{\"a\":2,\"b\":2},{\"a\":3,\"b\":4},{\"a\":8,\"b\":8}]"
          ],
          "actual": []
        },
        {
          "line": 1258,
          "program": ".[] | try (getpath([\"a\",0,\"b\"]) |= 5) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "{\"a\":[{\"b\":5}]}",
            "{\"b\":0,\"a\":[{\"b\":5}]}",
            "\"Cannot index number with number (0)\"",
            "{\"a\":[{\"b\":5}]}",
            "\"Cannot index number with string (\\\"b\\\")\"",
            "\"Cannot index object with number (0)\"",
            "{\"a\":[{\"b\":5}]}",
            "{\"a\":[{\"c\":3,\"b\":5}]}"
          ],
          "actual": []
        },
        {
          "line": 1270,
          "program": "(.[] | select(. >= 2)) |= empty",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1,0]"
          ],
          "actual": []
        },
        {
          "line": 1278,
          "program": ".foo[1,4,2,3] |= empty",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "{\"foo\":[0,5]}"
          ],
          "actual": [
            "{\"foo\":[0,4,5]}"
          ]
        },
        {
          "line": 1290,
          "program": "try ((map(select(.a == 1))[].b) = 10) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Invalid path expression near attempt to iterate through [{\\\"a\\\":1}]\""
          ],
          "actual": []
        },
        {
          "line": 1294,
          "program": "try ((map(select(.a == 1))[].a) |= .+1) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Invalid path expression near attempt to iterate through [{\\\"a\\\":1}]\""
          ],
          "actual": []
        },
        {
          "line": 1298,
          "program": "def x: .[1,2]; x=10",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[0,10,10]"
          ],
          "actual": []
        },
        {
          "line": 1302,
          "program": "try (def x: reverse; x=10) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Invalid path expression with result [2,1,0]\""
          ],
          "actual": []
        },
        {
          "line": 1306,
          "program": ".[] = 1",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1,1,1,1,1,1]"
          ],
          "actual": []
        },
        {
          "line": 1370,
          "program": "[.[] | [.foo[] // .bar]]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[[1,2], [1], [3], [42], [41]]"
          ],
          "actual": [
            "[[1,2,1,2],[1],[3,3,3],[],[41,41,41]]"
          ]
        },
        {
          "line": 1374,
          "program": ".[] //= .[0]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[\"hello\",true,\"hello\",[false],\"hello\"]"
          ],
          "actual": []
        },
        {
          "line": 1464,
          "program": "try error(0) // 1",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "1"
          ],
          "actual": []
        },
        {
          "line": 1481,
          "program": "try -.? catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"string (\\\"foo\\\") cannot be negated\""
          ],
          "actual": [
            "\"bad operand type for unary -: 'str'\""
          ]
        },
        {
          "line": 1499,
          "program": "try error(\"\\($__loc__)\") catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"{\\\"file\\\":\\\"<top-level>\\\",\\\"line\\\":1}\""
          ],
          "actual": [
            "\"variable $__loc__ is not defined\""
          ]
        },
        {
          "line": 1544,
          "program": "[(index(\",\"), rindex(\",\")), indices(\",\")]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1,13,[1,4,8,13]]"
          ],
          "actual": []
        },
        {
          "line": 1548,
          "program": "[ index(\"aba\"), rindex(\"aba\"), indices(\"aba\") ]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1,7,[1,3,5,7]]"
          ],
          "actual": []
        },
        {
          "line": 1553,
          "program": "try _strindices(\"abc\") catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"number (123) cannot be searched, as it is not a string\""
          ],
          "actual": [
            "\"unknown function _strindices\""
          ]
        },
        {
          "line": 1557,
          "program": "try _strindices(123) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"number (123) is not a string\""
          ],
          "actual": [
            "\"unknown function _strindices\""
          ]
        },
        {
          "line": 1575,
          "program": "try trim catch ., try ltrim catch ., try rtrim catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"trim input must be a string\"",
            "\"trim input must be a string\"",
            "\"trim input must be a string\""
          ],
          "actual": [
            "\"trim input must be a string\"",
            "\"ltrim input must be a string\"",
            "\"rtrim input must be a string\""
          ]
        },
        {
          "line": 1585,
          "program": "indices([1,2])",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1,8]"
          ],
          "actual": [
            "1",
            "8"
          ]
        },
        {
          "line": 1589,
          "program": "indices([1,2])",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[]"
          ],
          "actual": []
        },
        {
          "line": 1625,
          "program": "[.[] * \"abc\"]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[null,null,\"\",\"\",\"abc\",\"abc\",\"abcabcabc\",\"abcabcabcabcabcabcabcabcabcabc\"]"
          ],
          "actual": [
            "[\"\",\"\",\"\",\"\",\"abc\",\"abc\",\"abcabcabc\",\"abcabcabcabcabcabcabcabcabcabc\"]"
          ]
        },
        {
          "line": 1629,
          "program": "[. * (nan,-nan)]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[null,null]"
          ],
          "actual": []
        },
        {
          "line": 1677,
          "program": "(sort_by(.b) | sort_by(.a)), sort_by(.a, .b), sort_by(.b, .c), group_by(.b), group_by(.a + .b - .c == 2)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[{\"a\": 0, \"b\": 2, \"c\": 43}, {\"a\": 1, \"b\": 4, \"c\": 14}, {\"a\": 1, \"b\": 4, \"c\": 3}, {\"a\": 4, \"b\": 1, \"c\": 3}]",
            "[{\"a\": 0, \"b\": 2, \"c\": 43}, {\"a\": 1, \"b\": 4, \"c\": 14}, {\"a\": 1, \"b\": 4, \"c\": 3}, {\"a\": 4, \"b\": 1, \"c\": 3}]",
            "[{\"a\": 4, \"b\": 1, \"c\": 3}, {\"a\": 0, \"b\": 2, \"c\": 43}, {\"a\": 1, \"b\": 4, \"c\": 3}, {\"a\": 1, \"b\": 4, \"c\": 14}]",
            "[[{\"a\": 4, \"b\": 1, \"c\": 3}], [{\"a\": 0, \"b\": 2, \"c\": 43}], [{\"a\": 1, \"b\": 4, \"c\": 14}, {\"a\": 1, \"b\": 4, \"c\": 3}]]",
            "[[{\"a\": 1, \"b\": 4, \"c\": 14}, {\"a\": 0, \"b\": 2, \"c\": 43}], [{\"a\": 4, \"b\": 1, \"c\": 3}, {\"a\": 1, \"b\": 4, \"c\": 3}]]"
          ],
          "actual": []
        },
        {
          "line": 1693,
          "program": "[min, max, min_by(.[1]), max_by(.[1]), min_by(.[2]), max_by(.[2])]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[[1,3,\"a\"],[4,2,\"a\"],[3,1,\"a\"],[2,4,\"a\"],[4,2,\"a\"],[1,3,\"a\"]]"
          ],
          "actual": []
        },
        {
          "line": 1697,
          "program": "[min,max,min_by(.),max_by(.)]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[null,null,null,null]"
          ],
          "actual": []
        },
        {
          "line": 1701,
          "program": ".foo[.baz]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "4"
          ],
          "actual": [
            "null"
          ]
        },
        {
          "line": 1721,
          "program": "with_entries(.key |= \"KEY_\" + .)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "{\"KEY_a\": 1, \"KEY_b\": 2}"
          ],
          "actual": []
        },
        {
          "line": 1741,
          "program": "[][.]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "null"
          ],
          "actual": []
        },
        {
          "line": 1745,
          "program": "map([1,2][0:.])",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[[1], [1], [1,2], [1,2], [1,2]]"
          ],
          "actual": []
        },
        {
          "line": 1835,
          "program": "bsearch({x:1})",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "1"
          ],
          "actual": []
        },
        {
          "line": 1839,
          "program": "try [\"OK\", bsearch(0)] catch [\"KO\",.]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[\"KO\",\"string (\\\"aa\\\") cannot be searched from\"]"
          ],
          "actual": [
            "[\"KO\",\"unknown function bsearch\"]"
          ]
        },
        {
          "line": 1843,
          "program": "strftime(\"%Y-%m-%dT%H:%M:%SZ\")",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"2015-03-05T23:51:47Z\""
          ],
          "actual": []
        },
        {
          "line": 1847,
          "program": "strftime(\"%A, %B %d, %Y\")",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Tuesday, June 30, 2015\""
          ],
          "actual": []
        },
        {
          "line": 1851,
          "program": "strftime(\"%Y-%m-%dT%H:%M:%SZ\")",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"2024-03-15T00:00:00Z\""
          ],
          "actual": []
        },
        {
          "line": 1863,
          "program": "gmtime[5]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "47.25"
          ],
          "actual": []
        },
        {
          "line": 1868,
          "program": "try strftime(\"%Y-%m-%dT%H:%M:%SZ\") catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"strftime/1 requires parsed datetime inputs\""
          ],
          "actual": [
            "\"unknown function strftime\""
          ]
        },
        {
          "line": 1872,
          "program": "try strflocaltime(\"%Y-%m-%dT%H:%M:%SZ\") catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"strflocaltime/1 requires parsed datetime inputs\""
          ],
          "actual": [
            "\"unknown function strflocaltime\""
          ]
        },
        {
          "line": 1876,
          "program": "try mktime catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"mktime requires parsed datetime inputs\""
          ],
          "actual": [
            "\"unknown function mktime\""
          ]
        },
        {
          "line": 1881,
          "program": "try [\"OK\", strftime([])] catch [\"KO\", .]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[\"KO\",\"strftime/1 requires a string format\"]"
          ],
          "actual": [
            "[\"KO\",\"unknown function strftime\"]"
          ]
        },
        {
          "line": 1885,
          "program": "try [\"OK\", strflocaltime({})] catch [\"KO\", .]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[\"KO\",\"strflocaltime/1 requires a string format\"]"
          ],
          "actual": [
            "[\"KO\",\"unknown function strflocaltime\"]"
          ]
        },
        {
          "line": 1889,
          "program": "[strptime(\"%Y-%m-%dT%H:%M:%SZ\")|(.,mktime)]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[[2015,2,5,23,51,47,4,63],1425599507]"
          ],
          "actual": []
        },
        {
          "line": 1895,
          "program": "last(range(365 * 67)|(\"1970-03-01T01:02:03Z\"|strptime(\"%Y-%m-%dT%H:%M:%SZ\")|mktime) + (86400 * .)|strftime(\"%Y-%m-%dT%H:%M:%SZ\")|strptime(\"%Y-%m-%dT%H:%M:%SZ\"))",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[2037,1,11,1,2,3,3,41]"
          ],
          "actual": []
        },
        {
          "line": 1900,
          "program": "import \"a\" as foo; import \"b\" as bar; def fooa: foo::a; [fooa, bar::a, bar::b, foo::a]",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": false,
          "expected": [
            "[\"a\",\"b\",\"c\",\"a\"]"
          ],
          "actual": []
        },
        {
          "line": 1904,
          "program": "import \"c\" as foo; [foo::a, foo::c]",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": false,
          "expected": [
            "[0,\"acmehbah\"]"
          ],
          "actual": []
        },
        {
          "line": 1908,
          "program": "include \"c\"; [a, c]",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": false,
          "expected": [
            "[0,\"acmehbah\"]"
          ],
          "actual": []
        },
        {
          "line": 1912,
          "program": "import \"data\" as $e; import \"data\" as $d; [$d[].this,$e[].that,$d::d[].this,$e::e[].that]|join(\";\")",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": false,
          "expected": [
            "\"is a test;is too;is a test;is too\""
          ],
          "actual": []
        },
        {
          "line": 1917,
          "program": "import \"data\" as $a; import \"data\" as $b; def f: {$a, $b}; f",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": false,
          "expected": [
            "{\"a\":[{\"this\":\"is a test\",\"that\":\"is too\"}],\"b\":[{\"this\":\"is a test\",\"that\":\"is too\"}]}"
          ],
          "actual": []
        },
        {
          "line": 1929,
          "program": "import \"shadow1\" as f; import \"shadow2\" as f; import \"shadow1\" as e; [e::e, f::e]",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": false,
          "expected": [
            "[2,3]"
          ],
          "actual": []
        },
        {
          "line": 1973,
          "program": "modulemeta | .deps | length",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": false,
          "expected": [
            "6"
          ],
          "actual": []
        },
        {
          "line": 1977,
          "program": "modulemeta | .defs | length",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": false,
          "expected": [
            "2"
          ],
          "actual": []
        },
        {
          "line": 1982,
          "program": "import \"syntaxerror\" as e; .",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": true,
          "expected": [],
          "actual": []
        },
        {
          "line": 1997,
          "program": "try -. catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"string (\\\"very-long-long-long-long...\\\") cannot be negated\""
          ],
          "actual": [
            "\"bad operand type for unary -: 'str'\""
          ]
        },
        {
          "line": 2001,
          "program": "try (.-.) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"string (\\\"very-long-long-long-long...\\\") and string (\\\"very-long-long-long-long...\\\") cannot be subtracted\""
          ],
          "actual": [
            "\"unsupported operand type(s) for -: 'str' and 'str'\""
          ]
        },
        {
          "line": 2005,
          "program": "\"x\" * range(0; 12; 2) + \"\u2606\" * 8 | try -. catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"string (\\\"\u2606\u2606\u2606\u2606\u2606\u2606\u2606\u2606\\\") cannot be negated\"",
            "\"string (\\\"xx\u2606\u2606\u2606\u2606\u2606\u2606\u2606\u2606\\\") cannot be negated\"",
            "\"string (\\\"xxxx\u2606\u2606\u2606\u2606\u2606\u2606...\\\") cannot be negated\"",
            "\"string (\\\"xxxxxx\u2606\u2606\u2606\u2606\u2606\u2606...\\\") cannot be negated\"",
            "\"string (\\\"xxxxxxxx\u2606\u2606\u2606\u2606\u2606...\\\") cannot be negated\"",
            "\"string (\\\"xxxxxxxxxx\u2606\u2606\u2606\u2606...\\\") cannot be negated\""
          ],
          "actual": [
            "\"bad operand type for unary -: 'str'\"",
            "\"bad operand type for unary -: 'str'\"",
            "\"bad operand type for unary -: 'str'\"",
            "\"bad operand type for unary -: 'str'\"",
            "\"bad operand type for unary -: 'str'\"",
            "\"bad operand type for unary -: 'str'\""
          ]
        },
        {
          "line": 2014,
          "program": "try (. + \"x\") catch . == if have_decnum then \"number (12345678901234567890123456...) and string (\\\"x\\\") cannot be added\" else \"number (12345678901234568000000000...) and string (\\\"x\\\") cannot be added\" end",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": [
            "false"
          ]
        },
        {
          "line": 2034,
          "program": "try join(\",\") catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"string (\\\"1,2,\\\") and object ({\\\"a\\\":{\\\"b\\\":{\\\"c\\\":33}}}) cannot be added\""
          ],
          "actual": [
            "\"1,2,{\\\"a\\\":{\\\"b\\\":{\\\"c\\\":33}}}\""
          ]
        },
        {
          "line": 2038,
          "program": "try join(\",\") catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"string (\\\"1,2,\\\") and array ([3,4,5]) cannot be added\""
          ],
          "actual": [
            "\"1,2,[3,4,5]\""
          ]
        },
        {
          "line": 2086,
          "program": "(.[{}] = 0)?",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [],
          "actual": [
            "{\"{}\":0}"
          ]
        },
        {
          "line": 2089,
          "program": "INDEX(range(5)|[., \"foo\\(.)\"]; .[0])",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "{\"0\":[0,\"foo0\"],\"1\":[1,\"foo1\"],\"2\":[2,\"foo2\"],\"3\":[3,\"foo3\"],\"4\":[4,\"foo4\"]}"
          ],
          "actual": []
        },
        {
          "line": 2093,
          "program": "JOIN({\"0\":[0,\"abc\"],\"1\":[1,\"bcd\"],\"2\":[2,\"def\"],\"3\":[3,\"efg\"],\"4\":[4,\"fgh\"]}; .[0]|tostring)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[[[5,\"foo\"],null],[[3,\"bar\"],[3,\"efg\"]],[[1,\"foobar\"],[1,\"bcd\"]]]"
          ],
          "actual": []
        },
        {
          "line": 2135,
          "program": "(.. | select(type == \"object\" and has(\"b\") and (.b | type) == \"array\")|.b) |= .[0]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "{\"a\": {\"b\": 1}}"
          ],
          "actual": []
        },
        {
          "line": 2161,
          "program": "\"-1\"|IN(builtins[] / \"/\"|.[1])",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "false"
          ],
          "actual": []
        },
        {
          "line": 2165,
          "program": "all(builtins[] / \"/\"; .[1]|tonumber >= 0)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": []
        },
        {
          "line": 2169,
          "program": "builtins|any(.[:1] == \"_\")",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "false"
          ],
          "actual": []
        },
        {
          "line": 2196,
          "program": ".[0] | tostring | . == if have_decnum then \"13911860366432393\" else \"13911860366432392\" end",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": [
            "false"
          ]
        },
        {
          "line": 2200,
          "program": ".x | tojson | . == if have_decnum then \"13911860366432393\" else \"13911860366432392\" end",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": [
            "false"
          ]
        },
        {
          "line": 2204,
          "program": "(13911860366432393 == 13911860366432392) | . == if have_decnum then false else true end",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": [
            "false"
          ]
        },
        {
          "line": 2211,
          "program": ". - 10",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "13911860366432382"
          ],
          "actual": [
            "13911860366432383"
          ]
        },
        {
          "line": 2215,
          "program": ".[0] - 10",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "13911860366432382"
          ],
          "actual": [
            "13911860366432383"
          ]
        },
        {
          "line": 2219,
          "program": ".x - 10",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "13911860366432382"
          ],
          "actual": [
            "13911860366432383"
          ]
        },
        {
          "line": 2224,
          "program": "-. | tojson == if have_decnum then \"-13911860366432393\" else \"-13911860366432392\" end",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": [
            "false"
          ]
        },
        {
          "line": 2232,
          "program": "[1E+1000,-1E+1000 | tojson] == if have_decnum then [\"1E+1000\",\"-1E+1000\"] else [\"1.7976931348623157e+308\",\"-1.7976931348623157e+308\"] end",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": [
            "false"
          ]
        },
        {
          "line": 2241,
          "program": ".[] as $n | $n+0 | [., tostring, . == $n]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[-9007199254740992,\"-9007199254740992\",true]",
            "[-9007199254740992,\"-9007199254740992\",true]",
            "[9007199254740992,\"9007199254740992\",true]",
            "[9007199254740992,\"9007199254740992\",true]",
            "[13911860366432392,\"13911860366432392\",true]"
          ],
          "actual": [
            "[-9007199254740993,\"-9007199254740993\",true]",
            "[-9007199254740992,\"-9007199254740992\",true]",
            "[9007199254740992,\"9007199254740992\",true]",
            "[9007199254740993,\"9007199254740993\",true]",
            "[13911860366432393,\"13911860366432393\",true]"
          ]
        },
        {
          "line": 2271,
          "program": "[1E+1000,-1E+1000 | abs | tojson] | unique == if have_decnum then [\"1E+1000\"] else [\"1.7976931348623157e+308\"] end",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": [
            "false"
          ]
        },
        {
          "line": 2275,
          "program": "[1E+1000,-1E+1000 | length | tojson] | unique == if have_decnum then [\"1E+1000\"] else [\"1.7976931348623157e+308\"] end",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": []
        },
        {
          "line": 2304,
          "program": "{ a, $__loc__, c }",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "{\"a\":[1,2,3],\"__loc__\":{\"file\":\"<top-level>\",\"line\":1},\"c\":{\"hi\":\"hey\"}}"
          ],
          "actual": []
        },
        {
          "line": 2324,
          "program": ".[] | try (fromjson | isnan) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "true",
            "true",
            "\"Invalid numeric literal at EOF at line 1, column 4 (while parsing 'NaN1')\"",
            "\"Invalid numeric literal at EOF at line 1, column 5 (while parsing 'NaN10')\"",
            "\"Invalid numeric literal at EOF at line 1, column 6 (while parsing 'NaN100')\"",
            "\"Invalid numeric literal at EOF at line 1, column 7 (while parsing 'NaN1000')\"",
            "\"Invalid numeric literal at EOF at line 1, column 8 (while parsing 'NaN10000')\"",
            "\"Invalid numeric literal at EOF at line 1, column 9 (while parsing 'NaN100000')\""
          ],
          "actual": [
            "true",
            "\"invalid JSON\"",
            "\"invalid JSON\"",
            "\"invalid JSON\"",
            "\"invalid JSON\"",
            "\"invalid JSON\"",
            "\"invalid JSON\"",
            "\"invalid JSON\""
          ]
        },
        {
          "line": 2337,
          "program": "try input catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"break\""
          ],
          "actual": [
            "\"unknown function input\""
          ]
        },
        {
          "line": 2390,
          "program": ".[] |= try tonumber",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1, 3, 6.7, 0.89, -876, 5.43, 21]"
          ],
          "actual": [
            "[1,3,4,5,6.7,-876,21]"
          ]
        },
        {
          "line": 2407,
          "program": "map(try implode catch .)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[\"implode input must be an array\",\"string (\\\"a\\\") can't be imploded, unicode codepoint needs to be numeric\",\"number (null) can't be imploded, unicode codepoint needs to be numeric\"]"
          ],
          "actual": []
        },
        {
          "line": 2411,
          "program": "try 0[implode] catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Cannot index number with string (\\\"\\\")\""
          ],
          "actual": [
            "\"implode input must be an array\""
          ]
        },
        {
          "line": 2416,
          "program": "walk(.)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "{\"x\":0}"
          ],
          "actual": []
        },
        {
          "line": 2425,
          "program": "[walk(.,1)]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[{\"x\":0},1]"
          ],
          "actual": []
        },
        {
          "line": 2430,
          "program": "walk(select(IN({}, []) | not))",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "{\"a\":1}"
          ],
          "actual": []
        },
        {
          "line": 2455,
          "program": "[[range(10)] | .[1.1,1.5,1.7]]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1,1,1]"
          ],
          "actual": []
        },
        {
          "line": 2471,
          "program": "[range(3)] | .[nan]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "null"
          ],
          "actual": []
        },
        {
          "line": 2475,
          "program": "try ([range(3)] | .[nan] = 9) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Cannot set array element at NaN index\""
          ],
          "actual": [
            "\"cannot convert float NaN to integer\""
          ]
        },
        {
          "line": 2479,
          "program": "try (\"foobar\" | .[1.5:3.5] = \"xyz\") catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Cannot update string slices\""
          ],
          "actual": []
        },
        {
          "line": 2483,
          "program": "try ([range(10)] | .[1.5:3.5] = [\"xyz\"]) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[0,\"xyz\",4,5,6,7,8,9]"
          ],
          "actual": []
        },
        {
          "line": 2494,
          "program": "try [\"ok\", setpath([1]; 1)] catch [\"ko\", .]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[\"ko\",\"Cannot index object with number (1)\"]"
          ],
          "actual": [
            "[\"ok\",{\"hi\":\"hello\",\"1\":1}]"
          ]
        },
        {
          "line": 2498,
          "program": "try fromjson catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Invalid string literal; expected \\\", but got ' at line 1, column 5 (while parsing '{'a': 123}')\""
          ],
          "actual": [
            "\"invalid JSON\""
          ]
        },
        {
          "line": 2533,
          "program": "try [\"OK\", setpath([[1]]; 1)] catch [\"KO\", .]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[\"KO\",\"Cannot update field at array index of array\"]"
          ],
          "actual": [
            "[\"KO\",\"int() argument must be a string, a bytes-like object or a real number, not 'list'\"]"
          ]
        },
        {
          "line": 2548,
          "program": "strflocaltime(\"\" | ., @uri)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"\"",
            "\"\""
          ],
          "actual": []
        },
        {
          "line": 2593,
          "program": "try delpaths([[range(10001) | 0]]) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Path too deep\""
          ],
          "actual": [
            "null"
          ]
        },
        {
          "line": 2602,
          "program": "try (reduce range(10001) as $_ ([]; [.]) as $x | $x | contains($x)) catch .",
          "status": "fail",
          "detail": "exited 1: Traceback (most recent call last):",
          "expect_failure": false,
          "expected": [
            "\"Containment check too deep\""
          ],
          "actual": []
        },
        {
          "line": 2607,
          "program": "reduce range(10000) as $_ ({}; {a: .}) as $x | $x * $x | length",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "1"
          ],
          "actual": []
        }
      ]
    }
  stderr:
    --- drydock: progress ---
    cases: pass=331 fail=124 error=0 skip=9 total=464 from=summary
    --- drydock: end progress ---
    --- drydock: values at failure ---
      summary = {'pass': 331, 'fail': 124, 'error': 0, 'skip': 9}
    --- drydock: end values ---
    Traceback (most recent call last):
      File "parse-003-conformance.py", line 18, in <module>
        assert summary["fail"] == 0 and summary["error"] == 0
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- FAIL: parse-004-conformance (FEATURE-PARSE-004.md)
  intent: The executable passes every selected corpus case covering declarations, control syntax, bindings, reductions, labels, and required compile failures.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 1
  stdout:
    {
      "candidate": [
        "/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260822.044627/build/jq/jq"
      ],
      "corpus": "jq.test",
      "summary": {
        "pass": 153,
        "fail": 58,
        "error": 0,
        "skip": 13
      },
      "cases": [
        {
          "line": 229,
          "program": "try (.[999999999] = 0) catch .",
          "status": "fail",
          "detail": "exited 1: Traceback (most recent call last):",
          "expect_failure": false,
          "expected": [
            "\"Array index too large\""
          ],
          "actual": []
        },
        {
          "line": 353,
          "program": "[foreach .[] / .[] as $i (0; . + $i)]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1,3,3.5,4.5]"
          ],
          "actual": [
            "[1.0,1.5,3.5,4.5]"
          ]
        },
        {
          "line": 405,
          "program": "[nth(0,5,9,10,15; range(.)), try nth(-1; range(.)) catch .]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[0,5,9,\"nth doesn't support negative indices\"]"
          ],
          "actual": []
        },
        {
          "line": 798,
          "program": "def f: 1; def g: f, def f: 2; def g: 3; f, def f: g; f, g; def f: 4; [f, def f: g; def g: 5; f, g]+[f,g]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[4,1,2,3,3,5,4,1,2,3,3]"
          ],
          "actual": [
            "[4,5,5,4,4,2,3,3]"
          ]
        },
        {
          "line": 868,
          "program": "def f: .+1; def g: f; def f: .+100; def f(a):a+.+11; [(g|f(20)), f]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[33,101]"
          ],
          "actual": [
            "[132,101]"
          ]
        },
        {
          "line": 873,
          "program": "def id(x):x; 2000 as $x | def f(x):1 as $x | id([$x, x, x]); def g(x): 100 as $x | f($x,$x+x); g($x)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1,100,2100.0,100,2100.0]"
          ],
          "actual": [
            "[1,1,1]"
          ]
        },
        {
          "line": 938,
          "program": ".[] | . as {$a, b: [$c, {$d}]} ?// [$a, {$b}, $e] ?// $f | [$a, $b, $c, $d, $e, $f]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1, null, 2, 3, null, null]",
            "[4, 5, null, null, 7, null]",
            "[null, null, null, null, null, \"foo\"]"
          ],
          "actual": []
        },
        {
          "line": 1123,
          "program": "try path(.a | map(select(.b == 0))) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Invalid path expression with result [{\\\"b\\\":0}]\""
          ],
          "actual": [
            "\"Invalid path expression\""
          ]
        },
        {
          "line": 1127,
          "program": "try path(.a | map(select(.b == 0)) | .[0]) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Invalid path expression near attempt to access element 0 of [{\\\"b\\\":0}]\""
          ],
          "actual": [
            "\"Invalid path expression\""
          ]
        },
        {
          "line": 1131,
          "program": "try path(.a | map(select(.b == 0)) | .c) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Invalid path expression near attempt to access element \\\"c\\\" of [{\\\"b\\\":0}]\""
          ],
          "actual": [
            "\"Invalid path expression\""
          ]
        },
        {
          "line": 1135,
          "program": "try path(.a | map(select(.b == 0)) | .[]) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Invalid path expression near attempt to iterate through [{\\\"b\\\":0}]\""
          ],
          "actual": [
            "\"Invalid path expression\""
          ]
        },
        {
          "line": 1214,
          "program": "try pick(last) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Out of bounds negative array index\""
          ],
          "actual": [
            "\"unknown function pick\""
          ]
        },
        {
          "line": 1253,
          "program": "def inc(x): x |= .+1; inc(.[].a)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[{\"a\":2,\"b\":2},{\"a\":3,\"b\":4},{\"a\":8,\"b\":8}]"
          ],
          "actual": []
        },
        {
          "line": 1258,
          "program": ".[] | try (getpath([\"a\",0,\"b\"]) |= 5) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "{\"a\":[{\"b\":5}]}",
            "{\"b\":0,\"a\":[{\"b\":5}]}",
            "\"Cannot index number with number (0)\"",
            "{\"a\":[{\"b\":5}]}",
            "\"Cannot index number with string (\\\"b\\\")\"",
            "\"Cannot index object with number (0)\"",
            "{\"a\":[{\"b\":5}]}",
            "{\"a\":[{\"c\":3,\"b\":5}]}"
          ],
          "actual": []
        },
        {
          "line": 1290,
          "program": "try ((map(select(.a == 1))[].b) = 10) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Invalid path expression near attempt to iterate through [{\\\"a\\\":1}]\""
          ],
          "actual": []
        },
        {
          "line": 1294,
          "program": "try ((map(select(.a == 1))[].a) |= .+1) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Invalid path expression near attempt to iterate through [{\\\"a\\\":1}]\""
          ],
          "actual": []
        },
        {
          "line": 1298,
          "program": "def x: .[1,2]; x=10",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[0,10,10]"
          ],
          "actual": []
        },
        {
          "line": 1302,
          "program": "try (def x: reverse; x=10) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Invalid path expression with result [2,1,0]\""
          ],
          "actual": []
        },
        {
          "line": 1464,
          "program": "try error(0) // 1",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "1"
          ],
          "actual": []
        },
        {
          "line": 1481,
          "program": "try -.? catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"string (\\\"foo\\\") cannot be negated\""
          ],
          "actual": [
            "\"bad operand type for unary -: 'str'\""
          ]
        },
        {
          "line": 1499,
          "program": "try error(\"\\($__loc__)\") catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"{\\\"file\\\":\\\"<top-level>\\\",\\\"line\\\":1}\""
          ],
          "actual": [
            "\"variable $__loc__ is not defined\""
          ]
        },
        {
          "line": 1553,
          "program": "try _strindices(\"abc\") catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"number (123) cannot be searched, as it is not a string\""
          ],
          "actual": [
            "\"unknown function _strindices\""
          ]
        },
        {
          "line": 1557,
          "program": "try _strindices(123) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"number (123) is not a string\""
          ],
          "actual": [
            "\"unknown function _strindices\""
          ]
        },
        {
          "line": 1575,
          "program": "try trim catch ., try ltrim catch ., try rtrim catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"trim input must be a string\"",
            "\"trim input must be a string\"",
            "\"trim input must be a string\""
          ],
          "actual": [
            "\"trim input must be a string\"",
            "\"ltrim input must be a string\"",
            "\"rtrim input must be a string\""
          ]
        },
        {
          "line": 1839,
          "program": "try [\"OK\", bsearch(0)] catch [\"KO\",.]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[\"KO\",\"string (\\\"aa\\\") cannot be searched from\"]"
          ],
          "actual": [
            "[\"KO\",\"unknown function bsearch\"]"
          ]
        },
        {
          "line": 1868,
          "program": "try strftime(\"%Y-%m-%dT%H:%M:%SZ\") catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"strftime/1 requires parsed datetime inputs\""
          ],
          "actual": [
            "\"unknown function strftime\""
          ]
        },
        {
          "line": 1872,
          "program": "try strflocaltime(\"%Y-%m-%dT%H:%M:%SZ\") catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"strflocaltime/1 requires parsed datetime inputs\""
          ],
          "actual": [
            "\"unknown function strflocaltime\""
          ]
        },
        {
          "line": 1876,
          "program": "try mktime catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"mktime requires parsed datetime inputs\""
          ],
          "actual": [
            "\"unknown function mktime\""
          ]
        },
        {
          "line": 1881,
          "program": "try [\"OK\", strftime([])] catch [\"KO\", .]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[\"KO\",\"strftime/1 requires a string format\"]"
          ],
          "actual": [
            "[\"KO\",\"unknown function strftime\"]"
          ]
        },
        {
          "line": 1885,
          "program": "try [\"OK\", strflocaltime({})] catch [\"KO\", .]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[\"KO\",\"strflocaltime/1 requires a string format\"]"
          ],
          "actual": [
            "[\"KO\",\"unknown function strflocaltime\"]"
          ]
        },
        {
          "line": 1900,
          "program": "import \"a\" as foo; import \"b\" as bar; def fooa: foo::a; [fooa, bar::a, bar::b, foo::a]",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": false,
          "expected": [
            "[\"a\",\"b\",\"c\",\"a\"]"
          ],
          "actual": []
        },
        {
          "line": 1904,
          "program": "import \"c\" as foo; [foo::a, foo::c]",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": false,
          "expected": [
            "[0,\"acmehbah\"]"
          ],
          "actual": []
        },
        {
          "line": 1908,
          "program": "include \"c\"; [a, c]",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": false,
          "expected": [
            "[0,\"acmehbah\"]"
          ],
          "actual": []
        },
        {
          "line": 1912,
          "program": "import \"data\" as $e; import \"data\" as $d; [$d[].this,$e[].that,$d::d[].this,$e::e[].that]|join(\";\")",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": false,
          "expected": [
            "\"is a test;is too;is a test;is too\""
          ],
          "actual": []
        },
        {
          "line": 1917,
          "program": "import \"data\" as $a; import \"data\" as $b; def f: {$a, $b}; f",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": false,
          "expected": [
            "{\"a\":[{\"this\":\"is a test\",\"that\":\"is too\"}],\"b\":[{\"this\":\"is a test\",\"that\":\"is too\"}]}"
          ],
          "actual": []
        },
        {
          "line": 1921,
          "program": "include \"shadow1\"; e",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": false,
          "expected": [
            "2"
          ],
          "actual": []
        },
        {
          "line": 1925,
          "program": "include \"shadow1\"; include \"shadow2\"; e",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": false,
          "expected": [
            "3"
          ],
          "actual": []
        },
        {
          "line": 1929,
          "program": "import \"shadow1\" as f; import \"shadow2\" as f; import \"shadow1\" as e; [e::e, f::e]",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": false,
          "expected": [
            "[2,3]"
          ],
          "actual": []
        },
        {
          "line": 1969,
          "program": "modulemeta",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": false,
          "expected": [
            "{\"whatever\":null,\"deps\":[{\"as\":\"foo\",\"is_data\":false,\"relpath\":\"a\"},{\"search\":\"./\",\"as\":\"d\",\"is_data\":false,\"relpath\":\"d\"},{\"search\":\"./\",\"as\":\"d2\",\"is_data\":false,\"relpath\":\"d\"},{\"search\":\"./../lib/jq\",\"as\":\"e\",\"is_data\":false,\"relpath\":\"e\"},{\"search\":\"./../lib/jq\",\"as\":\"f\",\"is_data\":false,\"relpath\":\"f\"},{\"as\":\"d\",\"is_data\":true,\"relpath\":\"data\"}],\"defs\":[\"a/0\",\"c/0\"]}"
          ],
          "actual": []
        },
        {
          "line": 1973,
          "program": "modulemeta | .deps | length",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": false,
          "expected": [
            "6"
          ],
          "actual": []
        },
        {
          "line": 1977,
          "program": "modulemeta | .defs | length",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": false,
          "expected": [
            "2"
          ],
          "actual": []
        },
        {
          "line": 1982,
          "program": "import \"syntaxerror\" as e; .",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": true,
          "expected": [],
          "actual": []
        },
        {
          "line": 1993,
          "program": "import \"test_bind_order\" as check; check::check",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": []
        },
        {
          "line": 1997,
          "program": "try -. catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"string (\\\"very-long-long-long-long...\\\") cannot be negated\""
          ],
          "actual": [
            "\"bad operand type for unary -: 'str'\""
          ]
        },
        {
          "line": 2001,
          "program": "try (.-.) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"string (\\\"very-long-long-long-long...\\\") and string (\\\"very-long-long-long-long...\\\") cannot be subtracted\""
          ],
          "actual": [
            "\"unsupported operand type(s) for -: 'str' and 'str'\""
          ]
        },
        {
          "line": 2005,
          "program": "\"x\" * range(0; 12; 2) + \"\u2606\" * 8 | try -. catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"string (\\\"\u2606\u2606\u2606\u2606\u2606\u2606\u2606\u2606\\\") cannot be negated\"",
            "\"string (\\\"xx\u2606\u2606\u2606\u2606\u2606\u2606\u2606\u2606\\\") cannot be negated\"",
            "\"string (\\\"xxxx\u2606\u2606\u2606\u2606\u2606\u2606...\\\") cannot be negated\"",
            "\"string (\\\"xxxxxx\u2606\u2606\u2606\u2606\u2606\u2606...\\\") cannot be negated\"",
            "\"string (\\\"xxxxxxxx\u2606\u2606\u2606\u2606\u2606...\\\") cannot be negated\"",
            "\"string (\\\"xxxxxxxxxx\u2606\u2606\u2606\u2606...\\\") cannot be negated\""
          ],
          "actual": [
            "\"bad operand type for unary -: 'str'\"",
            "\"bad operand type for unary -: 'str'\"",
            "\"bad operand type for unary -: 'str'\"",
            "\"bad operand type for unary -: 'str'\"",
            "\"bad operand type for unary -: 'str'\"",
            "\"bad operand type for unary -: 'str'\""
          ]
        },
        {
          "line": 2014,
          "program": "try (. + \"x\") catch . == if have_decnum then \"number (12345678901234567890123456...) and string (\\\"x\\\") cannot be added\" else \"number (12345678901234568000000000...) and string (\\\"x\\\") cannot be added\" end",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": [
            "false"
          ]
        },
        {
          "line": 2034,
          "program": "try join(\",\") catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"string (\\\"1,2,\\\") and object ({\\\"a\\\":{\\\"b\\\":{\\\"c\\\":33}}}) cannot be added\""
          ],
          "actual": [
            "\"1,2,{\\\"a\\\":{\\\"b\\\":{\\\"c\\\":33}}}\""
          ]
        },
        {
          "line": 2038,
          "program": "try join(\",\") catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"string (\\\"1,2,\\\") and array ([3,4,5]) cannot be added\""
          ],
          "actual": [
            "\"1,2,[3,4,5]\""
          ]
        },
        {
          "line": 2196,
          "program": ".[0] | tostring | . == if have_decnum then \"13911860366432393\" else \"13911860366432392\" end",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": [
            "false"
          ]
        },
        {
          "line": 2200,
          "program": ".x | tojson | . == if have_decnum then \"13911860366432393\" else \"13911860366432392\" end",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": [
            "false"
          ]
        },
        {
          "line": 2204,
          "program": "(13911860366432393 == 13911860366432392) | . == if have_decnum then false else true end",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": [
            "false"
          ]
        },
        {
          "line": 2224,
          "program": "-. | tojson == if have_decnum then \"-13911860366432393\" else \"-13911860366432392\" end",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": [
            "false"
          ]
        },
        {
          "line": 2232,
          "program": "[1E+1000,-1E+1000 | tojson] == if have_decnum then [\"1E+1000\",\"-1E+1000\"] else [\"1.7976931348623157e+308\",\"-1.7976931348623157e+308\"] end",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": [
            "false"
          ]
        },
        {
          "line": 2241,
          "program": ".[] as $n | $n+0 | [., tostring, . == $n]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[-9007199254740992,\"-9007199254740992\",true]",
            "[-9007199254740992,\"-9007199254740992\",true]",
            "[9007199254740992,\"9007199254740992\",true]",
            "[9007199254740992,\"9007199254740992\",true]",
            "[13911860366432392,\"13911860366432392\",true]"
          ],
          "actual": [
            "[-9007199254740993,\"-9007199254740993\",true]",
            "[-9007199254740992,\"-9007199254740992\",true]",
            "[9007199254740992,\"9007199254740992\",true]",
            "[9007199254740993,\"9007199254740993\",true]",
            "[13911860366432393,\"13911860366432393\",true]"
          ]
        },
        {
          "line": 2271,
          "program": "[1E+1000,-1E+1000 | abs | tojson] | unique == if have_decnum then [\"1E+1000\"] else [\"1.7976931348623157e+308\"] end",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": [
            "false"
          ]
        },
        {
          "line": 2275,
          "program": "[1E+1000,-1E+1000 | length | tojson] | unique == if have_decnum then [\"1E+1000\"] else [\"1.7976931348623157e+308\"] end",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "true"
          ],
          "actual": []
        },
        {
          "line": 2324,
          "program": ".[] | try (fromjson | isnan) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "true",
            "true",
            "\"Invalid numeric literal at EOF at line 1, column 4 (while parsing 'NaN1')\"",
            "\"Invalid numeric literal at EOF at line 1, column 5 (while parsing 'NaN10')\"",
            "\"Invalid numeric literal at EOF at line 1, column 6 (while parsing 'NaN100')\"",
            "\"Invalid numeric literal at EOF at line 1, column 7 (while parsing 'NaN1000')\"",
            "\"Invalid numeric literal at EOF at line 1, column 8 (while parsing 'NaN10000')\"",
            "\"Invalid numeric literal at EOF at line 1, column 9 (while parsing 'NaN100000')\""
          ],
          "actual": [
            "true",
            "\"invalid JSON\"",
            "\"invalid JSON\"",
            "\"invalid JSON\"",
            "\"invalid JSON\"",
            "\"invalid JSON\"",
            "\"invalid JSON\"",
            "\"invalid JSON\""
          ]
        },
        {
          "line": 2337,
          "program": "try input catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"break\""
          ],
          "actual": [
            "\"unknown function input\""
          ]
        },
        {
          "line": 2390,
          "program": ".[] |= try tonumber",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1, 3, 6.7, 0.89, -876, 5.43, 21]"
          ],
          "actual": [
            "[1,3,4,5,6.7,-876,21]"
          ]
        },
        {
          "line": 2407,
          "program": "map(try implode catch .)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[\"implode input must be an array\",\"string (\\\"a\\\") can't be imploded, unicode codepoint needs to be numeric\",\"number (null) can't be imploded, unicode codepoint needs to be numeric\"]"
          ],
          "actual": []
        },
        {
          "line": 2411,
          "program": "try 0[implode] catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Cannot index number with string (\\\"\\\")\""
          ],
          "actual": [
            "\"implode input must be an array\""
          ]
        },
        {
          "line": 2475,
          "program": "try ([range(3)] | .[nan] = 9) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Cannot set array element at NaN index\""
          ],
          "actual": [
            "\"cannot convert float NaN to integer\""
          ]
        },
        {
          "line": 2479,
          "program": "try (\"foobar\" | .[1.5:3.5] = \"xyz\") catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Cannot update string slices\""
          ],
          "actual": []
        },
        {
          "line": 2483,
          "program": "try ([range(10)] | .[1.5:3.5] = [\"xyz\"]) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[0,\"xyz\",4,5,6,7,8,9]"
          ],
          "actual": []
        },
        {
          "line": 2494,
          "program": "try [\"ok\", setpath([1]; 1)] catch [\"ko\", .]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[\"ko\",\"Cannot index object with number (1)\"]"
          ],
          "actual": [
            "[\"ok\",{\"hi\":\"hello\",\"1\":1}]"
          ]
        },
        {
          "line": 2498,
          "program": "try fromjson catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Invalid string literal; expected \\\", but got ' at line 1, column 5 (while parsing '{'a': 123}')\""
          ],
          "actual": [
            "\"invalid JSON\""
          ]
        },
        {
          "line": 2533,
          "program": "try [\"OK\", setpath([[1]]; 1)] catch [\"KO\", .]",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[\"KO\",\"Cannot update field at array index of array\"]"
          ],
          "actual": [
            "[\"KO\",\"int() argument must be a string, a bytes-like object or a real number, not 'list'\"]"
          ]
        },
        {
          "line": 2593,
          "program": "try delpaths([[range(10001) | 0]]) catch .",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "\"Path too deep\""
          ],
          "actual": [
            "null"
          ]
        },
        {
          "line": 2602,
          "program": "try (reduce range(10001) as $_ ([]; [.]) as $x | $x | contains($x)) catch .",
          "status": "fail",
          "detail": "exited 1: Traceback (most recent call last):",
          "expect_failure": false,
          "expected": [
            "\"Containment check too deep\""
          ],
          "actual": []
        },
        {
          "line": 2607,
          "program": "reduce range(10000) as $_ ({}; {a: .}) as $x | $x * $x | length",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "1"
          ],
          "actual": []
        }
      ]
    }
  stderr:
    --- drydock: progress ---
    cases: pass=153 fail=58 error=0 skip=13 total=224 from=summary
    --- drydock: end progress ---
    --- drydock: values at failure ---
      summary = {'pass': 153, 'fail': 58, 'error': 0, 'skip': 13}
    --- drydock: end values ---
    Traceback (most recent call last):
      File "parse-004-conformance.py", line 18, in <module>
        assert summary["fail"] == 0 and summary["error"] == 0
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError

## Repair attempts
- attempt 0 (initial build): failed; 0/2 checks; 340/688 cases model=gpt-5.6-luna; execution 20260822.220746.747Z-525f03f6; reason: programmatic acceptance failed: parse-003-conformance, parse-004-conformance
- attempt 1 (repair 1): failed; 0/2 checks; 369/688 cases model=gpt-5.6-luna; execution 20260822.222140.216Z-50c59f2d; reason: programmatic acceptance failed: parse-003-conformance, parse-004-conformance
- attempt 2 (repair 2): failed; 0/2 checks; 397/688 cases model=gpt-5.6-luna; execution 20260822.223147.922Z-75b9cff2; reason: programmatic acceptance failed: parse-003-conformance, parse-004-conformance
- attempt 3 (repair 3): failed; 0/2 checks; 412/688 cases model=gpt-5.6-luna; execution 20260822.224330.910Z-6102de7b; reason: programmatic acceptance failed: parse-003-conformance, parse-004-conformance
- attempt 4 (repair 4): failed; 0/2 checks; 422/688 cases model=gpt-5.6-luna; execution 20260822.225404.795Z-9d946a42; reason: programmatic acceptance failed: parse-003-conformance, parse-004-conformance
- attempt 5 (repair 5): failed; 0/2 checks; 449/688 cases model=gpt-5.6-luna; execution 20260822.230353.199Z-399c8a04; reason: programmatic acceptance failed: parse-003-conformance, parse-004-conformance
- attempt 6 (repair 6): failed; 0/2 checks; 484/688 cases model=gpt-5.6-luna; execution 20260822.231236.324Z-ca97b585; reason: programmatic acceptance failed: parse-003-conformance, parse-004-conformance

## Agent self-report (advisory)
The build agent declared a failure. This is advisory only; the programmatic acceptance above is the authority for this block's outcome.
- summary: Scoped conformance suites still fail.
- detail:
    Both authoritative acceptance commands executed successfully but reported nonzero fail/error tallies; further evaluator and builtin implementation is required.

## Failure
- summary: programmatic acceptance failed: parse-003-conformance, parse-004-conformance
- detail:
    Block "Block 8 · Service" [block-8] failed its acceptance criteria.
      Story "Implement jq filter expression grammar." [PARSE-003] does not meet its own acceptance criteria:
        - AC parse-003-conformance — The executable passes every selected corpus case exercising expression punctuation, accessors, collections, and operators.
            assertion: assert summary["fail"] == 0 and summary["error"] == 0 → AssertionError
            cases: pass=331 fail=124 error=0 skip=9 total=464 from=summary
            raised at: parse-003-conformance.py:18
            process exit code: 1
            values at failure:
              summary = {'pass': 331, 'fail': 124, 'error': 0, 'skip': 9}
            observed output:
                    "line": 2607,
                    "program": "reduce range(10000) as $_ ({}; {a: .}) as $x | $x * $x | length",
                    "status": "fail",
                    "detail": "output mismatch",
                    "expect_failure": false,
                    "expected": [
                      "1"
                    ],
                    "actual": []
                  }
                ]
              }
              … 1633 earlier line(s) omitted, --full for all
            check stderr:
              Traceback (most recent call last):
                File "parse-003-conformance.py", line 18, in <module>
                  assert summary["fail"] == 0 and summary["error"] == 0
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
              AssertionError
      Story "Implement declarations and control syntax parsing." [PARSE-004] does not meet its own acceptance criteria:
        - AC parse-004-conformance — The executable passes every selected corpus case covering declarations, control syntax, bindings, reductions, labels, and required compile failures.
            assertion: assert summary["fail"] == 0 and summary["error"] == 0 → AssertionError
            cases: pass=153 fail=58 error=0 skip=13 total=224 from=summary
            raised at: parse-004-conformance.py:18
            process exit code: 1
            values at failure:
              summary = {'pass': 153, 'fail': 58, 'error': 0, 'skip': 13}
            observed output:
                    "line": 2607,
                    "program": "reduce range(10000) as $_ ({}; {a: .}) as $x | $x * $x | length",
                    "status": "fail",
                    "detail": "output mismatch",
                    "expect_failure": false,
                    "expected": [
                      "1"
                    ],
                    "actual": []
                  }
                ]
              }
              … 910 earlier line(s) omitted, --full for all
            check stderr:
              Traceback (most recent call last):
                File "parse-004-conformance.py", line 18, in <module>
                  assert summary["fail"] == 0 and summary["error"] == 0
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
              AssertionError

## Build summary
RESULT: FAILED

FILES CHANGED:
- jq_interpreter/parser.py
- jq_interpreter/evaluator.py

SUMMARY:
Implemented parser/evaluator fixes for recursive descent, generator indexes, ranges, slices, computed-key validation, paths, bindings, and control precedence. Project tests pass: 32 passed.

Scoped acceptance remains failing:
- parse-003: 331 passed, 123 failed, 1 errored, 9 skipped
- parse-004: 153 passed, 57 failed, 1 errored, 13 skipped

BLOCKERS:
- Significant evaluator functionality remains incomplete, including builtins, assignment semantics, function scoping, and advanced control behavior.

FAILURE_SUMMARY: Scoped conformance suites still fail.
FAILURE_DETAIL: Both authoritative acceptance commands executed successfully but reported nonzero fail/error tallies; further evaluator and builtin implementation is required.
