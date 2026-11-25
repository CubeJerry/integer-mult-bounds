#!/usr/bin/env python3
"""Exact finite checks for the sparse residual component, not a TM replay."""
from __future__ import annotations
from fractions import Fraction
from itertools import product
import json
from math import comb, gcd, prod
from pathlib import Path
from random import Random

RNG = Random(2026112604)
COUNTS: dict[str, int] = {}

def inc(name: str, n: int = 1) -> None:
    COUNTS[name] = COUNTS.get(name, 0) + n

def mul(a: list[int], b: list[int]) -> list[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            out[i + j] += ai * bj
    return out

def ev(a: list[int], r: int) -> int:
    z = 0
    for x in reversed(a):
        z = z * r + x
    return z

def theta(a: list[int]) -> list[int]:
    return [i * x for i, x in enumerate(a)]

def fold(a: list[int], ell: int) -> list[int]:
    out = [0] * ell
    for i, x in enumerate(a):
        out[i % ell] += x
    return out

def balanced_decode(value: int, ell: int, r: int) -> list[int]:
    modulus = r**ell - 1
    z = value % modulus
    if 2 * z > modulus:
        z -= modulus
    out = []
    for _ in range(ell):
        digit = z % r
        if 2 * digit >= r:
            digit -= r
        out.append(digit)
        z = (z - digit) // r
    assert z == 0, "radix height hypothesis violated"
    return out

def scan_mod(value: int, modulus: int, width: int) -> int:
    """Reference block reduction with the exact reciprocal in the proof."""
    assert value >= 0 and 1 < modulus < 1 << width
    reciprocal = (1 << (2 * width)) // modulus
    mask = (1 << width) - 1
    chunks = []
    while value:
        chunks.append(value & mask)
        value >>= width
    rem = 0
    for block in reversed(chunks):
        u = (rem << width) + block
        q0 = (u * reciprocal) >> (2 * width)
        assert u // modulus - 1 <= q0 <= u // modulus
        rem = u - q0 * modulus
        assert 0 <= rem < 2 * modulus
        if rem >= modulus:
            rem -= modulus
        inc("barrett_blocks")
    return rem

def recover_core(a: list[int], b: list[int], c: list[int], bits: int,
                 sparse_bound: int) -> tuple[dict[int, int], dict[str, int]]:
    """Tests modular core even when the physical theorem would fall back."""
    h = len(a)
    assert len(b) == h and len(c) == 2 * h
    d = 2 * h
    cmax = max(abs(x) for x in c)
    emax = h * (1 << (2 * bits)) + cmax
    q = (d - 1).bit_length()
    bstar = comb(2 * sparse_bound, 2) * q
    cap = 2 * bstar + 4
    beta = (8 * d * (sparse_bound + 1) * (emax + 1)).bit_length()
    radix = 1 << beta
    modulus = prod(radix**ell - 1 for ell in range(1, cap + 1))
    width = beta * cap * (cap + 1) // 2
    assert modulus < 1 << width
    # Derived from operands/candidate, not the test oracle's true residual.
    ar, br = ev(a, radix) % modulus, ev(b, radix) % modulus
    cr = ev(c, radix) % modulus
    ad, bd = ev(theta(a), radix) % modulus, ev(theta(b), radix) % modulus
    cd = ev(theta(c), radix) % modulus
    er = (ar * br - cr) % modulus
    ed = (ad * br + ar * bd - cd) % modulus
    assert scan_mod(ev(a, radix), modulus, width) == ar
    assert scan_mod(ev(b, radix), modulus, width) == br
    for ell in range(1, cap + 1):
        u = balanced_decode(er, ell, radix)
        v = balanced_decode(ed, ell, radix)
        inc("decoded_fold_pairs")
        cand: dict[int, int] = {}
        valid = True
        for j, (coefficient, weighted) in enumerate(zip(u, v)):
            if coefficient == 0:
                if weighted:
                    valid = False
                    break
                continue
            if weighted % coefficient:
                valid = False
                break
            exponent = weighted // coefficient
            if not (0 <= exponent < d and exponent % ell == j
                    and abs(coefficient) <= emax):
                valid = False
                break
            cand[exponent] = coefficient
        if not valid or len(cand) > sparse_bound:
            continue
        fingerprint = sum(value * pow(radix, exponent, modulus)
                          for exponent, value in cand.items()) % modulus
        if fingerprint == er:
            return cand, {"length": ell, "K": cap, "beta": beta,
                          "k": width, "V": d * beta}
    raise AssertionError("no candidate under sparse promise")

def test_lcm_and_collision_family() -> None:
    current = 1
    for n in range(1, 100):
        current = current * n // gcd(current, n)
        assert current * n >= 1 << (n - 1)
        for j in range(n):
            assert current % comb(n - 1, j) == 0
            inc("binomial_lcm_divisibilities")
    for d in range(2, 25):
        for s in range(1, min(5, d) + 1):
            cap = 2 * comb(2 * s, 2) * (d - 1).bit_length() + 4
            for _ in range(10):
                support = RNG.sample(range(d), min(2 * s, d))
                assert any(len({i % ell for i in support}) == len(support)
                           for ell in range(1, cap + 1))
                inc("collision_family_supports")

def test_balanced_folds() -> None:
    for d in range(2, 30):
        for s in range(1, min(d, 5) + 1):
            for _ in range(3):
                residual = [0] * d
                for i in RNG.sample(range(d), s):
                    residual[i] = RNG.choice([-7, -2, -1, 1, 3, 7])
                radix = 1 << (8 * d * (s + 1) * 8).bit_length()
                for ell in range(1, 10):
                    assert balanced_decode(ev(residual, radix), ell, radix) == fold(residual, ell)
                    assert balanced_decode(ev(theta(residual), radix), ell, radix) == fold(theta(residual), ell)
                    inc("signed_value_derivative_folds")

def test_barrett() -> None:
    for width in range(2, 33):
        for _ in range(15):
            modulus = RNG.randrange(2, 1 << width)
            value = RNG.getrandbits(5 * width + 3)
            assert scan_mod(value, modulus, width) == value % modulus
            inc("barrett_long_integers")
    found = False
    for width in range(2, 10):
        for modulus in range(2, 1 << width):
            reciprocal = (1 << (2 * width)) // modulus + 1
            for u in range(min(modulus * (1 << width), 400)):
                if (u * reciprocal) >> (2 * width) > u // modulus:
                    found = True
                    break
            if found:
                break
        if found:
            break
    assert found
    inc("rejected_wrong_reciprocal_control")

def test_end_to_end() -> None:
    for h, bits, s, repeats in [(2, 2, 1, 8), (3, 3, 1, 8),
                               (5, 3, 2, 8), (8, 4, 2, 6),
                               (9, 2, 3, 3)]:
        for _ in range(repeats):
            a = [RNG.randrange(1 << bits) for _ in range(h)]
            b = [RNG.randrange(1 << bits) for _ in range(h)]
            actual = mul(a, b) + [0]
            residual = [0] * (2 * h)
            count = RNG.randrange(s + 1)
            for i in RNG.sample(range(2 * h), count):
                residual[i] = RNG.choice([-9, -3, -1, 1, 4, 9])
            candidate = [x - e for x, e in zip(actual, residual)]
            decoded, metadata = recover_core(a, b, candidate, bits, s)
            assert decoded == {i: e for i, e in enumerate(residual) if e}
            corrected = [x + decoded.get(i, 0) for i, x in enumerate(candidate)]
            assert corrected == actual
            assert ev(corrected, 1 << bits) == ev(a, 1 << bits) * ev(b, 1 << bits)
            inc("complete_sparse_recovery_cases")
            if metadata["length"] > 1:
                inc("recovery_required_nontrivial_fold")
    e = [3, 0, -3]
    assert fold(e, 2) == [0, 0] and fold(theta(e), 2) == [-6, 0]
    inc("rejected_zero_sum_collision_control")

def test_dense_false_certificate() -> None:
    d, s = 4096, 1
    cap = 2 * comb(2 * s, 2) * (d - 1).bit_length() + 4
    j = [1]
    for ell in range(1, cap + 1):
        j = mul(j, [-1] + [0] * (ell - 1) + [1])
    error = mul(j, j)
    assert len(error) <= d and sum(x != 0 for x in error) > s
    for ell in range(1, cap + 1):
        assert all(x == 0 for x in fold(error, ell))
        assert all(x == 0 for x in fold(theta(error), ell))
        inc("dense_false_certificate_moduli")
    assert any(error)
    inc("rejected_general_certificate_claim")

def round_fraction(x: Fraction) -> int:
    return (2 * x.numerator + x.denominator) // (2 * x.denominator)

def test_dense_rounding_barrier() -> None:
    for m, rows in [(2, 1), (2, 2), (3, 1)]:
        n = 1 << m
        for _ in range(3):
            coeff = {(a, b, shift): Fraction(RNG.randrange(-3, 4), 2)
                     for a in range(rows) for b in range(rows)
                     for shift in range(n - 1)}
            wrong, cases = 0, 0
            for x in product((0, 1), repeat=rows * n):
                for a in range(rows):
                    for g in range(n):
                        y = sum(coeff[a, b, shift] * x[b * n + (g ^ shift)]
                                for b in range(rows) for shift in range(n - 1))
                        wanted = x[a * n + (g ^ (n - 1))]
                        wrong += round_fraction(y) != wanted
                        inc("ordinary_rounding_output_checks")
                cases += 1
            assert 2 * wrong >= cases * rows * n
            inc("dense_rounding_predictors")

def main() -> None:
    test_lcm_and_collision_family()
    test_balanced_folds()
    test_barrett()
    test_end_to_end()
    test_dense_false_certificate()
    test_dense_rounding_barrier()
    out = {"status": "passed", "scope": "Exact finite algebra and reference integer arithmetic; not a fixed-tape execution or proof of asymptotics", "seed": 2026112604, "counts": COUNTS}
    Path(__file__).with_name("sparse-residual-verification.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
