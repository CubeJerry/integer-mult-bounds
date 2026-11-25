#!/usr/bin/env python3
"""Exact finite tests for prime-characteristic factored carry formulas."""
from __future__ import annotations

import json
from math import comb, factorial
from pathlib import Path


def binomial_poly(x: int, degree: int, p: int) -> int:
    numerator = 1
    for j in range(degree):
        numerator = numerator*(x-j) % p
    return numerator*pow(factorial(degree),-1,p) % p


def generate(x: int,y: int,p: int) -> int:
    return sum(binomial_poly(x,a,p)*binomial_poly(y,p-a,p)
               for a in range(1,p)) % p


def propagate(x: int,y: int,p: int) -> int:
    return sum(binomial_poly(x,a,p)*binomial_poly(y,p-1-a,p)
               for a in range(p)) % p


def generalized_binomial(a: int,h: int) -> int:
    return comb(a,h) if a >= 0 else (-1)**h*comb(h-a-1,h)


def lucas_residue(a: int,h: int,p: int) -> int:
    modulus = p
    while modulus <= h:
        modulus *= p
    a %= modulus
    result = 1
    while h:
        result = result*binomial_poly(a%p,h%p,p) % p
        a //= p
        h //= p
    return result


def bstats(size: int,degree: int,a: int) -> tuple[int,int]:
    return (1,0) if a == 0 else (a*size+3*a+1,a*degree)


def product(a: tuple[int,int],b: tuple[int,int]) -> tuple[int,int]:
    return a[0]+b[0]+1,a[1]+b[1]


def summation(terms: list[tuple[int,int]]) -> tuple[int,int]:
    return sum(v[0] for v in terms)+len(terms)-1,max(v[1] for v in terms)


def bit_stats(children: list[tuple[int,int]],p: int,k: int) -> tuple[int,int]:
    carry = (1,0)
    for i in range(k):
        size,degree = children[i]
        g = summation([product(bstats(size,degree,a),bstats(size,degree,p-a))
                       for a in range(1,p)])
        h = summation([product(bstats(size,degree,a),bstats(size,degree,p-1-a))
                       for a in range(p)])
        carry = summation([g,product(h,carry)])
    return summation([children[k],children[k],carry])


def main() -> None:
    carries = lucas = budgets = predictions = 0
    for p in (2,3,5,7,11,13):
        for x in range(p):
            for y in range(p):
                g,h = generate(x,y,p),propagate(x,y,p)
                assert g == (x+y)//p
                assert h == int(x+y == p-1)
                assert h == (1-pow((x+y+1)%p,p-1,p))%p
                for c in (0,1):
                    assert (g+h*c)%p == (x+y+c)//p
                    assert (x+y+c)%p == x+y+c-p*((g+h*c)%p)
                    carries += 1
        for a in range(-100,101):
            for h in range(65):
                assert lucas_residue(a,h,p) == generalized_binomial(a,h)%p
                lucas += 1
        children = [(1,int(k == 0)) for k in range(11)]
        for r in range(1,11):
            nxt = [bit_stats(children,p,k) for k in range(11)]
            for k,(size,degree) in enumerate(nxt):
                assert degree <= p**k
                assert size <= 32*p*p*sum(children[i][0] for i in range(k+1))
                assert size <= (32*p*p)**r*comb(r+k,k)
                budgets += 1
            children = nxt
        if p > 2:
            for m in range(1,10):
                for u in range(-2,m+3):
                    for degree in range(m+1):
                        for count in range(m+1):
                            left = sum(pow(-2,h,p)*lucas_residue(count-u,h,p)
                                       for h in range(degree+1)) % p
                            exact = sum((-2)**h*generalized_binomial(count-u,h)
                                        for h in range(degree+1)) % p
                            assert left == exact
                            if 0 <= count-u <= degree:
                                assert left == pow(-1,count-u,p)
                            predictions += 1
        # Reduction of the count modulo p alone loses its next digit.
        assert lucas_residue(0,p,p) != lucas_residue(p,p,p)
        # Omitting propagation loses the carry when x+y=p-1 and c=1.
        assert generate(p-1,0,p) == 0 and (p-1+0+1)//p == 1

    result = {'status':'PASS','digit_carry_cases':carries,
              'signed_lucas_cases':lucas,'unfolded_size_degree_cases':budgets,
              'odd_prime_predictor_cases':predictions,'negative_controls':12,
              'floating_point_used':False,'full_multiplier_executed':False}
    Path(__file__).with_name('prime-carry-verification.json').write_text(
        json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
