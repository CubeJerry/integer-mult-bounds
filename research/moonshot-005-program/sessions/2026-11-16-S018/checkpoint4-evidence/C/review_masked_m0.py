#!/usr/bin/env python3
"""Independent physical and formal19-parameter review of A's pure masked M0 source."""
import argparse,copy,hashlib,json
from pathlib import Path
from release_projection import N,binary_basis,chart,replay,require,rref
from price_projection import moment,record
BASE='12ccd57ba43a8d4902c04724c70489a348266690d20ce2269ff68eec34b4835e'
PIN='fd9ce4903aab198d234e6956a877e97241ed7268c7dba657064fa8ebf8cba84c'

def main():
 ap=argparse.ArgumentParser()
 for n in ['repo','work','out']:ap.add_argument('--'+n,type=Path,required=True)
 a=ap.parse_args();br=(a.work/'C/m0-pair55/WORD.json').read_bytes();wr=(a.work/'A/m0-masked19-pure-pruned55/WORD.json').read_bytes()
 require(hashlib.sha256(br).hexdigest()==BASE and hashlib.sha256(wr).hexdigest()==PIN,'pair55 and mask source pins')
 b,w=json.loads(br),json.loads(wr);sr=(a.repo/w['source_path']).read_bytes()
 require(hashlib.sha256(sr).hexdigest()==w['source_sha256']==b['source_sha256'],'native source pin')
 R=json.loads(sr)['native_roots'];C={n:chart(z)for n,z in w['charts'].items()}
 for i in range(N):
  require(C[f'L{i}']==chart({'kind':'span','rows':[R[i]]}),'native line');require(C[f'F{i}']==chart({'kind':'ann','rows':[R[i]]}),'native facet')
 for n,z in b['charts'].items():require(w['charts'][n]==z,'all inherited charts')
 before,bt,_=replay(b,collect=True);after,nt,_=replay(w,collect=True);meta=w['masked_feedback']
 pairs=meta['pairs'];fields=meta['fields'];common=meta['common'];parts=meta['fixed_disjoint_partition'];U=sorted(i for p in parts for i in p)
 require(pairs==[[21,34],[64,108],[65,104]]and len(U)==len(set(U))==19,'three disjoint mask-source groups')
 require(meta['purified_at_M0']and meta['parameter_count']==19,'literal pure19 family')
 masks=[int(z,16)for z in meta['chosen_masks_hex']]
 require(masks==[sum(1<<i for i in p)for p in parts],'reviewed full19 mask instance')
 eligible=[]
 for j,((aa,bb),part)in enumerate(zip(pairs,parts)):
  T=C[f'MASK_CORRECTION_{j}'];require(T==chart({'kind':'ann','rows':[R[aa],R[bb]]})and len(T)==6,'actual rank6 correction chart')
  require(len(rref(C[common]+T)[0])==6,'common rank4 chart is inside correction chart')
  local=[i for i in b['released_carriers']if i not in b['targets']and len(rref(C[f'L{i}']+T)[0])==6]
  eligible.append(local);require(all(i in local for i in part),'every mask donor is a real eligible native original')
 require(eligible==meta['eligible_raw_inputs'],'exact advertised eligible geometry')
 require(w['targets']==b['targets']and len(w['targets'])==55,'same55 targets')
 pre=meta['prelude_end'];pv,pa=nt[pre];cells=[]
 for j,((aa,bb),part,u)in enumerate(zip(pairs,parts,masks)):
  source=f'MASK_SOURCE_{j}';snap=f'MASK_INITIAL_Y{j}'
  require(pv[source]==u and pa[source]==f'MASK_CORRECTION_{j}','actual stationary correction source')
  require(pv[snap]==1<<(N+aa)and pa[snap]=='M0','actual original-Y snapshot')
  require(pv[f'Y{aa}']==(1<<(N+aa))^(1<<bb)^u and pa[f'Y{aa}']==f'F{aa}','actual local primary field')
  for i in part+[aa,bb]:require(pv[f'X{i}']==1<<i and pa[f'X{i}']=='Hub','real raw Hub donor acquired')
  require(not any(o[0]=='MOVE'and o[1]in{source,snap}for o in w['operations']),'new owners are genuinely stationary')
  packet=f'P{j}';cell=meta['feedback_cells'][j];k=cell['before_operation'];v,at=nt[k]
  require(w['operations'][k:k+2]==[['ADD',packet,f'Y{aa}'],['ADD',f'Y{aa}',packet]],'actual two-ADD feedback')
  require(v[packet]==(1<<aa)^(1<<bb)^u and v[f'Y{aa}']==(1<<(N+aa))^(1<<bb)^u,'actual feedback input rows')
  require(at[packet]==at[f'Y{aa}']==f'F{aa}','actual changed first facet')
  v,at=nt[k+2];require(v[f'Y{aa}']==(1<<(N+aa))^(1<<aa)and v[packet]==(1<<(N+aa))^(1<<bb)^u,'primary completion and new packet history')
  pur=w['operations'].index(['ADD',snap,packet]);cap=w['operations'].index(['ADD',packet,fields[j]]);reset=w['operations'].index(['ADD',fields[j],packet]);ret=w['operations'].index(['CLEAR',snap]);down=w['operations'].index(['MOVE',fields[j],common])
  require(k+2<=pur<cap<reset<ret<down,'actual purification/reset/retirement/descent chronology')
  require(nt[pur][0][snap]==1<<(N+aa)and C[nt[pur][1][packet]]==C['M0'],'actual cocharted arbitrary-Y purifier')
  require(nt[cap][0][packet]==(1<<bb)^u and nt[reset+1][0][packet]==0,'pure first field and actual zero lower-packet reset')
  cells.append({'primary':aa,'target':bb,'feedback':k,'purification':pur,'capture':cap,'reset':reset,'snapshot_CLEAR':ret,'shared_descent':down})
 oldcut=b['pair_extension']['continuation_before_operation'];bv,ba=bt[oldcut];cut=meta['continuation_before_operation']
 originals={f'{p}{i}'for p in ['X','Y']for i in range(N)}
 ground=sorted(n for n,z in bv.items()if n not in originals and z and len(C[ba[n]])==0)
 require(len(ground)==25,'predecessor25 ground fields')
 def interface(ww):
  _,tr,_=replay(ww,collect=True);v,at=tr[ww['masked_feedback']['continuation_before_operation']]
  for n in ground:require(v[n]==bv[n]and len(C[at[n]])==0,('actual named ground field',n))
  for j,((aa,bb),u)in enumerate(zip(pairs,masks)):
   require(v[fields[j]]==(1<<bb)^u and at[fields[j]]==common,('actual retained masked field',j))
   require(v[f'MASK_SOURCE_{j}']==u and at[f'MASK_SOURCE_{j}']==f'MASK_CORRECTION_{j}',('actual proper correction source',j))
   require(f'MASK_INITIAL_Y{j}'not in v,'initial arbitrary-Y owner actually retired')
  for i in range(N):
   require(v[f'X{i}']==1<<i,'every cut original raw')
   if i in ww['released_carriers']:require(at[f'X{i}']==f'L{i}','actual retained native original')
   if i in ww['targets']:require(v[f'Y{i}']==(1<<(N+i))^(1<<i)and at[f'Y{i}']==f'F{i}','completed native output')
   else:require(v[f'Y{i}']==1<<(N+i)and at[f'Y{i}']=='zero','actual unfinished raw ground Y')
  owned={n:z for n,z in v.items()if n not in originals};require(all(z>>N==0 for z in owned.values()),'all actual cut owners pureX')
  for n,z in bv.items():
   if n in originals or n in fields or n.startswith('M0_PAIR_RAW_'):continue
   require(v[n]==z and C[at[n]]==C[ba[n]],('other old source record unchanged',n))
  return v,at,owned
 values,locations,owned=interface(w)
 require(w['released_carriers']==sorted(set(b['released_carriers'])-set(U))and len(w['released_carriers'])==50,'actual50 native originals')
 # Literal core matching with explicit insertions at first-source feedback cells.
 pos=pre;active=set();compared=0;mask_names={f'X{i}'for i in U};pair_roles={i for p in pairs for i in p}
 for k in range(b['pair_extension']['prelude_end'],b['pair_extension']['decode_start']):
  o=b['operations'][k]
  if o[0]=='MOVE'and o[1]in mask_names:continue
  if o[0]=='MOVE'and o[1]in{'P0','P1','P2'}and bt[k][1][o[1]]=='Hub':
   j=int(o[1][1:]);aa,bb=pairs[j]
   expected=[['ADD',f'X{i}',o[1]]for i in parts[j]]+[['MOVE',o[1],f'F{aa}'],['ADD',o[1],f'Y{aa}'],['ADD',f'Y{aa}',o[1]]]
   require(w['operations'][pos:pos+len(expected)]==expected,'actual source insertion and changed facet');pos+=len(expected);active.add(o[1])
  else:
   if o[0]=='ADD'and o[1]in{'P0','P1','P2'}and o[2]in fields:
    extra=['ADD',f'MASK_INITIAL_Y{int(o[1][1:])}',o[1]];require(w['operations'][pos]==extra,'actual purifier insertion');pos+=1
   require(w['operations'][pos]==o,('unchanged literal core',k,pos));pos+=1
   if o[0]=='ADD'and o[1]in fields and o[2]in{'P0','P1','P2'}:
    require(w['operations'][pos]==['CLEAR',f'MASK_INITIAL_Y{int(o[2][1:])}'],'actual purifier retirement');pos+=1;active.remove(o[2])
  ov,oa=bt[k+1];nv,na=nt[pos]
  for n,z in ov.items():
   if n in fields or n in active or n.startswith('M0_PAIR_RAW_')or(n.startswith('Y')and int(n[1:])in pair_roles):continue
   require(n in nv and nv[n]==z,('unaffected value',k,n))
   if n not in mask_names:require(C[na[n]]==C[oa[n]],('unaffected chart',k,n))
   compared+=1
 require(pos==meta['decode_start'],'entire retained core exhausted')
 # Every parameter is read only from an immutable raw original, exactly three times.
 event_parameter={};param_reads=[]
 require(not any(o[0]=='ADD'and(o[1]in mask_names or o[2]in mask_names)for o in b['operations']),'all19 routes originally detached')
 for j,part in enumerate(parts):
  aa=pairs[j][0]
  for i in part:
   events=[(k,o)for k,o in enumerate(w['operations'])if o[0]=='ADD'and o[1]==f'X{i}']
   require([o[2]for k,o in events]==[f'MASK_SOURCE_{j}',f'Y{aa}',f'P{j}'],'three consistent parameterized raw reads')
   require(not any(o[0]=='ADD'and o[2]==f'X{i}'for o in w['operations']),'parameter donor immutable')
   for k,o in events:event_parameter[k]=U.index(i);param_reads.append({'index':k,'source':i,'destination':o[2]})
 # Interpret formal monomials theta_i*x_i as additional independent columns.
 fv={f'X{i}':1<<i for i in range(N)};fv.update({f'Y{i}':1<<(N+i)for i in range(N)});fc=None
 for k,o in enumerate(w['operations']):
  if k==cut:fc=fv.copy()
  op,n,*q=o
  if op=='INIT':fv[n]=0
  elif op=='ADD':
   if k in event_parameter:
    idx=event_parameter[k];require(fv[n]==1<<U[idx],'formal parameter read from actual raw original');fv[q[0]]^=1<<(2*N+idx)
   else:fv[q[0]]^=fv[n]
  elif op=='CLEAR':del fv[n]
 for i in range(N):
  require(fv[f'X{i}']==1<<i and fv[f'Y{i}']==(1<<(N+i))^((1<<i)if i in w['targets']else 0),'all parameter monomials cancel at all endpoints')
 for j,part in enumerate(parts):
  formal=sum(1<<(2*N+U.index(i))for i in part)
  require(fc[f'MASK_SOURCE_{j}']==formal and fc[fields[j]]==(1<<pairs[j][1])^formal,'formal19-parameter cut fields')
 for n in ground:require(fc[n]==bv[n],'named ground fields independent of all19 parameters')
 def owned_profile(ww,tr):
  own={o[1]for o in ww['operations']if o[0]=='INIT'};p={}
  for k,o in enumerate(ww['operations']):
   if o[0]=='MOVE'and o[1]in own:
    d=len(C[tr[k][1][o[1]]])-len(C[o[2]]);require(d>0,'owned direction');p[d]=p.get(d,0)+1
  return p
 op_before,op_after=owned_profile(b,bt),owned_profile(w,nt)
 require(op_before==op_after,'complete owned MOVE profile unchanged')
 controls=[]
 def reject(label,bad,check=replay):
  try:check(bad)
  except(ValueError,KeyError)as e:controls.append({'control':label,'rejected':True,'reason':str(e)})
  else:raise ValueError(('accepted masked-source mutation',label))
 i=parts[0][0]
 for label,event in [
  ('omit true rank6 mask capture',['ADD',f'X{i}','MASK_SOURCE_0']),
  ('omit primary local mask observation',['ADD',f'X{i}','Y21']),
  ('omit actual Hub mask coefficient',['ADD',f'X{i}','P0']),
  ('omit arbitrary original-Y snapshot',['ADD','Y21','MASK_INITIAL_Y0']),
  ('omit actual Y purification',['ADD','MASK_INITIAL_Y0','P0']),
  ('omit changed packet reset',['ADD','KEEP_C0','P0']),
  ('omit actual retained-field descent',['MOVE','KEEP_C0',common]),
  ('omit correction source retirement',['CLEAR','MASK_SOURCE_0']),
  ('omit original-Y snapshot retirement',['CLEAR','MASK_INITIAL_Y0'])]:
  bad=copy.deepcopy(w);bad['operations'].remove(event);reject(label,bad)
 bad=copy.deepcopy(w);bad['operations'].insert(cut,['ADD','KEEP_C1','KEEP_C0']);bad['masked_feedback']['continuation_before_operation']=cut+1
 replay(bad);reject('changed unknown common source after all decoder reads',bad,interface)
 S=sorted(set(b['targets'])|{61,67});sm=sum(1<<i for i in S);support=0
 for z in owned.values():support|=z
 for i in range(N):support|=values[f'Y{i}']^(1<<(N+i))
 supp=[i for i in range(N)if support>>i&1]
 require(support>>N==0 and supp==sorted(set(S)|set(U))and len(supp)==76,'full cut X support76')
 quotient=len(binary_basis(z&~sm for z in owned.values()))
 require(quotient==3 and len(binary_basis(owned.values()))==57,'actual three new modes modulo reset-coordinate57')
 require(after['counts']=={'MOVE':469,'INIT':136,'ADD':448,'CLEAR':136},'complete source counts')
 require(after['movement_profile']=={1:211,2:14,3:34,4:35,5:35,6:9,7:131},'complete source profile')
 gate={127:37,64:74,1:-74}
 for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
 gl,gh=moment(gate);limit=(gl/6,gh/6);q=moment(after['movement_profile']);oq=moment(before['movement_profile'])
 result={'status':'PASS_INDEPENDENT_ACTUAL_M0_MASKED19_SOURCE_AND_FAMILY','word_sha256':PIN,'base_word_sha256':BASE,'native_source_sha256':w['source_sha256'],
  'before':before,'after':after,'actual_mask_partition':parts,'exact_eligible_native_sources':eligible,'feedback_cells':cells,
  'all25_named_ground_fields_unchanged':ground,'unaffected_core_state_comparisons':compared,
  'actual_live_owner_count':len(owned),'actual_live_owner_rank':57,'actual_owner_Y_rank':0,
  'full_cut_nonidentity_X_support':supp,'full_cut_nonidentity_X_support_count':76,
  'reset_coordinate_set_S57':S,'new_owned_X_rank_modulo_S57':quotient,
  'S57_scope':'This is a comparison coordinate set, not an assertion that raw S57 is already at ground in A word. A reset must acquire it physically.',
  'retained_raw_native_originals':w['released_carriers'],'remaining_raw_ground_Y_count':N-len(w['targets']),
  'complete_owned_MOVE_profile_before':op_before,'complete_owned_MOVE_profile_after':op_after,
  'formal_family':{'parameters':19,'added_formal_columns':19,'raw_parameter_read_events':param_reads,
   'parameter_monomials_cancel_at_all222_endpoints':True,'actual_cut_mask_forms_exact':True,
   'argument':'All parameter-dependent instructions read immutable raw originals, so the exact affine formal theta_i*x_i identity proves every binary mask selection. MOVE/INIT/CLEAR schedule is fixed. Three nonempty disjoint chosen forms give quotient rank3, not19.'},
  'whole_moment':record(q),'moment_increment':record((q[0]-oq[1],q[1]-oq[0])),
  'necessary_limiting_room':record((limit[0]-q[1],limit[1]-q[0])),'controls':controls,
  'scope':'Actual native rank6 acquisition, original-Y purification, true common descent, unchanged owned MOVE profile and all222 formal endpoint columns. All five global foundations remain open; no additional endpoints, all111 supplier or kappa.'}
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:result[k]for k in ['status','after','actual_live_owner_count','new_owned_X_rank_modulo_S57','whole_moment']},indent=2))
if __name__=='__main__':main()
