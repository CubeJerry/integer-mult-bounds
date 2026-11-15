from pathlib import Path
import json,hashlib
p=Path(__file__).parent;t=json.loads((p/'TABLE.json').read_text());Ns=t['orbit_intersection_matrices'];sizes=t['radial_orbit_sizes']
def partitions(n):
 if not n:yield [];return
 for q in partitions(n-1):
  yield q+[[n-1]]
  for i in range(len(q)):yield q[:i]+[q[i]+[n-1]]+q[i+1:]
cases=[]
for part in partitions(4):
 val=[next(i for i,g in enumerate(part)if d in g)for d in range(4)];ranks=[sum(N[i][j]for i in range(4)for j in range(4)if val[i]!=val[j])for N in Ns];cut_sum=[0]*4
 for g in part:
  for r,N in enumerate(Ns):cut_sum[r]+=sum(N[i][j]for i in g for j in range(4)if j not in g)
 assert cut_sum==ranks and ranks[2]<=ranks[1];assert(bool(ranks[1]))==(len(part)>1);cases.append({'orbit_partition':part,'commutator_ranks':ranks})
assert len(cases)==15
out={'status':'EXACT_FINITE_CONTROLS_FOR_LEVEL_SET_COROLLARY','table_sha256':hashlib.sha256((p/'TABLE.json').read_bytes()).hexdigest(),'cases':cases,'scope':'Arbitrary H-radial diagonal commutator-rank operators in the same135-state permutation representation; not all H-intertwiners.','new_complete_kappa':False};(p/'DIAGONAL-RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
files=['DIAGONAL-RANK-COROLLARY.md','diagonal.py','DIAGONAL-RESULT.json'];(p/'DIAGONAL-MANIFEST.json').write_text(json.dumps({'status':'AUTHOR_PROVED_COROLLARY_INDEPENDENT_REVIEW_PENDING','files':{f:hashlib.sha256((p/f).read_bytes()).hexdigest()for f in files},'dependency_table_sha256':out['table_sha256']},indent=2)+'\n');print('All15 radial diagonal level partitions PASS')
