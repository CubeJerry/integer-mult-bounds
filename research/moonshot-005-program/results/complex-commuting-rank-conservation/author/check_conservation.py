#!/usr/bin/env python3
"""Exact controls for all-call Pauli-split rank conservation; not its proof."""
import argparse,hashlib,importlib.util,itertools,json,random,sys
from fractions import Fraction as F
from pathlib import Path

def det(a):
 n=len(a)
 if n==1:return a[0][0]
 if n==2:return a[0][0]*a[1][1]-a[0][1]*a[1][0]
 if n==3:return sum((1 if p in [(0,1,2),(1,2,0),(2,0,1)] else -1)*a[0][p[0]]*a[1][p[1]]*a[2][p[2]] for p in itertools.permutations(range(3)))
 b=[[F(x) for x in r] for r in a];z=F(1)
 for j in range(n):
  p=next((i for i in range(j,n) if b[i][j]),None)
  if p is None:return 0
  if p!=j:b[j],b[p]=b[p],b[j];z=-z
  v=b[j][j];z*=v
  for i in range(j+1,n):
   t=b[i][j]/v
   for k in range(j+1,n):b[i][k]-=t*b[j][k]
 return z

def rank(a):
 n=len(a)
 if n==3:
  if det(a):return 3
  if any(a[i][k]*a[j][l]-a[i][l]*a[j][k] for i,j in itertools.combinations(range(3),2) for k,l in itertools.combinations(range(3),2)):return 2
  return int(any(x for r in a for x in r))
 b=[[F(x) for x in r] for r in a];r=0
 for j in range(n):
  p=next((i for i in range(r,n) if b[i][j]),None)
  if p is None:continue
  b[r],b[p]=b[p],b[r];v=b[r][j]
  for i in range(r+1,n):
   t=b[i][j]/v
   for k in range(j,n):b[i][k]-=t*b[r][k]
  r+=1
 return r

def eye(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def mm(a,b):return [[sum(a[i][k]*b[k][j] for k in range(len(a))) for j in range(len(a))] for i in range(len(a))]
def sub(a,b):return [[x-y for x,y in zip(r,s)] for r,s in zip(a,b)]
def proofpin(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rounding(M):
 n=len(M);signs=list(itertools.product([-1,1],repeat=n));ds=[]
 for c in signs:ds.append(det([[int(i==j)+c[i]*M[i][j] for j in range(n)] for i in range(n)]))
 assert sum(ds)==2**n
 c=next(c for c,d in zip(signs,ds) if d)
 for d in signs:
  r=rank([[M[i][j]-int(i==j)*d[i] for j in range(n)] for i in range(n)])
  assert sum(x!=y for x,y in zip(c,d))<=r
 return c

def word(factors,signs):
 z=eye(3)
 for u,v,ori,P in factors:
  a,b=signs[u-1],signs[v-1]
  N=[[a,1,0],[0,b,0],[0,0,1]] if not ori else [[a,-a*b,0],[0,b,0],[0,0,1]]
  z=mm(mm(z,N),P)
 return z

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=Path.cwd());ap.add_argument('--out',type=Path,default=Path(__file__).with_name('CONSERVATION-RESULT.json'));ar=ap.parse_args();base=Path(__file__).parent
 checked=0
 for xs in itertools.product([-1,0,1],repeat=9):
  rounding([list(xs[i:i+3]) for i in [0,3,6]]);checked+=1
 rng=random.Random(20261115)
 for n in [1,2,4,5]:
  for t in range(40):rounding([[rng.randrange(-3,4) for _ in range(n)] for _ in range(n)])
 # A fixed arbitrary sign vector does not work: M=-I and D=-I.
 Mneg=[[-int(i==j) for j in range(3)] for i in range(3)];Dneg=Mneg
 assert det([[int(i==j)+Mneg[i][j] for j in range(3)] for i in range(3)])==0
 assert rank(sub(Mneg,Dneg))==0 and sum(1!=-1 for _ in range(3))==3
 # No sign centre is within Hamming distance one of all four even diagonals.
 even=[d for d in itertools.product([-1,1],repeat=3) if d[0]*d[1]*d[2]==1]
 assert all(any(sum(x!=y for x,y in zip(c,d))>1 for d in even) for c in itertools.product([-1,1],repeat=3))
 flips=0
 for m in range(1,8):
  for t in range(20):
   factors=[];counts=[0]*7
   for j in range(m):
    u,v=rng.sample(range(1,8),2);counts[u-1]+=1;counts[v-1]+=1;P=eye(3)
    for _ in range(2):
     i,k=rng.sample(range(3),2);E=eye(3);E[i][k]=rng.choice([-1,1]);P=mm(P,E)
    factors.append((u,v,rng.randrange(2),P))
   eta=[1]*6+[-1];W=word(factors,eta)
   for v in range(7):
    xi=eta.copy();xi[v]*=-1
    assert rank(sub(W,word(factors,xi)))<=counts[v];flips+=1
 # Actual U(a), ordinary gauges, all 42 ordered pairs.
 hp=ar.repo/'research/moonshot-005-program/results/complex-nonordinary-row-seed/worker-b/check.py';expected='1d3c798c43b46e1983f4dc80d68e694b93d9cdee206ad4fe4d408e5f5e29ed91';assert proofpin(hp)==expected
 spec=importlib.util.spec_from_file_location('conservation_dyadic',hp);dy=importlib.util.module_from_spec(spec);sys.modules[spec.name]=dy;spec.loader.exec_module(dy)
 I=dy.eye(8);Z=dy.zero(8);S=dy.monomial([0,4,1,5,2,6,3,7],[0]*8);Si=S.star();X={v:dy.monomial([x^v for x in range(8)],[0]*8) for v in range(8)};C={v:dy.M((I.scale((1,1))+X[v].scale((1,-1))).a,1).norm() for v in range(1,8)};a=C[2]@S;U=dy.block([[a,(a@a).scale((-1,0))],[Z,a]])
 def binary_rank(vs):
  p={}
  for v in vs:
   while v:
    j=v.bit_length()-1
    if j not in p:p[j]=v;break
    v^=p[j]
  return len(p)
 def app(cs,x):
  y=0
  for j,c in enumerate(cs):
   if (x>>j)&1:y^=c
  return y
 for u,w in itertools.permutations(range(1,8),2):
  t=next(t for t in range(1,8) if binary_rank([w,u,t])==3);H=dy.monomial([app((w,u,t),x) for x in range(8)],[0]*8)
  L=dy.diagonal([H,X[u]@H@S]);R=dy.diagonal([Si@H.star()@X[u],Si@Si@H.star()@X[u]@X[w]])
  Cu=C[u].star();Cw=C[w].star();target=dy.block([[Cu,(Cu@Cw).scale((-1,0))],[Z,Cw]])
  assert L@U@R==target
 out={'status':'PASS_EXACT_RANK_ROUNDING_AND_CONSERVATION_CONTROLS','exhaustive_ternary_3x3_matrices':checked,'additional_exact_matrices':160,'source_word_flip_checks':flips,'actual_inverse_split_gauges':42,'negative_controls':{'arbitrary_fixed_rounding_sign_rejected':True,'four_even_sign_diagonals_have_no_Hamming_radius_one_centre':True},'proof_pins':{f:proofpin(base/f) for f in ['COMMUTING-PHASE-CONSERVATION.md','INVERSE-SPLIT-SOURCE-GAUGE.md','PAULI-SPLIT-GAUGED-SOURCE.md']},'scope':'Universal claims are proved in the Markdown arguments; these exact controls cover the stated finite domains only. No synthesis, supplier or new kappa.','new_kappa':False}
 ar.out.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out))
if __name__=='__main__':main()
