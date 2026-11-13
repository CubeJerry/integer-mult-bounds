"""Independent Lipschitz envelope, not the author's log/exp price oracle."""
from pathlib import Path
from fractions import Fraction as F
import argparse,json,hashlib,math
if not __debug__:raise SystemExit('Exact assertions required')
def sha(b):return hashlib.sha256(b).hexdigest()
def main(a):
 raw=a.q8.read_bytes();assert sha(raw)=='f1ec7b16a986c7b7ce7d9a3788bbea2943810cfd70386e554bd14a21759e07e2';q=json.loads(raw)
 rawb=a.budget.read_bytes();assert sha(rawb)=='92ab5d5cc08933f46c7eedb195f8d5f4e68a27dc189e6f8594876f70846db152';b=json.loads(rawb)
 k0=F(1,200);k1=F(2503,500000);eps=k1-k0;assert eps==F(3,500000)
 assert sum(F(7,10)**j/math.factorial(j) for j in range(5))>2 # exp(7/10)>2
 def profile(z):return {int(k):F(v) for k,v in z.items()}
 def lips(c):return F(7,10)*sum(abs(v)*r*((r-1).bit_length()) for r,v in c.items())
 def extend(c,lo,hi):
  L=lips(c);return {'derivative_absolute_upper':str(L),'lower':str(F(lo)-eps*L),'upper':str(F(hi)+eps*L),'decimal_display':[float(F(lo)-eps*L),float(F(hi)+eps*L)]}
 cases={}
 for m in [2,4,6]:
  x=q['fixed_even_cases'][str(m)];T=profile(x['T']);P=profile(x['P']);c={r:(T.get(r,0)-P.get(r,0))/F(18*(m-1)) for r in T.keys()|P.keys()};cases[m]=extend(c,x['perrail_margin']['lower'],x['perrail_margin']['upper'])
 assert F(cases[2]['upper'])<0 and F(cases[4]['upper'])<0 and F(cases[6]['lower'])>1 and F(cases[6]['upper'])<2
 N=profile(q['native_paid']);H=profile(q['helper_target']);T2=profile(q['paired_target']);P2=profile(q['paired_paid']);ranks=N.keys()|H.keys()|T2.keys()|P2.keys()|{1}
 c={r:N.get(r,0)-H.get(r,0)+(T2.get(r,0)-P2.get(r,0))/36-(1618 if r==1 else 0) for r in ranks};lim=extend(c,q['limiting_perrail_margin']['lower'],q['limiting_perrail_margin']['upper']);assert F(lim['lower'])>3 and F(lim['upper'])<4
 pairbase=b['at_t_199_over_200']['original_paired_margin'];pair=extend({r:T2.get(r,0)-P2.get(r,0) for r in ranks},pairbase['exact_lower'],pairbase['exact_upper']);assert F(pair['upper'])<0
 threshold=F(3112961,621875000);explicit=threshold+F(1,10**10);assert k0<F(50001,10**7)<explicit<k1
 out={'status':'PASS_UNIFORM_Q8_MOVEMENT_PRICE_INTERVAL','q8_receipt_sha256':sha(raw),'baseline_budget_sha256':sha(rawb),'kappa_interval':[str(k0),str(k1)],'t_interval':[str(1-k1),str(1-k0)],'epsilon_width':str(eps),'log_bound':'log r < (7/10)*ceil(log2 r), r>1; exp(7/10)>2 by positive degree4 Taylor sum.','derivative_bound':'For 0<=k<=1, |d/dk sum c_r r^(1-k)| <= (7/10)sum |c_r|r ceil(log2 r).','uniform_even_cases':cases,'uniform_limiting_margin':lim,'uniform_original_paired_moment':pair,'first_profitable_even_m_throughout_interval':6,'m6_extra_unit_moves_affordable_throughout_interval':1,'all_finite_m_at_most_extra_unit_moves':3,'one_stage_covered_threshold':str(threshold),'explicit_price_above_one_stage_threshold':str(explicit),'two_stage_price':str(F(50001,10**7)),'interval_upper_above_one_stage_threshold':str(k1-threshold),'scope':'Analytic uniform movement-profile lemma. Test exponent is not an admitted covered saving; source, allwidth, compiler cover/tail losses, changed atom, ordinary bootstrap and complex supplier remain open. No new kappa.'}
 a.output.mkdir(parents=True,exist_ok=True);(a.output/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','kappa_interval','uniform_even_cases','uniform_limiting_margin','uniform_original_paired_moment']},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--q8',type=Path,required=True);p.add_argument('--budget',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
