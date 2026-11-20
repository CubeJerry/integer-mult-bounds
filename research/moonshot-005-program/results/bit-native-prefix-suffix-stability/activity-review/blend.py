from pathlib import Path
from collections import Counter
import json,gzip,numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix
p=Path('work-c/pathloss-review/output');root=Path('programme/research/moonshot-005-program/results/bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz');q=json.loads(gzip.decompress(root.read_bytes()))
D=[set(x)&set(range(111))for x in q['D4']];opp=[D[x]for x in q['dual_D4']];R=np.array(q['root_table'][:111]);orth=R@R.T==0;supp=R!=0;degree=orth.sum(axis=1);exc={(7,80),(10,81),(80,96),(81,95)};exc|={(j,i)for i,j in exc};seen={};E={};cost=Counter()
for i,j in zip(*np.where(orth)):
    key=tuple(map(int,(degree[i],degree[j],supp[i].sum(),supp[j].sum(),(supp[i]&supp[j]).sum())));n=seen.setdefault(key,len(seen));E[i,j]=n;cost[n]+=1+((i,j)in exc)
Y=json.loads((p/'STAR-PACK.json').read_text())['donor_and_receiver_limits'];k=len(seen);c=np.array([cost[z]for z in range(k)]+[2*Y[str(j)]['max']for j in range(111)],np.int64)
A=np.zeros((3150,k+111),np.int64)
for d,ds in enumerate(D):
    for j in ds:
        A[d,k+j]+=1
        for i in opp[d]:A[d,E[i,j]]+=1
    for i in opp[d]:A[d,k+i]+=1
s=linprog(c,A_ub=-csr_matrix(A),b_ub=-np.ones(len(A)),bounds=(0,None));assert s.success
for f in (100,1000,10000,100000):
 z=np.rint(s.x*f).astype(np.int64);lo=int((A@z).min());m=int(c@z)
 if lo>0 and m//lo==int(s.fun+1e-6):break
print(s.fun,m,lo,m//lo,flush=True);res={'weights_by_contact_type':[[list(v),int(z[j])]for v,j in seen.items()if z[j]],'star_weights':list(map(int,z[k:])),'minimum_per_D':lo,'total_allowance':m,'maximum_dead':m//lo,'minimum_active':3150-m//lo};(p/'BLENDED.json').write_text(json.dumps(res,sort_keys=True,indent=1)+'\n')
