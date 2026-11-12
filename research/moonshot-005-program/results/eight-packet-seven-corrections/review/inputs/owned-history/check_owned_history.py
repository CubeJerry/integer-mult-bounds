#!/usr/bin/env python3
"""Independent source replay, annihilator review and positive common shadows."""
from collections import Counter, defaultdict
from fractions import Fraction as F
import gzip, hashlib, json, time
from pathlib import Path
BASE=Path('/workspace/scratch/6a77123a1d61')
SOURCE=BASE/'integer-mult-bounds/research/shared-wire-split-composition/data/final.json.gz'
AUTHOR=BASE/'worker-budget/OWNED-HISTORY-EXTRACT.json'
OUT=Path(__file__).resolve().parent
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
EVENTS=[28105,30806,32554,34446,36891,30629,38222,40087]
def need(v,m):
 if not v:raise ValueError(m)
def axpy(a,b,c):
 for k,v in b.items():
  v=a.get(k,F(0))+c*v
  if v:a[k]=v
  else:a.pop(k,None)
def vadd(a,b,c):return tuple(x+c*y for x,y in zip(a,b))
def span(frame):
 s={0}
 for v in frame:s.update([x^v for x in s.copy()])
 return frozenset(s)
def rank_rows(rows):
 basis={}
 for row in rows:
  row=row.copy()
  for p in sorted(basis):
   if p in row:axpy(row,basis[p],-row[p])
  if row:
   p=min(row);v=row[p];basis[p]={k:x/v for k,x in row.items()}
 return len(basis)
def factor(rows,responses):
 """Reduced common equations and8 RHS; return positive shadows if consistent."""
 basis={};pure_basis={}
 for row,rhs in zip(rows,responses):
  row=row.copy();rhs=tuple(rhs)
  for p in sorted(basis):
   if p in row:
    c=row[p];old,b=basis[p];axpy(row,old,-c);rhs=vadd(rhs,b,-c)
  if not row:
   pure={i:v for i,v in enumerate(rhs) if v}
   for p in sorted(pure_basis):
    if p in pure:axpy(pure,pure_basis[p],-pure[p])
   if pure:
    p=min(pure);v=pure[p];pure_basis[p]={i:x/v for i,x in pure.items()}
   continue
  p=min(row);v=row[p];row={k:x/v for k,x in row.items()};rhs=tuple(x/v for x in rhs)
  for op,(old,b) in list(basis.items()):
   if p in old:
    c=old[p];axpy(old,row,-c);basis[op]=(old,vadd(b,rhs,-c))
  basis[p]=(row,rhs)
 shadow={p:b for p,(_,b) in basis.items() if any(b)} if not pure_basis else None
 if shadow is not None:
  for row,rhs in zip(rows,responses):
   result=(F(0),)*8
   for k,c in row.items():
    if k in shadow:result=vadd(result,shadow[k],c)
   need(result==rhs,'positive source-common shadow identity')
 return len(basis),len(pure_basis),shadow,pure_basis
def main():
 start=time.monotonic();raw=SOURCE.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'native source pin')
 w=json.loads(gzip.decompress(raw));ab=AUTHOR.read_bytes();a=json.loads(ab)
 need(hashlib.sha256(ab).hexdigest()=='ef743bb4846997bde8e066bc444af5532c3d3bc0b0c041b269ac92ad2a07e9f4','frozen author report')
 need(a['source_sha256']==PIN and a['pulses']=={str(e):i for i,e in enumerate(EVENTS)},'control interface')
 first={};can=[]
 for i,frame in enumerate(w['frames']):can.append(first.setdefault(span(frame),i))
 xs=w['live'];ys=[x+112 for x in xs];n=w['public'];rt={y:{can[w['initial'][y]]} for y in ys}
 for op in w['program']:
  if op[0]=='MOVE' and op[1] in rt:rt[op[1]].add(can[op[3]])
 initial=[{j for j,c in enumerate(w['initial']) if can[c] in rt[y]} for y in ys]
 common=set.intersection(*initial);union=set.union(*initial);unknown=set(range(n))-common
 need(sorted(common)==a['common_initial_quotient'] and len(common)==1046 and len(unknown)==a['initial_quotient_columns']==434,'initial quotient')
 sees=defaultdict(list)
 for i,y in enumerate(ys):
  for c in rt[y]:sees[c].append(i)
 for e in EVENTS:
  op=w['program'][e];need(op[0]=='MOVE' and op[1]>=n and op[4] is True,'owned departure')
  need(can[op[2]] not in sees,'controls avoid every receiver chart')
 baseline={j:({j:F(1)} if j in unknown else {}) for j in range(n)}
 pulse={j:(F(0),)*8 for j in range(n)};loc=dict(enumerate(w['initial']))
 arrivals=[];obs=[[] for _ in ys];ctrl={e:i for i,e in enumerate(EVENTS)};prior={};guards=[];scalars={}
 def coef(s):
  if s not in scalars:scalars[s]=F(s)
  return scalars[s]
 for event,op in enumerate(w['program']):
  kind,j=op[:2]
  if event in ctrl:
   prior[str(event)]={str(i):str(v) for i,v in enumerate(pulse[j]) if v}
   p=list(pulse[j]);p[ctrl[event]]+=1;pulse[j]=tuple(p)
  if kind=='INIT':baseline[j]={};pulse[j]=(F(0),)*8;loc[j]=op[2]
  elif kind=='CLEAR':del baseline[j],pulse[j],loc[j]
  elif kind=='SCALE':
   c=coef(op[2]);baseline[j]={k:c*v for k,v in baseline[j].items() if c*v};pulse[j]=tuple(c*v for v in pulse[j])
  elif kind in ('ADD','COPY'):
   r,c,chart=op[2:];c=coef(c);need(loc[j]==loc[r]==chart,'source cochart arithmetic')
   if kind=='COPY':
    need(not baseline[j] and not any(pulse[j]),'source quotient and all8 pulse COPY guards');guards.append(event)
   axpy(baseline[j],baseline[r],c);pulse[j]=vadd(pulse[j],pulse[r],c)
  elif kind=='MOVE':
   need(loc[j]==op[2],'source MOVE version');loc[j]=op[3]
   receivers=sees.get(can[op[3]],())
   if receivers:
    key=len(arrivals);arrivals.append({'event':event,'role':j,'chart':op[3],'F':baseline[j].copy(),'B':pulse[j]})
    for i in receivers:obs[i].append(key)
  else:raise ValueError('unknown source opcode')
  if event%15000==0:print('SOURCE',event,'seconds',round(time.monotonic()-start,2),flush=True)
 need(prior==a['prior_pulse_responses'] and all(not row for row in prior.values()),'chronological cross-effects vanish')
 need(sum(map(len,obs))==2846 and guards==[31737],'history and guard census')
 print('SOURCE_COMPLETE','seconds',round(time.monotonic()-start,2),'unique_arrivals',len(arrivals),flush=True)
 reviews=[];x_only=0;null_checks=0
 for i,y in enumerate(ys):
  records=[arrivals[j] for j in obs[i]]
  rows=[{k:v for k,v in r['F'].items() if k not in initial[i]} for r in records]
  responses=[r['B'] for r in records]
  rank,gain,shadow,_=factor(rows,responses);need(gain==0 and shadow is not None,'all8 response columns lie in actual common-history image')
  ar=a['receivers'][i];need(ar['donor']==xs[i] and ar['receiver']==y and ar['initial_count']==len(initial[i]) and ar['arrivals']==len(records),'receiver census')
  need(ar['quotient_common_rank']==rank and ar['nullity']==len(records)-rank and ar['pure_pulse_rank']==0,'independently computed receiver ranks')
  target={str(k):str(v) for k,v in enumerate(pulse[y]) if v}
  need(target and ar['target_pulse_row']==target and ar['target_remainder']==target and not ar['target_decodable'],'every requested target pulse is nonzero and unextractable')
  relation_rows=[]
  for relation in ar['relations']:
   coeffs={int(k):F(v) for k,v in relation['arrival_coefficients'].items()};need(all(0<=j<len(records) for j in coeffs),'relation indices')
   common_sum={};pulse_sum=(F(0),)*8
   for j,c in coeffs.items():axpy(common_sum,rows[j],c);pulse_sum=vadd(pulse_sum,responses[j],c)
   need(not common_sum and not any(pulse_sum) and not relation['response'],'each supplied left-null relation is exact and pulse-neutral')
   relation_rows.append(coeffs);null_checks+=1
  need(len(relation_rows)==rank_rows(relation_rows)==len(records)-rank,'full independent left-null basis')
  final_row={k:v for k,v in baseline[y].items() if k not in initial[i]}
  need(rank_rows(rows+[final_row])==rank,'final receiver endpoint lies in its initial/arrival history span')
  final_shadow=(F(0),)*8
  for k,c in final_row.items():
   if k in shadow:final_shadow=vadd(final_shadow,shadow[k],c)
  need(final_shadow==pulse[y],'stable endpoint pulse is reproduced by the same common shadow')
  xr=[{k:v for k,v in row.items() if k in xs} for row in rows]
  xrank,xgain,xshadow,_=factor(xr,responses)
  if xgain==0:x_only+=1
  reviews.append({'donor':xs[i],'receiver':y,'initial_count':len(initial[i]),'arrivals':len(records),'common_rank':rank,'nullity':len(records)-rank,'pure_pulse_rank':gain,'shadow_rows':[[k,list(map(str,v))] for k,v in sorted(shadow.items())],'shadow_input_rows':len(shadow),'X_only_shadow_exists':xgain==0,'X_only_shadow_rows':[[k,list(map(str,v))] for k,v in sorted(xshadow.items())] if xshadow is not None else None,'X_only_rank':xrank,'X_only_pure_gain_rank':xgain})
  if i%20==19:print('RECEIVERS',i+1,'seconds',round(time.monotonic()-start,2),flush=True)
 # Pooling different receivers' data is deliberately a larger interface.
 grows=[{k:v for k,v in r['F'].items() if k not in union} for r in arrivals]
 gresponses=[r['B'] for r in arrivals]
 grank,ggain,gshadow,gbasis=factor(grows,gresponses)
 allxrank,allxgain,allxshadow,_=factor([{k:v for k,v in r['F'].items() if k in xs} for r in arrivals],gresponses)
 pooled=pooled_witness(w,arrivals,grows,gresponses,union,coef)
 need(ggain==len(pooled),'pooled extraction rank')
 known_x=sorted(set(xs)&union)
 terminal_constraints=[[x,list(map(str,pulse[x+112]))] for x in known_x]
 need(all({k:v for k,v in baseline[x+112].items() if k not in union}=={} for x in known_x),'known-X terminal constraints have no remaining baseline common columns')
 constraint_rank=rank_rows([{k:v for k,v in enumerate(pulse[x+112]) if v} for x in known_x])
 need(ggain>=constraint_rank,'pooled history gain includes known-X endpoint constraints')
 result={'status':'PASS_INDEPENDENT_EIGHT_OWNED_HISTORY_GATE','source_sha256':PIN,'author_report_sha256':hashlib.sha256(ab).hexdigest(),'controls_before_events':EVENTS,'control_charts_disjoint_from_all_receiver_itineraries':True,'copy_guard':guards,'all_first_entry_cross_effects_zero':True,'receivers':reviews,'initial_intersection':len(common),'initial_union':len(union),'initial_quotient_columns':len(unknown),'arrival_observations_with_receiver_multiplicity':sum(map(len,obs)),'unique_arrival_events':len(arrivals),'verified_null_relations':null_checks,'pure_pulse_rank_histogram':dict(Counter(r['pure_pulse_rank'] for r in reviews)),'X_only_shadow_receivers':x_only,'pooled_receiver_interface':{'common_rank':grank,'pure_pulse_rank':ggain,'all_X_unrestricted_initial_pure_rank':allxgain,'pooled_extractions':pooled,'single_global_shadow_for_all8_exists':gshadow is not None,'known_X_roles':known_x,'known_X_terminal_constraints':terminal_constraints,'known_X_constraint_rank':constraint_rank,'pure_pulse_basis':[[p,[[k,str(v)] for k,v in sorted(row.items())]] for p,row in sorted(gbasis.items())]},'elapsed_seconds':time.monotonic()-start,'scope':'Independent exact source replay and complete local annihilator check, with explicit per-receiver common-input shadows. Pooled receiver data are a separately larger interface. No mixed raw/common records, encoded-packet delivery or source supplier is supplied.'}
 payload=(json.dumps(result,indent=2)+'\n').encode();(OUT/'REVIEW.json.gz').write_bytes(gzip.compress(payload,mtime=0))
 canonical_result=dict(result);canonical_result.pop('elapsed_seconds',None)
 cert_payload=(json.dumps(canonical_result,indent=2,sort_keys=True)+'\n').encode();(OUT/'CERTIFICATE.json.gz').write_bytes(gzip.compress(cert_payload,mtime=0))
 summary={k:result[k] for k in ['status','source_sha256','author_report_sha256','verified_null_relations','initial_intersection','initial_union','initial_quotient_columns','arrival_observations_with_receiver_multiplicity','unique_arrival_events','X_only_shadow_receivers']}
 summary.update({'certificate_payload_sha256':hashlib.sha256(cert_payload).hexdigest(),'individual_pure_pulse_rank':0,'pooled_pure_pulse_rank':ggain,'maximum_X_shadow_support':max(len(r['X_only_shadow_rows']) for r in reviews),'pooled_decoder_terms':[(r['pulse'],r['arrival_count'],r['initial_count']) for r in pooled]})
 (OUT/'REVIEW-RESULT.json').write_text(json.dumps(summary,indent=2)+'\n')
 print(json.dumps(summary,indent=2),flush=True)

def pooled_witness(w,arrivals,rows,responses,known,coef):
 common_basis={};pulse_basis={}
 for index,(row,rhs) in enumerate(zip(rows,responses)):
  row=row.copy();rhs={j:v for j,v in enumerate(rhs) if v};combo={index:F(1)}
  for p in sorted(common_basis):
   if p in row:
    c=row[p];old,b,d=common_basis[p];axpy(row,old,-c);axpy(rhs,b,-c);axpy(combo,d,-c)
  if row:
   p=min(row);c=row[p];row={k:v/c for k,v in row.items()};rhs={k:v/c for k,v in rhs.items()};combo={k:v/c for k,v in combo.items()}
   common_basis[p]=(row,rhs,combo)
  else:
   for p in sorted(pulse_basis):
    if p in rhs:
     c=rhs[p];old,d=pulse_basis[p];axpy(rhs,old,-c);axpy(combo,d,-c)
   if rhs:
    p=min(rhs);c=rhs[p];rhs={k:v/c for k,v in rhs.items()};combo={k:v/c for k,v in combo.items()}
    for op,(old,d) in list(pulse_basis.items()):
     if p in old:
      c=old[p];axpy(old,rhs,-c);axpy(d,combo,-c)
    pulse_basis[p]=(rhs,combo)
 need(len(pulse_basis)==8 and all(pulse_basis[p][0]=={p:F(1)} for p in range(8)),'pooled independent pulse basis')
 timed=defaultdict(dict)
 for p,(_,combo) in pulse_basis.items():
  for index,c in combo.items():timed[arrivals[index]['event']][p]=c
 adj=[(F(0),)*8 for _ in range(w['public']+w['owned_fields'])];gains={}
 for event in range(len(w['program'])-1,-1,-1):
  op=w['program'][event];kind,j=op[:2]
  if event in timed:
   need(kind=='MOVE','actual observation event in pooled decoder');v=tuple(timed[event].get(p,F(0)) for p in range(8));adj[j]=vadd(adj[j],v,F(1))
  if kind in ('ADD','COPY'):
   adj[op[2]]=vadd(adj[op[2]],adj[j],coef(op[3]))
   if kind=='COPY':adj[j]=(F(0),)*8
  elif kind=='SCALE':adj[j]=tuple(coef(op[2])*v for v in adj[j])
  elif kind in ('INIT','CLEAR'):adj[j]=(F(0),)*8
  elif kind!='MOVE':raise ValueError(kind)
  if event in EVENTS:gains[EVENTS.index(event)]=adj[j]
 need(all(gains[k]==tuple(F(p==k) for p in range(8)) for k in range(8)),'fresh full-source adjoint authenticates all8 pooled decoder gains')
 need(all(not any(adj[j]) for j in range(w['public']) if j not in known),'pooled decoders use only actually granted initial fields')
 out=[]
 for p,(_,combo) in sorted(pulse_basis.items()):
  terms=[{'after_event':arrivals[i]['event'],'role':arrivals[i]['role'],'chart':arrivals[i]['chart'],'coefficient':str(c)} for i,c in sorted(combo.items())]
  initial=[{'role':j,'chart':w['initial'][j],'coefficient':str(-adj[j][p])} for j in range(w['public']) if adj[j][p]]
  out.append({'pulse':p,'arrival_terms':terms,'initial_terms':initial,'arrival_count':len(terms),'initial_count':len(initial)})
 return out
if __name__=='__main__':main()
