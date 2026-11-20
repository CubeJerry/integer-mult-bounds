#!/usr/bin/env python3
"""Transplant the two tighter losses to both separate m=870 mixed-cut controls."""
import argparse,json,sys
from fractions import Fraction as Q
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent));from price import D,power,need
def run(out):
    unit=10**11;k=Q('0.0050000005');t=1-k;costs={}
    for name,v,c,b,th,poly in [('short',88,31,32,Q(109,110),234),('low_log',194,24,38,Q(7,8),36)]:
        an,ad=th.numerator,th.denominator;need(c**ad<b**an and 2*c**(v*ad)<=127**(v*an),'shifted-log shrink')
        z=power(127,D('.0050000005')*v);need(th**poly<Q(t)/Q(z[1])and Q(z[1])<2**poly,'true uniform power')
        def works(n):return (n*unit+1)**poly<2**n
        lo,hi=1,1
        while not works(hi):hi*=2
        while hi-lo>1:
            mid=(lo+hi)//2
            if works(mid):hi=mid
            else:lo=mid
        need(works(hi)and not works(hi-1),'minimal grid');need(2**45>256*unit and 1+Q(1,2*unit)<=2**hi,'delayed-cover guards')
        costs[name]={'v':v,'polylogarithmic_power':poly,'log2_carrier':hi*unit}
    covered=k-Q(2,unit);old=Q(12039,3125000);prices=[]
    for _ in range(4):
        env=Q(249,250)*covered+old/250;tick=(env*10**15).__floor__()-1;old=Q(tick,10**15);need(old<env,'strict ramp');prices.append(f'0.{tick:015d}')
    ans={'raw':'0.0050000005','uniform':'0.00500000049','covered':'0.00500000048','conditional_ordinary_stages':prices,'cutoff_witnesses':costs,'loss_each':'1/100000000000','scope':'conditional complete physical tariff and the same admitted stock/cover interfaces'};out.mkdir(exist_ok=True,parents=True);(out/'LOSS.json').write_text(json.dumps(ans,indent=2)+'\n');print(ans)
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,required=True);run(p.parse_args().out)
