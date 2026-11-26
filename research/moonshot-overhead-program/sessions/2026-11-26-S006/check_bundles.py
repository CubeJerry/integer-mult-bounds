"""Exact finite cross-check of stable additive bundles; dense small oracles only."""

from math import gcd
from random import Random


def span(basis):
    elements = [0]
    for member in basis:
        elements += [x ^ member for x in elements]
    return elements


def kernel(images):
    pivots = {}
    answer = []
    for index, image in enumerate(images):
        preimage = 1 << index
        while image:
            slot = image.bit_length()
            if slot not in pivots:
                pivots[slot] = (image, preimage)
                break
            row, combination = pivots[slot]
            image ^= row
            preimage ^= combination
        if image == 0:
            answer.append(preimage)
    return answer


def column_orbits(width):
    """Compressed real cyclotomic basis r1,...,r_(b-1),1."""
    b = width
    polynomial = (1 << (2 * b)) | (1 << b) | 1
    one = 1 << (b - 1)
    columns = [(1 << j) ^ (1 << (2 * b - j)) ^ (1 << (b - j))
               for j in range(1, b)] + [1]

    def embed(x):
        out = 0
        while x:
            term = x & -x
            out ^= columns[term.bit_length() - 1]
            x ^= term
        return out

    def project(x):
        out = one if x & 1 else 0
        for j in range(1, b):
            out |= ((x >> (2 * b - j)) & 1) << (j - 1)
        assert embed(out) == x
        return out

    def multiply(x, y):
        p = 0
        left, right = embed(x), embed(y)
        while right:
            if right & 1:
                p ^= left
            left <<= 1
            right >>= 1
        # Independent long reduction in the ambient binary field.
        while p.bit_length() > 2 * b:
            p ^= polynomial << (p.bit_length() - 1 - 2 * b)
        return project(p)

    square_columns = [multiply(1 << i, 1 << i) for i in range(b)]

    def square(x):
        out = 0
        while x:
            bit = x & -x
            out ^= square_columns[bit.bit_length() - 1]
            x ^= bit
        return out

    def frobenius(x, count):
        for _ in range(count):
            x = square(x)
        return x

    def inv(x):
        assert x
        # Invert using x^(2^b-2), with unit and sign conventions explicit.
        y = one
        for bit in bin((1 << b) - 2)[2:]:
            y = square(y)
            if bit == "1":
                y = multiply(y, x)
        assert multiply(x, y) == one
        return y

    return one, multiply, square, frobenius, inv


def check_neighboring_stages(b, one, mul, square, inv, basis, reps, values):
    """Evaluate every adjacent basis level, then reconstruct in reverse."""
    dimension = len(basis)
    size = 1 << dimension
    directions = span(basis)

    # The small oracle constructs the subspace polynomials independently as
    # products over their roots, not by the executor's additivity recurrence.
    def subspace_value(x, level):
        acc = one
        for root in directions[:1 << level]:
            acc = mul(acc, x ^ root)
        return acc

    tables = [[subspace_value(x, j) for x in range(1 << b)] for j in range(dimension)]
    deltas = [tables[j][basis[j]] for j in range(dimension)]
    reciprocals = [inv(delta) for delta in deltas]
    for j in range(dimension - 1):
        assert all(tables[j+1][x] == square(tables[j][x]) ^ mul(deltas[j], tables[j][x])
                   for x in range(1 << b))

    def verify_stream(stream, alpha, level):
        width = 1 << level
        for offset in range(0, size, width):
            coeffs = stream[offset:offset+width]
            for address in range(offset, offset+width):
                x = alpha ^ directions[address]
                # Direct evaluation in the global binary-product basis.
                basis_values = [one]
                for j in range(level):
                    term = tables[j][x]
                    basis_values += [mul(term, v) for v in basis_values]
                y = 0
                for coeff, term in zip(coeffs, basis_values):
                    y ^= mul(coeff, term)
                assert y == values[x]

    def layer(stream, alpha, j, inverse):
        half = 1 << j
        out = []
        for offset in range(0, size, 2*half):
            a = alpha ^ directions[offset]
            t = tables[j][a]
            first = stream[offset:offset+half]
            second = stream[offset+half:offset+2*half]
            low, high = [], []
            for x, y in zip(first, second):
                if inverse:
                    v = mul(x ^ y, reciprocals[j])
                    low.append(x ^ mul(t, v))
                    high.append(v)
                else:
                    u = x ^ mul(t, y)
                    low.append(u)
                    high.append(u ^ mul(deltas[j], y))
            out += low + high
        return out

    for alpha in reps:
        leaves = [values[alpha ^ p] for p in directions]
        levels = [leaves]
        for j in range(dimension):
            parent = layer(levels[-1], alpha, j, True)
            verify_stream(parent, alpha, j+1)
            levels.append(parent)
        run = levels[-1]
        for j in reversed(range(dimension)):
            run = layer(run, alpha, j, False)
            assert run == levels[j]
        assert run == leaves
    print(f"  {dimension} consecutive layers in both directions on {len(reps)} bundles; "
          "every intermediate polynomial checked on all of its roots")


def check_degree(b):
    c = b // 3
    one, mul, sq, frob, inv = column_orbits(b)
    rel = lambda x: x ^ frob(x, c) ^ frob(x, 2 * c)

    def subfield_and_trace(x):
        total, point = 0, x
        for _ in range(c):
            total ^= point
            point = sq(point)
        return (total << b) ^ (point ^ x)

    ker = kernel([rel(1 << i) for i in range(b)])
    complement = kernel([subfield_and_trace(1 << i) for i in range(b)])
    assert len(ker) == 2 * c and len(complement) == c - 1
    eta = ker[0]
    assert eta != one and frob(eta, b) == eta and frob(eta, c) != eta
    assert b - len(kernel([frob(eta, i) for i in range(b)])) == 2 * c
    quotient = sorted(span(complement))
    reps = [x for x in quotient if x == min(frob(x, i) for i in range(c))]
    expected = sum(1 << (gcd(i, c) - 1) for i in range(c)) // c
    assert len(reps) == expected
    slots = (1 << (2 * c + 1)) * expected
    print(f"b={b} dim(V)={2*c + 1} quotient={len(quotient)} orbits={expected} "
          f"canonical_bits={b * slots} ratio={b * slots / (1 << b):g}")
    if b > 9:
        return

    q = 1 << b
    rng = Random(20261126 + b)
    coeffs = [rng.randrange(2) for _ in range(q)]
    values = []
    for z in range(q):
        y = 0
        for a in reversed(coeffs):
            y = mul(z, y) ^ (one if a else 0)
        values.append(y)
    assert all(values[sq(z)] == sq(values[z]) for z in range(q))
    icoef = inv(eta ^ sq(eta))

    def lagrange(points):
        # Direct Lagrange monomial interpolation, independently of the butterfly.
        result = [0] * len(points)
        for j, x in enumerate(points):
            polynomial, den = [one], one
            for i, y in enumerate(points):
                if i == j:
                    continue
                den = mul(den, x ^ y)
                nxt = [0] * (len(polynomial) + 1)
                for t, val in enumerate(polynomial):
                    nxt[t] ^= mul(val, y)
                    nxt[t + 1] ^= val
                polynomial = nxt
            scalar = mul(inv(den), values[x])
            for t, val in enumerate(polynomial):
                result[t] ^= mul(scalar, val)
        return result

    reconstructed = {}
    checks = 0
    for alpha in reps:
        local = {}
        # one and eta are the first directions; the other kernel vectors
        # sweep the four-point cosets of the chosen V-bundle.
        for nu in span(ker[1:]):
            a = alpha ^ nu
            points = [a, a ^ one, a ^ eta, a ^ eta ^ one]
            l0, l1, l2, l3 = lagrange(points)
            p1 = (l2 ^ l3, l3)
            p0 = (l0, l1 ^ p1[0])
            t0, t1 = sq(a) ^ a, sq(a ^ eta) ^ (a ^ eta)
            rows = [tuple(x ^ mul(t, y) for x, y in zip(p0, p1))
                    for t in (t0, t1)]
            assert [list(row) for row in rows] == [lagrange(points[:2]), lagrange(points[2:])]
            p1back = tuple(mul(x ^ y, icoef) for x, y in zip(*rows))
            p0back = tuple(x ^ mul(t0, y) for x, y in zip(rows[0], p1back))
            assert (p0back, p1back) == (p0, p1)
            for j, point in enumerate(points):
                low, high = rows[j // 2]
                local[point] = low ^ mul(point, high)
            checks += 1
        # Copy conjugate points to the omitted bundles; the ring arithmetic
        # must agree when a bundle orbit is shorter than the field degree.
        for z0, y0 in local.items():
            z, y = z0, y0
            for _ in range(b):
                assert z not in reconstructed or reconstructed[z] == y
                reconstructed[z] = y
                z, y = sq(z), sq(y)
    assert reconstructed == dict(enumerate(values))
    print(f"  {checks} forward/inverse four-point records; recovered all {q} binary-polynomial evaluations")
    check_neighboring_stages(b, one, mul, sq, inv, [one] + ker, reps, values)


if __name__ == "__main__":
    for degree in (3, 9, 27):
        check_degree(degree)
