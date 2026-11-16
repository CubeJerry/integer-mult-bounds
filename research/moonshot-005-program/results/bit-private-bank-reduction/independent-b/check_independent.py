#!/usr/bin/env python3
"""Independent exact replay/geometry/span/dual review; imports no author helper."""
from pathlib import Path
from sympy import Matrix
import argparse,hashlib,itertools,json
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--base-word',type=Path,required=True);p.add_argument('--author-result',type=Path,required=True);p.add_argument('--thirty-word',type=Path);p.add_argument('--affine-word',type=Path);p.add_argument('--out',type=Path,default=Path(__file__).parent/'output');a=p.parse_args()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(a.base_word)=='d28b6ae55b9d3c3cab440c24af971babbe7fb2413180ec1cb3d5e2fa4c77bb71'
w=json.loads(a.base_word.read_text());src=a.repo/w['source_path'];assert sha(src)==w['source_sha256']=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e';R=json.loads(src.read_text())['native_roots'];author=json.loads(a.author_result.read_text())
def cb(s):
 m=Matrix(s['rows'])if s['rows']else Matrix.zeros(0,8)
 if s['kind']=='ann':
  ns=m.nullspace();m=Matrix.vstack(*(v.T for v in ns))if ns else Matrix.zeros(0,8)
 else:assert s['kind']=='span'
 rr,ps=m.rref();return tuple(tuple(rr[i,j]for j in range(8))for i in range(len(ps)))
def replay(w):
 C={n:cb(s)for n,s in w['charts'].items()};v={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)};at={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)};owners=set();born=set()
 for step,o in enumerate(w['operations'],1):
  if o[0]=='INIT':
   _,n,c=o;assert n not in v and n not in born;v[n]=0;at[n]=c;owners.add(n);born.add(n)
  elif o[0]=='ADD':
   _,s,t=o;assert C[at[s]]==C[at[t]];v[t]^=v[s]
  elif o[0]=='MOVE':
   _,n,c=o;assert n in v and c in C;at[n]=c
  elif o[0]=='CLEAR':
   _,n=o;assert n in owners;owners.remove(n);del v[n];del at[n]
  else:raise AssertionError(o)
  if step==w['milestones']['seed8_before_Y']:return v,at,C
 raise AssertionError('cut')
def bas(rows):
 b={}
 for r in rows:
  while r:
   k=r&-r
   if k in b:r^=b[k]
   else:b[k]=r;break
 return b
def has(rows,v):
 b=bas(rows)
 while v:
  k=v&-v
  if k not in b:return False
  v^=b[k]
 return True
def dual(rows,i):
 b={}
 for r,z in [(r,0)for r in rows]+[(1<<i,1)]:
  while r:
   k=r&-r
   if k in b:s,t=b[k];r^=s;z^=t
   else:b[k]=(r,z);break
  if not r:assert not z
 out=0
 for k,(r,z)in sorted(b.items(),reverse=True):
  if ((r&out).bit_count()%2)^z:out^=k
 assert out>>i&1 and all(not((r&out).bit_count()%2)for r in rows);return out
v,at,C=replay(w);assert all(x>>111==0 for n,x in v.items()if not n.startswith('Y'))
local=[[1<<j for j in range(111)if sum(x*y for x,y in zip(R[i],R[j]))==0]for i in range(111)]
common=[c['roles']for c in w['cache_metadata']if c['family']==0 or(c['family']==1 and len(c['receivers'])==3)]
BB=[x for n,x in v.items()if not n.startswith('Y')and at[n]=='zero']
for chart in ['C0','M1']:BB +=[x for n,x in v.items()if not n.startswith('Y')and C[at[n]]==C[chart]]
BB +=[1<<j for g in common for j in g];assert[hex(x)for x in BB]==author['reconstructed_common_bank_rows_hex'];assert len(bas(BB))==47
E=set(w['point_targets']);groups=[[j for j in f['group']if j not in E]for f in w['forks']]+[[j for j in w['h1_private_roles'][str(i)]if j not in E]for i in[4,74,78]];assert groups==author['private_groups'];assert sum(map(len,groups))==33
assert E=={1,6,73,75,77,79}and all(has(BB,1<<j)for j in E)
first_names=[f'KEEP_C{i}'for i in range(3)]+[f'ZFIRST{i}'for i in range(3,6)]
assert all(n in v and has(BB,v[n])for n in first_names)
def closure(B):
 known=set();waves=[]
 while True:
  found={i for i in range(111)if has(B+[1<<j for j in sorted(known)]+local[i],1<<i)};assert known<=found
  if found==known:return sorted(known),waves
  waves.append(sorted(found-known));known=found
cases=[]
for mask in range(64):
 B=BB+[1<<j for k,g in enumerate(groups)if mask>>k&1 for j in g];fit=[i for i in range(111)if has(B+local[i],1<<i)];closed,waves=closure(B);old=author['cases'][mask];assert fit==old['initial_fits']and closed==old['feedback_closure']and waves==old['feedback_waves'];assert len(bas(B))==old['global_bank_rank_before_feedback'];cases.append({'mask':mask,'rank':len(bas(B)),'initial':len(fit),'closure':len(closed)})
B=BB+[1<<j for g in groups for j in g];closed,waves=closure(B);assert len(bas(B))==80 and len(closed)==83 and max(c['closure']for c in cases)==83;expanded=B+[1<<i for i in closed];duals=[]
for i in range(111):
 if i in closed:continue
 rows=expanded+local[i];duals.append({'receiver':i,'annihilator_hex':hex(dual(rows,i))});old=next(q for q in author['all_six_bank_exclusion_duals']if q['receiver']==i);d=int(old['annihilator_hex'],16);assert d>>i&1 and all(not((r&d).bit_count()%2)for r in rows)
assert len(duals)==28
for q in author['all_six_bank_fitting_witnesses']:
 i=q['receiver'];co=int(q['coefficient_hex'],16);rows=B+local[i];assert co>>len(rows)==0;out=0
 for j,r in enumerate(rows):
  if co>>j&1:out^=r
 assert out==1<<i
K=[(1<<i)^sum(local[i])for i in range(111)];assert len(bas(K))==9 and all(has(B+K+local[i],1<<i)for i in range(111))
filters=[]
for group in [5,7,9,11]:
 rows=[]
 for rec in w['history_cache_metadata']:
  if rec['group']==group:
   assert v[rec['name']]==int(rec['row_hex'],16)and at[rec['name']]==rec['chart'];rows.append(v[rec['name']])
 filters.append(rows)
assert [[hex(r)for r in g]for g in filters]==author['actual_remaining_filter_rows_hex']
filter_cases=[]
for mask in range(16):
 MM=expanded+[r for k,g in enumerate(filters)if mask>>k&1 for r in g];fits=[i for i in range(111)if has(MM+local[i],1<<i)];cl,ww=closure(MM);old=author['remaining_filter_bank_completion_cases'][mask]
 assert fits==old['fits']and cl==old['feedback_closure'];assert len(bas(MM))-len(bas(expanded))==old['additional_rank'];assert len(bas(MM+K))-len(bas(MM))==old['canonical_missing_dimensions'];filter_cases.append({'mask':mask,'extra_rank':old['additional_rank'],'fit':len(fits),'closure':len(cl),'missing_C9':old['canonical_missing_dimensions']})
all_filters=[r for g in filters for r in g];positive_rows=expanded+all_filters
def coefficient_value(rows,co):
 assert co>>len(rows)==0;out=0
 for j,r in enumerate(rows):
  if co>>j&1:out^=r
 return out
for i,co in enumerate(author['all_four_banks_canonical_witnesses']):assert coefficient_value(positive_rows,int(co,16))==K[i]
for rec in author['all_four_banks_positive_all111_witnesses']:
 i=rec['receiver'];assert coefficient_value(positive_rows+local[i],int(rec['coefficient_hex'],16))==1<<i
quotient_basis=[];current=list(expanded)
for i,r in enumerate(K):
 if not has(current,r):quotient_basis.append(i);current.append(r)
assert len(quotient_basis)==3
stock={}
def stockcheck(label,word):
 vv,pp,cc=replay(word);misses=[];checks=0
 for i in range(111):
  rows=expanded+local[i]
  for n,x in vv.items():
   if n.startswith('Y')or any(sum(t*z for t,z in zip(row,R[i]))for row in cc[pp[n]]):continue
   checks+=1
   if not has(rows,x):misses.append([i,n,pp[n],hex(x)])
 stock[label]={'visible_pureX_values_checked':checks,'noncontained_values':misses};return vv,pp,cc
stockcheck('27-output-base',w)
if a.thirty_word:
 assert sha(a.thirty_word)=='5566738ce7b2706c0094654fce0e4c1c438e82395dee2e6885ef917f2d4498f3';wt=json.loads(a.thirty_word.read_text());tv,tp,tc=stockcheck('30-output-base',wt)
 assert all(n in tv and has(BB,tv[n])for n in first_names)
if a.affine_word:
 assert sha(a.affine_word)=='7c5165a225e70e74181ac01c76dcde156c724aeb1e708309b146b7f174be723c';wa=json.loads(a.affine_word.read_text());av,ap,ac=stockcheck('concrete-affine-word',wa)
 assert set(tv)<=set(av)and all(ap[n]==tp[n]for n in tv)
 diffs={n:hex(x^tv[n])for n,x in av.items()if n in tv and x!=tv[n]};assert diffs=={'KEEP_C0':hex(1<<10),'ZFIRST3':hex((1<<25)^(1<<51))}
 assert av['AFF0']==1<<10 and ap['AFF0']=='D3_21'and av['AFF3']==(1<<25)^(1<<51)and ap['AFF3']=='F4'
assert all(not q['noncontained_values']for q in stock.values())
result={'status':'PASS_INDEPENDENT_PRIVATE_BANK_ENVELOPE_AND_AFFINE_SCOPE','base_word_sha256':sha(a.base_word),'native_source_sha256':sha(src),'author_result_sha256':sha(a.author_result),'independent_implementation':'Own symbolic operation replay, SymPy rational chart bases, low-pivot binary elimination and independent dual solve; no author code imported. Source movement validity inherited from separate published reviews.','common_global_rank':47,'all_private_global_rank':80,'private_groups':groups,'fitting_and_closed_receiver_set':closed,'all_subset_counts':cases,'independently_constructed_duals':duals,'author_duals_checked':28,'author_fitting_witnesses_checked':83,'four_filter_bank_cases':filter_cases,'all_four_bank_canonical_witnesses_checked':111,'all_four_bank_endpoint_witnesses_checked':111,'canonical_quotient_basis_native_row_indices':quotient_basis,'positive_C9_control':True,'canonical_missing_dimensions':len(bas(expanded+K))-len(bas(expanded)),'stock_scope_checks':stock,'new_kappa':False}
a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k]for k in['status','common_global_rank','all_private_global_rank','author_duals_checked','author_fitting_witnesses_checked','canonical_missing_dimensions','stock_scope_checks']}))
