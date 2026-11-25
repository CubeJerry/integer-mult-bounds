#!/usr/bin/env python3
"""Exact finite diagnostics for AI's arithmetic, not a tape implementation.

The executable toy local profile uses ell=m^2, a=floor(m^(1/4)) and
Lambda=2 ceil(sqrt(m))*2^ceil(cuberoot(u^2 v))+2a. It intentionally does
not pretend to construct the enormous asymptotic optimized geometry.
"""
from fractions import Fraction
import json
from math import isqrt
from pathlib import Path


def iroot(n, r):
    assert n >= 0 and r >= 1
    lo, hi = 0, 1 << ((n.bit_length() + r - 1) // r)
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if mid ** r <= n:
            lo = mid
        else:
            hi = mid
    return hi if hi ** r <= n else lo


def ceil_log2(n):
    assert n >= 1
    return (n - 1).bit_length()


def ceil_cuberoot(n):
    r = iroot(n, 3)
    return r if r ** 3 == n else r + 1


def profile(e, degree):
    m = iroot(e, degree)
    if m % 2 == 0:
        m -= 1
    assert m >= 3
    a, ell = iroot(m, 4), m * m
    f = (e - ell) // (m + 2 * a)
    u = ceil_log2(m)
    v = ceil_log2(u + 2)
    t = ceil_cuberoot(u * u * v)
    boost = 1 << t
    cs = isqrt(m)
    if cs * cs < m:
        cs += 1
    mass = 2 * cs * boost + 2 * a
    return m, a, ell, f, mass, 8 * boost, t


def run():
    counts = dict(root_boundary_cases=0, width_invoices=0,
                  normalized_mass_invoices=0, local_toll_invoices=0,
                  complete_recurrences=0, leading_batches=0,
                  rejected_missing_leading_reserve_budget=0,
                  rejected_missing_local_tolls=0)
    # Exact root/odd selection checks include both sides of perfect powers.
    for degree in (8, 16, 32, 64):
        for b in (3, 4, 5, 7, 9, 16, 17, 31):
            for off in (-1, 0, 1):
                n = b ** degree + off
                r = iroot(n, degree)
                assert r ** degree <= n < (r + 1) ** degree
                odd = r - (r % 2 == 0)
                assert odd % 2 == 1 and odd ** degree <= n
                assert (odd + 2) ** degree > n
                counts['root_boundary_cases'] += 1
    max_depth = 0
    for degree in (32, 64):
        base_limit = 3 ** degree - 1
        for bits in (128, 256, 512, 1024, 2048, 4096):
            for offset in (0, 17, 12345):
                start = (1 << bits) + offset
                e, chain = start, []
                while e > base_limit:
                    m, a, ell, f, mass, bnd, t = profile(e, degree)
                    assert f >= 1 and f * m <= e
                    assert ell + (m + 2 * a) * f <= e
                    assert e < ell + (m + 2 * a) * (f + 1)
                    assert f <= e // 2
                    counts['width_invoices'] += 1
                    wrong_f = e // m
                    if ell + (m + 2 * a) * wrong_f > e:
                        counts['rejected_missing_leading_reserve_budget'] += 1
                    # Squared exact version of mu<=bnd; no floating point.
                    assert mass * mass <= m * bnd * bnd
                    assert Fraction(mass * mass * f, e) <= bnd * bnd
                    counts['normalized_mass_invoices'] += 1
                    # K=2, delta<=1/32. Exact toll bound, and rational majorant.
                    assert m ** 16 <= e
                    root4 = iroot(e, 4)
                    assert (m * m) ** 2 * root4 * root4 <= e
                    counts['local_toll_invoices'] += 1
                    chain.append((e, m, f, mass, bnd, t, root4))
                    e = f
                max_depth = max(max_depth, len(chain))
                assert sum((Fraction(1, row[6]) for row in chain), Fraction()) <= 8
                base = max(1, e)
                total = base
                for old_e, m, f, mass, bnd, t, root4 in reversed(chain):
                    total = m * m + mass * total
                coeff, independently_unfolded, partial_bound = 1, 0, 1
                for old_e, m, f, mass, bnd, t, root4 in chain:
                    independently_unfolded += coeff * m * m
                    coeff *= mass
                    partial_bound *= bnd
                independently_unfolded += coeff * base
                assert total == independently_unfolded
                assert total * total <= start * (partial_bound * (base_limit + 8)) ** 2
                if chain:
                    assert total > coeff * base
                    counts['rejected_missing_local_tolls'] += 1
                    # A deliberately loose finite diagnostic for summable log loss.
                    u = ceil_log2(start)
                    major_phi = ceil_cuberoot(u * u * ceil_log2(u + 2))
                    assert sum(row[5] + 3 for row in chain) <= 64 * degree * major_phi
                counts['complete_recurrences'] += 1
    for width in (1, 2, 3, 5, 17, 35, 117, 1024):
        for h in (2, 4, 8, 16):
            rows = width * h
            power, ell = 1, 0
            while power < rows:
                power *= 3
                ell += 1
            padded = rows * ((power + rows - 1) // rows)
            assert power <= padded < 2 * power
            assert ell == 0 or power // 3 < rows
            assert padded % rows == 0
            counts['leading_batches'] += 1
    return {'status': 'pass', 'scope': 'exact toy-profile invoices; not optimized geometry or a tape-machine run',
            'counts': counts, 'maximum_checked_recursion_depth': max_depth,
            'toy_profile': {'K': 2, 'root_degrees': [32, 64], 'max_input_width_bitlength': 4097}}


if __name__ == '__main__':
    result = run()
    out = Path(__file__).with_name('adaptive-interchange-verification.json')
    out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
