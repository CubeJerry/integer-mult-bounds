#!/usr/bin/env python3
"""Exact retained-nine plus fresh-return budget gate for the clean BIT source."""
import argparse,hashlib,json
from decimal import Decimal,localcontext
from fractions import Fraction as F
from pathlib import Path
BUDGET_PIN='92ab5d5cc08933f46c7eedb195f8d5f4e68a27dc189e6f8594876f70846db152'
def need(c,m):
 if not c:raise ValueError(m)
def power(r):
 den=1<<144;target=r**199*den**200;lo,hi=0,r*den+1
 while hi-lo>1:
  mid=(lo+hi)//2
  if mid**200<=target:lo=mid
  else:hi=mid
 need(lo**200<=target<(lo+1)**200,'Directed root interval')
 return F(lo,den),F(lo if lo**200==target else lo+1,den)
def price(profile):
 lo=hi=F(0)
 for r,n in profile.items():
  a,b=power(r);lo+=n*a;hi+=n*b
 return lo,hi
def rec(pair):
 with localcontext() as c:
  c.prec=65
  decimals=[str(Decimal(x.numerator)/Decimal(x.denominator)) for x in pair]
 return {'lower':str(pair[0]),'upper':str(pair[1]),'decimals_for_display':decimals}
def main(a):
 path=a.repo/'research/moonshot-005-program/results/bit-rank-nine-shared-interface/BUDGET.json';raw=path.read_bytes();need(hashlib.sha256(raw).hexdigest()==BUDGET_PIN,'Complete caller budget source')
 prior=json.loads(raw)['at_t_199_over_200']['limiting_Q_allowance'];limit=(F(prior['exact_lower']),F(prior['exact_upper']))
 paths=json.loads(a.paths.read_text());need(paths['status']=='PASS_INDEPENDENT_SOURCE_AND_DOMINATED_UNION_PATH_REVIEW','Independent path receipt')
 need(paths['minimum_exception_ports_needed_even_for_one_output']==12,'Exact extra-port lower bound')
 caps={int(k):v for k,v in paths['maximum_source_history_support_by_chart_dimension'].items()}
 need(caps=={1:1,2:2,4:9,6:12,7:13,8:111},'Exact source chart support capacities')
 fixed={1:289,2:244,7:111,8:9};base=price(fixed);room=(limit[0]-base[1],limit[1]-base[0]);six=power(6)
 need(0<room[0] and room[1]<six[0],'Budget excludes total fresh birth dimension6')
 profiles=[]
 for ones in range(6):
  for twos in range(3):
   for fours in range(2):
    mass=ones+2*twos+4*fours
    if mass<=5:profiles.append({'counts':{1:ones,2:twos,4:fours},'mass':mass,'support_union_upper':ones+2*twos+9*fours})
 upper=max(x['support_union_upper'] for x in profiles);need(upper==10 and upper<12,'Every affordable fresh-return support union fails')
 need(any(x['support_union_upper']==10 and x['mass']==5 for x in profiles),'Tight relaxed profile4+1 retained')
 result={'status':'PASS_ALL_FIXED_M_RETAINED_NINE_FRESH_RETURN_CACHE_BUDGET_GATE','caller_budget_sha256':BUDGET_PIN,
  'independent_paths_sha256':hashlib.sha256(a.paths.read_bytes()).hexdigest(),'t':'199/200','fixed_profile_lower_bound':fixed,
  'limiting_Q_allowance':rec(limit),'fixed_X_minimum_Y_and_nine_Hub_packets':rec(base),'maximum_additional_allowance':rec(room),'six_power_lower_gate':rec(six),
  'maximum_affordable_total_fresh_birth_dimension':5,'all_integer_birth_profiles':profiles,'maximum_additional_input_support_union':10,
  'minimum_input_ports_needed_outside_last_partner_and_suffix':12,'contradiction_gap':2,
  'scope':'Retains nine canonical/gauge-equivalent all-Hub packets, the exact clean X source, monotone public Y coding and stationary caches. Additional pure-X packets are formed once from one source-history chart and delivered to0 without acquiring new information en route. No moving multi-chart assembly, changed source, alternative higher-rank packet code or complete-supplier impossibility is claimed.'}
 a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['status','maximum_affordable_total_fresh_birth_dimension','maximum_additional_input_support_union','minimum_input_ports_needed_outside_last_partner_and_suffix','contradiction_gap']}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--paths',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
