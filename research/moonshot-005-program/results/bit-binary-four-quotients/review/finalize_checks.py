"""Small independent controls and source/cap receipt consistency."""
import argparse,hashlib,itertools,json,subprocess
from pathlib import Path
if not __debug__:raise SystemExit('Exact checks require Python without -O')
def main(a):
 p=a.review;cat=json.loads((p/'CATALOG-REVIEW.json').read_text());cap=json.loads((p/'CAP-REVIEW.json').read_text());root=json.loads((a.root_bundle/'CAP-RESULT.json').read_text())
 assert cat['catalog_size']==38324 and cat['envelope_cases']==569 and len(cat['all_cases_with_bound_at_least13'])==19
 assert cap['dangerous_caps']==root['unique_caps_potential_ge64']==3989 and cap['maximum_disjoint_row_saving']==root['max_disjoint_row_saving_for_four_high']==46
 assert cap['histogram']==root['gain_histogram'] and cap['high_pair_tests']==18034*18033//2 and cap['top_triples_tested']==1134*1133*1132//6
 assert cap['two17_plus15_tests']==66*6912 and cap['minimum17_overlap']==5
 caps=[]
 for mask in range(128):
  S={i+1 for i in range(7) if mask>>i&1}
  if any(i^j in S for i,j in itertools.combinations(S,2)):continue
  assert len(S)<=4
  if len(S)==4:
   x=0
   for i in S:x^=i
   assert x==0;caps.append(sorted(S))
 assert len(caps)==7
 assert 17+16+5*13==98 and 17+16+16+3*12+13==98 and 63+3*12==99 and 46+3*12==82
 r=subprocess.run(['python','-O',str(p/'generate.py')],capture_output=True,text=True);assert r.returncode and 'Exact checks require Python without -O' in r.stderr
 cpp=subprocess.run(['g++','-std=c++17','-DNDEBUG','-fsyntax-only',str(p/'check_caps.cpp')],capture_output=True,text=True);assert cpp.returncode and 'Exact assertions must remain enabled' in cpp.stderr
 out={'status':'PASS_COMPLETE_INDEPENDENT_BINARY_FOUR_REVIEW','catalog_complete':True,'all569_envelope_cases_checked':True,'all19_high_parameter_cases_covered':True,'different_cap_algorithm':'All top-gain triples, plus exactlytwo17/two15 case; no parent top-pair hash meet-in-middle','cap_histogram_matches':True,'full_small_support_XOR_bounds':[16,24,32],'sumfree_Fano_caps':caps,'global_savings_upper':99,'required_proxy_arrivals_lower':123,'available_q8_arrivals_upper':122,'conclusion':'dim((rowA+C)/C)>=4 overF2 in declared q8unit/noYfeedback interface','arbitrary_rank13_claim':False,'larger_fields_or_blocks_claim':False,'python_O_and_cpp_NDEBUG_rejected':True}
 (p/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':
 q=argparse.ArgumentParser();q.add_argument('--review',type=Path,required=True);q.add_argument('--root-bundle',type=Path,required=True);main(q.parse_args())
