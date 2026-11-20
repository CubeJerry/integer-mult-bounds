#!/usr/bin/env python3
"""Exact invoice ceilings and native return gates; no new complete kappa.

All elementary powers are bounded with integer square roots, independently
of the predecessor price engines.  See PROOF.md for the quantified arguments
that extend the finite sign checks to every caller length and larger saving.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
from functools import cache
from hashlib import sha256
from math import isqrt
from pathlib import Path
import gzip
import json

HERE = Path(__file__).resolve().parent
RESULTS = HERE.parent
GRID = 1 << 384
BITS = 160


def require(condition, label):
    if not condition:
        raise ValueError(label)


def ceil(x):
    return -((-x.numerator) // x.denominator)


def scale(a, c):
    c = F(c)
    return (c*a[0], c*a[1]) if c >= 0 else (c*a[1], c*a[0])


def plus(*parts):
    return sum((p[0] for p in parts), F()), sum((p[1] for p in parts), F())


def product(a, b):
    vals = [x*y for x in a for y in b]
    return min(vals), max(vals)


def quotient(a, b):
    require(b[0] > 0, 'positive denominator')
    return product(a, (1/b[1], 1/b[0]))


@cache
def power(x, exponent):
    x, exponent = int(x), F(exponent)
    require(x >= 1 and 0 <= exponent <= 1, 'power domain')
    if exponent == 0:
        return F(1), F(1)
    if exponent == 1:
        return F(x), F(x)
    lo = hi = x * GRID
    zlo = zhi = GRID
    remainder = exponent
    for _ in range(BITS):
        root_lo = isqrt(lo*GRID)
        root_hi = isqrt(hi*GRID)
        lo, hi = root_lo, root_hi + (root_hi*root_hi != hi*GRID)
        digit, remainder = divmod(2*remainder, 1)
        if digit:
            zlo, zhi = zlo*lo//GRID, -(-zhi*hi//GRID)
        if not remainder:
            break
    if remainder:
        zhi = -(-zhi*hi//GRID)
    return F(zlo, GRID), F(zhi, GRID)


def profile(*terms):
    out = Counter()
    for c, hist in terms:
        for r, n in hist.items():
            out[int(r)] += F(c)*F(n)
    return {r:n for r,n in out.items() if n}


def moment(hist, exponent):
    return plus(*(scale(power(r, exponent), n) for r,n in hist.items()))


def show(interval, digits=15):
    q = 10**digits
    def fmt(v):
        sign = '-' if v < 0 else ''
        i,j = divmod(abs(v), q)
        return f'{sign}{i}.{j:0{digits}d}'
    return [fmt((interval[0]*q).__floor__()), fmt(ceil(interval[1]*q))]


def read_sources():
    entries = json.loads((HERE/'SOURCES.json').read_text())['files']
    for name, digest in entries.items():
        require(sha256((RESULTS/name).read_bytes()).hexdigest() == digest,
                'source pin '+name)
    return entries


def paired_wrapper(a):
    require(isinstance(a, int) and a >= 1, 'positive integer arm count')
    d = Counter({14*a+1:2, 1:-4})
    for j in range(1,a+1):
        d[7*j+1] += 4
    for j in range(1,a):
        d[7*j] -= 4
    return d


def arm_difference(a):
    return profile((a,paired_wrapper(a+1)),(-a-1,paired_wrapper(a)))


def optimal_arm(k):
    a = 1
    while moment(arm_difference(a),1-k)[0] > 0:
        a += 1
        require(a < 100, 'bounded sign-location search')
    require(moment(arm_difference(a),1-k)[1] < 0, 'strict upper arm sign')
    if a > 1:
        require(moment(arm_difference(a-1),1-k)[0] > 0,
                'strict lower arm sign')
    return a


def bit_ceiling():
    source = json.loads((RESULTS/'bit-covariant-rebalanced-cutoffs/grade14/sources/BIT.json').read_text())
    native = source['native']
    paid = {int(k):v for k,v in native['native_paid'].items()}
    targets = {int(k):v for k,v in native['native_targets'].items()}
    require(paid == {1:1376,2:1281,3:54,4:44,5:17,6:102}, 'current binary paid source')
    require(targets == {1:8,2:9,4:43,5:8,6:1,8:389}, 'current binary targets')
    delta = profile((1,targets),(-1,paid))
    require(delta == {1:F(-1368),2:F(-1272),3:F(-54),4:F(-1),5:F(-9),6:F(-101),8:F(389)},
            'native signed profile for normalized monotonicity proof')
    def gap(a,k):
        return moment(profile((4*a,delta),(111,paired_wrapper(a))),1-k)
    explicit = profile((36,delta),(111,paired_wrapper(9)))
    receipt = profile((1,native['targets']),(-1,native['paid']))
    require(explicit == receipt, 'arm-nine source census equality')
    lo,hi = F('.003879928046154'),F('.003879928046155')
    require(gap(9,lo)[0] > 0 > gap(9,hi)[1], 'binary raw crossing signs')
    require(optimal_arm(hi) == 9, 'global arm-nine optimizer at upper endpoint')
    tests = {}
    for literal in ['.004','.0043','.0045','.005']:
        k=F(literal);a=optimal_arm(k)
        per_native=scale(gap(a,k),F(1,4*a))
        require(per_native[1] < 0, 'all-arm source deficit '+literal)
        tests[literal]={'optimal_arms':a,'complete_native_calls':4*a,
                        'maximum_signed_gap_per_native':show(per_native),
                        'required_net_source_gain_per_native':show(scale(per_native,-1))}
    # Price-level mutation control: an alleged free five-unit native saving
    # changes the answer at .0043, so it must not be hidden in a cutoff choice.
    a=optimal_arm(F('.0043'))
    changed=plus(gap(a,F('.0043')),(F(20*a),F(20*a)))
    require(changed[0]>0, 'genuine changed-profile positive control')
    return {'raw_crossing':[str(lo),str(hi)],
            'upper_endpoint_signed_gap':show(gap(9,hi),24),
            'arm_H8_at_upper':show(moment(arm_difference(8),1-hi)),
            'arm_H9_at_upper':show(moment(arm_difference(9),1-hi)),
            'trials':tests,
            'positive_control_five_fewer_unit_jobs_per_native':show(changed),
            'closure':'positive scalar sums, direct products, paid splitting and productive discarding under the unchanged moment contract'}


OLD_N = {1:1386,2:1253,3:62,4:47,5:9,6:104,7:10}
OLD_H = {2:1,4:25,6:1,8:410}
Q0 = {1:F(4451,8),2:F(7213,16),4:24}
LIM = profile((F(37,6),{127:1}),(F(37,3),{64:1,1:-1}),
              *[(F(37,3),{7*j+1:1,7*j:-1}) for j in range(1,9)])
OLD_GAP = profile((36,OLD_H),(-36,OLD_N),(111,paired_wrapper(9)))


def source_gap(k, ratio, multiplicity=None):
    d=profile((1,LIM),(-1,Q0),(-F(ratio),{8:1}))
    if multiplicity is not None:
        require(multiplicity >= 2 and multiplicity%2==0, 'fixed even multiplicity')
        d=profile((1,d),(F(1,36*(multiplicity-1)),OLD_GAP))
    return moment(d,1-k)


def return_cap(k, multiplicity=None):
    return quotient(source_gap(k,0,multiplicity),power(8,1-k))


def crossing(ratio, multiplicity=None):
    ticks=10**14
    lo,hi=0,10**12
    require(source_gap(F(lo,ticks),ratio,multiplicity)[0]>0,
            'positive left threshold endpoint')
    require(source_gap(F(hi,ticks),ratio,multiplicity)[1]<0,
            'negative right threshold endpoint')
    while hi-lo>1:
        mid=(lo+hi)//2
        sign=source_gap(F(mid,ticks),ratio,multiplicity)
        require(sign[0]>0 or sign[1]<0,'resolved strict bisection sign')
        if sign[0]>0:lo=mid
        else:hi=mid
    left,right=F(lo,ticks),F(hi,ticks)
    require(source_gap(left,ratio,multiplicity)[0]>0>source_gap(right,ratio,multiplicity)[1],
            'final crossing signs')
    return show((left,right),14)


def native_gates():
    arc=json.loads((RESULTS/'bit-native-directed-arc-gap/author/output/RESULT.json').read_text())
    require(arc['arbitrary_one_directed_deletion_floor']==37120,
            'punctured source arc floor')
    require(arc['b3840_by_actual_direction']['full_Clebsch']['deleted_arc_floor']==37303,
            'regular source arc floor')
    ratios={'any_missing_direction':F(29,3),
            'regular_missing_direction_continuum':F(68,7),
            'regular_missing_direction_bank3840':F(37303,3840),
            'ideal_nine_bank':F(9)}
    thresholds={name:{'infinite_m':crossing(q),'m870':crossing(q,870),'m2':crossing(q,2)}
                for name,q in ratios.items()}
    tables={}
    for literal in ['.00387992802601','.004','.0043','.0045','.005']:
        k=F(literal);entries={}
        require(moment(OLD_GAP,1-k)[1]<0, 'finite multiplicity is stricter in the displayed positive-target range')
        for m in [2,4,10,100,870,None]:
            cap=return_cap(k,m)
            scaled=scale(cap,3840)
            cap_int=ceil(scaled[0])-1
            require(cap_int+1>=scaled[1], 'unambiguous strict integer return cap')
            entries['infinite_m' if m is None else str(m)]={
                'strict_q_over_b_cap':show(cap),
                'strict_field_cap_b3840':show(scaled),
                'largest_integer_q_b3840':cap_int}
        tables[literal]=entries
    # The same-tariff allowance decreases with k on [0,1].  At k=0
    # OLD_GAP is positive, so the most generous *finite* choice is m=2,
    # not the limiting allowance.  Preserve that favorable finite credit.
    zero=return_cap(F(0))
    require(zero==(F(629,48),F(629,48)), 'zero-saving normalized maximum')
    finite_zero=return_cap(F(0),2)
    require(finite_zero==(F(55,3),F(55,3)) and moment(OLD_GAP,1)==(F(1506),F(1506)),
            'zero-saving all-finite-m maximum and baseline credit')
    projection=json.loads((RESULTS/'bit-native-irreducible-target-projection/author/output/RESULT.json').read_text())
    require(projection['partial_word_return_rank_lower_bound_fields']==52860,
            'projection source return floor')
    require(projection['binary_original_input_columns_in_scope']==2*111*480*5,
            'projection actual bank 480 and five binary extension lanes')
    require({int(r):F(n,480*5) for r,n in projection['invoice']['proper_MOVE_binary_counts'].items()}==Q0,
            'projection genuine non-return tariff equals balanced tariff')
    two_star=json.loads((RESULTS/'bit-global-two-star-target/author/output/RESULT.json').read_text())
    require(two_star['complete_original_field_columns_on_each_whole_block']==3840 and two_star['new_MOVE']==0,
            'two-star genuine bank and unchanged movement census')
    comparators={
        'two_star':{'bank':3840,'return_lower':182875,'normalized_lower':str(F(182875,3840))},
        'eight_field_row_projection':{'bank':480,'return_lower':52860,'normalized_lower':str(F(52860,480))}}
    for row in comparators.values():
        require(F(row['return_lower'],row['bank'])>finite_zero[1],
                'measured return exceeds even most generous zero-saving finite cap')
    require(F(52860,3840)<finite_zero[0]<F(52860,480),
            'wrong-bank negative control would give a false favorable zero-saving screen')
    require(tables['.0043']['infinite_m']['largest_integer_q_b3840']<37120,
            'every original directed donor still necessary at significant target')
    require(tables['.005']['870']['largest_integer_q_b3840']==34688,
            'recover retained moonshot finite cap')
    require(source_gap(F('.005'),F(34688,3840),870)[0]>0>
            source_gap(F('.005'),F(34689,3840),870)[1],
            'one additional return field changes the finite moonshot sign')
    require(source_gap(F('.0043'),F(9),2)[1]<0,
            'even the abstract nine-bank floor fails m2 at .0043')
    return {'strict_return_caps':tables,'missing_direction_kappa_ceilings':thresholds,
            'zero_saving_asymptotic_q_over_b':str(zero[0]),
            'zero_saving_maximum_over_all_finite_even_m_q_over_b':str(finite_zero[0]),
            'source_specific_comparators':comparators,
            'scope':'balanced non-return tariff Q0; same measured return; different source/word tariffs require fresh comparison'}


@cache
def logarithm(x):
    x=F(x);require(x>=1,'logarithm domain')
    exponent=x.numerator.bit_length()-x.denominator.bit_length()
    if x<F(2)**exponent:exponent-=1
    u=x/F(2)**exponent
    def unit_log(a):
        z=(a-1)/(a+1)
        acc=F();term=z
        for n in range(96):
            acc+=2*term/(2*n+1);term*=z*z
        tail=2*term/(193*(1-z*z))
        return acc,acc+tail
    return plus(scale(unit_log(F(2)),exponent),unit_log(u))


def complex_ceiling():
    raw=gzip.decompress((RESULTS/'complex-native-contested-restoration/author/sources/DOUBLE-APPLICATION.json.gz').read_bytes())
    z=json.loads(raw)['application']['invoice']
    signed=profile((1,z['targets']),(-1,z['paid']))
    lo,hi=F('.00388013644474'),F('.00388013644475')
    require(moment(signed,1-lo)[0]>0>moment(signed,1-hi)[1], 'rational raw crossing signs')
    # G'(k)=-sum d_r r^(1-k) log r.  Bound it above throughout
    # the whole retained outer interval 0 <= k <= 1/32.
    upper=F()
    for r,n in signed.items():
        w=product(power(r,F(31,32) if n>0 else F(1)),logarithm(r))
        upper+=scale(w,-n)[1]
    require(upper < -790000, 'strict complex derivative on whole retained outer domain')
    trials={literal:show(moment(signed,1-F(literal)))
            for literal in ['.004','.0043','.0045','.005']}
    return {'raw_crossing':[str(lo),str(hi)],'derivative_upper_on_0_to_1_over_32':show((upper,upper)),
            'complete_caller_signed_gaps':trials,
            'scope':'unchanged rational word and complete 48-call caller; independent of how much BIT improves'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',type=Path,required=True)
    args=p.parse_args()
    pins=read_sources()
    result={'status':'PASS_SIGNIFICANT_GAIN_SOURCE_GATES','new_complete_kappa':False,
            'source_baseline':'dc063045868f2072e0be1ef9f3fbb4ca3d43c8f2',
            'authenticated_inputs':len(pins),'binary_all_arm_ceiling':bit_ceiling(),
            'balanced_source_return_gates':native_gates(),'unchanged_complex_ceiling':complex_ceiling()}
    args.out.mkdir(parents=True,exist_ok=False)
    (args.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(result['status'])
    print('No new complete kappa; changed paid binary and complex sources are required.')


if __name__=='__main__':
    main()
