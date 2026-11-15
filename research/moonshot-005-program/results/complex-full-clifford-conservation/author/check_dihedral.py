#!/usr/bin/env python3
"""Exact author controls for the ten-element ordinary-inverter extension."""
import importlib.util,sys,json
from pathlib import Path
here=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('author_phase',here/'check.py');m=importlib.util.module_from_spec(sp);sys.modules[sp.name]=m;sp.loader.exec_module(m)
i=m.eye(4);x=m.monomial([2,3,0,1],[0]*4);q=m.M((i.scale((1,1))+x.scale((1,-1))).a,1).norm()
s=m.monomial([0,3,1,2],[0,2,0,0]);b=(q@s).scale(m.II);t=m.monomial([1,0,2,3],[0,0,2,0])
assert t@t==i and t@b@t==b.power(4)
g={(k,e):b.power(k)@t.power(e) for k in range(5) for e in range(2)}
assert len({v for v in g.values()})==10
for (k,e),a in g.items():
 assert m.gaussian_rank(a)==[0,1,2,2,1][k]
 for (l,f),c in g.items():assert a@c==g[((k+(-1)**e*l)%5,(e+f)%2)]
 assert a.trace()==((4,0) if (k,e)==(0,0) else ((-1,0) if e==0 else (0,0)))
def modrank(rows,p=101):
 a=[row[:] for row in rows];r=0;n=len(a[0])
 for c in range(n):
  k=next((k for k in range(r,len(a)) if a[k][c]%p),None)
  if k is None:continue
  a[r],a[k]=a[k],a[r];v=pow(a[r][c],-1,p);a[r]=[(x*v)%p for x in a[r]]
  for j in range(len(a)):
   if j!=r and a[j][c]:
    v=a[j][c];a[j]=[(x-v*y)%p for x,y in zip(a[j],a[r])]
  r+=1
  if r==n:break
 return r
ranks=[]
for v in [1,2,3]:
 lifted=[a.tp(v) for a in g.values()]
 cols=[[(x+10*y)*pow(2,-a.k,101)%101 for row in a.a for x,y in row] for a in lifted]
 rank=modrank([list(z) for z in zip(*cols)]);ranks.append(rank);assert rank==(8 if v==1 else 10)
 bv=b.tp(v);tv=t.tp(v);iv=m.eye(4**v);su=m.zero(4**v)
 for k in range(5):su=su+bv.power(k)
 for sign in [1,-1]:
  z=su@(iv+tv.scale((sign,0)));assert z@z==z.scale((10,0))
  assert z.trace()==(4**v+4*(-1)**v,0)
# A concrete controlled shear alpha=2,beta=-1, exact restoration of its source.
v=2;tv=t.tp(v);iv=m.eye(16);z=m.zero(16)
def shear(c):return m.block([[iv,c],[z,iv]])
t_on_y=m.diagonal([iv,tv]);word=t_on_y@shear(iv.scale((-1,0)))@t_on_y@shear(iv.scale((2,0)))
assert word==shear(iv.scale((2,0))+tv.scale((-1,0)))
result={'status':'PASS_EXACT_DIHEDRAL_ORDINARY_INVERTER','group_order':10,'multiplication_pairs_checked':100,'ordinary_inverter':{'permutation':[1,0,2,3],'input_phase_mod4':[0,0,2,0]},'tensor_group_algebra_ranks_mod101':{'1':ranks[0],'2':ranks[1],'3':ranks[2]},'rank_pattern_each_reflection_column':[0,1,2,2,1],'controlled_shear_all_columns_and_source_restoration':True,'missing_one_column_character_blocks_rejected':True,'scope':'Structural ordinary service and faithful finite caller reduction; no actual profitable caller.','new_kappa':False}
(here/'DIHEDRAL-RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
