#!/usr/bin/env python3
"""Direct source-adjoint check of the two-endpoint history factorization."""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
import gzip,hashlib,json
BASE=Path('/workspace/scratch/6a77123a1d61')
SOURCE=BASE/'integer-mult-bounds/research/shared-wire-split-composition/data/final.json.gz'
HISTORY=BASE/'integer-mult-bounds/research/moonshot-005-program/results/joint-additive-history-obstruction/CERTIFICATE.json'
OUT=Path(__file__).resolve().parent
SPIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
HPIN='168fee8f09cdf0f33bcf5989630d244141d3c570808b7ccb553f6ad7be098dd7'
def need(a,b):
 if not a:raise ValueError(b)
def add(a,b,c):
 for k,v in b.items():
  v=a.get(k,F(0))+c*v
  if v:a[k]=v
  else:a.pop(k,None)
def run(w,h,sign=1,extra=()):
 allowed={16,35,127,318}|set(extra);loc=dict(enumerate(w['initial']));ops=w['program']
 for op in ops:
  if op[0]=='INIT':loc[op[1]]=op[2]
  elif op[0]=='MOVE':loc[op[1]]=op[3]
  elif op[0]=='CLEAR':del loc[op[1]]
 adj={189:{5:sign*F(1,2),7:sign*F(1,4)},215:{5:-sign*F(1,2),7:-sign*F(1,4)}} if sign else {}
 timed=defaultdict(list)
 for k,relation in enumerate(h['relations']):
  for t in relation:timed[t['after_event']].append((t['role'],k,F(t['coefficient']),t['chart']))
 checked=0;bad=None;last_nonzero=None;scalars={}
 def check(cut,role):
  nonlocal checked,bad,last_nonzero
  if loc[role] not in allowed:return
  checked+=1
  if adj.get(role):
   failure={'cut':cut,'role':role,'chart':loc[role],'residual':{str(k):str(v) for k,v in sorted(adj[role].items())}}
   if bad is None:bad=failure
   last_nonzero=failure
 for role in loc:check(len(ops),role)
 for cut in range(len(ops)-1,-1,-1):
  op=ops[cut];kind,j=op[:2];changed=set()
  for role,k,c,chart in timed.get(cut,[]):
   need(loc[role]==chart,'actual observation chart');add(adj.setdefault(role,{}),{k:c},F(1));changed.add(role)
  if kind in ('ADD','COPY'):
   r,c,chart=op[2:];c=scalars.setdefault(c,F(c));need(loc[j]==loc[r]==chart,'actual arithmetic chart')
   add(adj.setdefault(r,{}),adj.get(j,{}),c);changed.add(r)
   if kind=='COPY':adj[j]={};changed.add(j)
  elif kind=='SCALE':
   c=scalars.setdefault(op[2],F(op[2]));adj[j]={k:c*v for k,v in adj.get(j,{}).items() if c*v};changed.add(j)
  elif kind=='MOVE':need(loc[j]==op[3],'actual MOVE version');loc[j]=op[2];changed.add(j)
  elif kind=='INIT':del loc[j];adj[j]={};changed.discard(j)
  elif kind=='CLEAR':loc[j]=op[2];adj[j]={};changed.add(j)
  else:raise ValueError(kind)
  for role in changed:check(cut,role)
 if sign==0:
  for role,k,c,chart in timed[-1]:
   need(w['initial'][role]==chart,'initial observation chart');add(adj.setdefault(role,{}),{k:c},F(1))
  need(all(not row for row in adj.values()),'full source adjoint annihilates every common input for all nine original relations')
 return {'checked_changed_states':checked,'first_failure_reverse_order':bad,'last_failure_reverse_order':last_nonzero}

def main():
 raw=SOURCE.read_bytes();need(hashlib.sha256(raw).hexdigest()==SPIN,'native pin');w=json.loads(gzip.decompress(raw))
 raw=HISTORY.read_bytes();need(hashlib.sha256(raw).hexdigest()==HPIN,'history pin');h=json.loads(raw)
 routes=verify_routes(w)
 basis_check=verify_history_basis(w,h)
 run(w,h,sign=0)
 basis_check['full_input_adjoint_null_relations']=9
 good=run(w,h);need(good['first_failure_reverse_order'] is None,'all-cut factorization')
 wrong=run(w,h,sign=-1);need(wrong['first_failure_reverse_order'] is not None,'wrong-sign negative control')
 added=run(w,h,extra=[198]);need(added['first_failure_reverse_order'] is not None,'enlarged-station negative control')
 result={'status':'PASS_DIRECT_ALL_CUT_DUAL_CHECK','source_sha256':SPIN,'history_sha256':HPIN,'allowed_charts':[16,35,127,318],'identity':'N5=(final_delta_215-final_delta_189)/2; N7=(final_delta_215-final_delta_189)/4; all other N rows zero','normal':good,'history_basis':basis_check,'route_profiles':routes,'negative_wrong_dual_sign':wrong,'negative_extra_chart198':added,'scope':'Control responses on all live native fields at the listed charts, preserving the native chronology and COPY guard. This is separately implemented from the span derivation; both scripts are evidence authored by this review worker.'}
 (OUT/'DUAL-CHECK.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result,indent=2))

def verify_history_basis(w,h):
 routes={w['initial'][189]}|{o[3] for o in w['program'] if o[0]=='MOVE' and o[1]==189}
 known={j for j,c in enumerate(w['initial']) if c in routes}
 values={j:({j:F(1)} if j not in known else {}) for j in range(w['public'])};rows=[];observations={(-1,j) for j in known}
 def rank(data):
  basis={}
  for row in data:
   row=row.copy()
   for p in sorted(basis):
    if p in row:add(row,basis[p],-row[p])
   if row:
    p=min(row);c=row[p];basis[p]={j:v/c for j,v in row.items()}
  return len(basis)
 for event,op in enumerate(w['program']):
  kind,j=op[:2]
  if kind=='INIT':values[j]={}
  elif kind=='CLEAR':del values[j]
  elif kind=='SCALE':values[j]={k:F(op[2])*v for k,v in values[j].items() if F(op[2])*v}
  elif kind in ('ADD','COPY'):
   if kind=='COPY':need(not values[j],'quotiented baseline COPY guard')
   add(values[j],values[op[2]],F(op[3]))
  elif kind=='MOVE' and op[3] in routes:
   rows.append(values[j].copy());observations.add((event,j))
 relation_rows=[]
 for relation in h['relations']:
  row={}
  for t in relation:
   key=(t['after_event'],t['role']);need(key in observations,'relation uses actual receiver observation')
   row[key]=row.get(key,F(0))+F(t['coefficient'])
  relation_rows.append({k:v for k,v in row.items() if v})
 qrank=rank(rows);rrank=rank(relation_rows)
 need(len(observations)==h['observations']==1065,'complete observation census')
 need(len(known)+qrank==h['native_rank']==1056,'independent exact baseline history rank')
 need(rrank==len(h['relations'])==len(rows)-qrank==9,'complete independent null basis')
 return {'initial_units':len(known),'arrival_rows':len(rows),'quotient_rank':qrank,'complete_nullity':rrank}


def verify_routes(w):
 def space(vs):
  s={0}
  for v in vs:s.update([x^v for x in s.copy()])
  return s
 def rank(a,b):
  s,t=space(w['frames'][a]),space(w['frames'][b])
  return len(s).bit_length()+len(t).bit_length()-2*len(s&t).bit_length()
 first_x_charts={w['initial'][q] for q in w['live']}|{op[3] for op in w['program'] if op[0]=='MOVE' and op[1] in w['live']}
 need(318 not in first_x_charts,'chart318 outside original first-X itineraries')
 out={}
 for q,expected in [(17,[1,1,1,5]),(38,[1,1,3,1,1,1])]:
  old=[w['initial'][q]]+[o[3] for o in w['program'] if o[0]=='MOVE' and o[1]==q]
  new=[w['initial'][q],318,127]
  oldr=[rank(a,b) for a,b in zip(old,old[1:])];newr=[rank(a,b) for a,b in zip(new,new[1:])]
  need(oldr==expected and newr==[1,7],'actual rerouting ranks')
  out[str(q)]={'old_charts':old,'old_ranks':oldr,'new_charts':new,'new_ranks':newr}
 return out

if __name__=='__main__':main()
