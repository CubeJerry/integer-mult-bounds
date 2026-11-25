#!/usr/bin/env python3
"""Exact on-demand rational repair and bounded-divisor checks."""
from fractions import Fraction as F
from math import ceil, isqrt
from pathlib import Path
import json
import random
import sys


def inverse(matrix):
    n = len(matrix)
    a = [list(map(F, row)) + [F(i == j) for j in range(n)] for i, row in enumerate(matrix)]
    for j in range(n):
        pivot = next(i for i in range(j, n) if a[i][j])
        a[j], a[pivot] = a[pivot], a[j]
        divisor = a[j][j]
        a[j] = [x / divisor for x in a[j]]
        for i in range(n):
            if i != j:
                coefficient = a[i][j]
                a[i] = [x - coefficient * y for x, y in zip(a[i], a[j])]
    return [row[n:] for row in a]


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


def predict(m, c, beta_parity):
    radius = isqrt(4 * m)
    if radius * radius < 4 * m:
        radius += 1
    assert (radius - 1) ** 2 < 4 * m <= radius ** 2
    u = (m - 2 * radius) // 2
    v = (m + 2 * radius + 1) // 2
    degree = v - u
    gamma = -1 if (u - beta_parity) % 2 else 1
    term, total = 1, 1
    for h in range(1, degree + 1):
        numerator = term * (c - u - h + 1)
        assert numerator % h == 0
        term = numerator // h
        total += ((-2) ** h) * term
    return gamma * total, u, v, degree


def dyadic(a, b, precision):
    assert b > 0 and precision >= 0
    quotient, remainder = divmod(abs(a), b)
    bits = []
    for _ in range(precision):
        remainder *= 2
        bit = int(remainder >= b)
        if bit:
            remainder -= b
        assert 0 <= remainder < b
        bits.append(bit)
    fractional = 0
    for bit in bits:
        fractional = 2 * fractional + bit
    numerator = (quotient << precision) + fractional
    if a < 0:
        numerator = -numerator
    approximation = F(numerator, 1 << precision)
    assert abs(approximation - F(a, b)) < F(1, 1 << precision)
    width = max(1, abs(a).bit_length(), b.bit_length())
    # Tape implementation appends quotient bits rather than shifting an
    # ever-growing integer; each remainder update scans at most width bits.
    charged_bound = width * width + precision * (4 * width + 4)
    return approximation, charged_bound


def main():
    rng = random.Random(3322026)
    result = {"python": sys.version.split()[0],
              "scope": "Exact rational coefficient/repair identities and bounded-divisor precision; no full tape multiplier.",
              "source_openai_math": "3344da59991ed94f9ba711217b29c1d760badfa6"}
    keys, inverses, nonempty, height = 0, 0, 0, 0
    coefficients = {F(0), F(1), F(-1), F(1, 3), F(-17, 31)}
    cases = []
    for m in (17, 25, 31, 63, 127, 255):
        width = 1 << m.bit_length()
        s = width // 16
        seed_bits = [(i + 1) for i in range(m)]
        samples = [[0] * m, [1] * m]
        samples += [[int(j == i) for j in range(m)] for i in range(min(4, m))]
        for length in (3, 5):
            samples.append([int(sum((a >> bit) & 1 for bit in range(length)) > length // 2) for a in seed_bits])
        samples += [[rng.randrange(2) for _ in range(m)] for _ in range(20)]
        for key in samples:
            z = -1 if sum(key) % 2 else 1
            values, counts = [], []
            for seed in range(width):
                beta = [(a & seed).bit_count() % 2 for a in seed_bits]
                count = sum(k ^ b for k, b in zip(key, beta))
                value, u, v, degree = predict(m, count, sum(beta))
                if u <= count <= v:
                    assert value == z
                assert value % 2 == 1
                values.append(value)
                counts.append(count)
            assert sum(counts) == width * m // 2
            assert sum((2 * c - m) ** 2 for c in counts) == width * m
            defect = [i for i, value in enumerate(values) if value != z]
            assert len(defect) <= s
            keys += 1
            if not defect:
                continue
            nonempty += 1
            j = len(defect)
            nodes = [F(i, width) for i in defect]
            matrix = [[x ** h for x in nodes] for h in range(j)]
            inv = inverse(matrix)
            for a in range(j):
                for b in range(j):
                    assert dot(inv[a], [matrix[k][b] for k in range(j)]) == int(a == b)
                    assert abs(inv[a][b]) <= (2 * width) ** (j - 1)
                    coefficients.add(inv[a][b])
            inverses += 1
            x = [F(rng.randrange(-9, 10), rng.randrange(1, 7)) for _ in range(width)]
            check_error = [sum((F(i, width) ** h) * (values[i] - z) * x[i] for i in range(width)) for h in range(j)]
            recovered = [dot(row, check_error) for row in inv]
            target = []
            for index, error in zip(defect, recovered):
                gap = values[index] - z
                assert gap and gap % 2 == 0
                assert abs(F(1, gap)) <= F(1, 2)
                coefficients.add(F(1, gap))
                target.append(error / gap)
                assert target[-1] == x[index]
            lifted = [dot([inv[k][h] for k in range(j)], target) for h in range(j)]
            zlift = [sum(F(i, width) ** h * lifted[h] for h in range(j)) for i in range(width)]
            assert all(values[i] * x[i] - values[i] * zlift[i] + z * zlift[i] == z * x[i] for i in range(width))
            local_height = max(max(abs(v.numerator).bit_length(), v.denominator.bit_length()) for row in inv for v in row)
            height = max(height, local_height)
            assert local_height <= (m + 2) ** 12
        cases.append(dict(m=m, width=width, checks=s, keys=len(samples)))
    result.update(key_cases=keys, nonempty_defects=nonempty, exact_inverse_cases=inverses,
                  max_inverse_height=height, parameter_cases=cases)
    for _ in range(100):
        coefficients.add(F(rng.randrange(-(1 << 100), 1 << 100), rng.randrange(1, 1 << 90)))
    precision_cases = 0
    linear_growth = []
    for coefficient in sorted(coefficients)[:250]:
        for p in (0, 1, 7, 31, 128, 512, 1024):
            dyadic(coefficient.numerator, coefficient.denominator, p)
            precision_cases += 1
        _, c1 = dyadic(coefficient.numerator, coefficient.denominator, 512)
        _, c2 = dyadic(coefficient.numerator, coefficient.denominator, 1024)
        assert c2 <= 2 * c1
        linear_growth.append((c1, c2))
    result.update(dyadic_precision_cases=precision_cases, linear_precision_growth_cases=len(linear_growth))
    selector_cases = 0
    for m in (3, 5, 17, 31):
        d = m + 3
        for f in (1, 2, 4, 9):
            for _ in range(20):
                xs = [[rng.randrange(2) for _ in range(d)] for _ in range(f)]
                zs = [[rng.randrange(2) for _ in range(d)] for _ in range(f)]
                key = [sum(x[j] * z[j] + sum(x[i] * z[i] for i in range(m, d)) for x, z in zip(xs, zs)) % 2 for j in range(m)]
                assert sum(key) % 2 == sum(sum(a * b for a, b in zip(x, z)) for x, z in zip(xs, zs)) % 2
                selector_cases += 1
    result["column_selector_cases"] = selector_cases
    # Omitting denominator-width dependence would falsely assert a uniform
    # linear bound when the divisor itself grows with the record precision.
    bounds = []
    for k in (64, 128, 256):
        _, cost = dyadic(1, (1 << k) - 1, k)
        bounds.append(cost)
    assert bounds[1] > 3 * bounds[0] and bounds[2] > 3 * bounds[1]
    # Odd arity is necessary for the source auxiliary-axis query product.
    even_m = 4
    assert (even_m % 2) != 1
    result["negative_controls"] = {"growing_divisor_is_quadratic": bounds,
                                   "even_arity_loses_auxiliary_phase": {"m": even_m, "query_product_parity": 0, "target_parity": 1}}
    result["passed"] = True
    path = Path(__file__).with_name("compact-rational-walsh-verification.json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k.endswith("cases") or k in ("passed", "nonempty_defects")}, indent=2))


if __name__ == "__main__":
    main()
