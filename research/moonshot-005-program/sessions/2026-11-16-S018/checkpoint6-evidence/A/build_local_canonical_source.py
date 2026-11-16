"""Change source acquisition timing: gather one known-role canonical mode locally."""
from pathlib import Path
import argparse,hashlib,importlib.util,json
from build_d4_cohort import trace
from price_d4_cohort import moment,record
PIN='de6d6919f448b9f4bb09d106e35667572207c7155ab0ed9ce6193f6b17289325'
def save(p,z):
 raw=(json.dumps(z,indent=2)+'\n').encode();p.write_bytes(raw);return hashlib.sha256(raw).hexdigest()
def main():
 ap=argparse.ArgumentParser()
 for n in ['repo','work','out']:ap.add_argument('--'+n,type=Path,required=True)
 a=ap.parse_args();p=a.work/'A/canonical9-source/WORD.json';assert hashlib.sha256(p.read_bytes()).hexdigest()==PIN;old=json.loads(p.read_text());sr=(a.repo/old['source_path']).read_bytes();assert hashlib.sha256(sr).hexdigest()==old['source_sha256'];R=json.loads(sr)['native_roots'];sp=importlib.util.spec_from_file_location('local_canonical_native',a.repo/'research/moonshot-005-program/results/bit-leaf-capacity-quotient/author/check.py');e=importlib.util.module_from_spec(sp);sp.loader.exec_module(e);C,_,_=e.replay(old,R)
 S=old['targets'];U=sorted(set(range(111))-set(S));um=sum(1<<i for i in U);primaries=old['source_interface']['canonical_primaries'];names=old['source_interface']['canonical_fields'];mode=dict(zip(primaries,names));local=74;assert local in S and e.sub(C['M1'],C[f'F{local}'])
 rows={p:((1<<p)^sum(1<<i for i in range(111)if sum(x*y for x,y in zip(R[p],R[i]))==0))&um for p in primaries};localdonors=[i for i in U if rows[local]>>i&1];assert len(localdonors)==31 and all(e.sub(C[f'L{i}'],C[f'F{local}'])for i in localdonors)
 ops=[];owners=[];capture=[];loads=[];descents=[]
 for i in S:
  n=f'CANONICAL_RESET_RAW_{i}';owners.append(n);ops.extend([['INIT',n,f'L{i}'],['ADD',f'X{i}',n],['MOVE',n,'zero']])
 for i in U:
  n=f'CANONICAL_NATIVE_RAW_{i}';owners.append(n);ops.append(['INIT',n,f'L{i}']);capture.append(len(ops));ops.append(['ADD',f'X{i}',n])
 n=mode[local];owners.append(n);ops.append(['INIT',n,f'F{local}'])
 for i in localdonors:
  ops.append(['MOVE',f'X{i}',f'F{local}']);loads.append(len(ops));ops.extend([['ADD',f'X{i}',n],['MOVE',f'X{i}','Hub']])
 for i in U:
  if i not in localdonors:ops.append(['MOVE',f'X{i}','Hub'])
 descents.append(len(ops));ops.append(['MOVE',n,'M1'])
 for p in primaries:
  if p==local:continue
  n=mode[p];owners.append(n);ops.append(['INIT',n,'Hub'])
  for i in U:
   if rows[p]>>i&1:loads.append(len(ops));ops.append(['ADD',f'X{i}',n])
  descents.append(len(ops));ops.append(['MOVE',n,'M1'])
 for i in S:ops.extend([['ADD',f'CANONICAL_RESET_RAW_{i}',f'Y{i}'],['MOVE',f'Y{i}',f'F{i}']])
 cut=len(ops)
 for i in S:ops.append(['MOVE',f'X{i}','Hub'])
 for i in U:ops.append(['MOVE',f'Y{i}',f'F{i}'])
 ops.extend([['CLEAR',n]for n in owners])
 w={k:old[k]for k in ['source_path','source_sha256','charts']};w.update(schema='actual-canonical9-one-local-acquisition-native63-v1',base_word_sha256=PIN,operations=ops,targets=S,released_carriers=S,carrier_interface_before_operation=cut,source_interface={'actual_ground_raw_coordinates':S,'actual_native_unknown_caches':{str(i):f'CANONICAL_NATIVE_RAW_{i}'for i in U},'canonical_fields':names,'canonical_primaries':primaries,'canonical_chart':'M1','locally_acquired_primary':local,'local_acquisition_chart':f'F{local}','local_acquisition_donors':localdonors,'source_load_indices':loads,'native_capture_indices':capture,'mode_descent_indices':descents,'raw_native_originals':S,'raw_Hub_originals':U,'complete_outputs_at_cut':S,'raw_ground_output_roles':U,'omitted_old_proper_groups':old['source_interface']['proper_group_fields']},scope='Alternative source prefix: same nine pure canonical quotient rows at M1, same48 actual ground raw inputs and63 native caches; no seven proper group fields. One mode acquired from actual native donors at F74 before their Hub arrival, then descends rank2. Does not give remaining63 physical decoders or all111 supplier; no kappa.')
 _,_,st=e.replay(w,R);v,at=trace(ops)[cut];ov,oa=trace(old['operations'])[old['carrier_interface_before_operation']]
 for n in names:assert v[n]==ov[n]==rows[primaries[names.index(n)]]and at[n]==oa[n]=='M1'
 for i in U:assert v[f'CANONICAL_NATIVE_RAW_{i}']==1<<i and at[f'CANONICAL_NATIVE_RAW_{i}']==f'L{i}'and v[f'X{i}']==1<<i and at[f'X{i}']=='Hub'and v[f'Y{i}']==1<<(111+i)and at[f'Y{i}']=='zero'
 for i in S:assert v[f'CANONICAL_RESET_RAW_{i}']==1<<i and at[f'CANONICAL_RESET_RAW_{i}']=='zero'and v[f'X{i}']==1<<i and at[f'X{i}']==f'L{i}'and v[f'Y{i}']==(1<<i)^(1<<(111+i))and at[f'Y{i}']==f'F{i}'
 assert len(e.bb(v[n]for n in names))==9
 assert st['movement_profile']=={1:79,2:1,3:8,6:31,7:191}
 assert st['counts']=={'INIT':120,'ADD':464,'MOVE':310,'CLEAR':120}and st['dirty_CLEAR']==120
 J=[5,35,90,93,96,97,109,110];jm=sum(1<<i for i in J);assert all(sum(x*y for x,y in zip(R[i],R[j]))!=0 for i in J for j in J);dep=[n for n,z in v.items()if z&jm];assert not any(e.sub(C[at[n]],C[f'F{i}'])for n in dep for i in J)
 gate={127:37,64:74,1:-74}
 for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
 ceiling=tuple(z/6 for z in moment(gate));q=moment(st['movement_profile']);naive=moment({7:222,1:48,3:9});increment=moment({6:31,1:31,7:-31,2:1,3:-1})
 assert q[1]+8<ceiling[0]
 a.out.mkdir(parents=True,exist_ok=True);pin=save(a.out/'WORD.json',w);result={'status':'PASS_CANONICAL9_ONE_LOCAL_ACQUISITION','word_sha256':pin,'base_word_sha256':PIN,'cut':cut,'stats':st,'local_primary':local,'local_donors':localdonors,'actual_mode_rank':9,'unchanged_actual_mode_rows_and_charts':names,'actual_ground_raw_count':48,'actual_native_cache_count':63,'source_contract_change':'Seven old proper groups omitted; all nine canonical quotient modes, actual raw ground48/native63 and original/receiver locations preserved. Alternative prefix, no free adapter.','movement_moment':record(q),'saving_against_direct_all_Hub_modes':record((naive[0]-q[1],naive[1]-q[0])),'signed_profile_change_against_direct_all_Hub_modes':{6:31,1:31,7:-31,2:1,3:-1},'necessary_limiting_room':record((ceiling[0]-q[1],ceiling[1]-q[0])),'J8_dependent_initial_fields':len(dep),'J8_accessible_field_count':0,'eight_descent_floor_plus_current_source':record((q[0]+8,q[1]+8)),'remaining_room_after_eight_floor':record((ceiling[0]-q[1]-8,ceiling[1]-q[0]-8)),'scope':'This changed acquisition timing escapes the previously stated numerical eight-descent obstruction. It does not prove eight descents suffice, furnish actual63 decoders, or exclude stronger fixed-cut obstructions.'};save(a.out/'RESULT.json',result);print(result['status'],pin,st);print('Q',result['movement_moment']['decimal'][0],'room',result['necessary_limiting_room']['decimal'][0])
if __name__=='__main__':main()
