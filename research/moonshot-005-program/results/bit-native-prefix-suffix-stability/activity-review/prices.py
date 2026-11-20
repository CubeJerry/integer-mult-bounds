from pathlib import Path
import json,gzip,numpy as np
from scipy.optimize import linprog
P=Path('work-c/pathloss-review/output');L=json.loads(gzip.decompress(Path('programme/research/moonshot-005-program/results/bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz').read_bytes()));D=[set(x)&set(range(111))for x in L['D4']];opp=[D[x]for x in L['dual_D4']];c=np.array([w for i in range(111)for w in [json.loads((P/'STAR-PACK.json').read_text())['donor_and_receiver_limits'][str(i)]['max']]])
A=np.zeros((3150,111),np.int64)
for d in range(3150):
 for j in D[d]:A[d,j]+=1
 for i in opp[d]:A[d,i]+=1
s=linprog(2*c,A_ub=-A,b_ub=-np.ones(len(A)),bounds=(0,None));assert s.success
for m in [100,1000,10000,1000000]:
 z=np.rint(s.x*m).astype(np.int64);lo=int((A@z).min());mass=int(2*c@z)
 if lo and mass//lo==int(s.fun+1e-7):break
doc={'weights':[int(t)for t in z],'minimum_per_D':lo,'twice_weighted_native_star_capacity':mass,'dead_D_upper':mass//lo,'active_D_lower':3150-mass//lo};print(s.fun,doc);(P/'STAR-COVER.json').write_text(json.dumps(doc,indent=1)+'\n')
