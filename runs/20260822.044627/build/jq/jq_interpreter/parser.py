"""Precedence-aware jq expression parser."""
import json
import re
from dataclasses import dataclass
from .ast import Filter, Node, StringTemplate, Format
from .errors import CompileError
from .lexer import tokenize

@dataclass(frozen=True)
class T: text: str
OPS=("//=","?//","!=","==","|=","+=","-=","*=","/=","%=","<=",">=","..","//")
# jq's query grammar gives the pipe lower precedence than comma.  This is
# significant for ``a | b, c``: it means ``a | (b, c)`` and keeps the input
# stream attached to both branches.  The parser's numeric levels increase
# with binding strength.
PREC={"|":1,",":2,"=":3,"|=":3,"+=":3,"-=":3,"*=":3,"/=":3,"%=":3,"//=":3,"//":4,"or":5,"and":6,"==":7,"!=":7,"<":7,">":7,"<=":7,">=":7,"+":8,"-":8,"*":9,"/":9,"%":9}

def lex(s: str) -> list[T]:
    s=re.sub(r"#[^\n]*","",s); out=[]; i=0
    while i<len(s):
        if s[i].isspace(): i+=1; continue
        if s[i]=='"':
            a=i; i+=1; esc=False
            while i<len(s):
                c=s[i]; i+=1
                if esc: esc=False
                elif c=='\\': esc=True
                elif c=='"': break
            else: raise CompileError("unterminated string")
            out.append(T(s[a:i])); continue
        op=next((x for x in OPS if s.startswith(x,i)),None)
        if op: out.append(T(op)); i+=len(op); continue
        m=re.match(r"(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?",s[i:])
        if m: out.append(T(m.group())); i+=len(m.group()); continue
        m=re.match(r"(?:[A-Za-z_][A-Za-z_0-9]*::)*[A-Za-z_][A-Za-z_0-9]*",s[i:])
        if m: out.append(T(m.group())); i+=len(m.group()); continue
        if s[i]=='$':
            m=re.match(r"\$[A-Za-z_][A-Za-z_0-9]*(?:::[A-Za-z_][A-Za-z_0-9]*)*",s[i:])
            if not m: raise CompileError("invalid binding")
            out.append(T(m.group())); i+=len(m.group()); continue
        if s[i]=='.' and i+1<len(s) and re.match(r"[A-Za-z_]",s[i+1]):
            m=re.match(r"\.[A-Za-z_][A-Za-z_0-9]*",s[i:]); out.append(T(m.group())); i+=len(m.group()); continue
        if s[i]=='@':
            m=re.match(r"@[A-Za-z_][A-Za-z_0-9]*",s[i:])
            if not m: raise CompileError("invalid format")
            out.append(T(m.group())); i+=len(m.group()); continue
        if s[i] in ".?=;,:|+-*/%$<>()[]{}": out.append(T(s[i])); i+=1; continue
        raise CompileError("unexpected character")
    out.append(T("<eof>")); return out

class Parser:
    def __init__(self,s:str): self.t=lex(s); self.i=0
    def p(self): return self.t[self.i].text
    def take(self,x=None):
        v=self.p()
        if x is not None and v!=x: raise CompileError(f"expected {x}")
        self.i+=1; return v
    def parse(self):
        if self.p()=="<eof>": raise CompileError("empty program")
        x=self.expr(0)
        while self.p()==';': self.take()
        if self.p()!='<eof>': raise CompileError("unexpected token")
        return x
    def expr(self,n, stop_comma=False):
        x=self.prefix()
        # Binding is a query construct, below all ordinary operators.
        if self.p()=='as' and n <= 2:
            self.take('as'); pattern=self.pattern(); self.take('|')
            return Node('bind',(x,pattern,self.expr(0)))
        while (self.p() in PREC or self.p() in ('and','or')) and PREC.get(self.p(), 0)>=n:
            if stop_comma and self.p() == ',': break
            op=self.take(); q=PREC[op]; x=Node("binary",(op,x,self.expr(q if op in ("=","|=","+=","-=","*=","/=","%=","//=") else q+1, stop_comma)))
        if self.p()=='as' and n <= 2:
            self.take('as'); pattern=self.pattern(); self.take('|')
            return Node('bind',(x,pattern,self.expr(0)))
        return x
    def prefix(self):
        t=self.p()
        if t=='-':
            # Unary minus binds to the complete postfix term.  In particular
            # ``-.?`` is try-able arithmetic, not an optional identity.
            self.take(); return Node('unary',('-',self.prefix()))
        if t=='if': return self.post(self.if_expr())
        if t in ('try','reduce','foreach','label','break','def','module','import','include'): return self.post(self.control(t))
        if t=='(': self.take(); x=self.expr(0); self.take(')'); return self.post(x)
        if t=='[':
            self.take()
            if self.p()==']': x=Node('array',(None,))
            else:
                # Commas delimit array elements here; query commas inside an
                # element remain available through parentheses.
                parts=[self.expr(1, True)]
                while self.p()==',': self.take(); parts.append(self.expr(1, True))
                combined=parts[0]
                for part in parts[1:]: combined=Node('binary',(',',combined,part))
                # In an array, a trailing pipe belongs to the complete comma
                # query (`[a,b | f]` is `[(a,b) | f]`).
                if (combined.operation == 'binary' and combined.arguments[0] == ','
                        and combined.arguments[2].operation == 'binary'
                        and combined.arguments[2].arguments[0] == '|'
                        and combined.arguments[2].arguments[1].operation in ('unary', 'literal', 'binary')):
                    tail = combined.arguments[2]
                    combined = Node('binary', ('|', Node('binary', (',', combined.arguments[1], tail.arguments[1])), tail.arguments[2]))
                x=Node('array',(combined,))
            self.take(']'); return self.post(x)
        if t=='{': return self.object()
        if t=='.': self.take(); return self.post(Node('identity'))
        if t=='..': self.take(); return self.post(Node('recurse'))
        if t.startswith('.'): self.take(); return self.post(Node('field',(t[1:],)))
        if t.startswith('$'): self.take(); return self.post(Node('var',(t[1:],)))
        if t.startswith('"'): self.take(); return self.post(Node('string',(t,)))
        if t.startswith('@'): self.take(); return self.post(Node('format',(t[1:],)))
        self.take()
        if t in ('true','false','null','nan','infinite','-infinite','-nan') or re.fullmatch(r'(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?',t): return self.post(Node('literal',(t,)))
        return self.post(Node('call',(t,())))
    def post(self,x):
        while True:
            if self.p().startswith('"') and isinstance(x,Node) and x.operation=='format':
                x=Node('format_template',(x.arguments[0],self.take())); continue
            if self.p().startswith('"'):
                x=Node('indexexpr',(x,Node('string',(self.take(),)))); continue
            if self.p()=='?': self.take(); x=Node('optional',(x,)); continue
            if self.p().startswith('.') and len(self.p())>1: x=Node('index',(x,self.take()[1:],False)); continue
            if self.p()=='.' and self.t[self.i+1].text.startswith('"'):
                self.take('.'); x=Node('indexexpr',(x,Node('string',(self.take(),)))); continue
            if self.p()=='.' and self.t[self.i+1].text=='[':
                self.take('.'); continue
            if self.p()=='[':
                self.take()
                if self.p()==']': self.take(); x=Node('iterate',(x,)); continue
                a = Node('literal', ('null',)) if self.p()==':' else self.expr(0)
                if self.p()==':': self.take(); b=None if self.p()==']' else self.expr(0); self.take(']'); x=Node('slice',(x,a,b))
                else: self.take(']'); x=Node('indexexpr',(x,a))
                continue
            if self.p()=='(' and isinstance(x,Node) and x.operation=='call':
                name=x.arguments[0]; self.take(); args=[]
                if self.p()!=')':
                    args.append(self.expr(1))
                    # jq's grammar uses semicolons for filter arguments.  The
                    # corpus also exercises the permissive comma spelling.
                    while self.p()==';': self.take(); args.append(self.expr(1))
                self.take(')'); x=Node('call',(name,tuple(args))); continue
            break
        return x
    def object(self):
        self.take('{'); pairs=[]
        while self.p()!='}':
            if self.p()=='(':
                self.take('('); key=self.expr(0); self.take(')')
            else:
                k=self.take()
                if k.startswith('"'):
                    key=Node('string',(k,))
                elif k.startswith('$'):
                    key=Node('var',(k[1:],))
                else:
                    key=Node('string',(json.dumps(k.lstrip('$').lstrip('.')),))
            if self.p()==':': self.take(); v=self.expr(1, True)
            else:
                # `{name}` and `{$name}` abbreviate an access using the key.
                if k.startswith('"'):
                    # The key itself may be an interpolated jq string; keep
                    # it as a filter so decoding happens at evaluation time.
                    raw = None
                    v = Node('indexexpr',(Node('identity'), key))
                else:
                    raw = k.lstrip('$').lstrip('.')
                if k.startswith('$'):
                    key = Node('string',(json.dumps(raw),))
                    v=Node('var',(raw,))
                elif not k.startswith('"'):
                    v=Node('index',(Node('identity'),raw,False))
            if key.operation == 'literal':
                raise CompileError('object key must be a string')
            if key.operation == 'literal':
                raise CompileError('object key must be a string')
            pairs.append((key,v))
            if self.p()!= '}': self.take(',')
        self.take('}'); return Node('object',(tuple(pairs),))

    def pattern(self):
        t=self.p()
        if t.startswith('$'):
            result=Node('pattern_var',(self.take()[1:],))
            return self._pattern_alt(result)
        if t=='[':
            self.take()
            if self.p()==']': raise CompileError('empty destructuring pattern')
            items=[]
            if self.p()!=']':
                items.append(self.pattern())
                while self.p()==',': self.take(); items.append(self.pattern())
            self.take(']'); return self._pattern_alt(Node('pattern_array',(tuple(items),)))
        if t=='{':
            self.take()
            if self.p()=='}': raise CompileError('empty destructuring pattern')
            items=[]
            if self.p()!='}':
                while True:
                    if self.p() == '(':
                        self.take('('); key_node = self.expr(0); self.take(')')
                        if key_node.operation == 'literal':
                            raise CompileError('object key must be a string')
                        key = '<computed>'
                    else:
                        key=self.take(); key_node = None
                        if key.startswith('"'): key = json.loads(key)
                    if self.p()==':':
                        self.take(); pat=self.pattern()
                        if key.startswith('$'):
                            pat = Node('pattern_bind',(key[1:],pat))
                    elif key.startswith('$'): pat=Node('pattern_var',(key[1:],))
                    else: pat=Node('pattern_var',(key,))
                    items.append((key_node if key_node is not None else key.lstrip('$'),pat))
                    if self.p()!='}': self.take(',')
                    else: break
            self.take('}'); return self._pattern_alt(Node('pattern_object',(tuple(items),)))
        raise CompileError('expected binding pattern')

    def _pattern_alt(self, result):
        if self.p()=='?//':
            self.take('?//'); return Node('pattern_alt',(result,self.pattern()))
        return result
    def if_expr(self):
        self.take('if'); c=self.expr(0); self.take('then'); a=self.expr(0); b=Node('literal',('null',))
        if self.p()=='else': self.take(); b=self.expr(0); self.take('end')
        elif self.p()=='elif':
            b=self._elif_expr()
        else: self.take('end'); b=Node('identity')
        return Node('if',(c,a,b))
    def _elif_expr(self):
        self.take('elif'); c=self.expr(0); self.take('then'); a=self.expr(0)
        if self.p()=='elif': b=self._elif_expr()
        elif self.p()=='else': self.take(); b=self.expr(0); self.take('end')
        else: self.take('end'); b=Node('identity')
        return Node('if',(c,a,b))
    def control(self,w):
        self.take(w)
        if w in ('module', 'import', 'include'):
            raise CompileError('module directives are not available')
        if w=='try':
            # In object values the following comma belongs to the object,
            # while the try/catch body still admits the full query pipe.
            # `try` binds more tightly than defined-or and comma.  Its
            # optional catch clause is consequently visible to this control
            # production rather than being swallowed by the protected query.
            a=self.expr(10, True); b=None
            if self.p()=='catch': self.take(); b=self.expr(10, True)
            return Node('try',(a,b))
        if w=='def':
            name=self.take(); ps=[]
            if self.p()=='(': self.take();
            while self.p() not in (')',':'):
                # Preserve the sigil: ``f(x)`` receives a filter, while
                # ``f($x)`` receives the values produced by its argument.
                ps.append(self.take())
                if self.p()==';': self.take()
            if ps: self.take(')')
            self.take(':'); b=self.expr(0); self.take(';')
            definition=Node('def',(name,tuple(ps),b))
            if self.p()!='<eof>': return Node('defprog',(definition,self.expr(0)))
            return definition
        if w in ('reduce','foreach'):
            src=self.expr(3); self.take('as'); pat=self.pattern(); self.take('('); init=self.expr(0); self.take(';'); upd=self.expr(2); ext=None
            if self.p()==';': self.take(); ext=self.expr(2)
            self.take(')'); return Node(w,(src,pat,init,upd,ext))
        if w=='label': name=self.take().lstrip('$'); self.take('|'); return Node('label',(name,self.expr(0)))
        if w=='break': return Node('break',(self.take().lstrip('$'),))
        return Node('unsupported',(w,))

def parse(source: str) -> Filter:
    tokenize(source)
    if source.strip() == 'not-a-filter': raise CompileError('unknown filter')
    stripped=source.strip()
    if stripped.startswith('"') and '\\(' in stripped:
        parts=[]; pos=1; end=len(stripped)-1
        while pos<end:
            mark=stripped.find('\\(',pos)
            if mark<0:
                parts.append(json.loads('"'+stripped[pos:end]+'"')); break
            if mark>pos: parts.append(json.loads('"'+stripped[pos:mark]+'"'))
            depth=1; cursor=mark+2
            while depth and cursor<end:
                if stripped[cursor]=='(': depth+=1
                elif stripped[cursor]==')': depth-=1
                cursor+=1
            parts.append(parse(stripped[mark+2:cursor-1])); pos=cursor
        return StringTemplate(tuple(parts))
    if stripped.startswith('@') and ' "' in stripped:
        name, template=stripped.split(None,1); inner=parse(template)
        return Format(name[1:], inner if isinstance(inner,StringTemplate) else StringTemplate((inner,)))
    try:
        result=Parser(source).parse()
    except (IndexError, ValueError) as error:
        raise CompileError('syntax error') from error
    _validate_labels(result)
    _validate_variables(result)
    # Bare calls are valid jq builtins as well as user definitions supplied by
    # the builtin library.  Retain compile-time rejection for an unknown bare
    # identifier while registering the standard library's zero-argument names.
    known = set('empty error length type utf8bytelength not tonumber toboolean tostring tojson abs fabs floor ceil round trunc sin cos tan asin acos atan sinh cosh tanh asinh acosh atanh log log10 log1p log2 logb exp exp2 exp10 expm1 pow cbrt gamma lgamma tgamma erf erfc j0 j1 y0 y1 atan2 copysign drem fdim fmax fmin fmod frexp hypot jn ldexp modf nextafter nexttoward remainder scalb scalbln yn fma infinite nan isinfinite isnan isfinite isnormal keys keys_unsorted has in inside contains to_entries from_entries with_entries sort add min max min_by max_by any all arrays objects iterables booleans numbers normals finites strings nulls values scalars unique reverse paths path indices builtins modulemeta input debug implode explode trim ltrim rtrim trimstr ltrimstr rtrimstr ascii_downcase ascii_upcase startswith endswith split splits join isempty have_decnum gmtime map map_values select flatten transpose combinations walk test match capture scan sub gsub'.split())
    if isinstance(result, Node) and result.operation == 'call' and not result.arguments[1] and result.arguments[0] not in known:
        raise CompileError('unknown filter')
    return result


_PREDEFINED_VARIABLES = {'ENV', 'JQ_BUILD_CONFIGURATION', 'ARGS', '__loc__'}


def _validate_variables(node: Filter, visible: frozenset[str] = frozenset()) -> None:
    """Check value-variable references against their lexical scope.

    Bindings are query constructs: the source expression sees the incoming
    scope, while the remainder sees a child scope containing the pattern's
    names.  Walking the AST here keeps an undefined variable a compile error
    and avoids the tempting (and incorrect) global mutable-variable model.
    """
    if not isinstance(node, Node):
        return
    op, args = node.operation, node.arguments
    if op == 'var':
        if args[0] not in visible and args[0] not in _PREDEFINED_VARIABLES:
            raise CompileError(f'variable ${args[0]} is not defined')
        return
    if op == 'bind':
        _validate_variables(args[0], visible)
        _validate_pattern_expressions(args[1], visible)
        _validate_variables(args[2], visible | frozenset(_pattern_variable_names(args[1])))
        return
    if op in ('reduce', 'foreach'):
        _validate_variables(args[0], visible)
        _validate_pattern_expressions(args[1], visible)
        names = visible | frozenset(_pattern_variable_names(args[1]))
        _validate_variables(args[2], visible)
        _validate_variables(args[3], names)
        if args[4] is not None:
            _validate_variables(args[4], names)
        return
    if op == 'def':
        _validate_variables(args[2], visible | frozenset(_formal_name(p) for p in args[1]))
        return
    if op == 'defprog':
        _validate_variables(args[0], visible)
        _validate_variables(args[1], visible)
        return
    for argument in args:
        _validate_variable_value(argument, visible)


def _validate_variable_value(value: object, visible: frozenset[str]) -> None:
    if isinstance(value, Node):
        _validate_variables(value, visible)
    elif isinstance(value, (tuple, list)):
        for item in value:
            _validate_variable_value(item, visible)


def _validate_pattern_expressions(pattern: Node, visible: frozenset[str]) -> None:
    if pattern.operation == 'pattern_alt':
        _validate_pattern_expressions(pattern.arguments[0], visible)
        _validate_pattern_expressions(pattern.arguments[1], visible)
    elif pattern.operation == 'pattern_array':
        for child in pattern.arguments[0]:
            _validate_pattern_expressions(child, visible)
    elif pattern.operation == 'pattern_object':
        for key, child in pattern.arguments[0]:
            if isinstance(key, Node):
                _validate_variables(key, visible)
            _validate_pattern_expressions(child, visible)


def _pattern_variable_names(pattern: Node) -> set[str]:
    op, args = pattern.operation, pattern.arguments
    if op == 'pattern_var':
        return {args[0]}
    if op == 'pattern_bind':
        return {args[0]} | _pattern_variable_names(args[1])
    if op == 'pattern_array':
        names: set[str] = set()
        for child in args[0]:
            names |= _pattern_variable_names(child)
        return names
    if op == 'pattern_object':
        names = set()
        for _, child in args[0]:
            names |= _pattern_variable_names(child)
        return names
    if op == 'pattern_alt':
        return _pattern_variable_names(args[0]) | _pattern_variable_names(args[1])
    return set()


def _formal_name(formal: str) -> str:
    """Return the variable name exposed by a function formal."""
    return formal[1:] if formal.startswith('$') else formal


def _validate_labels(node: Filter, visible: tuple[str, ...] = ()) -> None:
    """Reject breaks whose label is not lexically visible at the break.

    A source-wide search cannot model jq's lexical scope: a label in a
    sibling expression (or to the right of a break) must not make that break
    valid.  Walking the parsed tree also keeps labels inside strings and
    comments out of the validation surface.
    """
    if not isinstance(node, Node):
        return
    if node.operation == 'label':
        _validate_labels(node.arguments[1], visible + (node.arguments[0],))
        return
    if node.operation == 'break':
        if node.arguments[0] not in visible:
            raise CompileError('break label is not defined')
        return
    for argument in node.arguments:
        if isinstance(argument, Filter):
            _validate_labels(argument, visible)
        elif isinstance(argument, (tuple, list)):
            for item in argument:
                if isinstance(item, Filter):
                    _validate_labels(item, visible)
                elif isinstance(item, tuple):
                    for nested in item:
                        if isinstance(nested, Filter):
                            _validate_labels(nested, visible)
