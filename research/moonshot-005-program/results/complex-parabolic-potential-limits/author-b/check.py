#!/usr/bin/env python3
"""Exact finite enumeration, independent of all prior research code."""
from collections import Counter,deque
from itertools import combinations
from pathlib import Path
import argparse,hashlib,json

def sp(u,v):return (((u&7)&(v>>3)).bit_count()+((v&7)&(u>>3)).bit_count())&1
def span(vs):
 s={0}
 for v in vs:s|={x^v for x in tuple(s)}
 return tuple(sorted(s-{0}))
def dist(L):
 k=1+sum((v&7)==0 for v in L);assert k in(1,2,4,8)
 return 3-(k.bit_length()-1)
def linear(cols,v):
 z=0
 for j in range(6):
  if v>>j&1:z^=cols[j]
 return z
def swap(r):
 a=[1<<j for j in range(6)]
 for i in range(r):a[i],a[i+3]=a[i+3],a[i]
 return a

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',default='RESULT.json');ap.add_argument('--spaces-out',default='LAGRANGIANS.json');args=ap.parse_args()
 spaces=set();bases=0
 for u,v,w in combinations(range(1,64),3):
  if w==u^v or sp(u,v) or sp(u,w) or sp(v,w):continue
  L=span((u,v,w));assert len(L)==7;spaces.add(L);bases+=1
 Ls=sorted(spaces);ix={L:i for i,L in enumerate(Ls)};ds=list(map(dist,Ls));Z=span((8,16,32))
 assert len(Ls)==135 and bases==3780 and Counter(ds)=={0:1,1:14,2:56,3:64}
 gens=[]
 for i in range(3):
  a=[1<<j for j in range(6)];a[i]^=1<<(i+3);gens.append(a)
 for i,j in combinations(range(3),2):
  a=[1<<k for k in range(6)];a[i]^=1<<(j+3);a[j]^=1<<(i+3);gens.append(a)
 for i in range(3):
  for j in range(3):
   if i==j:continue
   a=[1<<k for k in range(6)];a[i]^=1<<j;a[j+3]^=1<<(i+3);gens.append(a)
 def perm(g):return [ix[tuple(sorted(linear(g,v) for v in L))] for L in Ls]
 ps=[]
 for g in gens:
  assert all(sp(g[i],g[j])==sp(1<<i,1<<j) for i in range(6) for j in range(6))
  assert tuple(sorted(linear(g,v) for v in Z))==Z
  p=perm(g);assert len(set(p))==135 and all(ds[i]==ds[p[i]] for i in range(135));ps.append(p)
 rem=set(range(135));orbits=[]
 while rem:
  seed=min(rem);seen={seed};todo=deque([seed])
  while todo:
   i=todo.popleft()
   for p in ps:
    j=p[i]
    if j not in seen:seen.add(j);todo.append(j)
  rem-=seen;assert len({ds[i] for i in seen})==1;orbits.append(sorted(seen))
 assert sorted(map(len,orbits))==[1,14,56,64]
 for v in range(1,64):
  co=[set(L) for L in Ls if v in L];assert len(co)==15 and set.intersection(*co)=={v}
 reps=[swap(r) for r in range(4)];rp=list(map(perm,reps));table=[]
 for mask in range(8):
  plus={0}|{j for j in(1,2,3) if mask>>(j-1)&1};S={i for i,d in enumerate(ds) if d in plus};hs=[]
  for p in rp:
   n=len(S^{p[i] for i in S});assert n%2==0;hs.append(n//2)
   T=set(range(135))-S;assert n==len(T^{p[i] for i in T})
  _,h1,h2,h3=hs;assert h2<=h1 and 4*h3<=5*h1 and((h1==0)==(mask==7))
  table.append({'plus_shells':sorted(plus),'h':hs,'rank2_deficit':2*h1-h2,'rank3_deficit':3*h1-h3})
 k=next(i for i,d in enumerate(ds) if d==1);assert any(p[k]!=k for p in ps)
 S=set(Z);pauli=[len(S^{linear(g,v) for v in S})//2 for g in reps];assert pauli==[0,4,6,7]
 assert all(2*r['h'][2]<=3*r['h'][1] and 4*r['h'][3]<=7*r['h'][1] for r in table)
 w1=swap(1);w2=[1<<j for j in range(6)];w2[1],w2[4]=w2[4],w2[1]
 trans=lambda g,L:tuple(sorted(linear(g,v) for v in L))
 tuples=[]
 for L in [span((8,16,32)),span((8,16,4)),span((8^16,32,1^2))]:
  assert L in ix;tuples.append([dist(L),dist(trans(w1,L)),dist(trans(w2,L)),dist(trans(w1,trans(w2,L)))])
 assert tuples==[[0,1,1,2],[1,2,2,3],[1,2,2,1]]
 cert={'coordinate_order':['x1','x2','x3','z1','z2','z3'],'reference':list(Z),'lagrangians':[list(L) for L in Ls],'distance':ds,'H_generators':gens,'rank_representatives':reps}
 cp=Path(args.spaces_out);cp.write_text(json.dumps(cert,indent=2)+'\n')
 out={'status':'SCOPED_FAILURE_OF_FULL_H_RADIAL_LAGRANGIAN_SIGN_CUTS','lagrangians':135,'unordered_isotropic_bases':bases,'shell_sizes':[1,14,56,64],'H_generators':12,'H_orbits':sorted(map(len,orbits)),'H_order':10752,'faithful_group_action_line_checks':63,'cut_table':table,'cone_separator':['h2 <= h1','4 h3 <= 5 h1'],'pauli63_cut':pauli,'combined_separator':['2 h2 <= 3 h1','4 h3 <= 7 h1'],'hilbert_three_space_tuples':tuples,'controls':['135 isotropic spaces enumerated','12 generators symplectic and Z preserving','four full H orbits','63 line recovery intersections','cut complements agree','nonradial singleton fails H invariance','constant cut zero','rank representatives preserve spaces'],'certificate_sha256':hashlib.sha256(cp.read_bytes()).hexdigest(),'scope':'Only the stated permutation representation and potential families. No general caller obstruction and no new kappa.'}
 Path(args.out).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
