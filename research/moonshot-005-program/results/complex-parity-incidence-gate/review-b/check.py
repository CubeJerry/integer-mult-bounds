#!/usr/bin/env python3
"""Independent actual-incidence and sharp block-rank controls, no producer imports."""
import argparse,gzip,hashlib,json
from pathlib import Path
from collections import Counter

def need(x,m):
 if not x:raise ValueError(m)
def root(v):
 if v.bit_count()==3:return [2 if v>>i&1 else -1 for i in range(9)]
 z=[i for i in range(9) if not v>>i&1];need(len(z)==2,'actual E8 line');return [3*(int(i==z[0])-int(i==z[1])) for i in range(9)]
def rank(A,p):
 A=[[x%p for x in r] for r in A];i=0
 for j in range(len(A[0]) if A else 0):
  k=next((k for k in range(i,len(A)) if A[k][j]),None)
  if k is None:continue
  A[i],A[k]=A[k],A[i];c=pow(A[i][j],-1,p);A[i]=[x*c%p for x in A[i]]
  for k in range(len(A)):
   if k!=i and A[k][j]:
    c=A[k][j];A[k]=[(x-c*y)%p for x,y in zip(A[k],A[i])]
  i+=1
 return i
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True);p.add_argument('--proof',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();raw=a.native.read_bytes();need(hashlib.sha256(raw).hexdigest()=='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883','native pin');proof_sha=hashlib.sha256(a.proof.read_bytes()).hexdigest();need(proof_sha=='ece753988df8a09b836f1d2571c4b781913cd35b434d565152e2853b13a12560','reviewed proof bytes');n=json.loads(gzip.decompress(raw));P=n['live'];v={h:n['frames'][n['initial'][h]][0] for h in P};Z=[7,25,42,52,76,82,97,127];zr=[root(z) for z in Z];groups={}
 for h in P:
  r=root(v[h]);vals=[sum(a*b for a,b in zip(r,z)) for z in zr];S=tuple(i for i,x in enumerate(vals) if x);need(len(S)==4,'support4');sgn=1
  for i in S:need(abs(vals[i])==9,'exact sign magnitude');sgn*=1 if vals[i]>0 else -1
  groups.setdefault(S,{-1:[],1:[]})[sgn].append(h)
 receipts=[]
 for S,z in sorted(groups.items()):
  need(sorted(map(len,z.values())) in ([3,4],[4,4]),'half sizes')
  for sg,T in sorted(z.items()):
   C=[x for x in range(512) if all(not (x&v[h]).bit_count()%2 for h in T)];need(len(C)==64,'C6 size');actual=[h for h in P if v[h] in C];need(sorted(actual)==sorted(z[-sg]),'complete opposite-half incidence');need(all(L in C for L in Z if Z.index(L) in S),'mode lines below C6');receipts.append({'modes':S,'sign':sg,'targets':T,'actual_sources':actual})
 need(len(groups)==14 and len(receipts)==28,'all actual groups')
 controls=[]
 for field in (2,3,5,65537):
  for V in (1,2,3):
   total=0
   for z in groups.values():
    a0,b0=sorted((len(x)*V for x in z.values()),reverse=True);M=[[int(i==j) for j in range(a0+b0)] for i in range(a0+b0)]
    for j in range(b0):M[j][a0+j]=1;M[a0+j][j]=1
    got=rank(M,field);need(got==a0,'sharp block-rank attainment');total+=got
   need(total==56*V,'sharp global rank56V');controls.append({'field':field,'V':V,'rank':total})
 # Explicit geometry mutation: adding one target's own source violates incidence.
 r=receipts[0];need(v[r['targets'][0]] not in [x for x in range(512) if all(not (x&v[h]).bit_count()%2 for h in r['targets'])],'own input exclusion')
 out={'status':'PASS_INDEPENDENT_PARITY_INCIDENCE_AND_BLOCK_CONTROLS','proof_sha256':proof_sha,'native_sha256':hashlib.sha256(raw).hexdigest(),'groups':len(groups),'charts':len(receipts),'half_size_census':dict(Counter(len(x['targets']) for x in receipts)),'incidences':receipts,'sharp_controls':controls,'own_source_mutant_rejected':True,'scope':'Independent finite geometry and sharpness controls. All-field rank and phase-to-rowspace proof are reviewed in REVIEW.md; numerical checks do not replace that argument.'};a.output.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');print(out['status'])
