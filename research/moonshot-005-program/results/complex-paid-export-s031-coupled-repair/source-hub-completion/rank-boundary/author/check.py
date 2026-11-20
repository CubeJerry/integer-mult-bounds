from pathlib import Path
from fractions import Fraction as Q
import importlib.util,json
RESULTS=Path(__file__).resolve().parents[4]
source=RESULTS/'complex-native-funded-donor-cuts/inputs/7833-construction.py'
spec=importlib.util.spec_from_file_location('native_source',source);S=importlib.util.module_from_spec(spec);spec.loader.exec_module(S)
w=S.load_word(source.with_name('DOUBLE-CANDIDATE.json.gz'));g=S.compensated(w,True)
V=S.all_public_rows(g)
fixed=[e for e,c in g.terminals.items()if c!=127 and not any(g.inputs[~j]==3 for j in V[e][1])]
assert len(fixed)==11
ancestors=set(fixed)
for e in reversed(g.schedule):
 if e in ancestors:ancestors.update(f for f in g.forms[e]if f>=0)
assert 94019 not in ancestors
D1={86,89777,97232,97241,97320,97323,99064};assert not(D1&ancestors)
assert all(q.denominator%1000003 for e in g.forms for q in g.forms[e].values())

import numpy as np
p=1000003;controls=[e for e,(a,b)in g.routes.items()if a==3];pos={e:i for i,e in enumerate(controls)};m=len(controls);ends=[e for e in sorted(g.terminals)if g.terminals[e]!=127]
def rank(A):
 A=A.copy();r=0;row_ids=list(range(len(A)));pivot_rows=[];pivot_cols=[];determinant=1
 for j in range(A.shape[1]):
  ii=np.flatnonzero(A[r:,j])
  if not len(ii):continue
  k=r+int(ii[0]);A[[r,k]]=A[[k,r]];row_ids[r],row_ids[k]=row_ids[k],row_ids[r];pivot_rows.append(row_ids[r]);pivot_cols.append(j);determinant=determinant*int(A[r,j])%p;A[r,j:]=A[r,j:]*pow(int(A[r,j]),-1,p)%p
  ii=np.flatnonzero(A[r+1:,j])+r+1
  if len(ii):A[ii,j:]=(A[ii,j:]-A[ii,j,None]*A[r,j:])%p
  r+=1
  if r==A.shape[0]:break
 return r,pivot_rows,pivot_cols,determinant
results=[]
for D in [set(),{86,89777,97232,97241,97320,97323,99064}]:
 vals={e:np.zeros(m,dtype=np.int64)for e in g.inputs}
 for e in g.schedule:
  z=np.zeros(m,dtype=np.int64)
  if e in pos:z[pos[e]]=1
  elif e not in D:
   for f,q in g.forms[e].items():z=(z+(q.numerator*pow(q.denominator,-1,p)%p)*vals[f])%p
  vals[e]=z
 A=np.stack([vals[e]for e in ends]);r,pr,pc,det=rank(A);assert r==376;assert not np.any(A[[ends.index(e)for e in fixed],:])
 record={'deleted':sorted(D),'prime':p,'outside_control_rank_mod_p':r,'outside_rows':len(ends),'controls':m,'minor_terminal_rows':[ends[i]for i in pr],'minor_export_columns':[controls[j]for j in pc],'minor_determinant_mod_p':det,'exact_rational_rank':376,'upper_bound_reason':'The eleven fixed outside rows vanish identically: source endpoint has no chart-3 input there, row 94019 has no path to them, and D1 avoids their full ancestor closure.'};results.append(record);print({k:v for k,v in record.items()if k not in {'minor_terminal_rows','minor_export_columns'}},flush=True)
out=Path(__file__).resolve().parent/'output';out.mkdir(exist_ok=True);(out/'RESULT.json').write_text(json.dumps({'status':'PASS_EXACT_OUTSIDE_CONTROL_RANK_BOUNDARY','prime':p,'fixed_outside_terminals':sorted(fixed),'protected_ancestor_slots':sorted(ancestors),'cases':results},indent=2)+'\n')
