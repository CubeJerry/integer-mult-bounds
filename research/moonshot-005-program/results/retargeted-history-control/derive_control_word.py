#!/usr/bin/env python3
"""Exact endpoint/guard controllability with receiver189 history gains."""
from fractions import Fraction as F
from pathlib import Path
from collections import defaultdict
import gzip,hashlib,json,time
BASE=Path('/workspace/scratch/6a77123a1d61')
SRC=BASE/'integer-mult-bounds/research/shared-wire-split-composition/data/final.json.gz'
HIST=BASE/'integer-mult-bounds/research/moonshot-005-program/results/joint-additive-history-obstruction/CERTIFICATE.json'
OUT=Path(__file__).resolve().parent
SPIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
HPIN='168fee8f09cdf0f33bcf5989630d244141d3c570808b7ccb553f6ad7be098dd7'
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

def main():
 start=time.monotonic();raw=SRC.read_bytes();need(hashlib.sha256(raw).hexdigest()==SPIN,'source pin');w=json.loads(gzip.decompress(raw))
 raw=HIST.read_bytes();need(hashlib.sha256(raw).hexdigest()==HPIN,'history pin');h=json.loads(raw)
 need(h['source_sha256']==SPIN and h['receiver']==189 and len(h['relations'])==9,'history interface')
 loc=dict(enumerate(w['initial']))
 for op in w['program']:
  if op[0]=='MOVE':need(loc[op[1]]==op[2],'source location trace');loc[op[1]]=op[3]
  elif op[0]=='INIT':loc[op[1]]=op[2]
  elif op[0]=='CLEAR':del loc[op[1]]
 offhub=[j for j in range(w['public']) if loc[j]!=127]
 guards=[i for i,o in enumerate(w['program']) if o[0]=='COPY'];need(guards==[31737],'guard census')
 constraints=[{'kind':'final_public','role':j,'chart':loc[j]} for j in offhub]+[{'kind':'pre_COPY_guard','event':31737,'role':w['program'][31737][1]}]
 d=len(constraints);guardindex=len(offhub)
 adj={j:{i:F(1)} for i,j in enumerate(offhub)}
 observations=defaultdict(list)
 for i,relation in enumerate(h['relations']):
  for t in relation:observations[t['after_event']].append((t['role'],d+i,F(t['coefficient']),t['chart']))
 controls={q:Controls([w['initial'][q],318,127],d) for q in [17,38]}
 for role,chart in loc.items():
  for c in controls.values():c.add(len(w['program']),role,chart,adj.get(role,{}))
 scalars={};special=None
 for event in range(len(w['program'])-1,-1,-1):
  op=w['program'][event];kind,j=op[:2];changed=set()
  for role,index,c,chart in observations.get(event,[]):
   need(loc[role]==chart,'actual timed history observation')
   axpy(adj.setdefault(role,{}),{index:c},F(1));changed.add(role)
  if kind in ('ADD','COPY'):
   r,c,chart=op[2:];c=scalars.setdefault(c,F(c));need(loc[j]==loc[r]==chart,'native arithmetic location')
   axpy(adj.setdefault(r,{}),adj.get(j,{}),c);changed.add(r)
   if kind=='COPY':
    adj[j]={guardindex:F(1)};changed.add(j)
  elif kind=='SCALE':
   c=scalars.setdefault(op[2],F(op[2]));adj[j]={k:c*v for k,v in adj.get(j,{}).items() if c*v};changed.add(j)
  elif kind=='MOVE':
   need(loc[j]==op[3],'reverse source MOVE');loc[j]=op[2];changed.add(j)
  elif kind=='INIT':
   need(loc[j]==op[2],'reverse source INIT');del loc[j];adj[j]={};changed.discard(j)
  elif kind=='CLEAR':
   need(j not in loc,'reverse source CLEAR');loc[j]=op[2];adj[j]={};changed.add(j)
  else:raise ValueError(kind)
  for role in changed:
   for c in controls.values():c.add(event,role,loc[role],adj.get(role,{}))
  if event==37195:special={'cut':event,'role':979,'chart':loc[979],'endpoint_guard_response':[[constraints[k],str(v)] for k,v in sorted(adj[979].items()) if k<d],'history_response':[[k-d,str(v)] for k,v in sorted(adj[979].items()) if k>=d]}
  if event%15000==0:print('REVERSE',event,'seconds',round(time.monotonic()-start,2),'basis',[len(c.basis) for c in controls.values()],flush=True)
 for role,index,c,chart in observations[-1]:
  need(w['initial'][role]==chart,'actual initial history observation');axpy(adj.setdefault(role,{}),{index:c},F(1))
 need(all(not any(k>=d for k in row) for row in adj.values()),'all nine histories are exact zero-baseline relations on every common input')
 results={str(q):c.finish() for q,c in controls.items()}
 report={'source_sha256':SPIN,'history_certificate_sha256':HPIN,'receiver':189,'constraints':constraints,'guard_count':len(guards),'history_relations':9,'selected_control':special,'donors':results,'scope':'All linear additive controls at all cuts on native live fields at the three donor-specific charts. Requires every offhub public endpoint and pre-COPY target unchanged. Hub final debts may be repaired with the pure donor cache at127. No route, recorder or supplier cost follows from a control-space result.'}
 payload=(json.dumps(report,sort_keys=True,indent=2)+'\n').encode();(OUT/'RESULT.json').write_bytes(payload)
 print(json.dumps({'result_sha256':hashlib.sha256(payload).hexdigest(),'selected_control':special,'donors':results},indent=2),flush=True)
if __name__=='__main__':main()
