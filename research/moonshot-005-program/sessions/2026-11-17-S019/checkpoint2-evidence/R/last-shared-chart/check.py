"""Root's separate exact premises for the nonlinear last-shared-chart proof."""
from pathlib import Path
from collections import Counter
import runpy,json,hashlib
state=runpy.run_path(str(Path(__file__).resolve().parents[1]/'fanout-residual-review/check.py'))
N,U,code=state['N'],state['U'],state['code'];arg=state['a'];room=state['room'];dec=state['dec']
pairs=[((N[i]&~N[h]).bit_count(),i,h)for i in U for h in U if i!=h];assert len(pairs)==10920 and min(x[0]for x in pairs)==21
_,i,h=min(pairs);private=[j for j in range(111)if(N[i]&~N[h])>>j&1];R=private[:17];extra=private[17];missing=private[18]
equations=[(z,0)for z in code]+[(1<<j,0)for j in range(111)if N[i]>>j&1 and j!=missing]+[(1<<i,1)];rows={}
for z,rhs in equations:
 while z:
  p=z.bit_length()-1
  if p in rows:z^=rows[p][0];rhs^=rows[p][1]
  else:rows[p]=(z,rhs);break
 assert z or not rhs
witness=0
for p,(z,rhs)in sorted(rows.items()):
 if ((z&witness).bit_count()&1)!=rhs:witness|=1<<p
assert all(((z&witness).bit_count()&1)==rhs for z,rhs in equations)
assert witness>>missing&1 and witness>>i&1 and all(not(witness>>j&1)for j in R+[extra])
assert not(witness&(N[i]&N[h]))
excess=(18-room[1],18-room[0]);assert excess[0]>0
result={'status':'PASS_ROOT_LAST_SHARED_CHART_PREMISES','source_word_sha256':hashlib.sha256(arg.word.read_bytes()).hexdigest(),'ordered_receiver_pairs':len(pairs),'pair_gap_histogram':dict(sorted(Counter(v for v,i,h in pairs).items())),'minimum_pair_gap':21,'explicit_collision':{'receiver':i,'partner':h,'native_origin_grants':R,'extra_suffix_native':extra,'omitted_indispensable_native':missing,'difference_support':[j for j in range(111)if witness>>j&1]},'at_least_distinct_native_origins':18,'completion_movement_excess':list(map(dec,excess)),'scope':'Proof in C independent last-meeting review; fixed source, nonlinear local functions, Y-bearing stationary owners, private initial y grant only; every new owned descent originates on native line. No claim18 origins suffice.'}
(arg.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'])
