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

if __name__=='__main__':
 physical={1:60,2:432,5:432,6:36,7:444,8:12}
 r=invoice({k:F(v,4)for k,v in physical.items()});r['physical_binary_copies']=4;r['physical_profile']=physical;r['normalization']='Every native body and caller term scales by4 together with the4 actual productive binary copies; no wide-record discount.';r['scope']='Complete movement invoice of a four-copy partial source with canonical36 actually at ground and three native receivers (3,76,80) completed in each copy. All40owners,5012ADDs,1416MOVEs and40dirtyCLEARs are explicit. Full decoder and other supplier obligations remain.'
 (Path(__file__).parent/'PRICE.json').write_text(json.dumps(r,indent=2)+'\n');print(r['moment']['lower'],r['limiting_room']['lower'],r['first_positive_even_m_in_2_to_200'])
