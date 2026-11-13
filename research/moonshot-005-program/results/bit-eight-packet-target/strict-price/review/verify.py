"""Independent exact arithmetic audit of the uniform derivative envelope."""
import argparse,hashlib,json,math
from fractions import Fraction as F
from pathlib import Path
if not __debug__:raise SystemExit('Exact checks require Python without -O')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main(a):
 assert sha(a.q8)=='f1ec7b16a986c7b7ce7d9a3788bbea2943810cfd70386e554bd14a21759e07e2'
 assert sha(a.uniform_result)=='8178c76d1a20c39faf11c02bbb1c143eff151c4bb7ad717fd098ba8067137936'
 assert sha(a.uniform_proof)=='fb8e8592a7305fd27797047a73807160cffb207fdf5121b438e60dbe1e55a1a7'
 assert sha(a.baseline_budget)=='92ab5d5cc08933f46c7eedb195f8d5f4e68a27dc189e6f8594876f70846db152'
 q=json.loads(a.q8.read_text());u=json.loads(a.uniform_result.read_text());b=json.loads(a.baseline_budget.read_text());left,right=F(1,200),F(2503,500000);width=right-left;assert width==F(3,500000)
 def ceil_log2(r):
  k=0;p=1
  while p<r:k+=1;p*=2
  return k
 taylor=sum((F(7,10)**j/F(math.factorial(j)) for j in range(5)),F(0));assert taylor>2
 def prof(x):return {int(r):F(v) for r,v in x.items()}
 def bound(c,baseline):
  L=sum((F(7,10)*abs(v)*r*ceil_log2(r) for r,v in c.items()),F(0));lo,hi=map(F,baseline);return L,lo-width*L,hi+width*L
 def check(ours,entry):
  assert ours==tuple(F(entry[k]) for k in ['derivative_absolute_upper','lower','upper'])
 cases={}
 for m in [2,4,6]:
  z=q['fixed_even_cases'][str(m)];T,P=prof(z['T']),prof(z['P']);c={r:F(T.get(r,0)-P.get(r,0),18*(m-1)) for r in T.keys()|P.keys()};v=bound(c,[z['perrail_margin']['lower'],z['perrail_margin']['upper']]);check(v,u['uniform_even_cases'][str(m)]);cases[m]=v
 assert cases[2][2]<0 and cases[4][2]<0 and 1<cases[6][1]<cases[6][2]<2
 N,H,T,P=[prof(q[k]) for k in ['native_paid','helper_target','paired_target','paired_paid']];ranks=N.keys()|H.keys()|T.keys()|P.keys()|{1}
 c={r:N.get(r,0)-H.get(r,0)+F(T.get(r,0)-P.get(r,0),36)-(1618 if r==1 else 0) for r in ranks};lim=bound(c,[q['limiting_perrail_margin'][k] for k in ['lower','upper']]);check(lim,u['uniform_limiting_margin']);assert 3<lim[1]<lim[2]<4
 pb=b['at_t_199_over_200']['original_paired_margin'];pair=bound({r:T.get(r,0)-P.get(r,0) for r in ranks},[pb[k] for k in ['exact_lower','exact_upper']]);check(pair,u['uniform_original_paired_moment']);assert pair[2]<0
 threshold=F(3112961,621875000);assert left<F(50001,10**7)<threshold+F(1,10**10)<right
 assert right-threshold==F(581,2487500000)
 # Specific-price oracle is a corroborating independent dependency, not used above.
 strict=json.loads(a.two_price_result.read_text())
 for z in strict['cases'].values():
  assert left<=F(z['covered_C'])<=right
  for m in [2,4,6]:assert cases[m][1]<=F(z['margins'][str(m)]['lower'])<=F(z['margins'][str(m)]['upper'])<=cases[m][2]
 out={'status':'PASS_INDEPENDENT_UNIFORM_Q8_DERIVATIVE_PROOF_AND_RECEIPT','reviewed_proof_sha256':sha(a.uniform_proof),'reviewed_result_sha256':sha(a.uniform_result),'interval':[str(left),str(right)],'positive_Taylor_exp07_lower':str(taylor),'all_rational_derivative_constants_and_envelopes_match':True,'m6_first_profitable_even_uniformly':True,'m6_exactly_one_extra_unit_call_uniformly':True,'finite_m_at_most_three_extra_unit_calls':True,'both_sharper_independent_price_intervals_contained':True,'no_float_decisions':True,'scope':'Analytic movement profile only; test exponent not admitted covered saving, atomrho, complete source, compiler, ordinary bootstrap or complex supplier.'}
 a.output.mkdir(parents=True,exist_ok=True);(a.output/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();
 for f in ['q8','uniform-result','uniform-proof','baseline-budget','two-price-result','output']:p.add_argument('--'+f,type=Path,required=True)
 main(p.parse_args())
