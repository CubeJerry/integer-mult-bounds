#!/usr/bin/env python3
from itertools import product
from fractions import Fraction
from pathlib import Path
import json

def streamed(m,Q,gap,suffix):
    key=[0]*m
    for hs in product(range(Q),repeat=m):
        for g in range(gap):
            ns=[0]*m
            def visit(j):
                if j==m:
                    for b in range(suffix): yield hs,g,tuple(ns),b,tuple(key)
                    return
                n=0
                for length,label in ((hs[j],2),(1,0),(Q-hs[j]-1,1)):
                    key[j]=label
                    for _ in range(length):
                        ns[j]=n; n+=1
                        yield from visit(j+1)
            yield from visit(0)

records=wrong=0
for m,f,gap,suffix in [(1,1,1,1),(1,2,2,3),(1,4,1,1),(2,1,2,3),(2,2,1,1),(3,1,1,2)]:
    Q=3**f
    expected=((hs,g,ns,b,tuple(0 if h==n else 1 if h<n else 2 for h,n in zip(hs,ns)))
              for hs in product(range(Q),repeat=m) for g in range(gap)
              for ns in product(range(Q),repeat=m) for b in range(suffix))
    count=0
    for actual,wanted in zip(streamed(m,Q,gap,suffix),expected,strict=True):
        assert actual==wanted
        records+=1; count+=1
        wrong+=any(x and x!=(-x)%3 for x in actual[-1])
    assert count==Q**(2*m)*gap*suffix
assert wrong>0
# Exact control-preparation density for nested N loops.
ledgers=0; largest=Fraction(0)
for m in [1,2,3,10,100]:
    for f in range(1,65):
        Q=3**f
        ratio=Fraction(f**4*sum(Q**j for j in range(m)),Q**m)
        assert ratio<=4
        largest=max(largest,ratio); ledgers+=1
out={'status':'passed','complete_keys_checked':records,
     'wrong_orientation_negative_control_records':wrong,
     'exact_preparation_density_ledgers':ledgers,'largest_density':str(largest),
     'scope':'Exact nested-run ordering and boundary labels, plus finite rational amortization ledgers; not literal tape-head execution.'}
Path(__file__).with_name('streamed-keys-verification.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
