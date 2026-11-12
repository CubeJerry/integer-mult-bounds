#!/usr/bin/env python3
import gzip,json,time
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict,Counter
B=Path('/workspace/scratch/6a77123a1d61/integer-mult-bounds');O=Path('/workspace/scratch/6a77123a1d61/worker-budget')
w=json.loads(gzip.decompress((B/'research/shared-wire-split-composition/data/final.json.gz').read_bytes()));P=w['program'];xs=w['live'];ys=[x+112 for x in xs];n=w['public'];zero=F(0);one=F(1);start=time.monotonic()
sp=[];first={};canon=[]
for i,f in enumerate(w['frames']):
 s={0}
 for v in f:s.update(x^v for x in tuple(s))
 s=frozenset(s);first.setdefault(s,i);canon.append(first[s]);sp.append(s)
routes={y:{canon[w['initial'][y]]} for y in ys}
for e in P:
 if e[0]=='MOVE' and e[1] in routes:routes[e[1]].add(canon[e[3]])
observe=defaultdict(list)
for i,y in enumerate(ys):
 for c in routes[y]:observe[c].append(i)
initial=[{j for j,c in enumerate(w['initial']) if canon[c] in routes[y]} for y in ys]
common_initial=set.intersection(*initial);unknown=set(range(n))-common_initial
print('common initial',len(common_initial),'quotient columns',len(unknown),'initial counts',dict(Counter(map(len,initial))),flush=True)
rows=[({j:one} if j in unknown else {}) for j in range(n+w['owned_fields'])];obs=[[] for _ in ys];loc=dict(enumerate(w['initial']));scalars={str(c):F(c) for e in P for c in ([e[3]] if e[0] in('ADD','COPY') else [e[2]] if e[0]=='SCALE' else [])}
starts={28105:0,30806:1,32554:2,34446:3,36891:4,30629:5,38222:6,40087:7};prior={};guard=[]
def axpy(a,b,c):
 for j,v in tuple(b.items()):
  z=a.get(j,zero)+c*v
  if z:a[j]=z
  else:a.pop(j,None)
for t,e in enumerate(P):
 op,j=e[:2]
 if t in starts:
  prior[t]={k-n:str(v) for k,v in rows[j].items() if k>=n};rows[j][n+starts[t]]=rows[j].get(n+starts[t],zero)+1
 if op=='ADD':axpy(rows[j],rows[e[2]],scalars[str(e[3])])
 elif op=='COPY':
  guard.append({'event':t,'target_response':{str(k):str(v) for k,v in rows[j].items()}});assert not rows[j];rows[j]={k:v*scalars[str(e[3])] for k,v in rows[e[2]].items()}
 elif op=='SCALE':c=scalars[str(e[2])];rows[j]={k:c*v for k,v in rows[j].items()}
 elif op=='INIT':rows[j]={};loc[j]=e[2]
 elif op=='CLEAR':rows[j]={};loc.pop(j)
 elif op=='MOVE':
  assert loc[j]==e[2];loc[j]=e[3]
  if canon[e[3]] in observe:
   rr=rows[j].copy()
   for i in observe[canon[e[3]]]:obs[i].append({'event':t,'role':j,'chart':e[3],'row':rr})
 if t%15000==0:print('replay',t,'sec',round(time.monotonic()-start,3),flush=True)
print('replayed','sec',round(time.monotonic()-start,3),'arrivals',sum(map(len,obs)),flush=True)
def reduce_with(row,pivots):
 z=row.copy();co={}
 for k in sorted(pivots):
  if k in z:
   v=z[k];a,b=pivots[k];axpy(z,a,-v);axpy(co,b,-v)
 return z,co
result=[]
for i,y in enumerate(ys):
 cb={};sb={};relations=[];Frows=[];Brows=[]
 for ix,o in enumerate(obs[i]):
  rr=o['row'];f={k:v for k,v in rr.items() if k<n and k not in initial[i]};b={k-n:v for k,v in rr.items() if k>=n};Frows.append(f);Brows.append(b)
  combo={ix:one};z=f.copy()
  for p in sorted(cb):
   if p in z:
    v=z[p];ff,bb,cc=cb[p];axpy(z,ff,-v);axpy(b,bb,-v);axpy(combo,cc,-v)
  if z:
   p=min(z);v=z[p];cb[p]=({k:x/v for k,x in z.items()},{k:x/v for k,x in b.items()},{k:x/v for k,x in combo.items()})
  else:
   relations.append({'response':{str(k):str(v) for k,v in b.items()},'arrival_coefficients':{str(k):str(v) for k,v in combo.items()}})
   z=b.copy();cc=combo.copy()
   for p in sorted(sb):
    if p in z:
     v=z[p];bb,dd=sb[p];axpy(z,bb,-v);axpy(cc,dd,-v)
   if z:
    p=min(z);v=z[p];sb[p]=({k:x/v for k,x in z.items()},{k:x/v for k,x in cc.items()})
 target={k-n:v for k,v in rows[y].items() if k>=n};z=target.copy();cc={}
 for p in sorted(sb):
  if p in z:
   v=z[p];bb,dd=sb[p];axpy(z,bb,-v);axpy(cc,dd,v)
 decoded=not z
 rec={'donor':xs[i],'receiver':y,'initial_count':len(initial[i]),'arrivals':len(obs[i]),'quotient_common_rank':len(cb),'nullity':len(obs[i])-len(cb),'pure_pulse_rank':len(sb),'target_pulse_row':{str(k):str(v) for k,v in target.items()},'target_decodable':decoded,'target_remainder':{str(k):str(v) for k,v in z.items()},'relations':relations}
 if decoded:
  verify={}
  for ix,c in cc.items():axpy(verify,obs[i][ix]['row'],c)
  assert {k-n:v for k,v in verify.items() if k>=n}==target
  assert all(k in initial[i] for k in verify if k<n)
  rec['extraction']={'arrival_terms':[{'after_event':obs[i][ix]['event'],'role':obs[i][ix]['role'],'chart':obs[i][ix]['chart'],'coefficient':str(c)} for ix,c in sorted(cc.items())],'initial_terms':[{'role':k,'chart':w['initial'][k],'coefficient':str(-v)} for k,v in sorted(verify.items()) if k<n]}
 result.append(rec)
 if i%20==0:print('receiver',i,'decodable',sum(x['target_decodable'] for x in result),'pulse ranks',dict(Counter(x['pure_pulse_rank'] for x in result)),flush=True)
out={'status':'EXACT_EIGHT_OWNED_PULSE_HISTORY_TEST','source_sha256':'2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883','pulses':starts,'common_initial_quotient':sorted(common_initial),'initial_quotient_columns':len(unknown),'copy_guard':guard,'prior_pulse_responses':prior,'receivers':result,'decodable_count':sum(x['target_decodable'] for x in result),'pure_pulse_rank_histogram':dict(Counter(x['pure_pulse_rank'] for x in result)),'scope':'Exact linear history information gate with all initial values and all MOVE arrivals on every original receiver chart granted. Does not implement physical observation accumulation, paid extraction, restoration or complete native.'}
(O/'OWNED-HISTORY-EXTRACT.json').write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items() if k in ('decodable_count','pure_pulse_rank_histogram','prior_pulse_responses')},flush=True)
