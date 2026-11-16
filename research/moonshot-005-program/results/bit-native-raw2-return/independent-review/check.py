#!/usr/bin/env python3
"""Independent raw2 replacement, custody and historical-span review."""
from pathlib import Path
from fractions import Fraction
import argparse,copy,hashlib,importlib.util,json

V={
'birth41':('research/moonshot-005-program/results/bit-proper-birth-reduction/author/proper-birth41','research/moonshot-005-program/results/bit-native-raw2-return/author/birth41','6c76a836322483cc11888ae214379a27adbb8f638ac3a049584f75953c5185a9','6af12472710ddd26eb45cc58699652d8d68f4c6092907fde26a080d8dc9eaa08'),
'import41':('research/moonshot-005-program/results/bit-cyclic-import-source/author','research/moonshot-005-program/results/bit-native-raw2-return/author/import41','47cb0991e41d06efae453f0e2890af6f619ccc44109b46329749bee658a18d15','440bf0bb44f65180c066166e21691d15efcd19fb3e3bad7ea76038a4fa6834c8')}
MARK=['ADD','CAP46','P3']
def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def rb(rows):
 b={}
 for j,r in enumerate(rows):
  q=1<<j
  while r:
   p=r.bit_length()-1
   if p in b:r^=b[p][0];q^=b[p][1]
   else:b[p]=(r,q);break
 return b
def repr_(b,r):
 q=0
 while r:
  p=r.bit_length()-1
  if p not in b:return None
  x,y=b[p];r^=x;q^=y
 return q
def dominance(e,C0,H0,C1,H1,extra=0):
 exact={(C1[c],r)for _,_,c,r in H1};cache={};witnesses=[]
 for step,name,chart,row in H0:
  C=C0[chart]
  if (C,row)in exact:continue
  if C not in cache:
   records=[(s,n,c,r)for s,n,c,r in H1 if r and e.sub(C1[c],C)]
   if extra:records.append((-1,'FREE_RAW2','zero',extra))
   records.sort(key=lambda z:(z[3].bit_count(),len(C1[z[2]]),z[0]))
   cache[C]=(records,rb([z[3]for z in records]))
  records,b=cache[C];selector=repr_(b,row)
  assert selector is not None,('dominance failure',step,name,chart,hex(row))
  used=[records[j]for j in range(len(records))if selector>>j&1];check=0
  for _,_,c,r in used:assert e.sub(C1[c],C);check^=r
  assert check==row
  witnesses.append({'old_step':step,'old_field':name,'old_chart':chart,'old_row_hex':hex(row),'new_history_recipe':[{'step':s,'field':n,'chart':c,'row_hex':hex(r)}for s,n,c,r in used]})
 return witnesses
def cut(w):
 v={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)}
 at={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)};source=None;ground=None
 for step,o in enumerate(w['operations'],1):
  if o==MARK:source=(step,v.copy(),at.copy())
  op,n,*args=o
  if op=='INIT':v[n]=0;at[n]=args[0]
  elif op=='ADD':v[args[0]]^=v[n]
  elif op=='MOVE':at[n]=args[0]
  elif op=='CLEAR':del v[n],at[n]
  if ground is None and all(f'P{i}'in v and at[f'P{i}']=='zero'for i in range(8))and all(v[f'X{i}']==1<<i and at[f'X{i}']=='Hub'for i in range(111)):ground=(step,v.copy(),at.copy())
 assert source and ground
 return source,ground

def main():
 p=argparse.ArgumentParser()
 for n in ['workspace','repo','engine','price-engine','out']:p.add_argument('--'+n,type=Path,required=True)
 a=p.parse_args();e=load(a.engine,'geometry');price=load(a.price_engine,'price');result={};B={127:37,64:74,1:-74}
 for j in range(1,9):B[1+7*j]=B.get(1+7*j,0)+74;B[7*j]=B.get(7*j,0)-74
 allowance=tuple(x/6 for x in price.moment(B))
 for label,(bp,np,bpin,npin)in V.items():
  bp=a.workspace/bp/'WORD.json';np=a.workspace/np/'WORD.json';assert sha(bp)==bpin and sha(np)==npin
  old=json.loads(bp.read_text());w=json.loads(np.read_text());assert w['base_word_sha256']==bpin and w['targets']==old['targets']and w['source_sha256']==old['source_sha256']
  src=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(src).hexdigest()==w['source_sha256'];R=json.loads(src)['native_roots']
  C0,H0,r0=e.replay(old,R);C,H,r=e.replay(w,R)
  d={k:r['movement_profile'].get(k,0)-r0['movement_profile'].get(k,0)for k in set(r['movement_profile'])|set(r0['movement_profile'])};d={k:n for k,n in d.items()if n};assert d=={1:-1,3:-1,5:-1,7:1}
  assert r['counts']=={k:r0['counts'][k]+{'INIT':0,'ADD':-10,'MOVE':-2,'CLEAR':0}[k]for k in r0['counts']};assert r['dirty_CLEAR']==r['counts']['CLEAR']
  xops=lambda z:[o for o in z['operations']if (o[0]=='MOVE'and o[1].startswith('X'))or(o[0]=='ADD'and o[2].startswith('X'))]
  assert xops(w)==xops(old)and not any('BACK2'in o for o in w['operations'])
  assert w['operations'][:3]==[['INIT','COMMON_RAW2','L2'],['ADD','X2','COMMON_RAW2'],['MOVE','COMMON_RAW2','zero']]
  assert [o for o in w['operations']if 'Y2'in o]==[['ADD','COMMON_RAW2','Y2'],['MOVE','Y2','F2']]
  source0,ground0=cut(old);source1,ground1=cut(w);ss,sv,sa=source1
  assert sv['P3']==0 and sa['P3']=='M1'and sv['COMMON_RAW2']==1<<2 and sa['COMMON_RAW2']=='zero'
  inv0={n:z for n,z in source0[1].items()if n!='P3'and not z>>111 and C0[source0[2][n]]==C0['M1']}
  inv={n:z for n,z in sv.items()if n!='P3'and not z>>111 and C[sa[n]]==C['M1']}
  assert {n:z for n,z in inv0.items()if n!='BACK2'}==inv
  imports={}
  if label=='import41':
   for i in [8,9,36]:
    field=f'IMPORT_E{i}';assert inv[field]==1<<i;imports[field]=hex(inv[field]);probe=copy.deepcopy(w);ix=probe['operations'].index(MARK);probe['operations'][ix:ix]=[['ADD',field,'P3'],['ADD',field,'P3']];e.replay(probe,R)
  common=lambda t:[z for n,z in t[1].items()if t[2][n]=='zero'and not z>>111]
  rank0=len(e.bb(common(ground0)));rank1=len(e.bb(common(ground1)));assert (rank0,rank1)==(17,18)
  forward=dominance(e,C0,H0,C,H);reverse=dominance(e,C,H,C0,H0,1<<2)
  controls=[]
  for omitted in [['ADD','X2','COMMON_RAW2'],['MOVE','COMMON_RAW2','zero'],['ADD','COMMON_RAW2','Y2'],['CLEAR','COMMON_RAW2']]:
   bad=copy.deepcopy(w);bad['operations'].remove(omitted)
   try:e.replay(bad,R)
   except (AssertionError,KeyError)as ex:controls.append({'omitted':omitted,'rejected':str(ex)})
   else:raise AssertionError(('essential omission accepted',omitted))
  bad=copy.deepcopy(w);bad['operations'][0]=['INIT','COMMON_RAW2','zero']
  try:e.replay(bad,R)
  except AssertionError as ex:controls.append({'wrong_birth_chart':'zero','rejected':str(ex)})
  else:raise AssertionError('unpaid birthplace accepted')
  bad=copy.deepcopy(w);ix=bad['operations'].index(MARK);bad['operations'][ix:ix]=[['ADD','H6_0','P3'],['ADD','Q2','P3']]
  try:e.replay(bad,R)
  except AssertionError as ex:controls.append({'restored_unbalanced_old_P3_preload':True,'rejected':str(ex)})
  else:raise AssertionError('unbalanced source accepted')
  Q=price.moment(r['movement_profile']);room=(allowance[0]-Q[1],allowance[1]-Q[0]);author=json.loads((np.parent/'PRICE.json').read_text())
  for key,bounds in [('moment',Q),('limiting_allowance',allowance),('limiting_room',room)]:assert bounds[0]<=Fraction(author[key]['lower_fraction'])<=Fraction(author[key]['upper_fraction'])<=bounds[1]
  known=set(w['targets']);obs=[];mask=(1<<111)-1
  for i in range(111):
   rows=[v&mask for _,_,c,v in H if e.sub(C[c],C[f'F{i}'])];rows += [1<<j for j in range(111)if sum(x*y for x,y in zip(R[i],R[j]))==0];obs.append(rows)
  waves=[]
  while True:
   nxt={i for i,rows in enumerate(obs)if e.fits(rows+[1<<j for j in known],1<<i)};assert known<=nxt
   if nxt==known:break
   waves.append(sorted(nxt-known));known=nxt
  duals=[{'receiver':i,'dual_hex':hex(price.outsider_dual(rows+[1<<j for j in known],i))}for i,rows in enumerate(obs)if i not in known]
  result[label]={'status':'PASS_INDEPENDENT_RAW2_REPLACEMENT_AND_HISTORY_DOMINANCE','old_word_sha256':bpin,'word_sha256':npin,'native_source_sha256':w['source_sha256'],'before':r0,'after':r,'unchanged_original_X_routes':True,'source_cut_step':ss,'actual_M1_inventory_before':{n:hex(z)for n,z in inv0.items()},'actual_M1_inventory_after':{n:hex(z)for n,z in inv.items()},'M1_rank_before':len(e.bb(inv0.values())),'M1_rank_after':len(e.bb(inv.values())),'retained_exact_three_import_rows':imports,'current_common_rank_before':rank0,'current_common_rank_after':rank1,'exact_profile_difference':d,'price':{'moment':price.display(Q),'limiting_room':price.display(room),'increment':price.display(price.moment(d))},'independent_interval_contains_author_interval':True,'semantic_controls':controls,'all_old_full222_history_states_locally_spanned_by_new_histories':True,'nontrivial_forward_history_recipes':forward,'all_new_full222_history_states_locally_spanned_by_old_histories_plus_global_raw2':True,'nontrivial_reverse_history_recipes_with_global_raw2':reverse,'fresh_strongest_history_feedback_closure':sorted(known),'feedback_waves':waves,'fresh_outsider_duals':duals,'scope':'Literal41-output word and actual source custody. Historical local-span comparison grants simultaneous actual observations and ignores time; it does not replace actual M1 custody by observations at lower charts.'}
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:{'status':v['status'],'after':v['after'],'M1_ranks':[v['M1_rank_before'],v['M1_rank_after']],'common_ranks':[v['current_common_rank_before'],v['current_common_rank_after']],'history_recipe_count':len(v['nontrivial_forward_history_recipes']),'closure_count':len(v['fresh_strongest_history_feedback_closure']),'price':v['price']}for k,v in result.items()}))
if __name__=='__main__':main()
