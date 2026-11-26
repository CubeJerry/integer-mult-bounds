"""Independent integral, finite-switch and rational endpoint checks for coefficient 53."""
from decimal import Decimal as D, localcontext
from fractions import Fraction as F
from math import comb, factorial
import json


def ceil_log(n):
    return (n - 1).bit_length()


def q_at(j):
    return 3 * j + ceil_log(3 * j + 3) + 2


def check_degrees():
    total = counts_larger = 0
    for j in range(4, 225):
        d0 = 1 << j
        q = q_at(j)
        next_q = q_at(j + 1)
        band = q * d0 ** 3
        next_band = next_q * (2 * d0) ** 3
        candidates = {band + i for i in (0, 1, 2, 5)}
        candidates.update(a * band + i for a in (2, 3, 4, 7, 8) for i in (-1, 0, 1))
        candidates.update(next_band - i for i in (1, 2, 3, 17))
        for p in sorted(x for x in candidates if band <= x < next_band):
            # Actual e=2^{240u}, m=2^u−1, ceil(log₂m)=u. No huge m must be materialized.
            u = p + 2
            v = ceil_log(u + 2)
            d = 1 << (((u // v).bit_length() - 1) // 3)
            assert d ** 3 * v <= u < (2 * d) ** 3 * v and d >= d0
            if d == d0:
                t = (u + 2 * d * d - 2 + d * d - 1) // (d * d)
                assert t <= d0 * (8 * next_q + 1)
                assert 39 + 12 * d <= d * d
                assert F(d * d, u - 1) <= F(d0 * d0, p)
            else:
                counts_larger += 1
                assert d >= 2 * d0 and F(17, 4 * d) < F(3, d0)
            total += 1
    return {"actual_degree_probes": total, "earlier_degree_switches": counts_larger}


def rational():
    J = 11500
    j0 = J + 10
    M, h0 = F(1447, 200), F(36169, 5000)
    E, U = F(167, 500), F(8001, 1000)
    log_U = F(21, 10)
    assert 11500 // 500 == 23 and (1 << 14) > J + 2
    assert 3 * 11 + 6 <= (1 << (11 - 5))
    assert F(8) + F(32, 3 * J) < U
    assert sum(log_U ** n / factorial(n) for n in range(8)) > U
    assert sum(F(7, 10) ** n / factorial(n) for n in range(4)) > 2
    assert 6 + (h0 - 3 + E * log_U) / 4 == h0
    assert (20 - h0) / 4 ** 10 < M - h0
    assert 4 * M - (M + 3 * (U - 1) + E * log_U) == F(3, 5000)
    assert F(4497, 100) ** 3 - 240 * M ** 3 == F(50622783, 1000000)
    assert 240 * F(217, 30) ** 3 < 45 ** 3
    assert 3 * 1000 >= 2000 and F(1, 3000) + F(1, 2000) < F(1, 1000)
    assert F(4497, 100) + 8 * F(1001, 1000) == F(26489, 500)
    assert 4 * (F(26489, 500) - 48) * 4 >= 10 * (4 + 3)
    remaining = 53 - F(26489, 500) - F(1, 64)
    assert remaining == F(51, 8000)
    assert F(4096 * 31) <= (1 << 30)
    assert remaining * (1 << 20) > 182 + 2 * F(26489, 500) + 1
    Q = q_at(j0)
    v0 = 240 * (Q * (1 << (3 * j0)) + 2)
    assert Q == 34548 and (4 * v0) ** 2 < (1 << 69110)
    assert ((4 * v0) ** 2).bit_length() == 69110
    # The unrounded rank bound uses binom(2d−1,d)≤2^(2d−1).
    assert all(comb(2 * d - 1, d) <= 1 << (2 * d - 1) for d in (16, 32, 64, 128, 256, 512))
    return {"explicit_start_band": J, "certified_guard_exponent": 69110,
            "first_controlled_band": j0, "last_rational_slack": str(remaining)}


def quadrature():
    # Numerical quadrature checks the written integral independently of its closed form.
    with localcontext() as ctx:
        ctx.prec = 45
        ln2 = D(2).ln()
        h = D(7) + ln2 / 3
        R13 = (D(240).ln() / 3).exp()
        assert D('52.9371013839180') < 8 + R13 * h < D('52.9371013839182')
        probes = 0
        for j in (5, 31, 99, 511, 11500, 11510, 99999):
            q, after = D(q_at(j)), D(q_at(j + 1))
            U = 8 * after / q
            E = (j + (8 * after + 1).ln() / ln2 + 3) / q
            area = 3 * (U - 1) + E * U.ln()
            n = 257
            dx = (U - 1) / n
            left = dx * sum(3 + E / (1 + i * dx) for i in range(n))
            right = dx * sum(3 + E / (1 + i * dx) for i in range(1, n + 1))
            assert right < area < left
            probes += n
        for j in range(1, 1000):
            t = D(1) + 7 * D(j) / 1000
            F_t = (h + 3 * (t - 1) + t.ln() / 3) / (2 * t.ln() / 3).exp()
            assert F_t < h
        return {"quadrature_subintervals": probes, "limiting_interior_probes": 999,
                "invoice_limsup": str(8 + R13 * h)}


if __name__ == '__main__':
    print(json.dumps({**check_degrees(), **rational(), **quadrature()}, sort_keys=True))
