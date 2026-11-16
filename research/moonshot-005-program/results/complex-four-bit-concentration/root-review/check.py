"""Independent noncommutative block identities for the concentration boundary."""
from pathlib import Path
import argparse,hashlib,importlib.util,json
p=argparse.ArgumentParser();p.add_argument('--proof',type=Path,required=True);p.add_argument('--price-engine',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
def w(*letters,c=1):return {letters:c}
def plus(A,B):
 z=dict(A)
 for k,v in B.items():z[k]=z.get(k,0)+v
 return {k:v for k,v in z.items() if v}
def mul(X,Y):
 z=[[{} for _ in Y[0]] for _ in X]
 for i in range(len(X)):
  for j in range(len(Y[0])):
   for k in range(len(Y)):
    for u,c in X[i][k].items():
     for v,d in Y[k][j].items():z[i][j]=plus(z[i][j],{u+v:c*d})
 return z
def scalar(M):return [[w(c=v) if v else {} for v in row] for row in M]
I=scalar([[1,0,0],[0,1,0],[0,0,1]])
L=[[w('a'),{},{}],[w(),w('a'),{}],[{},{},w()]];U=[[w('a'),w('a','a',c=-1),{}],[{},w('a'),{}],[{},{},w()]]
target=[[{},w('a','a','a','a',c=-1),{}],[w('a','a'),{},{}],[{},{},w()]]
assert mul(mul(L,U),L)==target
T=scalar([[0,0,1],[1,0,-1],[1,1,-1]]);Ti=scalar([[1,1,0],[0,-1,1],[1,0,0]]);J=scalar([[0,1,0],[1,0,0],[0,0,1]]);P0=scalar([[1,1,0],[-1,0,1],[0,1,0]])
K0=[[w(),{},plus(w('a'),w(c=-1))],[w('a'),{},w('a',c=-1)],[w(),w(),w(c=-1)]]
K2=[[w('a','a',c=-1),{},plus(w('a'),w('a','a'))],[w('a'),{},w('a',c=-1)],[w(),w(),w(c=-1)]]
assert mul(T,Ti)==I and mul(Ti,J)==P0
M=J
for f in [K0,P0,K2,P0,K0,Ti,J]:M=mul(M,f)
assert M==target
Q=[[w('q'+str(i)+str(j)) for j in range(3)] for i in range(3)];M=mul(mul(mul(L,U),Q),L)
assert M[2]==[plus(w('q20','a'),w('q21')),w('q21','a'),w('q22')]
assert M[1][2]==w('a','q02') and M[0][2]==plus(w('a','a','q02'),w('a','a','a','q12',c=-1))
sp=importlib.util.spec_from_file_location('root_price',a.price_engine);b=importlib.util.module_from_spec(sp);sp.loader.exec_module(b)
profiles={'42':{25:1,23:1,1:-3,7:-3,8:-3},'420':{25:1,23:1,21:1,1:-3,7:-6,8:-3},'43_plus_query':{25:1,24:1,1:-4,7:-3,8:-3},'421_plus_query':{25:1,23:1,22:1,1:-4,7:-6,8:-3}}
prices={}
for k,v in profiles.items():
 lo,hi=b.moment(v);assert hi<0;prices[k]=[str(lo),str(hi)]
r={'status':'PASS_INDEPENDENT_CONCENTRATION_BLOCKS_AND_PRICES','proof_sha256':hashlib.sha256(a.proof.read_bytes()).hexdigest(),'generic_associative_LUL_identity':True,'generic_K_embedding':True,'noncommutative_last_interstage_entries':True,'negative_gaussian_margins':prices,'last_interstage_gate':'Independent written projection/rank proof in REVIEW.md; not inferred from computational search','new_complete_kappa':False};a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(r,indent=2)+'\n');print(r['status'])
