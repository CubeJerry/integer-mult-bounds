"""Independent exact matrix and formal monomial-algebra certificate audit."""
from pathlib import Path
from fractions import Fraction as F
import argparse,importlib.util,itertools,json,hashlib
p=argparse.ArgumentParser();p.add_argument('--engine',type=Path,required=True);p.add_argument('--certificates',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
spec=importlib.util.spec_from_file_location('root_engine',a.engine);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def norm(M,k=0):
 while k and all(z[0]%2==z[1]%2==0 for row in M for z in row):M=[[(z[0]//2,z[1]//2) for z in row] for row in M];k-=1
 return k,tuple(z for row in M for z in row)
def mat(x):return [list(x[1][8*i:8*i+8]) for i in range(8)]
def mul(x,y):return norm(g.mm(mat(x),mat(y)),x[0]+y[0])
def adj(x):
 M=mat(x);return norm([[(M[j][i][0],-M[j][i][1]) for j in range(8)] for i in range(8)],x[0])
def pw(x,n):
 z=I
 for _ in range(n):z=mul(z,x)
 return z
def mono(p,q=None):return norm(g.mono(p,q))
I=mono(list(range(8)));C=[norm(g.gaussian(j,3),1) for j in range(3)]
def ordinary(x):
 M=mat(x);return x[0]==0 and all(sum(z!=(0,0) for z in row)==1 for row in M) and all(sum(M[i][j]!=(0,0) for i in range(8))==1 for j in range(8)) and all(z==(0,0) or z in g.UNIT for row in M for z in row)
def padd(x,y):
 z=dict(x)
 for h,c in y.items():z[h]=z.get(h,F(0))+c
 return {h:c for h,c in z.items() if c}
def pmul(x,y):
 z={}
 for h,c in x.items():
  for k,d in y.items():v=mul(h,k);z[v]=z.get(v,F(0))+c*d
 return {h:c for h,c in z.items() if c}
def blockmul(X,Y):
 Z=[[{} for _ in Y[0]] for _ in X]
 for i,j,k in itertools.product(range(len(X)),range(len(Y[0])),range(len(Y))):Z[i][j]=padd(Z[i][j],pmul(X[i][k],Y[k][j]))
 return Z
def one(x,c=1):return {x:F(c)}
def fromjson(M):return [[{mono(t['permutation'],t['phase_mod4']):F(t['coefficient']) for t in cell} for cell in row] for row in M]
certs=json.loads(a.certificates.read_text());cases=[];inverse=[]
for mask,J,B in [(128,0,0),(64,0,1),(112,1,0),(176,1,1)]:
 A=norm(g.native(mask,3)[0],1);ai=adj(A);ai2=pw(ai,2);phase=[]
 for x in range(8):
  u,v,w=[x>>j&1 for j in range(3)];phase.append(2*(((J+1)*u+v+w+B*(u*v+u*w)+u*v*w)%2))
 T=mono([0,1,4,5,2,3,6,7],phase);assert mul(T,T)==I
 lhs=mul(mul(T,ai),adj(T));rhs=norm([[g.mul((0,-1),z) for z in row] for row in mat(A)],A[0]);assert lhs==rhs
 assert lhs!=A and mul(mul(mono([0,1,4,5,2,3,6,7]),ai),mono([0,1,4,5,2,3,6,7]))!=rhs
 inverse.append({'mask':mask,'input_phase':phase,'involution':True,'inverse_phase':'-i'})
 KI=[[one(ai),padd(one(ai),one(ai2,-1)),{}],[{},one(ai,-1),one(I)],[one(ai),one(ai2,-1),{}]]
 for label,targets in [('literal',[pw(A,3),pw(A,2),pw(A,2)]),('canonical',[mul(mul(C[0],C[1]),C[2]),mul(C[0],C[1]),mul(C[0],C[1])]),('baseline',[pw(A,2)]*3)]:
  DD=[[one(targets[i]) if i==j else {} for j in range(3)] for i in range(3)]
  BB=blockmul(blockmul(KI,DD),KI);equations=[]
  for row in BB:
   reps=[];eq=[]
   for j,cell in enumerate(row):
    for word,coef in cell.items():
     if ordinary(word):continue
     for k,rep in enumerate(reps):
      h=mul(adj(rep),word)
      if ordinary(h):break
     else:k=len(reps);reps.append(word);eq.append([{} for _ in range(3)]);h=I
     eq[k][j]=padd(eq[k][j],one(h,coef))
   equations.extend(eq)
  if label=='baseline':
   assert all(not row[1] for row in equations);continue
  record=next(c for c in certs if c['mask']==mask and c['endpoint']==label)
  expected=fromjson(record['constraint_matrix']);assert equations==expected
  E=fromjson(record['left_inverse']);assert blockmul(E,equations)==[[one(I) if i==j else {} for j in range(3)] for i in range(3)]
  assert len(equations)==(5 if label=='literal' else 11)
  if label=='canonical':assert [equations[i] for i in [4,1,7]]==[[one(I),{},{}],[{},one(I,-1),{}],[{},{},one(I,-1)]]
  cases.append({'mask':mask,'endpoint':label,'coset_equations':len(equations),'formal_left_inverse':True})
# Universal two-native formulas are checked as noncommutative word polynomials.
def wmul(X,Y):
 Z=[[{} for _ in Y[0]] for _ in X]
 for i,j,k in itertools.product(range(len(X)),range(len(Y[0])),range(len(Y))):
  for u,c in X[i][k].items():
   for v,d in Y[k][j].items():Z[i][j][u+v]=Z[i][j].get(u+v,0)+c*d
 return [[{w:c for w,c in cell.items() if c} for cell in row] for row in Z]
def word(s,c=1):return {tuple(s):c}
N0=[[word('a'),{}],[word(''),word('a')]];N2=[[word('b'),word('bb',-1)],[{},word('b')]];P=[[word('u'),word('v')],[word('w'),word('z')]]
M=wmul(wmul(N0,P),N2)
assert M[1][0]=={tuple('ub'):1,tuple('awb'):1}
assert M[1][1]=={tuple('ubb'):-1,tuple('awbb'):-1,tuple('vb'):1,tuple('azb'):1}
out={'status':'PASS_INDEPENDENT_INVERSE_AND_COSET_REVIEW','engine_sha256':hashlib.sha256(a.engine.read_bytes()).hexdigest(),'certificate_sha256':hashlib.sha256(a.certificates.read_bytes()).hexdigest(),'inverse_tables':inverse,'fixed_boundary_cases':cases,'two_native_formal_block_expansion':True,'scope':'Fixed tables and eventual tensor-faithful algebra; no profitable caller or new kappa'}
a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(out,indent=2)+'\n');print(out['status'])
