"""Discover a short exact symmetric entropy certificate; solver is not a premise."""
from pathlib import Path
from itertools import combinations,permutations
from fractions import Fraction as F
from collections import defaultdict
import json
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
pairs=list(combinations(range(5),2));index={p:i for i,p in enumerate(pairs)};FULL=1023
perms=[[index[tuple(sorted((p[a],p[b])))]for a,b in pairs]for p in permutations(range(5))]
def act(s,p):return sum(1<<p[i]for i in range(10)if s>>i&1)
canonical=[min(act(s,p)for p in perms)for s in range(1024)]
reps=sorted(set(canonical));orbit={r:i for i,r in enumerate(reps)};N=len(reps)
neigh=[sum(1<<j for j,q in enumerate(pairs)if not set(p)&set(q))for p in pairs]
rows=[];rhs=[];meta=[];seen=set()
def add(terms,b,desc):
 d=defaultdict(int)
 for s,c in terms:d[orbit[canonical[s]]]+=c
 d={s:c for s,c in d.items()if c};key=(tuple(sorted(d.items())),b)
 if not d or key in seen:return
 seen.add(key);rows.append(d);rhs.append(b);meta.append(desc)
add([(FULL,-1)],-10,['initialize'])
for s in reps:
 missing=[i for i in range(10)if not s>>i&1]
 for i in missing:
  u=s|1<<i
  add([(u,1),(s,-1)],1,['slope',s,i])
  add([(s,1),(u,-1)],0,['monotonicity',s,i])
  if neigh[i]&s==neigh[i]:add([(u,1),(s,-1)],0,['decode',s,i])
 for i,j in combinations(missing,2):add([(s,1),(s|1<<i|1<<j,1),(s|1<<i,-1),(s|1<<j,-1)],0,['submodularity',s,i,j])
ri=[];ci=[];da=[]
for r,d in enumerate(rows):
 for c,v in d.items():ri.append(r);ci.append(c);da.append(v)
a=coo_matrix((da,(ri,ci)),shape=(len(rows),N)).tocsr();c=np.zeros(N);c[orbit[0]]=1
sol=linprog(c,A_ub=a,b_ub=rhs,bounds=[(None,None)]*N,method='highs')
print('orbits',N,'constraints',len(rows),'result',sol.fun,sol.message,flush=True);assert sol.success and abs(sol.fun-5)<1e-7
weights=[-F(float(z)).limit_denominator(1000000) for z in sol.ineqlin.marginals];coeff=defaultdict(F);bound=F();terms=[]
for k,weight in enumerate(weights):
 assert weight>=0
 if not weight:continue
 for r,v in rows[k].items():coeff[reps[r]]+=weight*v
 bound+=weight*rhs[k]
 terms.append({'multiplier':str(weight),'inequality':meta[k],'orbit_coefficients':{str(reps[a]):v for a,v in rows[k].items()},'rhs':rhs[k]})
assert {a:v for a,v in coeff.items()if v}=={0:F(-1)}and bound==-5
out={'schema':'petersen-symmetric-shannon-dual-v1','status':'EXACT_PETERSEN_ENTROPY_5','pair_labels':pairs,'automorphism_group':'all120 permutations of the five pair-label symbols','orbit_representatives':reps,'terms':terms,'exact_conclusion':'Xbar(empty)>=5','scope':'Equal finite alphabet arbitrary zero-error deterministic index code; no linearity assumption. Rational weights verified exactly. Symmetry is obtained by averaging all entropy inequalities over120 automorphisms.'}
Path('/workspace/scratch/a40953eee9d0/workers/R/PETERSEN-SHORT-DUAL.json').write_text(json.dumps(out,indent=2)+'\n');print('EXACT_PASS terms',len(terms));print(json.dumps(terms,indent=2))
