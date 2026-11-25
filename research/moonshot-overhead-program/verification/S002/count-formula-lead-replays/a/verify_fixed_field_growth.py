#!/usr/bin/env python3
"""Exact finite checks of Q2--Q7 and the sparse Q11--Q12 inversion.

This does not construct the exponentially large finite template or execute
a tape multiplier. Every tested inequality uses integer/rational bounds.
"""
from __future__ import annotations

import json
from fractions import Fraction
from math import comb
from pathlib import Path


def ceil_log2(n: int) -> int:
    assert n >= 1
    return (n - 1).bit_length()


def invoices(j: int, u: int) -> tuple[Fraction, Fraction, int, int]:
    # For m=2^u+1, u<log2(m)<u+1.
    d = 1 << ceil_log2(100*j)
    ell = 2*((100*j+1)//2)
    x_upper = u+1
    interchange = Fraction(3*x_upper, d) + 10*d*d*ceil_log2(4*x_upper)+15
    fourier = (Fraction(2*x_upper, ell)+ell*ceil_log2(3*x_upper)
               +ceil_log2(3*ell)+8)
    return interchange, fourier, d, ell


def main() -> None:
    parameters = negatives = 0
    js = list(range(3,4097)) + [10**k+1 for k in range(4,31)]
    for j in js:
        x0_upper = (1 << 40)*j**3*ceil_log2(j)
        u = 1 << ceil_log2(x0_upper)
        interchange, fourier, d, ell = invoices(j,u)
        assert 100*j <= d < 200*j
        assert 100*j <= ell <= 202*j
        assert interchange+1 <= Fraction(u,2*j)
        assert fourier+2 <= Fraction(u,2*j)
        assert 12*d*d <= u
        assert ell <= u
        assert u >= 10
        parameters += 1
        too_small = j**3*ceil_log2(j)
        weak,_,_,_ = invoices(j,too_small)
        assert weak+1 > Fraction(too_small,2*j)
        negatives += 1

    labels = 0
    for d in (2,4,8,16):
        h = 2*d-1
        cr = 1 << (2*d*d-2)
        for u in range(d,513,7):
            m = (1 << u)+1
            t = max(1,(ceil_log2(cr*m)+d*d-1)//(d*d))
            q = 1 << t
            assert q**(d*d) >= cr*m
            if t > 1:
                assert (q//2)**(d*d) < cr*m
            assert t <= 3+Fraction(u+1,d*d)
            dimension = 2+h*q**h
            incidence = comb(h,d)**(d+1)*(q-1)**d*t**(d*(d-1))
            lhs_upper = ceil_log2(dimension*(1+incidence))
            rhs_lower = Fraction(3*u,d)+10*d*d*((4*u).bit_length()-1)
            assert lhs_upper <= rhs_lower
            labels += 1

    sparse = 0
    for constant in (1,2,16,128,1 << 20):
        for log_z in range(16,129):
            z = 1 << log_z
            h = 0
            while 2*constant*(1 << (3*(h+1)))*log_z <= z:
                h += 1
            if h < 2:
                continue
            j = 1 << h
            assert 2*constant*j**3*h <= z
            assert 2*constant*(2*j)**3*log_z > z
            assert j >= 4
            sparse += 1

    output = {
        'status':'PASS',
        'parameter_margin_and_guard_cases':parameters,
        'missing_threshold_constant_negative_controls':negatives,
        'exact_characteristic_two_label_majorants':labels,
        'sparse_profile_rounding_cases':sparse,
        'floating_point_used':False,
        'full_template_or_multiplier_executed':False,
    }
    Path(__file__).with_name('fixed-field-growth-verification.json').write_text(
        json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))


if __name__ == '__main__':
    main()
