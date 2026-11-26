#!/usr/bin/env python3
"""Integer receipts for the two declared ordinary polynomial operand extents."""
from math import gcd
import json


def volume(c):
    a = 1 << c
    h = a*a
    q = h*a
    b = 3*c
    ordinary = sum(1 << gcd(c, j) for j in range(c)) // c
    repp = sum((1 << gcd(c,j)) * (1 + int((c // gcd(c,j)) % 2 == 0)) for j in range(c))
    assert repp % c == 0
    planes = repp // c
    if c == 2:
        assert (ordinary, planes) == (3, 4)
    def operand(w):
        return (a-2)*(2*w-1)+w
    def rootbits(size):
        log2ceil = (2*size-2).bit_length()
        return 1 << (3*max(1,(log2ceil+2)//3))
    sizes = [((h+c-1)//c,operand(c)),(2*a*planes,operand(b))]
    by_family = [n*s/q for n,s in sizes]
    return {'c':c, 'actual_planes':str(planes), 'ordinary_orbits':str(ordinary), 'ratio_by_family':by_family, 'total_ratio':sum(by_family),
            'declared_two_full_children_ratio':sum(n*2*rootbits(s) for n,s in sizes)/q}

print(json.dumps({'cases':[volume(c) for c in (1,2,3,4,8,16,32,63,64,127,128,256,509)]},indent=2))
