#!/usr/bin/env python3
"""Exact initial-chart dependency graphs, physical controls and full invoices."""
import argparse,copy,hashlib,json,sys
from fractions import Fraction
from pathlib import Path
p=argparse.ArgumentParser()
for key in ['repo','work','proof','out']:p.add_argument('--'+key,type=Path,required=True)
a=p.parse_args();P=a.repo/'research/moonshot-005-program';sys.path.insert(0,str(P/'sessions/2026-11-16-S018/root-review'))
from optimize_word import independent_replay
from review_source_families import trace
from review_leaf_capacity import chart_basis,echelon
from price import invoice
N=111;xm=(1<<N)-1
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,w):
 data=(json.dumps(w,indent=2)+'\n').encode();(a.out/(name+'.json')).write_bytes(data);return hashlib.sha256(data).hexdigest()
def graph(w,cut):
 C={n:chart_basis(c)for n,c in w['charts'].items()};v,at=trace(w)[0][cut];U=sorted(set(range(N))-set(w['targets']));mask=sum(1<<i for i in U);S={i:0 for i in U};cache={}
 def below(H,F):
  k=(H,F)
  if k not in cache:cache[k]=len(C[H])<=len(C[F]) and len(echelon(C[H]+C[F])[0])==len(C[F])
  return cache[k]
 fields={}
 for n,row in v.items():
  z=row&mask
  if z:
   access=[i for i in U if below(at[n],f'F{i}')]
   fields[n]={'chart':at[n],'unfinished_columns':[j for j in U if z>>j&1],'accessible_receivers':access}
   for i in access:S[i]|=z
 return S,v,at,fields
def sink_order(S,W):
 remaining=set(W);out=[]
 while remaining:
  mask=sum(1<<i for i in remaining);sinks=sorted(i for i in remaining if not(S[i]&mask))
  if not sinks:return None
  out+=sinks;remaining-=set(sinks)
 return out
sources=[('paid59','A/lower-history59-paid/WORD.json','dd60233b57be5fdef83b86a2d2b816e665e3d939850da94b680838d1d6d178ce',1380),('five46','A/shared-proper-five46/WORD.json','14503b00ad6f9d1e4d85ec09769a51c14eca36d61edabe19d9ae2907608c7501',1364),('liberated55','C/mask-preserving-reset/LIBERATED-SOURCE-WORD.json','4fe64237569a99a41578a378145a7df7ceac8394d33c82ca4f5e1be166b8859c',350)]
fixed26=[5,13,14,31,33,52,57,58,59,60,82,83,86,87,89,91,96,97,98,99,100,101,105,106,107,109]
donors=[13,14,31,33,52,57,58,59,60,82,83,86,87,96,97,100,101,105,109]
reports={};a.out.mkdir(parents=True,exist_ok=True)
for label,path,pin,cut in sources:
 f=a.work/path;assert sha(f)==pin;w=json.loads(f.read_text());native=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(native).hexdigest()==w['source_sha256']=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
 roots=json.loads(native)['native_roots'];C={n:chart_basis(c)for n,c in w['charts'].items()}
 for i,r in enumerate(roots):
  assert len(C[f'L{i}'])==1 and len(echelon(C[f'L{i}']+[r])[0])==1
  assert len(C[f'F{i}'])==7 and all(sum(x*y for x,y in zip(z,r))==0 for z in C[f'F{i}'])
 stats=independent_replay(w);S,v,at,fields=graph(w,cut);U=sorted(S);W=U if label!='liberated55'else fixed26;order=sink_order(S,W);assert order is not None
 if label in ['paid59','five46']:
  rows=[26,61,67,72,84]if label=='paid59'else[18,26,61,67,68,71,72,81,84,85]
  assert {i:[j for j in U if S[i]>>j&1]for i in U if S[i]}=={i:[5,15]for i in rows}
 else:
  assert len(W)==26 and set(donors)<=set(W)
  assert set(order[:7])=={5,89,91,98,99,106,107}
 originals={f'{p}{i}'for p in 'XY'for i in range(N)};owners=set(v)-originals
 assert all(v[n]>>N==0 for n in owners)
 tail=w['operations'][cut:];assert all(o[0]in ['MOVE','CLEAR']for o in tail)
 for op in tail:
  if op[0]=='MOVE':
   assert op[1]in originals and op[2]==('Hub'if op[1][0]=='X'else'F'+op[1][1:])
 for i in U:assert v[f'Y{i}']==1<<(N+i)and at[f'Y{i}']=='zero'
 profile={int(k):n for k,n in stats['movement_profile'].items()};floor=profile.copy();floor[1]=floor.get(1,0)+len(W)
 price=invoice(profile);lower=invoice(floor);assert Fraction(lower['moment']['lower_fraction'])>Fraction(lower['limiting_allowance']['upper_fraction'])
 row={'word_sha256':pin,'cut':cut,'all222_native_stats':stats,'unfinished':U,'actual_initial_chart_dependencies':{str(i):[j for j in U if S[i]>>j&1]for i in U},'initial_field_dependency_ledger':fields,'acyclic_witness':W,'sink_elimination_order':order,'minimum_future_owned_descents':len(W),'frozen_suffix_original_MOVEs':sum(o[0]=='MOVE'for o in tail),'frozen_suffix_CLEARs':sum(o[0]=='CLEAR'for o in tail),'partial_price':price,'completion_floor':lower}
 if label in ['paid59','five46']:
  assert all(v[f'X{i}']==1<<i and at[f'X{i}']=='Hub'for i in range(N))
  c=copy.deepcopy(w);body=[];new=[]
  for i in U:
   n=f'ROOT_COMPLETE_{i}';new.append(n);body += [['INIT',n,'Hub'],['ADD',f'X{i}',n],['MOVE',n,f'F{i}'],['MOVE',f'Y{i}',f'F{i}'],['ADD',n,f'Y{i}']]
  c['operations']=w['operations'][:cut]+body+[o for o in tail if o[0]!='MOVE']+[['CLEAR',n]for n in new];c['targets']=list(range(N));c['schema']='actual-all111-fixed-cut-sharp-movement-control-v1'
  cs=independent_replay(c);assert {int(k):n for k,n in cs['movement_profile'].items()}==floor
  row['sharp_all111_control']={'word_sha256':save(label.upper()+'-ALL111-WORD',c),'stats':cs,'exact_floor_profile':True,'target_budget_pass':False}
 else:
  c=copy.deepcopy(w);prefix=[];new=[]
  for i in donors:
   n=f'RAW_NATIVE_SNAPSHOT_{i}';new.append(n);prefix += [['INIT',n,f'L{i}'],['ADD',f'X{i}',n]]
  adds=[['ADD','MASK_RESET_RAW_61','Y61'],['MOVE','Y61','F61'],['ADD','MASK_RESET_RAW_67','Y67'],['MOVE','Y67','F67']]
  assert all(n in v for n in ['MASK_RESET_RAW_61','MASK_RESET_RAW_67'])
  assert v['MASK_RESET_RAW_61']==1<<61 and v['MASK_RESET_RAW_67']==1<<67
  newtail=[op for op in tail if op not in [['MOVE','Y61','F61'],['MOVE','Y67','F67']]]
  c['operations']=prefix+w['operations'][:cut]+adds+newtail+[['CLEAR',n]for n in new];c['targets']=sorted(set(w['targets'])|{61,67});c['schema']='actual-native-cached57-mask-source-v1';nc=cut+len(prefix)+len(adds);c['carrier_interface_before_operation']=nc;c['base_word_sha256']=pin
  c['source_interface']={'ground_raw_S':w['source_interface']['ground_raw_S'],'ground_raw_names':w['source_interface']['ground_raw_names'],'unknown_mask_partition':w['source_interface']['unknown_mask_partition'],'common_fields':w['source_interface']['common_fields'],'common_chart':w['source_interface']['common_chart'],'proper_mask_fields':w['source_interface']['proper_mask_fields'],'continuation_before_operation':nc,'all57_targets_complete_at_native_facets':True,'remaining54_Y_raw_at_ground':True,'remaining92_X_raw_at_native_lines':True,'actual_raw_native_donor_caches':{str(i):f'RAW_NATIVE_SNAPSHOT_{i}'for i in donors},'parent_contract':'Same liberated55 source plus19 actual native raw caches and two actual known-coordinate output completions; no new MOVE.'}
  cs=independent_replay(c);assert cs['movement_profile']==stats['movement_profile'];assert cs['counts']=={'INIT':82,'ADD':155,'MOVE':301,'CLEAR':82};assert cs['dirty_CLEAR']==82
  ns,nv,na,nfields=graph(c,nc);assert sink_order(ns,W)is None
  assert sum(na[f'X{i}']==f'L{i}'and nv[f'X{i}']==1<<i for i in range(N))==92
  assert all(nv[f'RAW_NATIVE_SNAPSHOT_{i}']==1<<i and na[f'RAW_NATIVE_SNAPSHOT_{i}']==f'L{i}'for i in donors)
  for i in [61,67]:assert nv[f'Y{i}']==(1<<(N+i))^(1<<i)and na[f'Y{i}']==f'F{i}'
  row['native_cached57_repair']={'word_sha256':save('NATIVE-CACHED57-WORD',c),'cut':nc,'stats':cs,'raw_native_originals':92,'actual_raw_native_donor_caches':19,'same_movement_profile':True,'old26_witness_now_cyclic':True,'actual_initial_chart_dependencies':{str(i):[j for j in ns if ns[i]>>j&1]for i in ns},'known61_67_actual_ground_ADDs':True,'complete_supplier':False}
 reports[label]=row
 print('PASS',label,'acyclic witness',len(W),flush=True)
dep=P/'results/endpoint-side-information/PROOF.md'
result={'status':'PASS_ROOT_INITIAL_CHART_TRANSCRIPT_FLOORS_AND_NATIVE_CACHED57_REPAIR','proof_sha256':sha(a.proof),'retained_acyclic_side_information_proof_sha256':sha(dep),'sources':reports,'scope':'Universal initial-chart transcript and acyclic reconstruction arguments reviewed separately; exact graph witnesses, all222 native words, legal cuts, direct closure floors and actual all111 sharp controls. Native-cache repair changes the prefix and graph with fully counted stationary owners, no free source. No all111 target-compatible supplier, no global foundation discharge, no kappa.'}
(a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'])
