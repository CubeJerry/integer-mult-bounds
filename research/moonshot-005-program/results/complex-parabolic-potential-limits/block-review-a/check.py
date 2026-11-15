#!/usr/bin/env python3
"""Independent closure enumeration and rank-metric audit; imports no author code."""
import argparse, hashlib, itertools, json
from pathlib import Path

def sp(a,b):return (((a&7)&(b>>3)).bit_count()+((a>>3)&(b&7)).bit_count())&1

def swap(v,r):
 for j in range(r):
  if ((v>>j)^(v>>(j+3)))&1:v^=(1<<j)|(1<<(j+3))
 return v

def rank(a,p):
 a=[list(r) for r in a];n=len(a);m=len(a[0]) if a else 0;k=0
 for j in range(m):
  q=next((i for i in range(k,n) if a[i][j]%p),None)
  if q is None:continue
  a[k],a[q]=a[q],a[k];inv=pow(a[k][j]%p,-1,p);a[k]=[(x*inv)%p for x in a[k]]
  for i in range(n):
   if i!=k:
    c=a[i][j]%p;a[i]=[(x-c*y)%p for x,y in zip(a[i],a[k])]
  k+=1
 return k

def diff_rank(a,b,p):return rank([[x-y for x,y in zip(r,s)]for r,s in zip(a,b)],p)

def partitions(xs):
 if not xs:yield [];return
 for q in partitions(xs[1:]):
  yield [[xs[0]]]+q
  for j in range(len(q)):yield q[:j]+[[xs[0]]+q[j]]+q[j+1:]

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--author','--source',dest='author',type=Path,required=True);ap.add_argument('--diagonal',type=Path);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.diagonal=a.diagonal or a.author.parent/'independent-c';a.out.mkdir(parents=True,exist_ok=True)
 assert hashlib.sha256((a.author/'PROOF.md').read_bytes()).hexdigest()=='d17f439fec8a24f75ba6402f8bc32a7a213ee11dcc30afb5408b14f31b120959'
 # Every isotropic subspace grows by adjoining a perpendicular new vector.
 levels=[{frozenset([0])}]
 for d in range(3):
  nxt=set()
  for s in levels[-1]:
   for v in range(1,64):
    if v not in s and all(not sp(u,v)for u in s):nxt.add(s|frozenset(u^v for u in s))
  levels.append(nxt)
 assert [len(s)for s in levels]==[1,63,315,135]
 spaces=sorted(levels[3],key=lambda s:tuple(sorted(s)));Z=frozenset(range(8));dist=lambda s:3-((len(s&Z)).bit_length()-1)
 assert [sum(dist(s)==d for s in spaces)for d in range(4)]==[1,14,56,64]
 generators=[]
 for i in range(3):
  for j in range(3):
   if i!=j:generators.append(tuple(v^(((v>>j)&1)<<i)^(((v>>(i+3))&1)<<(j+3))for v in range(64)))
 for i in range(3):
  for j in range(i,3):generators.append(tuple(v^(((v>>(j+3))&1)<<i)^(0 if i==j else(((v>>(i+3))&1)<<j))for v in range(64)))
 for g in generators:
  assert {g[v]for v in Z}==set(Z)
  assert all(sp(u,v)==sp(g[u],g[v])for u in range(64)for v in range(64))
 unseen=set(spaces);orbits=[]
 while unseen:
  start=min(unseen,key=lambda s:tuple(sorted(s)));o={start};todo=[start]
  while todo:
   s=todo.pop()
   for g in generators:
    t=frozenset(g[v]for v in s)
    if t not in o:o.add(t);todo.append(t)
  unseen-=o;orbits.append((dist(start),len(o)));assert len({dist(s)for s in o})==1
 assert sorted(orbits)==[(0,1),(1,14),(2,56),(3,64)]
 N=[]
 for r in range(4):
  n=[[0]*4 for _ in range(4)]
  for s in spaces:n[dist(s)][dist(frozenset(swap(v,r)for v in s))]+=1
  assert n==[list(c)for c in zip(*n)];N.append(n)
 expected=[[[1,0,0,0],[0,14,0,0],[0,0,56,0],[0,0,0,64]],[[0,1,0,0],[1,1,12,0],[0,12,12,32],[0,0,32,32]],[[0,0,1,0],[0,3,3,8],[1,3,28,24],[0,8,24,32]],[[0,0,0,1],[0,0,7,7],[0,7,21,28],[1,7,28,28]]]
 assert N==expected
 assert N==json.loads((a.diagonal/'TABLE.json').read_text())['orbit_intersection_matrices']
 pairs=list(itertools.combinations(range(4),2));coefs=[[n[i][j]for i,j in pairs]for n in N]
 assert [x-y for x,y in zip(coefs[1],coefs[2])]==[1,-1,0,9,-8,8]
 assert [5*x-4*y for x,y in zip(coefs[1],coefs[3])]==[5,0,-4,32,-28,48]
 def audit(delta):
  assert all(delta[i][k]<=delta[i][j]+delta[j][k]for i in range(4)for j in range(4)for k in range(4))
  q=[sum(n[i][j]*delta[i][j]for i,j in pairs)for n in N]
  s1=delta[0][1]+delta[1][2]-delta[0][2]+8*(delta[1][2]+delta[2][3]-delta[1][3])
  s3=4*(delta[0][1]+delta[1][2]+delta[2][3]-delta[0][3])+28*(delta[1][2]+delta[2][3]-delta[1][3])+delta[0][1]+16*delta[2][3]
  assert q[1]-q[2]==s1>=0 and 5*q[1]-4*q[3]==s3>=0
  assert (q[1]==0)==all(x==0 for row in delta for x in row)
  return [2*v for v in q]
 matrices=[[[aa,b],[c,d]]for aa,b,c,d in itertools.product(range(2),repeat=4)];ds=[[diff_rank(x,y,2)for y in matrices]for x in matrices]
 for ids in itertools.product(range(16),repeat=4):audit([[ds[i][j]for j in ids]for i in ids])
 for seed in range(512):
  state=seed+1;ms=[]
  for t in range(4):
   vals=[]
   for x in range(9):state=(1103515245*state+12345)%2147483648;vals.append(state%3)
   ms.append([vals[0:3],vals[3:6],vals[6:9]])
  audit([[diff_rank(x,y,3)for y in ms]for x in ms])
 ps=list(partitions(list(range(4))));assert len(ps)==15;scalar=[]
 for p in ps:
  labels=[next(k for k,b in enumerate(p)if i in b)for i in range(4)];delta=[[int(x!=y)for y in labels]for x in labels];R=audit(delta)
  for r in range(4):
   cuts=0
   for k in range(len(p)):
    S={s for s in spaces if labels[dist(s)]==k};image={frozenset(swap(v,r)for v in s)for s in S};assert len(S^image)%2==0;cuts+=len(S^image)//2
   assert cuts==R[r]
  scalar.append({'partition':sorted([sorted(b)for b in p]),'ranks':R})
 author_scalar=json.loads((a.diagonal/'DIAGONAL-RESULT.json').read_text())
 def keyed(items,pk,rk):return {tuple(map(tuple,sorted([sorted(b)for b in v[pk]]))):v[rk]for v in items}
 assert keyed(scalar,'partition','ranks')==keyed(author_scalar['cases'],'orbit_partition','commutator_ranks')
 unseen=set(range(1,64));po=[]
 while unseen:
  v=min(unseen);o={v};todo=[v]
  while todo:
   u=todo.pop()
   for g in generators:
    w=g[u]
    if w not in o:o.add(w);todo.append(w)
  unseen-=o;po.append(o)
 assert sorted(map(len,po))==[7,56]
 pauli=[len((set(range(1,8)))^{swap(v,r)for v in range(1,8)})//2 for r in range(4)];assert pauli==[0,4,6,7]
 bad=[[0]*4 for _ in range(4)];bad[0][2]=bad[2][0]=1
 assert sum(N[2][i][j]*bad[i][j]for i,j in pairs)>sum(N[1][i][j]*bad[i][j]for i,j in pairs)
 s=next(s for s in spaces if dist(s)==1);assert any(frozenset(g[v]for v in s)!=s for g in generators)
 result={'status':'INDEPENDENT_BLOCK_RADIAL_REVIEW_PASS','isotropic_subspace_counts':[len(s)for s in levels],'orbit_sizes':[1,14,56,64],'intersection_matrices':N,'q_coefficients_pair_order':pairs,'q_coefficients':coefs,'exhaustive_F2_2x2_matrix_quadruples':16**4,'F3_3x3_matrix_quadruples':512,'scalar_equality_patterns':15,'scalar_level_set_identity':'Verified combinatorially for all 15 equality patterns; universal proof reviewed.','Pauli_point_orbit_sizes':[7,56],'Pauli_half_crossings':pauli,'controls':['constant blocks give zero','nonmetric shell assignment reverses R2<=R1','nonradial singleton fails H invariance','all 15 scalar equality patterns agree with independent C certificate'],'scope':'All fields and all finite block widths follow from the rank pseudometric proof, not finite matrix tests. Block diagonal shell-constant operators only; off-diagonal intertwiners remain open. No new kappa.'}
 (a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'])
if __name__=='__main__':main()
