#!/usr/bin/env python3
"""Independent certified interval invoice for the literal twelve-output word."""
import argparse, hashlib, json
from collections import Counter
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

SCALE = 10**30

def power(r):
    with localcontext() as c:
        c.prec = 90
        a = int(Decimal(r)**(Decimal(199)/200)*SCALE)
    n = r**199*SCALE**200
    while a**200 > n:
        a -= 1
    while (a+1)**200 <= n:
        a += 1
    assert a**200 <= n < (a+1)**200
    return Fraction(a, SCALE), Fraction(a+(a**200 != n), SCALE)

def interval(profile):
    lo = hi = Fraction(0)
    for r, v in profile.items():
        a, b = power(r)
        lo += v*(a if v >= 0 else b)
        hi += v*(b if v >= 0 else a)
    return lo, hi

def report(bound):
    with localcontext() as c:
        c.prec = 45
        return {"lower":str(Decimal(bound[0].numerator)/bound[0].denominator),
                "upper":str(Decimal(bound[1].numerator)/bound[1].denominator),
                "exact_bounds":[str(x) for x in bound]}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--review',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args()
    receipt=json.loads(a.review.read_text())
    actual={int(k):v for k,v in receipt['positive']['movement'].items()}
    control={7:222,8:8,1:12}
    diff=Counter(control)
    for r,v in actual.items():diff[r]-=v
    budget=Counter({127:Fraction(37,6),64:Fraction(74,6),1:Fraction(-74,6)})
    for j in range(1,9):
        budget[1+7*j]+=Fraction(74,6)
        budget[7*j]-=Fraction(74,6)
    room=budget.copy()
    for r,v in actual.items():room[r]-=v
    assert interval(diff)[0]>1
    assert interval(room)[0]>8
    out={"status":"PASS_EXACT_SAME_INTERFACE_PRICE",
         "review_sha256":hashlib.sha256(a.review.read_bytes()).hexdigest(),
         "moment_exponent":"199/200",
         "literal_word_profile":actual,
         "literal_word_price":report(interval(actual)),
         "same_S8_twelve_point_control":report(interval(control)),
         "control_minus_literal_word":report(interval(diff)),
         "retained_limiting_budget":report(interval(budget)),
         "limiting_room":report(interval(room)),
         "scope":"Partial12-output invoice only;99 outputs and full supplier admission remain open"}
    a.out.mkdir(parents=True,exist_ok=True)
    (a.out/'PRICE.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
