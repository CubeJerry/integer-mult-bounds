from pathlib import Path
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util,json,sys,time
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'worker-a/public-carrier943'))
spec=importlib.util.spec_from_file_location('root_carrier_import',ROOT/'worker-a/public-carrier943/import_gate.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
original=m.encoded_relation;seen={}
def collect(records):
 if records and all('event' in x for x in records):
  for x in records:
   key=(x['event'],x['owner'],x['frame'])
   if key in seen and (seen[key]['row']!=x['row'] or seen[key]['delta']!=x['delta']):raise ValueError('same observation changed')
   seen[key]=x
 return original(records)
m.encoded_relation=collect
start=time.monotonic();old=m.run(45)
if old['completed_domains']!=67 or not old['coverage_complete']:raise ValueError('incomplete cheap frame domain')
records=[seen[k] for k in sorted(seen)];witness,rank=original(records)
result={'source_sha256':m.PIN,'scope':'Latest single943 injection, fixed original prefix otherwise, demoted1459 initial value unavailable; pooled all67 available source coframes of exact distance1..3 from189 plus destination histories. No further original carrier edits.','available_frame_domains':67,'union_observations':len(records),'old_union_rank':rank,'encoded_dependence':witness is not None,'seconds':time.monotonic()-start}
if witness:
 result['witness']=[{'coefficient':str(q),'event':records[i]['event'],'owner':records[i]['owner'],'frame':records[i]['frame'],'delta':str(records[i]['delta'])} for i,q in sorted(witness.items())]
 result['status']='JOINT_CHEAP_HISTORY_INFORMATION_WITNESS_NO_PHYSICAL_CLAIM'
else:
 # Separate max-pivot equation solver builds a dual functional, then every
 # original equation is checked directly. Nonzero e885 never occurs in R.
 equations={}
 for rec in records:
  row=rec['row'].copy();rhs=rec['delta']
  while row:
   p=max(row)
   if p not in equations:
    scale=row[p];equations[p]=({j:v/scale for j,v in row.items()},rhs/scale);break
   b,d=equations[p];scale=row[p]
   m.add(row,b,-scale);rhs-=scale*d
  if not row and rhs:raise ValueError('dual equations inconsistent')
 x={}
 for p in sorted(equations):
  row,rhs=equations[p];x[p]=rhs-sum(v*x.get(j,Q(0)) for j,v in row.items() if j!=p)
 x[885]=-x.get(943,Q(0));x[1459]=x[885]-x.get(705,Q(0));x={j:v for j,v in x.items() if v}
 def dot(row,v):return sum(q*v.get(j,Q(0)) for j,q in row.items())
 for rec in records:
  if 885 in rec['row'] or 1459 in rec['row'] or dot(rec['row'],x)!=rec['delta']:raise ValueError('dual identity failed')
 if x.get(885,0)+x.get(943,0) or -x.get(1459,0)-x.get(705,0)+x.get(885,0):raise ValueError('dual target/promise adjustment failed')
 base={885:Q(1),1459:Q(1)}
 for alpha in [Q(0),Q(1),Q(-1),Q(2,3),Q(10)]:
  v=base.copy();m.add(v,x,-alpha)
  if dot({885:Q(1),943:Q(1)},v)!=1:raise ValueError('probe target')
  if dot({885:Q(1),705:Q(-1),1459:Q(-1)},v):raise ValueError('probe promise')
  for rec in records:
   if dot(rec['row'],v)+alpha*rec['delta']:raise ValueError('probe history')
 result['status']='NO_INFORMATION_IN_ENTIRE_CHEAP_HISTORY_UNION'
 result['dual_functional']={str(j):str(v) for j,v in sorted(x.items())}
 result['dual_equations_checked']=len(records);result['probe_controls']=5
 result['dual_meaning']='R*x=delta, z*x=0, u*x=0; base=e885+e1459. For any alpha, v=base-alpha*x obeys u(v)=0, z(v)=1 and (R+alpha*delta*z)(v)=0.'
raw=json.dumps(result,sort_keys=True,indent=2)+'\n';Path(__file__).with_name('RESULT.json').write_text(raw)
print(json.dumps({k:v for k,v in result.items() if k not in ['dual_functional','witness']},indent=2))
