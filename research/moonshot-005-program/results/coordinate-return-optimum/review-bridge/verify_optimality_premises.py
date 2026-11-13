#!/usr/bin/env python3
"""Four exact finite premises for the31-coordinate/rank58 optimum theorem."""
import argparse,gzip,hashlib,itertools,json
from fractions import Fraction as F
from pathlib import Path
if not __debug__:raise SystemExit('Exact assertion checks require Python without -O')
SP='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883';MP='13c185ec1ef237bdb0d707503ed6efcc5f5d66f0c364498402897ca32e7054e8'
def echelon(A):
 A=[list(map(F,r)) for r in A];k=0;p=[]
 if not A:return [],[]
 for j in range(len(A[0])):
  i=next((i for i in range(k,len(A)) if A[i][j]),None)
  if i is None:continue
  A[k],A[i]=A[i],A[k];v=A[k][j];A[k]=[x/v for x in A[k]]
  for i in range(len(A)):
   if i!=k and A[i][j]:
    v=A[i][j];A[i]=[x-v*y for x,y in zip(A[i],A[k])]
  p.append(j);k+=1
  if k==len(A):break
 return A[:k],p
def rank(A):return len(echelon(A)[0])
def norm(v):
 a=next(x for x in v if x);return tuple(x/a for x in v)
def root9(n):
 t=[j for j in range(9) if n>>j&1]
 if len(t)==3:return [2 if j in t else -1 for j in range(9)]
 assert len(t)==7;z=[j for j in range(9) if j not in t];return [3*(int(j==z[0])-int(j==z[1])) for j in range(9)]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def main(a):
 sb=(a.repo/'research/shared-wire-split-composition/data/final.json.gz').read_bytes();assert hashlib.sha256(sb).hexdigest()==SP;s=json.loads(gzip.decompress(sb))
 d=json.loads(a.coordinate_result.read_text());M=[[F(x) for x in r] for r in d['M']];Z=[[F(x) for x in r] for r in d['kernel_Z']];H=d['H'];K=d['K'];B=d['B'];hi={h:i for i,h in enumerate(H)}
 assert d['source_pin']==SP and hashlib.sha256(json.dumps([[str(x) for x in r] for r in M],separators=(',',':')).encode()).hexdigest()==MP
 assert len(H)==96 and rank(M)==82 and rank(Z)==14 and all(sum(M[i][j]*Z[j][k] for j in range(96))==0 for i in range(96) for k in range(14))
 O=[h for h in H if h not in K];Base=B+O;Extra=[h for h in H if h not in Base];assert len(Base)==82 and len(Extra)==14
 normal={h:s['frames'][s['initial'][h]][0] for h in H};aroot={h:root9(normal[h]) for h in H};U=[[-v for v in Z[hi[b]]] for b in B];assert rank(U)==8
 coordinates={}
 for h in Base:
  g=[F(dot(aroot[h],aroot[b]),18) for b in B];coordinates[h]=g;sign=-1 if h in B else 1
  assert Z[hi[h]]==[sign*sum(g[k]*U[k][t] for k in range(8)) for t in range(14)]
 assert len({norm(coordinates[h]) for h in Base})==82
 E,piv=echelon(U);free=[j for j in range(14) if j not in piv];assert len(free)==6;Q=[]
 for h in Extra:
  v=Z[hi[h]].copy()
  for row,j in zip(E,piv):
   if v[j]:
    c=v[j];v=[x-c*y for x,y in zip(v,row)]
  assert all(not v[j] for j in piv);Q.append([v[j] for j in free])
 assert all(any(r) for r in Q) and len({norm(r) for r in Q})==14
 # A8+Zw norm2 directions, exactly the native full120 projective E8 roots.
 N=[n for n in range(512) if n.bit_count() in (3,7)];A=[root9(n) for n in N];assert len(N)==120 and all(dot(v,v)==18 and sum(v)==0 for v in A)
 assert len({norm(v) for v in A})==120
 nidx={n:i for i,n in enumerate(N)};rootbase={nidx[normal[h]] for h in Base};flats={}
 for i,j in itertools.combinations(range(120),2):
  if not dot(A[i],A[j]):continue
  f=tuple(k for k,r in enumerate(A) if dot(r,A[i])==dot(r,A[j])==0);assert len(f)==36
  if f not in flats:
   assert rank([A[k] for k in f])==6;flats[f]=[N[i],N[j]]
 assert len(flats)==1120;counts={f:len(set(f)&rootbase) for f in flats};assert max(counts.values())==29
 best=max(flats,key=lambda f:counts[f]);J=d['J31'];assert len(J)==31 and len(set(J))==31 and rank([Z[hi[h]] for h in J])==7
 residual=rank([[r[j] for j,h in enumerate(H) if h not in J] for r in M]);assert residual==58
 out={'status':'PASS_FOUR_EXACT_COORDINATE_OPTIMALITY_PREMISES','source_sha256':SP,'M_sha256':MP,'rank_M':82,'kernel_dimension':14,'B':B,'base82':Base,'exceptional14':Extra,'base_E8_coordinates':{str(h):[str(v) for v in coordinates[h]] for h in Base},'kernel_embedding_U':[[str(v) for v in r] for r in U],'exceptional_quotient_coordinates':{str(h):[str(v) for v in r] for h,r in zip(Extra,Q)},'quotient_dimension':6,'quotient_lines_nonzero_distinct':14,'all_A2_perpendicular_E6_flats':1120,'max_base82_E6_intersection':29,'E6_max_witness':{'A2_normal_pair':flats[best],'base_ports':[h for h in Base if nidx[normal[h]] in best]},'J31':J,'J31_kernel_rank':7,'J31_remaining_rank':58,'negative_controls':{'duplicate_exceptional_row_fails_distinctness':len({norm(r) for r in Q[:-1]+[Q[0]]})==13,'wrong_base_orientation_rejected':Z[hi[B[0]]]!=U[0]},'scope':'Four finite premises only. The universal optimum additionally uses the separately audited E8 lattice/ADE argument; coordinate-only original whole-field returns, fixed M, characteristic zero.'}
 a.output.mkdir(parents=True,exist_ok=True);(a.output/'OPTIMALITY-PREMISES.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ('status','base82','exceptional14','quotient_lines_nonzero_distinct','all_A2_perpendicular_E6_flats','max_base82_E6_intersection','J31_kernel_rank','J31_remaining_rank')},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--coordinate-result',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
