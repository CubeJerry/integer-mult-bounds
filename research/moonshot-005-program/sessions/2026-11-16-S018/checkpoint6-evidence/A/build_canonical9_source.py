"""Actual canonical9 quotient source with63 native unknown caches."""
from pathlib import Path
import argparse,copy,hashlib,importlib.util,json
from build_d4_cohort import trace
from price_d4_cohort import moment,record
PIN='dda004b1c3cae1c0d0cfb0d698c101963842db12d542fed842a82dbffc14ee44'
EXTRA=[15,35,13,1,2,0];OLD=[4,74,78];OLDN=['ZFIRST3','ZFIRST4','ZFIRST5']
def save(p,z):
 b=(json.dumps(z,indent=2)+'\n').encode();p.write_bytes(b);return hashlib.sha256(b).hexdigest()
def xor(rows):
 z=0
 for r in rows:z^=r
 return z
def coordinates(rows,target):
 b={}
 for j,r in enumerate(rows):
  z=r;c=1<<j
  while z:
   p=z.bit_length()-1
   if p in b:rr,cc=b[p];z^=rr;c^=cc
   else:b[p]=(z,c);break
  assert z,'independent mode basis required'
 c=0;z=target
 while z:
  p=z.bit_length()-1;assert p in b;r,m=b[p];z^=r;c^=m
 assert target==xor(rows[j]for j in range(len(rows))if c>>j&1)
 return c
def main():
 ap=argparse.ArgumentParser()
 for n in ['repo','work','out']:ap.add_argument('--'+n,type=Path,required=True)
 a=ap.parse_args();src=a.work/'C/canonical3-reset-source/LIBERATED-CACHED48-WORD.json';assert hashlib.sha256(src.read_bytes()).hexdigest()==PIN;w0=json.loads(src.read_text());raw=(a.repo/w0['source_path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==w0['source_sha256'];R=json.loads(raw)['native_roots']
 ep=a.repo/'research/moonshot-005-program/results/bit-leaf-capacity-quotient/author/check.py';sp=importlib.util.spec_from_file_location('canonical9_native',ep);e=importlib.util.module_from_spec(sp);sp.loader.exec_module(e);C,_,before=e.replay(w0,R)
 oldcut=w0['carrier_interface_before_operation'];ov,oa=trace(w0['operations'])[oldcut];S=w0['targets'];U=sorted(set(range(111))-set(S));um=sum(1<<i for i in U)
 canonical=[((1<<p)^sum(1<<i for i in range(111)if sum(x*y for x,y in zip(R[p],R[i]))==0))&um for p in range(111)]
 existing=w0['source_interface']['actual_native_raw_donor_caches'];missing=sorted(set(U)-set(map(int,existing)));assert missing==[15,31,53,54,57,58]
 ops=copy.deepcopy(w0['operations'][:oldcut]);native_added=[];native_events=[];early_moves=[];new_modes=[];mode_events=[];mode_descents=[]
 for i in missing:
  n=f'CANONICAL_NATIVE_RAW_{i}';native_added.append(n);assert ov[f'X{i}']==1<<i and oa[f'X{i}']==f'L{i}'
  ops.append(['INIT',n,f'L{i}']);native_events.append(len(ops));ops.append(['ADD',f'X{i}',n]);early_moves.append(len(ops));ops.append(['MOVE',f'X{i}','Hub'])
 for p in EXTRA:
  n=f'CANONICAL9_MODE_{p}';new_modes.append(n);ops.append(['INIT',n,'Hub'])
  for i in U:
   if canonical[p]>>i&1:mode_events.append(len(ops));ops.append(['ADD',f'X{i}',n])
  mode_descents.append(len(ops));ops.append(['MOVE',n,'M1'])
 cut=len(ops);removed={i:0 for i in missing}
 for o in w0['operations'][oldcut:]:
  if o[0]=='MOVE'and o[1].startswith('X')and int(o[1][1:])in removed:
   assert o==['MOVE',o[1],'Hub'];removed[int(o[1][1:])]+=1;continue
  ops.append(o)
 assert all(n==1 for n in removed.values());ops.extend([['CLEAR',n]for n in native_added+new_modes])
 w={k:copy.deepcopy(w0[k])for k in ['source_path','source_sha256','charts']};names=OLDN+new_modes;primaries=OLD+EXTRA
 w.update(schema='actual-canonical9-quotient-source-native63-v1',base_word_sha256=PIN,operations=ops,targets=S,released_carriers=S,carrier_interface_before_operation=cut,source_interface={'actual_ground_raw_coordinates':S,'actual_ground_raw_names':w0['source_interface']['actual_ground_raw_names'],'actual_native_unknown_caches':{str(i):f'CANONICAL_NATIVE_RAW_{i}'for i in U},'proper_unknown_groups':w0['source_interface']['proper_unknown_groups'],'proper_group_fields':w0['source_interface']['proper_group_fields'],'canonical_fields':names,'canonical_primaries':primaries,'canonical_chart':'M1','raw_native_originals':S,'raw_Hub_originals':U,'complete_outputs_at_cut':S,'raw_ground_output_roles':U,'new_native_capture_indices':native_events,'retimed_original_moves':early_moves,'new_mode_load_indices':mode_events,'new_mode_descent_indices':mode_descents},scope='Actual canonical rank9 quotient source at M1,63 native unknown caches,48 ground known inputs. All48 known outputs complete;63 unknown receivers raw ground. All111 canonical quotient rows lie in the9 actual modes. Distribution, receiver chains, full111 supplier and five foundations remain open; no kappa.')
 charts,hist,after=e.replay(w,R);v,at=trace(ops)[cut]
 for n,z in ov.items():
  assert v[n]==z
  if n not in {f'X{i}'for i in missing}:assert charts[at[n]]==charts[oa[n]]
 for i in range(111):
  assert v[f'X{i}']==1<<i and at[f'X{i}']==(f'L{i}'if i in S else'Hub')
  assert v[f'Y{i}']==(1<<(111+i))^((1<<i)if i in S else 0)and at[f'Y{i}']==(f'F{i}'if i in S else'zero')
 for i in U:assert v[f'CANONICAL_NATIVE_RAW_{i}']==1<<i and at[f'CANONICAL_NATIVE_RAW_{i}']==f'L{i}'
 for i in S:assert v[f'CANONICAL_RESET_RAW_{i}']==1<<i and at[f'CANONICAL_RESET_RAW_{i}']=='zero'
 rows=[v[n]for n in names]
 for p,n,row in zip(primaries,names,rows):assert row==canonical[p]and at[n]=='M1'
 assert len(e.bb(rows))==len(e.bb(canonical))==9;coords=[coordinates(rows,z)for z in canonical]
 group_rows=[v[n]for n in w['source_interface']['proper_group_fields']];assert len(group_rows)==len(e.bb(group_rows))==7 and len(e.bb(group_rows+rows))==13
 allowners=[z for n,z in v.items()if n not in {f'{p}{i}'for p in 'XY'for i in range(111)}];assert all(z>>111==0 for z in allowners)and len(e.bb(allowners))==111
 expectedprofile=before['movement_profile'].copy();expectedprofile[3]+=6;assert after['movement_profile']==expectedprofile
 assert after['counts']['INIT']==after['counts']['CLEAR']==127 and after['counts']['MOVE']==336 and after['dirty_CLEAR']==after['peak_owned']==127
 decoders=[]
 for i in U:
  locals_=[j for j in U if sum(x*y for x,y in zip(R[i],R[j]))==0];chosen=[j for j in range(9)if coords[i]>>j&1]
  assert xor(rows[j]for j in chosen)^sum(1<<j for j in locals_)==1<<i
  decoders.append({'receiver':i,'actual_mode_names':[names[j]for j in chosen],'native_raw_local_roles':locals_})
 q=moment(after['movement_profile']);oldq=moment(before['movement_profile']);gate={127:37,64:74,1:-74}
 for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
 limit=tuple(z/6 for z in moment(gate));a.out.mkdir(parents=True,exist_ok=True);pin=save(a.out/'WORD.json',w)
 res={'status':'PASS_ACTUAL_CANONICAL9_SOURCE_NATIVE63','word_sha256':pin,'base_word_sha256':PIN,'native_source_sha256':w['source_sha256'],'cut':cut,'before':before,'after':after,'known_S48':S,'unknown_U63':U,'newly_cached_and_early_Hub_unknowns':missing,'canonical_primaries':primaries,'canonical_mode_names':names,'canonical_rows_hex':list(map(hex,rows)),'canonical_quotient_rank':9,'proper_group_rank':7,'union_mode_group_rank':13,'global_owned_rank_spread_across_charts':111,'native_original_count':48,'raw_ground_Y_count':63,'extra_ADD_count':after['counts']['ADD']-before['counts']['ADD'],'complete_moment':record(q),'extra_movement':record((q[0]-oldq[1],q[1]-oldq[0])),'necessary_limiting_room':record((limit[0]-q[1],limit[1]-q[0])),'canonical_span_coefficients':[{'canonical_receiver':i,'nine_mode_coefficients_hex':hex(m),'actual_mode_names':[names[j]for j in range(9)if m>>j&1]}for i,m in enumerate(coords)],'optimistic_direct_decoder_identities':decoders,'scope':w['scope']}
 save(a.out/'RESULT.json',res);print(res['status'],pin);print(after);print('Q',res['complete_moment']['decimal'][0],'room',res['necessary_limiting_room']['decimal'][0])
if __name__=='__main__':main()
