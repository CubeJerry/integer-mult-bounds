#!/usr/bin/env python3
"""Independent literal review of native-facet acquisition of one canonical mode."""
import argparse,copy,hashlib,json
from pathlib import Path
from release_projection import N,binary_basis,chart,replay,require,rref
from price_projection import moment,record
from review_canonical9_source import coordinates,xor
WORD='3643c6db33ce5ed1ea61724b126a8a3cad28be0c728376193b1f11fbf0457565'
OLD='de6d6919f448b9f4bb09d106e35667572207c7155ab0ed9ce6193f6b17289325'
PROOF='f207b6ec707d3bc4bda8470d7ba0cee9240e7f3d010191154da0218552c9bc5f'
J=[5,35,90,93,96,97,109,110]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser()
 for n in ['repo','work','out']:ap.add_argument('--'+n,type=Path,required=True)
 a=ap.parse_args();wp=a.work/'A/local-canonical9-source/WORD.json';op=a.work/'A/canonical9-source/WORD.json';require(sha(wp)==WORD and sha(op)==OLD,'frozen sources')
 w,old=json.loads(wp.read_text()),json.loads(op.read_text());source=(a.repo/w['source_path']).read_bytes();require(hashlib.sha256(source).hexdigest()==w['source_sha256']=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e','native source')
 require(sha(a.work/'A/LOCAL-CANONICAL-SOURCE-PROOF.md')==PROOF,'final author proof pin')
 R=json.loads(source)['native_roots'];C={n:chart(z)for n,z in w['charts'].items()}
 for i in range(N):require(C[f'L{i}']==chart({'kind':'span','rows':[R[i]]})and C[f'F{i}']==chart({'kind':'ann','rows':[R[i]]}),'native chart definitions')
 stats,tr,_=replay(w,collect=True);_,ot,_=replay(old,collect=True);cut=w['carrier_interface_before_operation'];v,at=tr[cut];ov,oa=ot[old['carrier_interface_before_operation']]
 S=w['targets'];U=sorted(set(range(N))-set(S));um=sum(1<<i for i in U);require(S==old['targets']and len(S)==48 and len(U)==63,'known48 and unknown63')
 primaries=[4,74,78,15,35,13,1,2,0];names=['ZFIRST3','ZFIRST4','ZFIRST5']+[f'CANONICAL9_MODE_{i}'for i in primaries[3:]];mode=dict(zip(primaries,names))
 local=[sum(1<<j for j in range(N)if sum(x*y for x,y in zip(R[i],R[j]))==0)for i in range(N)];canonical=[((1<<i)^local[i])&um for i in range(N)]
 donors=[i for i in U if canonical[74]>>i&1];require(74 in S and len(donors)==31 and donors==w['source_interface']['local_acquisition_donors'],'31 genuine local canonical donors')
 for i in donors:require(len(rref(C[f'L{i}']+C['F74'])[0])==7,'native donor lies below acquisition facet')
 require(len(C['M1'])==5 and len(C['F74'])==7 and len(rref(C['M1']+C['F74'])[0])==7,'legal rank-two packet descent')
 expected=[];owners=[]
 for i in S:
  n=f'CANONICAL_RESET_RAW_{i}';owners.append(n);expected += [['INIT',n,f'L{i}'],['ADD',f'X{i}',n],['MOVE',n,'zero']]
 for i in U:
  n=f'CANONICAL_NATIVE_RAW_{i}';owners.append(n);expected += [['INIT',n,f'L{i}'],['ADD',f'X{i}',n]]
 n=mode[74];owners.append(n);expected.append(['INIT',n,'F74'])
 for i in donors:expected += [['MOVE',f'X{i}','F74'],['ADD',f'X{i}',n],['MOVE',f'X{i}','Hub']]
 for i in U:
  if i not in donors:expected.append(['MOVE',f'X{i}','Hub'])
 expected.append(['MOVE',n,'M1'])
 for p in primaries:
  if p==74:continue
  n=mode[p];owners.append(n);expected.append(['INIT',n,'Hub']);expected += [['ADD',f'X{i}',n]for i in U if canonical[p]>>i&1];expected.append(['MOVE',n,'M1'])
 for i in S:expected += [['ADD',f'CANONICAL_RESET_RAW_{i}',f'Y{i}'],['MOVE',f'Y{i}',f'F{i}']]
 require(len(expected)==cut,'literal cut after actual acquisition and known completions')
 expected += [['MOVE',f'X{i}','Hub']for i in S]+[['MOVE',f'Y{i}',f'F{i}']for i in U]+[['CLEAR',n]for n in owners]
 require(w['operations']==expected,'independently reconstructed complete ordinary word')
 omitted=set(old['source_interface']['proper_group_fields']);require(set(v)==set(ov)-omitted,'exactly seven old group records omitted')
 for n,z in v.items():require(z==ov[n]and C[at[n]]==C[oa[n]],('all retained old cut rows and actual charts identical',n))
 for i in U:
  require(v[f'CANONICAL_NATIVE_RAW_{i}']==1<<i and at[f'CANONICAL_NATIVE_RAW_{i}']==f'L{i}','actual native raw cache')
  require(v[f'X{i}']==1<<i and at[f'X{i}']=='Hub'and v[f'Y{i}']==1<<(N+i)and at[f'Y{i}']=='zero','unknown original/receiver state')
 for i in S:
  require(v[f'CANONICAL_RESET_RAW_{i}']==1<<i and at[f'CANONICAL_RESET_RAW_{i}']=='zero','actual known ground copy')
  require(v[f'X{i}']==1<<i and at[f'X{i}']==f'L{i}'and v[f'Y{i}']==(1<<i)^(1<<(N+i))and at[f'Y{i}']==f'F{i}','known original/receiver state')
 rows=[v[n]for n in names]
 for p,n,z in zip(primaries,names,rows):require(z==canonical[p]and at[n]=='M1','actual common canonical mode')
 require(len(binary_basis(rows))==len(binary_basis(canonical))==9,'rank nine')
 coeff=[coordinates(rows,z)for z in canonical]
 for i in U:require(xor(rows[j]for j in range(9)if coeff[i]>>j&1)^(local[i]&um)==1<<i,'all63 static identities')
 profile={1:79,2:1,3:8,6:31,7:191};require(stats['movement_profile']==profile and stats['counts']=={'INIT':120,'ADD':464,'MOVE':310,'CLEAR':120}and stats['dirty_CLEAR']==stats['peak_owned']==120,'whole invoice and price profile')
 jm=sum(1<<i for i in J);ledger=[]
 require(set(J)<=set(U)and all(sum(x*y for x,y in zip(R[i],R[j]))!=0 for i in J for j in J),'same unfinished nonorthogonal witness')
 for n,z in v.items():
  if not z&jm:continue
  dest=[i for i in J if len(rref(C[at[n]]+C[f'F{i}'])[0])==7];require(not dest,'same zero-access premise');ledger.append({'field':n,'chart':at[n],'J_support':[i for i in J if z>>i&1],'accessible_J_targets':dest})
 gate={127:37,64:74,1:-74}
 for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
 limit=tuple(z/6 for z in moment(gate));q=moment(profile);direct=moment({7:222,1:48,3:9});change=moment({6:31,1:31,7:-31,2:1,3:-1});require(q[1]+8<limit[0],'eight-floor does not exclude this changed prefix')
 negatives=[]
 for label,operation,field,test in [
  ('missing_native_capture',['ADD','X15','CANONICAL_NATIVE_RAW_15'],'CANONICAL_NATIVE_RAW_15',lambda z,l:z==0),
  ('missing_local_code_input',['ADD',f'X{donors[0]}',mode[74]],mode[74],lambda z,l:z!=canonical[74]),
  ('missing_local_packet_descent',['MOVE',mode[74],'M1'],mode[74],lambda z,l:l=='F74')]:
  bad=copy.deepcopy(w);bad['operations'].remove(operation);_,t,_=replay(bad,collect=True);vv,ll=t[cut-1];require(test(vv[field],ll[field]),label);negatives.append({'type':label,'operation':operation,'endpoints_pass_but_source_fails':True})
 for label,operation in [('missing_native_donor_arrival',['MOVE',f'X{donors[0]}','F74']),('missing_local_packet_CLEAR',['CLEAR',mode[74]])]:
  bad=copy.deepcopy(w);bad['operations'].remove(operation)
  try:replay(bad)
  except ValueError as e:negatives.append({'type':label,'operation':operation,'rejection':str(e)})
  else:raise ValueError('invalid control passed '+label)
 result={'status':'PASS_INDEPENDENT_LOCAL_CANONICAL9_ACQUISITION_AND_REVISED_EIGHT_GATE','word_sha256':WORD,'comparison_word_sha256':OLD,'native_source_sha256':w['source_sha256'],'cut':cut,'stats':stats,'local_primary':74,'actual_local_donors':donors,'local_packet_birth_chart':'F74','local_packet_descent_rank':2,'other_eight_packets_actual_Hub_to_M1':True,'omitted_old_proper_groups':sorted(omitted),'every_retained_old_cut_row_and_chart_identical':True,'actual_ground_known_copies':48,'actual_native_unknown_caches':63,'canonical_rank':9,'all111_canonical_coefficients_hex':list(map(hex,coeff)),'all63_optimistic_static_identities':True,'whole_moment':record(q),'necessary_allowance':record(limit),'necessary_room':record((limit[0]-q[1],limit[1]-q[0])),'signed_profile_change_against_direct_nine_Hub_source':{6:31,1:31,7:-31,2:1,3:-1},'price_change_against_direct_nine_Hub_source':record(change),'saving_against_direct_nine_Hub_source':record((direct[0]-q[1],direct[1]-q[0])),'J8_witness':J,'J8_initial_dependent_field_ledger':ledger,'minimum_future_owned_descents':8,'eight_descent_floor':record((q[0]+8,q[1]+8)),'room_after_eight_floor':record((limit[0]-q[1]-8,limit[1]-q[0]-8)),'semantic_controls':negatives,'scope':'Alternative earlier acquisition prefix, not a free adapter. One mode is acquired at F74, so the earlier nine-Hub-acquired-mode architecture bound does not apply. The same zero-access witness still requires eight future descents, but that necessary floor no longer excludes budget. It does not show eight suffice or implement the63 missing physical decoders. All five global foundations remain open; no kappa.'}
 result['author_proof_sha256']=PROOF
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status']);print('cut',cut,'Q',record(q)['decimal'][0],'remaining after eight',result['room_after_eight_floor']['decimal'][0],'J-dependent',len(ledger))
if __name__=='__main__':main()
