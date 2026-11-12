#!/usr/bin/env python3
"""Independent full-history endpoint dual, including realized feedback increments."""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
import gzip,json,hashlib
BASE=Path('/workspace/scratch/6a77123a1d61');REPO=BASE/'integer-mult-bounds';PACK=BASE/'worker-coupling/chart318-swaps';OUT=Path(__file__).resolve().parent
SPIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883';FPIN='ef19dd321bb036a69e88e091983081f0dbba5694b5111d79de0c610f046e5540';PROOF='bbea2eaf4db1be40c32ac0eba486d5e8d40759126bb48112ac71fff32ec67339'
def need(b,m):
 if not b:raise ValueError(m)
def digest(b):return hashlib.sha256(b).hexdigest()
def add(a,b,c=F(1)):
 for k,v in b.items():
  q=a.get(k,F(0))+c*v
  if q:a[k]=q
  else:a.pop(k,None)
def span(fr):
 a={0}
 for v in fr:a.update(x^v for x in tuple(a))
 return a

def trace(source,observations,dual,allowed):
 P=source['program'];adj=[{} for _ in range(source['public']+source['owned_fields'])];loc=dict(enumerate(source['final']));timed={o['event']:(i,o) for i,o in enumerate(observations)}
 for i,row in dual.items():
  for r,c in row.items():add(adj[r],{i:-c})
 checked=0;first=None
 def inspect(j,cut,phase):
  nonlocal checked,first
  if j not in loc or loc[j] not in allowed:return
  checked+=1
  if adj[j] and first is None:first={'cut':cut,'phase':phase,'role':j,'chart':loc[j],'residual':{str(i):str(c) for i,c in sorted(adj[j].items())}}
 for j in loc:inspect(j,len(P),'final')
 for e in range(len(P)-1,-1,-1):
  o=P[e];kind,j=o[:2];changed=set()
  if e in timed:
   i,t=timed[e];need(kind=='MOVE' and j==t['role'] and o[3]==t['chart']==loc[j],'actual post-MOVE observation version')
   add(adj[j],{i:F(1)});inspect(j,e,'post-MOVE-before-sample');changed.add(j)
  if kind in ('ADD','COPY'):
   need(loc[j]==loc[o[2]]==o[4],'native actual cochart');add(adj[o[2]],adj[j],F(o[3]));changed.add(o[2])
   if kind=='COPY':adj[j]={};changed.add(j)
  elif kind=='SCALE':adj[j]={i:F(o[2])*c for i,c in adj[j].items()};changed.add(j)
  elif kind=='MOVE':need(loc[j]==o[3],'reverse source MOVE');loc[j]=o[2];changed.add(j)
  elif kind=='CLEAR':need(j not in loc,'reverse CLEAR');loc[j]=o[2];adj[j]={};changed.add(j)
  elif kind=='INIT':need(loc[j]==o[2],'reverse INIT');del loc[j];adj[j]={};changed.discard(j)
  else:raise ValueError(kind)
  for j in changed:inspect(j,e,'before-source-event')
 need([loc[j] for j in range(source['public'])]==source['initial'],'backward source initial charts')
 return {'allowed_charts':sorted(allowed),'checked_changed_states':checked,'first_failure':first,'initial_residual_nonzero_roles':sum(bool(r) for r in adj)}

def main():
 sb=(REPO/'research/shared-wire-split-composition/data/final.json.gz').read_bytes();need(digest(sb)==SPIN,'source pin');s=json.loads(gzip.decompress(sb));fb=(PACK/'FULL-HISTORY-FACTOR.json').read_bytes();need(digest(fb)==FPIN,'factor certificate pin');factor=json.loads(fb);need(digest((PACK/'PROOF.md').read_bytes())==PROOF,'frozen mathematical scope')
 P=s['program'];route=[s['initial'][189]]+[o[3] for o in P if o[0]=='MOVE' and o[1]==189];need(route==[3,307,901,198],'actual receiver route')
 obs=[{'event':e,'role':o[1],'chart':o[3]} for e,o in enumerate(P) if o[0]=='MOVE' and o[3] in route];need(obs==factor['arrival_observations'] and len(obs)==19,'all original receiver arrivals, without omission')
 known=[j for j,c in enumerate(s['initial']) if c in route];need(len(known)==1046 and all(s['initial'][j]==3 for j in known),'all original initial common observations')
 allowed={16,35,127,318};need(not (allowed&set(route)),'no inserted control acts at a receiver observation chart')
 formulas={37195:{215:F(1,2),189:F(-1,2)},40835:{129:F(-1,2),150:F(-1,2),189:F(-1),215:F(2)},40836:{129:F(-1),150:F(-1)},41626:{215:F(1,4),189:F(-1,4)},41650:{189:F(-1),215:F(2)}}
 need({o['event']:o['role'] for o in obs if o['event'] in formulas}=={37195:979,40835:215,40836:484,41626:953,41650:189},'binding every displayed coefficient to an actual source sample')
 dual={i:formulas.get(o['event'],{}) for i,o in enumerate(obs)};need({r:s['final'][r] for r in (129,150,189,215)}=={129:143,150:162,189:198,215:223},'four actual offhub endpoints')
 good=trace(s,obs,dual,allowed);need(good['first_failure'] is None and good['checked_changed_states']==28292,'all admitted source-control columns annihilate all19 residuals')
 need(good['initial_residual_nonzero_roles']>0,'formula is for differences, not an incorrect absolute history identity')
 wrong={i:{r:(-c if r==189 else c) for r,c in row.items()} for i,row in dual.items()};bad=trace(s,obs,wrong,allowed);need(bad['first_failure'] is not None,'wrong sign detected')
 extra=trace(s,obs,dual,allowed|{901});need(extra['first_failure'] is not None,'additional receiver chart violates admitted dual')
 # Independent chronological perturbation replay at the genuine changed-O cut.
 pulse={};loc=dict(enumerate(s['initial']));hist={};copy=[]
 for e,o in enumerate(P):
  kind,j=o[:2]
  if e==40835:need(j==215 and kind=='MOVE' and loc[j]==318,'actual overwrite source cut');pulse[j]=pulse.get(j,F(0))+1
  if kind=='INIT':pulse[j]=F(0);loc[j]=o[2]
  elif kind=='CLEAR':pulse.pop(j,None);del loc[j]
  elif kind=='MOVE':need(loc[j]==o[2],'forward pulse chart');loc[j]=o[3]
  elif kind=='ADD':pulse[j]=pulse.get(j,F(0))+F(o[3])*pulse.get(o[2],F(0))
  elif kind=='COPY':copy.append((e,pulse.get(j,F(0))));pulse[j]=F(o[3])*pulse.get(o[2],F(0))
  elif kind=='SCALE':pulse[j]=F(o[2])*pulse.get(j,F(0))
  else:raise ValueError(kind)
  if e in {o['event'] for o in obs}:hist[e]=pulse.get(j,F(0))
 end={j:c for j,c in pulse.items() if c};need(end.get(189)==end.get(215)==1 and all(not v for e,v in copy),'nonneutral changed-O pulse and COPY response')
 for o in obs:need(hist[o['event']]==sum(c*end.get(r,F(0)) for r,c in formulas.get(o['event'],{}).items()),'separate forward pulse checks full four-endpoint response identity')
 need(hist[40835]==1,'overwriting with q makes this arrival a pure q value before restoration')
 need(span(s['frames'][318])=={0,51,81,98} and span(s['frames'][16])=={0,81} and span(s['frames'][35])=={0,98},'actual donor17/38 detour geometry')
 need(s['initial'][17]==16 and s['initial'][38]==35 and s['final'][17]==s['final'][38]==127,'actual donor endpoints')
 result={'status':'PASS_INDEPENDENT_COMPLETE_HISTORY_FACTOR_FOR_REALIZED_FEEDBACK','source_sha256':SPIN,'factor_sha256':FPIN,'reviewed_proof_sha256':PROOF,'receiver':189,'receiver_route':route,'initial_observations':1046,'complete_arrivals':19,'allowed_source_control_charts':sorted(allowed),'restoration_endpoint_roles':[129,150,189,215],'exact_nonzero_arrival_coefficients':{str(e):{str(r):str(c) for r,c in row.items()} for e,row in formulas.items()},'other_arrival_differences_identically_zero':14,'correct_dual':good,'negative_wrong_endpoint_sign':bad,'negative_added_receiver_chart':extra,'forward_changed_matrix_control':{'before_event':40835,'role':215,'chart':318,'nonzero_arrival_response':{str(e):str(v) for e,v in hist.items() if v},'nonzero_final_response':{str(j):str(c) for j,c in end.items()}},'mathematical_scope':'For arbitrary realized increments on live native fields at the admitted charts, fixed native linear propagation gives history differences B delta and final endpoint differences A delta. The checked control-column identity B=D A implies exact original-history restoration whenever the four endpoints are restored, even if increments depend on common inputs or feedback. No fixed-O assumption is needed for constructing these increments.','excluded_interfaces':'Additional receiver raw/common records, new receiver charts, other source-control charts or altered native processing are not covered. Receiver initial observations precede controls. This is a source difference identity, not an absolute baseline history equation or a numeric paid-call lower bound.','review_method':'Separate exact19-residual source adjoints, complete source observation/geometry audit and separate forward pulse. No author code or earlier column-elimination helper imported. The24-cut exploratory swap-rank census is not independently audited by this checker.'}
 (OUT/'REVIEW-RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
