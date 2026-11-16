"""Native omissions and a279-column formal proof of the57-parameter mask family."""
import argparse,copy,hashlib,importlib.util,json
from pathlib import Path
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--word',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--repo',type=Path,default=Path('/workspace/scratch/b421dd0c4c1e/integer-mult-bounds'));a=ap.parse_args();raw=a.word.read_bytes();w=json.loads(raw);sr=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(sr).hexdigest()==w['source_sha256'];R=json.loads(sr)['native_roots'];s=importlib.util.spec_from_file_location('ascending_controls',a.repo/'research/moonshot-005-program/results/bit-leaf-capacity-quotient/author/check.py');e=importlib.util.module_from_spec(s);s.loader.exec_module(e);_,_,baseline=e.replay(w,R);ops=w['operations'];m=w['ascending_corrections'];cases=[]
 for label,key in [('raw_group_acquisition','raw_group_capture_indices'),('actual_packet_mask_load','packet_load_indices'),('actual_ground_nuisance_precoat','ground_precoat_indices'),('actual_original_coupling','carrier_coupling_indices'),('actual_facet_carrier_read','carrier_reader_indices'),('actual_Hub_original_inverse','carrier_restore_indices')]:cases.extend((label,k)for k in m[key])
 for k,o in enumerate(ops):
  if o[0]=='ADD'and o[1].startswith('ASC_GROUP_')and o[2]in{'Y4','Y74','Y78'}:cases.append(('direct_stationary_group_read',k))
  if o in[['ADD','ZFIRST3','P3'],['ADD','ZFIRST4','P4'],['ADD','ZFIRST5','P5']]:cases.append(('inherited_packet_reset',k))
 rejected=[]
 for label,k in cases:
  z=copy.deepcopy(w);del z['operations'][k]
  try:e.replay(z,R)
  except(AssertionError,KeyError)as ex:rejected.append({'kind':label,'index':k,'operation':ops[k],'failure':str(ex)[:110]or'222-column endpoint identity'})
  else:raise AssertionError(('accepted omission',label,k))
 # Each selected input's three coupled appearances are replaced by one new
 # formal independent vector z_i. This is an affine-linear identity proof,
 # specializing z_i=beta_i*x_i, rather than enumeration of scalar samples.
 inputs=sorted(int(ops[k][1][1:])for k in m['raw_group_capture_indices']);assert len(inputs)==57 and len(set(inputs))==57;formal={i:1<<(222+j)for j,i in enumerate(inputs)};special=set(m['raw_group_capture_indices']+m['packet_load_indices']+m['carrier_restore_indices']);v={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)};at={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)};cut=None
 for k,o in enumerate(ops):
  if k==w['carrier_interface_before_operation']:cut=(v.copy(),at.copy())
  typ,n,*q=o
  if typ=='INIT':v[n]=0;at[n]=q[0]
  elif typ=='MOVE':at[n]=q[0]
  elif typ=='ADD':v[q[0]]^=formal[int(n[1:])]if k in special else v[n]
  elif typ=='CLEAR':del v[n],at[n]
 for i in range(111):assert v[f'X{i}']==1<<i and v[f'Y{i}']==(1<<(111+i))^((1<<i)if i in w['targets']else 0)
 assert cut is not None;cv,ca=cut
 for i in range(111):assert cv[f'X{i}']==1<<i
 groups={tuple(map(int,k.split('_')))if k else():vals for k,vals in m['groups'].items()}
 formal_part=((1<<57)-1)<<222
 for group,values in groups.items():
  if group:assert cv['ASC_GROUP_'+'_'.join(map(str,group))]==sum(formal[i]for i in values)
 for aa,f in zip([4,74,78],['ZFIRST3','ZFIRST4','ZFIRST5']):
  expect=sum(formal[i]for g,values in groups.items()if aa in g for i in values);assert cv[f]&formal_part==expect
 res={'status':'PASS_ASCENDING_CARRIER_NATIVE_AND_FORMAL_CONTROLS','word_sha256':hashlib.sha256(raw).hexdigest(),'baseline':baseline,'omission_control_count':len(rejected),'rejected':rejected,'formal_input_columns':279,'independent_parameter_count':57,'formal_original_endpoints_and_restores_pass':True,'formal_retained_group_and_canonical_mask_rows_pass':True,'scope':'Literal native replay plus a linear formal57-input perturbation certificate specialized by z_i=beta_i*x_i. It proves the shared-mask family for all binary57 choices; it is not a finite scan.'};a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(res,indent=2)+'\n');print(res['status'],len(rejected),res['formal_input_columns'])
if __name__=='__main__':main()
