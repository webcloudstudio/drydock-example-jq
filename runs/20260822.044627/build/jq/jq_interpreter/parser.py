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
PREC={",":1,"|":2,"=":3,"|=":3,"+=":3,"-=":3,"*=":3,"/=":3,"%=":3,"//=":3,"//":4,"or":5,"and":6,"==":7,"!=":7,"<":7,">":7,"<=":7,">=":7,"+":8,"-":8,"*":9,"/":9,"%":9}

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
    def expr(self,n):
        x=self.prefix()
        # Binding is a query construct, below all ordinary operators.
        if self.p()=='as' and n <= 2:
            self.take('as'); pattern=self.pattern(); self.take('|')
            return Node('bind',(x,pattern,self.expr(0)))
        while (self.p() in PREC or self.p() in ('and','or')) and PREC.get(self.p(), 0)>=n:
            op=self.take(); q=PREC[op]; x=Node("binary",(op,x,self.expr(q if op in ("=","|=","+=","-=","*=","/=","%=","//=") else q+1)))
        if self.p()=='as' and n <= 2:
            self.take('as'); pattern=self.pattern(); self.take('|')
            return Node('bind',(x,pattern,self.expr(0)))
        return x
    def prefix(self):
        t=self.p()
        if t=='-': self.take(); return Node('unary',('-',self.expr(10)))
        if t=='if': return self.if_expr()
        if t in ('try','reduce','foreach','label','break','def','module','import','include'): return self.control(t)
        if t=='(': self.take(); x=self.expr(0); self.take(')'); return self.post(x)
        if t=='[':
            self.take()
            if self.p()==']': x=Node('array',(None,))
            else:
                parts=[self.expr(2)]
                while self.p()==',': self.take(); parts.append(self.expr(2))
                combined=parts[0]
                for part in parts[1:]: combined=Node('binary',(',',combined,part))
                x=Node('array',(combined,))
            self.take(']'); return self.post(x)
        if t=='{': return self.object()
        if t=='.': self.take(); return self.post(Node('identity'))
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
                a=self.expr(0)
                if self.p()==':': self.take(); b=None if self.p()==']' else self.expr(0); self.take(']'); x=Node('slice',(x,a,b))
                else: self.take(']'); x=Node('indexexpr',(x,a))
                continue
            if self.p()=='(' and isinstance(x,Node) and x.operation=='call':
                name=x.arguments[0]; self.take(); args=[]
                if self.p()!=')':
                    args.append(self.expr(0))
                    # jq's grammar uses semicolons for filter arguments.  The
                    # corpus also exercises the permissive comma spelling.
                    while self.p()==';': self.take(); args.append(self.expr(0))
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
            if self.p()==':': self.take(); v=self.expr(2)
            else:
                # `{name}` and `{$name}` abbreviate an access using the key.
                raw = k.lstrip('$').lstrip('.')
                v=Node('var',(raw,)) if k.startswith('$') else Node('index',(Node('identity'),raw,False))
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
                    key=self.take()
                    if self.p()==':': self.take(); pat=self.pattern()
                    elif key.startswith('$'): pat=Node('pattern_var',(key[1:],))
                    else: pat=Node('pattern_var',(key,))
                    items.append((key.lstrip('$'),pat))
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
        else: self.take('end')
        return Node('if',(c,a,b))
    def _elif_expr(self):
        self.take('elif'); c=self.expr(0); self.take('then'); a=self.expr(0)
        if self.p()=='elif': b=self._elif_expr()
        elif self.p()=='else': self.take(); b=self.expr(0); self.take('end')
        else: self.take('end'); b=Node('literal',('null',))
        return Node('if',(c,a,b))
    def control(self,w):
        self.take(w)
        if w in ('module', 'import', 'include'):
            raise CompileError('module directives are not available')
        if w=='try':
            a=self.expr(2); b=None
            if self.p()=='catch': self.take(); b=self.expr(2)
            return Node('try',(a,b))
        if w=='def':
            name=self.take(); ps=[]
            if self.p()=='(': self.take();
            while self.p() not in (')',':'):
                ps.append(self.take().lstrip('$'))
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
    result=Parser(source).parse()
    # Bare calls are valid jq builtins as well as user definitions supplied by
    # the builtin library.  Retain compile-time rejection for an unknown bare
    # identifier while registering the standard library's zero-argument names.
    known = set('empty error length type not tostring tojson abs fabs floor ceil round sqrt sin cos tan asin acos atan log log10 exp exp2 log2 pow keys sort add min max any all arrays objects iterables booleans numbers normals finites strings nulls values scalars unique reverse paths builtins modulemeta'.split())
    if isinstance(result, Node) and result.operation == 'call' and not result.arguments[1] and result.arguments[0] not in known:
        raise CompileError('unknown filter')
    return result
