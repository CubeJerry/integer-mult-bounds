#!/usr/bin/env python3
"""Independent base-p checks; propagation uses the Fermat polynomial."""
from __future__ import annotations

import itertools
import json
import math
from dataclasses import dataclass
from pathlib import Path


@dataclass(eq=False, slots=True)
class F:
    op: str
    a: object
    b: object = None
    size: int = 1
    degree: int = 0


def c(x): return F("c", x)
def v(x): return F("v", x, degree=1)
def plus(a, b): return F("+", a, b, 1+a.size+b.size, max(a.degree,b.degree))
def times(a, b): return F("*", a, b, 1+a.size+b.size, a.degree+b.degree)


def power(a, n):
    z = c(1)
    for _ in range(n): z = times(z, a)
    return z


def binomial(a, h, p):
    z = c(1)
    for j in range(h): z = times(z, plus(a, c(-j)))
    return times(c(pow(math.factorial(h) % p, -1, p)), z)


def add_digits(x, y, p):
    carry = c(0)
    out = []
    for a,b in zip(x,y):
        out.append(plus(plus(a,b),carry))
        generate = c(0)
        for h in range(1,p):
            generate = plus(generate, times(binomial(a,h,p),binomial(b,p-h,p)))
        propagate = plus(c(1), times(c(-1),power(plus(plus(a,b),c(1)),p-1)))
        carry = plus(generate,times(propagate,carry))
    return out


def count(m,t,u,p):
    r=(m-1).bit_length()
    words=[[v(j) if j<m and k==0 else c(0) for k in range(t)]
           for j in range(1<<r)]
    while len(words)>1:
        words=[add_digits(words[j],words[j+1],p) for j in range(0,len(words),2)]
    offset=(-u) % p**t
    out=add_digits(words[0],[c((offset//p**k)%p) for k in range(t)],p)
    for k,z in enumerate(out):
        assert z.degree<=p**k
        assert z.size<=(32*p*p)**(r+1)*math.comb(r+k+1,k)
    return out


def evaluate(nodes,values,p):
    cache={}
    def rec(z):
        if z in cache:return cache[z]
        if z.op=="c":a=z.a
        elif z.op=="v":a=values[z.a]
        elif z.op=="+":a=rec(z.a)+rec(z.b)
        else:a=rec(z.a)*rec(z.b)
        cache[z]=a%p
        return cache[z]
    return [rec(z) for z in nodes]


def comb(n,h):
    if n>=0:return math.comb(n,h) if h<=n else 0
    return (-1)**h*math.comb(h-n-1,h)


def lucas(n,h,p,t):
    n%=p**t
    z=1
    for _ in range(t):
        z=z*comb(n%p,h%p)%p
        n//=p;h//=p
    assert h==0
    return z


def main():
    result={"status":"PASS","digit_pair_carries":0,"propagation_forms":0,
            "balanced_assignments":0,"negative_offset_assignments":0,
            "copied_size_degree_budgets":0,"signed_Lucas":0,
            "binary_predictors":0,"central_matches":0,"negative_controls":0}
    primes=(2,3,5,7,11,13,17,19,23,31)
    for p in primes:
        for x,y in itertools.product(range(p),repeat=2):
            g=sum(comb(x,a)*comb(y,p-a) for a in range(1,p))%p
            h=sum(comb(x,a)*comb(y,p-1-a) for a in range(p))%p
            k=(1-pow((x+y+1)%p,p-1,p))%p
            assert h==k==int(x+y==p-1)
            result["propagation_forms"]+=1
            for carry in (0,1):
                assert (g+k*carry)%p==(x+y+carry)//p
                assert (x+y+carry)%p==(x+y+carry)-p*((x+y+carry)//p)
                result["digit_pair_carries"]+=1
        for t in range(1,4):
            for n in range(-2*p*p-3,2*p*p+4):
                for h in range(min(p**t,65)):
                    assert comb(n,h)%p==lucas(n,h,p,t)
                    result["signed_Lucas"]+=1
        assert comb(p,p)%p != comb(0,p)%p
        assert comb(-1,1)%p != comb(0,1)%p
        assert (1-pow(p-1,p-1,p))%p==0
        result["negative_controls"]+=3
    for p in (2,3,5,7):
        for m in range(1,5):
            t=1
            while p**t<=m:t+=1
            for u in (-2,m//2,m+1):
                nodes=count(m,t,u,p)
                for digits in itertools.product(range(p),repeat=m):
                    got=evaluate(nodes,digits,p)
                    assert sum(a*p**i for i,a in enumerate(got))==(sum(digits)-u)%p**t
                    result["balanced_assignments"]+=1
                    result["negative_offset_assignments"]+=sum(digits)<u
    for p in (2,3,5,7,11,13):
        for m in (2,3,4,7,8,16,32):
            for degree in sorted({1,math.isqrt(m),m}):
                t=1
                while p**t<=degree:t+=1
                nodes=count(m,t,m//2-3,p)
                size=0
                for h in range(degree+1):
                    digit=h
                    term=c(1)
                    for a in nodes:
                        term=times(term,binomial(a,digit%p,p))
                        digit//=p
                    assert digit==0 and term.degree<=h
                    size+=term.size+3
                assert size<=(m+2)**(20*(1+(p-1).bit_length()))
                result["copied_size_degree_budgets"]+=1
    for p in (3,5,7):
        for m in range(1,6):
            for degree in sorted({1,min(3,m),m}):
                t=1
                while p**t<=degree:t+=1
                for u in (-2,m//2,m+1):
                    nodes=count(m,t,u,p)
                    for values in itertools.product(range(2),repeat=m):
                        digits=evaluate(nodes,values,p)
                        beta_sum=sum((i+1)*v for i,v in enumerate(values))%2
                        predicted=0
                        for h in range(degree+1):
                            digit=h; coefficient=1
                            for a in digits:
                                coefficient=coefficient*comb(a,digit%p)%p
                                digit//=p
                            predicted=(predicted+pow(-2,h,p)*coefficient)%p
                        phase=1 if (u-beta_sum)%2==0 else p-1
                        predicted=predicted*phase%p
                        direct=sum(pow(-2,h,p)*comb(sum(values)-u,h)
                                   for h in range(degree+1))*phase%p
                        assert predicted==direct
                        result["binary_predictors"]+=1
                        if u<=sum(values)<=u+degree:
                            assert predicted==(1 if (sum(values)-beta_sum)%2==0 else p-1)
                            result["central_matches"]+=1
    assert 2%2==0 and all(pow(2,-1,p)*2%p==1 for p in primes if p>2)
    Path(__file__).with_name("prime-count-formula-verification.json").write_text(
        json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,sort_keys=True))


if __name__=="__main__":main()
