#!/usr/bin/env python3
"""Exact majorants for PP; no enormous template or full multiplier execution."""
from fractions import Fraction as F
from pathlib import Path
import json
import sys


def ceil_log2(x):
    assert x >= 1
    return (x - 1).bit_length()


def ceil_div(a, b):
    return (a + b - 1) // b


def main():
    count = 0
    max_h = 256
    coefficient = 2 * 8 * 24 * (2 ** 20) * 2 + 6 + 2
    assert 2 * coefficient < 2 ** 40
    for h in range(2, max_h + 1):
        j = 2 ** h
        d = 2 ** ceil_log2(100 * j)
        v = 100 * j
        u = 2 ** ceil_log2((2 ** 60) * j ** 3 * h)
        assert 100 * j <= d < 200 * j
        assert u <= (2 ** 61) * j ** 3 * h
        log4x = ceil_log2(4 * (u + 1))
        loss = F(3 * (u + 1), d) + 10 * d * d * log4x + 41
        assert loss < F(u, 2 * j)
        # m=2**u+1 is never constructed. The next integer exponent
        # above log2(2**(2*d*d-2)*m) is exactly u+2*d*d-1.
        t = ceil_div(u + 2 * d * d - 1, d * d)
        axis = 2 * d - 1
        assert axis * axis * t <= 5 * u
        log_dim = axis * t + ceil_log2(axis) + 3
        log_inc = axis * (d + 1) + d * t + d * (d - 1) * ceil_log2(t)
        assert log_dim <= u and log_inc <= u
        assert log_dim + log_inc + 1 <= F(3 * (u + 1), d) + 10 * d * d * log4x + 1
        tf = ceil_div(2 * (u + 1), v)
        assert v * tf <= 3 * u
        assert tf + ceil_log2(v) + 1 <= u
        fourier_loss = F(2 * (u + 1), v) + v * ceil_log2(3 * (u + 1)) + ceil_log2(3 * v) + 16
        assert fourier_loss < F(u, 2 * j)
        count += 1
    profiles = 0
    for exponent in range(12, 2049):
        s = 2 ** exponent
        h = 2
        while 2 ** (4 * (h + 1)) * (h + 1) <= s:
            h += 1
        j = 2 ** h
        assert j ** 4 * h <= s < (2 * j) ** 4 * (h + 1)
        assert F(j ** 3 * h) + F(s, j) <= 17 * j ** 3 * (h + 1)
        for constant in (1, 16, 2 ** 20, 2 ** 80):
            if j >= 2 * constant:
                assert 2 * constant * j ** 3 * h <= s
        profiles += 1
    caps = 0
    for log_c in range(1, 65):
        c = 2 ** log_c
        r = 4 * c
        n = 64 * c * c
        z = ceil_div(n, r)
        assert c * z + c <= n // 2
        assert c * n > n // 2  # negative control: omit chunk compression
        assert r * r * z <= 2 * r * n
        caps += 1
    # Retaining all spectral tags would destroy the raw 1/16 volume bill.
    m, field_bits = 4096, 14
    assert F(field_bits + 2 * m, 16 * field_bits) > 1
    # A much smaller arity exponent fails the sufficient label margin.
    j, d, u = 16, 2048, 256
    assert F(3 * (u + 1), d) + 10 * d * d * ceil_log2(4 * (u + 1)) > F(u, 2 * j)
    result = dict(python=sys.version.split()[0], passed=True,
                  scope="Exact finite majorants, dyadic eligibility and cap arithmetic; no template instantiation or tape execution.",
                  parameter_cases=count, profile_cases=profiles, cap_cases=caps,
                  paid_pencil_constant=2 ** 20, sufficient_parameter_constant=2 ** 60,
                  negative_controls=["omitted chunk cap", "recursive spectral tags", "insufficient arity guard"],
                  source_openai_math="3344da59991ed94f9ba711217b29c1d760badfa6")
    Path(__file__).with_name("polynomial-profile-verification.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
