#!/usr/bin/env python3
"""Exact finite checks for Route A's lemmas; not an asymptotic proof."""

from fractions import Fraction as F
from itertools import combinations
from math import comb, factorial, gcd, isqrt
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


def check_interchange_log_majorants():
    """Check q-free factors without constructing q, m or a template.

    The universal proof absorbs any fixed absolute pencil/stage constant.
    The 2**32 prefactor below is a generous finite arithmetic control, not
    a claim that the entire physical compiler has this particular constant.
    """
    rows = []
    for p in (29, 31, 43, 61, 101, 149, 211):
        assert all(p % divisor for divisor in range(2, isqrt(p)+1))
        h = 2*p-1
        r = ((64*p)**(64*p)-1).bit_length()
        rank_coefficient = (1+h**(p-1))**(p+1)
        binomial_majorant = 2**(h*(p+1))
        assert comb(h, p)**(p+1) <= binomial_majorant
        prefix = 2**32*(2*p+1)*binomial_majorant*rank_coefficient*r**(p*(p-1))
        square_prefix = prefix**2*(1+p*p*r)
        # 64*prefix**2*(1+p**2*r) < 2**(6*p*r).
        # Compare integer bit lengths; the huge right-hand value is absent.
        assert (64*square_prefix).bit_length() <= 6*p*r
        assert p*p >= 6*h  # (1/2)p**2-h >= p**2/3.
        assert 3*(8*h).bit_length() <= r*p*p
        assert 6*p*r >= 3  # m**(epsilon/2) >= 8 if epsilon*p >= 12.
        rows.append({
            "p": p, "r": r, "log2_m": r*p*p,
            "q_free_square_majorant_bits": square_prefix.bit_length(),
            "available_margin_bits": 6*p*r,
            "m_materialized": False,
        })
    return rows


def check_cyclotomic_units():
    cases = 0
    for prime in (3, 5, 7):
        for order in (4, 8, 16):
            degree = order//2

            def monomial(exponent):
                exponent %= order
                result = [0]*degree
                result[exponent % degree] = (-1 if exponent >= degree else 1) % prime
                return result

            def multiply(left, right):
                result = [0]*degree
                for a, av in enumerate(left):
                    for b, bv in enumerate(right):
                        result[(a+b) % degree] += av*bv*(-1 if a+b >= degree else 1)
                return [v % prime for v in result]

            def add(left, right):
                return [(a+b) % prime for a, b in zip(left, right)]

            for first in range(order):
                for second in range(order):
                    if first == second:
                        continue
                    difference = [(a-b) % prime for a, b in zip(monomial(first), monomial(second))]
                    exponent = (first-second) % order
                    half_order = order//gcd(exponent, order)//2
                    geometric = [0]*degree
                    for j in range(half_order):
                        geometric = add(geometric, monomial(exponent*j))
                    inverse = multiply(monomial(-second), geometric)
                    inverse = [(-pow(2, -1, prime)*a) % prime for a in inverse]
                    assert multiply(difference, inverse) == monomial(0)
                    cases += 1
    return {"unit_difference_identities": cases, "rings_are_not_assumed_fields": True}


def check_integral_predictor_specialization():
    cases = 0
    collision_seen = False
    for prime, m, low, high in ((3, 5, 1, 4), (5, 8, 1, 6)):
        degree = high-low
        for mask in range(2**m):
            bits = [(mask >> j) & 1 for j in range(m)]
            coeff = [generalized_binomial(-low, h) % prime for h in range(degree+1)]
            for bit in bits:
                for h in range(degree, 0, -1):
                    coeff[h] = (coeff[h]+bit*coeff[h-1]) % prime
            result = ((-1)**low * sum((-2)**h * coeff[h] for h in range(degree+1))) % prime
            count = sum(bits)
            if low <= count <= high:
                assert result == (-1)**count % prime
                cases += 1
        assert low % prime == (low+prime) % prime
        assert (-1)**low % prime != (-1)**(low+prime) % prime
        collision_seen = True
    return {"correct_specialized_window_values": cases, "field_count_collision_control": collision_seen}


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
        "interchange_log_majorants": check_interchange_log_majorants(),
        "cyclotomic_basis": check_cyclotomic_units(),
        "integral_specialization": check_integral_predictor_specialization(),
        "global_tower_status": "Written mathematical implementation and independent internal review completed; the asymptotic theorem is not established by these finite tests.",
        "proof_sha256": {
            path.name: hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(root.glob("*.md"))
        },
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
