#!/usr/bin/env python3
"""Exact H263 phase/cover witness and nilpotent common-algebra controls."""
from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256
from itertools import product,combinations
from pathlib import Path
import gzip,json

def rank(rows):
 piv={}
 for x in rows:
  while x:
   k=x.bit_length()-1
   if k in piv:x^=piv[k]
   else:piv[k]=x;break
 return len(piv)
def mm(A,B):
 out=[]
 for a in A:
  z=0
  while a:
   low=a&-a;z^=B[low.bit_length()-1];a^=low
  out.append(z)
 return out
def graph_span(units):
 n=len(units[0])
 return rank((1<<i)|(A[i]<<n)|(B[i]<<(2*n))for A,B in product(units,repeat=2)for i in range(n))
def algebra_controls():
 I2=[1,2];N=[2,0];U2=[I2,[x^y for x,y in zip(I2,N)]]
 assert mm(N,N)==[0,0]and graph_span(U2)==4
 I3=[1,2,4];A=[2,0,0];B=[4,0,0]
 assert mm(A,B)==mm(B,A)==[0,0,0]
 U3=[[I3[i]^((a&1)*A[i])^((a>>1)*B[i])for i in range(3)]for a in range(4)]
 assert all(rank(U)==3 for U in U3)and all(mm(U,V)==mm(V,U)for U,V in product(U3,repeat=2))
 assert graph_span(U3)==7
 GL2=[list(A)for A in product(range(4),repeat=2)if rank(A)==2]
 assert len(GL2)==6 and graph_span(GL2)==6
 assert any(mm(A,B)!=mm(B,A)for A,B in product(GL2,repeat=2))
 return{'single_Jordan_target_span':4,'single_Jordan_full_input':6,'two_nilpotent_target_span':7,'two_nilpotent_full_input':9,'noncommuting_scope_control_span':6,'noncommuting_full_input':6}

def main():
 ap=ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();p=a.repo/'research/moonshot-005-program/results'
 layout=p/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz';raw=gzip.decompress(layout.read_bytes());assert sha256(raw).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'
 L=json.loads(raw);roots=L['root_table'];Hs=list(map(set,L['A2']));Ds=list(map(set,L['D4']));native=set(range(111));H=263;donors=Hs[H]&native;assert donors=={0,61,62}
 adj=[{j for j,v in enumerate(roots)if i!=j and sum(x*y for x,y in zip(u,v))==0}for i,u in enumerate(roots)]
 singles={j:[h for h,P in enumerate(Hs)if j in P and len(P&native)==1]for j in donors}
 visible={};I=[]
 for i in range(111):
  if not Hs[H]<=adj[i]:continue
  tight=True
  for j in donors:
   hs=[h for h,P in enumerate(Hs)if j in P and P<=adj[i]];assert len(hs)==16;visible[i,j]=hs
   if any(h in singles[j]for h in hs):tight=False
  if tight:I.append(i)
 assert len(I)==33 and 80 not in I and 10 not in donors
 ports=[d for d,D in enumerate(Ds)if Hs[H]<=D];assert len(ports)==45
 audiences={d:set(I)&Ds[L['dual_D4'][d]]for d in ports};assert all(audiences.values())
 intersections=Counter()
 for d,e in combinations(ports,2):
  n=len(audiences[d]&audiences[e]);assert n>0;intersections[n]+=1
 assert sum(intersections.values())==990
 assert all(sum(i in audiences[d]for d in ports)==15 for i in I)
 route=p/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz';rawroutes=gzip.decompress(route.read_bytes());assert sha256(rawroutes).hexdigest()=='6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036'
 ingress=Counter();egress=Counter();late=0;owners=set()
 for line in rawroutes.splitlines():
  kind,j,c,h,d,k,left,right=json.loads(line)
  if h!=H:continue
  if kind=='X':
   assert j==left and j in donors and(j,c)not in owners;owners.add((j,c));ingress[j]+=1;egress[d]+=1
  else:late+=1
 assert ingress==Counter({j:30 for j in donors})and egress==Counter({d:2 for d in ports})and len(owners)==90 and late==0
 phases=p/'bit-asymmetric-balanced-atlas/author/output/PLANE-PHASES.json';ph=json.loads(phases.read_text())[str(H)];assert ph['early']==2 and ph['late']==0 and ph['source_quota']==30
 decisions=p/'bit-stripe-varying-port-cut/author/output/DECISIONS.json.gz';old=json.loads(gzip.decompress(decisions.read_bytes()));oldH=next(x for x in old['planes']if x['plane']==H)
 assert oldH['rank_cap']==1 and oldH['packing_cap']==1 and oldH['uncovered_ports']==0 and oldH['receivers']==I
 assert all(i!=80 and j!=10 for i in I for j in donors)
 controls=algebra_controls()
 deps=[layout,route,phases,decisions,p/'bit-common-semisimple-source-gate/author/PROOF.md',p/'bit-stripe-varying-port-cut/author/PROOF.md',p/'bit-irreducible-low-excess-target/author/PROOF.md']
 result={'status':'PASS_NONSEMISIMPLE_COMMUTING_SOURCE_EARLY_GATE','H':H,'native_donors':sorted(donors),'joint_tight_receivers':I,'ports':45,'early_original_owners':90,'late_owners_at_H':0,'nonempty_audiences':45,'audience_intersection_histogram':dict(intersections),'all_99_relevant_Bstar_blocks_identity':True,'controls':controls,'scope':'asymmetric bank480 replications, globally commuting source blocks, original or fixed Bstar proper target; nonlinear downstream allowed','older_balanced_phase_excluded':False,'new_complete_kappa':False,'pins':[{'path':str(x.relative_to(a.repo)),'sha256':sha256(x.read_bytes()).hexdigest()}for x in deps]}
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');(a.out/'AUDIENCES.json').write_text(json.dumps({str(d):sorted(v)for d,v in audiences.items()},indent=2,sort_keys=True)+'\n');print(result['status']);print(json.dumps({'audience_intersections':dict(intersections),'algebra_controls':controls},sort_keys=True))
if __name__=='__main__':main()
