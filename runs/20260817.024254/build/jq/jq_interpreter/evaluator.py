"""Ordered, generator-based jq evaluation."""
from __future__ import annotations
import base64, json, math, re, urllib.parse, copy
from decimal import Decimal
from collections.abc import Iterator
from .data_model import JsonValue, is_truthy, serialize_compact
from .diagnostics import RuntimeJqError
from .parser import Filter

class BreakSignal(Exception):
    pass

def _walk(v):
    yield v
    if isinstance(v,dict):
        for x in v.values(): yield from _walk(x)
    elif isinstance(v,list):
        for x in v: yield from _walk(x)

def _num(x):
    if isinstance(x,bool) or not isinstance(x,(int,float)): raise RuntimeJqError('number required')
    return x

def _jq_type_name(value: object) -> str:
    """Return jq's public type name rather than Python's implementation name."""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, (int, float)):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    return type(value).__name__

def _arith(x):
    return float(x)

def _freeze(value):
    if isinstance(value, dict):
        return ("object", tuple(sorted((key, _freeze(item)) for key, item in value.items())))
    if isinstance(value, list):
        return ("array", tuple(_freeze(item) for item in value))
    if isinstance(value, float) and math.isnan(value): return ("number", "nan")
    if isinstance(value, (int, float)) and not isinstance(value, bool): return ("number", float(value))
    return (type(value).__name__, value)

def _jq_compare(a, b, depth=0):
    if depth > 10000: raise RuntimeJqError("Comparison too deep")
    if a is None and b is None: return 0
    if isinstance(a, (int, float)) and not isinstance(a, bool) and isinstance(b, (int, float)) and not isinstance(b, bool):
        return (float(a) > float(b)) - (float(a) < float(b))
    rank = {type(None): 0, bool: 1, int: 2, float: 2, str: 3, list: 4, dict: 5}
    ka, kb = rank.get(type(a), 6), rank.get(type(b), 6)
    if ka != kb: return (ka > kb) - (ka < kb)
    if isinstance(a, dict):
        keys_a, keys_b = sorted(a), sorted(b)
        c = _jq_compare(keys_a, keys_b, depth + 1)
        if c: return c
        for key in keys_a:
            c = _jq_compare(a[key], b[key], depth + 1)
            if c: return c
        return 0
    if isinstance(a, list):
        for left, right in zip(a, b):
            c = _jq_compare(left, right, depth + 1)
            if c: return c
        return (len(a) > len(b)) - (len(a) < len(b))
    return (a > b) - (a < b)

def _merge_objects(left, right, depth=0):
    if depth > 10000: raise RuntimeJqError("Object merge too deep")
    merged = dict(left)
    for key, value in right.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = _merge_objects(merged[key], value, depth + 1)
        else:
            merged[key] = value
    return merged

def _call(name,args,inp,env):
    functions = env.get("__funcs__", {})
    function = functions.get((name, len(args)))
    if function is not None:
        params, body, captured_env, captured_funcs = function
        choices: list[list[tuple[str, object]]] = []
        for (kind, param), argument in zip(params, args):
            if kind == "filter": choices.append([("@" + param, ("filter", argument, env))])
            else:
                values = list(ev(argument, inp, env)) or [None]
                choices.append([("@" + param, value) for value in values])
        def invoke(index: int, local: dict[str, object]) -> Iterator[JsonValue]:
            if index == len(choices):
                yield from ev(body, inp, local)
                return
            for key, value in choices[index]:
                next_local = dict(local); next_local[key] = value
                yield from invoke(index + 1, next_local)
        base = dict(captured_env); base["__funcs__"] = captured_funcs
        yield from invoke(0, base)
        return
    # These forms consume generator arguments themselves.  Evaluating their
    # arguments through the ordinary cartesian-product path would repeat the
    # predicate once per source value and would lose empty-array semantics.
    if name in ('any', 'all') and len(args) == 1:
        if isinstance(inp, list):
            candidates = inp
        else:
            candidates = []
        outcomes = []
        for candidate in candidates:
            outcomes.extend(is_truthy(value) for value in ev(args[0], candidate, env))
            if name == 'any' and any(outcomes):
                break
            if name == 'all' and any(not value for value in outcomes):
                break
        yield any(outcomes) if name == 'any' else all(outcomes)
        return
    if name in ('any', 'all') and len(args) == 2:
        outcomes = []
        for candidate in ev(args[0], inp, env):
            outcomes.extend(is_truthy(value) for value in ev(args[1], candidate, env))
            if name == 'any' and any(outcomes):
                break
            if name == 'all' and any(not value for value in outcomes):
                break
        yield any(outcomes) if name == 'any' else all(outcomes)
        return
    if name == 'IN' and len(args) == 1:
        yield any(value == inp for value in ev(args[0], inp, env))
        return
    if name == 'IN' and len(args) == 2:
        yield any(left == right for left in ev(args[0], inp, env) for right in ev(args[1], inp, env))
        return
    if name == 'walk' and args:
        def visit(value):
            if isinstance(value, list):
                rebuilt = [[]]
                for item in value:
                    choices = visit(item)
                    rebuilt = [prefix + [choice] for prefix in rebuilt for choice in choices]
                value_choices = rebuilt
            elif isinstance(value, dict):
                value_choices = [{}]
                for key, item in value.items():
                    choices = visit(item)
                    value_choices = [dict(prefix, **{key: choice}) for prefix in value_choices for choice in choices] or value_choices
            else:
                value_choices = [value]
            return [result for candidate in value_choices for result in ev(args[0], candidate, env)]
        yield from visit(inp)
        return
    if name=='map' and args:
        yield [z for x in inp for z in ev(args[0],x,env)]
        return
    if name=='map_values' and args:
        yield [next(ev(args[0],x,env),None) for x in inp] if isinstance(inp,list) else next(ev(args[0],inp,env))
        return
    if name == 'isempty' and args:
        try: yield not any(True for _ in ev(args[0], inp, env))
        except RuntimeJqError: yield False
        return
    if name == 'first' and args:
        stream = ev(args[0], inp, env)
        try: yield next(stream)
        except StopIteration: pass
        return
    if name == 'del' and args:
        result = copy.deepcopy(inp)
        paths = _paths(args[0], inp, env)
        if not paths:
            yield inp
            return
        for path in sorted(paths, key=lambda item: (len(item), item), reverse=True):
            if not path: result = None
            else: _delete_path(result, path)
        yield result
        return
    if name == 'add' and args:
        generated = [value for argument in args for value in ev(argument, inp, env)]
        if not generated:
            yield None
        elif all(isinstance(value, (int, float)) and not isinstance(value, bool) for value in generated):
            yield sum(generated)
        elif all(isinstance(value, str) for value in generated):
            yield ''.join(generated)
        elif all(isinstance(value, list) for value in generated):
            yield [item for value in generated for item in value]
        else:
            result = generated[0]
            for value in generated[1:]: result = _binary('+', result, value)
            yield result
        return
    vals=[list(ev(a,inp,env)) for a in args]
    # Arguments are filters.  Each argument can be a generator, so ordinary
    # functions receive the cartesian product in source order.
    products = [[]]
    for choices in vals:
        products = [prefix + [choice] for prefix in products for choice in choices]
    if not products and args:
        return
    if not args:
        products = [[]]
    def one(i=0): return products[0][i] if products and products[0] else inp
    for selected in products:
        if selected:
            yield from _call_once(name, args, inp, env, selected)
        else:
            yield from _call_once(name, args, inp, env, selected)

def _call_once(name,args,inp,env,selected):
    def one(i=0): return selected[i] if i < len(selected) else inp
    if name=='range':
        a=_num(one()); b=_num(selected[1]) if len(selected)>1 else a; step=_num(selected[2]) if len(selected)>2 else 1
        if len(selected)==1: a,b=0,a
        if step==0: raise RuntimeJqError('range step cannot be zero')
        x=a
        while (step>0 and x<b) or (step<0 and x>b): yield x; x+=step
    elif name in ('length','utf8bytelength'):
        yield len(one()) if not isinstance(one(),(int,float)) else abs(one())
    elif name=='type': yield 'null' if one() is None else ('boolean' if isinstance(one(),bool) else 'number' if isinstance(one(),(int,float)) else 'string' if isinstance(one(),str) else 'array' if isinstance(one(),list) else 'object')
    elif name=='keys': yield list(range(len(one()))) if isinstance(one(),list) else sorted(one().keys())
    elif name=='values':
        if one() is not None: yield one()
    elif name in ('tonumber','tostring','tojson','fromjson'):
        x=one()
        if name=='tonumber':
            try:
                yield float(x) if '.' in str(x) else int(x)
            except (TypeError, ValueError, OverflowError) as exc:
                raise RuntimeJqError(f'cannot parse number: {x}') from exc
        elif name=='tostring': yield x if isinstance(x,str) else serialize_compact(x)
        elif name=='tojson': yield serialize_compact(x)
        else:
            from .data_model import parse_json_text
            try:
                yield parse_json_text(x)
            except (ValueError, json.JSONDecodeError) as exc:
                raise RuntimeJqError(str(exc)) from exc
    elif name in ('add','any','all','flatten','sort','unique','reverse','min','max'):
        x=one()
        if name=='add': yield sum(x) if x and all(isinstance(a,(int,float)) for a in x) else ''.join(x)
        elif name in ('any', 'all') and len(args) == 2:
            source, condition = args
            outcomes = []
            for candidate in ev(source, inp, env):
                outcomes.extend(is_truthy(v) for v in ev(condition, candidate, env))
                if name == 'any' and any(outcomes): break
                if name == 'all' and any(not v for v in outcomes): break
            yield any(outcomes) if name == 'any' else all(outcomes)
        elif name in ('any', 'all') and len(args) == 1:
            outcomes = [is_truthy(v) for candidate in x for v in ev(args[0], candidate, env)]
            yield any(outcomes) if name == 'any' else all(outcomes)
        elif name=='any': yield any(is_truthy(a) for a in x)
        elif name=='all': yield all(is_truthy(a) for a in x)
        elif name=='flatten':
            def flat(a):
                pending = list(reversed(a))
                while pending:
                    item = pending.pop()
                    if isinstance(item, list):
                        pending.extend(reversed(item))
                    else:
                        yield item
            yield list(flat(x))
        elif name in ('sort','unique'):
            from functools import cmp_to_key
            ordered = sorted(x, key=cmp_to_key(_jq_compare))
            if name == 'sort':
                yield ordered
            else:
                seen, unique = set(), []
                for item in ordered:
                    marker = _freeze(item)
                    if marker not in seen:
                        seen.add(marker); unique.append(item)
                yield unique
        elif name=='reverse': yield x[::-1]
        else: yield (min if name=='min' else max)(x)
    elif name=='contains': yield _contains(inp, selected[0])
    elif name == 'pow': yield math.pow(_num(selected[0]), _num(selected[1]))
    elif name == 'log2': yield math.log2(_num(inp))
    elif name == 'round': yield round(_num(inp))
    elif name=='getpath':
        # Each argument is one path.  A single path such as ["a", 0]
        # must not be mistaken for a stream of two paths.
        for path in selected:
            if len(path) > 10000:
                raise RuntimeJqError('Path too deep')
            current = inp
            try:
                for part in path:
                    if isinstance(current, list):
                        if not isinstance(part, int):
                            raise TypeError
                        current = current[part]
                    elif isinstance(current, dict):
                        if not isinstance(part, str):
                            raise TypeError
                        current = current[part]
                    else:
                        raise TypeError
            except (KeyError, IndexError, TypeError):
                current = None
            yield current
    elif name == 'setpath':
        path = selected[0] if selected else []
        replacement = selected[1] if len(selected) > 1 else None
        if not isinstance(path, list):
            raise RuntimeJqError('Path must be specified as an array')
        if len(path) > 10000:
            raise RuntimeJqError('Path too deep')
        result = copy.deepcopy(inp)
        result = _set_path_create(result, path, replacement)
        yield result
    elif name == 'delpaths':
        paths = selected[0] if selected else []
        if not isinstance(paths, list):
            raise RuntimeJqError('Paths must be specified as an array')
        result = copy.deepcopy(inp)
        for path in paths:
            if not isinstance(path, list):
                raise RuntimeJqError('Path must be specified as an array')
            if len(path) > 10000:
                raise RuntimeJqError('Path too deep')
            _delete_path(result, path)
        yield result
    elif name=='startswith': yield inp.startswith(selected[0])
    elif name=='endswith': yield inp.endswith(selected[0])
    elif name=='floor': yield math.floor(_num(one()))
    elif name=='ceil': yield math.ceil(_num(one()))
    elif name=='abs': yield abs(_num(one()))
    elif name=='sqrt': yield math.sqrt(_num(inp))
    elif name=='not': yield not is_truthy(inp)
    elif name in ('arrays','objects','iterables','scalars','booleans','nulls','strings','numbers'):
        ok={'arrays':isinstance(inp,list),'objects':isinstance(inp,dict),'iterables':isinstance(inp,(list,dict)),'scalars':not isinstance(inp,(list,dict)),'booleans':isinstance(inp,bool),'nulls':inp is None,'strings':isinstance(inp,str),'numbers':isinstance(inp,(int,float)) and not isinstance(inp,bool)}[name]
        if ok: yield inp
    elif name=='join': yield (selected[0] if selected else '').join('' if x is None else str(x).lower() if isinstance(x,bool) else str(x) for x in inp)
    elif name=='split': yield one().split(selected[1] if len(selected)>1 else None)
    elif name in ('ltrimstr','rtrimstr','trimstr'):
        q=one(); x=inp
        if name=='ltrimstr': yield x[len(q):] if x.startswith(q) else x
        elif name=='rtrimstr': yield x[:-len(q)] if q and x.endswith(q) else x
        else: yield x[len(q):] if x.startswith(q) else x[:-len(q)] if q and x.endswith(q) else x
    elif name=='range': return
    elif name=='error': raise RuntimeJqError(str(one()) if args else str(inp))
    elif name == 'have_decnum': yield False
    elif name == 'has':
        key = one()
        if isinstance(inp, dict) and isinstance(key, str): yield key in inp
        elif isinstance(inp, list) and isinstance(key, int) and not isinstance(key, bool): yield 0 <= key < len(inp)
        else: yield False
    elif name == 'first':
        stream = ev(args[0], inp, env) if args else (iter(inp) if isinstance(inp, list) else iter(()))
        try: yield next(stream)
        except StopIteration: return
    elif name == 'last':
        stream = ev(args[0], inp, env) if args else (iter(inp) if isinstance(inp, list) else iter(()))
        values = list(stream)
        if values: yield values[-1]
    elif name == 'nth':
        index = int(selected[0]) if selected else 0
        stream = ev(args[1], inp, env) if len(args) > 1 else (iter(inp) if isinstance(inp, list) else iter(()))
        for position, value in enumerate(stream):
            if position == index: yield value; break
    elif name == 'select':
        if is_truthy(selected[0] if selected else inp): yield inp
    elif name == 'isempty':
        yield not list(ev(args[0], inp, env))
    elif name == 'del':
        result = copy.deepcopy(inp)
        paths = _paths(args[0], inp, env)
        if not paths: yield inp; return
        for path in sorted(paths, key=lambda item: (len(item), item), reverse=True):
            if not path: result = None
            else: _delete_path(result, path)
        yield result
    elif name in ('in','inside'): yield False
    else: raise RuntimeJqError('unknown function '+name)

def _contains(a,b,depth=0):
    pending: list[tuple[object, object, int]] = [(a, b, depth)]
    while pending:
        left, right, level = pending.pop()
        if level > 10000:
            raise RuntimeJqError("Containment check too deep")
        if isinstance(left, str) and isinstance(right, str):
            if right not in left:
                return False
        elif isinstance(left, list) and isinstance(right, list):
            for wanted in right:
                if len(left) == 1:
                    pending.append((left[0], wanted, level + 1))
                elif not any(_contains(candidate, wanted, level + 1) for candidate in left):
                    return False
        elif isinstance(left, dict) and isinstance(right, dict):
            for key, wanted in right.items():
                if key not in left:
                    return False
                pending.append((left[key], wanted, level + 1))
        elif left != right:
            return False
    return True

def ev(f:Filter, inp:JsonValue, env:dict[str,JsonValue]|None=None)->Iterator[JsonValue]:
    env={} if env is None else env
    if "__funcs__" not in env:
        env = dict(env); env["__funcs__"] = {}
    k=f.kind
    if k=='identity': yield inp
    elif k=='literal': yield f.value
    elif k=='template':
        pieces = []
        for kind, value in f.value:
            if kind == 'text': pieces.append(value)
            else:
                from .parser import parse
                pieces.extend(str(x) if not isinstance(x, str) else x for x in ev(parse(value), inp, env))
        yield ''.join(pieces)
    elif k=='empty': return
    elif k=='error': raise RuntimeJqError(str(inp))
    elif k == 'binding':
        if f.value not in env: raise RuntimeJqError(f"no such variable: ${f.value}")
        yield env[f.value]
    elif k == 'param':
        value = env.get(f.value)
        if isinstance(value, tuple) and value and value[0] == "filter":
            yield from ev(value[1], inp, value[2])
        else:
            yield value
    elif k=='comma':
        for c in f.children: yield from ev(c,inp,env)
    elif k=='field':
        for x in ev(f.children[0],inp,env):
            if isinstance(x,dict): yield x.get(f.value)
            else: raise RuntimeJqError(f'Cannot index {_jq_type_name(x)} with string ("{f.value}")')
    elif k=='iterate':
        for x in ev(f.value[0],inp,env):
            if isinstance(x,(list,dict)): yield from (x if isinstance(x,list) else x.values())
            else: raise RuntimeJqError('cannot iterate')
    elif k in ('index','slice'):
        base,a,b=f.value
        for x in ev(base,inp,env):
            for ix in ev(a, x, env):
                if k=='index':
                    try: yield x[ix]
                    except (KeyError, IndexError, TypeError): raise RuntimeJqError('cannot index')
                else:
                    lo=ix; hi=None if b is None else next(ev(b,x,env),None); yield x[lo:hi]
    elif k=='array': yield [z for c in f.children for z in ev(c,inp,env)]
    elif k=='object':
        partials = [{}]
        for key_filter, value_filter in f.value:
            keys = list(ev(key_filter, inp, env))
            values = list(ev(value_filter, inp, env)) or [None]
            partials = [dict(existing, **{str(key): value})
                        for existing in partials for key in keys for value in values]
        yield from partials
    elif k == 'optional':
        try: yield from ev(f.children[0], inp, env)
        except RuntimeJqError: return
    elif k == 'try':
        try:
            yield from ev(f.children[0], inp, env)
        except RuntimeJqError as error:
            if f.children[1].kind != 'empty':
                yield from ev(f.children[1], str(error), env)
    elif k == 'label':
        try:
            yield from ev(f.children[0], inp, env)
        except BreakSignal:
            return
    elif k == 'break':
        raise BreakSignal()
    elif k == 'if':
        cond, yes, no = f.children
        for value in ev(cond, inp, env):
            yield from ev(yes if is_truthy(value) else no, inp, env)
    elif k == 'as':
        source, pattern, body = f.children
        for value in ev(source, inp, env):
            local = dict(env)
            if pattern.kind == "pattern_alt":
                last_error = None
                all_names = set().union(*(_pattern_names(candidate) for candidate in pattern.children))
                for candidate in pattern.children:
                    attempt = dict(env)
                    for variable in all_names:
                        attempt[variable] = None
                    try:
                        _bind(candidate, value, attempt)
                        yield from ev(body, inp, attempt)
                        last_error = None
                        break
                    except RuntimeJqError as exc:
                        last_error = exc
                if last_error is not None:
                    raise last_error
            else:
                _bind(pattern, value, local)
                yield from ev(body, inp, local)
    elif k == 'def':
        (name, params), (body, continuation) = f.value, f.children
        functions = dict(env.get("__funcs__", {}))
        captured = dict(env)
        captured["__funcs__"] = functions
        functions[(name, len(params))] = (params, body, captured, functions)
        local = dict(env); local["__funcs__"] = functions
        yield from ev(continuation, inp, local)
    elif k in ('reduce', 'foreach'):
        source, pattern, init, update, extract = f.value
        for initial in ev(init, inp, env):
            accumulators = [initial]
            for item in ev(source, inp, env):
                next_accumulators = []
                for accumulator in accumulators:
                    local = dict(env)
                    _bind(pattern, item, local)
                    for updated in ev(update, accumulator, local):
                        if k == 'foreach': yield from ev(extract, updated, local)
                        next_accumulators.append(updated)
                accumulators = next_accumulators
            if k == 'reduce': yield from accumulators
    elif k=='unary':
        for x in ev(f.children[0],inp,env): yield -_arith(_num(x))
    elif k=='call': yield from _call(str(f.value),f.children,inp,env)
    elif k=='binary':
        op=f.value; l,r=f.children
        if op=='|':
            for x in ev(l,inp,env): yield from ev(r,x,env)
        elif op==',': yield from ev(l,inp,env); yield from ev(r,inp,env)
        elif op == '//':
            produced = False
            for value in ev(l, inp, env):
                if is_truthy(value):
                    produced = True
                    yield value
            if not produced:
                yield from ev(r, inp, env)
        elif op in ('=', '|=', '+=', '-=', '*=', '/=', '%=', '//='):
            yield from _update(l, r, op, inp, env)
        else:
            # jq's generator cartesian product advances the right-hand
            # generator first.  This matters for reducers/foreach, where the
            # product order becomes observable accumulator order.
            right_values = list(ev(r, inp, env))
            left_values = list(ev(l, inp, env))
            for b in right_values:
                for a in left_values:
                    yield _binary(op, a, b)
    elif k=='recurse': yield from _walk(inp)
    else: raise RuntimeJqError('unsupported filter')

def _binary(op,a,b):
    if op=='//': return a if is_truthy(a) else b
    if op == 'and': return is_truthy(a) and is_truthy(b)
    if op == 'or': return is_truthy(a) or is_truthy(b)
    if op in ('==','!=','<','>','<=','>='):
        try:
            equal = _jq_compare(a, b) == 0
        except RuntimeJqError:
            if op in ('==', '!='): raise RuntimeJqError("Equality check too deep")
            raise
        if op == '==': return equal
        if op == '!=': return not equal
        comparison = _jq_compare(a, b)
        return {'<': comparison < 0, '>': comparison > 0,
                '<=': comparison <= 0, '>=': comparison >= 0}[op]
    if op=='+':
        if isinstance(a,dict) and isinstance(b,dict): return {**a,**b}
        if isinstance(a,list) and isinstance(b,list): return a+b
        if a is None: return b
        if b is None: return a
        if isinstance(a,(int,float)) and not isinstance(a,bool) and isinstance(b,(int,float)) and not isinstance(b,bool): return _arith(a) + _arith(b)
        if isinstance(a,str) and isinstance(b,str): return a+b
        raise RuntimeJqError(f'{_value_description(a)} and {_value_description(b)} cannot be added')
    if op=='-':
        if isinstance(a,(int,float)) and not isinstance(a,bool) and isinstance(b,(int,float)) and not isinstance(b,bool): return _arith(a) - _arith(b)
        if isinstance(a,list) and isinstance(b,list): return [x for x in a if x not in b]
        raise RuntimeJqError(f'{_value_description(a)} and {_value_description(b)} cannot be subtracted')
    if op=='*':
        if isinstance(a, dict) and isinstance(b, dict): return _merge_objects(a, b)
        if isinstance(a,(int,float)) and not isinstance(a,bool) and isinstance(b,(int,float)) and not isinstance(b,bool): return _arith(a)*_arith(b)
        if isinstance(a,str) and isinstance(b,(int,float)) and not isinstance(b,bool): return a * max(0, int(b))
        raise RuntimeJqError('cannot multiply values')
    if op=='/':
        if isinstance(a,str) and isinstance(b,str): return a.split(b)
        if isinstance(a,(int,float)) and not isinstance(a,bool) and isinstance(b,(int,float)) and not isinstance(b,bool):
            if b == 0: raise RuntimeJqError('division by zero')
            return _arith(a)/_arith(b)
        raise RuntimeJqError('cannot divide values')
    if op=='%':
        if not (isinstance(a,(int,float)) and not isinstance(a,bool) and isinstance(b,(int,float)) and not isinstance(b,bool)):
            raise RuntimeJqError('cannot take remainder')
        if b == 0: raise RuntimeJqError('division by zero')
        return math.fmod(_arith(a), _arith(b))
    raise RuntimeJqError('unsupported operator')


def _value_description(value: object) -> str:
    kind = _jq_type_name(value)
    if kind == 'string':
        rendered = json.dumps(value, ensure_ascii=False, separators=(',', ':'))
    elif kind == 'number' and isinstance(value, int) and abs(value) >= 10**20:
        rendered = format(Decimal(repr(float(value))), 'f')
        rendered = rendered[:26] + '...' if len(rendered) > 26 else rendered
    else:
        rendered = serialize_compact(value) if value is not None else 'null'
    return f'{kind} ({rendered})'


def _bind(pattern: Filter, value: JsonValue, env: dict[str, JsonValue]) -> None:
    if pattern.kind == 'pattern':
        env[str(pattern.value)] = value
    elif pattern.kind == 'array_pattern':
        if not isinstance(value, list): raise RuntimeJqError('cannot destructure')
        for index, child in enumerate(pattern.children):
            _bind(child, value[index] if index < len(value) else None, env)
    elif pattern.kind == 'object_pattern':
        if not isinstance(value, dict): raise RuntimeJqError('cannot destructure')
        for key, child in pattern.value:
            _bind(child, value.get(key), env)
    elif pattern.kind == 'pattern_alt':
        _bind(pattern.children[0], value, env)


def _pattern_names(pattern: Filter) -> set[str]:
    if pattern.kind == "pattern":
        return {str(pattern.value)}
    if pattern.kind == "array_pattern":
        result: set[str] = set()
        for child in pattern.children:
            result.update(_pattern_names(child))
        return result
    if pattern.kind == "object_pattern":
        result = set()
        for _, child in pattern.value:
            result.update(_pattern_names(child))
        return result
    return set()


def _update(path: Filter, rhs: Filter, op: str, root: JsonValue,
            env: dict[str, JsonValue]) -> Iterator[JsonValue]:
    """Apply basic jq path updates while retaining RHS generator values."""
    if path.kind == "param":
        callback = env.get(path.value)
        if isinstance(callback, tuple) and callback[0] == "filter":
            yield from _update(callback[1], rhs, op, root, callback[2])
            return
    if path.kind == "call":
        function = env.get("__funcs__", {}).get((str(path.value), 0))
        if function is not None:
            values = list(ev(function[1], root, function[2]))
            locations = _paths(function[1], root, function[2])
            if locations:
                path = function[1]
            else:
                displayed = values[0] if len(values) == 1 else values
                raise RuntimeJqError(f"Invalid path expression with result {json.dumps(displayed, separators=(',', ':'))}")
    if path.kind == 'identity':
        old = root
        replacements = list(ev(rhs, old, env))
        if op != '=':
            replacements = [_binary(op[:-1], old, x) if op != '//=' else (old if is_truthy(old) else x) for x in replacements]
        yield from replacements
        return
    if path.kind == 'field' and len(_paths(path, root, env)) <= 1:
        parent_values = list(ev(path.children[0], root, env))
        if not parent_values or not isinstance(parent_values[0], dict):
            raise RuntimeJqError('cannot index')
        parent = parent_values[0]
        old = parent.get(path.value)
        vals = list(ev(rhs, old, env))
        if not vals and op != '=':
            result = copy.deepcopy(root)
            _delete_path(result, _field_chain(path))
            yield result
            return
        if not vals: vals = [None]
        chain = _field_chain(path)
        for val in vals:
            new = val if op in ('=', '|=') else (old if op == '//=' and is_truthy(old) else _binary(op[:-1], old, val))
            result = copy.deepcopy(root)
            target = result
            for key in chain[:-1]: target = target[key]
            target[chain[-1]] = new
            yield result
        return
    locations = _paths(path, root, env)
    if locations:
        result = copy.deepcopy(root)
        for location in sorted(locations, key=lambda item: (len(item), item), reverse=True):
            try: old = _get_path(result, location)
            except (KeyError, IndexError, TypeError): old = None
            values = list(ev(rhs, root if op == '=' else old, env))
            if not values:
                _delete_path(result, location)
                continue
            replacement = values[0]
            value = replacement if op in ('=', '|=') else _binary(op[:-1], old, replacement)
            _set_path_create(result, location, value)
        yield result
        return
    raise RuntimeJqError('invalid update path')


def _paths(node: Filter, root: JsonValue, env: dict[str, JsonValue], prefix: list[object] | None = None) -> list[list[object]]:
    prefix = [] if prefix is None else prefix
    if node.kind == "identity":
        return [prefix]
    if node.kind == "as":
        source, pattern, body = node.children
        result = []
        for value in ev(source, root, env):
            local = dict(env)
            _bind(pattern, value, local)
            result.extend(_paths(body, root, local, prefix))
        return result
    if node.kind == "field":
        return [p + [str(node.value)] for p in _paths(node.children[0], root, env, prefix)]
    if node.kind == "call" and node.value == "select":
        condition = node.children[0] if node.children else Filter("literal", True)
        value = _get_path(root, prefix) if prefix else root
        try:
            accepted = any(is_truthy(v) for v in ev(condition, value, env))
        except RuntimeJqError:
            accepted = False
        return [prefix] if accepted else []
    if node.kind == "call":
        function = env.get("__funcs__", {}).get((str(node.value), 0))
        if function is not None:
            _, body, captured_env, _ = function
            return _paths(body, root, captured_env, prefix)
        return []
    if node.kind == "index":
        base, key, _ = node.value
        result: list[list[object]] = []
        for p in _paths(base, root, env, prefix):
            try:
                parent = _get_path(root, p)
            except (KeyError, IndexError, TypeError, ValueError):
                continue
            if not isinstance(parent, (list, dict, str)):
                continue
            for value in ev(key, parent, env):
                result.append(p + [value])
        return result
    if node.kind == "iterate":
        result = []
        for p in _paths(node.value[0], root, env, prefix):
            try:
                parent = _get_path(root, p)
            except (KeyError, IndexError, TypeError, ValueError):
                continue
            if isinstance(parent, list): result.extend(p + [i] for i in range(len(parent)))
            elif isinstance(parent, dict): result.extend(p + [key] for key in parent)
        return result
    if node.kind == "recurse":
        result = []
        def descend(value, current):
            result.append(current)
            if isinstance(value, list):
                for index, child in enumerate(value): descend(child, current + [index])
            elif isinstance(value, dict):
                for key, child in value.items(): descend(child, current + [key])
        start = _get_path(root, prefix) if prefix else root
        descend(start, prefix)
        return result
    if node.kind == "binary" and node.value == "|":
        result = []
        for left_path in _paths(node.children[0], root, env, prefix):
            try:
                value = _get_path(root, left_path)
            except (KeyError, IndexError, TypeError, ValueError):
                continue
            result.extend([left_path + child for child in _paths(node.children[1], value, env, [])])
        return result
    if node.kind == "binary" and node.value == ",":
        return _paths(node.children[0], root, env, prefix) + _paths(node.children[1], root, env, prefix)
    return []


def _get_path(value: JsonValue, path: list[object]) -> JsonValue:
    current = value
    for part in path:
        if isinstance(current, list): current = current[int(part)]
        else: current = current[part]  # type: ignore[index]
    return current


def _set_path(value: JsonValue, path: list[object], replacement: JsonValue) -> None:
    if not path: return
    current = value
    for part in path[:-1]:
        current = current[int(part)] if isinstance(current, list) else current[part]  # type: ignore[index]
    last = path[-1]
    if isinstance(current, list): current[int(last)] = replacement
    else: current[last] = replacement  # type: ignore[index]

def _set_path_create(value: JsonValue, path: list[object], replacement: JsonValue) -> JsonValue:
    if not path: return replacement
    if value is None:
        if isinstance(path[0], int): value = []
        elif isinstance(path[0], str): value = {}
        else: raise RuntimeJqError('Invalid path')
    current = value
    for index, part in enumerate(path[:-1]):
        nxt = path[index + 1]
        if isinstance(current, dict):
            if not isinstance(part, str):
                raise RuntimeJqError(f'Cannot index object with number ({part})')
            if part not in current or current[part] is None: current[part] = [] if isinstance(nxt, int) else {}
            current = current[part]
        elif isinstance(current, list):
            if not isinstance(part, int):
                raise RuntimeJqError(f'Cannot index array with string ("{part}")')
            part = int(part)
            if part < 0:
                if -part > len(current): raise RuntimeJqError('Out of bounds negative array index')
                part += len(current)
            while len(current) <= part: current.append(None)
            if current[part] is None: current[part] = [] if isinstance(nxt, int) else {}
            current = current[part]
        else:
            raise RuntimeJqError('Cannot index null')
    last = path[-1]
    if isinstance(current, list):
        if not isinstance(last, int):
            raise RuntimeJqError(f'Cannot update field at array index of string')
        last = int(last)
        if last < 0:
            if -last > len(current): raise RuntimeJqError('Out of bounds negative array index')
            last += len(current)
        while len(current) <= last: current.append(None)
        current[last] = replacement
    elif isinstance(current, dict):
        if not isinstance(last, str):
            raise RuntimeJqError(f'Cannot index object with number ({last})')
        current[last] = replacement
    elif current is None:
        # A null root can grow into the container required by the first
        # path component; callers receive the replacement root back.
        if isinstance(path[0], int):
            root: JsonValue = []
        elif isinstance(path[0], str):
            root = {}
        else:
            raise RuntimeJqError('Invalid path')
        return _set_path_create(root, path, replacement)
    else:
        raise RuntimeJqError('Cannot index value')
    return value

def _delete_path(value: JsonValue, path: list[object]) -> None:
    if not path: return
    try:
        parent = _get_path(value, path[:-1]) if len(path) > 1 else value
        last = path[-1]
        if isinstance(parent, list) and isinstance(last, int) and 0 <= last < len(parent): parent.pop(last)
        elif isinstance(parent, dict): parent.pop(last, None)
    except (KeyError, IndexError, TypeError): return


def _field_chain(node: Filter) -> list[str]:
    if node.kind == 'field': return _field_chain(node.children[0]) + [str(node.value)]
    if node.kind == 'identity': return []
    raise RuntimeJqError('invalid update path')

evaluate=ev
