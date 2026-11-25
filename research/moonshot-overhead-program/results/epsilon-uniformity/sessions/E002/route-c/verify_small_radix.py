#!/usr/bin/env python3
"""Finite exact support for small radix and multidigit batching; not tape execution."""
from fractions import Fraction
from functools import lru_cache
from itertools import product
from math import comb, gcd, isqrt, lcm, prod
from pathlib import Path
import json, platform, sys


def prime(n):return n>=2 and all(n%d for d in range(2,isqrt(n)+1))
def compatible(values):
    M=2*prod(abs(x) for x in values)
    assert M
    B=M.bit_length();limit=32*(B+1)**2
    for b in range(3,limit+1,2):
        if prime(b) and M%b:return b,B
    raise AssertionError('R1 finite failure')


def main():
    primecases=0; binomialcases=0; batchcases=0; partitions=0; neg=0; recurrences=0
    for k in range(1,8):
        n=2**k
        Q=lcm(*range(1,n+1));P=prod(p for p in range(2,n+1) if prime(p))
        assert Q%comb(n,n//2)==0
        assert Q<=P**k
        assert comb(n,n//2)*(n+1)>=2**n
        binomialcases+=1
    seeds=[-105,-77,-35,-15,-7,-3,-1,1,2,3,5,7,11,13,105]
    for values in product(seeds,repeat=3):
        b,B=compatible(values)
        assert b<=32*(B+1)**2 and b%2 and all(x%b for x in values)
        primecases+=1
    for b in [2,3,5,7,11]:
        for W in range(3,100):
            for eta in [Fraction(1),Fraction(1,2),Fraction(1,4),Fraction(2,3)]:
                ell=0;A=1
                while A*eta<W:ell+=1;A*=b
                q=(A+W-1)//W
                assert Fraction(q*W,A)<=1+eta
                assert A>=W/eta and A<b*W/eta
                assert q<=b/eta+1
                # Every actual row appears exactly once; only last group can have padding.
                unpacked=[g*W+r for g in range(q) for r in range(W) if g*W+r<A]
                assert unpacked==list(range(A))
                assert all(g*W+r<A for g in range(q-1) for r in range(W))
                batchcases+=1
                if ell>1 and b<W:neg+=1  # literal one digit cannot supply W rows
    for ell in range(1,5):
        for m in range(1,5):
            for a in range(3):
                for e in range(ell+m+2*a,ell+m+2*a+20):
                    f=(e-ell)//(m+2*a);rem=e-ell-(m+2*a)*f
                    assert f>=1 and 0<=rem<m+2*a and f*m<=e
                    cuts=[ell]+[f]*a+[f]*m+[f]*a+[rem]
                    assert sum(cuts)==e
                    # Symbolic index swaps on two chunks, including occupied reserves.
                    old=list(range(2*e));new=old[:];offsets=[];s=0
                    for size in cuts:offsets.append((s,size));s+=size
                    # Main swaps, both reserve groups, then direct leading/remainder.
                    order=list(range(1+a,1+a+m))+list(range(1,1+a))+list(range(1+a+m,1+2*a+m))+[0,len(cuts)-1]
                    for idx in order:
                        start,size=offsets[idx]
                        for u in range(start,start+size):new[u],new[e+u]=new[e+u],new[u]
                    assert new==old[e:]+old[:e]
                    partitions+=1
    for ell in [1,2,5,11]:
        for m in [4,16,36]:
            a=1;E=ell+m+2*a;k=Fraction(isqrt(m),2);C=E
            @lru_cache(None)
            def T(e):
                if e<E:return Fraction(e)
                f=(e-ell)//(m+2*a)
                return C+k*T(f)
            K=2*C+E
            for e in range(1,1001):
                assert T(e)**2<=K*K*e
                recurrences+=1
    assert neg
    out={'status':'PASS_FINITE_EXACT_SMALL_RADIX_AND_MULTIDIGIT_BATCHING',
         'compatible_prime_lists':primecases,'binomial_lcm_cases':binomialcases,
         'batch_padding_cases':batchcases,'digit_partition_cases':partitions,
         'contractive_recurrence_cases':recurrences,
         'one_digit_batch_negative_controls':neg,
         'scope':'Finite arithmetic, occupancy, permutation-partition and recurrence checks. No tape compiler or full multiplier executed.',
         'python':sys.version,'platform':platform.platform()}
    Path('small-radix-verification.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
