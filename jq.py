#!/usr/bin/env python3
import sys,json,re,math,base64,urllib.parse,html,functools,statistics

class CompileError(Exception): pass
class RuntimeErrorJQ(Exception): pass
class Empty: pass
EMPTY=Empty()

def truth(x): return x is not False and x is not None
def equal(a,b):
    if isinstance(a,bool) or isinstance(b,bool): return type(a) is type(b) and a==b
    return a==b
def compact(x):
    if isinstance(x,float):
        if math.isnan(x): return 'null'
        if math.isinf(x): return '1.7976931348623157e+308' if x>0 else '-1.7976931348623157e+308'
    return json.dumps(x,separators=(',',':'),ensure_ascii=False,allow_nan=False)

TOKEN=re.compile(r'''\s*(?:(\d+(?:\.\d*)?(?:[eE][+-]?\d+)?)|("(?:\\.|[^"\\])*")|(\$[A-Za-z_][A-Za-z_0-9]*)|([A-Za-z_][A-Za-z_0-9]*)|(==|!=|<=|>=|//|\?//|\+=|-=|\*=|/=|%=|\|=|\.\.|[{}\[\](),;:.|+*/%<>=?!-]))''')
class Parser:
 def __init__(self,s):
  self.t=[]; p=0
  while p<len(s):
   m=TOKEN.match(s,p)
   if not m:
    if s[p:].strip(): raise CompileError('invalid token')
    break
   p=m.end(); v=next(x for x in m.groups() if x is not None); self.t.append(v)
  self.i=0
 def peek(self): return self.t[self.i] if self.i<len(self.t) else None
 def pop(self,x=None):
  v=self.peek()
  if x is not None and v!=x: raise CompileError('expected '+x)
  self.i+=1; return v
 def program(self):
  n=self.expr()
  if self.peek() is not None: raise CompileError('unexpected token '+str(self.peek()))
  return n
 def expr(self,minp=0):
  a=self.atom()
  # postfix field/index/call and binding
  while True:
   t=self.peek()
   if t=='.' and self.i+1<len(self.t) and re.match(r'^[A-Za-z_]',self.t[self.i+1]): self.pop(); a=('get',a,('lit',self.pop())); continue
   if t=='[':
    self.pop()
    if self.peek()==']': self.pop(); a=('iter',a); continue
    b=self.expr();
    if self.peek()==':': self.pop(); c=None if self.peek()==']' else self.expr(); self.pop(']'); a=('slice',a,b,c)
    else: self.pop(']'); a=('index',a,b)
    continue
   if t=='?': self.pop(); a=('try',a,('emptycatch',)); continue
   if t=='as':
    self.pop(); var=self.pop(); self.pop('|'); a=('as',a,var,self.expr(0)); continue
   prec={'|':1,',':1,'//':2,'or':3,'and':4,'==':5,'!=':5,'<':5,'>':5,'<=':5,'>=':5,'+':6,'-':6,'*':7,'/':7,'%':7}.get(t,-1)
   if prec<minp: break
   self.pop(); b=self.expr(prec+(0 if t==',' else 1)); a=(t,a,b)
  return a
 def atom(self):
  t=self.pop()
  if t is None: raise CompileError('incomplete program')
  if t=='(':
   a=self.expr(); self.pop(')'); return a
  if t=='.': return ('dot',)
  if t.startswith('$'): return ('var',t)
  if t[0]=='"':
   try: return ('lit',json.loads(t))
   except: raise CompileError('bad string')
  if re.match(r'^\d',t): return ('lit',float(t) if any(c in t for c in '.eE') else int(t))
  if t=='-': return ('neg',self.expr(8))
  if t in ('true','false','null'): return ('lit',{'true':True,'false':False,'null':None}[t])
  if t=='empty': return ('empty',)
  if t=='[':
   if self.peek()==']': self.pop(); return ('array',None)
   a=self.expr(); self.pop(']'); return ('array',a)
  if t=='{':
   pairs=[]
   while self.peek()!='}':
    k=self.pop();
    if k==',': raise CompileError('bad object')
    if self.peek()==':': self.pop(); v=self.expr(0)
    else: v=('get',('dot',),('lit',k))
    pairs.append((k[1:-1] if k.startswith('"') else k,v))
    if self.peek()==',': self.pop()
    else: break
   self.pop('}'); return ('object',pairs)
  if t=='if':
   c=self.expr(); self.pop('then'); a=self.expr(); b=('lit',None)
   if self.peek()=='else': self.pop(); b=self.expr()
   self.pop('end'); return ('if',c,a,b)
  if t=='try':
   a=self.expr(); b=('emptycatch',)
   if self.peek()=='catch': self.pop(); b=self.expr()
   return ('try',a,b)
  if re.match(r'^[A-Za-z_]',t):
   if self.peek()=='(':
    self.pop(); args=[]
    if self.peek()!=')':
     args.append(self.expr())
     while self.peek()==';': self.pop(); args.append(self.expr())
    self.pop(')'); return ('call',t,args)
   return ('call',t,[])
  raise CompileError('unexpected '+t)

def walk_get(v,k):
 if isinstance(v,dict): return v.get(str(k),None)
 if isinstance(v,list):
  try: return v[int(k)] if -len(v)<=int(k)<len(v) else None
  except: return None
 if isinstance(v,str):
  try:return v[int(k)]
  except:return None
 raise RuntimeErrorJQ('cannot index')
def values(ast,inp,env):
 typ=ast[0]
 if typ=='lit': yield ast[1]
 elif typ=='dot': yield inp
 elif typ=='var': yield env.get(ast[1],None)
 elif typ=='empty': return
 elif typ=='neg':
  for x in values(ast[1],inp,env): yield -x
 elif typ=='get':
  for x in values(ast[1],inp,env): yield walk_get(x,ast[2][1])
 elif typ=='index':
  for x in values(ast[1],inp,env):
   for k in values(ast[2],inp,env): yield walk_get(x,k)
 elif typ=='iter':
  for x in values(ast[1],inp,env):
   if isinstance(x,dict): yield from x.values()
   elif isinstance(x,(list,str)): yield from x
   else: raise RuntimeErrorJQ('cannot iterate')
 elif typ=='slice':
  for x in values(ast[1],inp,env):
   for a in values(ast[2],inp,env):
    bs=list(values(ast[3],inp,env)) if ast[3] else [None]
    for b in bs: yield x[int(a) if a is not None else None:int(b) if b is not None else None]
 elif typ=='array':
  if ast[1] is None: yield []
  else: yield list(values(ast[1],inp,env))
 elif typ=='object':
  def rec(i,o):
   if i==len(ast[1]): yield o; return
   k,v=ast[1][i]
   for z in values(v,inp,env): yield from rec(i+1,{**o,k:z})
  yield from rec(0,{})
 elif typ==',': yield from values(ast[1],inp,env); yield from values(ast[2],inp,env)
 elif typ=='|':
  for x in values(ast[1],inp,env): yield from values(ast[2],x,env)
 elif typ=='as':
  for x in values(ast[1],inp,env):
   for _ in [x]:
    e=dict(env); e[ast[2]]=x; yield from values(ast[3],inp,e)
 elif typ=='if':
  for c in values(ast[1],inp,env): yield from values(ast[2] if truth(c) else ast[3],inp,env)
 elif typ=='try':
  try: yield from values(ast[1],inp,env)
  except RuntimeErrorJQ as e:
   if ast[2][0]!='emptycatch': yield from values(ast[2],str(e),env)
 elif typ in ('+','-','*','/','%','==','!=','<','>','<=','>=','and','or','//'):
  left=list(values(ast[1],inp,env))
  if typ=='//':
   good=[x for x in left if truth(x)]
   yield from (good or list(values(ast[2],inp,env))); return
  for a in left:
   for b in values(ast[2],inp,env): yield op(typ,a,b)
 elif typ=='call': yield from builtin(ast[1],ast[2],inp,env)
 else: raise RuntimeErrorJQ('unsupported')

def op(t,a,b):
 if t=='==': return equal(a,b)
 if t=='!=': return not equal(a,b)
 if t in ('<','>','<=','>='): return {'<':a<b,'>':a>b,'<=':a<=b,'>=':a>=b}[t]
 if t=='and': return truth(a) and truth(b)
 if t=='or': return truth(a) or truth(b)
 if t=='+':
  if a is None:return b
  if b is None:return a
  if isinstance(a,list) and isinstance(b,list):return a+b
  if isinstance(a,dict) and isinstance(b,dict):return {**a,**b}
  if isinstance(a,str) and isinstance(b,str):return a+b
  return a+b
 if t=='-': return [x for x in a if x not in b] if isinstance(a,list) else a-b
 if t=='*': return a*b if not isinstance(a,dict) else {**a,**b}
 if t=='/':
  if b==0: raise RuntimeErrorJQ('division by zero')
  return a/b
 if t=='%': return a%b

def builtin(n,args,inp,env):
 def av(i=0): return list(values(args[i],inp,env)) if i<len(args) else [inp]
 if n=='length': yield len(inp) if hasattr(inp,'__len__') else 0
 elif n=='add': yield sum(inp) if isinstance(inp,list) else inp
 elif n in ('type',): yield 'null' if inp is None else 'boolean' if isinstance(inp,bool) else 'number' if isinstance(inp,(int,float)) else 'string' if isinstance(inp,str) else 'array' if isinstance(inp,list) else 'object'
 elif n=='keys': yield list(range(len(inp))) if isinstance(inp,list) else sorted(inp)
 elif n=='range':
  aa=av(); start=aa[0]; end=aa[1] if len(aa)>1 else start; step=aa[2] if len(aa)>2 else 1
  yield from range(int(start),int(end),int(step))
 elif n in ('map','map_values'):
  out=[]
  for x in inp:
   z=list(values(args[0],x,env)); out.extend(z if n=='map' else [z[-1] if z else None])
  yield out
 elif n=='select':
  if truth(next(values(args[0],inp,env),None)): yield inp
 elif n=='not': yield not truth(inp)
 elif n=='error': raise RuntimeErrorJQ(str(av()[0]) if args else 'error')
 elif n=='tostring': yield compact(inp) if not isinstance(inp,str) else inp
 elif n=='tojson': yield compact(inp)
 elif n=='fromjson': yield json.loads(inp)
 elif n=='tonumber': yield float(inp) if '.' in str(inp) else int(inp)
 elif n=='abs': yield abs(inp)
 elif n=='floor': yield math.floor(inp)
 elif n=='sqrt': yield math.sqrt(inp)
 elif n=='sin': yield math.sin(inp)
 elif n=='cos': yield math.cos(inp)
 elif n=='empty': return
 elif n=='first': yield next(iter(values(args[0],inp,env)))
 elif n=='last': yield list(values(args[0],inp,env))[-1]
 elif n=='sort': yield sorted(inp)
 elif n=='unique': yield sorted(set(inp))
 elif n=='reverse': yield inp[::-1]
 elif n in ('arrays','objects','iterables','scalars','values','booleans','nulls'):
  ok={'arrays':isinstance(inp,list),'objects':isinstance(inp,dict),'iterables':isinstance(inp,(list,dict)),'scalars':not isinstance(inp,(list,dict)),'values':inp is not None,'booleans':isinstance(inp,bool),'nulls':inp is None}[n]
  if ok: yield inp
 elif n=='contains':
  b=av(0)[0]; yield b in inp
 elif n=='startswith': yield inp.startswith(av()[0])
 elif n=='endswith': yield inp.endswith(av()[0])
 elif n=='split': yield inp.split(av()[0])
 elif n=='join': yield av()[0].join(map(str,inp))
 elif n=='trim': yield inp.strip()
 elif n=='ltrim': yield inp.lstrip()
 elif n=='rtrim': yield inp.rstrip()
 elif n=='utf8bytelength': yield len(inp.encode())
 elif n=='has': yield (av()[0] in inp)
 elif n=='implode': yield ''.join(chr(x) for x in inp)
 elif n=='explode': yield [ord(x) for x in inp]
 else: raise RuntimeErrorJQ('unknown function '+n)

def main(argv):
 if len(argv)!=3 or argv[1]!='-c': print('usage: jq -c PROGRAM',file=sys.stderr); return 3
 try: ast=Parser(argv[2]).program()
 except Exception as e: print('compile error: '+str(e),file=sys.stderr); return 3
 try:
  for line in sys.stdin:
   if not line.strip(): continue
   inp=json.loads(line)
   for x in values(ast,inp,{}): print(compact(x))
  return 0
 except Exception as e:
  print('runtime error: '+str(e),file=sys.stderr); return 5
if __name__=='__main__': raise SystemExit(main(sys.argv))
