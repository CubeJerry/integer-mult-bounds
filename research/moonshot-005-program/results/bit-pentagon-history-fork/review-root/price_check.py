#!/usr/bin/env python3
"""Independent integer enclosures of the fork's local movement improvement."""
import argparse,json
from fractions import Fraction as F
from pathlib import Path
S=10**12
def power(n):
    lo,hi=0,n*S;target=n**199*S**200
    while hi-lo>1:
        mid=(lo+hi)//2
        if mid**200<=target:lo=mid
        else:hi=mid
    if not lo**200<=target<=hi**200:raise ValueError('root enclosure')
    return F(lo,S),F(hi,S)
def linear(profile):
    lo=hi=F(0)
    for r,c in profile.items():
        a,b=power(r);lo+=c*(a if c>0 else b);hi+=c*(b if c>0 else a)
    return lo,hi
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    cost=linear({1:9,2:2,5:2,6:7,7:215});gain=linear({1:-9,2:-2,5:-2,6:-7,7:7,8:3})
    if gain[0]<=0:raise ValueError('strict comparison')
    d={'status':'PASS_INDEPENDENT_FORK_MOVEMENT_COMPARISON','power':'199/200','actual_partial_moment_interval':list(map(str,cost)),'saving_against_three_isolated_full_routes_interval':list(map(str,gain)),'approximate_saving':float(sum(gain)/2),'scope':'Same original endpoints and at least three full monotone routes only; seven real owners and all remaining target duties remain','no_new_kappa':True}
    a.output.write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(d))
if __name__=='__main__':main()
