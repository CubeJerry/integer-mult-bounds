#!/usr/bin/env python3
"""Exact controls for the positive residual certificate, not a TM replay."""
from itertools import product
from math import comb, prod
from pathlib import Path
import json
import random

COUNTS = {}


def count(key, amount=1):
    COUNTS[key] = COUNTS.get(key, 0) + amount


def mul(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return out


def theta(a):
    return [i*x for i, x in enumerate(a)]


def evaluate(a, r):
    value = 0
    for x in reversed(a):
        value = value*r+x
    return value


def fold(a, ell):
    out = [0]*ell
    for i, x in enumerate(a):
        out[i % ell] += x
    return out


def decode(value, r, ell):
    modulus = r**ell-1
    value %= modulus
    if 2*value > modulus:
        value -= modulus
    out = []
    for _ in range(ell):
        digit = value % r
        if 2*digit >= r:
            digit -= r
        out.append(digit)
        value = (value-digit)//r
    assert value == 0
    return out


def recover_from_folds(triples, total, d, height):
    recovered = {}
    for ell, (u, v, w) in enumerate(triples, 1):
        for j, (mass, first, second) in enumerate(zip(u, v, w)):
            assert mass >= 0 and first >= 0 and second >= 0
            determinant = mass*second-first*first
            assert determinant >= 0
            count("checked_nonnegative_bucket_variances")
            if mass == 0:
                assert first == second == 0
                continue
            if determinant:
                continue
            assert first % mass == 0
            exponent = first//mass
            assert 0 <= exponent < d and exponent % ell == j
            assert mass <= height
            assert exponent not in recovered or recovered[exponent] == mass
            recovered[exponent] = mass
    assert sum(recovered.values()) <= total
    return recovered, sum(recovered.values()) == total


def core(a, b, c, bits, budget):
    d = len(c)
    height = len(a)*(1 << (2*bits)) + max(abs(x) for x in c)
    beta = (8*d**3*(height+1)).bit_length()
    radix = 1 << beta
    cap = 2*comb(budget, 2)*(d-1).bit_length()+4
    modulus = prod(radix**ell-1 for ell in range(1, cap+1))
    ar, br, cr = (evaluate(x, radix) % modulus for x in (a, b, c))
    ad, bd, cd = (evaluate(theta(x), radix) % modulus for x in (a, b, c))
    add, bdd, cdd = (evaluate(theta(theta(x)), radix) % modulus
                     for x in (a, b, c))
    residues = ((ar*br-cr) % modulus,
                (ad*br+ar*bd-cd) % modulus,
                (add*br+2*ad*bd+ar*bdd-cdd) % modulus)
    oracle = [x-y for x, y in zip(mul(a, b)+[0], c)]
    assert all(x >= 0 for x in oracle)
    derivatives = (oracle, theta(oracle), theta(theta(oracle)))
    triples = []
    for ell in range(1, cap+1):
        triple = tuple(decode(value, radix, ell) for value in residues)
        assert triple == tuple(fold(x, ell) for x in derivatives)
        triples.append(triple)
        count("decoded_three_moment_families")
    total = sum(a)*sum(b)-sum(c)
    recovered, accepted = recover_from_folds(triples, total, d, height)
    truth = {i: x for i, x in enumerate(oracle) if x}
    assert all(truth[i] == x for i, x in recovered.items())
    if accepted:
        assert recovered == truth
    if len(truth) <= budget:
        assert accepted
    return recovered, accepted, cap


def main():
    rng = random.Random(2026112506)
    for d in range(2, 8):
        for residual in product(range(3), repeat=d):
            derivatives = (residual, theta(residual), theta(theta(residual)))
            triples = [tuple(fold(x, ell) for x in derivatives)
                       for ell in range(1, 5)]
            for ell, (u, v, w) in enumerate(triples, 1):
                for j in range(ell):
                    support = [i for i, x in enumerate(residual)
                               if x and i % ell == j]
                    rhs = sum(residual[i]*residual[t]*(i-t)**2
                              for p, i in enumerate(support)
                              for t in support[p+1:])
                    assert u[j]*w[j]-v[j]*v[j] == rhs
                    assert (u[j] > 0 and rhs == 0) == (len(support) == 1)
                    count("exact_variance_identities")
            recovered, accepted = recover_from_folds(triples, sum(residual), d, 2)
            truth = {i: x for i, x in enumerate(residual) if x}
            assert all(truth[i] == x for i, x in recovered.items())
            if accepted:
                assert recovered == truth
            count("exhaustive_nonnegative_residuals")

    for h, bits, budget, actual_support in (
        (3, 2, 1, 1), (6, 3, 1, 8), (8, 4, 2, 2),
        (10, 3, 2, 7), (12, 4, 3, 3), (12, 2, 3, 9)):
        for _ in range(5):
            a = [rng.randrange(1 << bits) for _ in range(h)]
            b = [rng.randrange(1 << bits) for _ in range(h)]
            actual = mul(a, b)+[0]
            error = [0]*(2*h)
            for i in rng.sample(range(2*h), actual_support):
                error[i] = rng.randrange(1, 12)
            c = [x-y for x, y in zip(actual, error)]
            recovered, accepted, _ = core(a, b, c, bits, budget)
            count("modular_operand_product_cases")
            if actual_support > budget:
                count("deliberately_false_sparsity_guesses")
            count("accepted_cases" if accepted else "incomplete_budget_cases")

    error = [0]*12
    for i in (0, 2, 4, 5, 11):
        error[i] = 1
    _, accepted, cap = core([0]*6, [0]*6, [-x for x in error], 1, 1)
    assert cap == 4 and accepted
    assert all(len({i % ell for i, x in enumerate(error) if x}) < 5
               for ell in range(1, 5))
    count("union_isolation_without_full_single_modulus")

    _, accepted, _ = core([0]*6, [0]*6, [-1]*12, 1, 1)
    assert not accepted
    count("dense_positive_incomplete_control")

    error = [1, 0, 1]
    u, v, w = (fold(x, 1)[0] for x in (error, theta(error), theta(theta(error))))
    assert (u, v, w) == (2, 2, 4)
    assert v//u == 1 and u == sum(error) and u*w-v*v > 0
    count("first_derivative_only_false_candidate_rejected")

    j = [1]
    for ell in range(1, 5):
        j = mul(j, [-1]+[0]*(ell-1)+[1])
    signed_error = mul(mul(j, j), j)
    assert any(x < 0 for x in signed_error) and any(x > 0 for x in signed_error)
    assert sum(signed_error) == 0
    for derivative in (signed_error, theta(signed_error), theta(theta(signed_error))):
        for ell in range(1, 5):
            assert all(x == 0 for x in fold(derivative, ell))
            count("signed_false_certificate_zero_folds")
    count("rejected_unrestricted_signed_certificate_claim")

    result = {"status": "all exact finite controls passed", "seed": 2026112506,
              "scope": "certificate arithmetic; not a finite-tape timing simulation",
              "counts": COUNTS}
    Path(__file__).with_name("one-sided-certificate-verification.json").write_text(
        json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
