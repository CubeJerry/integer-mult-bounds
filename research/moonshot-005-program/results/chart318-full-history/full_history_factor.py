#!/usr/bin/env python3
"""Full-arrival extension of the reviewed chart318 null-relation control screen.

The sparse column/elimination helper is explicitly reused from math_review's
chart318-control/derive_control_word.py. We replace nine null-history outputs by
all19 actual arrivals and test whether their entire response factors through
common endpoints. This is authored source evidence, not independent review.
"""
import argparse
from fractions import Fraction as F
from pathlib import Path
from collections import defaultdict
import gzip,hashlib,json,time
SPIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def need(a,b):
 if not a:raise ValueError(b)
def axpy(dst,src,c):
 for k,v in list(src.items()) if src is dst else src.items():
  v=dst.get(k,F(0))+c*v
  if v:dst[k]=v
  else:dst.pop(k,None)
def sparse(v):return [[k,str(c)] for k,c in sorted(v.items())]
class Controls:
 def __init__(self,charts,dim):
  self.charts=set(charts);self.dim=dim;self.basis={};self.columns=[];self.seen=set();self.checked=0;self.witness=None
 def add(self,cut,role,chart,vec):
  if chart not in self.charts:return
  self.checked+=1
  key=tuple(sorted(vec.items()))
  if key in self.seen:return
  self.seen.add(key)
  if not vec:return
  idx=len(self.columns);self.columns.append({'cut':cut,'role':role,'chart':chart,'vector':vec.copy()})
  e={j:v for j,v in vec.items() if j<self.dim};n={j-self.dim:v for j,v in vec.items() if j>=self.dim};combo={idx:F(1)}
  for p in sorted(self.basis):
   if p in e:
    c=e[p];be,bn,bc=self.basis[p];axpy(e,be,-c);axpy(n,bn,-c);axpy(combo,bc,-c)
  if not e:
   if n and self.witness is None:self.witness=(combo,n)
   return
  p=min(e);v=e[p]
  self.basis[p]=({j:c/v for j,c in e.items()},{j:c/v for j,c in n.items()},{j:c/v for j,c in combo.items()})
 def finish(self):
  r={'allowed_charts':sorted(self.charts),'checked_changed_states':self.checked,'unique_nonzero_columns':len(self.columns),'endpoint_guard_rank':len(self.basis)}
  if self.witness is not None:
   combo,gain=self.witness;sumvec={};word=[]
   for i,c in sorted(combo.items()):
    col=self.columns[i];axpy(sumvec,col['vector'],c)
    word.append({k:v for k,v in col.items() if k!='vector'}|{'coefficient':str(c)})
   need(not any(j<self.dim for j in sumvec),'exact endpoint/guard neutral word')
   r.update({'status':'CONSTRUCTED_NEUTRAL_HISTORY_CONTROL','word':sorted(word,key=lambda a:(a['cut'],a['role'])),'history_gain':sparse(gain)})
  else:
   dual={}
   for p in sorted(self.basis,reverse=True):
    e,n,_=self.basis[p];v=n.copy()
    for j,c in e.items():
     if j!=p:axpy(v,dual.get(j,{}),-c)
    if v:dual[p]=v
   for col in self.columns:
    v={}
    for j,c in col['vector'].items():
     if j<self.dim:axpy(v,dual.get(j,{}),c)
    need(v=={j-self.dim:c for j,c in col['vector'].items() if j>=self.dim},'history responses factor through endpoints/guard')
   r.update({'status':'PROVED_ZERO_ATTAINABLE_NEUTRAL_GAIN','endpoint_guard_dual':[[j,sparse(v)] for j,v in sorted(dual.items())]})
  return r

def main(a):
 start=time.monotonic();raw=a.source.read_bytes();need(hashlib.sha256(raw).hexdigest()==SPIN,'source pin');w=json.loads(gzip.decompress(raw));ops=w['program']
 route={w['initial'][189]}|{e[3] for e in ops if e[0]=='MOVE' and e[1]==189};known={i for i,s in enumerate(w['initial']) if s in route}
 arrivals=[dict(event=t,role=e[1],chart=e[3]) for t,e in enumerate(ops) if e[0]=='MOVE' and e[3] in route]
 need(len(known)==1046 and len(arrivals)==19,'complete source receiver history')
 loc=dict(enumerate(w['initial']))
 for e in ops:
  if e[0]=='MOVE':need(loc[e[1]]==e[2],'source location');loc[e[1]]=e[3]
  elif e[0]=='INIT':loc[e[1]]=e[2]
  elif e[0]=='CLEAR':loc.pop(e[1])
 offhub=[r for r in range(1480) if loc[r]!=127]
 need([t for t,e in enumerate(ops) if e[0]=='COPY']==[31737],'unique source COPY guard')
 constraints=[dict(kind='final_public',role=r,chart=loc[r]) for r in offhub]+[dict(kind='pre_COPY_guard',event=31737,role=ops[31737][1])]
 d=len(constraints);adj={r:{i:F(1)} for i,r in enumerate(offhub)};obs={x['event']:(i,x) for i,x in enumerate(arrivals)}
 scopes={'chart318':Controls([318],d),'donor17_detour':Controls([16,318,127],d),'donor38_detour':Controls([35,318,127],d),'joint_detours':Controls([16,35,318,127],d)}
 for r,chart in loc.items():
  for c in scopes.values():c.add(len(ops),r,chart,adj.get(r,{}))
 scalars={}
 for t in range(len(ops)-1,-1,-1):
  e=ops[t];op,r=e[:2];changed=set()
  if t in obs:
   i,o=obs[t];need(loc[o['role']]==o['chart'],'actual arrival cut');axpy(adj.setdefault(o['role'],{}),{d+i:F(1)},F(1));changed.add(o['role'])
  if op in ('ADD','COPY'):
   s,c,chart=e[2:];c=scalars.setdefault(c,F(c));need(loc[r]==loc[s]==chart,'source cochart arithmetic');axpy(adj.setdefault(s,{}),adj.get(r,{}),c);changed.add(s)
   if op=='COPY':adj[r]={len(offhub):F(1)};changed.add(r)
  elif op=='SCALE':
   c=scalars.setdefault(e[2],F(e[2]));adj[r]={k:c*v for k,v in adj.get(r,{}).items() if c*v};changed.add(r)
  elif op=='MOVE':need(loc[r]==e[3],'reverse source MOVE');loc[r]=e[2];changed.add(r)
  elif op=='INIT':need(loc[r]==e[2],'reverse source INIT');loc.pop(r);adj[r]={};changed.discard(r)
  elif op=='CLEAR':need(r not in loc,'reverse source CLEAR');loc[r]=e[2];adj[r]={};changed.add(r)
  else:raise ValueError(op)
  for r in changed:
   for c in scopes.values():c.add(t,r,loc[r],adj.get(r,{}))
  if t%15000==0:print('reverse',t,'seconds',round(time.monotonic()-start,2),'endpoint ranks',{k:len(c.basis) for k,c in scopes.items()},flush=True)
 results={k:c.finish() for k,c in scopes.items()}
 record=dict(schema='chart318-full-arrival-factor-v1',source_sha256=SPIN,receiver=189,receiver_itinerary_charts=sorted(route),initial_common_units=len(known),arrival_observations=arrivals,constraints=constraints,scopes=results,scope='Complete actual arrival responses, not merely old null relations. If factorization passes, every realized common-dependent control word at the declared stations with restored offhub endpoints and valid COPY guard leaves all original receiver histories unchanged. Changed receiver access, additional raw records at receiver, altered native chronology, and other control charts are outside scope.')
 a.output.write_text(json.dumps(record,indent=2,sort_keys=True)+'\n');print(json.dumps({k:v for k,v in record.items() if k not in ('constraints','arrival_observations')},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
