"""Finite exact algebra checks; not an asymptotic or tape-time proof.

Uses Z[z]/(z^2-z+1). The regular representation is tested modulo 3,
where the algebra is nonreduced and the order-three root nonsemisimple.
"""

from dataclasses import dataclass
from itertools import product
from math import comb
import json
from pathlib import Path

ZERO, ONE, ROOT = (0, 0), (1, 0), (0, 1)


def ra(x, y):
    return x[0] + y[0], x[1] + y[1]


def rm(x, y):
    a, b = x
    c, d = y
    return a * c - b * d, a * d + b * c + b * d


def rp(x, n):
    out = ONE
    for _ in range(n):
        out = rm(out, x)
    return out


def eye(n):
    return [[ONE if i == j else ZERO for j in range(n)] for i in range(n)]


def mm(a, b):
    n = len(a)
    out = [[ZERO for _ in range(n)] for _ in range(n)]
    nz = [[(j, v) for j, v in enumerate(row) if v != ZERO] for row in b]
    for i, row in enumerate(a):
        for k, v in enumerate(row):
            if v != ZERO:
                for j, w in nz[k]:
                    out[i][j] = ra(out[i][j], rm(v, w))
    return out


def scalar_identity(a, value):
    return all(v == ((value, 0) if i == j else ZERO)
               for i, row in enumerate(a) for j, v in enumerate(row))


def ti(a, n):
    k = len(a)
    out = [[ZERO for _ in range(k * n)] for _ in range(k * n)]
    for i in range(k):
        for j in range(k):
            for r in range(n):
                out[i * n + r][j * n + r] = a[i][j]
    return out


def it(n, a):
    k = len(a)
    out = [[ZERO for _ in range(k * n)] for _ in range(k * n)]
    for r in range(n):
        for i in range(k):
            for j in range(k):
                out[r * k + i][r * k + j] = a[i][j]
    return out


@dataclass
class Factor:
    matrices: list
    constant: int | None = None

    @property
    def degree(self):
        return len(self.matrices)

    @property
    def rank(self):
        return len(self.matrices[0]) if self.matrices else 1


def constant(c):
    return Factor([], c)


def scale(f, c):
    if not f.degree:
        return constant(f.constant * c)
    matrices = list(f.matrices)
    matrices[0] = [[rm((c, 0), x) for x in row] for row in matrices[0]]
    return Factor(matrices)


def elementary(values, degree):
    if degree == 0:
        return constant(1)
    if len(values) == 1:
        assert degree == 1
        return Factor([[[(values[0], 0)]]])
    cut = len(values) // 2
    left, right = values[:cut], values[cut:]
    terms = [multiply(elementary(left, r), elementary(right, degree - r))
             for r in range(max(0, degree - len(right)), min(degree, len(left)) + 1)]
    result = terms[0]
    for term in terms[1:]:
        result = add(result, term)
    return result


def coefficients(u, degree):
    def negative_binomial(t):
        return int(t == 0) if u == 0 else (-1) ** t * comb(u + t - 1, t)
    return [(-1) ** u * sum((-2) ** h * negative_binomial(h - a)
                           for h in range(a, degree + 1))
            for a in range(degree + 1)]


def predictor(values, u, v):
    coeff = coefficients(u, v - u)
    f = constant(coeff[0])
    for a in range(1, len(coeff)):
        f = add(f, scale(elementary(values, a), coeff[a]))
    symmetric = [1] + [0] * len(values)
    for value in values:
        for a in range(len(values), 0, -1):
            symmetric[a] += value * symmetric[a - 1]
    return f, sum(c * e for c, e in zip(coeff, symmetric))


def cyclic_products(f):
    for start in range(f.degree):
        result = eye(f.rank)
        for step in range(f.degree):
            result = mm(f.matrices[(start - step) % f.degree], result)
        yield result


def block_cycle(f):
    b = 2
    while b < f.degree:
        b *= 2
    f = pad(f, b)
    k = f.rank
    out = [[ZERO for _ in range(b * k)] for _ in range(b * k)]
    for grade, factor in enumerate(f.matrices):
        for i in range(k):
            for j in range(k):
                out[((grade - 1) % b) * k + i][grade * k + j] = factor[i][j]
    return out, b


def descend(a):
    n = len(a)
    out = [[0 for _ in range(2 * n)] for _ in range(2 * n)]
    for i, row in enumerate(a):
        for j, (c, d) in enumerate(row):
            out[2 * i][2 * j], out[2 * i][2 * j + 1] = c, -d
            out[2 * i + 1][2 * j], out[2 * i + 1][2 * j + 1] = d, c + d
    return out


def integer_mm(a, b, modulus):
    n = len(a)
    out = [[0 for _ in range(n)] for _ in range(n)]
    nz = [[(j, v) for j, v in enumerate(row) if v] for row in b]
    for i, row in enumerate(a):
        for k, v in enumerate(row):
            if v:
                for j, w in nz[k]:
                    out[i][j] += v * w
    if modulus:
        out = [[v % modulus for v in row] for row in out]
    return out


def root_check(f, expected, modulus):
    root, exponent = block_cycle(f)
    root = descend(root)
    n = len(root)
    out = [[int(i == j) for j in range(n)] for i in range(n)]
    for _ in range(exponent):
        out = integer_mm(root, out, modulus)
    for i, row in enumerate(out):
        for j, value in enumerate(row):
            target = expected if i == j else 0
            assert value == (target % modulus if modulus else target)
    return n


def pad(f, d):
    if not f.degree:
        return Factor([[[(f.constant, 0)]]] + [eye(1) for _ in range(d - 1)])
    return Factor(f.matrices + [eye(f.rank) for _ in range(d - f.degree)])


def multiply(f, g):
    if not f.degree:
        return scale(g, f.constant)
    if not g.degree:
        return scale(f, g.constant)
    return Factor([ti(a, g.rank) for a in f.matrices]
                  + [it(f.rank, b) for b in g.matrices])


def add(f, g, wrong_phase=False):
    if not f.degree and not g.degree:
        return constant(f.constant + g.constant)
    d = max(f.degree, g.degree)
    assert d in (1, 2, 3)
    f, g = pad(f, d), pad(g, d)
    a, b = f.rank, g.rank
    block = a * b
    phase = ONE if wrong_phase else rp(ROOT, 6 // d)
    matrices = []
    for k in range(d):
        mat = [[ZERO for _ in range(d * block)] for _ in range(d * block)]
        for i in range(d):
            j = (k - i) % d
            left, right = ti(f.matrices[i], b), it(a, g.matrices[j])
            weight = rp(phase, i)
            for r in range(block):
                for s in range(block):
                    row, col = ((i - 1) % d) * block + r, i * block + s
                    mat[row][col] = ra(mat[row][col], left[r][s])
                    row = i * block + r
                    mat[row][col] = ra(mat[row][col], rm(weight, right[r][s]))
        matrices.append(mat)
    return Factor(matrices)


def main():
    cases = cycles = roots = 0
    max_dimension = 0
    for m in (2, 3):
        for u in range(m):
            for v in range(u + 1, m + 1):
                for values in product((0, 1), repeat=m):
                    f, expected = predictor(values, u, v)
                    assert f.degree == v - u
                    for result in cyclic_products(f):
                        assert scalar_identity(result, expected)
                        cycles += 1
                    if u <= sum(values) <= v:
                        assert expected == (-1) ** sum(values)
                    cases += 1
    for u, v in ((0, 2), (1, 3), (0, 3)):
        for beta in product((0, 1), repeat=3):
            values = tuple(1 - a if shift else a
                           for a, shift in zip((2, -1, 3), beta))
            f, expected = predictor(values, u, v)
            sign = (-1) ** sum(beta)
            f, expected = scale(f, sign), expected * sign
            for result in cyclic_products(f):
                assert scalar_identity(result, expected)
                cycles += 1
            for modulus in (None, 3, 5):
                max_dimension = max(max_dimension, root_check(f, expected, modulus))
                roots += 1
            cases += 1
    f = Factor([[[(2, 0)]], [[(3, 0)]]])
    g = Factor([[[(5, 0)]], [[(7, 0)]]])
    bad = add(f, g, wrong_phase=True)
    assert any(not scalar_identity(a, 41) for a in cyclic_products(bad))
    # At p=3, z^2 is nontrivial unipotent, not the scalar 1.
    z2 = descend([[rp(ROOT, 2)]])
    assert [[x % 3 for x in row] for row in z2] != [[1, 0], [0, 1]]
    nil = [[(z2[i][j] - int(i == j)) % 3 for j in range(2)] for i in range(2)]
    assert integer_mm(nil, nil, 3) == [[0, 0], [0, 0]]
    receipt = {
        "status": "passed",
        "scope": "finite exact cyclic-factor and full-coordinate matrix-root checks only",
        "coefficient_ring": "Z[z]/(z^2-z+1), regular representation over Z, F_3 and F_5",
        "predictor_cases": cases,
        "all_cyclic_product_checks": cycles,
        "full_regular_matrix_root_checks": roots,
        "largest_descended_dimension": max_dimension,
        "wrong_phase_negative_controls": 1,
        "nonsemisimple_characteristic_three_controls": 1,
        "not_established": ["asymptotic generator bound", "complete tape complexity", "endpoint time"],
    }
    Path(__file__).with_name("formula-factorization-verification.json").write_text(
        json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
