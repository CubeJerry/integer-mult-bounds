#!/usr/bin/env python3
"""Exact finite certificate checks; neither JR nor SN is established here."""
from hashlib import sha256
from math import isqrt
from pathlib import Path
import json
import random
import sys


def ceil_log2(n):
    return (n - 1).bit_length()


def ceil_sqrt(n):
    r = isqrt(n)
    return r + (r * r != n)


def evaluated_bound(ys):
    value = 1
    for y in reversed(ys):
        p = ceil_sqrt(y * ceil_log2(y + 2))
        value = (1 << y) + (value << p)
    return value


def main():
    rng = random.Random(20261126003)
    cases = 0
    maximum_bits = 0
    for length in range(1, 81):
        for _ in range(8):
            ys = [rng.randrange(1, 2049) for _ in range(length)]
            drops = [rng.randrange(1, 4 * y + 1) for y in ys]
            x = sum(drops)
            value = evaluated_bound(ys)
            floor_log = value.bit_length() - 1
            # C=4; 1/16 is below the proof's 1/(8 sqrt(3)).
            # The ceiling log makes this finite check slightly stronger.
            assert (16 * floor_log) ** 3 >= x * x * ceil_log2(x + 2)
            assert floor_log >= max(ys)
            assert floor_log >= sum(ceil_sqrt(y * ceil_log2(y + 2)) for y in ys)
            maximum_bits = max(maximum_bits, value.bit_length())
            cases += 1

    # Controls show that each stated certificate premise matters.
    x = 1 << 60
    no_local_log = ceil_sqrt(x * ceil_log2(x + 2))
    assert (16 * no_local_log) ** 3 < x * x * ceil_log2(x + 2)
    x = 1 << 40
    no_penalty = 1 + 2 * x  # x unit-arity levels, multiplier one.
    assert (16 * (no_penalty.bit_length() - 1)) ** 3 < x * x * ceil_log2(x + 2)
    fast_descent = evaluated_bound([1])
    assert (16 * (fast_descent.bit_length() - 1)) ** 3 < x * x * ceil_log2(x + 2)

    # A log-free penalty admits a different certificate order. This uses
    # an exact closed-form upper bound, without enumerating 2^20000 levels.
    n = 1 << 20000
    x = n ** 3
    upper_log_without_log_penalty = 2 * n * n + 20001
    assert (16 * upper_log_without_log_penalty) ** 3 < x * x * ceil_log2(x + 2)

    # Exact dyadic-power shape ledgers for the conditional fast numerical
    # schedule. A=4m is a conservative padded arity, not an instantiated JR.
    paths = []
    for root_log in (512, 1024, 2048, 4096, 8192):
        root = a = 1 << root_log
        levels = 0
        product_arity = 1
        sum_gain = 0
        while a.bit_length() - 1 >= 128:
            y = (a.bit_length() - 1) // 32
            m = (1 << y) - 1
            arity = 4 * m
            child = 2 * (a // (2 * arity))
            assert child > 0 and arity * child <= a
            assert child * 8 * m >= a
            assert child * 2 * m <= a
            assert m ** 32 <= a
            # K=4, delta=1/32: local polynomial and gain absorption.
            assert m ** (8 * 4) <= a
            product_arity *= arity
            sum_gain += m ** 4
            levels += 1
            a = child
        assert product_arity * a <= root
        assert sum_gain * 10 < root
        # This base-two batch upper bound divides a root spectator range
        # with exponent root/2, with enormous slack.
        assert 8 * root_log <= root // 2
        paths.append(dict(root_log2_active=root_log, levels=levels,
                          terminal_log2_active=a.bit_length() - 1,
                          product_arity_bound=True, norm_gain_guard=True))

    result = dict(status="pass", scope="Exact positive-majorant and conditional shape diagnostics; no proof of JR, SN or full multiplier execution.",
                  irregular_certificates=cases, maximum_exact_integer_bits=maximum_bits,
                  negative_controls=4, conditional_shape_paths=paths,
                  python=sys.version.split()[0],
                  checker_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                  limitations=["The lower theorem is about a specified positive upper-cost certificate, not runtime.",
                               "Conditional path constants are illustrative; no JR rectangle search is instantiated.",
                               "The unbounded proofs and explicit open hypotheses are in numerical-toll-gate.md."])
    Path(__file__).with_name("numerical-toll-gate-verification.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
