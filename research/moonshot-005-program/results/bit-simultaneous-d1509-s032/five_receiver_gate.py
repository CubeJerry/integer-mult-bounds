"""Exact finite diagram gate for unchanged source/H/D data up to input gauges."""
from pathlib import Path
import importlib.util,itertools,json,numpy as np
here=Path(__file__).parent;s=importlib.util.spec_from_file_location('s032_solve',here/'solve_gauges.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
g,a,ff,Ks,C=m.common_data(Path.cwd());js=sorted(ff);rs=[i for i in sorted(ff[0])if i<111];rows=[];feasible=[]
for R in itertools.combinations(rs,5):
 ranks={};U0=None;ker=True
 for j in js:
  U=np.hstack([ff[j][i]for i in R]);rk=a.rank(U);ranks[j]=rk
  if U0 is None:U0=U;r0=rk
  elif rk!=r0 or a.rank(np.vstack([U0,U]))!=r0:ker=False
 if ker:feasible.append(R)
 rows.append({'receivers':R,'ranks':ranks,'joint_kernel_equal':ker})
 if len(rows)%100==0:print('FIVE_CENSUS',len(rows),len(feasible),flush=True)
result={'scope':'literal S031 source/H/D word under arbitrary independent invertible whole-bank linear input changes; not arbitrary changed source/H/D','native_receivers':rs,'donors':js,'five_receiver_subsets':len(rows),'compatible_sets':feasible,'all_native_joint_ranks':{j:a.rank(np.hstack([ff[j][i]for i in rs]))for j in js},'records':rows}
(here/'output/FIVE-RECEIVER-CENSUS.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print('FIVE_DONE',len(rows),len(feasible),flush=True)
