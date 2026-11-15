#!/usr/bin/env python3
"""Directed integer-root intervals for fully replicated finite caller invoices."""
from fractions import Fraction as F
from pathlib import Path
import json
D=10**50

def iroot(n,k):
 lo=0;hi=1<<((n.bit_length()+k-1)//k)
 while lo+1<hi:
  m=(lo+hi)//2
  if m**k<=n:lo=m
  else:hi=m
 return lo
bounds={r:(F(iroot(r**199*D**200,200),D),F(iroot(r**199*D**200,200)+1,D))for r in range(1,128)}
def add(a,b):return(a[0]+b[0],a[1]+b[1])
def scale(x,c):return(c*x[0],c*x[1])if c>=0 else(c*x[1],c*x[0])
def linear(d):
 z=(F(0),F(0))
 for r,c in d.items():z=add(z,scale(bounds[r],F(c)))
 return z
def combine(*terms):
 out={}
 for d,c in terms:
  for r,v in d.items():out[r]=out.get(r,F(0))+F(c)*v
 return{k:v for k,v in out.items()if v}
def dec(x):
 sign='-'if x<0 else'';x=abs(x);a=x.numerator*10**35//x.denominator;return sign+str(a//10**35)+'.'+str(a%10**35).zfill(35)
def rec(x):return{'lower_rational':str(x[0]),'upper_rational':str(x[1]),'lower_decimal':dec(x[0]),'upper_decimal':dec(x[1])}
N={1:1386,2:1253,3:62,4:47,5:9,6:104,7:10};H={2:1,4:25,6:1,8:410};P2=combine((N,36),({1:444},1),({7*j:444 for j in range(1,9)},1));T2=combine((H,36),({127:222},1),({1+7*j:444 for j in range(1,10)},1));Q0={1:183,2:12,3:119,4:71,7:110};delta=combine((T2,1),(P2,-1));Binf=combine((N,1),(H,-1),(delta,F(1,36)))
cases=[]
for extra in range(6):
 # Two copies, extra separately owned Hub-ground rank8 banks, secondYchain percopy.
 fullQ=combine((Q0,2),({8:extra},1),({1:14,7:-2},1));Qnorm={r:c/2 for r,c in fullQ.items()};room=linear(combine((Binf,1),(Qnorm,-1)));slope=linear(combine((delta,F(1,2)),(N,18),(H,-18),(Qnorm,-18)));margins=[]
 for m in range(2,42,2):
  margin=linear(combine((delta,F(m,2)),(N,18*(m-1)),(H,-18*(m-1)),(Qnorm,-18*(m-1))))
  margins.append({'m':m,'normalized_margin':rec(margin),'two_copy_margin':rec(scale(margin,2))})
 first=next((x['m']for x in margins if F(x['normalized_margin']['lower_rational'])>0),None)
 cases.append({'principal_physical_banks':16+extra,'normalized_principals':str(F(16+extra,2)),'full_movement_profile':{str(r):int(c)for r,c in fullQ.items()},'normalized_Q':rec(linear(Qnorm)),'limiting_normalized_room':rec(room),'finite_even_m_first_certified':first,'finite_margin_slope':rec(slope),'all_even_m_from_first_if_positive_slope':first is not None and slope[0]>0,'finite_samples':margins})
assert cases[3]['limiting_normalized_room']['lower_decimal'][0]!='-';assert F(cases[4]['limiting_normalized_room']['upper_rational'])<0
# Full duplication identity is coefficientwise, not a floating-point inference.
for m in [2,4,6,10]:
 pm=combine((P2,F(m,2)),(N,-18*(m-1)),(Q0,18*(m-1)))
 assert combine((pm,2))==combine((P2,m),(N,-36*(m-1)),(Q0,36*(m-1)))
out={'status':'PASS_EXACT_TWO_COPY_PRINCIPAL_BUDGET','target_exponent':'199/200','new_complete_kappa':False,'B_infinity':rec(linear(Binf)),'cases':cases,'scope':'Two complete caller copies, actual integer principal bank counts, all secondY movement paid; no complete decoder or supplier inferred.'};Path(__file__).with_name('RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'cases':[{'banks':x['principal_physical_banks'],'Q':x['normalized_Q']['lower_decimal'],'room':x['limiting_normalized_room']['lower_decimal'],'first_even_m':x['finite_even_m_first_certified']}for x in cases]}))
