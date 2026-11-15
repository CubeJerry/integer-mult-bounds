from pathlib import Path
import json,itertools,hashlib
root=Path(__file__).parent;R=json.loads(Path('programme/research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json').read_text())['native_roots'];g=json.loads(Path('worker-c/shared-facet-coding/GEOMETRY.json').read_text());geo=json.loads(Path('worker-c/joint-two-receiver-mds-source/GEOMETRY.json').read_text());dot=lambda a,b:sum(x*y for x,y in zip(a,b));i=80;common=geo['common_roles'];roles=[j for j in range(111)if dot(R[i],R[j])==0 and j not in common];assert len(roles)==26
K=[sum(1<<j for j in range(111)if i==j or dot(R[i],R[j])==0)for i in range(111)];basis=[0,1,2,4,8,9,14,30,59];cols={j:sum(((K[t]>>j)&1)<<k for k,t in enumerate(basis))for j in range(111)}
def rank(rows):
 B={}
 for v in rows:
  while v:
   q=v.bit_length()-1
   if q in B:v^=B[q]
   else:B[q]=v;break
 return len(B)
old=[cols[j]for j in[1,4,60,64]];assert rank(old)==4;U=sum(1<<j for j in roles);atlas=g['rows'][i]['atlas'];ms=[int(z['native_mask_hex'],16)&U for z in atlas];found=None
for combo in itertools.combinations(range(28),4):
 cov=0
 for a,b in itertools.combinations(combo,2):cov|=ms[a]&ms[b]
 if cov!=U:continue
 for pair in itertools.combinations(combo,2):
  rest=tuple(z for z in combo if z not in pair);order=list(pair)+list(rest);p1=[j for j in roles if (ms[pair[0]]&ms[pair[1]])>>j&1];p2=[j for j in roles if(ms[rest[0]]&ms[rest[1]])>>j&1]
  for j,k in itertools.product(p1,p2):
   if j!=k and rank(old+[cols[j],cols[k]])==6:found=(order,j,k);break
  if found:break
 if found:break
assert found
order,j,k=found;geo['receivers']=[3,76,80];geo['private_data'].append({'receiver':80,'other':3,'private_roles':roles,'atlas_indices':order,'normals':[atlas[t]['normal']for t in order],'pivot_roles':[j,k],'pivot_selected_pairs':[[0,1],[2,3]]});geo['source_scope']='One common A2-plane chart for all three targets; three disjoint private sets. Scalar canonical evaluations on six pivot roles have rank6.';geo['six_pivot_roles']=[1,4,60,64,j,k];geo['canonical_pivot_evaluation_rank']=6;(root/'GEOMETRY.json').write_text(json.dumps(geo,indent=2)+'\n');print('third',order,j,k,'private',len(roles),'A2 triple',[3,76,80])
