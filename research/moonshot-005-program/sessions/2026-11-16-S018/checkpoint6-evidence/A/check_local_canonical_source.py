"""Exact source omissions and inherited canonical matrix identity for local gather."""
from pathlib import Path
import argparse,copy,hashlib,importlib.util,json
from build_d4_cohort import trace

def main():
 ap=argparse.ArgumentParser()
 for n in ['repo','work','word','out']:ap.add_argument('--'+n,type=Path,required=True)
 a=ap.parse_args();raw=a.word.read_bytes();w=json.loads(raw);sr=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(sr).hexdigest()==w['source_sha256'];R=json.loads(sr)['native_roots'];sp=importlib.util.spec_from_file_location('local_canonical_controls',a.repo/'research/moonshot-005-program/results/bit-leaf-capacity-quotient/author/check.py');e=importlib.util.module_from_spec(sp);sp.loader.exec_module(e);C,_,st=e.replay(w,R);ops=w['operations'];cut=w['carrier_interface_before_operation'];v,at=trace(ops)[cut];m=w['source_interface'];cases=[]
 for label,key in [('actual_native_capture','native_capture_indices'),('actual_canonical_input','source_load_indices'),('actual_mode_descent','mode_descent_indices')]:cases.extend((label,k)for k in m[key])
 cases.extend(('native_donor_facet_visit',k)for k,o in enumerate(ops)if o[0]=='MOVE'and o[1].startswith('X')and o[2]==m['local_acquisition_chart'])
 cases.extend(('mode_retirement',k)for k,o in enumerate(ops)if o[0]=='CLEAR'and o[1]in m['canonical_fields'])
 controls=[]
 for label,k in cases:
  bad=copy.deepcopy(w);del bad['operations'][k];bc=cut-(k<cut)
  try:e.replay(bad,R)
  except(AssertionError,KeyError):reason='exact native colocation/endpoint/ownership rejects'
  else:
   bv,ba=trace(bad['operations'])[bc];assert bv!=v or any(C[ba[n]]!=C[at[n]]for n in v);reason='partial48 endpoints pass; actual cut source rejects'
  controls.append({'kind':label,'index':k,'operation':ops[k],'rejection':reason})
 cert=json.loads((a.work/'A/canonical9-source/CONTROLS.json').read_text());assert cert['mode_basis_names']==m['canonical_fields'];rows=[v[n]for n in m['canonical_fields']];um=sum(1<<i for i in range(111)if i not in w['targets']);coeff=list(map(lambda x:int(x,16),cert['canonical_111_by9_coefficients_hex']))
 assert len(e.bb(rows))==9
 for i,c in enumerate(coeff):
  z=0
  for j in range(9):
   if c>>j&1:z^=rows[j]
  expected=((1<<i)^sum(1<<j for j in range(111)if sum(x*y for x,y in zip(R[i],R[j]))==0))&um;assert z==expected
 primary=m['locally_acquired_primary'];localname=m['canonical_fields'][m['canonical_primaries'].index(primary)];assert primary in w['targets']and C[m['local_acquisition_chart']]==C[f'F{primary}']and e.sub(C['M1'],C[f'F{primary}'])
 for i in m['local_acquisition_donors']:assert i not in w['targets']and sum(x*y for x,y in zip(R[primary],R[i]))==0
 for o in ops:
  if o[0]=='ADD'and o[2]==localname:
   k=ops.index(o);vv,aa=trace(ops)[k];assert vv[o[1]]==1<<int(o[1][1:]) and aa[o[1]]==aa[localname]==f'F{primary}'
 result={'status':'PASS_LOCAL_CANONICAL_SOURCE_CONTROLS_AND_UNIVERSAL_SPAN','word_sha256':hashlib.sha256(raw).hexdigest(),'all_222_native_baseline':st,'control_count':len(controls),'controls':controls,'canonical_111_row_identity_verified_against_actual_modes':True,'canonical_rank':9,'actual_local_primary':primary,'actual_local_donor_count':len(m['local_acquisition_donors']),'actual_all_local_donor_capture_columns_and_charts_checked':True,'scope':'Earlier native acquisition changes the source price. The inherited exact nine-mode span is preserved. No physical63decoder or eight-descent sufficiency claim.'};a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,indent=2)+'\n');print(result['status'],len(controls))
if __name__=='__main__':main()
