#!/usr/bin/env python3
"""Source-derived exact fixed-m screen; every continuation remains conditional."""
import argparse,collections,gzip,hashlib,json,runpy
from fractions import Fraction as F
from pathlib import Path
PIN='6a88ca1fb962391190626539ce098517785a717c34ea0af61b533ea64821b1d1'
def main(a):
 if hashlib.sha256(a.moment_checker.read_bytes()).hexdigest()!=PIN:raise ValueError('rational moment checker pin')
 m=runpy.run_path(str(a.moment_checker));combine=m['combine'];moment=m['moment'];record=m['record'];w=json.loads(gzip.decompress(a.word.read_bytes()));fr=w['frames'];pending={};Q=collections.Counter()
 def d(c):return fr[str(c)]['dim']
 def flush(f):
  if f in pending:
   c,e=pending.pop(f);Q[abs(d(e)-d(c))]+=1
 for op in w['program']:
  kind,f=op[:2]
  if kind=='MOVE':
   _,f,c,e=op
   if f not in pending:pending[f]=(c,e)
   else:
    start,end=pending[f]
    if end!=c:raise ValueError('broken actual record route')
    if(d(e)-d(c))*(d(end)-d(start))>0:pending[f]=(start,e)
    else:flush(f);pending[f]=(c,e)
  else:
   flush(f)
   if kind=='ADD':flush(op[2])
 for f in list(pending):flush(f)
 if Q!={1:57,6:56,7:167,8:2}:raise ValueError(('actual profile',Q))
 raw=a.native.read_bytes()
 if hashlib.sha256(raw).hexdigest()!='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78':raise ValueError('native pin')
 native=json.loads(gzip.decompress(raw));nf=native['frames'];N=collections.Counter(abs(nf[str(o[2])]['dim']-nf[str(o[3])]['dim'])for o in native['program']if o[0]=='MOVE');H={2:1,4:25,6:1,8:410}
 P2=combine((36,N),(444,{1:1}),(444,{7*j:1 for j in range(1,9)}));T2=combine((36,H),(222,{127:1}),(444,{1+7*j:1 for j in range(1,10)}));M2=combine((1,T2),(-1,P2));B=combine((1,N),(-1,H),(F(1,36),M2));cases={}
 for future in(6,7):
  q=combine((1,Q),(future,{8:1}));lim=combine((1,B),(-1,q));fixed={};first=None
  for mult in range(2,66,2):
   margin=moment(combine((1,lim),(F(1,36*(mult-1)),M2)))
   if margin[0]>0 and first is None:first=mult
   if mult in(2,4,6,8,10,16,32,64):fixed[str(mult)]=record(margin)
  cases[str(future)]={'optimistic_full_profile':{str(k):str(v)for k,v in q.items()},'moment':record(moment(q)),'limiting_extra_moment_room':record(moment(lim)),'first_profitable_even_m_at_most64_before_decoder_extra_cost':first,'fixed_m_margins':fixed}
 if(cases['6']['first_profitable_even_m_at_most64_before_decoder_extra_cost'],cases['7']['first_profitable_even_m_at_most64_before_decoder_extra_cost'])!=(4,6):raise ValueError('finite-m signs')
 out={'status':'PASS_EXACT_CONDITIONAL_CANONICAL_PIVOT_CALLER_SCREEN','word_sha256':hashlib.sha256(a.word.read_bytes()).hexdigest(),'moment_checker_sha256':PIN,'t':'199/200','actual_partial_profile':dict(Q),'actual_partial_moment':record(moment(Q)),'limiting_allowance':record(moment(B)),'finite_m_correction_numerator':record(moment(combine((F(1,36),M2)))),'conditional_future_Hub_modes':cases,'retained_caller_formulas':{'P_m':'(m/2)P2 -18(m-1)N +18(m-1)Q','T_m':'(m/2)T2 -18(m-1)H','normalized_gap':'B_infinity - moment(Q) + moment(T2-P2)/(36(m-1))'},'ordinary_ownership':{'prefix_ADD':575,'prefix_INIT':117,'prefix_CLEAR':3,'prefix_owned_live':114,'prefix_peak':115,'complete_Q_if_appending':'ADD=575+A_cont; lifetimes=117+L_cont, including all continuation births and eventual114 retained retirements','minimum_six_separate_Hub_packet_lifetimes':6,'shared_ADD':'30789+(m-1)*(444+A_Q), retaining3 native SWAPs','shared_owned_lifetimes':'237+(m-1)*L_Q','shared_sequential_peak':'max(237,peak(Q))'},'retained_open_obligations':['Actual complete remaining decoder with every new route, stop, local acquisition, ordinary operation and ownership lifetime.','Additional histories/fitting beyond the simple C+e0 completion, whose natural support charge is220>194.','Source interface, compiler, strict supplier admission, complete ordinary BIT, compatible complex supplier, recursive accounting and foundational assumptions.'],'complete_source':False,'new_kappa':False}
 a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':out['status'],'six_future_moment':cases['6']['moment']['lower_decimal'],'six_future_limiting_room':cases['6']['limiting_extra_moment_room']['lower_decimal'],'first_even_m':{k:v['first_profitable_even_m_at_most64_before_decoder_extra_cost']for k,v in cases.items()}}))
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for n in('word','native','moment-checker','output'):p.add_argument('--'+n,type=Path,required=True)
 main(p.parse_args())
