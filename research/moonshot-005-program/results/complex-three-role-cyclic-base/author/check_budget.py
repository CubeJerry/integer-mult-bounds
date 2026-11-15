#!/usr/bin/env python3
"""Integer-power rational enclosures for exact prospective movement invoices."""
import json
from pathlib import Path
S=10**30

def interval(r,p,q):
 if r==1:return S,S
 N=pow(r,p)*pow(S,q);lo=S;hi=r*S
 while lo+1<hi:
  mid=(lo+hi)//2
  if pow(mid,q)<=N:lo=mid
  else:hi=mid
 return (lo,lo) if pow(lo,q)==N else (lo,hi)
def margin(heads,p,q):
 R=len(heads);target={21+h:heads.count(h) for h in set(heads)};price={1:3,7:3*(R-1),8:3}
 table={r:interval(r,p,q) for r in set(target)|set(price)}
 lo=sum(c*table[r][0] for r,c in target.items())-sum(c*table[r][1] for r,c in price.items())
 hi=sum(c*table[r][1] for r,c in target.items())-sum(c*table[r][0] for r,c in price.items())
 return {'exponent':f'{p}/{q}','heads':heads,'roles':R,'natives':3,'paid_rank7_idles':3*(R-2),'target':target,'price':price,'margin_numerators':[str(lo),str(hi)],'denominator':str(S),'strict_positive':lo>0,'one_extra_rank1_query_fails':hi<S,'root_enclosures':{str(r):[str(x) for x in b] for r,b in table.items()}}
def main():
 rows=[margin(h,p,q) for p,q in [(199,200),(99,100)] for h in [(3,3,1),(3,2,2),(2,2,2),(3,2,2,0),(3,3,1,1)]]
 assert all(r['strict_positive'] for r in rows if len(r['heads'])==3 and r['heads']!=(2,2,2))
 out={'status':'PASS_RIGOROUS_PROSPECTIVE_THREE_NATIVE_MOVEMENT_BUDGETS','scale':str(S),'cases':rows,'scope':'Necessary optimistic movement arithmetic only. No caller, ordinary/precision/compiler/ownership bill, uniform supplier or new kappa follows.'};Path(__file__).with_name('BUDGET-RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'three_role_intervals':[r for r in rows if r['roles']==3]}))
if __name__=='__main__':main()
