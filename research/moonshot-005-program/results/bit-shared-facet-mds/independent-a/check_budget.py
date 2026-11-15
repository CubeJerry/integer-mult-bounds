#!/usr/bin/env python3
"""Independent decimal-denominator interval arithmetic for the conditional envelope."""
import json,hashlib,argparse
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal,localcontext
S=10**40

def root(n):
 lo=0;hi=1<<((n.bit_length()+199)//200)
 while hi-lo>1:
  m=(hi+lo)//2
  if m**200<=n:lo=m
  else:hi=m
 assert lo**200<=n<hi**200
 return lo
P={r:(F(root(r**199*S**200),S),F(root(r**199*S**200)+1,S))for r in range(1,128)}
def scale(c,x):return(c*x[0],c*x[1])if c>=0 else(c*x[1],c*x[0])
def add(*xs):return tuple(sum(x[k]for x in xs)for k in (0,1))
def lin(d):return add(*[scale(F(c),P[r])for r,c in d.items()])
def rec(x):
 with localcontext()as c:
  c.prec=60
  return {'lower_fraction':str(x[0]),'upper_fraction':str(x[1]),'lower_decimal':str(Decimal(x[0].numerator)/Decimal(x[0].denominator)),'upper_decimal':str(Decimal(x[1].numerator)/Decimal(x[1].denominator))}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,required=True);ap.add_argument('--out',type=Path,default=Path(__file__).parent/'output');a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True);x=json.loads((a.source/'OPTIMISTIC-BUDGET.json').read_text())
 N=lin({1:1386,2:1253,3:62,4:47,5:9,6:104,7:10});H=lin({2:1,4:25,6:1,8:410});p2=add(scale(36,N),lin({1:444,**{7*j:444 for j in range(1,9)}}));t2=add(scale(36,H),lin({127:222,**{1+7*j:444 for j in range(1,10)}}));diff=add(t2,scale(-1,p2));allow=add(N,scale(-1,H),scale(F(1,36),diff));q=lin({1:F(555,2),2:F(111,4),5:111,6:111,8:9});room=add(allow,scale(-1,q))
 for ours,key in [(q,'moment'),(allow,'limiting_allowance'),(room,'limiting_room')]:
  z=x[key];assert ours[0]<=F(z['upper_fraction'])and F(z['lower_fraction'])<=ours[1]
 m2=add(scale(18,room),scale(F(1,2),diff));m4=add(scale(54,room),scale(F(1,2),diff));assert m2[1]<0<m4[0]and room[0]>0
 full={1:22200,2:2220,5:8880,6:8880,8:720};assert {r:F(v,80)for r,v in full.items()}=={1:F(555,2),2:F(111,4),5:F(111),6:F(111),8:F(9)}
 local=scale(F(1,4),lin({1:12,2:228,5:232,6:4,7:652}));complete=add(local,P[1]);baseline=lin({7:222})
 out={'status':'PASS_INDEPENDENT_CONDITIONAL_ENVELOPE_ARITHMETIC','author_sha256':hashlib.sha256((a.source/'OPTIMISTIC-BUDGET.json').read_bytes()).hexdigest(),'independent_decimal_scale':str(S),'Q_opt':rec(q),'room':rec(room),'m2':rec(m2),'m4':rec(m4),'all_even_m_at_least4_positive_by_positive_slope':True,'literal_four_copy_local_moment_per_copy':rec(local),'literal_four_copy_completed_control_moment_per_copy':rec(complete),'literal_local_premium_over_direct_all_original_ascents':rec(add(local,scale(-1,baseline))),'scope':'Only conditional allocation arithmetic; simultaneous acquisition and canonical chronology are not established and the strict one-hop global model has a separate obstruction under review.'}
 (a.out/'BUDGET-RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status']);print('Q local',out['literal_four_copy_local_moment_per_copy']['lower_decimal'])
if __name__=='__main__':main()
