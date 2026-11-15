#!/usr/bin/env python3
import importlib.util,sys,json
from pathlib import Path
here=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('author_matrices',here/'check.py');m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
def par(x):return x.bit_count()%2
def omega(x,y):return par((x&3)&(y>>2))^par((x>>2)&(y&3))
def act(g,x):
 y=0
 for k in range(4):
  if x>>k&1:y^=g[k]
 return y

def rank2(a,b):return int(a!=0)+int(b!=0 and b!=a)
def mul(g,h):return tuple(act(g,x) for x in h)
def invert(g):
 p=[act(g,v) for v in range(16)];return tuple(p.index(1<<j) for j in range(4))
def qp(t,v):return par((v&3)&(v>>2))^par(t&v)
odd=[t for t in range(16) if par((t&3)&(t>>2))];assert odd==[5,7,10,11,13,14]
truth={tuple(qp(t,v) for v in range(16)):i for i,t in enumerate(odd)}
def rho(g):
 gi=invert(g);return tuple(truth[tuple(qp(t,act(gi,v)) for v in range(16))] for t in odd)
def pmul(a,b):return tuple(a[j] for j in b)
def pinv(a):return tuple(a.index(i) for i in range(len(a)))
def cycles(p):
 seen=set();n=0
 for j in range(len(p)):
  if j in seen:continue
  n+=1
  while j not in seen:seen.add(j);j=p[j]
 return n
G=[]
for a in range(1,16):
 for b in range(1,16):
  if b==a or omega(a,b):continue
  for c in range(1,16):
   if omega(a,c)!=1 or omega(b,c):continue
   for d in range(1,16):
    if omega(a,d) or omega(b,d)!=1 or omega(c,d):continue
    G.append((a,b,c,d))
assert len(G)==len(set(G))==720
H=[g for g in G if not(g[2]&3 or g[3]&3)];assert len(H)==48
T=tuple(next(j for j,u in enumerate(odd) if u!=t and u>>2==t>>2) for t in odd);assert T==(1,0,3,2,5,4)
census={};rs={g:rho(g) for g in G}
for g in G:
 p=rs[g];r=rank2(g[2]&3,g[3]&3);diff=6-cycles(pmul(pinv(p),pmul(T,pmul(p,T))))
 assert diff==2*r;census[(r,diff)]=census.get((r,diff),0)+1
 if g in H:assert pmul(p,T)==pmul(T,p)
gens=[tuple((1<<j)^(v if omega(v,1<<j) else 0) for j in range(4)) for v in [1,2,4,8,5,10]]
for g in G:
 for h in gens:assert rs[mul(g,h)]==pmul(rs[g],rs[h])
I=m.eye(4);X={x:m.monomial([j^x for j in range(4)],[0]*4) for x in range(4)}
Z={z:m.monomial(list(range(4)),[2*par(z&j) for j in range(4)]) for z in range(4)}
pauli={x+4*z:X[x]@Z[z] for x in range(4) for z in range(4)};units=[(1,0),(-1,0),(0,1),(0,-1)]
def symp(u):
 ans=[]
 for j in range(4):
  image=u@pauli[1<<j]@u.star();found=[v for v,p in pauli.items() if any(image==p.scale(c) for c in units)]
  assert len(found)==1;ans.append(found[0])
 return tuple(ans)
qb=m.M((I.scale((1,1))+X[2].scale((1,-1))).a,1).norm();s=m.monomial([0,3,1,2],[0,2,0,0]);b=(qb@s).scale(m.II);gb=symp(b)
assert gb in G and gb==(13,11,10,14)
ordinary={}
for name,u in {'S':s,'G1':s.scale(m.II),'G2':m.monomial([0,3,2,1],[2,1,1,2]),'H2':m.monomial([0,2,3,1],[3,3,3,1]),'T':m.monomial([1,0,2,3],[0,0,2,0])}.items():
 gu=symp(u);assert gu in H;ordinary[name]={'symplectic_columns':gu,'odd_form_permutation':rs[gu]}
# Six-dimensional permutation representation and exact rational ranks.
from fractions import Fraction

def ident(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def mat(p):return [[int(i==p[j]) for j in range(len(p))] for i in range(len(p))]
def mm(a,b):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def minus(a,b):return [[x-y for x,y in zip(r,s)] for r,s in zip(a,b)]
def scale(a,c):return [[c*x for x in r] for r in a]
def pw(a,k):
 out=ident(len(a))
 for _ in range(k):out=mm(out,a)
 return out

def rank(a):
 a=[[Fraction(x) for x in row] for row in a];n=0
 for c in range(len(a[0])):
  k=next((k for k in range(n,len(a)) if a[k][c]),None)
  if k is None:continue
  a[n],a[k]=a[k],a[n];v=a[n][c];a[n]=[x/v for x in a[n]]
  for k in range(n+1,len(a)):
   v=a[k][c]
   if v:a[k]=[x-v*y for x,y in zip(a[k],a[n])]
  n+=1
 return n

def block(a,b,c,d):return [x+y for x,y in zip(a,b)]+[x+y for x,y in zip(c,d)]
P=mat(T);U=mat(rs[gb]);zero=[[0]*6 for _ in range(6)];P2=block(P,zero,zero,P);ns=[]
for sig in [-1,1]:
 for eps in [-1,1]:
  for c in [-1,1]:
   x=pw(U,sig%5);y=scale(pw(U,(sig+eps)%5),c);native=block(x,y,zero,x)
   dr=rank(minus(native,mm(mm(P2,native),P2)));assert dr==4;ns.append([sig,eps,c,dr])
# Diagonal signs cannot replace the non-diagonal matching involution.
wrong=[[int(i==j)*(1 if i<3 else -1) for j in range(6)] for i in range(6)]
assert any(mm(wrong,mat(rs[g]))!=mm(mat(rs[g]),wrong) for g in H)
out={'status':'PASS_INDEPENDENT_FULL_TWO_HEAD_CLIFFORD_RANK_REPRESENTATION','arithmetic':'Python integers, Gaussian dyadics and Fraction elimination','symplectic_elements':720,'ordinary_stabilizer':48,'odd_quadratic_parameters':odd,'matching_permutation':T,'rank_difference_census':[{'gaussian_rank':r,'difference_rank':d,'count':n} for (r,d),n in sorted(census.items())],'homomorphism_generator_products':len(G)*len(gens),'actual_B_symplectic_columns':gb,'actual_B_odd_form_permutation':rs[gb],'actual_ordinary_gauges':ordinary,'native_orientation_checks':ns,'wrong_diagonal_cut_rejected':True,'phase_handling':'Universal proof tensors both auxiliary representations with the same physical g^tensor V; exact central phase and every residue retained.','scope':'Full finite two-head monomial Clifford ordinary family, independent complete endpoints, common fresh body. No general multiplication lower bound.','new_kappa':False}
(here/'FULL-CLIFFORD-RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
