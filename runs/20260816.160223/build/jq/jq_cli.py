import sys
from jq_evaluator import RuntimeErrorJq, evaluate
from jq_parser import ParseError, parse
from jq_values import encode_compact, parse_json

def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[0] != "-c" or not argv[1]:
        print("usage: jq -c PROGRAM", file=sys.stderr); return 3
    try: program = parse(argv[1])
    except (ParseError, ValueError) as error:
        print(str(error), file=sys.stderr); return 3
    try:
        for line in sys.stdin:
            if not line.strip():
                continue
            input_value = parse_json(line)
            for value in evaluate(program, input_value):
                sys.stdout.write(encode_compact(value) + "\n")
    except (RuntimeErrorJq, ValueError, TypeError, IndexError, ArithmeticError) as error:
        print(str(error), file=sys.stderr); return 5
    return 0
