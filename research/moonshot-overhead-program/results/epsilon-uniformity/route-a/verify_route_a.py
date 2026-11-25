#!/usr/bin/env python3
"""Exact finite checks for Route A's lemmas; not an asymptotic proof."""

from fractions import Fraction as F
from itertools import combinations
from math import comb, factorial
import hashlib
import json
from pathlib import Path


def poly_mul_linear(poly, root):
    out = [0] * (len(poly) + 1)
    for i, value in enumerate(poly):
        out[i] -= root * value
        out[i + 1] += value
    return out


def inverse_vandermonde(nodes):
    rows = []
    for node in nodes:
        poly, denominator = [1], 1
        for other in nodes:
            if other != node:
                poly = poly_mul_linear(poly, other)
                denominator *= node - other
        rows.append([F(x, denominator) for x in poly])
    return rows


def matvec(matrix, vector):
    return [sum((a * b for a, b in zip(row, vector)), F(0)) for row in matrix]


def check_repair():
    cases = 0
    max_numerator_bits = 0
    for size in range(2, 10):
        common = 2 * factorial(size - 1) ** 4
        for count in range(1, min(4, size) + 1):
            for nodes in combinations(range(1, size + 1), count):
                inv = inverse_vandermonde(nodes)
                vandermonde = [[F(node**a) for node in nodes] for a in range(count)]
                for column in range(count):
                    basis = [F(int(i == column)) for i in range(count)]
                    assert matvec(inv, matvec(vandermonde, basis)) == basis
                for z in (-1, 1):
                    p = [z] * size
                    for node in nodes:
                        p[node - 1] = 3 * node - 5 * z
                    diag = [F(-(p[node - 1] + 2 * z), 2) for node in nodes]
                    kernel = [
                        [sum((inv[i][a] * diag[i] * inv[i][b] for i in range(count)), F(0))
                         for b in range(count)] for a in range(count)
                    ]
                    for row in kernel:
                        for entry in row:
                            numerator = entry * common
                            assert numerator.denominator == 1
                            max_numerator_bits = max(max_numerator_bits, abs(numerator.numerator).bit_length())
                    x = [F((-1)**i * (i + 1)**2, i + 2) for i in range(size)]
                    checks = [[F(node**a) for node in range(1, size + 1)] for a in range(count)]
                    discrepancy = matvec(checks, [(pi-z)*xi for pi, xi in zip(p, x)])
                    repair = matvec(kernel, discrepancy)
                    lifted = [sum((F(node**a)*repair[a] for a in range(count)), F(0))
                              for node in range(1, size+1)]
                    out = [F(3*pi-pi**3, 2)*xi - pi*li + z*li
                           for pi, xi, li in zip(p, x, lifted)]
                    assert out == [z*xi for xi in x]
                    cases += 1
    return {"cases": cases, "max_numerator_bits_observed": max_numerator_bits,
            "includes_overmarked_exceptions": True}


def generalized_binomial(t, degree):
    value = F(1)
    for h in range(1, degree+1):
        value *= F(t-h+1, h)
    assert value.denominator == 1
    return value.numerator


def check_predictor_values():
    cases = 0
    for m in range(2, 35):
        for u in range(m):
            for v in {u+1, min(m, u+3), m}:
                degree = v-u
                for count in range(m+1):
                    value = (-1)**u * sum((-2)**h * generalized_binomial(count-u, h)
                                         for h in range(degree+1))
                    assert abs(value) <= (4*m)**(degree+1)
                    if u <= count <= v:
                        assert value == (-1)**count
                    cases += 1
    return {"integer_count_cases": cases}


def parity_error(m, p):
    signed = [0] * p
    for count in range(m+1):
        signed[count % p] += (-1)**count * comb(m, count)
    return F(2**m-sum(abs(x) for x in signed), 2**(m+1))


def check_modular_obstruction():
    rows = []
    for p in (3, 5, 7, 11, 17):
        # This integer threshold is larger than the analytic threshold.
        m = p*p*(4*p).bit_length()
        error = parity_error(m, p)
        assert error >= F(1, 4)
        assert parity_error(1, p) == 0  # Required small-m negative control.
        rows.append({"p": p, "m": m, "error_at_least_quarter": True,
                     "exact_error_numerator_bits": error.numerator.bit_length()})
    return rows


def check_integer_parameters():
    rows = []
    for t in (8, 9, 12, 16, 20, 32, 40, 80, 160, 400):
        power = (16*t)**(16*t)
        r = (power-1).bit_length()  # Exact ceil(16t log_2(16t)).
        z = t*r
        assert 2**r >= power
        assert 1+r <= (16*t)**2
        assert z+1 <= 2*t*(1+r)
        assert (2304*t)**2*(z+1)*(1+r)**(4*t) <= (16*t)**(12*t)
        assert 2**(t-1) >= 2*t+1
        rows.append({"t": t, "r": r, "log2_m_plus_1": z,
                     "log2_W": 6*z*z+6*z})
    return rows


def main():
    root = Path(__file__).resolve().parent
    result = {
        "scope": "Exact finite identity checks and integer boundary controls; universal claims are proved in Markdown.",
        "source_math_sha": "3344da59991ed94f9ba711217b29c1d760badfa6",
        "compact_predictor_checkpoint": "bbfd1086b7e629375f9891998e4602270d8801cd",
        "repair": check_repair(),
        "predictor": check_predictor_values(),
        "modular_obstruction": check_modular_obstruction(),
        "integer_parameters": check_integer_parameters(),
        "proof_sha256": {
            path.name: hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(root.glob("*.md"))
        },
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
