"""Native/source omission controls and universal canonical matrix identity."""
from pathlib import Path
import argparse,copy,hashlib,importlib.util,json
from build_d4_cohort import trace
from price_d4_cohort import moment,record

def main():
 ap=argparse.ArgumentParser()
 for n in ['repo','word','out']:ap.add_argument('--'+n,type=Path,required=True)
 a=ap.parse_args();raw=a.word.read_bytes();w=json.loads(raw);sr=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(sr).hexdigest()==w['source_sha256'];R=json.loads(sr)['native_roots'];ep=a.repo/'research/moonshot-005-program/results/bit-leaf-capacity-quotient/author/check.py';sp=importlib.util.spec_from_file_location('canonical9_controls',ep);e=importlib.util.module_from_spec(sp);sp.loader.exec_module(e);C,_,st=e.replay(w,R);cut=w['carrier_interface_before_operation'];v,at=trace(w['operations'])[cut];m=w['source_interface'];ops=w['operations'];cases=[]
 for label,key in [('native_raw_capture','new_native_capture_indices'),('early_original_Hub_arrival','retimed_original_moves'),('actual_mode_input','new_mode_load_indices'),('actual_common_descent','new_mode_descent_indices')]:
  cases.extend((label,k)for k in m[key])
 fresh={f'CANONICAL_NATIVE_RAW_{i}'for i in [15,31,53,54,57,58]}|set(m['canonical_fields'][3:])
 cases.extend(('owned_retirement',k)for k,o in enumerate(ops)if o[0]=='CLEAR'and o[1]in fresh)
 reports=[]
 for label,k in cases:
  b=copy.deepcopy(w);del b['operations'][k];bc=cut-(k<cut)
  try:e.replay(b,R)
  except(AssertionError,KeyError)as er:failure='native geometry, endpoint or ownership rejects'
  else:
   bv,ba=trace(b['operations'])[bc];assert bv!=v or any(C[ba[n]]!=C[at[n]]for n in v);failure='partial endpoints pass; declared actual source rejects'
  reports.append({'kind':label,'operation_index':k,'operation':ops[k],'rejection':failure})
 S=w['targets'];U=sorted(set(range(111))-set(S));um=sum(1<<i for i in U);names=m['canonical_fields'];rows=[v[n]for n in names];assert len(rows)==9
 # A concrete invertible9x9 minor proves independence; a111x9 coefficient
 # matrix proves the entire canonical quotient matrix lies in these9 rows.
 pivots=sorted(e.bb(rows));assert len(pivots)==9
 minor=[sum(((r>>p)&1)<<j for j,p in enumerate(pivots))for r in rows];assert len(e.bb(minor))==9
 def solve(target):
  basis={}
  for j,r in enumerate(rows):
   z=r;c=1<<j
   while z:
    p=z.bit_length()-1
    if p in basis:rr,cc=basis[p];z^=rr;c^=cc
    else:basis[p]=(z,c);break
  z=target;c=0
  while z:
   p=z.bit_length()-1;assert p in basis;r,m=basis[p];z^=r;c^=m
  test=0
  for j in range(9):
   if c>>j&1:test^=rows[j]
  assert test==target
  return c
 coefficients=[]
 for i in range(111):
  row=((1<<i)^sum(1<<j for j in range(111)if sum(x*y for x,y in zip(R[i],R[j]))==0))&um;coefficients.append(solve(row))
 assert len(e.bb(rows))==9
 result={'status':'PASS_CANONICAL9_NATIVE_SOURCE_CONTROLS_AND_MATRIX_CERTIFICATE','word_sha256':hashlib.sha256(raw).hexdigest(),'all_222_native_baseline':st,'control_count':len(reports),'controls':reports,'mode_basis_names':names,'independent_minor_input_columns':pivots,'invertible_minor_rows_hex':list(map(hex,minor)),'canonical_111_by9_coefficients_hex':list(map(hex,coefficients)),'quantified_identity':'For every F2 vector space V and all111 independent x_i in V, the actual9 fields span every canonical row K_i restricted to U. The binary matrix identity and invertible9x9 minor certify this uniformly; no enumeration of input assignments is used.','scope':'Physical source contract, not physical receiver decoding. Globally granting the9 modes and every raw geometric local yields all111 algebraic outputs; those grants are not supplied by this word. Frozen-cut completion remains a separate priced obligation.'}
 J=[5,35,90,93,96,97,109,110];jm=sum(1<<i for i in J);assert set(J).isdisjoint(S)
 assert all(sum(x*y for x,y in zip(R[i],R[j]))!=0 for i in J for j in J)
 dep=[n for n,z in v.items()if z&jm];access={str(i):[n for n in dep if e.sub(C[at[n]],C[f'F{i}'])]for i in J};assert all(not ns for ns in access.values())
 gate={127:37,64:74,1:-74}
 for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
 limit=tuple(z/6 for z in moment(gate));q=moment(st['movement_profile']);direct=moment({7:222,1:56,3:9})
 cutgate={'status':'PASS_CANONICAL9_J8_INITIAL_CHART_PREMISE','word_sha256':result['word_sha256'],'J8':J,'J_dependent_initial_fields':[{'name':n,'chart':at[n],'J_row_hex':hex(v[n]&jm)}for n in dep],'accessible_J_fields_by_receiver':access,'future_owned_descent_floor':8,'actual_closed_word_plus_floor':record((q[0]+8,q[1]+8)),'necessary_ceiling':record(limit),'optimistic_direct_known48_nineM1_modes_plus8':record(direct),'direct_optimistic_excess':record((direct[0]-limit[1],direct[1]-limit[0])),'scope':'Concrete premise check for the retained initial-chart transcript theorem; no new theorem claimed. Native charts and actual cut rows checked on the literal word. Rules out fixed-cut suffix, not earlier history or placement changes.'}
 a.out.parent.mkdir(parents=True,exist_ok=True);(a.out.parent/'J8-CUT-GATE.json').write_text(json.dumps(cutgate,indent=2)+'\n');a.out.write_text(json.dumps(result,indent=2)+'\n');print(result['status'],len(reports),'controls; minor',pivots)

if __name__=='__main__':main()
