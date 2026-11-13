#!/usr/bin/env python3
"""Exact source-bound coordinate-return algebra; no constructor imports."""
import argparse,gzip,hashlib,json,itertools
from fractions import Fraction as F
from pathlib import Path
if not __debug__:raise SystemExit('Exact assertion checks require Python without -O')
SP='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883';WP='ca493a06385fc55a1b1b2d30ddb638c7f5b021d19459aa6b0b8c85e3797510d2'
def plus(a,b,c):
 a=a.copy()
 for j,x in b.items():
  v=a.get(j,0)+c*x
  if v:a[j]=v
  else:a.pop(j,None)
 return a
def rank(A):
 A=[list(map(F,r)) for r in A];k=0
 if not A:return 0
 for j in range(len(A[0])):
  i=next((i for i in range(k,len(A)) if A[i][j]),None)
  if i is None:continue
  A[k],A[i]=A[i],A[k];v=A[k][j];A[k]=[x/v for x in A[k]]
  for i in range(k+1,len(A)):
   if A[i][j]:
    v=A[i][j];A[i]=[x-v*y for x,y in zip(A[i],A[k])]
  k+=1
  if k==len(A):break
 return k
def normalized(v):
 a=next(x for x in v if x);return tuple(x/a for x in v)
def main(a):
 def load(path,pin):
  b=path.read_bytes();assert hashlib.sha256(b).hexdigest()==pin;return json.loads(gzip.decompress(b))
 s=load(a.repo/'research/shared-wire-split-composition/data/final.json.gz',SP);w=load(a.repo/'research/moonshot-005-program/results/joint-current-row-codes/cyclic-dual/WORD.json.gz',WP)
 raw={int(k):v for k,v in w['private_role_map'].items()};assert sorted(raw.values())==list(range(1480,1880))
 # All400 independent private inputs, all common originals zero. Entire word retained.
 rows={r:({r-1480:F(1)} if r>=1480 else {}) for r in range(1880)}
 for e in w['program']:
  op,r=e[:2]
  if op=='INIT':assert r not in rows;rows[r]={}
  elif op=='CLEAR':del rows[r]
  elif op in ('ADD','COPY'):rows[r]=plus(rows[r],rows[e[2]],F(e[3]))
  elif op=='SCALE':rows[r]={j:F(e[2])*x for j,x in rows[r].items()}
  else:assert op=='MOVE'
 assert all(not rows[r] for r in range(1480)) and len(rows)==1880
 H=[s['live'][i] for i in s['hosted']['Dports']];host=dict(zip(H,zip(s['hosted']['X2'],s['hosted']['Y2'])));hi={h:i for i,h in enumerate(H)}
 K=[h for g in w['cyclic_dual']['source_groups'] for f in ['B','S','T'] for h in g[f]];B=[h for g in w['cyclic_dual']['source_groups'] for h in g['B']];O=[h for h in H if h not in K];Frees=[h for h in K if h not in B]
 bq={h:raw[host[h][0]]-1480 for h in H};dq={h:raw[host[h][1]]-1480 for h in H};M=[]
 for h in H:
  row=rows[raw[host[h][0]]];assert row.get(bq[h])==1 and all(j==bq[h] or j in dq.values() for j in row)
  assert rows[raw[host[h][1]]]=={dq[h]:F(1)}
  M.append([row.get(dq[j],F(0))+int(h==j) for j in H])
 I=[hi[h] for h in K];Jout=[hi[h] for h in O];BI=[hi[h] for h in B]
 assert len(K)==22 and len(B)==8 and all(M[hi[h]][hi[j]]==int(h==j) for h in O for j in O)
 assert all(not M[hi[h]][hi[j]] for h in K for j in O)
 assert all(M[hi[h]][hi[j]]==int(h==j) for h in B for j in B)
 def r9(h):
  n=s['frames'][s['initial'][h]][0];t=[j for j in range(9) if n>>j&1]
  if len(t)==3:return [2 if j in t else -1 for j in range(9)]
  z=[j for j in range(9) if j not in t];return [3*(int(j==z[0])-int(j==z[1])) for j in range(9)]
 roots={h:r9(h) for h in H}
 gram=lambda h,j:F(sum(x*y for x,y in zip(roots[h],roots[j])),18)
 assert all(M[hi[h]][hi[j]]==gram(h,j) for h in K for j in K)
 assert all(not M[hi[h]][j] for h in O for j in I if j not in BI)
 assert all(M[hi[h]][hi[b]]==gram(h,b) for h in O for b in B)
 G=[[M[i][j] for j in I] for i in I];assert rank(G)==8 and rank(M)==82
 U=[[M[hi[b]][hi[f]] for f in Frees] for b in B];assert rank(U)==8
 Z=[]
 for h in H:
  if h in B:z=[-x for x in U[B.index(h)]]
  elif h in Frees:z=[F(int(h==f)) for f in Frees]
  else:z=[sum(M[hi[h]][hi[b]]*U[k][t] for k,b in enumerate(B)) for t in range(14)]
  Z.append(z)
 assert all(sum(M[i][j]*Z[j][k] for j in range(96))==0 for i in range(96) for k in range(14)) and rank(Z)==14
 assert all(any(z) for z in Z) and len({normalized(z) for z in Z})==96
 triple=[1,4,105];assert all(Z[hi[1]][k]-Z[hi[4]][k]-Z[hi[105]][k]==0 for k in range(14))
 assert rank([[r[j] for j,h in enumerate(H) if h not in triple] for r in M])==81
 weights=[]
 for block in (K[:11],K[11:]):
  idx=[hi[h] for h in block];gg=[[M[i][j] for j in idx] for i in idx];assert rank(gg)==4;best={};wit={}
  for bits in range(1<<11):
   j=[k for k in range(11) if bits>>k&1];c=[k for k in range(11) if not bits>>k&1];gain=4-rank([[r[k] for k in c] for r in gg])
   for d in range(1,gain+1):
    if d not in best or len(j)<best[d]:best[d]=len(j);wit[d]=[block[k] for k in j]
  assert list(best[d] for d in range(1,5))==[5,8,10,11];weights.append({'ports':block,'weights':best,'witnesses':wit})
 choice=[56,65,69,77,96,100,103,6,9,10,12,13,16,22,25,28,29,31,32,33,35,41,50,53,55,63,66,71,72,74,75]
 comp=[j for j,h in enumerate(H) if h not in choice];N=[[r[j] for j in comp] for r in M];complete=[H[i] for i,r in enumerate(N) if not any(r)];assert rank(N)==58 and len(complete)==24
 # Negative control: support2 cannot have a rank gain; consuming one truncated column differs.
 assert rank([[r[j] for j,h in enumerate(H) if h not in triple[:2]] for r in M])==82
 payload=json.dumps([[str(x) for x in row] for row in M],separators=(',',':')).encode()
 out={'status':'PASS_EXACT_SOURCE_BOUND_COORDINATE_RETURN_ALGEBRA','source_pin':SP,'cyclic_pin':WP,'source_scope':'Full400 private columns of authenticated1880-word; common originals zero for this residual extraction. Inherited whole-source admission and pure-rail review separately establish its current-row meaning.','H':H,'K':K,'B':B,'M_sha256':hashlib.sha256(payload).hexdigest(),'M':[[str(x) for x in r] for r in M],'kernel_Z':[[str(x) for x in r] for r in Z],'rank_M':82,'minimum_support':3,'minimum_support_witness':triple,'witness_coefficients':[1,-1,-1],'Gram_weights':weights,'J31':choice,'J31_remaining_rank':58,'J31_completed_original_B':complete,'negative_controls':{'two_returns_no_rank_gain':True,'projective_pair_scan_complete':4560},'scope':'Coordinate-return theorem and finite source algebra only. No universal31-return optimality without further classification, no complete native or kappa.'}
 a.output.mkdir(parents=True,exist_ok=True);(a.output/'COORDINATE-RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ('status','M_sha256','rank_M','minimum_support','J31_remaining_rank','J31_completed_original_B')},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
