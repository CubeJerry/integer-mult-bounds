#!/usr/bin/env python3
"""Exact full-E8 A2^4 symmetry in the programme's nine-bit normal convention."""
from fractions import Fraction as F
from pathlib import Path
import json

def root(v):
 if v.bit_count()==3:return [2 if v>>i&1 else -1 for i in range(9)]
 o=[i for i in range(9)if not v>>i&1];assert len(o)==2
 return [3*(int(i==o[0])-int(i==o[1]))for i in range(9)]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def mm(A,B):return [[sum(x*y for x,y in zip(r,c))for c in zip(*B)]for r in A]
def tr(A):return list(map(list,zip(*A)))
def eye(n):return [[F(i==j)for j in range(n)]for i in range(n)]
Z=list(map(root,[7,25,42,52,76,82,97,127]));P=[v for v in range(512)if v.bit_count()in(3,7)];g={v:[F(dot(root(v),z),18)for z in Z]for v in P};lookup={tuple(s*x for x in g[v]):(v,s)for v in P for s in[-1,1]}
def find(planes,candidates):
 if len(planes)==4:return planes
 if len(candidates)<2:return
 a=min(candidates)
 for b in candidates:
  if a==b or abs(dot(g[a],g[b]))!=F(1,2):continue
  rest=[v for v in candidates if not dot(g[v],g[a])and not dot(g[v],g[b])]
  ans=find(planes+[(a,b)],rest)
  if ans:return ans
planes=find([],P);assert planes
R=eye(8)
for a,b in planes:
 A=[[F(i==j)-2*g[a][i]*g[a][j]for j in range(8)]for i in range(8)];B=[[F(i==j)-2*g[b][i]*g[b][j]for j in range(8)]for i in range(8)];R=mm(mm(R,A),B)
R2=mm(R,R);assert mm(R,tr(R))==eye(8)and all(R2[i][j]+R[i][j]+int(i==j)==0 for i in range(8)for j in range(8));permutation={};signs={}
for v in P:
 row=tuple(sum(R[i][j]*g[v][j]for j in range(8))for i in range(8));v2,sg=lookup[row];permutation[v]=v2;signs[v]=sg
assert all(permutation[permutation[permutation[v]]]==v and permutation[v]!=v for v in P)
def brank(vs):
 base={}
 for x in vs:
  while x:
   p=x.bit_length()-1
   if p in base:x^=base[p]
   else:base[p]=x;break
 return len(base)
basis=[]
for v in P:
 if brank(basis+[v])>len(basis):basis.append(v)
 if len(basis)==9:break
assert len(basis)==9
images=[permutation[v]for v in basis];mapping={0:0}
for v,w in zip(basis,images):mapping.update({x^v:y^w for x,y in list(mapping.items())})
assert len(mapping)==512 and all(mapping[v]==permutation[v]for v in P)
cols=[mapping[1<<i]for i in range(9)];rows=[sum(((cols[j]>>i)&1)<<j for j in range(9))for i in range(9)]
assert all(((cols[i]&cols[j]).bit_count()%2)==int(i==j)for i in range(9)for j in range(9))
assert all(mapping[mapping[x]]^mapping[x]^x==(511 if x.bit_count()%2 else 0)for x in range(512))
assert all(mapping[v]^mapping[mapping[v]]^v==511 and(v&mapping[v]).bit_count()%2==0 for v in P)
assert all(c.bit_count()%4==1 for c in cols)
seen=set();cycles=[]
for v in P:
 if v not in seen:
  cyc=[v,permutation[v],permutation[permutation[v]]];cycles.append(cyc);seen.update(cyc)
assert len(cycles)==40
out={'status':'PASS_EXACT_FULL_E8_EISENSTEIN_SYMMETRY','A2_planes':planes,'real_matrix':[[str(x)for x in r]for r in R],'binary_rows':rows,'binary_columns':cols,'basis_normals':basis,'cycles':cycles,'canonical_root_signs':signs,'all_cycles_pairwise_binary_orthogonal':True,'all_cycles_sum_to':511,'T2_plus_T_plus_I':'all-ones matrix','column_weights':[c.bit_count()for c in cols],'construction':'product of four mutually orthogonal A2 Coxeter rotations, generated from the same normalized E8 roots','no_caller_admission':True,'no_new_kappa':True};Path(__file__).with_name('SYMMETRY.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({k:out[k]for k in['status','A2_planes','binary_rows','column_weights','all_cycles_sum_to']},indent=2))
