#!/usr/bin/env python3
"""Exact optimistic complete BIT budget for monotone arrivals and reversals."""
from fractions import Fraction as F
from decimal import Decimal,localcontext
from pathlib import Path
import argparse,hashlib,json
PIN='92ab5d5cc08933f46c7eedb195f8d5f4e68a27dc189e6f8594876f70846db152'
def power(r):
    den=1<<160;target=r**199*den**200;lo=0;hi=r*den+1
    while hi-lo>1:
        mid=(lo+hi)//2
        if mid**200<=target:lo=mid
        else:hi=mid
    assert lo**200<=target<(lo+1)**200
    return F(lo,den),F(lo if lo**200==target else lo+1,den)
def add(*pairs):return sum((p[0] for p in pairs),F()),sum((p[1] for p in pairs),F())
def mul(k,p):return (k*p[0],k*p[1]) if k>=0 else (k*p[1],k*p[0])
def sub(a,b):return add(a,mul(-1,b))
def record(p):
    with localcontext() as c:
        c.prec=65;d=[str(Decimal(x.numerator)/Decimal(x.denominator)) for x in p]
    return {'lower':str(p[0]),'upper':str(p[1]),'display':d}
def main(a):
    p=a.repo/'research/moonshot-005-program/results/bit-rank-nine-shared-interface/BUDGET.json'
    raw=p.read_bytes();assert hashlib.sha256(raw).hexdigest()==PIN
    z=json.loads(raw)['at_t_199_over_200']['limiting_Q_allowance']
    ceiling=F(z['exact_lower']),F(z['exact_upper'])
    pp={r:power(r) for r in range(1,9)};per_rank=mul(F(1,8),pp[8])
    assert all(pp[r][0]>r*per_rank[1] for r in range(1,8))
    generic=add(mul(222,pp[7]),mul(9,pp[8]))
    clean=add((F(289),F(289)),mul(244,pp[2]),mul(111,pp[7]),mul(9,pp[8]))
    def bound(base,expected):
        n=0
        while add(base,mul(2*(n+1),per_rank))[0]<=ceiling[1]:n+=1
        assert n==expected
        admitted=add(base,mul(2*n,per_rank));excluded=add(base,mul(2*(n+1),per_rank))
        assert admitted[1]<ceiling[0] and excluded[0]>ceiling[1]
        return {'necessary_integer_upper':n,'optimistic_price_at_upper':record(admitted),'first_excluded_price':record(excluded),'first_excluded_deficit':record(sub(excluded,ceiling))}
    all_records=mul(1626,per_rank)
    out={'status':'PASS_EXACT_OPTIMISTIC_COMPLETE_BIT_REVERSAL_AND_ARRIVAL_BUDGETS','caller_sha256':PIN,'t':'199/200','caller_limit':record(ceiling),'ranks':'integer1..8','per_movement_rank_lower_factor':record(per_rank),'minimum_direct_original_profile':{7:222,8:9},'minimum_direct_original_cost':record(generic),'optimistic_remaining_moment':record(sub(ceiling,generic)),
         'fixed_clean_X_minimum_Y_packet_upward_rank':bound(clean,2),
         'arbitrary_monotone_XY_packet_upward_rank':bound(generic,5),
         'all_original_records_total_reverse_rank':bound(all_records,6),
         'all_records_dimension_telescoping':'111 X line1->Hub8 plus111 Y0->facet7 plus9 packetsHub8->0: total rank>=1626+2R, where R=downward X/Y rank + upward packet rank.',
         'optional_102_extra_local_arrivals_deficit':record(sub(add(generic,(F(102),F(102))),ceiling)),
         'scope':'Necessary optimistic movement budgets, not constructions. All fixed even m have stricter ceilings. Nine persistent packet routes and prescribed whole-V endpoints retained; extra lifetimes/movements need separate accounting. The102-arrival premise is a separate reviewed-or-pending theorem, not proved by this arithmetic.'}
    assert F(out['optional_102_extra_local_arrivals_deficit']['lower'])>F('90.45799327294747')
    a.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'fixed_clean_U':2,'monotone_XY_U':5,'all_records_R':6,'extra102_deficit':out['optional_102_extra_local_arrivals_deficit']['display']}))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
