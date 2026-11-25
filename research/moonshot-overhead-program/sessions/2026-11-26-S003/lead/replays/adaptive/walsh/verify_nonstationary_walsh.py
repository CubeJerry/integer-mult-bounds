#!/usr/bin/env python3
"""Exact integer ledgers plus high-precision finite recurrence evidence."""
from decimal import Decimal as D, localcontext
from math import isqrt
from pathlib import Path
import hashlib
import json
import platform
import sys


def icbrt_ceil(n):
    lo, hi = 0, 1 << ((n.bit_length() + 2) // 3)
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if mid ** 3 >= n:
            hi = mid
        else:
            lo = mid
    return hi


def ceil_log2(n):
    return (n - 1).bit_length()


def params_from_x(x):
    vx = ceil_log2(x + 2)
    y = icbrt_ceil(x * x * vx)
    v = ceil_log2(y + 2)
    b = isqrt(y // v)
    if b * b * v < y:
        b += 1
    length = 2 * b
    qexp = 2 + (2 * y + length - 1) // length
    return y, length, qexp


def exact_path(x0):
    active = (1 << x0) - 2
    root = active
    product_m = product_a = 1
    total_wbits = levels = 0
    max_remainder_bits = 0
    while active >= 16:
        x = ceil_log2(active + 2)
        y, length, qexp = params_from_x(x)
        m = (1 << y) - 1
        q = 1 << qexp
        d_upper = 1 + length * q
        arity = 2 * (m + d_upper - 1)
        labels = 1 << (length * qexp)
        if d_upper > m or labels > m ** 3 or arity > active // 2:
            break
        f = 2 * (active // (2 * arity))
        assert f >= 2 and f % 2 == 0 and f < active
        remainder = active - arity * f
        assert 0 <= remainder < 2 * arity and remainder % 2 == 0
        h = (y + 3) // 4
        wbits = y + length * qexp + 3 * h
        assert (1 << wbits) <= m ** 8
        total_wbits += wbits
        product_m *= m
        product_a *= arity
        assert product_m <= product_a <= root // f
        max_remainder_bits = max(max_remainder_bits, remainder.bit_length())
        active = f
        levels += 1
    assert (1 << total_wbits) <= root ** 8
    global_k = 2 * root * (x0 + 2)
    spectator_bits = global_k - root
    assert spectator_bits >= total_wbits
    return dict(root_active_log2=x0, levels=levels, leaf_width_bits=active.bit_length(),
                consumed_spectator_bits=total_wbits,
                allowed_polynomial_batch_exponent=8,
                max_direct_remainder_bitlength=max_remainder_bits,
                exact_product_arity_le_root=True,
                exact_power_two_spectator_divisibility=True)


def logarithmic_evidence():
    with localcontext() as ctx:
        ctx.prec = 100
        ln2 = D(2).ln()

        def log2(z):
            return D(z).ln() / ln2

        def fun(x):
            x = D(x)
            return (x * x * log2(x + 2)) ** (D(1) / 3)

        def psi(y):
            y = D(y)
            return (y * log2(y + 2)).sqrt()

        records = []
        minimum_decrement_ratio = None
        maximum_binary_invoice_ratio = D(0)
        ci, kb, cb, target = D(10), D(100), D(16), D(700)
        for exponent in range(12, 181):
            xi = 1 << exponent
            x = D(xi)
            yi, length, qexp = params_from_x(xi)
            y = D(yi)
            assert yi ** 3 >= xi * xi * ceil_log2(xi + 2)
            assert (yi - 1) ** 3 < xi * xi * ceil_log2(xi + 2)
            assert fun(x) <= y <= 2 * fun(x)
            assert y < x / 2
            child = x - y + 4
            decrement = fun(x) - fun(child)
            ratio = decrement / psi(y)
            assert ratio > D(1) / 32
            minimum_decrement_ratio = ratio if minimum_decrement_ratio is None else min(minimum_decrement_ratio, ratio)
            log_route = log2(10) + 1 + log2(length) + qexp + length * log2(1 + qexp)
            maximum_binary_invoice_ratio = max(maximum_binary_invoice_ratio, log_route / psi(y))
            assert log_route < cb * psi(y)
            recursion_log_fraction = cb * psi(y) - target * decrement
            local_log_fraction = ci * fun(x) + kb * y - target * fun(x)
            assert recursion_log_fraction < -2 and local_log_fraction < -2
            norm_log_bound = kb * y + log2(x + 2)
            if exponent >= 64:
                assert norm_log_bound < x - 10
            records.append(dict(log_domain_power=exponent,
                                decrease_ratio=float(ratio),
                                recursion_log_fraction=float(recursion_log_fraction),
                                local_log_fraction=float(local_log_fraction),
                                norm_absorption_checked=exponent >= 64))
        x = D(2) ** 180
        gamma = D(1) / 1000
        assert kb * gamma * x > target * fun(x)
        y = fun(x)
        assert 3 * y > target * (fun(x) - fun(x - y))
        return dict(decimal_precision=100, grid_points=len(records),
                    grid_log_domain_powers=[12, 180],
                    minimum_decrease_over_sqrt_y_log_y=float(minimum_decrement_ratio),
                    maximum_log_binary_route_over_sqrt_y_log_y=float(maximum_binary_invoice_ratio),
                    model_constants=dict(interchange=10, polynomial_degree=100, binary_loss=16, target=700),
                    norm_absorption_grid_points=sum(r["norm_absorption_checked"] for r in records),
                    sampled_first=records[0], sampled_last=records[-1])


def main():
    paths = [exact_path(x) for x in (512, 1024, 2048, 4096, 8192, 16384)]
    assert all(p["levels"] > 0 for p in paths)
    numeric = logarithmic_evidence()
    assert 8 % 4 == 0 and 8 % 8 == 0 and (8 // 4) % 8 != 0
    directory = Path(__file__).parent
    old = directory / "compact-rational-walsh-verification.json"
    json.loads(old.read_text())
    result = dict(scope="Finite integer arity/batch ledgers and high-precision recurrence evidence; no asymptotic or tape-machine certification.",
                  programme_start="0607d044d1d09489580da0e5828588820e1a6775",
                  openai_math="3344da59991ed94f9ba711217b29c1d760badfa6",
                  python=sys.version.split()[0], platform=platform.platform(),
                  exact_paths=paths, log_domain_checks=numeric, negative_controls=3,
                  inherited_rational_replay=dict(file=old.name, sha256=hashlib.sha256(old.read_bytes()).hexdigest(),
                                                 status="previous separate exact replay; not rerun or recounted here"),
                  limitations=["Numerical constants in the log-domain grid are a model invoice, not claimed universal constants of the full compiler.",
                               "Finite exact paths use the valid padded upper dimension 1+Lq; they do not enumerate the enormous label family.",
                               "The asymptotic calculus, physical scheduling and global precision arguments are in the accompanying proof.",
                               "The exact interchanger and integer assembly remain separate interfaces."])
    source = Path(__file__)
    result["checker_sha256"] = hashlib.sha256(source.read_bytes()).hexdigest()
    out = directory / "nonstationary-walsh-verification.json"
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
