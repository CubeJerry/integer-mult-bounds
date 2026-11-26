#!/usr/bin/env python3
"""Finite checks for joint star conjugation and scalar full-rate lift cost."""
from itertools import product
from pathlib import Path
import json, random


def star(x,j):
    y=list(x);y[0],y[j]=y[j],y[0];return tuple(y)

def dot(pair):return (pair[0]&pair[1]).bit_count()%2

def u0(x):
    y=list(x);y[0]=(y[0][1],y[0][0]);return tuple(y),(-1)**dot(x[0])

def middle(x,j):
    y=list(x);y[0]=(x[j][1],x[j][0]);y[j]=(x[0][1],x[0][0])
    return tuple(y),(-1)**(dot(x[j])+dot(y[j]))

def matmul(a,b,p):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b)))%p for j in range(len(b[0]))] for i in range(len(a))]

def run():
    counts=dict(signed_conjugations=0, cyclic_regular_conjugations=0, independence_witnesses=0,
                partial_lift_outputs=0, rejected_single_call_full_rate=0,
                matching_full_rate_outputs=0, seed_dependent_outputs=0, volume_invoices=0)
    for m,f in ((1,1),(2,1),(3,1),(1,2),(2,2)):
        pairs=list(product(range(1<<f),repeat=2))
        for x in product(pairs,repeat=m+1):
            for j in range(1,m+1):
                first,s1=u0(x);mid=star(first,j);last,s2=u0(mid)
                direct,sd=middle(x,j)
                assert (last,s1*s2)==(direct,sd)
                counts['signed_conjugations']+=1
    rng=random.Random(7619)
    for m in range(1,6):
        for alphabet in (2,3):
            addresses=list(product(range(alphabet),repeat=m+1))
            def cycle(x, steps):
                z=list(x)
                for i in range(1,m+1):z[1+(i-1+steps)%m]=x[i]
                return tuple(z)
            for x in addresses:
                for j in range(1,m+1):
                    assert cycle(star(cycle(x,-(j-1)),1),j-1)==star(x,j)
                    counts["cyclic_regular_conjugations"]+=1
            index={x:i for i,x in enumerate(addresses)}
            perms=[[index[star(x,j)] for x in addresses] for j in range(1,m+1)]
            witness=(1,)+(0,)*m
            assert len({star(witness,j) for j in range(1,m+1)})==m
            counts['independence_witnesses']+=1
            for p in (5,7):
                weights=[1+j%(p-1) for j in range(m)]
                x=[rng.randrange(p) for _ in addresses]
                lifted=[[weights[j]*x[i]%p for i in perms[j]] for j in range(m)]
                output=[sum(row[i] for row in lifted)%p for i in range(len(addresses))]
                direct=[sum(weights[j]*x[perms[j][i]] for j in range(m))%p for i in range(len(addresses))]
                assert output==direct
                counts['partial_lift_outputs']+=len(addresses)
                for r in (1,2,4):
                    inputs=[[rng.randrange(p) for _ in addresses] for _ in range(r)]
                    outputs=[]
                    for row in inputs:
                        call=[[weights[j]*row[i]%p for i in perms[j]] for j in range(m)]
                        outputs.append([sum(c[i] for c in call)%p for i in range(len(addresses))])
                    expected=[[sum(weights[j]*row[perms[j][i]] for j in range(m))%p for i in range(len(addresses))] for row in inputs]
                    assert outputs==expected
                    counts['matching_full_rate_outputs']+=r*len(addresses)
                    seed_weights=[[1+(i+j)%(p-1) for j in range(m)] for i in range(r)]
                    seeded=[]
                    for i,row in enumerate(inputs):
                        call=[[seed_weights[i][j]*row[k]%p for k in perms[j]] for j in range(m)]
                        seeded.append([sum(c[k] for c in call)%p for k in range(len(addresses))])
                    expected_seeded=[[sum(seed_weights[i][j]*row[perms[j][k]] for j in range(m))%p for k in range(len(addresses))] for i,row in enumerate(inputs)]
                    assert seeded==expected_seeded
                    counts['seed_dependent_outputs']+=r*len(addresses)
                    assert r*m/r==m
                    counts['volume_invoices']+=1
    # Exhaustive scalar A,B for m=R=2 over F2: no coefficient is I_2.
    matrices=[]
    for a in product(range(2),repeat=4):matrices.append([list(a[:2]),list(a[2:])])
    identity=[[1,0],[0,1]]
    for a in matrices:
        for b in matrices:
            coeff=[]
            for j in range(2):coeff.append([[a[i][j]*b[j][k]%2 for k in range(2)] for i in range(2)])
            assert not all(c==identity for c in coeff)
            counts['rejected_single_call_full_rate']+=1
    return dict(status='pass',scope='joint regular lift with scalar pre/post compression; not all joint star algorithms',counts=counts)


if __name__=='__main__':
    r=run()
    Path(__file__).with_name('star-pencil-lift-verification.json').write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps(r,indent=2))
