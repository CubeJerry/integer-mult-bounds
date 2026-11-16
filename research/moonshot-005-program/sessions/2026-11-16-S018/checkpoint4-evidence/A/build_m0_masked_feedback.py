"""Actual local masks in a lower changing-history source; binary19-parameter family."""
import argparse,copy,hashlib,importlib.util,json
from pathlib import Path
PINS={'12ccd57ba43a8d4902c04724c70489a348266690d20ce2269ff68eec34b4835e','38cd6486a2e00a39ad139d751fcc8523afd93c4e2588f4597b20e5d09015a38d'}
def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def write(path,obj):
 raw=(json.dumps(obj,indent=2)+'\n').encode();path.write_bytes(raw);return hashlib.sha256(raw).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path('/workspace/scratch/b421dd0c4c1e/integer-mult-bounds'));p.add_argument('--word',type=Path,default=Path('/workspace/scratch/b421dd0c4c1e/work-S018/C/m0-pair55/WORD.json'));p.add_argument('--out',type=Path,required=True);p.add_argument('--masks',nargs=3);p.add_argument('--purify',action='store_true');a=p.parse_args();raw=a.word.read_bytes();input_pin=hashlib.sha256(raw).hexdigest();assert input_pin in PINS;w=json.loads(raw);source=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(source).hexdigest()==w['source_sha256'];R=json.loads(source)['native_roots']
 e=load(a.repo/'research/moonshot-005-program/results/bit-leaf-capacity-quotient/author/check.py','mask_engine');tracer=load(Path(__file__).with_name('build_d4_cohort.py'),'mask_trace');price=load(Path(__file__).with_name('price_d4_cohort.py'),'mask_price')
 C,_,before=e.replay(w,R);bt=tracer.trace(w['operations']);pairs=w['pair_extension']['pairs'];fields=w['pair_extension']['fields'];packets=['P0','P1','P2'];common=w['pair_extension']['common'];charts=copy.deepcopy(w['charts']);eligible=[]
 for j,(aa,bb)in enumerate(pairs):
  lab=f'MASK_CORRECTION_{j}';charts[lab]={'kind':'ann','rows':[R[aa],R[bb]]};T=e.chart(charts[lab]);assert len(T)==6 and e.sub(C[common],T)
  eligible.append([i for i in w['released_carriers']if i not in w['targets']and e.sub(C[f'L{i}'],T)])
 union=sorted(set().union(*map(set,eligible)));assert union==[13,14,31,33,52,57,58,59,60,82,83,86,87,96,97,100,101,105,109]
 partition=[[],[],[]]
 for i in union:
  j=min((j for j in range(3)if i in eligible[j]),key=lambda j:(len(partition[j]),j));partition[j].append(i)
 allowed=[sum(1<<i for i in part)for part in partition];masks=allowed if a.masks is None else[int(x,0)for x in a.masks];assert all(z&~s==0 for z,s in zip(masks,allowed))
 mask_names={f'X{i}'for i in union};assert not any(o[0]=='ADD'and(o[1]in mask_names or o[2]in mask_names)for o in w['operations'])
 assert all([o for o in w['operations']if o[0]=='MOVE'and o[1]==f'X{i}']==[['MOVE',f'X{i}','Hub']]for i in union)
 ops=[];newowners=[];precoats=[]
 def add(*rows):ops.extend([list(r)for r in rows])
 if not a.purify:
  for aa,bb in pairs:precoats.append(len(ops));add(('ADD',f'Y{aa}',f'Y{bb}'))
 for j,((aa,bb),part,z)in enumerate(zip(pairs,partition,masks)):
  lab=f'MASK_CORRECTION_{j}';owner=f'MASK_SOURCE_{j}';newowners.append(owner)
  if a.purify:add(('MOVE',f'Y{aa}','M0'),('INIT',f'MASK_INITIAL_Y{j}','M0'),('ADD',f'Y{aa}',f'MASK_INITIAL_Y{j}'))
  add(('MOVE',f'Y{aa}',f'F{aa}'),('INIT',owner,lab))
  for i in part:
   add(('MOVE',f'X{i}',lab))
   if z>>i&1:add(('ADD',f'X{i}',owner))
   add(('MOVE',f'X{i}',f'F{aa}'))
   if z>>i&1:add(('ADD',f'X{i}',f'Y{aa}'))
   add(('MOVE',f'X{i}','Hub'))
  add(('MOVE',f'X{bb}',f'F{aa}'),('ADD',f'X{bb}',f'Y{aa}'),('MOVE',f'X{bb}','Hub'),('MOVE',f'X{aa}','Hub'))
 prelude=len(ops);start=w['pair_extension']['prelude_end'];end=w['pair_extension']['decode_start'];cells=[];mapping={};programmed=set()
 for k in range(start,end):
  o=w['operations'][k].copy()
  if o[0]=='MOVE'and o[1]in mask_names:mapping[k]=len(ops);continue
  if o[0]=='MOVE'and o[1]in packets and bt[k][1][o[1]]=='Hub':
   j=int(o[1][1:]);aa,bb=pairs[j];assert j not in programmed
   for i in partition[j]:
    if masks[j]>>i&1:add(('ADD',f'X{i}',o[1]))
   o[2]=f'F{aa}';add(o);pos=len(ops);add(('ADD',o[1],f'Y{aa}'),('ADD',f'Y{aa}',o[1]));cells.append({'packet':o[1],'primary':aa,'target':bb,'before_operation':pos,'after_operation':len(ops)});programmed.add(j)
  else:
   if a.purify and o[0]=='ADD'and o[1]in packets and o[2]in fields:add(('ADD',f'MASK_INITIAL_Y{int(o[1][1:])}',o[1]))
   add(o)
   if a.purify and o[0]=='ADD'and o[1]in fields and o[2]in packets:add(('CLEAR',f'MASK_INITIAL_Y{int(o[2][1:])}'))
  mapping[k]=len(ops)
 assert len(cells)==3;decode_start=len(ops)
 for f in fields:add(('MOVE',f,common))
 for j,(f,(aa,bb))in enumerate(zip(fields,pairs)):
  add(('MOVE',f'Y{bb}',common),('ADD',f,f'Y{bb}'),('MOVE',f'Y{bb}',f'MASK_CORRECTION_{j}'),('ADD',f'MASK_SOURCE_{j}',f'Y{bb}'),('MOVE',f'Y{bb}',f'F{bb}'))
 interface=len(ops)
 for o in w['operations'][w['pair_extension']['continuation_before_operation']:]:
  if o[0]=='CLEAR'and o[1].startswith('M0_PAIR_RAW_'):continue
  if o[0]=='MOVE'and o[1]in mask_names:continue
  add(o)
 add(*[('CLEAR',n)for n in newowners]);nw=copy.deepcopy(w)
 nw.update(charts=charts,operations=ops,schema='M0-actual-rank6-mask-changing-history-family-v1',base_word_sha256=input_pin,released_carriers=sorted(set(w['released_carriers'])-set(union)),carrier_interface_before_operation=interface,masked_feedback={'pairs':pairs,'fields':fields,'common':common,'eligible_raw_inputs':eligible,'fixed_disjoint_partition':partition,'allowed_masks_hex':list(map(hex,allowed)),'chosen_masks_hex':list(map(hex,masks)),'precoat_operations':precoats,'feedback_cells':cells,'prelude_end':prelude,'decode_start':decode_start,'continuation_before_operation':interface,'parameter_count':sum(len(x)for x in partition)},scope='All55 endpoints preserved. Three masks on19 free unfinished inputs are gathered at actual rank6 intersections, used in primary Y feedback, and retained inside dirty fields at rank4. Same MOVE profile for all binary19-parameter choices. No new endpoints, all111 completion or kappa.')
 nw['pair_extension']['prelude_end']=prelude;nw['pair_extension']['decode_start']=decode_start;nw['pair_extension']['continuation_before_operation']=interface
 nw['masked_feedback']['purified_at_M0']=a.purify
 if a.purify:nw['scope']='All55 endpoints preserved. Three binary local masks on19 unfinished inputs are acquired at rank6 and retained at rank4. Actual initial-Y snapshots purify every shared field atM0 before its descent; all cut owners are pureX. No new endpoints, all111 completion or kappa.'
 CC,_,after=e.replay(nw,R);nt=tracer.trace(ops);values,locations=nt[interface]
 for j,((aa,bb),f,z,cell)in enumerate(zip(pairs,fields,masks,cells)):
  assert values[f]==(0 if a.purify else 1<<(111+aa))^(1<<bb)^z and locations[f]==common
  assert values[f'MASK_SOURCE_{j}']==z and locations[f'MASK_SOURCE_{j}']==f'MASK_CORRECTION_{j}'
  vv,aa_loc=nt[cell['before_operation']];assert vv[cell['packet']]==(1<<aa)^(1<<bb)^z;assert vv[f'Y{aa}']==(1<<(111+aa))^(1<<bb)^z
  vv,aa_loc=nt[cell['after_operation']];assert vv[cell['packet']]==(1<<(111+aa))^(1<<bb)^z;assert vv[f'Y{aa}']==(1<<(111+aa))^(1<<aa)
 for i in range(111):
  assert values[f'X{i}']==1<<i
  if i in nw['released_carriers']:assert locations[f'X{i}']==f'L{i}'
  if i not in nw['targets']:assert values[f'Y{i}']==1<<(111+i)and locations[f'Y{i}']=='zero'
 active=set();compared=0;pair_roles={i for pair in pairs for i in pair}
 for k in range(start,end):
  o=w['operations'][k]
  if o[0]=='MOVE'and o[1]in packets and bt[k][1][o[1]]=='Hub':active.add(o[1])
  if o[0]=='ADD'and o[1]in fields and o[2]in active:active.remove(o[2])
  ov,oa=bt[k+1];v,loc=nt[mapping[k]]
  for n,z in ov.items():
   if n in fields or n in active or n.startswith('M0_PAIR_RAW_'):continue
   if n.startswith('Y')and int(n[1:])in pair_roles:continue
   if n not in v:continue
   assert v[n]==z,(k,n)
   if n not in mask_names:assert CC[loc[n]]==C[oa[n]],(k,n,'chart')
   compared+=1
 born={o[1]for o in ops if o[0]=='INIT'};owned={n:z for n,z in values.items()if n in born};xm=(1<<111)-1
 owner_support=sorted({i for z in owned.values()for i in range(111)if z>>i&1});support=sorted(set(owner_support)|{i for j in range(111)for i in range(111)if values[f'Y{j}']>>i&1})
 prior_values,prior_charts=bt[w['pair_extension']['continuation_before_operation']];mask_union=sum(1<<i for i in union);assert all(not(z&mask_union)for n,z in prior_values.items()if not n.startswith('X'));known=set(w['targets'])|{61,67};knownmask=sum(1<<i for i in known);newrank=len(e.bb(z&xm&~knownmask for z in owned.values()))
 a.out.mkdir(parents=True,exist_ok=True);sha=write(a.out/'WORD.json',nw);gate={127:37,64:74,1:-74}
 for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
 limit=tuple(x/6 for x in price.moment(gate));q=price.moment(after['movement_profile']);qo=price.moment(before['movement_profile'])
 result={'status':'PASS_ACTUAL_THREE_RANK6_MASKS_AT_LOWER_SOURCE','word_sha256':sha,'base_word_sha256':input_pin,'before':before,'after':after,'masked_feedback':nw['masked_feedback'],'all_targets':nw['targets'],'continuation_index':interface,'retained_native_carriers':nw['released_carriers'],'remaining_ground_Y_count':111-len(nw['targets']),'owner_X_rank':len(e.bb(z&xm for z in owned.values())),'owner_Y_rank':len(e.bb(z>>111 for z in owned.values())),'owned_full_222_rank':len(e.bb(owned.values())),'owned_X_rank_modulo_known57':newrank,'new_mask_rank_modulo_prior_source':len(e.bb(masks)),'full_cut_nonidentity_X_support':support,'full_cut_nonidentity_X_support_count':len(support),'unaffected_core_comparisons':compared,'whole_moment':price.record(q),'moment_increment':price.record((q[0]-qo[1],q[1]-qo[0])),'necessary_limiting_room':price.record((limit[0]-q[1],limit[1]-q[0])),'direct_full_support_point_baseline':{'completed_count':len(support),'moment':price.record(price.moment({1:len(support),7:222}))},'scope':nw['scope']};write(a.out/'RESULT.json',result);print(json.dumps({k:result[k]for k in['status','word_sha256','after','owner_X_rank','owner_Y_rank','owned_X_rank_modulo_known57','full_cut_nonidentity_X_support_count','whole_moment']}))
if __name__=='__main__':main()
