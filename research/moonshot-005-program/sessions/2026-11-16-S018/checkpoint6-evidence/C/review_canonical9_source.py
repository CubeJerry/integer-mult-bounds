#!/usr/bin/env python3
"""Independent exact nine-mode source and initial-chart eight-role gate."""
import argparse,copy,hashlib,json
from pathlib import Path
from release_projection import N,binary_basis,chart,replay,require,rref
from price_projection import moment,record
WORD='de6d6919f448b9f4bb09d106e35667572207c7155ab0ed9ce6193f6b17289325'
BASE='dda004b1c3cae1c0d0cfb0d698c101963842db12d542fed842a82dbffc14ee44'
PROOF='f5b20ddf5e59384ac1c994d9acae32fc37eda067ffb205214a392ccb0b64c32c'
J=[5,35,90,93,96,97,109,110]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def coordinates(rows,target):
 b={}
 for j,r in enumerate(rows):
  c=1<<j
  while r:
   p=r.bit_length()-1
   if p not in b:b[p]=(r,c);break
   s,t=b[p];r^=s;c^=t
  require(r!=0,'independent actual modes')
 c=0
 while target:
  p=target.bit_length()-1;require(p in b,'canonical span');r,t=b[p];target^=r;c^=t
 return c
def xor(rows):
 z=0
 for r in rows:z^=r
 return z
def main():
 ap=argparse.ArgumentParser()
 for n in ['repo','work','out']:ap.add_argument('--'+n,type=Path,required=True)
 a=ap.parse_args();wp=a.work/'A/canonical9-source/WORD.json';bp=a.work/'C/canonical3-reset-source/LIBERATED-CACHED48-WORD.json';pp=a.work/'A/CANONICAL9-SOURCE-PROOF.md'
 require(sha(wp)==WORD and sha(bp)==BASE and sha(pp)==PROOF,'frozen pins')
 w,b=json.loads(wp.read_text()),json.loads(bp.read_text());source=(a.repo/w['source_path']).read_bytes();require(hashlib.sha256(source).hexdigest()==w['source_sha256']=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e','native pin')
 R=json.loads(source)['native_roots'];C={n:chart(z)for n,z in w['charts'].items()}
 for i in range(N):require(C[f'L{i}']==chart({'kind':'span','rows':[R[i]]})and C[f'F{i}']==chart({'kind':'ann','rows':[R[i]]}),'native definitions')
 stats,tr,_=replay(w,collect=True);bs,bt,_=replay(b,collect=True);cut=w['carrier_interface_before_operation'];bc=b['carrier_interface_before_operation'];v,at=tr[cut];bv,ba=bt[bc]
 require(cut==873 and bc==634,'cut indices');S=w['targets'];U=sorted(set(range(N))-set(S));um=sum(1<<i for i in U);require(S==b['targets']and len(S)==48 and len(U)==63,'known and unknown sets')
 missing=[15,31,53,54,57,58];extra=[15,35,13,1,2,0];primaries=[4,74,78]+extra;names=['ZFIRST3','ZFIRST4','ZFIRST5']+[f'CANONICAL9_MODE_{i}'for i in extra]
 local=[sum(1<<j for j in range(N)if sum(x*y for x,y in zip(R[i],R[j]))==0)for i in range(N)];canonical=[((1<<i)^local[i])&um for i in range(N)]
 expected=copy.deepcopy(b['operations'][:bc]);newnames=[]
 for i in missing:
  n=f'CANONICAL_NATIVE_RAW_{i}';newnames.append(n);expected += [['INIT',n,f'L{i}'],['ADD',f'X{i}',n],['MOVE',f'X{i}','Hub']]
 for i in extra:
  n=f'CANONICAL9_MODE_{i}';newnames.append(n);expected.append(['INIT',n,'Hub']);expected += [['ADD',f'X{j}',n]for j in U if canonical[i]>>j&1];expected.append(['MOVE',n,'M1'])
 require(len(expected)==cut,'actual acquisition length')
 expected += [o for o in b['operations'][bc:]if not(o[0]=='MOVE'and o[1]in{f'X{i}'for i in missing})];expected += [['CLEAR',n]for n in newnames]
 require(w['operations']==expected,'literal source acquisition and old closure replacement')
 for n,z in bv.items():require(v[n]==z and(n in{f'X{i}'for i in missing}or C[at[n]]==C[ba[n]]),('old cut row/chart',n))
 for i in range(N):
  require(v[f'X{i}']==1<<i and at[f'X{i}']==(f'L{i}'if i in S else'Hub'),'actual original custody')
  require(v[f'Y{i}']==(1<<(N+i))^((1<<i)if i in S else 0)and at[f'Y{i}']==(f'F{i}'if i in S else'zero'),'actual receiver cut row/chart')
 for i in U:require(v[f'CANONICAL_NATIVE_RAW_{i}']==1<<i and at[f'CANONICAL_NATIVE_RAW_{i}']==f'L{i}','actual native cache')
 for i in S:require(v[f'CANONICAL_RESET_RAW_{i}']==1<<i and at[f'CANONICAL_RESET_RAW_{i}']=='zero','actual raw ground record')
 rows=[v[n]for n in names]
 for p,n,z in zip(primaries,names,rows):require(z==canonical[p]and at[n]=='M1','actual common canonical row')
 require(len(binary_basis(rows))==len(binary_basis(canonical))==9,'canonical rank nine')
 coeff=[coordinates(rows,z)for z in canonical];author=json.loads((wp.parent/'RESULT.json').read_text());controls=json.loads((wp.parent/'CONTROLS.json').read_text())
 require(coeff==[int(q['nine_mode_coefficients_hex'],16)for q in author['canonical_span_coefficients']]==[int(q,16)for q in controls['canonical_111_by9_coefficients_hex']],'all111 coefficients independently recomputed')
 for i in U:require(xor(rows[j]for j in range(9)if coeff[i]>>j&1)^(local[i]&um)==1<<i,'63 optimistic identities')
 cols=controls['independent_minor_input_columns'];minor=[sum(((z>>k)&1)<<j for j,k in enumerate(cols))for z in rows];require(len(cols)==9 and len(binary_basis(minor))==9,'invertible actual minor')
 groups=w['source_interface']['proper_group_fields'];grows=[v[n]for n in groups];require(len(grows)==len(binary_basis(grows))==7 and len(binary_basis(grows+rows))==13,'group and union ranks')
 originals={f'{p}{i}'for p in 'XY'for i in range(N)};owners=set(v)-originals;require(len(owners)==127 and all(v[n]>>N==0 for n in owners)and len(binary_basis(v[n]for n in owners))==111,'global rank at separate charts')
 require(stats['counts']=={'INIT':127,'ADD':521,'MOVE':336,'CLEAR':127}and stats['dirty_CLEAR']==stats['peak_owned']==127,'full invoice')
 profile={1:67,2:37,3:10,4:1,5:37,6:19,7:165};require(stats['movement_profile']==profile,'full profile')
 q=moment(profile);gate={127:37,64:74,1:-74}
 for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
 limit=tuple(z/6 for z in moment(gate));require(set(J)<=set(U),'eight unfinished demands')
 dots=[[sum(x*y for x,y in zip(R[i],R[j]))for j in J]for i in J];require(all(z for row in dots for z in row),'pairwise nonorthogonality including diagonal')
 jm=sum(1<<i for i in J);ledger=[]
 for n,z in v.items():
  if not z&jm:continue
  dest=[i for i in J if len(rref(C[at[n]]+C[f'F{i}'])[0])==7]
  require(not dest,('no initial J-dependent field has upward target access',n,dest));ledger.append({'field':n,'chart':at[n],'J_support':[i for i in J if z>>i&1],'accessible_J_targets':dest})
 require(len(ledger)==30,'all thirty J-dependent live fields')
 tail=w['operations'][cut:];moves=[o for o in tail if o[0]=='MOVE'];clears=[o for o in tail if o[0]=='CLEAR'];require(len(tail)==len(moves)+len(clears)and len(moves)==111 and len(clears)==127,'suffix is direct original closures and CLEARs')
 for o in moves:require(o[1]in originals and o[2]==('Hub'if o[1].startswith('X')else f'F{o[1][1:]}'),'direct original closure')
 floor=(q[0]+8,q[1]+8);require(floor[0]>limit[1],'fixed-cut eight-descent floor excludes room')
 direct=moment({7:222,1:56,3:9});require(direct[0]>limit[1],'scoped direct-source lower bound exceeds gate')
 negatives=[]
 for label,op,field,test in [
  ('missing_native_capture',['ADD','X15','CANONICAL_NATIVE_RAW_15'],'CANONICAL_NATIVE_RAW_15',lambda z,l:z==0),
  ('missing_mode_load',w['operations'][w['source_interface']['new_mode_load_indices'][0]],'CANONICAL9_MODE_15',lambda z,l:z!=canonical[15]),
  ('missing_mode_descent',['MOVE','CANONICAL9_MODE_15','M1'],'CANONICAL9_MODE_15',lambda z,l:l=='Hub')]:
  bad=copy.deepcopy(w);bad['operations'].remove(op);_,t,_=replay(bad,collect=True);vv,ll=t[cut-1];require(test(vv[field],ll[field]),label);negatives.append({'type':label,'omitted_operation':op,'endpoints_pass_but_actual_source_fails':True})
 for label,op in [('missing_early_Hub_arrival',['MOVE','X15','Hub']),('missing_CLEAR',['CLEAR','CANONICAL9_MODE_15'])]:
  bad=copy.deepcopy(w);bad['operations'].remove(op)
  try:replay(bad)
  except ValueError as e:negatives.append({'type':label,'omitted_operation':op,'rejection':str(e)})
  else:raise ValueError('accepted invalid '+label)
 result={'status':'PASS_INDEPENDENT_ACTUAL_CANONICAL9_AND_SCOPED_EIGHT_DESCENT_GATE','word_sha256':WORD,'proof_sha256':PROOF,'base_word_sha256':BASE,'native_source_sha256':w['source_sha256'],'cut':cut,'stats':stats,'known48':S,'unknown63':U,'actual_native_unknown_caches':63,'actual_known_raw_ground_records':48,'raw_native_originals':S,'raw_Hub_originals':U,'all_old_cut_values_preserved':True,'retimed_originals':missing,'canonical_names':names,'canonical_primaries':primaries,'canonical_rows_hex':list(map(hex,rows)),'independently_recomputed_111_by9_coefficients_hex':list(map(hex,coeff)),'canonical_rank':9,'proper_group_rank':7,'union_rank':13,'invertible_minor_columns':cols,'invertible_minor_rows_hex':list(map(hex,minor)),'global_owned_rank_at_separate_charts':111,'independent_representative_semantic_controls':negatives,'author_239_controls_not_all_rerun':True,'whole_moment':record(q),'necessary_limiting_allowance':record(limit),'necessary_room':record((limit[0]-q[1],limit[1]-q[0])),'J8_gate':{'witness':J,'native_dot_matrix':dots,'initial_J_dependent_field_ledger':ledger,'minimum_future_owned_descents':8,'suffix_direct_original_closures':111,'suffix_CLEARs':127,'completion_floor':record(floor),'excess':record((floor[0]-limit[1],floor[1]-limit[0]))},'scoped_direct_source_gate':{'profile':{7:222,1:56,3:9},'formula':'222*7^(199/200)+48+9*3^(199/200)+8','floor':record(direct),'excess':record((direct[0]-limit[1],direct[1]-limit[0])),'class':'All222 original rank-seven closures,48 actual native-to-ground whole-field acquisitions,nine whole code fields acquired at Hub and held at M1 before the frozen cut,and the same zero-access J8 initial-chart premise. Future eight descents occur after that cut. Not an arbitrary-source lower bound.'},'scope':'Physical source and exact canonical matrix identities, not a physical all111 decoder. Frozen-cut exclusion permits arbitrary cocharted nonlinear arithmetic but does not restrict changed earlier sources or placement. Formal all222 endpoint replay does not discharge global native_all_columns. All five foundations remain open; no kappa.'}
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status']);print('cut',cut,'Q',record(q)['decimal'][0],'direct excess',result['scoped_direct_source_gate']['excess']['decimal'][0])
if __name__=='__main__':main()
