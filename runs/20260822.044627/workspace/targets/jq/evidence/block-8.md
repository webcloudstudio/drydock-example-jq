# Evidence: Block 8 · Service (block-8)

- block type: block
- date: 2026-08-22
- resulting state: closed/verified
- story points (combined assembled cost): 25931
- execution id: 20260823.020504.857Z-c6c1a57e

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
- jq_interpreter/evaluator.py
- jq_interpreter/interpreter.py
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
        "pass": 153,
        "fail": 57,
        "error": 1,
        "skip": 13
      },
      "cases": [
        {
          "line": 229,
          "program": "try (.[999999999] = 0) catch .",
          "status": "error",
          "detail": "timed out after 10s",
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
    cases: pass=153 fail=57 error=1 skip=13 total=224 from=summary
    --- drydock: end progress ---
    --- drydock: values at failure ---
      summary = {'pass': 153, 'fail': 57, 'error': 1, 'skip': 13}
    --- drydock: end values ---
    Traceback (most recent call last):
      File "parse-004-conformance.py", line 18, in <module>
        assert summary["fail"] == 0 and summary["error"] == 0
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError

## Post-build programmatic acceptance
- PASS: parse-003-conformance (FEATURE-PARSE-003.md)
  intent: The executable passes every selected corpus case exercising expression punctuation, accessors, collections, and operators.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
  stdout:
    {
      "candidate": [
        "/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260822.044627/build/jq/jq"
      ],
      "corpus": "jq.test",
      "summary": {
        "pass": 455,
        "fail": 0,
        "error": 0,
        "skip": 9
      },
      "cases": [
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
        }
      ]
    }
- PASS: parse-004-conformance (FEATURE-PARSE-004.md)
  intent: The executable passes every selected corpus case covering declarations, control syntax, bindings, reductions, labels, and required compile failures.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
  stdout:
    {
      "candidate": [
        "/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260822.044627/build/jq/jq"
      ],
      "corpus": "jq.test",
      "summary": {
        "pass": 211,
        "fail": 0,
        "error": 0,
        "skip": 13
      },
      "cases": [
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
        }
      ]
    }

## Repair attempts
- attempt 0 (initial build): failed; 0/2 checks; 507/688 cases model=gpt-5.6-luna; execution 20260822.235339.932Z-4de96731; reason: programmatic acceptance failed: parse-003-conformance, parse-004-conformance
- attempt 1 (repair 1): failed; 0/2 checks; 527/688 cases model=gpt-5.6-luna; execution 20260823.000143.358Z-bf6da6b1; reason: programmatic acceptance failed: parse-003-conformance, parse-004-conformance
- attempt 2 (repair 2): failed; 0/2 checks; 546/688 cases model=gpt-5.6-luna; execution 20260823.001232.569Z-0f28cedb; reason: programmatic acceptance failed: parse-003-conformance, parse-004-conformance
- attempt 3 (repair 3): failed; 0/2 checks; 558/688 cases model=gpt-5.6-luna; execution 20260823.002204.979Z-c838b1c2; reason: programmatic acceptance failed: parse-003-conformance, parse-004-conformance
- attempt 4 (repair 4): failed; 0/2 checks; 567/688 cases model=gpt-5.6-luna; execution 20260823.003038.923Z-cf0bf882; reason: programmatic acceptance failed: parse-003-conformance, parse-004-conformance
- attempt 5 (repair 5): failed; 0/2 checks; 573/688 cases model=gpt-5.6-luna; execution 20260823.004037.072Z-5412cbba; reason: programmatic acceptance failed: parse-003-conformance, parse-004-conformance
- attempt 6 (repair 6): failed; 0/2 checks; 591/688 cases model=gpt-5.6-luna; execution 20260823.005049.805Z-cb2d06fb; reason: programmatic acceptance failed: parse-003-conformance, parse-004-conformance
- attempt 7 (repair 7): failed; 0/2 checks; 594/688 cases model=gpt-5.6-luna; execution 20260823.005903.917Z-34989652; reason: programmatic acceptance failed: parse-003-conformance, parse-004-conformance
- attempt 8 (repair 8): failed; 0/2 checks; 617/688 cases model=gpt-5.6-luna; execution 20260823.010841.589Z-02f53a81; reason: programmatic acceptance failed: parse-003-conformance, parse-004-conformance
- attempt 9 (repair 9): failed; 0/2 checks; 619/688 cases model=gpt-5.6-luna; execution 20260823.011808.307Z-f32ef2f1; reason: programmatic acceptance failed: parse-003-conformance, parse-004-conformance
- attempt 10 (repair 10): failed; 0/2 checks; 627/688 cases model=gpt-5.6-luna; execution 20260823.013010.037Z-f5e23d3d; reason: programmatic acceptance failed: parse-003-conformance, parse-004-conformance
- attempt 11 (repair 11): failed; 1/2 checks; 435/464 cases model=gpt-5.6-luna; execution 20260823.014128.073Z-613a1d60; reason: programmatic acceptance failed: parse-003-conformance
- attempt 12 (repair 12): failed; 1/2 checks; 446/464 cases model=gpt-5.6-luna; execution 20260823.015653.931Z-3e0de83b; reason: programmatic acceptance failed: parse-003-conformance
- attempt 13 (repair 13): built; 2/2 checks model=gpt-5.6-luna; execution 20260823.020504.857Z-c6c1a57e

## Build summary
RESULT: SUCCESS

FILES CHANGED:
- jq_interpreter/evaluator.py
- jq_interpreter/interpreter.py
- jq_interpreter/parser.py

SUMMARY:
- PARSE-003: 455 passed, 0 failed, 0 errors.
- PARSE-004: 211 passed, 0 failed, 0 errors.
- Local tests: 32 passed.

BLOCKERS:
- None
