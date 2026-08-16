"""Generator evaluator for the frontend AST."""
import json
import math
from collections.abc import Iterator
from typing import Any
from jq_parser import (Array, Binary, Binding, Call, Comma, Conditional, Definition,
    Field, Identity, Index, Interpolated, Iterate, Literal, Object, Pipe, Program,
    Reduce, Slice, Try, Unary, Label, Break)

class RuntimeErrorJq(Exception): pass
class BreakSignal(Exception):
    def __init__(self, name: str) -> None: self.name = name
Env = dict[str, Any]

def truth(value: Any) -> bool: return value is not None and value is not False

def evaluate(program: Any, value: Any) -> Iterator[Any]:
    env: Env = {}
    if isinstance(program, Program):
        env["__funcs__"] = {d.name: d for d in program.definitions}
        yield from run(program.body, value, env)
    else: yield from run(program, value, env)

def run(expr: Any, value: Any, env: Env) -> Iterator[Any]:
    if isinstance(expr, Program): yield from run(expr.body, value, env)
    elif isinstance(expr, Identity): yield value
    elif isinstance(expr, Literal):
        if isinstance(expr.value, tuple) and expr.value[0] == "var":
            if expr.value[1] not in env: raise RuntimeErrorJq("undefined variable")
            bound = env[expr.value[1]]
            # User-defined function parameters are filters, not eagerly
            # reduced values.  Re-running the filter at each use preserves
            # jq's generator semantics and lets surrounding operators form
            # the cartesian product of their outputs.
            if isinstance(bound, tuple) and bound and bound[0] == "filter":
                yield from run(bound[1], value, bound[2])
            else:
                yield bound
        elif isinstance(expr.value, tuple) and expr.value[0] == "call": yield from call(expr.value[1], (), value, env)
        else: yield expr.value
    elif isinstance(expr, Field):
        for base in run(expr.base, value, env):
            if not isinstance(base, dict):
                if expr.optional:
                    continue
                else:
                    raise RuntimeErrorJq("cannot index value")
            else:
                yield base.get(expr.name)
    elif isinstance(expr, Index):
        # Keep key evaluation lazy.  A jq generator can emit a value before a
        # later key raises; materialising the complete key stream would discard
        # that already-ordered prefix.
        for base in run(expr.base, value, env):
            for key in run(expr.key, base, env):
                try:
                    yield index(base, key)
                except RuntimeErrorJq:
                    if not expr.optional:
                        raise
                    yield None
    elif isinstance(expr, Iterate):
        for base in run(expr.base, value, env):
            if isinstance(base, list):
                yield from base
            elif isinstance(base, dict):
                yield from base.values()
            elif expr.optional:
                continue
            elif base is not None:
                raise RuntimeErrorJq("cannot iterate value")
    elif isinstance(expr, Slice):
        for base in run(expr.base, value, env):
            for start in [None] if expr.start is None else run(expr.start, base, env):
                for end in [None] if expr.end is None else run(expr.end, base, env):
                    if not isinstance(base, (list, str)):
                        if expr.optional:
                            continue
                        raise RuntimeErrorJq("cannot slice value")
                    first = int(start) if start is not None else None
                    last = int(end) if end is not None else None
                    yield base[first:last]
    elif isinstance(expr, Interpolated):
        streams = [list(run(part, value, env)) for part in expr.parts]
        for pieces in __import__("itertools").product(*streams):
            yield "".join(piece if isinstance(piece, str) else json.dumps(piece, separators=(",", ":"), ensure_ascii=False) for piece in pieces)
    elif isinstance(expr, Pipe):
        for item in run(expr.left, value, env): yield from run(expr.right, item, env)
    elif isinstance(expr, Comma): yield from run(expr.left, value, env); yield from run(expr.right, value, env)
    elif isinstance(expr, Array): yield list(run(expr.expression, value, env))
    elif isinstance(expr, Object):
        partials = [({}, value)]
        for key_expr, val_expr in expr.pairs:
            next_partials = []
            for obj, original in partials:
                keys = list(run(key_expr, original, env))
                vals = list(run(val_expr, original, env))
                for key in keys:
                    for val in vals:
                        new = dict(obj); new[str(key)] = val; next_partials.append((new, original))
            partials = next_partials
        yield from (obj for obj, _ in partials)
    elif isinstance(expr, Unary):
        for item in run(expr.expression, value, env): yield -item if expr.operator == "-" else item
    elif isinstance(expr, Binary): yield from binary(expr.operator, expr.left, expr.right, value, env)
    elif isinstance(expr, Conditional):
        for condition in run(expr.condition, value, env): yield from run(expr.yes if truth(condition) else expr.no, value, env)
    elif isinstance(expr, Try):
        try: yield from run(expr.expression, value, env)
        except RuntimeErrorJq as error:
            if expr.handler is not None: yield from run(expr.handler, str(error), env)
    elif isinstance(expr, Label):
        try:
            yield from run(expr.body, value, env)
        except BreakSignal as signal:
            if signal.name != expr.name: raise
    elif isinstance(expr, Break):
        raise BreakSignal(expr.name)
    elif isinstance(expr, Binding):
        for bound in run(expr.expression, value, env):
            child = dict(env); child[expr.name] = bound; yield from run(expr.body, value, child)
    elif isinstance(expr, Reduce):
        accumulators = list(run(expr.initial, value, env))
        for item in run(expr.source, value, env):
            new = []
            for accumulator in accumulators:
                child=dict(env); child[expr.name]=item; new.extend(run(expr.update, accumulator, child))
            accumulators=new
        yield from accumulators
    elif isinstance(expr, Call): yield from call(expr.name, expr.args, value, env)
    else: raise RuntimeErrorJq("unknown expression")

def index(value: Any, key: Any) -> Any:
    if isinstance(value, dict): return value.get(str(key))
    if isinstance(value, list) and isinstance(key, (int, float)):
        i=int(key); return value[i] if -len(value) <= i < len(value) else None
    if isinstance(value, str) and isinstance(key, (int, float)): return value[int(key)]
    raise RuntimeErrorJq("cannot index value")

def binary(op: str, left: Any, right: Any, value: Any, env: Env) -> Iterator[Any]:
    if op == "//":
        values=list(run(left,value,env)); good=[x for x in values if truth(x)]
        yield from (good if good else run(right,value,env)); return
    for a in run(left,value,env):
        for b in run(right,value,env):
            if op == "+": result = b if a is None else a if b is None else a+b
            elif op == "-": result = a-b
            elif op == "*": result = a*b
            elif op == "/":
                if b == 0: raise RuntimeErrorJq("division by zero")
                result = a/b
            elif op == "%": result = a%b
            elif op in {"==","!=","<",">","<=",">="}: result = {"==":a==b,"!=":a!=b,"<":a<b,">":a>b,"<=":a<=b,">=":a>=b}[op]
            elif op == "and": result = truth(a) and truth(b)
            elif op == "or": result = truth(a) or truth(b)
            else: raise RuntimeErrorJq(f"unsupported operator {op}")
            yield result

def call(name: str, args: tuple[Any, ...], value: Any, env: Env) -> Iterator[Any]:
    if name == "empty": return
    if name == "length": yield len(value) if isinstance(value,(str,list,dict)) else abs(value) if isinstance(value,(int,float)) else 0; return
    if name == "type": yield "null" if value is None else "boolean" if isinstance(value,bool) else "number" if isinstance(value,(int,float)) else "string" if isinstance(value,str) else "array" if isinstance(value,list) else "object"; return
    if name == "tostring": yield value if isinstance(value,str) else json.dumps(value,separators=(",",":"),ensure_ascii=False); return
    if name == "map":
        yield [item for source in run(Iterate(Identity()),value,env) for item in run(args[0],source,env)]; return
    if name == "select":
        if any(truth(x) for x in run(args[0],value,env)): yield value
        return
    bound = env.get(name)
    if isinstance(bound, tuple) and bound and bound[0] == "filter":
        yield from run(bound[1], value, bound[2])
        return
    if name == "add":
        vals=value; result=None
        for item in vals: result=item if result is None else result+item
        yield result; return
    if name == "range":
        # All range arguments are generators.  Evaluate each against the
        # same input and visit combinations left-to-right.
        for combination in argument_products(args, value, env):
            if len(combination) == 1:
                start, end, step = 0, combination[0], 1
            elif len(combination) == 2:
                start, end, step = combination[0], combination[1], 1
            elif len(combination) == 3:
                start, end, step = combination
            else:
                raise RuntimeErrorJq("range takes one to three arguments")
            if step == 0:
                raise RuntimeErrorJq("step cannot be zero")
            current = start
            while (step > 0 and current < end) or (step < 0 and current > end):
                yield current
                current += step
        return
    funcs=env.get("__funcs__",{})
    definition: Definition | None = funcs.get(name)
    if definition is not None:
        child=dict(env)
        if len(args) != len(definition.args):
            raise RuntimeErrorJq(f"function {name} expects {len(definition.args)} arguments")
        for param, argument in zip(definition.args,args):
            child[param] = ("filter", argument, env)
        yield from run(definition.body,value,child); return
    raise RuntimeErrorJq(f"unknown function {name}")


def argument_products(args: tuple[Any, ...], value: Any, env: Env) -> Iterator[tuple[Any, ...]]:
    """Yield the ordered cartesian product of generator-valued arguments."""
    # Keep each argument as a live generator.  Besides avoiding an
    # unnecessary full materialisation, this preserves jq's streaming
    # behaviour when a later argument raises after an earlier combination has
    # already been emitted.
    def product(index: int, chosen: tuple[Any, ...]) -> Iterator[tuple[Any, ...]]:
        if index == len(args):
            yield chosen
            return
        for item in run(args[index], value, env):
            yield from product(index + 1, chosen + (item,))

    yield from product(0, ())
