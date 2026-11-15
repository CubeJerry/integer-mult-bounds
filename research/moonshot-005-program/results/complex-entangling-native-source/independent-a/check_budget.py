#!/usr/bin/env python3
"""Separate directed integer-root invoices for the exact complex source targets."""
from fractions import Fraction as F
from decimal import Decimal,localcontext
from pathlib import Path
import json
S=10**45

def iroot(n):
 lo=0;hi=1<<((n.bit_length()+199)//200)
 while hi-lo>1:
  m=(hi+lo)//2
  if m**200<=n:lo=m
  else:hi=m
 assert lo**200<=n<hi**200
 return lo
P={r:(F(iroot(r**199*S**200),S),F(iroot(r**199*S**200)+1,S))for r in [1,7,8,23,24,30,31]}
def linear(d):
 a=b=F(0)
 for r,c in d.items():
  u,v=P[r]
  if c<0:u,v=v,u
  a+=c*u;b+=c*v
 return a,b

def rec(x):
 with localcontext()as c:
  c.prec=65
  return {'lower':str(x[0]),'upper':str(x[1]),'decimal_lower':str(Decimal(x[0].numerator)/Decimal(x[0].denominator)),'decimal_upper':str(Decimal(x[1].numerator)/Decimal(x[1].denominator))}

def main():
 cases={'three_native_322':{24:1,23:2,1:-3,7:-6,8:-3},'three_native_333':{24:3,1:-3,7:-6,8:-3},'three_native_222_control':{23:3,1:-3,7:-6,8:-3},'four_native_333':{31:3,1:-4,7:-8,8:-4},'four_native_222_control':{30:3,1:-4,7:-8,8:-4}}
 vals={k:linear(v)for k,v in cases.items()}
 assert vals['three_native_322'][0]>0 and vals['three_native_333'][0]>0 and vals['four_native_333'][0]>0
 assert vals['three_native_222_control'][1]<0 and vals['four_native_222_control'][1]<0
 lo=F(561007339600891538672434298712,10**30);hi=F(561007339600891538672434298724,10**30)
 assert lo<=vals['three_native_322'][0]<=vals['three_native_322'][1]<=hi
 out={'status':'PASS_INDEPENDENT_COMPLEX_SOURCE_GAUSSIAN_INVOICES','power':'199/200','integer_root_scale':str(S),'target_minus_complete_Gaussian_price':{k:rec(v)for k,v in vals.items()},'scope':'All rank7 idles included. Positive Gaussian surplus is only an optimistic target; no actual target caller or ordinary/compiler/precision/recursive supplier admission is inferred.'}
 p=Path(__file__).parent/'output';p.mkdir(exist_ok=True);(p/'BUDGET-RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'])
if __name__=='__main__':main()
