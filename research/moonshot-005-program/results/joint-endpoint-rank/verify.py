#!/usr/bin/env python3
"""Exact current-source corroboration of the joint Y2 endpoint rank theorem."""
import argparse,gzip,itertools,json
from fractions import Fraction as F
from pathlib import Path
from independent_engine import need,sha,span,root9,dot,replay,rowplus
SOURCE='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
WORD='3d7ada763346a5658ef481f84bf895b668005a558e999be431d2257e16fbd101'
B=[5,56,65,69,77,96,100,103];S=[0,7,20,27,36,46,57,111]
def rank(A):
 if not A:return 0
 D=[list(map(F,r)) for r in A];k=0
 for j in range(len(D[0])):
  i=next((i for i in range(k,len(D)) if D[i][j]),None)
  if i is None:continue
  D[k],D[i]=D[i],D[k];c=D[k][j];D[k]=[v/c for v in D[k]]
  for i in range(k+1,len(D)):
   c=D[i][j]
   if c:D[i]=[u-c*v for u,v in zip(D[i],D[k])]
  k+=1
  if k==len(D):break
 return k
def inverse(A):
 n=len(A);D=[list(map(F,r))+[F(i==j) for j in range(n)] for i,r in enumerate(A)]
 for j in range(n):
  i=next((i for i in range(j,n) if D[i][j]),None);need(i is not None,'invertible basis');D[j],D[i]=D[i],D[j];c=D[j][j];D[j]=[v/c for v in D[j]]
  for i in range(n):
   if i!=j:
    c=D[i][j]
    if c:D[i]=[u-c*v for u,v in zip(D[i],D[j])]
 return [r[n:] for r in D]
def main(a):
 sb=(a.repo/'research/shared-wire-split-composition/data/final.json.gz').read_bytes();wb=(a.repo/'research/moonshot-005-program/results/orthogonal-frame-feedback/output/WORD.json.gz').read_bytes();need(sha(sb)==SOURCE and sha(wb)==WORD,'exact source pins')
 s,w=[json.loads(gzip.decompress(b)) for b in (sb,wb)];H=[s['live'][i] for i in s['hosted']['Dports']];host=dict(zip(H,zip(s['hosted']['X2'],s['hosted']['Y2'])));raw={int(k):v for k,v in w['private_role_map'].items()}
 roots={h:root9(s['frames'][s['initial'][h]][0]) for h in H};G={(i,j):F(dot(roots[i],roots[j]),18) for i in H for j in H};frames=s['frames']+[d['frame'] for d in w['additional_charts']];rows,loc,_=replay(w,list(map(span,frames)),w['marks']['common_starts'],True)
 R={i:{j:rows[raw[host[i][0]]].get(raw[host[j][1]],F(0)) for j in H} for i in H};M={i:{j:F(i==j)+R[i][j] for j in H} for i in H}
 q={r:{raw[r]:F(1),r:F(-1)} for r in raw}
 for h in H:
  expected=q[host[h][0]]
  for j,c in R[h].items():
   if c:expected=rowplus(expected,q[host[j][1]],c)
  need(rows[raw[host[h][0]]]==expected and rows[raw[host[h][1]]]==q[host[h][1]],'complete arbitrary-input b+Rd,d premise')
 need(all(M[i][j]==F(i==j)+(G[i,j] if j in B and i not in B else 0)+(G[i,j] if i in B and j in S else 0) for i in H for j in H),'actual current rank88 source model')
 Z={h:[(-1 if h in B else 1)*G[h,t] for t in S] for h in H};need(all(sum(M[i][j]*Z[j][k] for j in H)==0 for i in H for k in range(8)),'actual current kernel')
 need(rank([[M[i][j] for j in H] for i in H])==88,'exact current rank88')
 Q={i:{j:M[i][j]-G[i,j] for j in H} for i in H};need(all(not Q[i][b] for i in H for b in B),'baseline kernel coordinate B')
 need(rank([[Q[i][j] for j in H] for i in H])==88,'exact supplied-Gram rank88')
 basis=[]
 for h in H:
  if h not in B+S and rank([roots[j] for j in basis+[h]])>len(basis):basis.append(h)
  if len(basis)==8:break
 need(len(basis)==8,'eighty outside roots span8')
 cases=[];no_baseline=None;actual_stale_difference=None
 for overlap in range(9):
  I=next(B[:overlap]+list(extra) for extra in itertools.combinations(S,8-overlap) if rank([roots[h] for h in B[:overlap]+list(extra)])==8)
  inv=inverse([[G[i,j] for j in I] for i in I]);C=[[sum(inv[k][l]*G[I[l],h] for l in range(8)) for h in H] for k in range(8)]
  D={i:{h:C[k][j]-F(i==h) for j,h in enumerate(H)} for k,i in enumerate(I)}
  need(all(not D[i][j] for i in I for j in I),'systematic triangular pivot map')
  compressed=[[D[i][b] for b in B] for i in I];defect=rank(compressed);need(defect==8-overlap,'every tested overlap exact compressed rank')
  case={'overlap':overlap,'pivots':I,'compressed_endpoint_rank':defect,'joint_rank_with_supplied_G':88+defect}
  if overlap in (0,8):
   RD={i:{h:sum(R[i][k]*D[k][h] for k in I if R[i][k]) for h in H} for i in H}
   E=[[Q[i][h]+RD[i][h] for h in H] for i in H]+[[D[i][h] for h in H] for i in I]
   need(rank(E)==96-overlap,'direct full joint-stack corroboration')
   case['direct_stack_rank']=rank(E)
   if overlap==8:
    KZ=[[sum(D[i][h]*Z[h][k] for h in H) for k in range(8)] for i in I]
    need(rank(KZ)==8,'without-baseline all prior null directions become debt')
    E0=[[M[i][h]+RD[i][h] for h in H] for i in H]+[[D[i][h] for h in H] for i in I]
    no_baseline=rank(E0);need(no_baseline==96,'no-baseline joint rank96')
    actual_stale_difference=sum(bool(RD[i][h]) for i in H for h in H);need(actual_stale_difference>0,'old reads materially depend on encoded current rows')
    need(sum(bool(D[i][h]) for i in I for h in H)==352,'exact source encoder support352')
    need(sum(bool(G[h,b]) for h in H for b in B)==360,'exact source baseline support360')
    need(all(sum(G[h,b]*C[I.index(b)][j] for b in B)==G[h,z] for h in H for j,z in enumerate(H)),'copied systematic B packet rows factor supplied G')
  cases.append(case)
 result={'status':'PASS_EXACT_JOINT_Y2_ENDPOINT_GATE','source_sha256':SOURCE,'current_word_sha256':WORD,'exact_input_columns':1880,'current_rank':88,'no_baseline_systematic_B_joint_rank':no_baseline,'supplied_G_best_joint_rank':88,'outside_BS_root_basis':basis,'overlap_cases':cases,'stale_read_coefficient_differences':actual_stale_difference,'proposed_encoder_ADDs':352,'proposed_baseline_ADDs':360,'proposed_copy_ADDs':8,'proposed_owned_rank1_calls':8,'scope':'Algebraic endpoint identity plus exact source corroboration; no new physical word, cost lower bound or kappa.'}
 a.output.mkdir(parents=True,exist_ok=True);(a.output/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(result['status'],'no K:',no_baseline,'with G best:88')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
