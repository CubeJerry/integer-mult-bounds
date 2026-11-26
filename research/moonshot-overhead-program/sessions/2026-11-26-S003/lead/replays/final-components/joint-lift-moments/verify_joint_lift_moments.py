#!/usr/bin/env python3
from itertools import product
from pathlib import Path
import json


def compose(a,b):return tuple(a[b[i]] for i in range(len(a)))

def run():
    counts=dict(word_moments=0, weighted_cases=0, scalar_shift_cases=0, negative_controls=0)
    for m in range(2,9):
        identity=tuple(range(m+1));stars=[]
        for j in range(1,m+1):
            p=list(identity);p[0],p[j]=p[j],p[0];stars.append(tuple(p))
        for weights in ([1]*m, [(-1)**j for j in range(m)], [j%3-1 for j in range(m)]):
            if not any(weights):continue
            moments={}
            for length in (1,2,3,4):
                trace=0
                for word in product(range(m),repeat=length):
                    p=identity;c=1
                    for j in word:p=compose(stars[j],p);c*=weights[j]
                    if p==identity:trace+=c
                    counts['word_moments']+=1
                moments[length]=trace
            q=sum(a*a for a in weights);r4=sum(a**4 for a in weights)
            assert moments[1]==moments[3]==0
            assert moments[2]==q and moments[4]==2*q*q-r4
            assert 0<moments[4]<=2*q*q
            counts['weighted_cases']+=1
            for c in range(-5,6):
                mean2=q+c*c
                mean4=moments[4]+6*c*c*q+c**4
                assert mean4<=3*mean2**2
                counts['scalar_shift_cases']+=1
        # Alternating distinct stars do not cancel at word length four.
        assert compose(compose(compose(stars[0],stars[1]),stars[0]),stars[1])!=identity
        counts['negative_controls']+=1
    return dict(status='pass',scope='low-rank-mixer joint product architecture only',counts=counts)


if __name__=='__main__':
    result=run();Path(__file__).with_name('joint-lift-moments-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
