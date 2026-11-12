#!/usr/bin/env python3
"""Direct full19-arrival adjoint check, separate from column elimination."""
import argparse,gzip,hashlib,json
from fractions import Fraction as F
from pathlib import Path
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'

def need(ok,msg):
 if not ok:raise ValueError(msg)

def add(a,b,c=F(1)):
 for k,v in tuple(b.items()):
  t=a.get(k,F(0))+c*v
  if t:a[k]=t
  else:a.pop(k,None)

def check(w,record,wrong=False,extra=()):
 ops=w['program'];arrivals=record['arrival_observations'];allowed={16,35,127,318}|set(extra)
 # Explicit candidate identity, with output indices authenticated against actual source events below.
 D={129:{13:F(-1,2),14:F(-1)},150:{13:F(-1,2),14:F(-1)},189:{10:F(-1,2),13:F(-1),16:F(-1,4),17:F(-1)},215:{10:F(1,2),13:F(2),16:F(1,4),17:F(2)}}
 if wrong:D[189]={i:-c for i,c in D[189].items()}
 adj={r:{i:-c for i,c in row.items()} for r,row in D.items()};loc=dict(enumerate(w['initial']))
 for e in ops:
  if e[0]=='INIT':loc[e[1]]=e[2]
  elif e[0]=='CLEAR':loc.pop(e[1])
  elif e[0]=='MOVE':need(loc[e[1]]==e[2],'forward chart authentication');loc[e[1]]=e[3]
 for r in D:need(loc[r]!=127,'dual uses real offhub endpoint')
 timed={x['event']:(i,x) for i,x in enumerate(arrivals)};tested=0;first=None
 def test(cut,r):
  nonlocal tested,first
  if loc[r] not in allowed:return
  tested+=1
  if adj.get(r) and first is None:first=dict(cut=cut,role=r,chart=loc[r],residual=[[i,str(c)] for i,c in sorted(adj[r].items())])
 for r in loc:test(len(ops),r)
 for t in range(len(ops)-1,-1,-1):
  e=ops[t];kind,r=e[:2];changed=set()
  if t in timed:
   i,x=timed[t];need(e[0]=='MOVE' and e[1]==x['role'] and e[3]==x['chart']==loc[x['role']],'actual complete arrival version')
   add(adj.setdefault(x['role'],{}),{i:F(1)});changed.add(x['role'])
  if kind in ('ADD','COPY'):
   s,c,at=e[2:];need(loc[r]==loc[s]==at,'source arithmetic chart');add(adj.setdefault(s,{}),adj.get(r,{}),F(c));changed.add(s)
   if kind=='COPY':adj[r]={};changed.add(r)
  elif kind=='SCALE':adj[r]={i:F(e[2])*c for i,c in adj.get(r,{}).items() if F(e[2])*c};changed.add(r)
  elif kind=='MOVE':need(loc[r]==e[3],'reverse MOVE source');loc[r]=e[2];changed.add(r)
  elif kind=='INIT':need(loc[r]==e[2],'reverse INIT');loc.pop(r);adj[r]={};changed.discard(r)
  elif kind=='CLEAR':need(r not in loc,'reverse CLEAR');loc[r]=e[2];adj[r]={};changed.add(r)
  else:raise ValueError(kind)
  for r in changed:test(t,r)
 return dict(allowed_charts=sorted(allowed),checked_changed_states=tested,first_failure=first)

def main(a):
 b=a.source.read_bytes();need(hashlib.sha256(b).hexdigest()==PIN,'source SHA256');w=json.loads(gzip.decompress(b));rb=a.certificate.read_bytes();r=json.loads(rb)
 route={w['initial'][189]}|{e[3] for e in w['program'] if e[0]=='MOVE' and e[1]==189}
 obs=[dict(event=t,role=e[1],chart=e[3]) for t,e in enumerate(w['program']) if e[0]=='MOVE' and e[3] in route]
 need(obs==r['arrival_observations'] and len(obs)==19,'whole original receiver arrival family')
 need({obs[i]['event'] for i in [10,13,14,16,17]}=={37195,40835,40836,41626,41650},'explicit dual observation binding')
 good=check(w,r);need(good['first_failure'] is None,'full19 arrival factorization for all allowed control cuts')
 wrong=check(w,r,wrong=True);need(wrong['first_failure'] is not None,'wrong-sign dual rejected')
 expanded=check(w,r,extra=[901]);need(expanded['first_failure'] is not None,'added receiver chart is outside scope')
 result=dict(schema='chart318-direct-full-arrival-dual-v1',status='PASS_FULL19_ARRIVAL_FACTOR_INCLUDING_COMMON_DEPENDENT_CONTROLS',source_sha256=PIN,factor_certificate_sha256=hashlib.sha256(rb).hexdigest(),receiver=189,endpoint_roles=[129,150,189,215],correct=good,negative_wrong_sign=wrong,negative_extra_chart901=expanded,scope='The entire original receiver history response vanishes once the four listed offhub endpoints are restored, for arbitrary realized increments on live native fields at16,35,127,318. This includes common-dependent swaps and feedback with actual donor records, provided no new receiver records/access or native chronology changes are introduced.')
 a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--certificate',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
