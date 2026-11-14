#!/usr/bin/env python3
"""Exact source witnesses for modal fitting rigidity; standard library only."""
from fractions import Fraction as Q
from pathlib import Path
from collections import Counter
import argparse,gzip,hashlib,json
PIN='0edf81ca8f6a7e60e5a01d4acdcaefdb74882180b8d12c408513bc91cd625b1c'
FRAME=[0,7,20,27,36,46,57,111]
# a,b are coordinates in FRAME; i,j are actual native port labels.
TREE=[(0,4,1,12),(1,4,1,8),(1,5,1,10),(2,5,2,10),(0,3,2,13),(4,6,4,9),(6,7,5,9)]
def need(p,m):
 if not p:raise ValueError(m)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def root(b):
 if b.bit_count()==3:return [2 if b>>i&1 else -1 for i in range(9)]
 z=[i for i in range(9)if not b>>i&1]
 need(b.bit_count()==7 and len(z)==2,'legal native normal')
 return [3*(int(i==z[0])-int(i==z[1]))for i in range(9)]
def mul(A,B):return [[sum(A[i][k]*B[k][j]for k in range(len(B)))for j in range(len(B[0]))]for i in range(len(A))]
def tr(A):return list(map(list,zip(*A)))
def eye(n):return [[Q(int(i==j))for j in range(n)]for i in range(n)]
def det(A):
 A=[r[:]for r in A];d=Q(1)
 for j in range(len(A)):
  i=next((i for i in range(j,len(A))if A[i][j]),None)
  if i is None:return Q(0)
  if i!=j:A[i],A[j]=A[j],A[i];d=-d
  p=A[j][j];d*=p
  for i in range(j+1,len(A)):
   if A[i][j]:
    f=A[i][j]/p
    for k in range(j,len(A)):A[i][k]-=f*A[j][k]
 return d
def rankmod(A,p):
 A=[[int(x.numerator)*pow(x.denominator,-1,p)%p for x in r]for r in A];row=0
 for j in range(len(A[0])):
  i=next((i for i in range(row,len(A))if A[i][j]),None)
  if i is None:continue
  A[row],A[i]=A[i],A[row];inv=pow(A[row][j],-1,p);A[row]=[x*inv%p for x in A[row]]
  for i in range(row+1,len(A)):
   q=A[i][j]
   if q:A[i]=[(x-q*y)%p for x,y in zip(A[i],A[row])]
  row+=1
  if row==len(A):break
 return row
parser=argparse.ArgumentParser();parser.add_argument('--source',type=Path,required=True);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
raw=args.source.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'literal source hash');w=json.loads(gzip.decompress(raw));H=sorted(set(w['relay']['restored_ports'])|set(w['relay']['unrestored_ports']));P=sorted(int(x)for x in w['source_role_map']if int(x)<112);need(len(H)==96 and len(P)==104,'port domains')
normal={h:w['frames'][w['initial'][w['source_role_map'][str(h)]]][0]for h in P};Z=[root(z)for z in w['relay']['ground_Gram_frame']];g={h:[Q(dot(root(normal[h]),z),18)for z in Z]for h in P}
need(all(dot(g[h],g[h])==1 for h in P),'unit root rows')
need(all((dot(g[h],g[j])==0)==bool((normal[h]&normal[j]).bit_count()%2)for h in P for j in P if h!=j),'literal off-diagonal cochart fitting')
F=[g[h]for h in FRAME];need(all(h in H for h in FRAME),'hosted frame');need(mul(F,tr(F))==eye(8),'orthonormal frame')
f={h:[dot(g[h],g[j])for j in FRAME]for h in H};tree=[];reached={0}
for a,b,i,j in TREE:
 need(i in H and j in H and i!=j,'hosted distinct witness')
 need((normal[i]&normal[j]).bit_count()%2==1,'forbidden cochart witness')
 products=[4*x*y for x,y in zip(f[i],f[j])];expected=[Q(int(k==a)-int(k==b))for k in range(8)]
 need(products==expected or products==[-x for x in expected],'two-coordinate equality')
 tree.append({'coordinates':[a,b],'ports':[i,j],'four_times_products':[str(x)for x in products],'twice_first_coordinates':[str(2*x)for x in f[i]],'twice_second_coordinates':[str(2*x)for x in f[j]]})
for _ in range(8):
 for a,b,_,_ in TREE:
  if a in reached or b in reached:reached.update([a,b])
need(len(reached)==8,'connected equality tree')
L=[[Q(int(a==b),4)for b in range(8)]for a in range(8)]
for a,b in [(0,2),(1,3)]:L[a][a]+=Q(1,24);L[b][b]+=Q(1,24);L[a][b]-=Q(1,24);L[b][a]-=Q(1,24)
def val(i,j,A):return dot(g[i],[sum(A[a][b]*g[j][b]for b in range(8))for a in range(8)])
counts={}
for name,ports in [('hosted96',H),('all104',P)]:
 bad=[(i,j)for i in ports for j in ports if i!=j and (normal[i]&normal[j]).bit_count()%2]
 values=[val(i,j,L)for i,j in bad];changed=[x for x in values if x]
 counts[name]={'forbidden_off_diagonal_ordered_pairs':len(bad),'new_nonzero_forbidden_pairs':len(changed),'forbidden_coefficients':dict(Counter(map(str,changed))),'diagonal_gram_values':dict(Counter(str(val(i,i,L))for i in ports)),'nonzero_diagonal_defects':sum(val(i,i,L)!=1 for i in ports)}
 need(all(not val(i,j,eye(8))for i,j in bad),'identity preserves fitting')
 need(all(not val(i,j,[[Q(int(a==b),4)for b in range(8)]for a in range(8)])for i,j in bad),'scalar quarter preserves off-diagonal zeros')
S=w['relay']['unrestored_ports'];C=[[sum(g[h][a]*g[h][b]for h in S)for b in range(8)]for a in range(8)];CMI=[[C[a][b]-int(a==b)for b in range(8)]for a in range(8)];need(rankmod(CMI,127)==6,'two-dimensional original bad-prime eigenspace')
LC=mul(L,C);need(det([[Q(int(a==b))-LC[a][b]for b in range(8)]for a in range(8)])==Q(3375,128),'anisotropic unit determinant boundary')
# Removing one equality from the chosen tree must leave a disconnected graph.
for excluded in range(7):
 r={0}
 for _ in range(8):
  for k,(a,b,_,_)in enumerate(TREE):
   if k!=excluded and(a in r or b in r):r.update([a,b])
 need(len(r)<8,'tree edge is needed by this proof certificate')
# N^2=0 gives a formal two-channel ring repair; its diagonal defect is full rank.
N=[[Q(0),Q(1)],[Q(0),Q(0)]];need(mul(N,N)==[[0,0],[0,0]],'nilpotent boundary');need(det([[Q(int(a==b))-N[a][b]for b in range(2)]for a in range(2)])==1,'nilpotent diagonal debt')
out={'status':'PASS_EXACT_FRAME_RIGIDITY_WITNESS','source_sha256':PIN,'frame_ports':FRAME,'frame_normals':[normal[h]for h in FRAME],'frame_rows_in_omitted_basis':[[str(x)for x in r]for r in F],'equality_tree':tree,'used_ports':sorted(set(FRAME)|{i for _,_,i,j in TREE}|{j for _,_,i,j in TREE}),'anisotropic_violations':counts,'rank_C_minus_I_mod127':6,'anisotropic_residual_determinant':'3375/128','negative_controls':['scalar quarter retains off-diagonal zeros but violates every unit-diagonal equation','anisotropic unit determinant violates original fitting','deleting any selected tree edge leaves this proof certificate disconnected','two-channel square-zero operator repairs arithmetic while retaining full diagonal debt'],'theorem_scope':'Exact modal matrix entries over characteristic-zero fields; arbitrary whole-field operator blocks via the same central dyadic identities','no_physical_completion':True,'no_new_kappa':True}
args.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({k:out[k]for k in ['status','source_sha256','used_ports','anisotropic_violations','rank_C_minus_I_mod127','no_new_kappa']},indent=2))
