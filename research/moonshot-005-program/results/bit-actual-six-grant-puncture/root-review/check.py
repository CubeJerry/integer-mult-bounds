"""Independent native incidence and punctured canonical rank check."""
from pathlib import Path
from collections import Counter
import argparse,hashlib,json,itertools
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();d=json.loads(a.source.read_text())
for key in ['native_source','archived_star','rank_floor']:
 raw=(a.repo/d[key+'_path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==d[key+'_sha256']
R=json.loads((a.repo/d['native_source_path']).read_text())['native_roots'];dot=lambda i,j:sum(x*y for x,y in zip(R[i],R[j]))
I=d['frame'];E=d['erased_raw_points'];edges=d['retained_edges'];assert len(I)==len(set(I))==8 and not set(I)&set(E)
assert all(dot(i,j)!=0 for i in I for j in I);degrees=Counter();seen=set()
for e in edges:
 u,v=e['pair'];r=e['role'];assert u<v and (u,v) not in seen and r not in E+I;seen.add((u,v));degrees[u]+=1;degrees[v]+=1
 assert [j for j,i in enumerate(I) if dot(r,i)==0]==[u,v]
for e,f in itertools.combinations(edges,2):
 if set(e['pair'])&set(f['pair']):assert dot(e['role'],f['role'])!=0
assert len(edges)==27 and [degrees[i] for i in range(8)]==[6,7,7,7,6,7,7,7]
J=[i for i in range(111) if i not in E];piv={}
for i in J:
 x=sum(1<<j for j in J if i==j or dot(i,j)==0)
 while x:
  k=x.bit_length()-1
  if k in piv:x^=piv[k]
  else:piv[k]=x;break
assert len(piv)==9
out={'status':'PASS_INDEPENDENT_ACTUAL_SIX_GRANT_STAR','source_sha256':hashlib.sha256(a.source.read_bytes()).hexdigest(),'frame':I,'edges':27,'degrees':[degrees[i] for i in range(8)],'retained_roles':105,'canonical_rank':9,'scope':'Inherited all-field block-star theorem; arbitrary8 linear ground records plusE6; no later free feedback','new_complete_kappa':False}
a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(out,indent=2)+'\n');print(out['status'])
