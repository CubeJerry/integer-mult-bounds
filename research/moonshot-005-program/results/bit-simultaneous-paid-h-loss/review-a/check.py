#!/usr/bin/env python3
"""Independent raw-owner census and integer-root interval review of joint paid losses."""
from argparse import ArgumentParser
from collections import Counter,defaultdict
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import gzip,hashlib,itertools,json

def need(ok,text):
 if not ok:raise ValueError(text)
@lru_cache(None)
def power(n):
 scale=10**35;N=n**199*scale**200;x=1<<((N.bit_length()+199)//200)
 while True:
  y=(199*x+N//(x**199))//200
  if y>=x:break
  x=y
 while x**200>N:x-=1
 while (x+1)**200<=N:x+=1
 need(x**200<=N<(x+1)**200,'exact integer-root enclosure')
 return F(x,scale),F(x+1,scale)
def moment(h):
 lo=hi=F(0)
 for n,c in h.items():
  l,u=power(n);lo+=c*(l if c>=0 else u);hi+=c*(u if c>=0 else l)
 return lo,hi
def add(out,scale,h):
 for n,c in h.items():out[n]+=scale*c

def main(repo,out):
 out.mkdir(parents=True,exist_ok=True);base=repo/'research/moonshot-005-program/results';here=Path(__file__).parent
 pins=here/'SOURCE-PINS.json'
 if pins.exists():
  for p,d in json.loads(pins.read_text()).items():need(hashlib.sha256((repo/p).read_bytes()).hexdigest()==d,'source pin '+p)
 layout=json.loads(gzip.decompress((base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz').read_bytes()));owned={};quotas=Counter();groups=defaultdict(set)
 for line in gzip.decompress((base/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz').read_bytes()).splitlines():
  phase,j,x,h,d,target,source,extra=json.loads(line)
  if phase!='X' or h is None:continue
  key=(j,int(x));need(source==j and key not in owned,'genuine original owner assigned once');owned[key]=h;groups[h].add(key);quotas[h,j]+=1
 need(set(owned)=={(j,x) for j in range(111) for x in range(480)},'exact53280-owner frontier')
 doubles=[];singles=[];profiles=Counter();graph=defaultdict(set)
 for h,ds in enumerate(layout['A2']):
  if not all(j<111 for j in ds):continue
  pp=tuple(sorted(quotas[h,j] for j in ds));profiles[pp]+=1
  if pp==(30,30,30):
   doubles.append(h)
   for j in ds:graph[('h',h)].add(('x',j));graph[('x',j)].add(('h',h))
  if pp==(15,15,15):singles.append(h)
 need(profiles=={(30,30,30):65,(15,15,15):816},'native same-quota census')
 visited=set();components=[]
 for start in graph:
  if start in visited:continue
  pending=[start];part=set()
  while pending:
   x=pending.pop()
   if x in part:continue
   part.add(x);pending.extend(graph[x]-part)
  visited|=part;components.append(part)
 degrees=Counter(len(v) for k,v in graph.items() if k[0]=='x');need(len(components)==1 and len(graph)==158 and degrees=={1:32,2:30,3:21,4:10},'actual double-quota incidence graph')
 # Independent four-bit control with an invertible triangular original preparation.
 fibres=defaultdict(list)
 for x in itertools.product([0,1],repeat=4):
  z=(x[0],x[0]^x[1],x[1]^x[2],x[2]^x[3]);retained=(z[0]^z[1],z[2]^z[3]);fibres[retained].append((x,(z[1],z[3]),z[1]^z[3]))
 need(len(fibres)==4 and all(len(v)==4 and len({t for _,t,_ in v})==4 and len({p for _,_,p in v})==2 for v in fibres.values()),'nonlinear joint recovery needs two extra bits in the independent-loss control')
 # Rebuild the retained necessary screen; no price implementation is imported.
 oldN={1:1386,2:1253,3:62,4:47,5:9,6:104,7:10};oldH={2:1,4:25,6:1,8:410}
 wrapper=Counter({127:2,1:-4})
 for j in range(1,10):wrapper[7*j+1]+=4
 for j in range(1,9):wrapper[7*j]-=4
 gap=Counter();add(gap,F(36),oldH);add(gap,F(-36),oldN);add(gap,F(111),wrapper)
 allowance=Counter({127:F(37,6),64:F(37,3),1:-F(37,3)})
 for j in range(1,9):allowance[7*j+1]+=F(37,3);allowance[7*j]-=F(37,3)
 basehist=allowance.copy();add(basehist,-1,{1:F(4451,8),2:F(7213,16),4:F(24)})
 def margin(e,m,q=34560):
  h=basehist.copy();h[8]-=F(q,3840);h[6]-=F(e,3840)
  if m is not None:add(h,F(1,36*(m-1)),gap)
  return moment(h)
 transitions=[]
 for m,cap in [(870,21),(None,22)]:
  accepted=margin(8*cap,m);rejected=margin(8*(cap+1),m);all65=margin(1040,m)
  need(accepted[0]>0 and rejected[1]<0 and all65[1]<0,'exact movement-cap transition')
  transitions.append({'m':m,'maximum_eight_field_units':cap,'accepted_margin':[str(v) for v in accepted],'next_margin':[str(v) for v in rejected],'all65_margin_upper':str(all65[1])})
 need(margin(16,870,34675)[0]>0 and margin(16,870,34676)[1]<0,'exact one-defect return transition')
 result={'status':'PASS_INDEPENDENT_JOINT_H_LOSS_INFORMATION_AND_PRICE','base_original_owners':len(owned),'native_double_quota_H':doubles,'native_single_quota_count':len(singles),
  'double_quota_graph_vertices':len(graph),'double_quota_graph_components':1,'double_quota_donor_degrees':dict(degrees),'movement_transitions':transitions,'one_double_defect_return_cap_m870':34675,
  'exact_power_method':'integer200th-root bounds at10^35 scaling','new_author_code_imported':False,'fixed_frontier_information_lemma_accepted':True,'arbitrary_route_tariff_proved':False,'complete_global_source_preparation_proved':False,'new_complete_kappa':False}
 (out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(result['status'],53280,65,816,21,22,flush=True)
if __name__=='__main__':
 p=ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);z=p.parse_args();main(z.repo.resolve(),z.out.resolve())
