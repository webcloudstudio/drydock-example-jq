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
            raise RuntimeError("cannot iterate over value")
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
        if isinstance(bound, Node):
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
    elif op == "index":
        for base in _node(a[0],value,env): yield _index(base,a[1])
    elif op == "iterate":
        for base in _node(a[0],value,env):
            if isinstance(base,dict): yield from base.values()
            elif isinstance(base,list): yield from base
            else: raise RuntimeError("cannot iterate over value")
    elif op in ("indexexpr","slice"):
        for base in _node(a[0],value,env):
            if op=="slice":
                start=_one(a[1],base,env); end=None if a[2] is None else _one(a[2],base,env); yield base[int(start) if start is not None else 0:int(end) if end is not None else None]
            else: yield _index(base,_one(a[1],base,env))
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
        x=_one(a[1],value,env); yield -x
    elif op == "optional":
        try: yield from _node(a[0],value,env)
        except (RuntimeError, ValueError, TypeError, IndexError): return
    elif op == "if":
        branch=a[1] if _truth(_one(a[0],value,env)) else a[2]; yield from _node(branch,value,env)
    elif op == "try":
        try: yield from _node(a[0],value,env)
        except RuntimeError as error:
            if a[1] is not None: yield from _node(a[1],str(error),env)
    elif op == "label":
        try: yield from _node(a[1], value, {**env, '__label__': a[0]})
        except _Break as exc:
            if exc.name != a[0]: raise
    elif op == "break":
        raise _Break(a[0])
    elif op in ("reduce", "foreach"):
        states=list(_node(a[0], value, env)); initial=list(_node(a[2], value, env))
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
        env.setdefault('__funcs__',{})[a[0]]=(a[1],a[2])
        yield value
    elif op == "defprog":
        funcs=dict(env.get('__funcs__',{}))
        program: Node = node
        while program.operation == 'defprog':
            definition = program.arguments[0]
            funcs[definition.arguments[0]] = (definition.arguments[1], definition.arguments[2])
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
    elif op=='pattern_array':
        if not isinstance(value,list): return False
        for i,p in enumerate(args[0]):
            if not _bind_pattern(p, value[i] if i<len(value) else None, env): return False
        return True
    elif op=='pattern_object':
        if not isinstance(value,dict): return False
        for key,p in args[0]:
            if not _bind_pattern(p, value.get(key), env): return False
        return True
    return False

def _one(node, value, env):
    vals=list(_node(node,value,env)); return vals[0] if vals else None
def _truth(x): return x is not None and x is not False
def _index(v,k):
    if isinstance(v,dict): return v.get(str(k))
    if isinstance(v,list):
        if isinstance(k, bool) or not isinstance(k, (int, float)) or int(k) != k:
            raise RuntimeError("cannot index array with string")
        index = int(k)
        return v[index] if -len(v) <= index < len(v) else None
    if isinstance(v,str):
        if isinstance(k, bool) or not isinstance(k, (int, float)) or int(k) != k:
            raise RuntimeError("cannot index string with number")
        index = int(k)
        return v[index] if -len(v) <= index < len(v) else None
    raise RuntimeError("cannot index value")
def _binary(op,left,right,value,env):
    if op==',': yield from _node(left,value,env); yield from _node(right,value,env); return
    if op=='|':
        for x in _node(left,value,env): yield from _node(right,x,env)
        return
    if op in ('=', '|=', '+=', '-=', '*=', '/=', '%=', '//='):
        paths = _paths(left, value, env)
        replacements = [value] if op == '|=' else list(_node(right, value, env))
        for replacement in replacements:
            result = value
            for path in paths:
                old = _get_path(result, path)
                new = replacement if op == '=' else _one(right, old, env)
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
        elif op in ('==','!=','<','>','<=','>='): yield {'==':x==y,'!=':x!=y,'<':x<y,'>':x>y,'<=':x<=y,'>=':x>=y}[op]
        elif op in ('and','or'): yield (_truth(x) and _truth(y)) if op=='and' else (_truth(x) or _truth(y))
        elif op=='//': yield x if _truth(x) else y
        else: yield x

def _arithmetic(op, left, right):
    if op == '+': return left + right
    if op == '-': return left - right
    if op == '*': return left * right
    if op == '/': return left / right
    if op == '%': return math.fmod(left, right)
    return right

def _merge_objects(left: dict, right: dict) -> dict:
    merged = dict(left)
    for key, item in right.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(item, dict):
            merged[key] = _merge_objects(merged[key], item)
        else:
            merged[key] = item
    return merged

def _paths(node, value, env):
    op, args = node.operation, node.arguments
    if op == 'identity': return [()]
    if op == 'field': return [(args[0],)]
    if op == 'index': return [p + (args[1],) for p in _paths(args[0], value, env)]
    if op == 'indexexpr':
        return [p + (key,) for p in _paths(args[0], value, env) for key in _node(args[1], value, env)]
    if op == 'iterate':
        result = []
        for p in _paths(args[0], value, env):
            current = _get_path(value, p)
            if isinstance(current, list): result.extend(p + (i,) for i in range(len(current)))
            elif isinstance(current, dict): result.extend(p + (k,) for k in current)
        return result
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
    return {str(path[0]): _set_path(None, path[1:], replacement)}
def _call(name,args,value,env):
    if not args and name in env:
        bound = env[name]
        if isinstance(bound, Node):
            yield from _node(bound, value, env)
        else:
            yield bound
        return
    if name in env.get('__funcs__',{}):
        params,body=env['__funcs__'][name]
        if not args:
            yield from _node(body,value,env); return
        # Function parameters are filters, not eagerly evaluated values.  A
        # parameter is evaluated against the function's current input each
        # time its name is used, which preserves jq's generator semantics.
        local=dict(env)
        local.update({param:arg for param,arg in zip(params,args)})
        yield from _node(body,value,local); return
    if name == 'empty': return
    if name == 'error': raise RuntimeError(_one(args[0],value,env) if args else 'error')
    if name=='length': yield len(value); return
    if name == 'add':
        items = list(value)
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
    if name == 'isempty':
        try:
            next(_node(args[0], value, env))
            yield False
        except StopIteration:
            yield True
        return
    if name in ('tostring','tojson'): yield json.dumps(value,separators=(',',':')) if name=='tojson' else _stringify(value); return
    if name=='abs': yield abs(value); return
    if name=='floor': yield math.floor(value); return
    if name=='ceil': yield math.ceil(value); return
    if name=='map':
        result=[]
        for x in value:
            result.extend(_node(args[0], x, env))
        yield result; return
    if name=='range':
        if len(args) == 1:
            start, end, step = 0, _one(args[0], value, env), 1
        else:
            start=_one(args[0],value,env); end=_one(args[1],value,env) if len(args)>1 else start; step=_one(args[2],value,env) if len(args)>2 else 1
        yield from range(int(start),int(end),int(step)); return
    if name == 'tonumber':
        if isinstance(value, (int, float)): yield value
        elif isinstance(value, str):
            try: yield json.loads(value)
            except Exception: raise RuntimeError(f'string ({json.dumps(value)}) cannot be parsed as a number')
        else: raise RuntimeError('cannot parse number')
        return
    if name == 'fromjson':
        if not isinstance(value, str): raise RuntimeError('only strings can be parsed')
        try: yield json.loads(value, parse_constant=lambda x: float('nan'))
        except Exception: raise RuntimeError('invalid JSON')
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
        yield getattr(math, name)(value); return
    if name == 'split':
        separator = _one(args[0], value, env); yield value.split(separator); return
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


def _jq_sort_key(value: object) -> tuple[object, ...]:
    """Return jq's basic total-order key for values used by sort/unique."""
    if value is None: return (0,)
    if isinstance(value, bool): return (1, int(value))
    if isinstance(value, (int, float)): return (2, value)
    if isinstance(value, str): return (3, value)
    if isinstance(value, list): return (4, tuple(_jq_sort_key(item) for item in value))
    if isinstance(value, dict):
        return (5, tuple((key, _jq_sort_key(item)) for key, item in sorted(value.items())))
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
