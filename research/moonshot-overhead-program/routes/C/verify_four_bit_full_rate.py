#!/usr/bin/env python3
"""Formal multivariate full-row factorization of the four-bit carry."""
import itertools
import json
from dataclasses import dataclass
from pathlib import Path

ZERO=frozenset()
ONE=frozenset({(0,0,0,0)})


def plus(a,b):return a^b


def times(a,b):
    out=set()
    for x in a:
        for y in b:
            z=tuple(u+v for u,v in zip(x,y))
            if z in out:out.remove(z)
            else:out.add(z)
    return frozenset(out)


def matrix(n):return [[ZERO for _ in range(n)] for _ in range(n)]


def identity(n,p=ONE):
    out=matrix(n)
    for i in range(n):out[i][i]=p
    return out


def mmul(a,b):
    n=len(a);out=matrix(n)
    for i in range(n):
        for k in range(n):
            if not a[i][k]:continue
            for j in range(n):
                if b[k][j]:out[i][j]=plus(out[i][j],times(a[i][k],b[k][j]))
    return out


def kron(a,b):
    r,s=len(a),len(b)
    return [[times(a[i//s][j//s],b[i%s][j%s]) for j in range(r*s)]
            for i in range(r*s)]


@dataclass
class Module:
    scalar:frozenset
    factors:list
    width:int


def leaf(i):
    exponents=tuple(int(j==i) for j in range(4))
    p=frozenset({exponents})
    return Module(p,[[[p]]],1)


def product(a,b):
    factors=[kron(x,identity(b.width)) for x in a.factors]
    factors += [kron(identity(a.width),y) for y in b.factors]
    return Module(times(a.scalar,b.scalar),factors,a.width*b.width)


def add(a,b):
    d=max(len(a.factors),len(b.factors))
    assert d in (1,2,4)  # odd part one, so the root twist is exactly one
    af=a.factors+[identity(a.width)]*(d-len(a.factors))
    bf=b.factors+[identity(b.width)]*(d-len(b.factors))
    block=a.width*b.width
    factors=[]
    for grade in range(d):
        out=matrix(d*block)
        for first in range(d):
            x=kron(af[first],identity(b.width))
            y=kron(identity(a.width),bf[(grade-first)%d])
            for i in range(block):
                for j in range(block):
                    source=first*block+j
                    dx=((first+1)%d)*block+i
                    dy=first*block+i
                    out[dx][source]=plus(out[dx][source],x[i][j])
                    out[dy][source]=plus(out[dy][source],y[i][j])
        factors.append(out)
    return Module(plus(a.scalar,b.scalar),factors,d*block)


def gf4mul(a,b):
    z=0
    for _ in range(2):
        if b&1:z^=a
        b>>=1;a<<=1
        if a&4:a^=7
    return z


def evaluate(poly,point):
    out=0
    for monomial in poly:
        value=1
        for x,e in zip(point,monomial):
            for _ in range(e):value=gf4mul(value,x)
        out^=value
    return out


def main():
    x1,x2,x3,x4=[leaf(i) for i in range(4)]
    a0,b0=add(x1,x2),add(x3,x4)
    a1,b1=product(x1,x2),product(x3,x4)
    carry=add(product(a1,b1),product(product(add(a1,b1),a0),b0))
    assert carry.width==8 and len(carry.factors)==4
    assert len(carry.scalar)==9
    affine_entries=0
    for factor in carry.factors:
        for row in factor:
            for entry in row:
                assert all(sum(exponents)<=1 for exponents in entry)
                affine_entries+=1
    rotations=0
    for start in range(4):
        got=identity(carry.width)
        for i in range(4):got=mmul(carry.factors[(start+i)%4],got)
        assert got==identity(carry.width,carry.scalar)
        rotations+=1
    cube=0
    for point in itertools.product((0,1),repeat=4):
        assert evaluate(carry.scalar,point)==int(sum(point)==4)
        cube+=1
    assert any(max(exponents)>1 for exponents in carry.scalar)
    assert evaluate(carry.scalar,(2,1,1,0))==1
    assert evaluate(times(times(x1.scalar,x2.scalar),times(x3.scalar,x4.scalar)),
                    (2,1,1,0))==0
    result={"status":"PASS","independent_rows":8,"affine_stages":4,
            "formal_cyclic_matrix_identities":rotations,
            "affine_matrix_entries":affine_entries,"formal_monomials":9,
            "Boolean_count_assignments":cube,"off_cube_negative_controls":1}
    Path(__file__).with_name("four-bit-full-rate-verification.json").write_text(
        json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,sort_keys=True))


if __name__=="__main__":main()
