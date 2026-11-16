"""Independent exact sixteen-column source, inverse, kernel and invoice audit."""
from pathlib import Path
import argparse,hashlib,importlib.util,json
p=argparse.ArgumentParser();p.add_argument('--engine',type=Path,required=True);p.add_argument('--price-engine',type=Path,required=True);p.add_argument('--proof',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
g=load('root_exact',a.engine);b=load('root_price',a.price_engine)
mm=g.mm;N=16;I=g.mono(list(range(N)));bits=lambda x:tuple((x>>j)&1 for j in range(4))
def mon(f,h):return g.mono([f(*bits(x)) for x in range(N)],[h(*bits(x))%4 for x in range(N)])
def pw(M,k):
 v=I
 for _ in range(k):v=mm(v,M)
 return v
def adj(M):return [[(M[j][i][0],-M[j][i][1]) for j in range(len(M))] for i in range(len(M))]
def scal(M,z):return [[g.mul(z,v) for v in row] for row in M]
C=[g.gaussian(j,4) for j in range(4)]
P=mon(lambda u,v,w,z:v+2*w+4*z+8*u,lambda *x:0)
S=mon(lambda u,v,w,z:v+2*w+4*z+8*u,lambda u,v,w,z:2*u*v*z)
A=mm(C[1],S);A2=pw(A,2);A3=pw(A,3);A4=pw(A,4)
R=mon(lambda u,v,w,z:u+2*v+4*(w^(u*v))+8*z,lambda u,v,w,z:u*v*(1+2*w+2*z))
L=mon(lambda u,v,w,z:u+2*(v^(w*z))+4*w+8*z,lambda u,v,w,z:w*z*(2*u+2*v-1))
J=mon(lambda u,v,w,z:(u^(w*z))+2*v+4*w+8*z,lambda u,v,w,z:w*z)
R2=mm(J,pw(S,2));G2=mm(C[0],C[1]);G4=mm(mm(G2,C[2]),C[3]);B=mm(G2,pw(P,2))
assert R2==mm(pw(P,2),R) and pw(R,2)==pw(L,2)==I
assert A2==mm(G2,R2) and A4==mm(mm(L,G4),R)
assert mm(mm(adj(S),C[0]),R2)==A and pw(B,2)==G4
assert mm(mm(B,R),adj(B))==scal(L,(16,0))
T=mon(lambda u,v,w,z:z+2*w+4*v+8*u,lambda u,v,w,z:2*(u+v+w+z))
assert pw(T,2)==I and mm(mm(T,adj(A)),T)==scal(A,(0,-1))
# Derive every A^4 coefficient directly from its four successive unique paths.
for x in range(N):
 u,v,w,z=bits(x)
 for y in range(N):
  aa,bb,cc,dd=bits(y)
  parity=(u*v*z+u*v*cc+v*cc*dd+aa*cc*dd)%2
  q=-((u^aa)+(v^bb)+(w^cc)+(z^dd))+2*parity
  assert A4[y][x]==g.scale(g.UNIT[q%4],-4)
trace=tuple(sum(A3[j][j][k] for j in range(N)) for k in range(2));assert trace==(12,-12)
assert A4!=mm(mm(mon(lambda u,v,w,z:u+2*(v^(w*z))+4*w+8*z,lambda *x:0),G4),mon(lambda u,v,w,z:u+2*v+4*(w^(u*v))+8*z,lambda *x:0))
assert A4!=mm(L,G4) and A4!=mm(G4,R) and pw(mm(C[1],P),4)!=A4
assert mm(mm(T,adj(A)),T)!=A
# Universal concentration checked in the integer polynomial ring, with no matrix assumptions.
def mul(X,Y):
 out=[[{} for _ in Y[0]] for _ in X]
 for i in range(len(X)):
  for j in range(len(Y[0])):
   for k in range(len(Y)):
    for u,c in X[i][k].items():
     for v,d in Y[k][j].items():out[i][j][u+v]=out[i][j].get(u+v,0)+c*d
 return [[{k:v for k,v in c.items() if v} for c in row] for row in out]
L0=[[{1:1},{}],[{0:1},{1:1}]];U2=[[{1:1},{2:-1}],[{},{1:1}]]
assert mul(mul(L0,U2),L0)==[[{},{4:-1}],[{2:1},{}]]
profiles={'42_two_roles':{25:1,23:1,1:-3,7:-3,8:-3},'43_two_roles':{25:1,24:1,1:-3,7:-3,8:-3},'421_three_roles':{25:1,23:1,22:1,1:-3,7:-6,8:-3},'422_three_roles':{25:1,23:2,1:-3,7:-6,8:-3}}
prices={}
for name,profile in profiles.items():
 lo,hi=b.moment(profile);prices[name]={'lower':str(lo),'upper':str(hi)}
 assert (hi<0 if name=='42_two_roles' else lo>0)
result={'status':'PASS_INDEPENDENT_FOUR_BIT_SOURCE_AND_CONCENTRATION','proof_sha256':hashlib.sha256(a.proof.read_bytes()).hexdigest(),'matrix_dimension':16,'fourth_kernel_entries':256,'cube_trace':'3(1-i)/2','exact_square_and_fourth_gauges':True,'fresh_inverse_phase':'-i','generic_LUL_concentration':True,'negative_controls':5,'gaussian_margin_intervals':prices,'scope':'All-width identities by tensoring exact base matrices; generic LUL block identity over any associative unital algebra. No profitable caller, complete supplier, or new kappa.'}
a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,indent=2)+'\n');print(result['status'])
