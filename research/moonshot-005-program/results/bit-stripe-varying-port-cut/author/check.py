#!/usr/bin/env python3
"""Exact exhaustive native stripe-partition decisions; no timeouts or numerical solver."""
import argparse,gzip,json
from pathlib import Path
from collections import Counter
from functools import lru_cache
from hashlib import sha256
def solve(ports,n,k):
 allv=(1<<n)-1;contains=[[p for p in ports if p>>v&1]for v in range(n)];nodes=0
 @lru_cache(None)
 def search(C):
  nonlocal nodes
  nodes+=1
  C=list(C)
  while True:
   assigned=0
   for c in C:
    if assigned&c:return None
    assigned|=c
   changed=False
   for v in range(n):
    b=1<<v;chosen=next((i for i,c in enumerate(C)if c&b),None)
    poss=[tuple(p for p in contains[v]if not p&(assigned^c))for c in C]
    if chosen is None:
     colors=[i for i,p in enumerate(poss)if p]
     if not colors:return None
     if len(colors)==1:C[colors[0]]|=b;changed=True;break
    else:
     if not poss[chosen]:return None
     if len(poss[chosen])==1 and poss[chosen][0]&~C[chosen]:C[chosen]|=poss[chosen][0];changed=True;break
   if not changed:break
  free=allv^assigned
  if free.bit_count()<sum(c==0 for c in C):return None
  if not free:return tuple(C) if all(C) else None
  v=(free&-free).bit_length()-1;b=1<<v
  order=sorted(range(k),key=lambda i:(bool(C[i]),C[i].bit_count()))
  for i in order:
   cc=C[:];cc[i]|=b;res=search(tuple(cc))
   if res:return res
  return None
 res=search(tuple([1]+[0]*(k-1)))
 if res:
  assert all(res) and sum(x.bit_count()for x in res)==n and __import__('functools').reduce(int.__or__,res)==allv
  for c in res:
   for v in range(n):
    if c>>v&1:assert any(p>>v&1 and p&c==p for p in ports)
 return {'status':'SAT'if res else'UNSAT','colors':res,'nodes':nodes}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 p=a.repo/'research/moonshot-005-program'
 lr=gzip.decompress((p/'results/bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz').read_bytes());fr=(p/'results/bit-all111-balanced-causal-atlas/author/output/BALANCED-FACTOR.json').read_bytes()
 assert sha256(lr).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'
 assert sha256(fr).hexdigest()=='346e7604b000ba057e49e8dcae639eaf1b8d82aeb1466f8b959a84390971dfa7'
 l=json.loads(lr);R=l['root_table'];Hs=list(map(set,l['A2']));Ds=list(map(set,l['D4']));native=set(range(111));fac=dict(json.loads(fr)['factors'])
 O=[{j for j,v in enumerate(R)if sum(x*y for x,y in zip(u,v))==0}for u in R[:111]];DV=[{i for i in range(111)if d<=O[i]}for d in Ds]
 visible=[{i for i in range(111)if H<=O[i]}for H in Hs];capacity=[[0]*111 for _ in range(111)]
 for h,H in enumerate(Hs):
  J=H&native;m=len(J)
  if not m:continue
  bundle=45*max(8,12//m+fac.get(h,0))
  for i in visible[h]:
   for j in J:capacity[i][j]+=bundle
 tight=[{j for j in range(111)if capacity[i][j]==5760}for i in range(111)];assert sum(map(len,tight))==6110
 records=[];hist=Counter();total=5940;uncovered_total=0;statuses=Counter();max_nodes=0
 for h,H in enumerate(Hs):
  donors=H&native;m=len(donors)
  if m<2:continue
  I=sorted(i for i in visible[h]if donors<=tight[i]);ix={i:v for v,i in enumerate(I)}
  masks=[sum(1<<ix[i]for i in DV[d]&set(I))for d,D in enumerate(Ds)if H<=D];assert len(masks)==45
  ports=sorted(set(masks)-{0});alpha=1
  for z,x in enumerate(ports):
   for y in range(z+1,len(ports)):
    if x&ports[y]:continue
    alpha=2
    if m==3 and any(not w&(x|ports[y])for w in ports[y+1:]):alpha=3;break
   if alpha==m:break
  r={'plane':h,'donors':sorted(donors),'receivers':I,'packing_cap':alpha,'two_colors':None,'three_colors':None}
  if alpha>=2:
   r['two_colors']=solve(ports,len(I),2)
   if r['two_colors']['status']=='UNSAT':alpha=1
   elif alpha==3:
    r['three_colors']=solve(ports,len(I),3)
    if r['three_colors']['status']=='UNSAT':alpha=2
  for k in ['two_colors','three_colors']:
   if r[k]:statuses[r[k]['status']]+=1;max_nodes=max(max_nodes,r[k]['nodes'])
  r['rank_cap']=alpha;r['uncovered_ports']=masks.count(0);records.append(r);hist[(m,alpha)]+=1;uncovered_total+=r['uncovered_ports'];total+=360*alpha+24*r['uncovered_ports']
 assert len(records)==1108 and uncovered_total==1436
 assert hist==Counter({(2,1):204,(2,2):23,(3,1):630,(3,2):249,(3,3):2}) and total==538644
 controls=[]
 for ports,n,k,expected in [([3,5,6],3,2,'UNSAT'),([3,12],4,2,'SAT'),([3,12],4,3,'UNSAT'),([3,12,48],6,3,'SAT'),([3,6,12,9],4,2,'SAT'),([1,2,4],3,3,'SAT')]:
  got=solve(ports,n,k);assert got['status']==expected;controls.append({'ports':ports,'vertices':n,'colors':k,'status':expected})
 raw=(json.dumps({'schema':'native-stripe-partition-v1','planes':records},sort_keys=True,separators=(',',':'))+'\n').encode();a.out.mkdir(parents=True,exist_ok=True);(a.out/'DECISIONS.json.gz').write_bytes(gzip.compress(raw,mtime=0))
 result={'status':'PASS_EXHAUSTIVE_STRIPE_VARYING_SCALAR_GATE','layout_uncompressed_sha256':sha256(lr).hexdigest(),'factor_sha256':sha256(fr).hexdigest(),'decisions_uncompressed_sha256':sha256(raw).hexdigest(),'ordinary_planes':1108,'tight_pairs':6110,'rank_cap_histogram':[[list(k),v]for k,v in sorted(hist.items())],'uncovered_ports':uncovered_total,'information_capacity':total,'required_dimension':587520,'strict_deficit':587520-total,'exact_search_statuses':dict(sorted(statuses.items())),'maximum_search_nodes':max_nodes,'time_limit_used':False,'controls':controls,'scope':'Aligned scalar stripes only; arbitrary stripe-varying rows and nonlinear downstream allowed. General arrays remain open.','new_complete_kappa':False}
 (a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'])
if __name__=='__main__':main()
