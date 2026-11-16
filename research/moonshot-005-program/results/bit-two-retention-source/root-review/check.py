"""Independent all-column replay and full proper nonlocal stock audit."""
from pathlib import Path
import argparse,hashlib,json,sys
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--engine',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();sys.path.insert(0,str(a.engine));from check import replay,rr,null,rank
from budget import budget
raw=a.word.read_bytes();w=json.loads(raw);src=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(src).hexdigest()==w['source_sha256'];R=json.loads(src)['native_roots'];report=replay(w,R)
C={n:rr(c['rows']) if c['kind']=='span' else null(c['rows']) for n,c in w['charts'].items()};sub=lambda x,y:len(rr(x+y))==len(y)
val={f'X{j}':1<<j for j in range(111)}|{f'Y{j}':1<<(111+j) for j in range(111)};at={f'X{j}':f'L{j}' for j in range(111)}|{f'Y{j}':'zero' for j in range(111)};cut=None
for step,o in enumerate(w['operations'],1):
 if o[0]=='INIT':val[o[1]]=0;at[o[1]]=o[2]
 elif o[0]=='ADD':val[o[2]]^=val[o[1]]
 elif o[0]=='MOVE':at[o[1]]=o[2]
 elif o[0]=='CLEAR':del val[o[1]];del at[o[1]]
 if step==w['milestones']['seed8_before_Y']:cut={n:(v,at[n]) for n,v in val.items()}
assert cut is not None;mask=(1<<111)-1;ground=[];nonlocal_stock={};local_stock=[]
for n,(full,c) in cut.items():
 v=full&mask
 if not v or n.startswith('Y'):continue
 if not C[c]:ground.append(v);continue
 if c=='Hub':continue
 local=all(sub(rr([R[j]]),C[c]) for j in range(111) if v>>j&1)
 if local:local_stock.append(n)
 else:nonlocal_stock[n]={'chart':c,'row':hex(v)}
G=ground+[int(x['row'],16) for x in nonlocal_stock.values()]
fits=[]
for i in range(111):
 rows=ground+[int(v['row'],16) for v in nonlocal_stock.values() if sub(C[v['chart']],C[f'F{i}'])]
 rows += [1<<j for j in range(111) if sum(x*y for x,y in zip(R[i],R[j]))==0]
 if rank(rows+[1<<i])==rank(rows):fits.append(i)

from copy import deepcopy
controls=[]
if 'double_retention' in w:
 e6={1,6,73,75,77,79}
 h=int(nonlocal_stock['KEEP_L7']['row'],16)
 support={j for j in range(111) if h>>j&1}
 def puncture(rows,removed):
  m=mask^sum(1<<j for j in removed)
  return rank([x&m for x in rows])
 reduced=ground+[int(nonlocal_stock[n]['row'],16) for n in ('KEEP_C0','KEEP_L7')]
 punctures={label:{'removed':sorted(S),'full_inventory_rank':puncture(G,S),'two_new_retentions_only_rank':puncture(reduced,S)} for label,S in [('E6_plus_7',e6|{7}),('E6_plus_h_support',e6|support)]}
 assert set(nonlocal_stock)=={'KEEP_C0','KEEP_L7','Q1','Q3','Q4'},nonlocal_stock
 assert rank(ground)==14 and rank(G)==19 and len(fits)==21,(rank(ground),rank(G),fits)
 for label,pred in [('high capture',lambda o:o==['ADD','P0','KEEP_C0']),('nonlocal capture',lambda o:o==['ADD','P0','KEEP_L7']),('raw correction',lambda o:o[0]=='ADD' and o[2]=='CORR16'),('raw early source',lambda o:o[0]=='ADD' and o[2]=='EARLY7'),('retirement',lambda o:o==['CLEAR','KEEP_L7'])]:
  x=deepcopy(w);i=next(i for i,o in enumerate(x['operations']) if pred(o));del x['operations'][i]
  try:replay(x,R,False)
  except ValueError as e:controls.append({'control':label,'rejected':str(e)})
  else:raise AssertionError(label)
else:punctures={}
full_fits=[]
for i in range(111):
 rows=[v for n,(v,c) in cut.items() if sub(C[c],C[f'F{i}'])]
 rows += [1<<j for j in range(111) if sum(x*y for x,y in zip(R[i],R[j]))==0]
 target=(1<<i)|(1<<(111+i))
 if rank(rows+[target])==rank(rows):full_fits.append(i)
result={'full_222_column_static_fits':full_fits,'full_222_column_static_fit_count':len(full_fits),'status':'PASS_INDEPENDENT_ALL_COLUMN_NONLOCAL_STOCK_AUDIT','word_sha256':hashlib.sha256(raw).hexdigest(),'replay':report,'budget':budget(report['movement_profile']),'source_cut':w['milestones']['seed8_before_Y'],'ground_rank':rank(ground),'ground_plus_nonlocal_rank':rank(G),'proper_nonlocal_stock':nonlocal_stock,'local_stock_count':len(local_stock),'optimistic_fit_count':len(fits),'optimistic_fits':fits,'puncture_audit':punctures,'semantic_controls':controls,'scope':'Actual source-cut fields plus freely granted geometric raw locals. Does not prove any full-extension impossibility.','new_complete_kappa':False}
a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':result['status'],'word_sha256':result['word_sha256'],'rank':rank(G),'fits':len(fits),'punctures':punctures,'controls':len(controls)}))
