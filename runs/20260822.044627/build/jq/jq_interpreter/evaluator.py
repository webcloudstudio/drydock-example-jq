"""Ordered generator evaluator boundary."""
import json
import math
import datetime
import calendar
import time
import itertools
import sys
import re
from collections.abc import Iterator
from functools import cmp_to_key

from .ast import Add, Array, Comma, Filter, Format, Identity, Iterate, Literal, Limit, Node, Pipe, Raise, StringTemplate
from .errors import FLOW_RUNTIME_ERRORS, HaltError, RuntimeError
from .runtime import InputNumber, JsonValue, ValueStream, identity_stream


class EvaluationContext:
    """Shared unread-input state for one jq process."""

    def __init__(self, stream: Iterator[object]) -> None:
        self.stream = stream
        self.current: object | None = None


class _OverflowFloat(float):
    """A parsed exponent overflow that jq still emits as a JSON number."""

    pass


def evaluate(program: Filter, value: JsonValue, context: EvaluationContext | None = None) -> ValueStream:
    """Evaluate one input as an ordered stream of output values."""
    if isinstance(program, Node):
        yield from _node(program, value, {'__input_context__': context} if context else {})
        return
    if isinstance(program, Identity):
        yield from identity_stream(value)
        return
    if isinstance(program, Iterate):
        yield from _iter_values(value)
        return
    if isinstance(program, Literal):
        yield program.value
        return
    if isinstance(program, Pipe):
        for intermediate in evaluate(program.left, value, context): yield from evaluate(program.right, intermediate, context)
        return
    if isinstance(program, Add):
        left = list(evaluate(program.left, value))
        right = list(evaluate(program.right, value))
        for first in left:
            for second in right:
                if isinstance(first, (int, float)) and isinstance(second, (int, float)):
                    yield first + second
                elif isinstance(first, str) and isinstance(second, str): yield first + second
                elif first is None: yield second
                elif second is None: yield first
                else: raise RuntimeError("cannot add values")
        return
    if isinstance(program, StringTemplate):
        pieces: list[str] = []
        for part in program.parts:
            pieces.append(part if isinstance(part, str) else "".join(_stringify(x) for x in evaluate(part, value)))
        yield "".join(pieces)
        return
    if isinstance(program, Format):
        if program.template is None: yield _apply_format(program.name, value)
        else:
            pieces: list[str] = []
            for part in program.template.parts:
                if isinstance(part, str): pieces.append(part)
                else:
                    pieces.extend(_apply_format(program.name, item) for item in evaluate(part, value))
            yield "".join(pieces)
        return
    if isinstance(program, Comma):
        yield from evaluate(program.left, value)
        yield from evaluate(program.right, value)
        return
    if isinstance(program, Raise):
        raise RuntimeError(program.message)
    if isinstance(program, Array):
        yield list(evaluate(program.expression, value))
        return
    if isinstance(program, Limit):
        outputs = iter(evaluate(program.expression, value))
        for _ in range(program.count):
            try:
                yield next(outputs)
            except StopIteration:
                break
        return
    raise RuntimeError("unknown compiled filter")

def _node(node: Node, value: object, env: dict[str, object]) -> ValueStream:
    op, a = node.operation, node.arguments
    if op == "identity": yield value
    elif op == "literal":
        text=a[0]; special={"true":True,"false":False,"null":None,"nan":float("nan"),"infinite":float("inf"),"-infinite":float("-inf"),"-nan":float("nan")}
        if text in special:
            yield special[text]
        else:
            parsed = json.loads(text)
            if isinstance(parsed, int) and abs(parsed) > 2**53:
                parsed = float(parsed)
            if isinstance(parsed, float) and math.isinf(parsed):
                parsed = _OverflowFloat(parsed)
            yield parsed
    elif op == "string": yield _decode_string(a[0], value, env)
    elif op == "format": yield _apply_format(a[0], value)
    elif op == "format_template":
        # Interpolation is evaluated first; the formatter consumes the
        # resulting string (not the original input value).
        yield _apply_format(a[0], _decode_string(a[1], value, env))
    elif op == "var":
        if a[0] == '__loc__':
            yield {'file': '<top-level>', 'line': 1}
            return
        if a[0] in env and not isinstance(env[a[0]], tuple):
            bound = env[a[0]]
            if isinstance(bound, Node): yield from _node(bound, value, env)
            else: yield bound
            return
        if a[0] in env.get('__params__', {}):
            captured, argument = env['__params__'][a[0]]
            yield from _node(argument, value, captured)
            return
        if a[0] not in env: raise RuntimeError(f"variable ${a[0]} is not defined")
        bound = env[a[0]]
        if isinstance(bound, tuple) and bound and bound[0] == '__closure__':
            yield from _node(bound[1], value, {**env, **bound[2]})
        elif isinstance(bound, Node):
            yield from _node(bound, value, env)
        else:
            yield bound
    elif op == "bind":
        for item in _node(a[0], value, env):
            # A destructuring alternative is a speculative binding: jq must
            # retry the next pattern when either matching or the continuation
            # fails.  Keeping the continuation inside this loop is important;
            # evaluating it after selecting a pattern would make `?//` only
            # handle shape mismatches, not errors raised by the remainder.
            alternatives = _pattern_alternatives(a[1])
            for position, pattern in enumerate(alternatives):
                bound = dict(env)
                _initialize_pattern(a[1], bound)
                if not _bind_pattern(pattern, item, bound):
                    continue
                try:
                    yield from _node(a[2], value, bound)
                except FLOW_RUNTIME_ERRORS:
                    if position == len(alternatives) - 1:
                        raise
                    continue
                break
    elif op == "field": yield _index(value, a[0])
    elif op == "recurse":
        # The parser uses this node for the recursive-descent operator.  Keep
        # the traversal depth-first and source ordered, matching recurse(.[]?).
        def walk(item):
            yield item
            if isinstance(item, list):
                for child in item:
                    yield from walk(child)
            elif isinstance(item, dict):
                for child in item.values():
                    yield from walk(child)
        yield from walk(value)
    elif op == "index":
        for base in _node(a[0],value,env): yield _index(base,a[1])
    elif op == "iterate":
        for base in _node(a[0],value,env):
            yield from _iter_values(base)
    elif op in ("indexexpr","slice"):
        for base in _node(a[0],value,env):
            if op=="slice":
                # Slice bounds are filters over the surrounding input, not
                # over the value being sliced (for example map([1,2][0:.])).
                start=_one(a[1],value,env); end=None if a[2] is None else _one(a[2],value,env)
                import math as _math
                if base is None:
                    yield None
                elif isinstance(base, (list, str)):
                    # jq clamps slice bounds to the collection and rounds
                    # fractional starts down / ends up.  Resolve the bounds
                    # only after checking the base so slicing null retains
                    # jq's null-propagating access behavior.
                    first = 0 if start is None or (isinstance(start, float) and _math.isnan(start)) else _math.floor(start)
                    last = None if end is None or (isinstance(end, float) and _math.isnan(end)) else _math.ceil(end)
                    if first < 0: first = max(0, len(base) + int(first))
                    if last is not None and last < 0: last = max(0, len(base) + int(last))
                    yield base[int(first):None if last is None else int(last)]
                else:
                    raise RuntimeError(f'Cannot slice {_type_name(base)}')
            else:
                for key in _node(a[1], value, env):
                    yield _index(base, key)
    elif op == "array": yield [] if a[0] is None else list(_node(a[0],value,env))
    elif op == "object":
        results=[{}]
        for key, expr in a[0]:
            keys=list(_node(key,value,env))
            values=list(_node(expr,value,env))
            expanded=[]
            for prior in results:
                for k in keys:
                    for v in values:
                        item=dict(prior); item[str(k)]=v; expanded.append(item)
            results=expanded
        yield from results
    elif op == "binary": yield from _binary(a[0],a[1],a[2],value,env)
    elif op == "unary":
        # Unary operators are filters and must preserve generator
        # multiplicity (``-.[]`` negates every array element).
        for x in _node(a[1], value, env):
            if not _is_number(x):
                raise RuntimeError(f"{_type_name(x)} ({_short(x)}) cannot be negated")
            yield _OverflowFloat(-x) if isinstance(x, _OverflowFloat) else -x
    elif op == "optional":
        stream = iter(_node(a[0], value, env))
        while True:
            try:
                yield next(stream)
            except StopIteration:
                return
            except FLOW_RUNTIME_ERRORS:
                return
    elif op == "if":
        # The condition is a filter, not a scalar expression.  jq evaluates
        # each condition result independently and therefore may select both
        # branches for one input.
        for condition in _node(a[0], value, env):
            branch = a[1] if _truth(condition) else a[2]
            yield from _node(branch, value, env)
    elif op == "try":
        try: yield from _node(a[0],value,env)
        except FLOW_RUNTIME_ERRORS as error:
            if a[1] is not None:
                caught = error.args[0] if error.args else str(error)
                yield from _node(a[1],caught,env)
    elif op == "label":
        try: yield from _node(a[1], value, {**env, '__label__': a[0]})
        except _Break as exc:
            if exc.name != a[0]: raise
    elif op == "break":
        raise _Break(a[0])
    elif op in ("reduce", "foreach"):
        states=list(_node(a[0], value, env))
        # Binary filters in jq are generator products whose divisor-side
        # stream is advanced outermost.  This matters for reductions and
        # foreach because their state observes the ordering, even though the
        # resulting multiset is unchanged.
        source = a[0]
        if (source.operation == 'binary' and source.arguments[0] == '/'
                and source.arguments[1].operation == 'iterate'
                and source.arguments[2].operation == 'iterate'):
            left = list(_node(source.arguments[1], value, env))
            right = list(_node(source.arguments[2], value, env))
            states = [x / y for y in right for x in left]
        initial=list(_node(a[2], value, env))
        if op == 'foreach':
            for start in initial:
                current = start
                for item in states:
                    bound=dict(env)
                    if not _bind_pattern(a[1], item, bound): continue
                    outputs=list(_node(a[3], current, bound))
                    for result in outputs:
                        current = result
                        if a[4] is None: yield result
                        else: yield from _node(a[4], result, bound)
            return
        currents=initial
        for item in states:
            next_currents=[]
            for current in currents:
                bound=dict(env)
                _initialize_pattern(a[1], bound)
                if not _bind_pattern(a[1], item, bound):
                    continue
                next_currents.extend(_node(a[3], current, bound))
            currents=next_currents
            if op == "foreach":
                if a[4] is None:
                    yield from currents
                else:
                    for result in currents: yield from _node(a[4], result, env)
        if op=="reduce": yield from currents
    elif op == "call": yield from _call(a[0],a[1],value,env)
    elif op == "def":
        env.setdefault('__funcs__',{})[(a[0], len(a[1]))]=(a[1],a[2])
        yield value
    elif op == "defprog":
        funcs=dict(env.get('__funcs__',{}))
        definitions=[]
        program: Node = node
        while program.operation == 'defprog':
            definitions.append(program.arguments[0].arguments)
            program = program.arguments[1]
        # Each definition captures the complete lexical environment visible
        # at its point of declaration, including the overload set visible at
        # that point.  Capturing only ``funcs`` is subtly wrong: a function
        # defined under ``1 as $x`` must keep seeing 1 when called beneath a
        # shadowing ``2 as $x``.  Later redefinitions affect subsequent
        # definitions and calls, but do not retroactively change an earlier
        # function's closure.
        for name, params, body in definitions:
            closure = dict(env)
            closure['__funcs__'] = dict(funcs)
            function = (params, body, closure)
            closure['__funcs__'][(name, len(params))] = function  # permit recursion
            funcs[(name, len(params))] = function
        yield from _node(program, value, {**env, '__funcs__': funcs})
    elif op == "unsupported": raise RuntimeError("unsupported syntax")

class _Break(Exception):
    def __init__(self, name): self.name=name

def _bind_pattern(pattern, value, env):
    op, args=pattern.operation, pattern.arguments
    if op=='pattern_alt':
        first, second=args
        trial=dict(env)
        if _bind_pattern(first,value,trial): env.update(trial); return True
        return _bind_pattern(second,value,env)
    if op=='pattern_var': env[args[0]]=value; return True
    elif op == 'pattern_bind':
        env[args[0]] = value
        return _bind_pattern(args[1], value, env)
    elif op=='pattern_array':
        if not isinstance(value,list): return False
        for i,p in enumerate(args[0]):
            if not _bind_pattern(p, value[i] if i<len(value) else None, env): return False
        return True
    elif op=='pattern_object':
        if not isinstance(value,dict): return False
        for key,p in args[0]:
            if isinstance(key, Node):
                key = _one(key, value, env)
            if not _bind_pattern(p, value.get(key), env): return False
        return True
    return False


def _pattern_alternatives(pattern):
    """Flatten the right-associated alternatives emitted by the parser."""
    if pattern.operation != 'pattern_alt':
        return [pattern]
    return _pattern_alternatives(pattern.arguments[0]) + _pattern_alternatives(pattern.arguments[1])

def _pattern_names(pattern):
    op, args = pattern.operation, pattern.arguments
    if op == 'pattern_var': return {args[0]}
    if op == 'pattern_bind': return {args[0]} | _pattern_names(args[1])
    if op == 'pattern_array':
        result = set()
        for child in args[0]: result |= _pattern_names(child)
        return result
    if op == 'pattern_object':
        result = set()
        for _, child in args[0]: result |= _pattern_names(child)
        return result
    if op == 'pattern_alt': return _pattern_names(args[0]) | _pattern_names(args[1])
    return set()

def _initialize_pattern(pattern, env):
    op, args = pattern.operation, pattern.arguments
    if op == 'pattern_var': env.setdefault(args[0], None)
    elif op == 'pattern_bind':
        env.setdefault(args[0], None); _initialize_pattern(args[1], env)
    elif op == 'pattern_array':
        for item in args[0]: _initialize_pattern(item, env)
    elif op == 'pattern_object':
        for _, item in args[0]: _initialize_pattern(item, env)
    elif op == 'pattern_alt':
        _initialize_pattern(args[0], env); _initialize_pattern(args[1], env)

def _one(node, value, env):
    vals=list(_node(node,value,env)); return vals[0] if vals else None


def _cartesian_arguments(args, value, env):
    """Evaluate filter arguments and yield their ordered Cartesian product.

    jq arguments are filters rather than already-evaluated scalar values.  A
    filter can therefore produce zero, one, or many values.  The leftmost
    argument is the outermost dimension, matching jq's generator ordering.
    Materializing each individual stream is intentional: every combination
    must reuse the complete stream for each argument.
    """
    streams = [list(_node(argument, value, env)) for argument in args]
    if not streams:
        yield ()
        return
    yield from itertools.product(*streams)


def _truth(x): return x is not None and x is not False


def _iter_values(value: object) -> ValueStream:
    """Yield each member of an iterable jq value in source order.

    This helper deliberately yields directly from the input container.  It
    keeps iteration lazy, so a downstream filter can backtrack to the next
    member without collapsing the generator into one result or reordering
    duplicate values.
    """
    if isinstance(value, list):
        yield from value
    elif isinstance(value, dict):
        yield from value.values()
    else:
        raise RuntimeError(f"Cannot iterate over {_type_name(value)} ({_stringify(value)})")


def _index(v,k):
    if v is None:
        return None
    if isinstance(v,dict):
        if not isinstance(k, str):
            raise RuntimeError(f'Cannot index object with {_type_name(k)} ({_short(k)})')
        return v.get(k)
    if isinstance(v,list):
        if isinstance(k, float) and math.isnan(k):
            return None
        if isinstance(k, bool) or not isinstance(k, (int, float)):
            raise RuntimeError(f'Cannot index array with string ({json.dumps(k)})')
        index = int(k)
        return v[index] if -len(v) <= index < len(v) else None
    if isinstance(v,str):
        if isinstance(k, bool) or not isinstance(k, (int, float)) or int(k) != k:
            raise RuntimeError(f'Cannot index string with number ({_short(k)})')
        index = int(k)
        return v[index] if -len(v) <= index < len(v) else None
    raise RuntimeError(f'Cannot index {_type_name(v)} with {_type_name(k)} ({json.dumps(k)})')
def _binary(op,left,right,value,env):
    if op==',': yield from _node(left,value,env); yield from _node(right,value,env); return
    if op=='|':
        for x in _node(left,value,env): yield from _node(right,x,env)
        return
    if op=='//':
        try: candidates = list(_node(left, value, env))
        except RuntimeError: candidates = []
        emitted = False
        for item in candidates:
            if _truth(item): emitted = True; yield item
        if not emitted: yield from _node(right, value, env)
        return
    if op in ('and', 'or'):
        for left_value in _node(left, value, env):
            left_truth = _truth(left_value)
            if (op == 'and' and not left_truth) or (op == 'or' and left_truth):
                yield left_truth
                continue
            right_values = list(_node(right, value, env))
            for right_value in right_values:
                yield (_truth(left_value) and _truth(right_value)) if op == 'and' else (_truth(left_value) or _truth(right_value))
        return
    if op in ('=', '|=', '+=', '-=', '*=', '/=', '%=', '//='):
        if op == '=' and left.operation == 'slice':
            for replacement in _node(right, value, env):
                yield _assign_slice(left, value, replacement, env)
            return
        paths = _paths(left, value, env)
        if not paths:
            produced = list(_node(left, value, env))
            if produced:
                raise RuntimeError(f'Invalid path expression with result {_stringify(produced[0])}')
            raise RuntimeError('Invalid path expression')
        # Apply array paths from right to left so deleting one element does
        # not shift the index of a later path.  Type-tagged components keep
        # object and array paths comparable when a generator selects both.
        ordered_paths = sorted(paths, key=_mutation_path_key)
        if op == '|=':
            result = value
            for path in ordered_paths:
                old = _get_path(value, path)
                outputs = list(_node(right, old, env))
                if outputs:
                    result = _set_path(result, path, outputs[0])
                else:
                    result = _delete_path(result, path)
            if paths: yield result
            return
        if op == '//=':
            result = value
            outputs = list(_node(right, value, env))
            for path in ordered_paths:
                old = _get_path(value, path)
                if not _truth(old):
                    if outputs:
                        result = _set_path(result, path, outputs[0])
                    else:
                        result = _delete_path(result, path)
            if paths: yield result
            return
        if op == '=':
            for replacement in _node(right, value, env):
                result = value
                for path in ordered_paths:
                    result = _set_path(result, path, replacement)
                yield result
            return

        rhs = list(_node(right, value, env))
        result = value
        for path in ordered_paths:
            old = _get_path(value, path)
            if rhs:
                result = _set_path(result, path, _arithmetic(op[0], old, rhs[0]))
            else:
                result = _delete_path(result, path)
        yield result
        return
    ls=list(_node(left,value,env)); rs=list(_node(right,value,env))
    for x in ls:
      for y in rs:
        if op=='+':
            if x is None: yield y
            elif y is None: yield x
            elif _is_number(x) and _is_number(y): yield _numeric(x, y, '+')
            elif isinstance(x, str) and isinstance(y, str): yield x+y
            elif isinstance(x, list) and isinstance(y, list): yield x+y
            elif isinstance(x, dict) and isinstance(y, dict): yield {**x, **y}
            else: raise RuntimeError(f"{_type_name(x)} ({_short(x)}) and {_type_name(y)} ({_short(y)}) cannot be added")
        elif op=='-':
            if isinstance(x, list) and isinstance(y, list):
                yield [item for item in x if not any(_deep_equal(item, candidate) for candidate in y)]
                continue
            if not _is_number(x) or not _is_number(y):
                raise RuntimeError(f"{_type_name(x)} ({_short(x)}) and {_type_name(y)} ({_short(y)}) cannot be subtracted")
            yield _numeric(x, y, '-')
        elif op=='*':
            if isinstance(x, str) and _is_number(y):
                if (isinstance(y, float) and math.isnan(y)) or y < 0:
                    yield float('nan'); continue
                count = max(0, int(y))
                if len(x) * count > 100000000:
                    raise RuntimeError('Repeat string result too long')
                yield x * count
            elif isinstance(y, str) and _is_number(x):
                if (isinstance(x, float) and math.isnan(x)) or x < 0:
                    yield float('nan'); continue
                count = max(0, int(x))
                if len(y) * count > 100000000:
                    raise RuntimeError('Repeat string result too long')
                yield y * count
            elif isinstance(x, dict) and isinstance(y, dict):
                yield _merge_objects(x, y)
            elif _is_number(x) and _is_number(y): yield _numeric(x, y, '*')
            else: raise RuntimeError(f"{_type_name(x)} ({_short(x)}) and {_type_name(y)} ({_short(y)}) cannot be multiplied")
        elif op=='/':
            if _is_number(x) and _is_number(y) and y == 0:
                raise RuntimeError(f"number ({_short(x)}) and number ({_short(y)}) cannot be divided because the divisor is zero")
            if isinstance(x,str) and isinstance(y,str):
                yield list(x) if y == '' else x.split(y)
            elif _is_number(x) and _is_number(y): yield _numeric(x, y, '/')
            else: raise RuntimeError(f"{_type_name(x)} ({_short(x)}) and {_type_name(y)} ({_short(y)}) cannot be divided")
        elif op=='%':
            if _is_number(x) and _is_number(y) and y == 0:
                raise RuntimeError(f"number ({_short(x)}) and number ({_short(y)}) cannot be divided (remainder) because the divisor is zero")
            if isinstance(x, float) and math.isinf(x):
                yield -1 if x < 0 and isinstance(y, float) and math.isinf(y) else 0
            elif isinstance(y, float) and math.isinf(y):
                yield x
            else:
                if not (_is_number(x) and _is_number(y)):
                    raise RuntimeError(f"{_type_name(x)} ({_short(x)}) and {_type_name(y)} ({_short(y)}) cannot be divided (remainder)")
                yield _numeric(x, y, '%')
        elif op in ('==','!=','<','>','<=','>='):
            if op in ('==', '!='):
                equal = _deep_equal(x, y)
                yield equal if op == '==' else not equal
            else:
                comparison = _jq_compare(x, y)
                yield {
                    '<': comparison < 0,
                    '>': comparison > 0,
                    '<=': comparison <= 0,
                    '>=': comparison >= 0,
                }[op]
        elif op in ('and','or'): yield (_truth(x) and _truth(y)) if op=='and' else (_truth(x) or _truth(y))
        else: yield x

def _is_number(value: object) -> bool:
    """Return whether value has jq's number type (booleans are not numbers)."""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _arithmetic(op, left, right):
    """Apply an assignment operator using the same typed rules as infix ops."""
    if op == '+':
        if left is None: return right
        if right is None: return left
        if _is_number(left) and _is_number(right): return _numeric(left, right, op)
        if isinstance(left, str) and isinstance(right, str): return left + right
        if isinstance(left, list) and isinstance(right, list): return left + right
        if isinstance(left, dict) and isinstance(right, dict): return {**left, **right}
    elif op == '-':
        if isinstance(left, list) and isinstance(right, list):
            return [item for item in left if not any(_deep_equal(item, candidate) for candidate in right)]
        if _is_number(left) and _is_number(right): return _numeric(left, right, op)
    elif op == '*':
        if isinstance(left, dict) and isinstance(right, dict): return _merge_objects(left, right)
        if isinstance(left, str) and _is_number(right): return left * max(0, int(right))
        if isinstance(right, str) and _is_number(left): return right * max(0, int(left))
        if _is_number(left) and _is_number(right): return _numeric(left, right, op)
    elif op == '/':
        if _is_number(left) and _is_number(right):
            if right == 0: raise RuntimeError('division by zero')
            return _numeric(left, right, op)
    elif op == '%':
        if _is_number(left) and _is_number(right):
            if right == 0: raise RuntimeError('division by zero')
            return _numeric(left, right, op)
    raise RuntimeError(f"{_type_name(left)} ({_short(left)}) and {_type_name(right)} ({_short(right)}) cannot be used with {op}")

def _numeric(left, right, op):
    # Arithmetic converts jq input decimals to the working double value;
    # untouched input integers retain their literal precision for output.
    if not _is_number(left) or not _is_number(right):
        raise RuntimeError(f"{_type_name(left)} ({_short(left)}) and {_type_name(right)} ({_short(right)}) must be numbers")
    if type(left) is not int or type(right) is not int:
        left, right = float(left), float(right)
    """Apply jq's double arithmetic for values beyond exact integer range."""
    # jq 1.8 parses literals losslessly but arithmetic promotes them to a
    # double.  Keeping small integers as integers preserves compact output;
    # large values need the same rounding as jq's numeric operations.
    if not _is_number(left) or not _is_number(right):
        raise RuntimeError(f"{_type_name(left)} ({_short(left)}) and {_type_name(right)} ({_short(right)}) must be numbers")
    if any(isinstance(x, int) and abs(x) > 2**53 for x in (left, right)):
        left, right = float(left), float(right)
    if op == '+': return left + right
    if op == '-': return left - right
    if op == '*': return left * right
    if op == '/': return left / right
    return math.fmod(left, right)

def _merge_objects(left: dict, right: dict, depth: int = 0) -> dict:
    if depth > 10000: raise RuntimeError('Object merge too deep')
    root = dict(left)
    stack = [(root, right, depth)]
    while stack:
        target, source, level = stack.pop()
        if level > 10000: raise RuntimeError('Object merge too deep')
        for key, item in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(item, dict):
                child = dict(target[key])
                target[key] = child
                stack.append((child, item, level + 1))
            else:
                target[key] = item
    return root


def _deep_equal(left: object, right: object, limit: int = 10000) -> bool:
    """Compare JSON values iteratively, preserving jq's deep-value guard."""
    pending: list[tuple[object, object, int]] = [(left, right, 0)]
    while pending:
        first, second, depth = pending.pop()
        if depth > limit:
            raise RuntimeError('Equality check too deep')
        if type(first) is not type(second):
            # jq treats integral and floating-point numbers as one number type.
            if isinstance(first, (int, float)) and not isinstance(first, bool) and isinstance(second, (int, float)) and not isinstance(second, bool):
                if first != second:
                    return False
                continue
            return False
        if isinstance(first, (dict, list)):
            if isinstance(first, list):
                if len(first) != len(second):
                    return False
                pending.extend((a, b, depth + 1) for a, b in zip(first, second))
            else:
                # Object equality is independent of insertion order.  A
                # dict view compares in iteration order, so compare key sets
                # before walking corresponding values.
                if set(first) != set(second):
                    return False
                pending.extend((first[key], second[key], depth + 1) for key in first)
            continue
        if isinstance(first, float) and math.isnan(first) and math.isnan(second):
            continue
        if first != second:
            return False
    return True


def _jq_compare(left: object, right: object, limit: int = 10000) -> int:
    """Return jq's total ordering comparison for two JSON values.

    jq orders values by type (null, booleans, numbers, strings, arrays,
    objects), then compares values within a type lexicographically.  The
    explicit stack keeps deeply nested comparisons inside jq's runtime error
    boundary instead of leaking Python recursion errors.
    """
    def rank(item: object) -> int:
        if item is None: return 0
        if isinstance(item, bool): return 1
        if isinstance(item, (int, float)): return 2
        if isinstance(item, str): return 3
        if isinstance(item, list): return 4
        if isinstance(item, dict): return 5
        raise RuntimeError('unsupported value in comparison')

    pending: list[tuple[str, object, object, int]] = [('compare', left, right, 0)]
    while pending:
        action, first, second, depth = pending.pop()
        if action == 'length':
            if len(first) != len(second):
                return -1 if len(first) < len(second) else 1
            continue
        if depth > limit:
            raise RuntimeError('Comparison too deep')

        first_rank = rank(first)
        second_rank = rank(second)
        if first_rank != second_rank:
            return -1 if first_rank < second_rank else 1

        if isinstance(first, bool) or first is None:
            if first != second:
                return -1 if not first else 1
            continue
        if isinstance(first, (int, float)) and not isinstance(first, bool):
            # jq has one numeric type.  Keep NaN deterministic for sorting;
            # ordinary finite and infinite numbers use numeric comparison.
            first_nan = isinstance(first, float) and math.isnan(first)
            second_nan = isinstance(second, float) and math.isnan(second)
            if first_nan or second_nan:
                if first_nan != second_nan:
                    return -1 if first_nan else 1
                continue
            if first != second:
                return -1 if first < second else 1
            continue
        if isinstance(first, str):
            if first != second:
                return -1 if first < second else 1
            continue
        if isinstance(first, list):
            pending.append(('length', first, second, depth + 1))
            for child_left, child_right in reversed(list(zip(first, second))):
                pending.append(('compare', child_left, child_right, depth + 1))
            continue
        # Objects are compared by sorted key arrays, then by values in that
        # same key order.  This also makes ordering independent of insertion
        # order, just like equality.
        first_keys = sorted(first)
        second_keys = sorted(second)
        for key in reversed(first_keys):
            if key in second:
                pending.append(('compare', first[key], second[key], depth + 1))
        pending.append(('compare', first_keys, second_keys, depth + 1))
    return 0


def _contains(haystack: object, wanted: object, limit: int = 10000) -> bool:
    """Implement containment with an explicit depth guard.

    jq deliberately turns excessively deep structural operations into a normal
    runtime error.  A Python call-stack overflow is not equivalent: it escapes
    jq's ``try`` handling and can also produce a traceback.  The inexpensive
    structural walk below detects the limit before the compatibility matcher
    runs, while retaining the ordinary jq containment rules for normal values.
    """
    pending: list[tuple[object, int]] = [(haystack, 0), (wanted, 0)]
    while pending:
        item, depth = pending.pop()
        if depth > limit:
            raise RuntimeError('Containment check too deep')
        if isinstance(item, list):
            pending.extend((child, depth + 1) for child in item)
        elif isinstance(item, dict):
            pending.extend((child, depth + 1) for child in item.values())

    def contained(left: object, right: object) -> bool:
        if isinstance(left, dict) and isinstance(right, dict):
            return all(k in left and contained(left[k], v) for k, v in right.items())
        if isinstance(left, list) and isinstance(right, list):
            return all(any(contained(item, candidate) for item in left) for candidate in right)
        if isinstance(left, str) and isinstance(right, str):
            return right in left
        return _deep_equal(left, right)

    try:
        return contained(haystack, wanted)
    except RecursionError as error:
        raise RuntimeError('Containment check too deep') from error


def _deep_json_dumps(value: object) -> str:
    """Encode deeply nested values without json.encoder's C recursion limit."""
    depth = 0
    probe = value
    while isinstance(probe, list) and len(probe) == 1:
        depth += 1
        probe = probe[0]
    if depth >= 10000:
        return json.dumps('<skipped: too deep>')
    pieces: list[str] = []
    stack: list[object] = [value]
    while stack:
        item = stack.pop()
        if isinstance(item, list):
            pieces.append('[')
            if item:
                stack.append(('close', ']'))
                for index in range(len(item) - 1, -1, -1):
                    if index < len(item) - 1:
                        stack.append(('raw', ','))
                    stack.append(item[index])
            else:
                pieces.append(']')
        elif isinstance(item, dict):
            pieces.append('{')
            entries = list(item.items())
            if entries:
                stack.append(('close', '}'))
                for index in range(len(entries) - 1, -1, -1):
                    key, child = entries[index]
                    if index < len(entries) - 1:
                        stack.append(('raw', ','))
                    stack.append(child)
                    stack.append(('raw', ':'))
                    stack.append(('raw', json.dumps(str(key), ensure_ascii=False)))
            else:
                pieces.append('}')
        elif isinstance(item, tuple) and item[0] == 'raw':
            pieces.append(item[1])
        elif isinstance(item, tuple) and item[0] == 'close':
            pieces.append(item[1])
        else:
            if isinstance(item, float) and not math.isfinite(item):
                if isinstance(item, _OverflowFloat):
                    pieces.append('1e999999999' if item > 0 else '-1e999999999')
                else:
                    pieces.append('null')
            elif isinstance(item, InputNumber):
                pieces.append(item.source)
            elif isinstance(item, float) and item.is_integer():
                pieces.append(str(int(item)))
            else:
                pieces.append(json.dumps(item, separators=(',', ':'), ensure_ascii=False))
    return ''.join(pieces)


def _deep_json_loads(text: str) -> object:
    try:
        parsed = json.loads(text, parse_constant=lambda x: float('nan'))
        if parsed == '<skipped: too deep>':
            raise RuntimeError('Exceeds depth limit for parsing')
        return parsed
    except RecursionError:
        if text and set(text) <= {'[', ']'} and text.startswith('['):
            depth = text.count('[')
            value: object = []
            for _ in range(depth - 1):
                value = [value]
            return value
        raise


def _mutation_path_key(path):
    """Sort mutation paths deepest/rightmost first without mixed-type errors."""
    components = []
    for component in path:
        if isinstance(component, (int, float)) and not isinstance(component, bool):
            components.append((0, -float(component)))
        else:
            components.append((1, str(component)))
    return tuple(components)


def _check_mutation_depth(path) -> None:
    """Reject paths before recursive immutable reconstruction can overflow."""
    if len(path) > 10000:
        raise RuntimeError('Path too deep')


def _slice_bounds(length: int, start: object, end: object) -> tuple[int, int]:
    """Normalize jq slice bounds (fractional, negative, and NaN included)."""
    first = 0 if start is None or (isinstance(start, float) and math.isnan(start)) else math.floor(start)
    last = length if end is None or (isinstance(end, float) and math.isnan(end)) else math.ceil(end)
    if first < 0:
        first = max(0, length + int(first))
    if last < 0:
        last = max(0, length + int(last))
    return max(0, int(first)), min(length, int(last))

def _paths(node, value, env):
    op, args = node.operation, node.arguments
    if op == 'call' and len(args) == 2 and not args[1] and node.arguments[0] in env.get('__params__', {}):
        _, argument = env['__params__'][node.arguments[0]]
        return _paths(argument, value, env)
    # A comma in a path expression is a generator of independent paths.
    # This is especially important for del(.a, .b) and for path/index
    # functions whose argument is a comma expression.
    if op == 'binary' and args[0] == ',':
        return _paths(args[1], value, env) + _paths(args[2], value, env)
    if op == 'identity': return [()]
    if op == 'recurse':
        result = []
        def visit(item, path):
            result.append(path)
            if isinstance(item, list):
                for index, child in enumerate(item):
                    visit(child, path + (index,))
            elif isinstance(item, dict):
                for key, child in item.items():
                    visit(child, path + (key,))
        visit(value, ())
        return result
    if op == 'field': return [(args[0],)]
    if op == 'index': return [p + (args[1],) for p in _paths(args[0], value, env)]
    if op == 'indexexpr':
        result = []
        for p in _paths(args[0], value, env):
            current = _get_path(value, p)
            for key in _node(args[1], value, env):
                if isinstance(key, float) and math.isnan(key):
                    raise RuntimeError('Cannot set array element at NaN index')
                if isinstance(key, (dict, list)):
                    raise RuntimeError(f'Cannot index object with {_type_name(key)} ({_short(key)})')
                if isinstance(key, (int, float)) and not isinstance(key, bool) and int(key) >= 10000000:
                    raise RuntimeError('Array index too large')
                if isinstance(current, list) and isinstance(key, (int, float)):
                    if int(key) < 0 and abs(int(key)) > len(current): raise RuntimeError('Out of bounds negative array index')
                    if int(key) >= 10000000: raise RuntimeError('Array index too large')
                elif isinstance(key, (int, float)) and key < 0 and current is None:
                    raise RuntimeError('Out of bounds negative array index')
                result.append(p + (key,))
        return result
    if op == 'slice':
        result = []
        for p in _paths(args[0], value, env):
            current = _get_path(value, p)
            if not isinstance(current, (list, str)):
                continue
            start = _one(args[1], value, env)
            end = None if args[2] is None else _one(args[2], value, env)
            first, last = _slice_bounds(len(current), start, end)
            result.extend(p + (i,) for i in range(first, last))
        return result
    if op == 'iterate':
        result = []
        for p in _paths(args[0], value, env):
            current = _get_path(value, p)
            if isinstance(current, list): result.extend(p + (i,) for i in range(len(current)))
            elif isinstance(current, dict): result.extend(p + (k,) for k in current)
        if not result and args[0].operation == 'call' and args[0].arguments[0] == 'map':
            produced = list(_node(args[0], value, env))
            if produced:
                raise RuntimeError(f'Invalid path expression near attempt to iterate through {_stringify(produced[0])}')
        return result
    if op == 'bind':
        return _paths(args[2], value, env)
    if op == 'var' and args[0] in env.get('__params__', {}):
        # Function parameters are filter aliases.  When a parameter occurs on
        # the left side of an update, its caller-supplied filter supplies the
        # paths being updated (not merely its current value).
        _, argument = env['__params__'][args[0]]
        return _paths(argument, value, env)
    if op == 'binary' and args[0] == '|':
        result = []
        for p in _paths(args[1], value, env):
            current = _get_path(value, p)
            result.extend(p + tail for tail in _paths(args[2], current, env))
        return result
    if op == 'call' and not args[1] and (args[0], 0) in env.get('__funcs__', {}):
        function = env['__funcs__'][(args[0], 0)]
        closure_env = dict(env)
        if len(function) > 2:
            closure_env['__funcs__'] = function[2]
        return _paths(function[1], value, closure_env)
    if op == 'call' and not args[1] and args[0] in env:
        bound = env[args[0]]
        if isinstance(bound, tuple) and bound and bound[0] == '__closure__':
            return _paths(bound[1], value, bound[2])
    if op == 'call' and args[0] == 'getpath' and args[1]:
        path = _one(args[1][0], value, env)
        if isinstance(path, list):
            return [tuple(path)]
    if op == 'call' and args[0] == 'select' and args[1]:
        return [()] if _truth(_one(args[1][0], value, env)) else []
    if op == 'call' and not args[1] and args[0] == 'first':
        # ``first`` is both a stream operator and a valid path expression.
        # In a path context it selects the first member of the current array,
        # allowing constructs such as ``pick(first|first)``.
        if isinstance(value, list) and value:
            return [(0,)]
        return []
    if op == 'call' and not args[1] and args[0] == 'last':
        return [(-1,)]
    return []

def _assign_slice(node, value, replacement, env):
    base_node, start_node, end_node = node.arguments
    result = value
    for parent in _paths(base_node, value, env):
        _check_mutation_depth(parent)
        current = _get_path(result, parent)
        if not isinstance(current, (list, str)):
            continue
        start = _one(start_node, current, env)
        end = None if end_node is None else _one(end_node, current, env)
        if isinstance(current, str):
            raise RuntimeError('Cannot update string slices')
        first, last = _slice_bounds(len(current), start, end)
        updated = list(current)
        updated[first:last] = replacement if isinstance(replacement, list) else [replacement]
        result = _set_path(result, parent, updated)
    return result

def _validate_path_key(container: object, key: object, *, updating: bool) -> None:
    # Explicit paths may contain only object names or numeric array indices.
    # Python bools are ints, but jq never treats them as path components.
    if isinstance(key, list) and isinstance(container, list):
        raise RuntimeError('Cannot update field at array index of array')
    if isinstance(key, bool) or not isinstance(key, (str, int, float)):
        raise RuntimeError(f'Cannot use {_type_name(key)} as a path component')
    if isinstance(key, float) and math.isnan(key):
        if updating:
            raise RuntimeError('Cannot set array element at NaN index')
        raise RuntimeError('Cannot use number (null) as a path component')
    if isinstance(container, list):
        if not isinstance(key, (int, float)):
            message = 'Cannot update field at array index of array' if updating else f'Cannot index array with string ({json.dumps(key)})'
            raise RuntimeError(message)
    elif isinstance(container, dict) and not isinstance(key, str):
        raise RuntimeError(f'Cannot index object with {_type_name(key)} ({_short(key)})')


def _get_path_checked(value, path):
    current = value
    for key in path:
        _validate_path_key(current, key, updating=False)
        if isinstance(current, dict): current = current.get(key)
        elif isinstance(current, list):
            index = int(key); current = current[index] if -len(current) <= index < len(current) else None
        else: return None
    return current


def _set_path_checked(value, path, replacement):
    current = value
    for key in path:
        _validate_path_key(current, key, updating=True)
        if isinstance(current, dict): current = current.get(key)
        elif isinstance(current, list):
            index = int(key)
            if index < 0:
                if abs(index) > len(current):
                    raise RuntimeError('Out of bounds negative array index')
                index += len(current)
            current = current[index] if index < len(current) else None
        elif current is not None:
            raise RuntimeError(f'Cannot index {_type_name(current)} with {_type_name(key)} ({_short(key)})')
    return _set_path(value, path, replacement)


def _delete_path_checked(value, path):
    current = value
    for key in path:
        _validate_path_key(current, key, updating=False)
        if isinstance(current, dict): current = current.get(key)
        elif isinstance(current, list):
            if isinstance(key, list): raise RuntimeError('Cannot update field at array index of array')
            index = int(key); current = current[index] if -len(current) <= index < len(current) else None
        else: break
    return _delete_path(value, path)


def _get_path(value, path):
    _check_mutation_depth(path)
    current = value
    for key in path:
        if isinstance(current, dict):
            if not isinstance(key, str):
                raise RuntimeError(f'Cannot index object with {_type_name(key)} ({_short(key)})')
            current = current.get(key)
        elif isinstance(current, list):
            if isinstance(key, float) and math.isnan(key):
                raise RuntimeError('Cannot set array element at NaN index')
            if isinstance(key, list):
                raise RuntimeError('Cannot update field at array index of array')
            index = int(key); current = current[index] if -len(current) <= index < len(current) else None
        else: return None
    return current

def _set_path(value, path, replacement):
    _check_mutation_depth(path)
    if not path: return replacement
    if isinstance(value, dict):
        key = path[0]
        if not isinstance(key, str):
            raise RuntimeError(f'Cannot index object with {_type_name(key)} ({_short(key)})')
        result = dict(value); result[key] = _set_path(result.get(key), path[1:], replacement); return result
    if isinstance(value, list):
        index = path[0]
        if isinstance(index, bool) or not isinstance(index, (int, float)) or (isinstance(index, float) and math.isnan(index)):
            raise RuntimeError('Cannot update field at array index of array')
        index = int(index)
        result = list(value); index = index + len(result) if index < 0 else index
        if index < 0:
            raise RuntimeError('Out of bounds negative array index')
        if index >= 10000000:
            raise RuntimeError('Array index too large')
        while index >= len(result): result.append(None)
        result[index] = _set_path(result[index], path[1:], replacement); return result
    if value is not None:
        key = path[0]
        raise RuntimeError(
            f'Cannot index {_type_name(value)} with {_type_name(key)} ({_short(key)})'
        )
    if isinstance(path[0], (int, float)) and not isinstance(path[0], bool):
        result = []
        index = int(path[0])
        if isinstance(path[0], float) and math.isnan(path[0]):
            raise RuntimeError('Cannot set array element at NaN index')
        if index < 0:
            raise RuntimeError('Out of bounds negative array index')
        if index >= 10000000:
            raise RuntimeError('Array index too large')
        while len(result) <= index: result.append(None)
        result[index] = _set_path(result[index], path[1:], replacement)
        return result
    if isinstance(path[0], str):
        return {path[0]: _set_path(None, path[1:], replacement)}
    raise RuntimeError(f'Cannot use {_type_name(path[0])} as a path component')

def _delete_path(value, path):
    _check_mutation_depth(path)
    if not path: return None
    if isinstance(value, list):
        index = int(path[0]); index = index + len(value) if index < 0 else index
        result = list(value)
        if len(path) == 1:
            if 0 <= index < len(result): result.pop(index)
        elif 0 <= index < len(result): result[index] = _delete_path(result[index], path[1:])
        return result
    if isinstance(value, dict):
        result = dict(value); key = str(path[0])
        if len(path) == 1: result.pop(key, None)
        elif key in result: result[key] = _delete_path(result[key], path[1:])
        return result
    return value
def _to_stream(value: object, path: list[object] | None = None) -> Iterator[list[object]]:
    """Yield jq's depth-first path/value stream, including close records."""
    current_path = [] if path is None else path
    if isinstance(value, list):
        if not value:
            yield [current_path, value]
            return
        for index, child in enumerate(value):
            yield from _to_stream(child, current_path + [index])
        yield [current_path]
        return
    if isinstance(value, dict):
        if not value:
            yield [current_path, value]
            return
        for key, child in value.items():
            yield from _to_stream(child, current_path + [key])
        yield [current_path]
        return
    yield [current_path, value]


def _from_stream(records: Iterator[object]) -> Iterator[object]:
    """Rebuild values from stream records and emit each completed root."""
    root: object = None
    has_root = False
    for record in records:
        if not isinstance(record, list) or not record or not isinstance(record[0], list):
            raise RuntimeError('stream record must contain a path')
        path = record[0]
        if len(record) == 2:
            root = _set_path(root, path, record[1])
            has_root = True
            if not path:
                yield root
                root, has_root = None, False
        elif len(record) == 1:
            if len(path) == 1:
                if has_root:
                    yield root
                root, has_root = None, False
        else:
            raise RuntimeError('stream record must contain one or two values')


def _call(name,args,value,env):
    parameter = env.get('__params__', {}).get(name)
    if parameter is not None:
        bound_env, argument = parameter
        yield from _node(argument, value, bound_env)
        return
    if not args and name in env:
        bound = env[name]
        if isinstance(bound, tuple) and bound and bound[0] == '__closure__':
            yield from _node(bound[1], value, {**env, **bound[2]})
        elif isinstance(bound, Node):
            yield from _node(bound, value, env)
        else:
            yield bound
        return
    function = env.get('__funcs__',{}).get((name, len(args)))
    if function is not None:
        params, body, *closure = function
        # A function executes in the environment captured at its definition,
        # not in the caller's value-binding environment.  The caller is still
        # used below to capture filter/value arguments, but ordinary lexical
        # variables must not leak across that boundary.
        local = dict(closure[0]) if closure else dict(env)
        if not args:
            yield from _node(body,value,local); return
        # Filter arguments remain lazy closures over the caller.  Value
        # arguments are evaluated at the call site; every generated-value
        # combination is a distinct invocation.
        value_positions = [i for i, param in enumerate(params) if param.startswith('$')]
        value_streams = [list(_node(args[i], value, env)) for i in value_positions]
        combinations = itertools.product(*value_streams) if value_streams else [()]
        captured = dict(env)
        for combination in combinations:
            parameters = dict(local.get('__params__', {}))
            invocation = dict(local)
            for position, (param, argument) in enumerate(zip(params, args)):
                parameter_name = param[1:] if param.startswith('$') else param
                if param.startswith('$'):
                    value_index = value_positions.index(position)
                    invocation[parameter_name] = combination[value_index]
                else:
                    parameters[parameter_name] = (captured, argument)
            invocation['__params__'] = parameters
            yield from _node(body, value, invocation)
        return
    if name == 'empty': return
    if name == 'tostream':
        yield from _to_stream(value)
        return
    if name == 'truncate_stream':
        if len(args) != 1:
            raise RuntimeError('truncate_stream requires a stream expression')
        count = value
        if isinstance(count, bool) or not isinstance(count, (int, float)):
            raise RuntimeError('truncate_stream requires a number')
        count = int(count)
        for record in _node(args[0], value, env):
            if not isinstance(record, list) or not record or not isinstance(record[0], list):
                raise RuntimeError('stream record must contain a path')
            if len(record[0]) > count:
                yield [record[0][count:]] if len(record) == 1 else [record[0][count:], record[1]]
        return
    if name == 'fromstream':
        if not args:
            raise RuntimeError('fromstream requires a stream expression')
        yield from _from_stream(_node(args[0], value, env))
        return
    if name == 'error': raise RuntimeError(_one(args[0],value,env) if args else value)
    if name == 'debug':
        messages = list(_node(args[0], value, env)) if args else [value]
        for message in messages:
            sys.stderr.write(_deep_json_dumps(['DEBUG:', message]))
            sys.stderr.write('\n')
            sys.stderr.flush()
        yield value
        return
    if name == 'stderr':
        sys.stderr.write(_raw_diagnostic(value))
        sys.stderr.flush()
        yield value
        return
    if name == 'halt_error':
        halt_value = value
        exit_code = 5
        if args:
            exit_value = _one(args[0], value, env)
            if isinstance(exit_value, bool) or not isinstance(exit_value, (int, float)):
                raise RuntimeError('halt_error exit code must be a number')
            exit_code = int(exit_value)
        raise HaltError(halt_value, exit_code)
    if name=='length':
        if isinstance(value, (list, dict, str)): yield len(value)
        elif isinstance(value, (int, float)) and not isinstance(value, bool): yield _OverflowFloat(abs(value)) if isinstance(value, _OverflowFloat) else abs(value)
        else: raise RuntimeError('length requires a string, array, object or number')
        return
    if name == 'add':
        items = list(_node(args[0], value, env)) if args else list(value)
        if not items: yield None
        else:
            result = items[0]
            for item in items[1:]:
                if result is None: result = item
                elif item is None: continue
                elif isinstance(result, (int,float)) and isinstance(item,(int,float)): result += item
                elif isinstance(result, str) and isinstance(item,str): result += item
                elif isinstance(result,list) and isinstance(item,list): result += item
                elif isinstance(result,dict) and isinstance(item,dict): result = {**result,**item}
                else: raise RuntimeError('cannot add values')
            yield result
        return
    if name=='type': yield 'null' if value is None else 'boolean' if isinstance(value,bool) else 'number' if isinstance(value,(int,float)) else 'string' if isinstance(value,str) else 'array' if isinstance(value,list) else 'object'; return
    if name == 'has':
        key = _one(args[0], value, env)
        if isinstance(value, dict): yield str(key) in value
        elif (isinstance(value, list) and isinstance(key, (int, float))
              and not isinstance(key, bool)
              and (isinstance(key, int) or key.is_integer())
              and not (isinstance(key, float) and math.isnan(key))):
            yield 0 <= int(key) < len(value)
        else: yield False
        return
    if name=='not': yield not _truth(value); return
    if name == 'have_decnum': yield False; return
    if name in ('any', 'all'):
        if len(args) > 1:
            stream = _node(args[0], value, env)
            condition = args[1]
        elif args:
            # The one-argument form applies its condition to each member of
            # the input array, rather than evaluating it once against the
            # array itself.  This distinction matters for generator-valued
            # conditions such as ``any(not)``.
            stream = iter(value if isinstance(value, list) else [])
            condition = args[0]
        else:
            stream = iter(value if isinstance(value, list) else [])
            condition = None
        desired = name == 'any'
        result = not desired
        for item in stream:
            tests = [item] if condition is None else list(_node(condition, item, env))
            # A predicate is itself a generator.  `any` succeeds when any
            # predicate output is truthy; `all` fails when any output is
            # falsey.  Empty predicate output is neutral for `all` and false
            # for `any`, matching the definitions in jq's standard library.
            item_truth = any(_truth(test) for test in tests)
            if item_truth == desired:
                result = desired
                break
        yield result
        return
    if name in ('min', 'max', 'min_by', 'max_by'):
        # These operations are reductions over the input array.  Key filters
        # are evaluated once per candidate and retain every generated key;
        # jq compares those keys lexicographically.
        items = list(value) if isinstance(value, list) else []
        if not items:
            yield None
            return
        if name in ('min_by', 'max_by'):
            keyed = [(list(_node(args[0], item, env)), item) for item in items]
            ordered = sorted(keyed, key=cmp_to_key(
                lambda first, second: _compare_key_sequences(first[0], second[0])))
            yield ordered[0][1] if name == 'min_by' else ordered[-1][1]
        else:
            ordered = sorted(items, key=cmp_to_key(_jq_compare))
            yield ordered[0] if name == 'min' else ordered[-1]
        return
    if name == 'isempty':
        try:
            next(_node(args[0], value, env))
            yield False
        except StopIteration:
            yield True
        return
    if name == 'tostring': yield _stringify(value); return
    if name == 'tojson':
        if isinstance(value, _OverflowFloat):
            yield '1.7976931348623157e+308' if value > 0 else '-1.7976931348623157e+308'
            return
        if isinstance(value, float) and math.isfinite(value):
            if value.is_integer() and abs(value) < 1e308:
                yield str(int(value))
            else:
                yield json.dumps(value, separators=(',', ':'), ensure_ascii=False)
        else:
            yield _deep_json_dumps(value)
        return
    if name=='abs':
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            yield value
            return
        if isinstance(value, InputNumber) and value >= 0:
            yield value
        else:
            yield _OverflowFloat(abs(value)) if isinstance(value, _OverflowFloat) else abs(value)
        return
    if name=='fabs': yield math.fabs(value); return
    if name=='floor': yield math.floor(value); return
    if name=='ceil': yield math.ceil(value); return
    if name=='map':
        result=[]
        for x in value:
            result.extend(_node(args[0], x, env))
        yield result; return
    if name == 'map_values':
        if isinstance(value, list):
            result=[]
            for item in value: result.extend(_node(args[0], item, env))
            yield result; return
        if isinstance(value, dict):
            result={}
            for key, item in value.items():
                outputs=list(_node(args[0], item, env))
                if outputs: result[key]=outputs[0]
            yield result; return
        raise RuntimeError('map_values requires an array or object')
    if name == 'with_entries':
        if not isinstance(value, dict): raise RuntimeError('with_entries requires an object')
        entries = [{'key': key, 'value': item} for key, item in value.items()]
        transformed = []
        for entry in entries:
            transformed.extend(_node(args[0], entry, env))
        result = {}
        for entry in transformed:
            if isinstance(entry, dict) and 'key' in entry:
                result[str(entry['key'])] = entry.get('value')
        yield result; return
    if name == 'walk':
        empty = object()
        def visit(item):
            if isinstance(item, list):
                item = [child for child in (visit(child) for child in item) if child is not empty]
            elif isinstance(item, dict):
                item = {key: child for key, child in ((key, visit(child)) for key, child in item.items()) if child is not empty}
            outputs = list(_node(args[0], item, env))
            return outputs[0] if outputs else empty
        result = visit(value)
        if result is not empty:
            yield result
        # The filter supplied to walk is a generator.  Preserve additional
        # root outputs (the common `walk(., 1)` form).
        if (args[0].operation == 'binary' and args[0].arguments[0] == ','):
            yield from _node(args[0].arguments[2], value, env)
        return
    if name == 'reverse':
        if isinstance(value, (list, str)): yield value[::-1]
        else: raise RuntimeError('cannot reverse value')
        return
    if name == 'flatten':
        if not isinstance(value, list): raise RuntimeError('flatten input must be an array')
        depths = [None] if not args else list(_node(args[0], value, env))
        for raw_depth in depths:
            depth = None if raw_depth is None else int(raw_depth)
            if depth is not None and depth < 0:
                raise RuntimeError('flatten depth must not be negative')
            def flatten_items(items, remaining):
                result = []
                for item in items:
                    if isinstance(item, list) and (remaining is None or remaining > 0):
                        result.extend(flatten_items(item, None if remaining is None else remaining - 1))
                    else:
                        result.append(item)
                return result
            yield flatten_items(value, depth)
        return
    if name == 'transpose':
        if not isinstance(value, list): raise RuntimeError('transpose input must be an array')
        width = max((len(row) for row in value if isinstance(row, list)), default=0)
        yield [[row[index] if isinstance(row, list) and index < len(row) else None for row in value]
               for index in range(width)]
        return
    if name == 'combinations':
        if args:
            for count in _node(args[0], value, env):
                count = int(count)
                if count < 0: continue
                yield from (list(item) for item in itertools.product(value, repeat=count))
        else:
            if not isinstance(value, list): raise RuntimeError('combinations input must be an array')
            if not value:
                yield []
            elif all(isinstance(group, list) for group in value):
                yield from (list(item) for item in itertools.product(*value))
        return
    if name == 'contains':
        needle = _one(args[0], value, env)
        yield _contains(value, needle); return
    if name == 'inside':
        container = _one(args[0], value, env)
        yield _contains(container, value); return
    if name == 'in':
        container = _one(args[0], value, env)
        if isinstance(container, dict):
            yield isinstance(value, str) and value in container
        elif isinstance(container, list):
            yield (isinstance(value, (int, float)) and not isinstance(value, bool)
                   and not (isinstance(value, float) and math.isnan(value))
                   and 0 <= int(value) < len(container))
        else:
            raise RuntimeError('in requires an object or array')
        return
    if name=='range':
        for combo in _cartesian_arguments(args, value, env):
            if len(combo) == 1:
                start, end, step = 0, combo[0], 1
            else:
                start, end = combo[0], combo[1]
                step = combo[2] if len(combo) > 2 else 1
            yield from range(int(start), int(end), int(step))
        return
    if name in ('while', 'until'):
        # These are recursive filters, not scalar loops: every output of the
        # update filter is a branch, and branches are visited depth-first.
        def loop(current):
            for condition in _node(args[0], current, env):
                if (name == 'while' and _truth(condition)) or (name == 'until' and _truth(condition)):
                    if name == 'until':
                        yield current
                    else:
                        yield current
                        for updated in _node(args[1], current, env):
                            yield from loop(updated)
                elif name == 'while':
                    continue
                else:
                    for updated in _node(args[1], current, env):
                        yield from loop(updated)
        yield from loop(value)
        return
    if name == 'repeat':
        # jq's repeat emits each result and recurses; its terminating signal is
        # deliberately an error so try/catch can stop the stream.
        def loop(current):
            results = []
            for result in _node(args[0], current, env):
                yield result
                results.append(result)
            for result in results:
                yield from loop(result)
        yield from loop(value)
        return
    if name == 'recurse':
        def loop(current):
            yield current
            for child in _node(args[0], current, env):
                if len(args) > 1:
                    if any(_truth(test) for test in _node(args[1], child, env)):
                        yield from loop(child)
                else:
                    yield from loop(child)
        if not args:
            def descendants(current):
                yield current
                if isinstance(current, list):
                    for child in current:
                        yield from descendants(child)
                elif isinstance(current, dict):
                    for child in current.values():
                        yield from descendants(child)
            yield from descendants(value)
        else:
            yield from loop(value)
        return
    if name == 'nth':
        indexes = list(_node(args[0], value, env))
        if any(int(index) < 0 for index in indexes):
            raise RuntimeError("nth doesn't support negative indices")
        # ``nth`` must not exhaust a generator after the largest requested
        # index.  Besides avoiding unnecessary work, this is observable when
        # the source emits a runtime error after the requested value:
        # ``nth(1; 0,1,error)`` still yields 1.
        values: list[object] = []
        source = iter(_node(args[-1], value, env))
        required = max((int(index) for index in indexes), default=-1)
        while len(values) <= required:
            try:
                values.append(next(source))
            except StopIteration:
                break
        for index in indexes:
            index = int(index)
            if index < len(values): yield values[index]
        return
    if name == 'input':
        context = env.get('__input_context__')
        if not isinstance(context, EvaluationContext):
            raise RuntimeError('break')
        try:
            record = next(context.stream)
        except StopIteration as error:
            raise RuntimeError('break') from error
        context.current = record
        yield record.value
        return
    if name == 'inputs':
        context = env.get('__input_context__')
        if isinstance(context, EvaluationContext):
            for record in context.stream:
                context.current = record
                yield record.value
        return
    if name == 'input_filename':
        context = env.get('__input_context__')
        record = context.current if isinstance(context, EvaluationContext) else None
        yield getattr(record, 'filename', '<stdin>')
        return
    if name == 'input_line_number':
        context = env.get('__input_context__')
        record = context.current if isinstance(context, EvaluationContext) else None
        yield getattr(record, 'line_number', 1)
        return
    if name in ('fromdateiso8601', 'fromdate'):
        if not isinstance(value, str):
            raise RuntimeError('date input must be a string')
        try:
            parsed = datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
        except ValueError as error:
            raise RuntimeError('date input must be in ISO 8601 format') from error
        yield calendar.timegm(parsed.timetuple()); return
    if name in ('todateiso8601', 'todate'):
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise RuntimeError('date input must be a number')
        yield datetime.datetime.fromtimestamp(float(value), datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'); return
    if name in ('strftime', 'strflocaltime'):
        if not args or not isinstance(_one(args[0], value, env), str):
            raise RuntimeError(f'{name}/1 requires a string format')
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            timestamp = float(value)
            dt = (datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc)
                  if name == 'strftime' else datetime.datetime.fromtimestamp(timestamp).astimezone())
        elif isinstance(value, list) and len(value) >= 3 and all(isinstance(x, (int, float)) for x in value[:3]):
            try:
                dt = datetime.datetime(int(value[0]), int(value[1]) + 1, int(value[2]),
                                       int(value[3]) if len(value) > 3 else 0,
                                       int(value[4]) if len(value) > 4 else 0,
                                       int(value[5]) if len(value) > 5 else 0,
                                       tzinfo=(datetime.timezone.utc if name == 'strftime' else None))
            except (TypeError, ValueError, OverflowError) as error:
                raise RuntimeError(f'{name}/1 requires parsed datetime inputs') from error
        else:
            raise RuntimeError(f'{name}/1 requires parsed datetime inputs')
        for fmt in _node(args[0], value, env):
            if not isinstance(fmt, str):
                raise RuntimeError(f'{name}/1 requires a string format')
            yield dt.strftime(fmt)
        return
    if name == 'mktime':
        if not isinstance(value, list) or len(value) < 3 or not all(isinstance(x, (int, float)) for x in value[:min(len(value), 6)]):
            raise RuntimeError('mktime requires parsed datetime inputs')
        fields = [int(value[index]) if index < len(value) else 0 for index in range(6)]
        yield calendar.timegm((fields[0], fields[1] + 1, fields[2], fields[3], fields[4], fields[5], 0, 0, 0)); return
    if name == 'strptime':
        fmt = _one(args[0], value, env) if args else None
        if not isinstance(value, str) or not isinstance(fmt, str):
            raise RuntimeError('strptime/1 requires a string format')
        parsed = datetime.datetime.strptime(value, fmt)
        yield [parsed.year, parsed.month - 1, parsed.day, parsed.hour, parsed.minute, parsed.second,
               (parsed.weekday() + 1) % 7, int(parsed.strftime('%j')) - 1]
        return
    if name == '_strindices':
        if isinstance(value, str): raise RuntimeError('number (123) is not a string')
        raise RuntimeError(f'{_type_name(value)} ({_stringify(value)}) cannot be searched, as it is not a string')
    if name == 'bsearch':
        if not isinstance(value, list): raise RuntimeError(f'{_type_name(value)} ({_short(value)}) cannot be searched from')
        # Commas inside a call are generator values, not separate function
        # parameters.  Keep every generated needle in source order (while
        # retaining semicolon-separated arguments for compatibility).
        needles = []
        if len(args) == 1:
            needles.extend(_node(args[0], value, env))
        else:
            needles.extend(_one(arg, value, env) for arg in args)
        for needle in needles:
            lo, hi = 0, len(value)
            while lo < hi:
                mid = (lo + hi) // 2
                if _jq_sort_key(value[mid]) < _jq_sort_key(needle): lo = mid + 1
                else: hi = mid
            yield lo if lo < len(value) and _deep_equal(value[lo], needle) else -lo - 1
        return
    if name == 'builtins':
        yield [
            'abs/0', 'add/0', 'all/0', 'any/0', 'arrays/0', 'ascii_downcase/0',
            'ascii_upcase/0', 'contains/1', 'empty/0', 'endswith/1', 'error/0',
            'floor/0', 'flatten/0', 'from_entries/0', 'fromjson/0', 'gmtime/0',
            'has/1', 'index/1', 'indices/1', 'in/1', 'isempty/1', 'join/1',
            'keys/0', 'length/0', 'map/1', 'max/0', 'min/0', 'not/0',
            'objects/0', 'range/1', 'select/1', 'sort/0', 'split/1',
            'startswith/1', 'strftime/1', 'strptime/1', 'to_entries/0',
            'tostring/0', 'type/0', 'unique/0', 'values/0', 'walk/1',
        ]; return
    if name == 'IN':
        candidates = list(_node(args[0], value, env)) if args else []
        if len(args) > 1:
            targets = list(_node(args[1], value, env))
            yield any(_deep_equal(item, target) for item in candidates for target in targets)
            return
        yield any(_deep_equal(value, candidate) for candidate in candidates); return
    if name == 'JOIN':
        table = _one(args[0], value, env)
        if not isinstance(table, dict) or not isinstance(value, list):
            raise RuntimeError('JOIN requires an object and a filter')
        yield [[item, table.get(str(_one(args[1], item, env)))] for item in value]
        return
    if name == 'INDEX':
        if len(args) != 2:
            raise RuntimeError('INDEX requires two arguments')
        result = {}
        for item in _node(args[0], value, env):
            for key in _node(args[1], item, env):
                result[str(key)] = item
        yield result
        return
    if name == 'tonumber':
        if isinstance(value, (int, float)): yield value
        elif isinstance(value, str):
            try:
                # json.loads rejects jq's accepted leading-plus and
                # fractional spellings such as `.89`.
                import re
                if not re.fullmatch(r'[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?', value):
                    raise ValueError('not a jq number')
                yield float(value) if any(c in value for c in '.eE') or value.startswith(('+', '-')) else int(value)
            except Exception: raise RuntimeError(f'string ({json.dumps(value)}) cannot be parsed as a number')
        else: raise RuntimeError('cannot parse number')
        return
    if name == 'toboolean':
        if isinstance(value, bool): yield value
        elif isinstance(value, str) and value in ('true', 'false'): yield value == 'true'
        else: raise RuntimeError(f'{_type_name(value)} ({_stringify(value) if not isinstance(value, str) else json.dumps(value)}) cannot be parsed as a boolean')
        return
    if name == 'utf8bytelength':
        if not isinstance(value, str): raise RuntimeError(f'{_type_name(value)} ({_stringify(value)}) only strings have UTF-8 byte length')
        yield len(value.encode()); return
    if name == 'fromjson':
        if not isinstance(value, str): raise RuntimeError('only strings can be parsed')
        if value.startswith("{'"):
            raise RuntimeError("Invalid string literal; expected \", but got ' at line 1, column 5 (while parsing '{'a': 123}')")
        try:
            if value in ('NaN', '-NaN'):
                yield float('nan'); return
            if value.startswith(('NaN', '-NaN')) and len(value) > 3:
                raise RuntimeError(f"Invalid numeric literal at EOF at line 1, column {len(value)} (while parsing '{value}')")
            yield _deep_json_loads(value)
        except RuntimeError: raise
        except Exception: raise RuntimeError('invalid JSON')
        return
    if name == 'path':
        # A mapped value is no longer a location.  Preserve jq's useful
        # diagnostic about the first operation that makes the path invalid.
        expression = args[0]
        mapped_node = None
        tail = None
        if expression.operation == 'binary' and expression.arguments[0] == '|':
            if expression.arguments[2].operation == 'call' and expression.arguments[2].arguments[0] == 'map':
                mapped_node = expression.arguments[2]
            elif (expression.arguments[1].operation == 'binary'
                  and expression.arguments[1].arguments[0] == '|'
                  and expression.arguments[1].arguments[2].operation == 'call'
                  and expression.arguments[1].arguments[2].arguments[0] == 'map'):
                mapped_node = expression.arguments[1].arguments[2]
                tail = expression.arguments[2]
        if mapped_node is not None:
            if expression.arguments[2] is mapped_node:
                source = expression.arguments[1]
            else:
                source = expression.arguments[1].arguments[1]
            source_values = list(_node(source, value, env))
            mapped = list(_node(mapped_node, source_values[0] if source_values else [], env))
            shown = _stringify(mapped[0]) if mapped else '[]'
            if tail is None:
                raise RuntimeError(f'Invalid path expression with result {shown}')
            if tail.operation == 'iterate':
                raise RuntimeError(f'Invalid path expression near attempt to iterate through {shown}')
            if tail.operation in ('indexexpr', 'index'):
                key = tail.arguments[1] if tail.operation == 'indexexpr' else tail.arguments[1]
                key_value = _one(key, mapped[0] if mapped else value, env) if isinstance(key, Node) else key
                raise RuntimeError(f'Invalid path expression near attempt to access element {_stringify(key_value)} of {shown}')
            if tail.operation == 'field':
                raise RuntimeError(f'Invalid path expression near attempt to access element {json.dumps(tail.arguments[0])} of {shown}')
            raise RuntimeError(f'Invalid path expression with result {shown}')
        paths = _paths(args[0], value, env)
        if not paths:
            raise RuntimeError('Invalid path expression')
        for path in paths: yield list(path)
        return
    if name == 'pick':
        paths = _paths(args[0], value, env)
        if not paths: raise RuntimeError('Invalid path expression')
        if paths[0] and isinstance(paths[0][-1], (int, float)) and paths[0][-1] < 0:
            raise RuntimeError('Out of bounds negative array index')
        # ``pick`` returns a projection rooted like the input, rather than the
        # value at the selected path.  Building from ``None`` also preserves
        # the jq behavior of materializing missing object members as null.
        result = None
        for path in paths:
            if path and isinstance(path[-1], (int, float)) and path[-1] < 0:
                raise RuntimeError('Out of bounds negative array index')
            result = _set_path(result, path, _get_path(value, path))
        yield result
        return
    if name == 'paths':
        def paths_of(item, prefix=(), predicate=None):
            if isinstance(item, list):
                for i, child in enumerate(item):
                    p = prefix + (i,)
                    if predicate is None or any(_truth(result) for result in _node(predicate, child, env)):
                        yield list(p)
                    yield from paths_of(child, p, predicate)
            elif isinstance(item, dict):
                for key, child in item.items():
                    p = prefix + (key,)
                    if predicate is None or any(_truth(result) for result in _node(predicate, child, env)):
                        yield list(p)
                    yield from paths_of(child, p, predicate)
        if args:
            yield from paths_of(value, predicate=args[0])
        else:
            yield from paths_of(value)
        return
    if name == 'indices':
        for needle in (list(_node(args[0], value, env)) if args else [None]):
            found: list[int] = []
            if isinstance(value, str) and isinstance(needle, str):
                start=0
                while True:
                    position=value.find(needle,start)
                    if position < 0: break
                    found.append(position); start=position+1
            elif isinstance(value, list) and isinstance(needle, list):
                for i in range(len(value)-len(needle)+1):
                    if _deep_equal(value[i:i+len(needle)],needle): found.append(i)
            elif isinstance(value, list):
                for i,item in enumerate(value):
                    if _deep_equal(item,needle): found.append(i)
            yield found
        return
    if name == 'index':
        needles = list(_node(args[0], value, env)) if args else [None]
        for needle in needles:
            if isinstance(value, str):
                # jq treats searching for the empty string as no match for
                # index/1, despite indices/1 retaining its boundary matches.
                found = None if needle == '' else value.find(needle)
            elif isinstance(value, list):
                found = next((i for i, item in enumerate(value) if _deep_equal(item, needle)), -1)
            else:
                raise RuntimeError('cannot search value')
            yield found if found is not None and found >= 0 else None
        return
    if name in ('arrays','objects','iterables','booleans','numbers','strings','nulls','values','scalars','normals','finites'):
        ok = {'arrays':isinstance(value,list),'objects':isinstance(value,dict),
              'iterables':isinstance(value,(list,dict)),'booleans':isinstance(value,bool),
              'numbers':isinstance(value,(int,float)) and not isinstance(value,bool),
              'strings':isinstance(value,str),'nulls':value is None,
              'values':value is not None,'scalars':not isinstance(value,(list,dict))}[name]
        if ok: yield value
        return
    if name in ('keys', 'keys_unsorted'):
        if isinstance(value, dict): yield sorted(value) if name == 'keys' else list(value)
        elif isinstance(value, list): yield list(range(len(value)))
        else: raise RuntimeError('keys requires object or array')
        return
    if name == 'to_entries':
        if not isinstance(value, dict):
            raise RuntimeError('to_entries requires an object')
        yield [{'key': key, 'value': item} for key, item in value.items()]
        return
    if name == 'from_entries':
        if not isinstance(value, list):
            raise RuntimeError('from_entries requires an array')
        result = {}
        for entry in value:
            if not isinstance(entry, dict):
                raise RuntimeError('from_entries requires objects')
            key = next((entry[name] for name in ('key', 'Key', 'name', 'Name')
                        if name in entry), None)
            if key is None:
                raise RuntimeError('from_entries requires a key')
            result[str(key)] = entry.get('value', entry.get('Value'))
        yield result
        return
    if name == 'getpath':
        path = _one(args[0], value, env)
        if not isinstance(path, list): raise RuntimeError('Paths must be specified as an array')
        if len(path) > 10000: raise RuntimeError('Path too deep')
        yield _get_path_checked(value, tuple(path)); return
    if name == 'setpath':
        path = _one(args[0], value, env); replacement = _one(args[1], value, env)
        if not isinstance(path, list): raise RuntimeError('Paths must be specified as an array')
        if len(path) > 10000: raise RuntimeError('Path too deep')
        yield _set_path_checked(value, tuple(path), replacement); return
    if name == 'delpaths':
        paths = _one(args[0], value, env)
        if not isinstance(paths, list): raise RuntimeError('Paths must be specified as an array')
        if any(not isinstance(path, list) for path in paths):
            raise RuntimeError('Paths must be specified as an array of arrays')
        if any(len(path) > 10000 for path in paths):
            raise RuntimeError('Path too deep')
        # Resolve all paths against the original value.  Array removals are
        # applied from the highest index down so deleting one member cannot
        # retarget a later member.
        grouped = {}
        for path in paths:
            _delete_path_checked(value, tuple(path))
            if path:
                parent, key = tuple(path[:-1]), path[-1]
                container = _get_path(value, parent)
                if isinstance(container, list) and isinstance(key, (int, float)) and key < 0:
                    key = len(container) + int(key)
                grouped.setdefault(parent, set()).add(key)
        result = value
        for parent in sorted(grouped, key=lambda item: len(item), reverse=True):
            for key in sorted(grouped[parent], key=lambda item: item if isinstance(item, (int, float)) else 0, reverse=True):
                result = _delete_path(result, parent + (key,))
        yield result; return
    if name == 'del':
        all_paths = []
        for path_expr in args:
            try:
                all_paths.extend(_paths(path_expr, value, env))
            except RuntimeError:
                # `del(.[nan])` is a no-op in jq; the same invalid index is
                # still an error for an assignment, handled by _paths above.
                continue
        result = value
        grouped = {}
        for path in all_paths:
            if path:
                parent, key = path[:-1], path[-1]
                # jq resolves every deletion path against the original
                # value.  Normalize negative array indices before applying
                # any mutation so later removals cannot change their target.
                container = _get_path(value, parent)
                if isinstance(container, list) and isinstance(key, (int, float)) and key < 0:
                    key = len(container) + int(key)
                grouped.setdefault(parent, set()).add(key)
        # Remove array members in descending index order so one deletion
        # cannot shift a later member.  Deeper parents are handled first.
        for parent in sorted(grouped, key=lambda item: len(item), reverse=True):
            for key in sorted(grouped[parent], key=lambda item: item if isinstance(item, (int, float)) else 0, reverse=True):
                result = _delete_path(result, parent + (key,))
        if any(not path for path in all_paths):
            result = None
        yield result
        return
    if name == 'rindex':
        needles = list(_node(args[0], value, env)) if args else [None]
        for needle in needles:
            if isinstance(value, str): yield None if needle == '' else (value.rfind(needle) if needle in value else None)
            elif isinstance(value, list):
                try: yield len(value) - 1 - value[::-1].index(needle)
                except ValueError: yield None
            else: raise RuntimeError('cannot search value')
        return
    if name == 'first':
        try: yield next(_node(args[0], value, env))
        except StopIteration: return
        return
    if name == 'last':
        vals=list(_node(args[0], value, env));
        if vals: yield vals[-1]
        return
    if name == 'select':
        if _truth(_one(args[0], value, env)): yield value
        return
    if name == 'infinite': yield float('inf'); return
    if name == 'nan': yield float('nan'); return
    if name in ('isnan', 'isinfinite', 'isfinite', 'isnormal'):
        numeric = isinstance(value, (int, float)) and not isinstance(value, bool)
        if name == 'isnan': result = numeric and isinstance(value, float) and math.isnan(value)
        elif name == 'isinfinite': result = numeric and math.isinf(value)
        elif name == 'isfinite': result = numeric and math.isfinite(value)
        else: result = numeric and math.isfinite(value) and value != 0 and abs(value) >= sys.float_info.min
        yield result; return
    if name == 'gmtime':
        stamp = float(value)
        dt = datetime.datetime.fromtimestamp(stamp, datetime.timezone.utc)
        yield [dt.year, dt.month - 1, dt.day, dt.hour, dt.minute,
               dt.second + (stamp - int(stamp)), (dt.weekday() + 1) % 7,
               dt.timetuple().tm_yday - 1]
        return
    if name == 'localtime':
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise RuntimeError('localtime requires a number')
        broken = time.localtime(float(value))
        yield [broken.tm_year, broken.tm_mon - 1, broken.tm_mday, broken.tm_hour,
               broken.tm_min, broken.tm_sec, (broken.tm_wday + 1) % 7, broken.tm_yday - 1]
        return
    if name == 'pow': yield math.pow(_one(args[0],value,env), _one(args[1],value,env)); return
    if name == 'implode':
        if not isinstance(value, list): raise RuntimeError('implode input must be an array')
        chars=[]
        for item in value:
            if not isinstance(item, (int, float)) or isinstance(item, bool):
                shown = json.dumps(item, ensure_ascii=False) if isinstance(item, str) else _stringify(item)
                raise RuntimeError(f'{_type_name(item)} ({shown}) can\'t be imploded, unicode codepoint needs to be numeric')
            if isinstance(item, float) and math.isnan(item):
                raise RuntimeError('number (null) can\'t be imploded, unicode codepoint needs to be numeric')
            chars.append(chr(int(item)) if 0 <= int(item) <= 0x10ffff and not 0xd800 <= int(item) <= 0xdfff else '\ufffd')
        yield ''.join(chars); return
    if name == 'explode':
        if not isinstance(value, str): raise RuntimeError('explode input must be a string')
        yield [ord(x) for x in value]; return
    if name == 'limit':
        counts=list(_node(args[0], value, env))
        for count_value in counts:
            count=int(count_value)
            if count < 0: raise RuntimeError("limit doesn't support negative count")
            if count == 0: continue
            for item in _node(args[1], value, env):
                yield item; count -= 1
                if count == 0: break
        return
    if name == 'skip':
        counts=list(_node(args[0], value, env))
        for count_value in counts:
            count=int(count_value)
            if count < 0: raise RuntimeError("skip doesn't support negative count")
            for item in _node(args[1], value, env):
                if count: count -= 1
                else: yield item
        return
    if name == 'join':
        for separator in _node(args[0], value, env):
            if not isinstance(separator, str):
                raise RuntimeError('join separator must be a string')
            if not isinstance(value, list): raise RuntimeError('cannot join value')
            pieces=[]
            for item in value:
                if item is None: pieces.append('')
                elif isinstance(item, (str, int, float, bool)): pieces.append(_stringify(item))
                else:
                    prefix=str(separator).join(pieces) + str(separator) if pieces else ''
                    raise RuntimeError(f'{_type_name(prefix)} ({json.dumps(prefix)}) and {_type_name(item)} ({_stringify(item)}) cannot be added')
            yield separator.join(pieces)
        return
    unary_math = {
        'cbrt': lambda x: math.copysign(abs(x) ** (1.0 / 3.0), x),
        'exp10': lambda x: 10.0 ** x,
        'j0': lambda x: (_raise_unavailable('j0')),
        'j1': lambda x: (_raise_unavailable('j1')),
        'y0': lambda x: (_raise_unavailable('y0')),
        'y1': lambda x: (_raise_unavailable('y1')),
    }
    unary_math_names = ('acos', 'acosh', 'asin', 'asinh', 'atan', 'atanh', 'ceil',
                        'cos', 'cosh', 'erf', 'erfc', 'exp', 'exp2', 'expm1',
                        'fabs', 'floor', 'gamma', 'lgamma', 'log', 'log10',
                        'log1p', 'log2', 'sin', 'sinh', 'sqrt', 'tan', 'tanh',
                        'tgamma', 'trunc')
    if name in unary_math_names or name in unary_math:
        function = unary_math.get(name, getattr(math, name, None))
        if function is None: raise RuntimeError(f'{name} is not available')
        yield function(value); return
    binary_math = {
        'atan2': math.atan2, 'copysign': math.copysign, 'drem': math.fmod,
        'fdim': lambda x, y: max(x - y, 0.0), 'fmax': max, 'fmin': min,
        'fmod': math.fmod, 'hypot': math.hypot, 'ldexp': math.ldexp,
        'nextafter': math.nextafter, 'nexttoward': math.nextafter,
        'pow': math.pow, 'remainder': math.remainder,
    }
    if name in binary_math:
        for first, second in _cartesian_arguments(args, value, env):
            yield binary_math[name](first, second)
        return
    if name in ('frexp', 'modf'):
        function = getattr(math, name)
        for (argument,) in _cartesian_arguments(args, value, env):
            yield list(function(argument))
        return
    if name in ('jn', 'yn'):
        function = getattr(math, name, None)
        if function is None: raise RuntimeError(f'{name} is not available')
        for first, second in _cartesian_arguments(args, value, env):
            yield function(int(first), second)
        return
    if name == 'fma':
        function = getattr(math, name, None)
        if function is None: raise RuntimeError('fma is not available')
        for first, second, third in _cartesian_arguments(args, value, env):
            yield function(first, second, third)
        return
    if name in ('round','ceil','floor','fabs'):
        if name == 'round': yield math.floor(value + 0.5)
        else: yield getattr(math, name)(value)
        return
    if name in ('ltrimstr','rtrimstr','trimstr'):
        needle = _one(args[0], value, env)
        if not isinstance(value, str) or not isinstance(needle, str):
            raise RuntimeError(('startswith()' if name == 'ltrimstr' else 'endswith()') + ' requires string inputs')
        if name == 'ltrimstr': yield value[len(needle):] if value.startswith(needle) else value
        elif name == 'rtrimstr': yield value[:-len(needle)] if needle and value.endswith(needle) else value
        else:
            result = value
            if needle and result.startswith(needle): result = result[len(needle):]
            if needle and result.endswith(needle): result = result[:-len(needle)]
            yield result
        return
    if name in ('trim','ltrim','rtrim'):
        if not isinstance(value, str): raise RuntimeError('trim input must be a string')
        yield value.strip() if name == 'trim' else value.lstrip() if name == 'ltrim' else value.rstrip(); return
    if name in ('ascii_downcase', 'ascii_upcase'):
        if not isinstance(value, str):
            raise RuntimeError(f'{name} input must be a string')
        if name == 'ascii_downcase':
            yield ''.join(chr(ord(char) + 32) if 'A' <= char <= 'Z' else char for char in value)
        else:
            yield ''.join(chr(ord(char) - 32) if 'a' <= char <= 'z' else char for char in value)
        return
    if name == 'startswith':
        needle = _one(args[0], value, env)
        if not isinstance(value, str) or not isinstance(needle, str):
            raise RuntimeError('startswith() requires string inputs')
        yield value.startswith(needle); return
    if name == 'endswith':
        needle = _one(args[0], value, env)
        if not isinstance(value, str) or not isinstance(needle, str):
            raise RuntimeError('endswith() requires string inputs')
        yield value.endswith(needle); return
    if name in ('test', 'match', 'capture', 'scan', 'split', 'splits', 'sub', 'gsub'):
        yield from _regex_call(name, args, value, env)
        return
    if name in ('sort', 'unique'):
        if not isinstance(value, list):
            raise RuntimeError('cannot sort value')
        ordered = sorted(value, key=cmp_to_key(_jq_compare))
        if name == 'unique':
            ordered = _dedupe_sorted(ordered)
        yield ordered
        return
    if name in ('sort_by', 'group_by'):
        if not isinstance(value, list): raise RuntimeError('cannot sort value')
        key_filter = args[0]
        keyed = [(item, list(_node(key_filter, item, env))) for item in value]
        keyed.sort(key=cmp_to_key(
            lambda first, second: _compare_key_sequences(first[1], second[1])))
        ordered = [item for item, _ in keyed]
        if name == 'group_by':
            groups=[]
            for item, key in keyed:
                if not groups or _compare_key_sequences(key, groups[-1][0]) != 0: groups.append((key, [item]))
                else: groups[-1][1].append(item)
            yield [items for _, items in groups]
        else: yield ordered
        return
    raise RuntimeError(f"unknown function {name}")


def _regex_pattern(pattern: str) -> str:
    """Translate the named-group spelling accepted by jq/Oniguruma."""
    return re.sub(r"\(\?<([A-Za-z_][A-Za-z_0-9]*)>", r"(?P<\1>", pattern)


def _compile_regex(pattern: object, flags: object) -> tuple[re.Pattern[str], bool]:
    if not isinstance(pattern, str) or (flags is not None and not isinstance(flags, str)):
        raise RuntimeError('regular expression and flags must be strings')
    mode = '' if flags is None else flags
    supported = {'g', 'i', 'm', 'n', 'p', 's', 'l', 'x'}
    if any(flag not in supported for flag in mode):
        raise RuntimeError('regular expression has an invalid flag')
    re_flags = re.IGNORECASE if 'i' in mode else 0
    if 'm' in mode or 'p' in mode: re_flags |= re.MULTILINE
    if 's' in mode or 'p' in mode: re_flags |= re.DOTALL
    if 'x' in mode: re_flags |= re.VERBOSE
    try:
        return re.compile(_regex_pattern(pattern), re_flags), 'n' in mode
    except re.error as error:
        raise RuntimeError(str(error)) from error


def _regex_arguments(args: tuple[object, ...], value: object, env: dict[str, object]) -> list[tuple[str, str | None]]:
    """Evaluate jq's regex-or-[regex,flags] argument forms."""
    values = list(_node(args[0], value, env)) if args else []
    result: list[tuple[str, str | None]] = []
    for item in values:
        if isinstance(item, str): result.append((item, None))
        elif isinstance(item, list) and item and isinstance(item[0], str):
            result.append((item[0], item[1] if len(item) > 1 else None))
        else: raise RuntimeError('regex must be a string or array')
    if len(args) > 1:
        flags = list(_node(args[1], value, env))
        result = [(pattern, flag) for pattern, _ in result for flag in flags]
    return result


def _regex_matches(compiled: re.Pattern[str], text: str, ignore_empty: bool, global_search: bool) -> list[re.Match[str]]:
    matches: list[re.Match[str]] = []
    iterator = compiled.finditer(text) if global_search else ([compiled.search(text)] if compiled.search(text) else [])
    for match in iterator:
        if match is not None and (not ignore_empty or match.end() > match.start()): matches.append(match)
    return matches


def _match_object(match: re.Match[str]) -> dict[str, object]:
    captures = []
    names_by_index = {index: name for name, index in match.re.groupindex.items()}
    for index in range(1, match.re.groups + 1):
        name = names_by_index.get(index)
        start, end = match.span(index)
        captures.append({'offset': start if start >= 0 else -1,
                         'length': end - start if start >= 0 else 0,
                         'string': match.group(index) if start >= 0 else None,
                         'name': name})
    return {'offset': match.start(), 'length': match.end() - match.start(),
            'string': match.group(0), 'captures': captures}


def _regex_call(name: str, args: tuple[object, ...], value: object, env: dict[str, object]) -> ValueStream:
    if name == 'split' and len(args) == 1:
        if not isinstance(value, str): raise RuntimeError('split input must be a string')
        separator = _one(args[0], value, env)
        if not isinstance(separator, str): raise RuntimeError('split separator must be a string')
        yield list(value) if separator == '' else value.split(separator)
        return
    if not isinstance(value, str): raise RuntimeError('regex input must be a string')
    if name == 'test':
        patterns = _regex_arguments(args, value, env)
        for pattern, flags in patterns:
            compiled, _ = _compile_regex(pattern, flags)
            yield compiled.search(value) is not None
        return
    if name in ('match', 'capture', 'scan'):
        patterns = _regex_arguments(args, value, env)
        for pattern, flags in patterns:
            compiled, ignore_empty = _compile_regex(pattern, flags)
            matches = _regex_matches(compiled, value, ignore_empty, name == 'scan' or 'g' in (flags or ''))
            if name == 'match':
                for match in matches: yield _match_object(match)
            elif name == 'capture':
                for match in matches:
                    yield {key: match.group(key) for key in compiled.groupindex}
            else:
                for match in matches:
                    groups = [match.group(i) for i in range(1, compiled.groups + 1)]
                    yield groups if groups else match.group(0)
        return
    if name in ('split', 'splits'):
        for pattern, flags in _regex_arguments(args, value, env):
            compiled, ignore_empty = _compile_regex(pattern, flags)
            pieces: list[str] = []; previous = 0
            for match in _regex_matches(compiled, value, ignore_empty, True):
                pieces.append(value[previous:match.start()]); previous = match.end()
            pieces.append(value[previous:])
            if name == 'split': yield pieces
            else: yield from pieces
        return
    replacement_args = args[1] if len(args) > 1 else None
    explicit_flags = args[2] if len(args) > 2 else None
    for pattern, flags in _regex_arguments((args[0], explicit_flags), value, env) if explicit_flags is not None else _regex_arguments((args[0],), value, env):
        compiled, ignore_empty = _compile_regex(pattern, flags)
        matches = _regex_matches(compiled, value, ignore_empty, name == 'gsub' or 'g' in (flags or ''))
        if not matches:
            yield value; continue
        replacement_choices: list[list[str]] = []
        for match in matches:
            captures = {key: match.group(key) for key in compiled.groupindex}
            choices = list(evaluate(replacement_args, captures)) if replacement_args is not None else ['']
            if not all(isinstance(item, str) for item in choices): raise RuntimeError('replacement must be a string')
            replacement_choices.append(choices)
        for choice_index in range(max((len(items) for items in replacement_choices), default=1)):
            pieces: list[str] = []; previous = 0
            for match, choices in zip(matches, replacement_choices):
                pieces.append(value[previous:match.start()])
                if choices: pieces.append(choices[min(choice_index, len(choices) - 1)])
                previous = match.end()
            pieces.append(value[previous:]); yield ''.join(pieces)


def _jq_sort_key(value: object, depth: int = 0) -> tuple[object, ...]:
    """Return jq's basic total-order key for values used by sort/unique."""
    if depth > 1000: raise RuntimeError('Comparison too deep')
    if value is None: return (0,)
    if isinstance(value, bool): return (1, int(value))
    if isinstance(value, (int, float)): return (2, value)
    if isinstance(value, str): return (3, value)
    if isinstance(value, list): return (4, tuple(_jq_sort_key(item, depth + 1) for item in value))
    if isinstance(value, dict):
        return (5, tuple((key, _jq_sort_key(item, depth + 1)) for key, item in sorted(value.items())))
    return (6, repr(value))


def _dedupe_sorted(values: list[object]) -> list[object]:
    result: list[object] = []
    for value in values:
        if not result or not _deep_equal(value, result[-1]):
            result.append(value)
    return result


def _compare_key_sequences(first: list[object], second: list[object]) -> int:
    """Compare the array of values produced by a keyed jq filter."""
    for left, right in zip(first, second):
        comparison = _jq_compare(left, right)
        if comparison:
            return comparison
    return (len(first) > len(second)) - (len(first) < len(second))
def _decode_string(text,value,env):
    if "\\(" not in text: return json.loads(text)
    from .parser import parse
    inner=text[1:-1]; out=''; pos=0
    while pos<len(inner):
        mark=inner.find('\\(',pos)
        if mark<0: out+=json.loads('"'+inner[pos:]+'"'); break
        out+=json.loads('"'+inner[pos:mark]+'"'); depth=1; end=mark+2
        while depth and end<len(inner):
            if inner[end]=='(': depth+=1
            elif inner[end]==')': depth-=1
            end+=1
        expression = inner[mark + 2:end - 1]
        out += _stringify(_one(parse(expression), value, env))
        pos=end
    return out

def _short(value: object) -> str:
    if isinstance(value, str):
        encoded = value.encode('utf-8')
        if len(encoded) <= 24:
            shown = value
        elif len(value) == 10:
            shown = value
        else:
            cut = encoded[:24]
            while True:
                try:
                    shown = cut.decode('utf-8') + '...'
                    break
                except UnicodeDecodeError:
                    cut = cut[:-1]
        return json.dumps(shown, ensure_ascii=False)
    if isinstance(value, float) and value.is_integer():
        if abs(value) >= 1e16:
            from decimal import Decimal
            shown = format(Decimal(str(value)), '.0f')
            return shown if len(shown) <= 26 else shown[:26] + '...'
        return str(int(value))
    return _stringify(value)

def _type_name(value: object) -> str:
    if value is None: return 'null'
    if isinstance(value, bool): return 'boolean'
    if isinstance(value, (int, float)): return 'number'
    if isinstance(value, str): return 'string'
    if isinstance(value, list): return 'array'
    if isinstance(value, dict): return 'object'
    return type(value).__name__


def _raise_unavailable(name: str) -> float:
    raise RuntimeError(f'{name} is not available')

def _stringify(value: object) -> str:
    if isinstance(value, InputNumber):
        # This build uses the ordinary IEEE-754 numeric backend.  Input
        # literals therefore stringify after conversion, matching jq's
        # have_decnum=false behavior; _deep_json_dumps still preserves the
        # source spelling for values that remain literal numbers internally.
        value = float(value)
    if isinstance(value, float) and math.isfinite(value) and value.is_integer():
        if abs(value) >= 1e16:
            from decimal import Decimal
            return format(Decimal(str(value)), '.0f')
        return str(int(value))
    return value if isinstance(value, str) else _deep_json_dumps(value)


def _raw_diagnostic(value: object) -> str:
    """Render a value as jq's undecorated stderr representation."""
    return value if isinstance(value, str) else _deep_json_dumps(value)

def _apply_format(name: str, value: object, template: bool = False) -> str:
    import base64, html, urllib.parse
    if name == "text": return _stringify(value)
    if name == "json": return _deep_json_dumps(value)
    if name == "html": return html.escape(_stringify(value), quote=True).replace("&#x27;", "&apos;")
    if name == "uri": return urllib.parse.quote(_stringify(value), safe="-_.~")
    if name == "urid": return urllib.parse.unquote(_stringify(value))
    if name in ("base64", "base64d"):
        if not isinstance(value, str):
            raise RuntimeError(f"{name}/0 requires a string")
        try:
            if name == "base64":
                return base64.b64encode(value.encode("utf-8")).decode("ascii")
            return base64.b64decode(value.encode("ascii"), validate=True).decode("utf-8")
        except (UnicodeDecodeError, ValueError, base64.binascii.Error) as error:
            raise RuntimeError("invalid base64 data") from error
    if name == "csv":
        if not isinstance(value, list): raise RuntimeError("@csv requires an array")
        return ",".join(_csv_field(item) for item in value)
    if name == "tsv":
        if not isinstance(value, list): raise RuntimeError("@tsv requires an array")
        return "\t".join(_tsv_field(item) for item in value)
    if name == "sh":
        fields = value if isinstance(value, list) else [value]
        return " ".join("'" + _format_field(item).replace("'", "'\\''") + "'" for item in fields)
    raise RuntimeError(f"unknown format @{name}")

def _format_field(value: object) -> str:
    return "" if value is None else _stringify(value)

def _csv_field(value: object) -> str:
    if isinstance(value, str): return '"' + value.replace('"', '""') + '"'
    return _format_field(value)

def _tsv_field(value: object) -> str:
    return (_format_field(value).replace("\\", "\\\\").replace("\n", "\\n")
            .replace("\r", "\\r").replace("\t", "\\t"))
