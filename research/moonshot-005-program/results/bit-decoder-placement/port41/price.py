#!/usr/bin/env python3
from fractions import Fraction as F
from functools import lru_cache
from collections import Counter
from decimal import Decimal,localcontext,ROUND_FLOOR,ROUND_CEILING
from pathlib import Path
import json
SCALE=1<<160
def need(ok,msg):
 if not ok:raise AssertionError(msg)
def iroot(n, k):
    x = 1 << ((n.bit_length() + k - 1) // k)
    while True:
        y = ((k - 1) * x + n // pow(x, k - 1)) // k
        if y >= x:
            break
        x = y
    while pow(x, k) > n:
        x -= 1
    while pow(x + 1, k) <= n:
        x += 1
    return x

@lru_cache(None)
def power(rank):
    integer = pow(rank, 199) * pow(SCALE, 200)
    low = iroot(integer, 200)
    need(pow(low, 200) <= integer < pow(low + 1, 200), "directed power invariant")
    return F(low, SCALE), F(low if pow(low, 200) == integer else low + 1, SCALE)

def add(*terms):
    result = Counter()
    for coefficient, profile in terms:
        for rank, count in profile.items():
            result[rank] += coefficient * count
    return dict(result)

def moment(profile):
    low = high = F(0)
    for rank, coefficient in profile.items():
        left, right = power(rank)
        low += coefficient * (left if coefficient >= 0 else right)
        high += coefficient * (right if coefficient >= 0 else left)
    return low, high

def encode(interval):
    left, right = interval
    with localcontext() as ctx:
        ctx.prec = 60
        ctx.rounding = ROUND_FLOOR
        a = str(Decimal(left.numerator) / Decimal(left.denominator))
        ctx.rounding = ROUND_CEILING
        b = str(Decimal(right.numerator) / Decimal(right.denominator))
    return {"lower": a, "upper": b,
            "lower_fraction": str(left), "upper_fraction": str(right)}

def invoice(profile):
    N = {1: 1386, 2: 1253, 3: 62, 4: 47, 5: 9, 6: 104, 7: 10}
    H = {2: 1, 4: 25, 6: 1, 8: 410}
    P2 = add((36, N), (444, {1: 1}), (444, {7*j: 1 for j in range(1, 9)}))
    T2 = add((36, H), (222, {127: 1}), (444, {1+7*j: 1 for j in range(1, 10)}))
    allowance = add((1, N), (-1, H), (F(1, 36), T2), (F(-1, 36), P2))
    displayed = {127: F(37, 6), 64: F(74, 6), 1: F(-74, 6)}
    for j in range(1, 9):
        displayed[1+7*j] = displayed.get(1+7*j, F(0)) + F(74, 6)
        displayed[7*j] = displayed.get(7*j, F(0)) - F(74, 6)
    need({r: v for r, v in allowance.items() if v} == displayed, "caller allowance cancellation")
    rows = []
    first_positive = None
    for m in range(2, 202, 2):
        paid = add((F(m, 2), P2), (-18*(m-1), N), (18*(m-1), profile))
        target = add((F(m, 2), T2), (-18*(m-1), H))
        margin = moment(add((1, target), (-1, paid)))
        if first_positive is None and margin[0] > 0:
            first_positive = m
        if m in (2, 4, 6, 8, 10, 12):
            rows.append({"m": m, "target_minus_paid": encode(margin), "strictly_positive": margin[0] > 0})
    return {"exponent": "199/200", "directed_method": "binary fixed-point scale2^160 and exact integer200th root",
            "moment": encode(moment(profile)), "limiting_allowance": encode(moment(allowance)),
            "limiting_room": encode(moment(add((1, allowance), (-1, profile)))),
            "finite_even_m_checks": rows, "first_positive_even_m_in_2_to_200": first_positive,
            "scope": "movement-only necessary interface; all remaining supplier costs retained", "new_complete_kappa": False}

if __name__ == '__main__':
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 result=json.loads((a.out/'RESULT.json').read_text());profile={int(r):F(n)for r,n in result['movement_profile'].items()}
 out=invoice(profile);out['physical_copies']=1;out['physical_profile']={str(k):int(v)for k,v in profile.items()};out['targets']=result['targets'];out['operation_counts']=result['counts'];out['predecessor_pricer']='bit-joint-a2-mds-source/three-author/price.py';out['scope']='Every movement in one actually executed partial native source. Complete all111 receiver endpoints and all ordinary/compiler/precision/supplier contracts remain open; finite m comparison is hypothetical only.'
 (a.out/'PRICE.json').write_text(json.dumps(out,indent=2)+'\n');print('Q',out['moment']['lower'],'room',out['limiting_room']['lower'],'first even m',out['first_positive_even_m_in_2_to_200'])
