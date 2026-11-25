#!/usr/bin/env python3
"""Exact dense-recurrence controls; not a finite-tape timing simulation."""
from fractions import Fraction
from itertools import product
from math import comb, factorial, gcd, isqrt, lcm
from pathlib import Path
from random import Random
import json

COUNTS = {}

def inc(name):
    COUNTS[name] = COUNTS.get(name, 0)+1

def mul(a, b):
    c = [0]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i+j] += x*y
    return c

def ev(a, r):
    v = 0
    for x in reversed(a):
        v = v*r+x
    return v

def digits(v, r, length):
    out = []
    for _ in range(length):
        out.append(v % r)
        v //= r
    return out

def solve(a, b):
    n = len(a)
    a = [[Fraction(x) for x in row]+[Fraction(y)] for row, y in zip(a, b)]
    pivots = []
    for j in range(n):
        k = len(pivots)
        p = next((i for i in range(k, n) if a[i][j]), None)
        if p is None:
            continue
        a[k], a[p] = a[p], a[k]
        v = a[k][j]
        a[k] = [x/v for x in a[k]]
        for i in range(n):
            if i != k and a[i][j]:
                v = a[i][j]
                a[i] = [x-v*y for x, y in zip(a[i], a[k])]
        pivots.append(j)
    assert all(any(row[:-1]) or row[-1] == 0 for row in a)
    out = [Fraction(0)]*n
    for i, j in enumerate(pivots):
        out[j] = a[i][-1]
    return out

def prime(p):
    return p >= 2 and all(p % d for d in range(2, isqrt(p)+1))

def pp(a, b, modulus, length):
    r = 1 << (4*(max(len(a), len(b))+1)*modulus**2).bit_length()
    c = digits(ev(a, r)*ev(b, r), r, length)
    oracle = mul(a, b)+[0]*length
    assert c == oracle[:length]
    inc("packed_polynomial_products")
    return [x % modulus for x in c]

def recover(a, b, c, bits, s):
    height = len(a)*(1 << (2*bits))+max(abs(x) for x in c)
    r = 1 << (4*height).bit_length()
    prefix = [x-y for x, y in zip(digits(ev(a[:2*s], r)*ev(b[:2*s], r), r, 2*s), c)]
    coeffs = solve([[prefix[s+i-j-1] for j in range(s)] for i in range(s)],
                   [-prefix[s+i] for i in range(s)])
    denominator = lcm(*(x.denominator for x in coeffs))
    q = [denominator]+[int(x*denominator) for x in coeffs]
    assert all(abs(x) <= factorial(s)*height**s for x in q)
    bound = max(1, denominator.bit_length())
    p = next(p for p in range(2, 8*(bound+2)**2+1) if prime(p) and denominator % p)
    assert gcd(p, denominator) == 1
    modulus = p
    while modulus <= 2*height:
        modulus *= p
    qi = pow(denominator, -1, modulus)
    q = [x % modulus for x in q]
    w = [qi]
    for i in range(1, s):
        w.append(-qi*sum(q[j]*w[i-j] for j in range(1, i+1)) % modulus)
    assert pp(q, w, modulus, s) == [1]+[0]*(s-1)
    previous = [x % modulus for x in prefix[:s]]
    emitted = previous.copy()
    while len(emitted) < len(c):
        rhs = [-x % modulus for x in pp(q, previous, modulus, 2*s)[s:2*s]]
        previous = pp(w, rhs, modulus, s)
        emitted.extend(previous)
        inc("emitted_blocks")
    inc("bounded_rational_reconstructions")
    emitted = [x if 2*x <= modulus else x-modulus for x in emitted[:len(c)]]
    assert all(abs(x) <= height for x in emitted)
    return emitted, denominator, p

def rank(a, q):
    a = [[x % q for x in row] for row in a]
    r = 0
    for j in range(len(a[0])):
        p = next((i for i in range(r, len(a)) if a[i][j]), None)
        if p is None:
            continue
        a[r], a[p] = a[p], a[r]
        v = pow(a[r][j], -1, q)
        a[r] = [v*x % q for x in a[r]]
        for i in range(len(a)):
            if i != r:
                v = a[i][j]
                a[i] = [(x-v*y) % q for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r

def main():
    rng = Random(2026112508)
    examples = []
    for h in (4, 7, 12):
        d = 2*h
        for s in range(1, 5):
            period = [rng.randrange(-9, 10) for _ in range(s)]
            examples.append((h, s, [period[i % s] for i in range(d)], "periodic"))
            coefficients = [rng.randrange(-3, 4) for _ in range(s)]
            examples.append((h, s, [sum(coefficients[j]*comb(i, j) for j in range(s))
                                    for i in range(d)], "polynomial"))
        examples.append((h, 1, [1 << (d-1-i) for i in range(d)], "dyadic"))
        examples.append((h, 1, [0]*d, "zero"))
        examples.append((h, 1, [7]+[0]*(d-1), "initial_impulse"))
        fib = [2, -1]
        while len(fib) < d:
            fib.append(fib[-1]+fib[-2])
        examples.append((h, 2, fib, "fibonacci"))
    for h, s, error, kind in examples:
        a, b = ([rng.randrange(8) for _ in range(h)] for _ in range(2))
        actual = mul(a, b)+[0]
        c = [x-y for x, y in zip(actual, error)]
        result, denominator, p = recover(a, b, c, 3, s)
        assert result == error
        corrected = [x+y for x, y in zip(c, result)]
        assert corrected == actual and ev(corrected, 8) == ev(a, 8)*ev(b, 8)
        if kind == "dyadic":
            assert denominator % 2 == 0 and p != 2
            inc("nonunit_modulus_choices_rejected")
        inc("complete_integer_recovery_cases")

    cap = 8*82**2
    sieve = [True]*(cap+1)
    sieve[0] = sieve[1] = False
    for p in range(2, isqrt(cap)+1):
        if sieve[p]:
            for j in range(p*p, cap+1, p):
                sieve[j] = False
    for bound in range(1, 81):
        assert sum(sieve[:8*(bound+2)**2+1]) > bound
        inc("elementary_small_prime_count_bounds")

    for q in (2, 3):
        for d in (3, 4, 5):
            for _ in range(12):
                a = [[rng.randrange(q) for _ in range(d)] for _ in range(d)]
                r = rank(a, q)
                image = {tuple(sum(row[j]*x[j] for j in range(d)) % q for row in a)
                         for x in product(range(q), repeat=d)}
                assert len(image) == q**r
                if r:
                    assert any(not any(y[:r-1]) and any(y) for y in image)
                inc("linear_image_prefix_injection_controls")

    d = 10
    tail = [0]*(d-1)+[1]
    for rows in range(1, d+1):
        cols = d+1-rows
        assert rank([[tail[i+j] for j in range(cols)] for i in range(rows)], 3) == 1
        inc("finite_hankel_boundary_controls")
    error = [0]*12
    error[2] = 1
    result, _, _ = recover([0]*6, [0]*6, [-x for x in error], 1, 1)
    assert result == [0]*12 and result != error
    inc("rejected_unrestricted_prefix_certificate_claim")
    result = {"status": "all exact finite controls passed", "seed": 2026112508,
              "scope": "exact algebra and packing; not a tape-time simulation", "counts": COUNTS}
    Path(__file__).with_name("dense-recurrence-verification.json").write_text(
        json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
