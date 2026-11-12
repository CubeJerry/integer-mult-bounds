#!/usr/bin/env python3
"""Independent q/u-basis replay and joint endpoint review; no author imports."""
import argparse,gzip,hashlib,json
from fractions import Fraction as F
from pathlib import Path
SOURCE='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
PAYLOAD='2e0853ba95763f5182d675fbf08317871ca4b5df7328066230e446ef959f782a'
B=[5,56,65,69,77,96,100,103];S=[0,7,20,27,36,46,57,111]
def need(q,m):
 if not q:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def root(v):
 bs=[i for i in range(9) if v>>i&1]
 if len(bs)==3:return [2*int(i in bs) for i in range(8)] if 8 in bs else [1 if i in bs else -1 for i in range(8)]
 need(len(bs)==7,'source root type');i,j=[i for i in range(9) if i not in bs]
 return [1 if k==i else -1 for k in range(8)] if j==8 else [2*(int(k==i)-int(k==j)) for k in range(8)]
def span(a):
 q={0}
 for v in a:q|={u^v for u in tuple(q)}
 return q
def plus(a,b,c=F(1)):
 q=a.copy()
 for k,v in b.items():
  x=q.get(k,F(0))+c*v
  if x:q[k]=x
  else:q.pop(k,None)
 return q
def inv(A):
 n=len(A);M=[[F(x) for x in r]+[F(i==j) for j in range(n)] for i,r in enumerate(A)];det=F(1)
 for j in range(n):
  k=next(i for i in range(j,n) if M[i][j])
  if k!=j:M[k],M[j]=M[j],M[k];det=-det
  c=M[j][j];det*=c;M[j]=[x/c for x in M[j]]
  for i in range(n):
   if i!=j:
    c=M[i][j]
    if c:M[i]=[x-c*y for x,y in zip(M[i],M[j])]
 return [r[n:] for r in M],det
def rank_mod(A,p=65537):
 M=[[F(x).numerator*pow(F(x).denominator%p,-1,p)%p for x in r] for r in A];k=0
 if not M:return 0
 for j in range(len(M[0])):
  q=next((i for i in range(k,len(M)) if M[i][j]),None)
  if q is None:continue
  M[k],M[q]=M[q],M[k];c=pow(M[k][j],-1,p);M[k]=[x*c%p for x in M[k]]
  for i in range(k+1,len(M)):
   c=M[i][j]
   if c:M[i]=[(x-c*y)%p for x,y in zip(M[i],M[k])]
  k+=1
  if k==len(M):break
 return k
def replay(w,spaces,raw,sub=None):
 # Invertible1880-coordinate basis:1480 common u,400 private differences q.
 rows={i:{i:F(1)} for i in range(1880)};loc=dict(enumerate(w['initial']))
 for x,r in raw.items():rows[r]=plus({x:F(1)},(sub or {}).get(r,{r:F(1)}))
 for k,e in enumerate(w['program'][:w['marks']['common_starts']]):
  op,r=e[:2]
  if op=='INIT':need(r>=1880 and r not in rows,'fresh owner');rows[r]={};loc[r]=e[2]
  elif op=='CLEAR':need(r>=1880 and loc.get(r)==e[2],'owned retirement');del rows[r];del loc[r]
  elif op=='MOVE':
   x,y,o=e[2:];need(loc.get(r)==x and o==(r>=1880),'current move source/ownership');need(spaces[x]<spaces[y] or o and spaces[y]<spaces[x],'nested move');loc[r]=y
  elif op=='SCALE':
   c=F(e[2]);need(c and loc.get(r)==e[3],'cochart scale');rows[r]={j:c*v for j,v in rows[r].items()}
  elif op in('ADD','COPY'):
   j,c,at=e[2:];need(j!=r and loc[j]==loc[r]==at,'actual cochart read '+str(k));need(op!='COPY' or not rows[r],'empty copy target');rows[r]=plus(rows[r],rows[j],F(c))
  else:raise ValueError(op)
 return rows,loc

def main(a):
 sb=(a.repo/'research/shared-wire-split-composition/data/final.json.gz').read_bytes();wb=(a.repo/'research/moonshot-005-program/results/orthogonal-frame-feedback/output/WORD.json.gz').read_bytes();need(sha(sb)==SOURCE and sha(gzip.decompress(wb))==PAYLOAD,'actual source pins')
 s=json.loads(gzip.decompress(sb));w=json.loads(gzip.decompress(wb));raw={int(x):r for x,r in w['private_role_map'].items()};spaces=list(map(span,s['frames']+[d['frame'] for d in w['additional_charts']]))
 H=[s['live'][i] for i in s['hosted']['Dports']];ix={h:i for i,h in enumerate(H)};host={h:(x,y) for h,x,y in zip(H,s['hosted']['X2'],s['hosted']['Y2'])};roots={h:root(s['frames'][s['initial'][h]][0]) for h in H}
 G=[[F(sum(x*y for x,y in zip(roots[i],roots[j])),8) for j in H] for i in H];rows,loc=replay(w,spaces,raw);R=[]
 for h in H:
  r=rows[raw[host[h][0]]];line=[r.get(raw[host[j][1]],F(0)) for j in H];want={raw[host[h][0]]:F(1)}
  for j,c in zip(H,line):
   if c:want[raw[host[j][1]]]=c
  need(r==want and rows[raw[host[h][1]]]=={raw[host[h][1]]:F(1)},'all1880-column b+Rd,d source premise');R.append(line)
 M=[[F(i==j)+R[i][j] for j in range(96)] for i in range(96)];Q=[[M[i][j]-G[i][j] for j in range(96)] for i in range(96)]
 need(all(M[i][j]==F(i==j)+(G[i][j] if k in B and h not in B else 0)+(G[i][j] if h in B and k in S else 0) for i,h in enumerate(H) for j,k in enumerate(H)),'both current reciprocal blocks')
 Z=[[-G[ix[h]][ix[t]] if h in B else G[ix[h]][ix[t]] for t in S] for h in H]
 need(all(sum(M[i][j]*Z[j][k] for j in range(96))==0 for i in range(96) for k in range(8)) and [[Z[ix[h]][k] for k in range(8)] for h in S]==[[F(i==j) for j in range(8)] for i in range(8)],'exact independent8-column kernel')
 need(rank_mod(M)==88 and rank_mod(Q)==88 and all(not Q[i][ix[b]] for i in range(96) for b in B),'rank lower minors match explicit8-dimensional kernels')
 outside=[]
 for h in reversed(H):
  if h not in B+S and rank_mod([roots[j] for j in outside+[h]])>len(outside):outside.append(h)
  if len(outside)==8:break
 _,outdet=inv([[roots[h][k] for h in outside] for k in range(8)])
 cases=[];PB=None;stale=None;noK=None
 for k in range(9):
  I=B[:k].copy()
  for h in reversed(H):
   if h not in B+S and rank_mod([roots[j] for j in I+[h]])>len(I):I.append(h)
   if len(I)==8:break
  Wi,det=inv([[roots[h][l] for h in I] for l in range(8)]);C=[[sum(Wi[i][l]*roots[h][l] for l in range(8)) for h in H] for i in range(8)];D=[[C[i][j]-F(h==q) for j,q in enumerate(H)] for i,h in enumerate(I)]
  need(all(not D[i][ix[h]] for i in range(8) for h in I),'systematic identity pivot block')
  need(rank_mod([[D[i][ix[b]] for b in B] for i in range(8)])==8-k,'independent overlap rank compressed gate')
  RD=[[sum(R[i][ix[I[l]]]*D[l][j] for l in range(8)) for j in range(96)] for i in range(96)];need(rank_mod([[Q[i][j]+RD[i][j] for j in range(96)] for i in range(96)]+D)==96-k,'direct joint-stack modular lower witness matches algebraic upper bound')
  cases.append({'overlap':k,'pivots':I,'determinant':str(det),'joint_rank_with_G':96-k})
  if k==8:
   PB=C;stale=sum(bool(x) for r in RD for x in r);noK=rank_mod([[M[i][j]+RD[i][j] for j in range(96)] for i in range(96)]+D);need(noK==96 and stale==3638,'actual no-baseline debt and stale-read mutant')
   need(sum(bool(c) for row in D for c in row)==352 and sum(bool(G[i][ix[b]]) for i in range(96) for b in B)==360,'exact physical-proposal support counts')
   need(all(sum(G[i][ix[B[l]]]*C[l][j] for l in range(8))==G[i][j] for i in range(96) for j in range(96)),'copied current pivot values factor actual supplied K=G')
 sub={raw[host[b][1]]:{raw[host[h][1]]:c for h,c in zip(H,PB[k]) if c} for k,b in enumerate(B)};coded,cloc=replay(w,spaces,raw,sub);need(cloc==loc,'same source charts under input substitution')
 for i,h in enumerate(H):
  want={raw[host[h][0]]:F(1)}
  for j,q in enumerate(H):
   if R[i][j]:want=plus(want,sub.get(raw[host[q][1]],{raw[host[q][1]]:F(1)}),R[i][j])
  need(coded[raw[host[h][0]]]==want,'actual old reads use RP, not stale R')
  need(coded[raw[host[h][1]]]==sub.get(raw[host[h][1]],{raw[host[h][1]]:F(1)}),'actual output preserves coded Pd and its original-Y2 restoration debt')
 changed=sum(coded[raw[host[h][1]]]!={raw[host[h][1]]:F(1)} for h in H);need(changed==8,'eight pivot endpoints remain changed')
 suffix=w['program'][w['marks']['common_starts']:]
 for x in s['hosted']['X2']+s['hosted']['Y2']:
  rr=raw[x];uses=[e for e in suffix if e[1]==rr or e[0] in('ADD','COPY') and e[2]==rr]
  need(uses==[['ADD',rr,x,'1',s['final'][x]]],'all192 actual raw endpoints only recouple after the checked boundary; no hidden later restoration')
 witness=ix[B[0]];need(any(M[i][witness] for i in range(96)) and all(not Q[i][witness] for i in range(96)),'silently credited G cancels an actual nonzero no-K column')
 files=['PROOF.md','verify.py','independent_engine.py','output/RESULT.json','NOTE-REVIEW.json'];report={'status':'PASS_INDEPENDENT_JOINT_ENDPOINT_INTERFACE_AND_SOURCE_REVIEW','reviewed_files':{f:sha((a.author/f).read_bytes()) for f in files},'source_sha256':SOURCE,'word_payload_sha256':PAYLOAD,'method':'Fresh1880-column replay in independent q/u coordinates, separate8-coordinate root embedding, distinct nonorthogonal pivot examples outside B and S, exact rational kernel identities plus nonzero modular minors, and a second literal source replay with coded Y2 input rows. No reviewed checker/engine imported or executed.','current_rank':88,'no_baseline_joint_rank':noK,'with_actually_supplied_G_best_joint_rank':88,'outside_basis':outside,'outside_determinant':str(outdet),'overlap_cases':cases,'stale_read_coefficient_changes':stale,'coded_Y2_endpoints_still_changed':changed,'suffix_192_raw_endpoint_uses':'one literal recoupling ADD each; no feedback, no hidden restoration','proposed_encoder_adds':352,'baseline_adds_if_supplied':360,'copy_adds_if_supplied':8,'new_rank1_moves_if_supplied':8,'negative_controls':['silent K=G credit cancels a nonzero actual no-K column','stale d reads differ from actual coded replay','discarding restoration block hides eight changed Y2 endpoints'],'scope':'Accepted algebraic/source interface theorem. K=G must actually be transported and subtracted; this rank calculation does not provide its cost or source-word admission. No new physical encoded word, restoration algorithm, global multiplication cost lower bound or kappa.'};a.output.mkdir(parents=True,exist_ok=True);(a.output/'REVIEW.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');print(report['status']);print('noK',noK,'withG88','unrestored outputs',changed)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--author',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);main(ap.parse_args())
