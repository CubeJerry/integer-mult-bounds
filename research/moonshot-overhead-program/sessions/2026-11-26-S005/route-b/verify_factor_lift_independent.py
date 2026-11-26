#!/usr/bin/env python3
"""Small independent integer-remainder controls for change of factor lift."""
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
from itertools import product
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
counts = Counter()

def rem(poly, divisor, modulus):
    out = list(poly)
    while len(out) >= len(divisor):
        offset, lead = len(out) - len(divisor), out[-1]
        for j, coefficient in enumerate(divisor):
            out[offset+j] -= lead * coefficient
        while out and out[-1] == 0:
            out.pop()
    return [(v % modulus) for v in out] + [0] * (len(divisor)-1-len(out))

def mul(a, b):
    out = [0] * max(0, len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return out

def deriv(a):
    return [i*a[i] for i in range(1,len(a))]

factors2 = ((0,1), (1,1), (1,1,1))
wrong_sign = omitted_representative = 0
for t in (1,2):
    Q = 2**t
    for g in factors2:
        d = len(g)-1
        for delta in product(range(Q), repeat=d):
            h = [(-v) % Q for v in rem(mul(delta,deriv(g)),g,Q)]
            gn = [g[i]+Q*h[i] for i in range(d)]+[1]
            for F in product(range(Q),repeat=4):
                old, new = rem(F,g,Q*Q), rem(F,gn,Q*Q)
                r = [v % Q for v in old]
                assert r == [v % Q for v in new]
                lhs = [v//Q for v in new]
                ko = [v//Q for v in old]
                df = rem(deriv(F),g,Q)
                dr = rem(deriv(r),g,Q)
                correction = rem(mul(delta,[(x-y)%Q for x,y in zip(df,dr)]),g,Q)
                assert lhs == [(x+y)%Q for x,y in zip(ko,correction)]
                wrong_sign += lhs != [(x-y)%Q for x,y in zip(ko,correction)]
                uncorrected = rem(mul(delta,df),g,Q)
                omitted_representative += lhs != [(x+y)%Q for x,y in zip(ko,uncorrected)]
                counts['general_transport_inputs'] += 1
assert wrong_sign and omitted_representative

root_families = {1: ((0,1),(1,1)), 2: factors2,
                 3: ((0,1),(1,1),(1,1,0,1),(1,0,1,1))}
for b, factors in root_families.items():
    q = 2**b
    total = [1]
    for g in factors:
        d = len(g)-1
        alpha = rem([0,1],g,4)
        alpha_q = alpha
        for _ in range(b):
            alpha_q = rem(mul(alpha_q,alpha_q),g,4)
        difference = [(x-y)%4 for x,y in zip(alpha_q,alpha)]
        assert all(v%2==0 for v in difference)
        delta = [v//2 for v in difference]
        h = rem(mul(delta,deriv(g)),g,2)
        gn = [g[i]+2*h[i] for i in range(d)]+[1]
        target = [0,-1]+[0]*(q-2)+[1]
        assert rem(target,gn,4) == [0]*d
        total = mul(total,gn)
        counts['mod4_root_factors'] += 1
    expected = [0,-1]+[0]*(q-2)+[1]
    assert [v%4 for v in total] == [v%4 for v in expected]
    counts['complete_mod4_factor_products'] += 1

receipt = {'status':'passed','utc':datetime.now(timezone.utc).isoformat(),
           'scope':'Exact small integer-polynomial transport and mod-4 factor controls; no fast CRT or all-precision setup claim',
           'counts':dict(counts), 'wrong_sign_adverse_cases':wrong_sign,
           'omitted_representative_derivative_adverse_cases':omitted_representative,
           'checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
           'proof_sha256':sha256((ROOT.parent/'route-a/factor-lift-carry-transport.md').read_bytes()).hexdigest(),
           'review_sha256':sha256((ROOT/'REVIEW-FACTOR-LIFT-TRANSPORT.md').read_bytes()).hexdigest()}
(ROOT/'factor-lift-independent-verification.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
