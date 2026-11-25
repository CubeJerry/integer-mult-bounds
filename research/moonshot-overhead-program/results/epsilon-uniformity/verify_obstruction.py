#!/usr/bin/env python3
"""Finite exact checks for INTERCHANGE-OBSTRUCTION.md, not an asymptotic proof."""
import json
from math import comb, isqrt
import platform


def require(ok, message):
    if not ok:
        raise AssertionError(message)


def krawtchouk(n, degree, weight):
    return sum((-1)**r * comb(weight, r) * comb(n-weight, degree-r)
               for r in range(max(0, degree-n+weight), min(weight, degree)+1))


def fwht(values):
    a = list(values)
    stride = 1
    while stride < len(a):
        for start in range(0, len(a), 2*stride):
            for j in range(start, start+stride):
                u, v = a[j], a[j+stride]
                a[j], a[j+stride] = u+v, u-v
        stride *= 2
    return a


def main():
    primes = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 43, 61, 101, 251]
    count = 0
    for p in primes:
        n = 2*p-1
        for t in range(n+1):
            value = krawtchouk(n, p, t)
            r = t//2
            dual = (-1)**(r+t%2)*comb(p-1, r)
            require(value != 0, (p, t, 'zero eigenvalue'))
            require(comb(n, t)*value == comb(n, p)*dual, (p, t, 'duality'))
            count += 1
        require((1<<n)*p > 2*comb(n, p), 'constant eigenvalue')
        require((1<<(2*p))-2 > p*p, 'reserve/count comparison')
    # Independent complete cube spectra, without the closed coefficient formula.
    for p in [3, 5, 7]:
        n = 2*p-1
        spectrum = fwht([int(x.bit_count() == p) for x in range(1<<n)])
        for x, value in enumerate(spectrum):
            require(value == krawtchouk(n, p, x.bit_count()), 'cube spectrum')
    aliases = 0
    for m in range(2, 20000):
        r = (2*m-1).bit_length()
        z = 2*m*r
        root = isqrt(z)
        radius = root + (root*root < z)
        lo, hi = max(0, m//2-radius), min(m, (m+1)//2+radius)
        width = hi-lo
        require(width == min(m, 2*radius+m%2), 'clipped-window formula')
        require(width*width >= m, 'window lower bound')
        for p in [3, 5, 7]:
            if m > (1<<(2*p))-2:
                require(lo+p <= hi, 'missing alias pair')
                require(lo%p == (lo+p)%p, 'different field counts')
                require(pow(-1, lo, p) != pow(-1, lo+p, p), 'same parity')
                aliases += 1
    # Negative controls: changing the dimension/window invalidates the obstruction.
    require(krawtchouk(4, 3, 2) == 0, 'dimension control')
    for p in [3, 5, 7]:
        for start in range(p+2):
            short = {c%p: pow(-1, c, p) for c in range(start, start+p)}
            require(len(short) == p, 'short-window collision')
            require(short[(start+p)%p] != pow(-1, start+p, p), 'extended window')
    require(pow(-1, 1, 2) == pow(-1, 3, 2), 'odd-characteristic restriction')
    print(json.dumps({
        'status': 'PASS_FINITE_INTERCHANGE_OBSTRUCTION_CHECKS',
        'scope': 'Finite exact identities and negative controls; not a universal proof or multiplier benchmark',
        'python': platform.python_version(), 'primes': primes,
        'eigenvalue_duality_checks': count, 'complete_cube_spectra': [32, 512, 8192],
        'integer_windows': 19998, 'alias_pairs': aliases,
        'negative_controls': ['changed cube dimension', 'short window succeeds',
                              'extended window fails', 'characteristic two']
    }, indent=2))


if __name__ == '__main__':
    main()
