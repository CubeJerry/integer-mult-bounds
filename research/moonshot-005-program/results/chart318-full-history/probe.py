#!/usr/bin/env python3
"""Source-exact single-overwrite interface screen at changed donor chart318."""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict,Counter
import argparse,json,gzip,hashlib
BASE=Path('/workspace/scratch/6a77123a1d61')
SOURCE=BASE/'integer-mult-bounds/research/shared-wire-split-composition/data/final.json.gz'
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
OUT=Path(__file__).resolve().parent

def need(ok,msg):
 if not ok:raise ValueError(msg)

def add(a,b,c=F(1)):
 for k,v in tuple(b.items()):
  z=a.get(k,F(0))+c*v
  if z:a[k]=z
  else:a.pop(k,None)

def ser(a):return [[k,str(v)] for k,v in sorted(a.items())]

def main(a):
 blob=a.source.read_bytes();need(hashlib.sha256(blob).hexdigest()==PIN,'source pin');w=json.loads(gzip.decompress(blob));ops=w['program']
 route={w['initial'][189]}|{e[3] for e in ops if e[0]=='MOVE' and e[1]==189}
 known={i for i,s in enumerate(w['initial']) if s in route};need(len(known)==1046,'initial common receiver grant')
 loc=dict(enumerate(w['initial']));candidates=[];cuts=defaultdict(list)
 for t,e in enumerate(ops):
  touched={e[1],e[2]} if e[0] in ('ADD','COPY') else {e[1]}
  for r in sorted(touched):
   if loc.get(r)==318:
    j=len(candidates);candidates.append(dict(cut=t,role=r,chart=318,next_operation=e));cuts[t].append((j,r))
  if e[0]=='INIT':loc[e[1]]=e[2]
  elif e[0]=='CLEAR':loc.pop(e[1])
  elif e[0]=='MOVE':loc[e[1]]=e[3]
 for r,s in sorted(loc.items()):
  if s==318:
   j=len(candidates);candidates.append(dict(cut=len(ops),role=r,chart=318,next_operation=None));cuts[len(ops)].append((j,r))
 print('candidate cuts',len(candidates),flush=True)
 values={i:({i:F(1)} if i not in known else {}) for i in range(1480)};pulse={i:{} for i in range(1480)}
 payloads={};observations=[];guards=[]
 for t,e in enumerate(ops):
  for j,r in cuts[t]:payloads[j]=values[r].copy();pulse[r][j]=F(1)
  op,r=e[:2]
  if op=='INIT':values[r]={};pulse[r]={}
  elif op=='CLEAR':values.pop(r);pulse.pop(r)
  elif op=='SCALE':values[r]={k:F(e[2])*v for k,v in values[r].items()};pulse[r]={k:F(e[2])*v for k,v in pulse[r].items()}
  elif op in ('ADD','COPY'):
   if op=='COPY':need(not values[r],'baseline quotient guard');guards.append((t,pulse[r].copy()))
   add(values[r],values[e[2]],F(e[3]));add(pulse[r],pulse[e[2]],F(e[3]))
  elif op=='MOVE' and e[3] in route:observations.append(dict(event=t,role=r,chart=e[3],common=values[r].copy(),response=pulse[r].copy()))
 for j,r in cuts[len(ops)]:payloads[j]=values[r].copy();pulse[r][j]=F(1)
 need(len(observations)==19,'complete receiver arrival grant')
 basis={}
 for i,o in enumerate(observations):
  row=o['common'].copy();comb={i:F(1)}
  for pivot,(v,cc) in sorted(basis.items()):
   c=row.get(pivot,F(0));add(row,v,-c);add(comb,cc,-c)
  if row:
   pivot=min(row);c=row[pivot];basis[pivot]=({j:v/c for j,v in row.items()},{j:v/c for j,v in comb.items()})
 need(len(basis)==10,'source receiver common quotient rank')
 records=[]
 for j,item in enumerate(candidates):
  z={r:row[j] for r,row in pulse.items() if j in row};b={i:o['response'][j] for i,o in enumerate(observations) if j in o['response']};h=payloads[j]
  guard={t:row[j] for t,row in guards if j in row};outside={r:c for r,c in z.items() if w['final'][r]!=127}
  remainder=h.copy();decoder={}
  for pivot,(v,cc) in sorted(basis.items()):
   c=remainder.get(pivot,F(0));add(remainder,v,-c);add(decoder,cc,c)
  beta=sum(c*b.get(i,F(0)) for i,c in decoder.items()) if not remainder else None
  # Recompute rank([O-bh,b]) and rank(O-bh) directly, including all known initial columns quotiented out.
  changed=[];extended=[]
  for i,o in enumerate(observations):
   row=o['common'].copy();add(row,h,-b.get(i,F(0)));changed.append(row)
   ext=row.copy()
   if b.get(i):ext[2000]=b[i]
   extended.append(ext)
  def rank(rows):
   bs={}
   for rr in rows:
    rr=rr.copy()
    for p,v in sorted(bs.items()):add(rr,v,-rr.get(p,F(0)))
    if rr:
     p=min(rr);c=rr[p];bs[p]={k:v/c for k,v in rr.items()}
   return len(bs)
  cr=rank(changed);er=rank(extended)
  records.append(dict(**item,guard_response=ser(guard),offhub_response=ser(outside),hub_response=ser({r:c for r,c in z.items() if r not in outside}),receiver_arrival_response=ser(b),payload_mod_initial_support=len(h),payload_in_original_receiver_span=not remainder,beta=None if beta is None else str(beta),payload_remainder=ser(remainder),original_history_quotient_rank=10,changed_history_quotient_rank=cr,changed_history_plus_q_rank=er,pure_q_gain_rank=er-cr,neutral=not guard and not outside,payload_mod_initial=ser(h),old_history_expression=ser(decoder) if not remainder else None))
 neutral=[r for r in records if r['neutral']];positive=[r for r in neutral if r['pure_q_gain_rank']]
 result=dict(schema='chart318-single-overwrite-interface-screen-v1',source_sha256=PIN,receiver=189,allowed_swap_chart=318,original_receiver_charts=sorted(route),initial_common_units=len(known),arrival_count=len(observations),original_history_quotient_rank=10,candidate_state_cuts=len(candidates),neutral_candidates=len(neutral),neutral_receiver_response_nonzero=sum(bool(r['receiver_arrival_response']) for r in neutral),neutral_changed_O_pure_q_positive=len(positive),nonneutral_pure_q_positive=sum(bool(r['pure_q_gain_rank']) for r in records if not r['neutral']),neutral_cuts=[(r['cut'],r['role']) for r in neutral],positive_neutral_cuts=[(r['cut'],r['role']) for r in positive],observations=[{k:v for k,v in o.items() if k not in ('common','response')} for o in observations],records=records,scope='All single pure-q swaps at source state intervals on chart318; receiver gets its original common initial/arrival history. Displaced h is retained on donor raw route318->127, without receiver access to h. Offhub-neutral and COPY-valid cases tested. Multi-overwrite families, added observations and altered receiver routes are outside scope.')
 a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k not in ('records','observations')},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,default=SOURCE);p.add_argument('--output',type=Path,default=OUT/'SWAP-SCREEN.json');main(p.parse_args())
