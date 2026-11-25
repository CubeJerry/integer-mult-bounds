#!/usr/bin/env python3
"""Finite exact support for E003's two-scale recurrence and radix bridge.

This checks integer choices and adverse cases. It does not execute a tape
multiplier, verify the prime-interval theorem, or prove asymptotic bounds.
"""

from __future__ import annotations

import json
import math
import platform
from datetime import datetime, timezone
from pathlib import Path


def ceil_root(n: int, r: int) -> int:
    assert n >= 0 and r >= 1
    if n <= 1:
        return n
    lo = 0
    hi = 1 << ((n.bit_length() + r - 1) // r)
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if mid**r >= n:
            hi = mid
        else:
            lo = mid
    return hi


def floor_root(n: int, r: int) -> int:
    t = ceil_root(n, r)
    return t if t**r == n else t - 1


def ceil_log2(n: int) -> int:
    assert n >= 1
    return (n - 1).bit_length()


def phi_upper(y: int) -> int:
    return ceil_root(y * y * ceil_log2(y + 2), 3)


def psi_upper(z: int) -> int:
    return ceil_root(z * ceil_log2(z + 2), 2)


counts: dict[str, int] = {}


def count(key: str, n: int = 1) -> None:
    counts[key] = counts.get(key, 0) + n


# All roots are tested against the two exact defining inequalities.
for r in range(1, 10):
    for n in list(range(257)) + [2**k + d for k in range(9, 80, 7) for d in (-1, 0, 1)]:
        c = ceil_root(n, r)
        f = floor_root(n, r)
        assert c**r >= n and (c == 0 or (c - 1) ** r < n)
        assert f**r <= n < (f + 1) ** r
        count("exact_integer_roots")


# Actual source-local label formulas. These checks do not build the huge
# independent-row templates, but they use their exact published majorants.
for z in (64, 96, 128, 192, 256, 384, 512, 768, 1024, 2048, 4096, 8192, 16384, 32768):
    m = (1 << z) + 1
    z_hat = ceil_log2(m)
    v = ceil_log2(z_hat + 2)
    d = 2
    while d**3 * v < z_hat:
        d *= 2
    h = 2 * d - 1
    t = (2 * d * d - 2 + z_hat + d * d - 1) // (d * d)
    q = 1 << t
    assert (1 << (t * d * d)) >= (1 << (2 * d * d - 2)) * m
    routing_dimension = 2 + h * q**h
    incidence = math.comb(h, d) ** (d + 1) * (q - 1) ** d * t ** (d * (d - 1))
    label_log_invoice = ceil_log2(routing_dimension * (1 + incidence)) + 18
    assert label_log_invoice <= 200 * phi_upper(z_hat)
    count("source_interchange_label_profiles")
    if h * h * t <= 5 * z:
        count("source_interchange_polynomial_label_guards")

    ell = 2 * ceil_root((z_hat + v - 1) // v, 2)
    tq = 2 + (2 * z_hat + ell - 1) // ell
    qf = 1 << tq
    route = 10 * (1 + ell * qf) * (1 + tq) ** ell
    assert ceil_log2(route) <= 40 * psi_upper(z_hat)
    count("source_walsh_label_profiles")
    if ell * tq <= 3 * z and 1 + ell * qf <= m:
        count("source_walsh_polynomial_label_guards")


# Interchange's rounded width chain. These are explicit synthetic spatial
# shapes obeying the proved reserve/prefix bounds, not giant source templates.
max_i_ratio = (0, 1)
for y0 in (64, 96, 128, 192, 256, 384, 512, 768, 1024, 2048, 4096, 8192):
    for r in (8, 12, 16):
        for perturb in (-1, 0, 1):
            e = (1 << y0) + perturb
            loss = 0
            depth = 0
            while e.bit_length() > 16:
                m = floor_root(e, r)
                if m % 2 == 0:
                    m -= 1
                if m < 3:
                    break
                reserve = m // 8
                prefix = m * m
                if e < 4 * prefix or e < 32 * m:
                    break
                f = (e - prefix) // (m + 2 * reserve)
                assert e <= 8 * m * f
                assert m * f <= e and 2 <= f < e
                loss += phi_upper(ceil_log2(m))
                e = f
                depth += 1
                count("interchange_rounded_nodes")
            den = phi_upper(y0)
            assert loss <= 128 * den
            if loss * max_i_ratio[1] > max_i_ratio[0] * den:
                max_i_ratio = (loss, den)
            assert depth <= y0
            count("interchange_chains")


# Walsh chooses log m comparable to Phi(log active width), while preserving
# even children and explicitly charging the omitted remainder.
max_w_ratio = (0, 1)
max_b_ratio = (0, 1)
for y0 in (32, 48, 64, 96, 128, 192, 256, 512, 1024, 2048, 4096, 8192, 16384):
    for mult in (2, 3, 4):
        for perturb in (-2, 0, 2):
            a = (1 << y0) + perturb
            loss = 0
            sum_z = 0
            log_batch_product = 0
            depth = 0
            while a.bit_length() > 16:
                y = ceil_log2(a + 2)
                z = phi_upper(y)
                m = (1 << z) + 1
                arity = mult * m
                if a < 4 * arity:
                    break
                f = 2 * (a // (2 * arity))
                remainder = a - arity * f
                assert 0 <= remainder < 2 * arity
                assert 2 * arity * f >= a
                assert arity * f <= a and 2 <= f < a
                loss += psi_upper(z + 3)
                sum_z += z
                # Mock exact power-two batch width <=m^6, as in the source
                # rational family; W5's sum remains an exact integer bound.
                wlog = 5 * z
                assert 1 << wlog <= m**6
                log_batch_product += wlog
                a = f
                depth += 1
                count("walsh_rounded_nodes")
            den = phi_upper(y0)
            assert loss <= 32 * den
            assert sum_z <= y0 + 1
            assert log_batch_product <= 5 * (y0 + 1)
            assert depth <= y0
            if loss * max_w_ratio[1] > max_w_ratio[0] * den:
                max_w_ratio = (loss, den)
            if log_batch_product * max_b_ratio[1] > max_b_ratio[0] * y0:
                max_b_ratio = (log_batch_product, y0)
            count("walsh_chains")


# The common-radix interval's integer guards, without pretending to check
# an unknown analytic cutoff or enumerating astronomically large primes.
for u in (512, 1024, 2048, 4096, 8192, 16384, 32768, 65536):
    for degree in (0, 1, 2, 3):
        s = max(2, u**degree)
        t = 3 * s.bit_length() + 3 * u.bit_length() + 13
        if u < 4 * t:
            count("radix_guarded_fallbacks")
            continue
        e = u // t
        b0 = ceil_root(1 << u, e)
        assert b0 >= 1 << t
        assert b0 >= 4 * e + 4
        assert b0 * b0 >= (16 * (s + 1) * e) ** 5
        assert 3 * u <= 4 * t * e + 4 * t  # floor-rounding sanity
        assert b0 <= (1 << ((4 * t + 2) // 3)) + 1
        count("common_radix_exact_guards")


# Check actual padding ratios for all integer candidates in manageable
# instances. Primality/compatibility do not affect the volume inequality.
for e in range(4, 13):
    for log_b0 in range(6, 12):
        for offset in (-1, 0, 1):
            u = e * log_b0 + offset
            b0 = ceil_root(1 << u, e)
            if b0 < 4 * e + 4:
                continue
            for b in range(b0, b0 + b0 // (2 * e) + 1):
                assert b**e >= 1 << u
                assert b**e < 3 * (1 << u)
                count("exact_padding_candidates")


# Negative controls: the width rounding and the difference between the
# two arity rules are substantive, not labels for an unchanged recurrence.
for arity in range(2, 33):
    for a in range(4 * arity, 8 * arity):
        bad_f = 2 * ((a + 2 * arity - 1) // (2 * arity))
        if arity * bad_f > a:
            count("rejected_round_up_children")
assert counts["rejected_round_up_children"] > 0

for y in (2**12, 2**18, 2**24, 2**30, 2**36):
    # Same power-arity choice would put a linear-y proportional toll in
    # the normalized Walsh invoice; it is not O(Phi(y)).
    if y > 8 * phi_upper(y):
        count("rejected_unpriced_power_arity_walsh_tolls")
assert counts["rejected_unpriced_power_arity_walsh_tolls"] >= 3

report = {
    "status": "passed finite exact checks",
    "utc": datetime.now(timezone.utc).isoformat(),
    "python": platform.python_version(),
    "counts": counts,
    "maximum_finite_interchange_loss_ratio": list(max_i_ratio),
    "maximum_finite_walsh_loss_ratio": list(max_w_ratio),
    "maximum_finite_batch_product_log_ratio": list(max_b_ratio),
    "limitations": [
        "No complete source template or tape multiplier execution",
        "No finite test establishes the asymptotic theorem",
        "No test of the prime-interval theorem or its absolute cutoff",
        "No Lean build or human refereeing",
    ],
}
out = Path(__file__).with_name("two-scale-verification.json")
out.write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
