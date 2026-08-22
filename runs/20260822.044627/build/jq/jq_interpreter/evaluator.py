"""Ordered generator evaluator boundary."""
import json
import math

from .ast import Add, Array, Comma, Filter, Format, Identity, Iterate, Literal, Limit, Node, Pipe, Raise, StringTemplate
from .errors import RuntimeError
from .runtime import JsonValue, ValueStream, identity_stream


def evaluate(program: Filter, value: JsonValue) -> ValueStream:
    """Evaluate one input as an ordered stream of output values."""
    if isinstance(program, Node):
        yield from _node(program, value, {})
        return
    if isinstance(program, Identity):
        yield from identity_stream(value)
        return
    if isinstance(program, Iterate):
        if isinstance(value, list):
            yield from value
        elif isinstance(value, dict):
            yield from value.values()
        else:
            raise RuntimeError(f"Cannot iterate over {_type_name(value)} ({_stringify(value)})")
        return
    if isinstance(program, Literal):
        yield program.value
        return
    if isinstance(program, Pipe):
        for intermediate in evaluate(program.left, value): yield from evaluate(program.right, intermediate)
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
        text=a[0]; special={"true":True,"false":False,"null":None,"nan":float("nan"),"infinite":float("inf"),"-infinite":float("-inf"),"-nan":float("nan")}; yield special[text] if text in special else json.loads(text)
    elif op == "string": yield _decode_string(a[0], value, env)
    elif op == "format": yield _apply_format(a[0], value)
    elif op == "format_template": yield _decode_string(a[1], value, env).replace(_decode_string(a[1], value, env), _apply_format(a[0], value))
    elif op == "var":
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
            bound=dict(env)
            if not _bind_pattern(a[1], item, bound):
                continue
            # `exp as $x | rest` binds the value produced by exp while the
            # remainder continues with the original input.
            yield from _node(a[2], value, bound)
    elif op == "field": yield _index(value, a[0])
    elif op == "recurse":
        def walk(item):
            yield item
            if isinstance(item, list):
                for child in item: yield from walk(child)
            elif isinstance(item, dict):
                for child in item.values(): yield from walk(child)
        yield from walk(value)
    elif op == "index":
        for base in _node(a[0],value,env): yield _index(base,a[1])
    elif op == "iterate":
        for base in _node(a[0],value,env):
            if isinstance(base,dict): yield from base.values()
            elif isinstance(base,list): yield from base
            else: raise RuntimeError(f"Cannot iterate over {_type_name(base)} ({_stringify(base)})")
    elif op in ("indexexpr","slice"):
        for base in _node(a[0],value,env):
            if op=="slice":
                start=_one(a[1],base,env); end=None if a[2] is None else _one(a[2],base,env)
                import math as _math
                first = 0 if start is None or (isinstance(start, float) and _math.isnan(start)) else _math.floor(start)
                last = None if end is None or (isinstance(end, float) and _math.isnan(end)) else _math.ceil(end)
                yield base[int(first):None if last is None else int(last)]
            else:
                for key in _node(a[1], base, env):
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
            yield -x
    elif op == "optional":
        try: yield from _node(a[0],value,env)
        except (RuntimeError, ValueError, TypeError, IndexError): return
    elif op == "if":
        # The condition is a filter, not a scalar expression.  jq evaluates
        # each condition result independently and therefore may select both
        # branches for one input.
        for condition in _node(a[0], value, env):
            branch = a[1] if _truth(condition) else a[2]
            yield from _node(branch, value, env)
    elif op == "try":
        try: yield from _node(a[0],value,env)
        except (RuntimeError, ValueError, TypeError, IndexError) as error:
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
        states=list(_node(a[0], value, env)); initial=list(_node(a[2], value, env))
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
        program: Node = node
        while program.operation == 'defprog':
            definition = program.arguments[0]
            funcs[(definition.arguments[0], len(definition.arguments[1]))] = (definition.arguments[1], definition.arguments[2])
            program = program.arguments[1]
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

def _one(node, value, env):
    vals=list(_node(node,value,env)); return vals[0] if vals else None
def _truth(x): return x is not None and x is not False
def _index(v,k):
    if v is None:
        return None
    if isinstance(v,dict): return v.get(str(k))
    if isinstance(v,list):
        if isinstance(k, bool) or not isinstance(k, (int, float)) or int(k) != k:
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
    if op in ('=', '|=', '+=', '-=', '*=', '/=', '%=', '//='):
        paths = _paths(left, value, env)
        if op == '|=':
            result = value
            for path in reversed(paths):
                old = _get_path(result, path)
                outputs = list(_node(right, old, env))
                if outputs:
                    result = _set_path(result, path, outputs[0])
                else:
                    result = _delete_path(result, path)
            if paths: yield result
            return
        replacements = [None] if op == '|=' else list(_node(right, value, env))
        for replacement in replacements:
            result = value
            for path in paths:
                old = _get_path(result, path)
                new = replacement if op in ('=',) else (_one(right, old, env) if op == '|=' else replacement)
                if op not in ('=', '|='):
                    new = _arithmetic(op[0], old, replacement)
                result = _set_path(result, path, new)
            if paths: yield result
        return
    ls=list(_node(left,value,env)); rs=list(_node(right,value,env))
    for x in ls:
      for y in rs:
        if op=='+': yield y if x is None else x if y is None else x+y
        elif op=='-': yield x-y
        elif op=='*':
            if isinstance(x, str) and isinstance(y, (int,float)):
                count = max(0, int(y))
                if len(x) * count > 100000000:
                    raise RuntimeError('Repeat string result too long')
                yield x * count
            elif isinstance(y, str) and isinstance(x, (int,float)):
                count = max(0, int(x))
                if len(y) * count > 100000000:
                    raise RuntimeError('Repeat string result too long')
                yield y * count
            elif isinstance(x, dict) and isinstance(y, dict):
                yield _merge_objects(x, y)
            else: yield x*y
        elif op=='/':
            if y==0: raise RuntimeError(f"number ({_short(x)}) and number ({_short(y)}) cannot be divided because the divisor is zero")
            if isinstance(x,str) and isinstance(y,str): yield x.split(y)
            else: yield x/y
        elif op=='%':
            if y==0: raise RuntimeError(f"number ({_short(x)}) and number ({_short(y)}) cannot be divided (remainder) because the divisor is zero")
            yield math.fmod(x,y)
        elif op in ('==','!=','<','>','<=','>='):
            if op in ('==', '!='):
                equal = _deep_equal(x, y)
                yield equal if op == '==' else not equal
            else:
                yield {'<':x<y,'>':x>y,'<=':x<=y,'>=':x>=y}[op]
        elif op in ('and','or'): yield (_truth(x) and _truth(y)) if op=='and' else (_truth(x) or _truth(y))
        elif op=='//':
            emitted = False
            for item in ls:
                if _truth(item):
                    emitted = True
                    yield item
            if not emitted:
                yield from _node(right, value, env)
        else: yield x

def _arithmetic(op, left, right):
    if op == '+': return left + right
    if op == '-': return left - right
    if op == '*': return left * right
    if op == '/': return left / right
    if op == '%': return math.fmod(left, right)
    return right

def _merge_objects(left: dict, right: dict, depth: int = 0) -> dict:
    if depth > 1000: raise RuntimeError('Object merge too deep')
    merged = dict(left)
    for key, item in right.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(item, dict):
            merged[key] = _merge_objects(merged[key], item, depth + 1)
        else:
            merged[key] = item
    return merged


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
                if first.keys() != second.keys():
                    return False
                pending.extend((first[key], second[key], depth + 1) for key in first)
            continue
        if isinstance(first, float) and math.isnan(first) and math.isnan(second):
            continue
        if first != second:
            return False
    return True


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
                pieces.append('null')
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

def _paths(node, value, env):
    op, args = node.operation, node.arguments
    if op == 'identity': return [()]
    if op == 'field': return [(args[0],)]
    if op == 'index': return [p + (args[1],) for p in _paths(args[0], value, env)]
    if op == 'indexexpr':
        result = []
        for p in _paths(args[0], value, env):
            current = _get_path(value, p)
            for key in _node(args[1], value, env):
                if isinstance(current, list) and isinstance(key, (int, float)):
                    if int(key) < 0 and abs(int(key)) > len(current): raise RuntimeError('Out of bounds negative array index')
                elif isinstance(key, (int, float)) and key < 0 and current is None:
                    raise RuntimeError('Out of bounds negative array index')
                result.append(p + (key,))
        return result
    if op == 'iterate':
        result = []
        for p in _paths(args[0], value, env):
            current = _get_path(value, p)
            if isinstance(current, list): result.extend(p + (i,) for i in range(len(current)))
            elif isinstance(current, dict): result.extend(p + (k,) for k in current)
        return result
    if op == 'bind':
        return _paths(args[2], value, env)
    if op == 'call' and not args[1] and args[0] in env.get('__funcs__', {}):
        return _paths(env['__funcs__'][args[0]][1], value, env)
    return []

def _get_path(value, path):
    current = value
    for key in path:
        if isinstance(current, dict): current = current.get(str(key))
        elif isinstance(current, list):
            index = int(key); current = current[index] if -len(current) <= index < len(current) else None
        else: return None
    return current

def _set_path(value, path, replacement):
    if not path: return replacement
    if isinstance(value, dict):
        result = dict(value); key = str(path[0]); result[key] = _set_path(result.get(key), path[1:], replacement); return result
    if isinstance(value, list):
        result = list(value); index = int(path[0]); index = index + len(result) if index < 0 else index
        while index >= len(result): result.append(None)
        result[index] = _set_path(result[index], path[1:], replacement); return result
    if isinstance(path[0], (int, float)) and not isinstance(path[0], bool):
        result = []
        index = int(path[0])
        while len(result) <= index: result.append(None)
        result[index] = _set_path(result[index], path[1:], replacement)
        return result
    return {str(path[0]): _set_path(None, path[1:], replacement)}

def _delete_path(value, path):
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
def _call(name,args,value,env):
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
        params,body=function
        if not args:
            yield from _node(body,value,env); return
        # Function parameters are filters, not eagerly evaluated values.  A
        # parameter is evaluated against the function's current input each
        # time its name is used, which preserves jq's generator semantics.
        local=dict(env)
        local.update({param:('__closure__', arg, dict(env)) for param,arg in zip(params,args)})
        yield from _node(body,value,local); return
    if name == 'empty': return
    if name == 'error': raise RuntimeError(_one(args[0],value,env) if args else value)
    if name=='length': yield len(value); return
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
    if name=='not': yield not _truth(value); return
    if name == 'have_decnum': yield False; return
    if name in ('any', 'all'):
        values = list(_node(args[0], value, env)) if args else (list(value) if isinstance(value, list) else [])
        if len(args) > 1:
            values = [_one(args[1], item, env) for item in values]
        yield (any if name == 'any' else all)(_truth(item) for item in values)
        return
    if name == 'isempty':
        try:
            next(_node(args[0], value, env))
            yield False
        except StopIteration:
            yield True
        return
    if name in ('tostring','tojson'): yield _deep_json_dumps(value) if name=='tojson' else _stringify(value); return
    if name=='abs': yield abs(value); return
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
    if name == 'reverse':
        if isinstance(value, (list, str)): yield value[::-1]
        else: raise RuntimeError('cannot reverse value')
        return
    if name == 'flatten':
        depth = None if not args else int(_one(args[0], value, env))
        if depth is not None and depth < 0: raise RuntimeError('flatten depth must not be negative')
        if not isinstance(value, list): raise RuntimeError('flatten input must be an array')
        result=[]
        stack=[(value, depth)]
        while stack:
            items, remaining = stack.pop()
            for item in reversed(items):
                if isinstance(item, list) and (remaining is None or remaining > 0):
                    stack.append((item, None if remaining is None else remaining - 1))
                else:
                    result.append(item)
        result.reverse()
        yield result; return
    if name == 'contains':
        needle = _one(args[0], value, env)
        def contained(haystack, wanted):
            if isinstance(haystack, dict) and isinstance(wanted, dict):
                return all(k in haystack and contained(haystack[k], v) for k,v in wanted.items())
            if isinstance(haystack, list) and isinstance(wanted, list):
                return all(any(contained(item, candidate) for item in haystack) for candidate in wanted)
            if isinstance(haystack, str) and isinstance(wanted, str): return wanted in haystack
            return haystack == wanted
        yield contained(value, needle); return
    if name=='range':
        import itertools
        choices = [list(_node(arg, value, env)) for arg in args]
        for combo in itertools.product(*choices):
            if len(combo) == 1:
                start, end, step = 0, combo[0], 1
            else:
                start, end = combo[0], combo[1]
                step = combo[2] if len(combo) > 2 else 1
            yield from range(int(start), int(end), int(step))
        return
    if name == 'tonumber':
        if isinstance(value, (int, float)): yield value
        elif isinstance(value, str):
            try: yield json.loads(value)
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
        try: yield _deep_json_loads(value)
        except RuntimeError: raise
        except Exception: raise RuntimeError('invalid JSON')
        return
    if name == 'path':
        paths = _paths(args[0], value, env)
        if not paths:
            raise RuntimeError('Invalid path expression')
        for path in paths: yield list(path)
        return
    if name == 'paths':
        def paths_of(item, prefix=()):
            if isinstance(item, list):
                for i, child in enumerate(item):
                    p=prefix+(i,); yield list(p); yield from paths_of(child,p)
            elif isinstance(item, dict):
                for key, child in item.items():
                    p=prefix+(key,); yield list(p); yield from paths_of(child,p)
        if args:
            for item in _node(args[0], value, env): yield from paths_of(item)
        else: yield from paths_of(value)
        return
    if name == 'indices':
        needle = _one(args[0], value, env)
        if isinstance(value, str) and isinstance(needle, str):
            start=0
            while True:
                found=value.find(needle,start)
                if found < 0: break
                yield found; start=found+1
        elif isinstance(value, list) and isinstance(needle, list):
            for i in range(len(value)-len(needle)+1):
                if _deep_equal(value[i:i+len(needle)],needle): yield i
        elif isinstance(value, list):
            for i,item in enumerate(value):
                if _deep_equal(item,needle): yield i
        return
    if name in ('arrays','objects','iterables','booleans','numbers','strings','nulls','values','scalars','normals','finites'):
        ok = {'arrays':isinstance(value,list),'objects':isinstance(value,dict),
              'iterables':isinstance(value,(list,dict)),'booleans':isinstance(value,bool),
              'numbers':isinstance(value,(int,float)) and not isinstance(value,bool),
              'strings':isinstance(value,str),'nulls':value is None,
              'values':value is not None,'scalars':not isinstance(value,(list,dict))}[name]
        if ok: yield value
        return
    if name == 'keys':
        if isinstance(value, dict): yield sorted(value)
        elif isinstance(value, list): yield list(range(len(value)))
        else: raise RuntimeError('keys requires object or array')
        return
    if name == 'getpath':
        path = _one(args[0], value, env)
        if not isinstance(path, list): raise RuntimeError('Paths must be specified as an array')
        if len(path) > 10000: raise RuntimeError('Path too deep')
        yield _get_path(value, tuple(path)); return
    if name == 'setpath':
        path = _one(args[0], value, env); replacement = _one(args[1], value, env)
        if not isinstance(path, list): raise RuntimeError('Paths must be specified as an array')
        if len(path) > 10000: raise RuntimeError('Path too deep')
        yield _set_path(value, tuple(path), replacement); return
    if name == 'delpaths':
        paths = _one(args[0], value, env)
        if not isinstance(paths, list): raise RuntimeError('Paths must be specified as an array')
        result = value
        for path in paths:
            if isinstance(path, list): result = _delete_path(result, tuple(path))
        yield result; return
    if name == 'rindex':
        needle = _one(args[0], value, env)
        if isinstance(value, str): yield value.rfind(needle) if needle in value else None
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
    if name == 'isnan': yield isinstance(value, float) and math.isnan(value); return
    if name == 'pow': yield math.pow(_one(args[0],value,env), _one(args[1],value,env)); return
    if name == 'implode':
        if not isinstance(value, list): raise RuntimeError('implode input must be an array')
        yield ''.join(chr(int(x)) for x in value); return
    if name == 'explode':
        if not isinstance(value, str): raise RuntimeError('explode input must be a string')
        yield [ord(x) for x in value]; return
    if name == 'limit':
        count=int(_one(args[0], value, env))
        if count < 0: raise RuntimeError("limit doesn't support negative count")
        for item in _node(args[1], value, env):
            if count <= 0: break
            yield item; count -= 1
        return
    if name == 'skip':
        count=int(_one(args[0], value, env))
        if count < 0: raise RuntimeError("skip doesn't support negative count")
        for item in _node(args[1], value, env):
            if count: count -= 1
            else: yield item
        return
    if name == 'join':
        for separator in _node(args[0], value, env):
            if not isinstance(value, list): raise RuntimeError('cannot join value')
            yield str(separator).join('' if item is None else _stringify(item) for item in value)
        return
    if name in ('sin','cos','tan','asin','acos','atan','sqrt','log','log10','exp','exp2','log2'):
        yield getattr(math, name)(value); return
    if name in ('round','ceil','floor','fabs'):
        if name == 'round': yield math.floor(value + 0.5)
        else: yield getattr(math, name)(value)
        return
    if name == 'split':
        separator = _one(args[0], value, env); yield value.split(separator); return
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
        if not isinstance(value, str): raise RuntimeError(f'{name} input must be a string')
        yield value.strip() if name == 'trim' else value.lstrip() if name == 'ltrim' else value.rstrip(); return
    if name == 'startswith':
        yield value.startswith(_one(args[0], value, env)); return
    if name == 'endswith':
        yield value.endswith(_one(args[0], value, env)); return
    if name in ('sort', 'unique'):
        if not isinstance(value, list):
            raise RuntimeError('cannot sort value')
        ordered = sorted(value, key=_jq_sort_key)
        if name == 'unique':
            ordered = _dedupe_sorted(ordered)
        yield ordered
        return
    raise RuntimeError(f"unknown function {name}")


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
        if not result or value != result[-1]:
            result.append(value)
    return result
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
    if isinstance(value, float) and value.is_integer():
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

def _stringify(value: object) -> str:
    import json
    return value if isinstance(value, str) else json.dumps(value, separators=(",", ":"), ensure_ascii=False, allow_nan=False)

def _apply_format(name: str, value: object, template: bool = False) -> str:
    import base64, html, json, urllib.parse
    if name == "text": return _stringify(value)
    if name == "json": return json.dumps(value, separators=(",", ":"), ensure_ascii=False)
    if name == "html": return html.escape(_stringify(value), quote=True).replace("&#x27;", "&apos;")
    if name == "uri": return urllib.parse.quote(_stringify(value), safe="-_.~")
    if name == "urid": return urllib.parse.unquote(_stringify(value))
    if name == "base64": return base64.b64encode(_stringify(value).encode()).decode()
    if name == "base64d": return base64.b64decode(_stringify(value)).decode()
    if name == "csv": return ",".join('"' + str(x).replace('"', '""') + '"' if isinstance(x, str) else _stringify(x) for x in value)
    if name == "tsv": return "\t".join(_stringify(x).replace("\\", "\\\\").replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t") for x in value)
    if name == "sh": return "'" + _stringify(value).replace("'", "'\\''") + "'"
    raise RuntimeError(f"unknown format @{name}")
