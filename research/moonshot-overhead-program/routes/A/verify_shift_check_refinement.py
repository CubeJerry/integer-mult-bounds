#!/usr/bin/env python3
"""Independent exact moment, rounding and tensor-check tests."""
import itertools
import json
import random
from math import isqrt
from pathlib import Path


def shifts(m):
    r=1
    while (3**r-1)//2<m:
        r+=1
    basis=[tuple(int(i==j) for i in range(r)) for j in range(r)]
    reps=basis[:]
    for a in itertools.product(range(3),repeat=r):
        if any(a) and next(x for x in a if x)==1 and a not in reps:
            reps.append(a)
    vectors=reps[:m]
    return [tuple(sum(x*y for x,y in zip(a,t))%3 for a in vectors)
            for t in itertools.product(range(3),repeat=r)]


def main():
    rng=random.Random(20261125)
    moments=fractions=tensor=0
    for m in list(range(1,7))+[41,81,121,122,256]:
        family=shifts(m)
        count=len(family)
        assert len(set(family))==count and 2*m+1<=count<6*m+3
        frequencies=(itertools.product(range(3),repeat=m) if m<=6 else
                     [tuple([v]*m) for v in range(3)]+
                     [tuple(rng.randrange(3) for _ in range(m)) for _ in range(8)])
        radius=5*(isqrt(m)+(isqrt(m)**2<m))
        for frequency in frequencies:
            values=[sum((x+y)%3 for x,y in zip(frequency,b)) for b in family]
            assert sum(values)==m*count
            assert 3*sum((v-m)**2 for v in values)==2*m*count
            bad=sum(abs(v-m)>radius for v in values)
            assert 75*bad<=2*count
            if count>=219:
                assert bad<=count//32
            moments+=1
    for r in range(5,17):
        count=3**r
        assert 75*(count//32)>=2*count
        for logw in range(12):
            v=32*(1<<logw)
            rows=count*v
            checks=rows//32
            actual=(count//32)*v
            assert 0<=checks-actual<v
            assert 2*checks==rows//16
            fractions+=1
    for j in (1,2):
        for chosen in itertools.combinations(range(4),j):
            inv=([[1]] if j==1 else
                 [[chosen[1]*pow(chosen[1]-chosen[0],-1,5)%5,
                   -pow(chosen[1]-chosen[0],-1,5)%5],
                  [-chosen[0]*pow(chosen[1]-chosen[0],-1,5)%5,
                   pow(chosen[1]-chosen[0],-1,5)%5]])
            for width in (1,3,7):
                for source in range(j*width):
                    error=[[int(a*width+b==source) for b in range(width)] for a in range(j)]
                    checked=[[sum(pow(chosen[a],h,5)*error[a][b] for a in range(j))%5
                              for b in range(width)] for h in range(j)]
                    recovered=[[sum(inv[a][h]*checked[h][b] for h in range(j))%5
                                for b in range(width)] for a in range(j)]
                    assert recovered==error
                    lift=[[sum(inv[a][h]*error[a][b] for a in range(j))%5
                           for b in range(width)] for h in range(j)]
                    returned=[[sum(pow(chosen[a],h,5)*lift[h][b] for h in range(j))%5
                               for b in range(width)] for a in range(j)]
                    assert returned==error
                    tensor+=1
    assert 3*sum((v-2)**2 for v in (0,3,3))!=2*2*3
    result={'status':'PASS','exact_moment_and_tail_cases':moments,
            'check_budget_cases':fractions,'tensor_left_right_basis_cases':tensor,
            'proportional_vectors_negative_control':True,'full_tape_execution':False}
    Path(__file__).with_name('shift-check-refinement-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
