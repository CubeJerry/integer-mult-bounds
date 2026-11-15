#!/usr/bin/env python3
import argparse,hashlib,json
from pathlib import Path

def spaces(n):
 out={frozenset([0])}
 for v in range(1,1<<n):
  for S in list(out):
   if v not in S:out.add(S|frozenset(x^v for x in S))
 return sorted(out,key=lambda s:(len(s),sorted(s)))
def rank(rows):
 S={0}
 for v in rows:
  if v not in S:S|={x^v for x in list(S)}
 return len(S).bit_length()-1
def run(h,ds,prices):
 n=h+sum(ds);hm=(1<<h)-1;dm=[];at=h
 for d in ds:dm.append(((1<<d)-1)<<at);at+=d
 A,B,C=prices;pack=[]
 for v in range(1,1<<n):
  hp=v&hm;hd=v^hp
  if not hd:pack.append((min(A,B+C),v))
  elif sum(bool(v&m)for m in dm)==1:pack.append((B+C if hp else C,v))
 pack.sort();allS=spaces(n);opts=[]
 for S in allS:
  U={0};price=0
  for w,v in pack:
   if v in S and v not in U:price+=w;U|={x^v for x in list(U)}
  if U==S:opts.append((price,S))
 cnt=bad=0
 for K in allS:
  c=len(K).bit_length()-1;hr=rank(v&hm for v in K);p=rank(v&~hm for v in K);t=sum(rank(v&m for v in K)for m in dm)
  opt=min(z for z,S in opts if K<=S);pred=(c-p)*A+p*B+t*C
  if hr==c:assert opt==pred,(K,opt,pred);cnt+=1
  elif opt<pred:bad+=1
 return {'H':h,'D_blocks':ds,'prices':prices,'spaces':len(allS),'transverse_exact':cnt,'nontransverse_rejections':bad}
p=argparse.ArgumentParser();p.add_argument('--proof',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
R=[run(h,ds,cost)for h,ds in [(1,[1,1]),(2,[1,1]),(1,[2,2]),(2,[1,1,1])]for cost in [(7,2,6),(7,4,4),(9,7,4),(8,2,6)]]
assert sum(x['nontransverse_rejections']for x in R)>0
out={'status':'PASS_INDEPENDENT_QUERY_MOVEMENT_REVIEW','proof_sha256':hashlib.sha256(a.proof.read_bytes()).hexdigest(),'positive_transverse_cases_including_zero':sum(x['transverse_exact']for x in R),'finite_optimizations':R,'method':'Each binary ambient subspace, minimum-weight admissible vector basis by greedy exchange; then minimize over superspaces containing target. Claimed formula used only for comparison.','scope':'Finite independent checks; universal proof separately audited.'}
a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'],out['positive_transverse_cases_including_zero'])
